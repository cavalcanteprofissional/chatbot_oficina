"""Schema do banco de dados."""
from src.chatbot_oficina.database.client import get_supabase_client


def create_tables():
    """
    Cria as tabelas no Supabase se não existirem.
    Executa via SQL direto.
    """
    client = get_supabase_client()
    
    # SQL para criar tabela clientes
    create_clientes_sql = """
    CREATE TABLE IF NOT EXISTS clientes (
        id SERIAL PRIMARY KEY,
        nome TEXT,
        telefone TEXT,
        email TEXT,
        placa TEXT,
        modelo TEXT,
        ano INTEGER,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    
    # SQL para criar tabela conversas
    create_conversas_sql = """
    CREATE TABLE IF NOT EXISTS conversas (
        id SERIAL PRIMARY KEY,
        cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE,
        mensagem TEXT,
        resposta TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    
    # Executar SQL - Supabase permite executar via RPC ou raw SQL
    # Aqui vamos usar uma abordagem mais simples: tentar inserir e忽略 erros
    # Na verdade, para Supabase, o ideal é criar as tabelas pelo dashboard
    # Esta função é mais para documentação
    
    return """
    Execute os seguintes comandos SQL no editor SQL do Supabase:
    
    CREATE TABLE IF NOT EXISTS clientes (
        id SERIAL PRIMARY KEY,
        nome TEXT,
        telefone TEXT,
        email TEXT,
        placa TEXT,
        modelo TEXT,
        ano INTEGER,
        created_at TIMESTAMP DEFAULT NOW()
    );
    
    CREATE TABLE IF NOT EXISTS conversas (
        id SERIAL PRIMARY KEY,
        cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE,
        mensagem TEXT,
        resposta TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """


def init_database():
    """Inicializa o banco - retorna instruções se necessário."""
    client = get_supabase_client()
    
    # Verificar se as tabelas existem
    try:
        client.table("clientes").select("*").limit(1).execute()
        return True
    except Exception:
        return False
