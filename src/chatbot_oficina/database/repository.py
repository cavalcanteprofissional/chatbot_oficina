"""Repository para operações de banco de dados."""
from typing import Optional, Dict, Any, List
from src.chatbot_oficina.database.client import get_supabase_client


def salvar_cliente(
    nome: str,
    telefone: str,
    email: Optional[str] = None,
    placa: Optional[str] = None,
    modelo: Optional[str] = None,
    ano: Optional[int] = None
) -> int:
    """
    Salva um novo cliente e retorna o ID.
    
    Args:
        nome: Nome do cliente
        telefone: Telefone do cliente
        email: Email (opcional)
        placa: Placa do veículo (opcional)
        modelo: Modelo do veículo (opcional)
        ano: Ano do veículo (opcional)
    
    Returns:
        ID do cliente criado
    """
    client = get_supabase_client()
    
    data = {
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "placa": placa,
        "modelo": modelo,
        "ano": ano
    }
    
    response = client.table("clientes").insert(data).execute()
    
    if response.data:
        return response.data[0]["id"]
    
    raise Exception("Erro ao salvar cliente")


def buscar_cliente_por_telefone(telefone: str) -> Optional[Dict[str, Any]]:
    """
    Busca cliente pelo telefone.
    
    Args:
        telefone: Telefone do cliente
    
    Returns:
        Dados do cliente ou None se não encontrar
    """
    client = get_supabase_client()
    
    response = client.table("clientes").select("*").eq("telefone", telefone).execute()
    
    if response.data:
        return response.data[0]
    
    return None


def buscar_cliente_por_id(cliente_id: int) -> Optional[Dict[str, Any]]:
    """
    Busca cliente pelo ID.
    
    Args:
        cliente_id: ID do cliente
    
    Returns:
        Dados do cliente ou None se não encontrar
    """
    client = get_supabase_client()
    
    response = client.table("clientes").select("*").eq("id", cliente_id).execute()
    
    if response.data:
        return response.data[0]
    
    return None


def salvar_conversa(cliente_id: int, mensagem: str, resposta: str) -> int:
    """
    Salva uma conversa.
    
    Args:
        cliente_id: ID do cliente
        mensagem: Mensagem do usuário
        resposta: Resposta do chatbot
    
    Returns:
        ID da conversa salva
    """
    client = get_supabase_client()
    
    data = {
        "cliente_id": cliente_id,
        "mensagem": mensagem,
        "resposta": resposta
    }
    
    response = client.table("conversas").insert(data).execute()
    
    if response.data:
        return response.data[0]["id"]
    
    raise Exception("Erro ao salvar conversa")


def listar_conversas_cliente(cliente_id: int, limite: int = 50) -> List[Dict[str, Any]]:
    """
    Lista conversas de um cliente.
    
    Args:
        cliente_id: ID do cliente
        limite: Número máximo de conversas
    
    Returns:
        Lista de conversas
    """
    client = get_supabase_client()
    
    response = (
        client.table("conversas")
        .select("*")
        .eq("cliente_id", cliente_id)
        .order("created_at", desc=True)
        .limit(limite)
        .execute()
    )
    
    return response.data or []


def atualizar_cliente(cliente_id: int, **kwargs) -> bool:
    """
    Atualiza dados de um cliente.
    
    Args:
        cliente_id: ID do cliente
        **kwargs: Campos a atualizar
    
    Returns:
        True se sucesso
    """
    client = get_supabase_client()
    
    response = client.table("clientes").update(kwargs).eq("id", cliente_id).execute()
    
    return len(response.data) > 0


def identificar_ou_criar_cliente(telefone: str, nome: str = None) -> Optional[Dict[str, Any]]:
    """
    Busca cliente por telefone. Se não existir e nome for fornecido, cria novo.
    
    Args:
        telefone: Telefone do cliente
        nome: Nome do cliente (opcional, mas necessário se cliente não existir)
    
    Returns:
        Dados do cliente ou None se não encontrado/criado
    """
    cliente = buscar_cliente_por_telefone(telefone)
    if cliente:
        return cliente
    
    if nome:
        cliente_id = salvar_cliente(nome=nome, telefone=telefone)
        return buscar_cliente_por_id(cliente_id)
    
    return None
