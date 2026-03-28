from pydantic import BaseModel, Field
from enum import Enum


class QueryComplexity(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, description="Pergunta em linguagem natural sobre legislação ambiental")


class SourceChunk(BaseModel):
    content: str
    law_name: str
    article: str | None = None
    score: float
    retrieval_method: str  # "bm25", "semantic", "knowledge_graph"


class HypaParams(BaseModel):
    complexity: QueryComplexity
    top_k: int
    query_rewrites: int
    rewritten_queries: list[str] = []


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    hypa_params: HypaParams
    query: str
    processing_time_ms: float


class IngestRequest(BaseModel):
    file_path: str | None = None
    raw_text: str | None = None
    law_name: str = Field(..., description="Nome da lei (ex: 'Código Florestal - Lei 12.651/2012')")


class IngestResponse(BaseModel):
    law_name: str
    chunks_created: int
    triplets_extracted: int
    message: str


class LegislationInfo(BaseModel):
    law_name: str
    total_chunks: int
    total_triplets: int


class HealthResponse(BaseModel):
    status: str
    llm_loaded: bool
    embeddings_loaded: bool
    faiss_index_loaded: bool
    bm25_index_loaded: bool
    legislation_count: int
