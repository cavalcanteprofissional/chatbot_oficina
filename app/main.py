"""Aplicação Streamlit para o Chatbot da Oficina."""
import warnings
warnings.filterwarnings("ignore")

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from src.chatbot_oficina.rag.loader import load_documents, split_documents
from src.chatbot_oficina.rag.vectorstore import create_embeddings, create_vectorstore, load_vectorstore
from src.chatbot_oficina.chat.model import get_llm
from src.chatbot_oficina.rag.chain import create_rag_chain
from src.chatbot_oficina.guards.topic_validator import validate_topic
from src.chatbot_oficina.guards.injection_detector import detect_injection
from src.chatbot_oficina.database.repository import (
    identificar_ou_criar_cliente, salvar_conversa, buscar_cliente_por_telefone
)


DATA_PATH = "data/documentos"
CHROMA_PATH = "data/chroma_db"


@st.cache_resource
def initialize_rag():
    """Inicializa o sistema RAG."""
    embeddings = create_embeddings()
    
    vectorstore = load_vectorstore(embeddings, CHROMA_PATH)
    
    if vectorstore is None:
        documents = load_documents(DATA_PATH)
        chunks = split_documents(documents)
        vectorstore = create_vectorstore(chunks, embeddings, CHROMA_PATH)
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = get_llm()
    rag_chain = create_rag_chain(llm, retriever)
    
    return rag_chain


st.set_page_config(
    page_title="Chatbot - AutoCare Oficina",
    page_icon="🚗",
    initial_sidebar_state="expanded"
)


st.title("🚗 Chatbot - AutoCare Oficina")
st.markdown("Bem-vindo! Sou o assistente virtual da AutoCare. Como posso ajudar você hoje?")


# Inicializar sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

if "cliente_id" not in st.session_state:
    st.session_state.cliente_id = None
    st.session_state.cliente_nome = None
    st.session_state.cliente_telefone = None

# ============================================
# SIDEBAR - Login / Identificação
# ============================================
with st.sidebar:
    st.header("🔐 Identificação")
    
    if st.session_state.cliente_id is None:
        # Cliente não logado - mostrar formulário de login
        telefone_input = st.text_input("Telefone", placeholder="(11) 99999-9999", key="telefone_login")
        
        if st.button("Entrar", key="btn_entrar"):
            if telefone_input:
                # Buscar cliente por telefone
                try:
                    cliente = buscar_cliente_por_telefone(telefone_input)
                    if cliente:
                        # Cliente encontrado - login automático
                        st.session_state.cliente_id = cliente["id"]
                        st.session_state.cliente_nome = cliente["nome"]
                        st.session_state.cliente_telefone = telefone_input
                        st.rerun()
                    else:
                        # Cliente não encontrado
                        st.error("Telefone não cadastrado!")
                        st.session_state.telefone_para_cadastro = telefone_input
                        st.rerun()
                except Exception as e:
                    st.error(f"Erro ao buscar cliente: {str(e)}")
            else:
                st.warning("Informe seu telefone")
        
        # Se tem telefone para cadastro (não encontrou)
        if "telefone_para_cadastro" in st.session_state:
            st.markdown("---")
            st.markdown("### 📝 Cadastro Rápido")
            st.write(f"Telefone: {st.session_state.telefone_para_cadastro}")
            
            nome_cadastro = st.text_input("Seu nome", placeholder="Seu nome completo", key="nome_cadastro")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Cadastrar", key="btn_cadastrar"):
                    if nome_cadastro:
                        try:
                            cliente = identificar_ou_criar_cliente(
                                st.session_state.telefone_para_cadastro, 
                                nome_cadastro
                            )
                            if cliente:
                                st.session_state.cliente_id = cliente["id"]
                                st.session_state.cliente_nome = cliente["nome"]
                                st.session_state.cliente_telefone = st.session_state.telefone_para_cadastro
                                if "telefone_para_cadastro" in st.session_state:
                                    del st.session_state.telefone_para_cadastro
                                st.rerun()
                            else:
                                st.error("Erro ao cadastrar")
                        except Exception as e:
                            st.error(f"Erro: {str(e)}")
                    else:
                        st.warning("Informe seu nome")
            
            with col2:
                if st.button("Usar sem cadastro", key="btn_sem_cadastro"):
                    st.session_state.cliente_id = 0  # Anônimo
                    st.session_state.cliente_nome = "Cliente"
                    st.session_state.cliente_telefone = st.session_state.get("telefone_para_cadastro", "")
                    if "telefone_para_cadastro" in st.session_state:
                        del st.session_state.telefone_para_cadastro
                    st.rerun()
    else:
        # Cliente logado
        st.success(f"✅ Olá, {st.session_state.get('cliente_nome', 'Cliente')}!")
        if st.session_state.get("cliente_telefone"):
            st.caption(f"📱 {st.session_state.cliente_telefone}")
        
        if st.button("Sair"):
            st.session_state.cliente_id = None
            st.session_state.cliente_nome = None
            st.session_state.cliente_telefone = None
            st.session_state.messages = []
            st.rerun()

# ============================================
# ÁREA PRINCIPAL - Chat
# ============================================

# Mostrar mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do chat
if prompt := st.chat_input("Digite sua mensagem..."):
    # Verificar prompt injection primeiro
    is_injection, msg_injection = detect_injection(prompt)
    if is_injection:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "assistant", "content": msg_injection})
        with st.chat_message("assistant"):
            st.markdown(msg_injection)
        
        # Salvar no banco se cliente logado
        if st.session_state.get("cliente_id") and st.session_state.cliente_id > 0:
            try:
                salvar_conversa(st.session_state.cliente_id, prompt, msg_injection)
            except:
                pass
        
        st.rerun()
    
    # Verificar se o tema é válido
    is_valid, msg_topic = validate_topic(prompt)
    if not is_valid:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "assistant", "content": msg_topic})
        with st.chat_message("assistant"):
            st.markdown(msg_topic)
        
        # Salvar no banco se cliente logado
        if st.session_state.get("cliente_id") and st.session_state.cliente_id > 0:
            try:
                salvar_conversa(st.session_state.cliente_id, prompt, msg_topic)
            except:
                pass
        
        st.rerun()
    
    # Processar mensagem normalmente
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                rag_chain = initialize_rag()
                response = rag_chain.invoke(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Salvar no banco de dados se cliente logado
                if st.session_state.get("cliente_id") and st.session_state.cliente_id > 0:
                    try:
                        salvar_conversa(st.session_state.cliente_id, prompt, response)
                    except Exception as e:
                        st.warning(f"Erro ao salvar conversa: {e}")
                        
            except Exception as e:
                error_msg = f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(e)}"
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# ============================================
# SIDEBAR - Informações Adicionais
# ============================================
with st.sidebar:
    st.markdown("---")
    st.header("Sobre")
    st.info("""
    **AutoCare Oficina**
    
    Especialistas em manutenção automotiva
    
    📞 (11) 99999-9999
    📍 Rua das Oficinas, 123
    """)
    
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Dúvidas Frequentes")
    st.markdown("""
    - Quais serviços oferecem?
    - Qual o horário de funcionamento?
    - Quanto custa a troca de óleo?
    - Vocês atendem sem agendamento?
    - Quais formas de pagamento?
    """)
