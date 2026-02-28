"""Cliente Supabase."""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

_supabase_client = None


def get_supabase_client():
    """Retorna o cliente SupabaseSingleton."""
    global _supabase_client
    
    if _supabase_client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados no .env")
        
        _supabase_client = create_client(url, key)
    
    return _supabase_client
