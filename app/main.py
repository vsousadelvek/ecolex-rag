from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.config import settings
from app.routers.query import router
from app.services.embeddings import embedding_service
from app.services.knowledge_graph import kg_service
from app.services.llm import llm_service
from app.services.retriever import bm25_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Inicializando EcoLex RAG...")

    embedding_service.load()
    bm25_service.load()
    kg_service.load()
    llm_service.load()

    logger.info("EcoLex RAG pronto!")
    yield
    logger.info("Encerrando EcoLex RAG...")


app = FastAPI(
    title="EcoLex RAG",
    description=(
        "Sistema HyPA-RAG com Legal-BERTimbau e Mistral 7B "
        "para suporte explicável à decisão em gestão ambiental brasileira"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)
