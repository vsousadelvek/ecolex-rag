from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    model_name: str = "mistralai/Mistral-7B-Instruct-v0.3"
    embedding_model: str = "rufimelo/Legal-BERTimbau-sts-base-ma"
    device: str = "cuda"
    torch_dtype: str = "float16"

    faiss_index_path: str = "./data/faiss_index"
    bm25_index_path: str = "./data/bm25_index.json"
    kg_index_path: str = "./data/kg_index.json"
    legislation_path: str = "./data/legislation"

    max_new_tokens: int = 1024
    temperature: float = 0.1

    log_level: str = "INFO"

    # HyPA-RAG adaptive params per complexity level
    hypa_k_simple: int = 5
    hypa_k_medium: int = 10
    hypa_k_complex: int = 15
    hypa_rewrites_simple: int = 0
    hypa_rewrites_medium: int = 1
    hypa_rewrites_complex: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
