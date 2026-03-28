import json
from pathlib import Path

import faiss
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger

from app.config import settings


class EmbeddingService:
    def __init__(self):
        self._model: HuggingFaceEmbeddings | None = None
        self._index: faiss.IndexFlatIP | None = None
        self._chunks: list[dict] = []
        self._dimension: int = 768

    def load(self):
        logger.info(f"Carregando embedding model: {settings.embedding_model}")
        self._model = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={"device": settings.device},
            encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
        )
        self._load_index()
        logger.info("Embedding model carregado")

    def _load_index(self):
        index_path = Path(settings.faiss_index_path)
        chunks_path = index_path / "chunks.json"
        faiss_path = str(index_path / "index.faiss")

        if index_path.exists() and chunks_path.exists():
            self._index = faiss.read_index(faiss_path)
            with open(chunks_path, "r", encoding="utf-8") as f:
                self._chunks = json.load(f)
            self._dimension = self._index.d
            logger.info(f"FAISS index carregado: {len(self._chunks)} chunks")
        else:
            self._index = faiss.IndexFlatIP(self._dimension)
            self._chunks = []
            logger.info("FAISS index vazio inicializado")

    def save_index(self):
        index_path = Path(settings.faiss_index_path)
        index_path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self._index, str(index_path / "index.faiss"))
        with open(index_path / "chunks.json", "w", encoding="utf-8") as f:
            json.dump(self._chunks, f, ensure_ascii=False, indent=2)
        logger.info(f"FAISS index salvo: {len(self._chunks)} chunks")

    def add_chunks(self, chunks: list[dict]):
        texts = [c["content"] for c in chunks]
        embeddings = self._model.embed_documents(texts)
        vectors = np.array(embeddings, dtype=np.float32)
        faiss.normalize_L2(vectors)
        self._index.add(vectors)
        self._chunks.extend(chunks)

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        if self._index.ntotal == 0:
            return []

        query_vec = np.array(
            [self._model.embed_query(query)], dtype=np.float32
        )
        faiss.normalize_L2(query_vec)

        k = min(top_k, self._index.ntotal)
        scores, indices = self._index.search(query_vec, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            chunk = self._chunks[idx].copy()
            chunk["score"] = float(score)
            chunk["retrieval_method"] = "semantic"
            results.append(chunk)
        return results

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    @property
    def total_chunks(self) -> int:
        return len(self._chunks)


embedding_service = EmbeddingService()
