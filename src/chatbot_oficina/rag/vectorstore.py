"""Módulo para criação do vectorstore com FAISS."""
import os
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def create_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """Cria o modelo de embeddings."""
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'}
    )


def create_vectorstore(chunks, embeddings, persist_directory: str = "data/faiss_db"):
    """Cria e persiste o vectorstore."""
    Path(persist_directory).mkdir(parents=True, exist_ok=True)
    
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    vectorstore.save_local(persist_directory)
    return vectorstore


def load_vectorstore(embeddings, persist_directory: str = "data/faiss_db"):
    """Carrega o vectorstore persistido."""
    if not Path(persist_directory).exists():
        return None
    
    return FAISS.load_local(
        persist_directory,
        embeddings,
        allow_dangerous_deserialization=True
    )
