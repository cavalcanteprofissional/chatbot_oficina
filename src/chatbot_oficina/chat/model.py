"""Módulo para configuração do modelo Ollama Cloud."""
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()


def get_llm(model_name: str = "gemma3:4b", temperature: float = 0.7):
    """Configura o modelo Ollama Cloud."""
    return ChatOllama(
        model=model_name,
        temperature=temperature,
        base_url="https://ollama.com",
        api_key=os.getenv("OLLAMA_API_KEY", ""),
    )
