import time

from loguru import logger

from app.models.schemas import (
    HypaParams,
    QueryComplexity,
    QueryResponse,
    SourceChunk,
)
from app.services.classifier import classify_query
from app.services.llm import llm_service
from app.services.retriever import hypa_retriever


class RAGPipeline:
    """Pipeline HyPA-RAG completo:
    1. Classificar complexidade da query
    2. Ajustar parâmetros adaptativos (top_k, rewrites)
    3. Reescrever queries (se necessário)
    4. Recuperar chunks via BM25 + FAISS + KG + RRF
    5. Gerar resposta com citações via LLM
    """

    def process(self, question: str) -> QueryResponse:
        t0 = time.perf_counter()

        # 1. Classificar complexidade
        complexity, params = classify_query(question)
        top_k = params["top_k"]
        n_rewrites = params["query_rewrites"]

        logger.info(
            f"Query classificada: {complexity.value} | "
            f"top_k={top_k}, rewrites={n_rewrites}"
        )

        # 2. Reescrever queries se necessário
        rewritten = []
        if n_rewrites > 0 and llm_service.is_loaded:
            rewritten = llm_service.rewrite_query(question, n_rewrites)
            logger.info(f"Queries reescritas: {rewritten}")

        # 3. Recuperar chunks
        chunks = hypa_retriever.retrieve(
            query=question,
            top_k=top_k,
            additional_queries=rewritten,
        )

        if not chunks:
            elapsed = (time.perf_counter() - t0) * 1000
            return QueryResponse(
                answer="Não foram encontrados trechos de legislação relevantes para esta consulta. "
                "Verifique se a base de legislação foi ingerida corretamente.",
                sources=[],
                hypa_params=HypaParams(
                    complexity=complexity,
                    top_k=top_k,
                    query_rewrites=n_rewrites,
                    rewritten_queries=rewritten,
                ),
                query=question,
                processing_time_ms=elapsed,
            )

        # 4. Gerar resposta com LLM
        answer = llm_service.generate(question, chunks)

        elapsed = (time.perf_counter() - t0) * 1000

        # 5. Montar resposta
        sources = [
            SourceChunk(
                content=c["content"][:500],
                law_name=c.get("law_name", "N/A"),
                article=c.get("article"),
                score=c.get("score", 0.0),
                retrieval_method=c.get("retrieval_method", "unknown"),
            )
            for c in chunks
        ]

        logger.info(f"Resposta gerada em {elapsed:.0f}ms | {len(sources)} fontes")

        return QueryResponse(
            answer=answer,
            sources=sources,
            hypa_params=HypaParams(
                complexity=complexity,
                top_k=top_k,
                query_rewrites=n_rewrites,
                rewritten_queries=rewritten,
            ),
            query=question,
            processing_time_ms=elapsed,
        )


rag_pipeline = RAGPipeline()
