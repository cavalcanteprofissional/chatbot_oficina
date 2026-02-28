"""Módulo para carregamento de documentos."""
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(data_path: str) -> list:
    """Carrega documentos de um diretório."""
    data_dir = Path(data_path)
    documents = []
    
    for file_path in data_dir.glob("*.txt"):
        loader = TextLoader(str(file_path), encoding="utf-8")
        documents.extend(loader.load())
    
    return documents


def split_documents(documents: list, chunk_size: int = 500, chunk_overlap: int = 100) -> list:
    """Divide documentos em chunks menores."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return text_splitter.split_documents(documents)
