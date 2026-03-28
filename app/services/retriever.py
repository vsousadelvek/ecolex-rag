import json
from pathlib import Path

from rank_bm25 import BM25Okapi
from loguru import logger

from app.config import settings
from app.services.embeddings import embedding_service
from app.services.knowledge_graph import kg_service


class BM25Service:
    def __init__(self):
        self._bm25: BM25Okapi | None = None
        self._chunks: list[dict] = []

    def load(self):
        bm25_path = Path(settings.bm25_index_path)
        if bm25_path.exists():
            with open(bm25_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._chunks = data.get("chunks", [])
            if self._chunks:
                corpus = [c["content"].lower().split() for c in self._chunks]
                self._bm25 = BM25Okapi(corpus)
            logger.info(f"BM25 index carregado: {len(self._chunks)} chunks")
        else:
            logger.info("BM25 index vazio")

    def save(self):
        bm25_path = Path(settings.bm25_index_path)
        bm25_path.parent.mkdir(parents=True, exist_ok=True)
        with open(bm25_path, "w", encoding="utf-8") as f:
            json.dump({"chunks": self._chunks}, f, ensure_ascii=False, indent=2)
        logger.info(f"BM25 index salvo: {len(self._chunks)} chunks")

    def add_chunks(self, chunks: list[dict]):
        self._chunks.extend(chunks)
        corpus = [c["content"].lower().split() for c in self._chunks]
        self._bm25 = BM25Okapi(corpus)

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        if not self._bm25 or not self._chunks:
            return []

        tokenized_query = query.lower().split()
        scores = self._bm25.get_scores(tokenized_query)

        top_indices = scores.argsort()[-top_k:][::-1]

        results = []
        for idx in top_indices:
            if scores[idx] <= 0:
                continue
            chunk = self._chunks[idx].copy()
            chunk["score"] = float(scores[idx])
            chunk["retrieval_method"] = "bm25"
            results.append(chunk)
        return results

    @property
    def is_loaded(self) -> bool:
        return self._bm25 is not None

    @property
    def total_chunks(self) -> int:
        return len(self._chunks)


bm25_service = BM25Service()


def reciprocal_rank_fusion(
    *result_lists: list[dict],
    k: int = 60,
    top_n: int = 10,
) -> list[dict]:
    """Reciprocal Rank Fusion (RRF) para combinar múltiplos rankings.

    RRF_score(d) = Σ 1 / (k + rank_i(d))

    onde k=60 é o padrão do paper original (Cormack et al., 2009).
    """
    doc_scores: dict[str, float] = {}
    doc_map: dict[str, dict] = {}

    for results in result_lists:
        for rank, doc in enumerate(results):
            doc_id = _doc_key(doc)
            rrf_score = 1.0 / (k + rank + 1)
            doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + rrf_score

            if doc_id not in doc_map:
                doc_map[doc_id] = doc.copy()
                doc_map[doc_id]["retrieval_methods"] = set()
            doc_map[doc_id]["retrieval_methods"].add(doc["retrieval_method"])

    sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

    fused = []
    for doc_id, rrf_score in sorted_docs[:top_n]:
        doc = doc_map[doc_id]
        methods = doc.pop("retrieval_methods", set())
        doc["score"] = rrf_score
        doc["retrieval_method"] = "+".join(sorted(methods))
        fused.append(doc)

    return fused


def _doc_key(doc: dict) -> str:
    content = doc.get("content", "")
    return content[:200]


class HypaRetriever:
    """HyPA-RAG: Hybrid Parameter-Adaptive Retrieval.

    Combina BM25 (sparse) + Legal-BERTimbau/FAISS (dense) + Knowledge Graph
    com Reciprocal Rank Fusion e parâmetros adaptativos por complexidade.
    """

    def retrieve(self, query: str, top_k: int, additional_queries: list[str] | None = None) -> list[dict]:
        all_queries = [query] + (additional_queries or [])

        # BM25 sparse retrieval
        bm25_results = []
        for q in all_queries:
            bm25_results.extend(bm25_service.search(q, top_k=top_k))
        bm25_results = _deduplicate(bm25_results, top_k)

        # FAISS dense retrieval
        semantic_results = []
        for q in all_queries:
            semantic_results.extend(embedding_service.search(q, top_k=top_k))
        semantic_results = _deduplicate(semantic_results, top_k)

        # Knowledge Graph retrieval
        kg_results = []
        for q in all_queries:
            kg_results.extend(kg_service.search(q, top_k=top_k))
        kg_results = _deduplicate(kg_results, top_k)

        # Reciprocal Rank Fusion
        fused = reciprocal_rank_fusion(
            bm25_results, semantic_results, kg_results, top_n=top_k
        )

        logger.info(
            f"HyPA Retrieval: BM25={len(bm25_results)}, "
            f"Semantic={len(semantic_results)}, KG={len(kg_results)}, "
            f"Fused={len(fused)}"
        )

        return fused


def _deduplicate(results: list[dict], top_k: int) -> list[dict]:
    seen = set()
    deduped = []
    for r in results:
        key = _doc_key(r)
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    deduped.sort(key=lambda x: x.get("score", 0), reverse=True)
    return deduped[:top_k]


hypa_retriever = HypaRetriever()
