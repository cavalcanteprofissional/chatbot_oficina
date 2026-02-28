"""Módulo para criação da chain RAG."""
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


SYSTEM_PROMPT = """Você é um assistente de atendimento de uma oficina automotiva chamada "AutoCare". 
Seu objetivo é ajudar clientes com dúvidas sobre serviços, preços, agendamento e outras informações da oficina.

Use apenas as informações fornecidas no contexto para responder. Se não souber a resposta, diga que não tem essa informação e sugere entrar em contato diretamente com a oficina.

Seja sempre simpático, profissional e prestativo.

Contexto dos documentos:
{context}"""


QUESTION_PROMPT = """Pergunta: {question}"""


def create_rag_chain(llm, retriever):
    """Cria a chain RAG completa."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", QUESTION_PROMPT)
    ])
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain
