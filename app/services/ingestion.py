import re
from pathlib import Path

import pdfplumber
from loguru import logger

from app.models.schemas import IngestResponse
from app.services.embeddings import embedding_service
from app.services.knowledge_graph import kg_service
from app.services.retriever import bm25_service


def ingest_legislation(
    law_name: str,
    file_path: str | None = None,
    raw_text: str | None = None,
) -> IngestResponse:
    if file_path:
        text = _load_file(file_path)
    elif raw_text:
        text = raw_text
    else:
        raise ValueError("file_path ou raw_text é obrigatório")

    logger.info(f"Ingerindo: {law_name} ({len(text)} caracteres)")

    # 1. Chunking legal-aware
    chunks = legal_chunk(text, law_name)
    logger.info(f"Chunks criados: {len(chunks)}")

    # 2. Adicionar aos índices
    embedding_service.add_chunks(chunks)
    bm25_service.add_chunks(chunks)

    # 3. Extrair triplets para Knowledge Graph
    triplets = kg_service.extract_triplets(text, law_name)
    logger.info(f"Triplets extraídos: {len(triplets)}")

    # 4. Persistir
    embedding_service.save_index()
    bm25_service.save()
    kg_service.save()

    return IngestResponse(
        law_name=law_name,
        chunks_created=len(chunks),
        triplets_extracted=len(triplets),
        message=f"Legislação '{law_name}' ingerida com sucesso",
    )


def legal_chunk(text: str, law_name: str) -> list[dict]:
    """Chunking baseado na estrutura legal brasileira.

    Divide por artigos, preservando contexto hierárquico
    (capítulo, seção, artigo com seus parágrafos e incisos).
    """
    chunks = []

    # Rastrear hierarquia atual
    current_title = ""
    current_chapter = ""
    current_section = ""

    # Detectar títulos, capítulos e seções
    hierarchy_pattern = re.compile(
        r"(TÍTULO\s+[IVXLC]+[^.\n]*|"
        r"CAPÍTULO\s+[IVXLC]+[^.\n]*|"
        r"Capítulo\s+[IVXLC]+[^.\n]*|"
        r"SEÇÃO\s+[IVXLC]+[^.\n]*|"
        r"Seção\s+[IVXLC]+[^.\n]*)",
        re.MULTILINE,
    )

    # Dividir por artigos
    article_splits = re.split(
        r"(?=Art\.\s*\d+[\w-]*[.°º]?\s)", text, flags=re.IGNORECASE
    )

    for segment in article_splits:
        segment = segment.strip()
        if not segment:
            continue

        # Atualizar hierarquia
        for h_match in hierarchy_pattern.finditer(segment):
            h_text = h_match.group(1).strip()
            if h_text.upper().startswith("TÍTULO"):
                current_title = h_text
                current_chapter = ""
                current_section = ""
            elif h_text.upper().startswith("CAPÍTULO"):
                current_chapter = h_text
                current_section = ""
            elif h_text.upper().startswith("SEÇÃO"):
                current_section = h_text

        # Extrair número do artigo
        art_match = re.match(
            r"(Art\.\s*\d+[\w-]*[.°º]?)", segment, re.IGNORECASE
        )
        article_id = art_match.group(1).strip() if art_match else None

        # Se o segmento é muito grande, subdividir por parágrafos
        if len(segment) > 2000:
            sub_chunks = _split_long_article(segment, law_name, article_id)
            for sc in sub_chunks:
                sc["title"] = current_title
                sc["chapter"] = current_chapter
                sc["section"] = current_section
            chunks.extend(sub_chunks)
        elif len(segment) > 30:
            hierarchy = " > ".join(
                filter(None, [current_title, current_chapter, current_section])
            )
            chunks.append({
                "content": f"[{law_name}] [{hierarchy}]\n{segment}" if hierarchy else f"[{law_name}]\n{segment}",
                "law_name": law_name,
                "article": article_id,
                "title": current_title,
                "chapter": current_chapter,
                "section": current_section,
            })

    # Fallback: se não conseguiu dividir por artigos, chunk por tamanho
    if not chunks:
        chunks = _fallback_chunk(text, law_name)

    return chunks


def _split_long_article(text: str, law_name: str, article_id: str | None) -> list[dict]:
    """Subdivide artigos muito longos por parágrafos."""
    parts = re.split(
        r"(?=§\s*\d+|Parágrafo\s+único)", text, flags=re.IGNORECASE
    )

    chunks = []
    for part in parts:
        part = part.strip()
        if len(part) > 30:
            chunks.append({
                "content": f"[{law_name}] {part}",
                "law_name": law_name,
                "article": article_id,
            })
    return chunks if chunks else [{"content": f"[{law_name}] {text}", "law_name": law_name, "article": article_id}]


def _fallback_chunk(text: str, law_name: str, chunk_size: int = 1000, overlap: int = 200) -> list[dict]:
    """Chunking por tamanho com overlap quando a estrutura legal não é detectada."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]
        if len(chunk_text.strip()) > 30:
            chunks.append({
                "content": f"[{law_name}]\n{chunk_text.strip()}",
                "law_name": law_name,
                "article": None,
            })
        start += chunk_size - overlap
    return chunks


def _load_file(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    if path.suffix.lower() == ".pdf":
        return _load_pdf(path)
    else:
        return path.read_text(encoding="utf-8")


def _load_pdf(path: Path) -> str:
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)
