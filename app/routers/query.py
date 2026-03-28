from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    HealthResponse,
    IngestRequest,
    IngestResponse,
    LegislationInfo,
    QueryRequest,
    QueryResponse,
)
from app.services.embeddings import embedding_service
from app.services.knowledge_graph import kg_service
from app.services.llm import llm_service
from app.services.rag_pipeline import rag_pipeline
from app.services.retriever import bm25_service
from app.services.ingestion import ingest_legislation

router = APIRouter(prefix="/api", tags=["EcoLex RAG"])


@router.post("/query", response_model=QueryResponse)
async def query_legislation(request: QueryRequest):
    if not llm_service.is_loaded:
        raise HTTPException(status_code=503, detail="LLM ainda não foi carregado")
    if not embedding_service.is_loaded:
        raise HTTPException(status_code=503, detail="Embeddings ainda não foram carregados")

    return rag_pipeline.process(request.question)


@router.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest):
    if not request.file_path and not request.raw_text:
        raise HTTPException(status_code=400, detail="Envie file_path ou raw_text")

    result = ingest_legislation(
        law_name=request.law_name,
        file_path=request.file_path,
        raw_text=request.raw_text,
    )
    return result


@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        llm_loaded=llm_service.is_loaded,
        embeddings_loaded=embedding_service.is_loaded,
        faiss_index_loaded=embedding_service.total_chunks > 0,
        bm25_index_loaded=bm25_service.is_loaded,
        legislation_count=embedding_service.total_chunks,
    )


@router.get("/legislation", response_model=list[LegislationInfo])
async def list_legislation():
    chunks_by_law: dict[str, int] = {}
    for chunk in embedding_service._chunks:
        law = chunk.get("law_name", "N/A")
        chunks_by_law[law] = chunks_by_law.get(law, 0) + 1

    triplets_by_law: dict[str, int] = {}
    for t in kg_service._triplets:
        law = t.get("object", "N/A").split(",")[0] if t["relation"] == "pertence_a" else "N/A"
        triplets_by_law[law] = triplets_by_law.get(law, 0) + 1

    all_laws = set(chunks_by_law.keys()) | set(triplets_by_law.keys())
    return [
        LegislationInfo(
            law_name=law,
            total_chunks=chunks_by_law.get(law, 0),
            total_triplets=triplets_by_law.get(law, 0),
        )
        for law in sorted(all_laws)
        if law != "N/A"
    ]
