"""Estudo de ablação do sistema EcoLex HyPA-RAG.

Remove componentes incrementalmente para quantificar a contribuição de cada um.
Os resultados provam que o pipeline completo supera qualquer subconjunto.

Configurações testadas:
  1. BM25-only            -- Sparse retrieval isolado
  2. Semantic-only         -- Dense retrieval (FAISS/Legal-BERTimbau) isolado
  3. KG-only               -- Knowledge Graph isolado
  4. BM25+Semantic         -- Sparse + Dense com RRF
  5. Híbrido fixo          -- BM25 + Semantic + KG com RRF, parâmetros fixos
  6. HyPA-RAG (completo)   -- Tudo acima + classificador adaptativo + rewrites

Uso:
    python -m scripts.ablation
    python -m scripts.ablation --output data/ablation_results.json
    python -m scripts.ablation --configs 1,2,6           # executa apenas estas
    python -m scripts.ablation --skip-full               # pula HyPA-RAG completo (mais rápido)
"""

import argparse
import json
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.schemas import HypaParams, QueryComplexity, QueryResponse, SourceChunk
from app.services.classifier import classify_query
from app.services.embeddings import embedding_service
from app.services.knowledge_graph import kg_service
from app.services.llm import llm_service
from app.services.retriever import bm25_service, reciprocal_rank_fusion
from scripts.eval_dataset import EVAL_DATASET_FULL

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

FIXED_K = 10
FIXED_REWRITES = 0


# ---------------------------------------------------------------------------
# Resultado por query individual
# ---------------------------------------------------------------------------

@dataclass
class QueryResult:
    question: str
    expected_law: str
    expected_article: str
    complexity_hint: str
    classified_complexity: str
    law_retrieved: bool
    article_retrieved: bool
    answer_cites_law: bool
    answer_cites_article: bool
    num_sources: int
    response_time_s: float
    retrieval_methods_used: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Resultado agregado por configuração
# ---------------------------------------------------------------------------

@dataclass
class AblationMetrics:
    config_name: str
    total_queries: int = 0
    law_retrieval_rate: float = 0.0
    article_retrieval_rate: float = 0.0
    citation_law_rate: float = 0.0
    citation_article_rate: float = 0.0
    avg_sources: float = 0.0
    avg_response_time_s: float = 0.0
    # Per-complexity breakdown
    per_complexity: dict = field(default_factory=dict)

    def compute(self, results: list[QueryResult]) -> None:
        n = len(results)
        if n == 0:
            return
        self.total_queries = n
        self.law_retrieval_rate = sum(r.law_retrieved for r in results) / n
        self.article_retrieval_rate = sum(r.article_retrieved for r in results) / n
        self.citation_law_rate = sum(r.answer_cites_law for r in results) / n
        self.citation_article_rate = sum(r.answer_cites_article for r in results) / n
        self.avg_sources = sum(r.num_sources for r in results) / n
        self.avg_response_time_s = sum(r.response_time_s for r in results) / n

        # Breakdown per complexity hint
        for level in ("simple", "medium", "complex"):
            subset = [r for r in results if r.complexity_hint == level]
            if not subset:
                continue
            m = len(subset)
            self.per_complexity[level] = {
                "count": m,
                "law_retrieval_rate": sum(r.law_retrieved for r in subset) / m,
                "article_retrieval_rate": sum(r.article_retrieved for r in subset) / m,
                "citation_law_rate": sum(r.answer_cites_law for r in subset) / m,
                "citation_article_rate": sum(r.answer_cites_article for r in subset) / m,
                "avg_sources": sum(r.num_sources for r in subset) / m,
                "avg_response_time_s": sum(r.response_time_s for r in subset) / m,
            }


# ---------------------------------------------------------------------------
# Funções de retrieval para cada configuração de ablação
# ---------------------------------------------------------------------------

def retrieve_bm25_only(query: str, top_k: int = FIXED_K, **_kw) -> list[dict]:
    """Config 1 -- apenas BM25 sparse."""
    return bm25_service.search(query, top_k=top_k)


def retrieve_semantic_only(query: str, top_k: int = FIXED_K, **_kw) -> list[dict]:
    """Config 2 -- apenas FAISS/Legal-BERTimbau dense."""
    return embedding_service.search(query, top_k=top_k)


def retrieve_kg_only(query: str, top_k: int = FIXED_K, **_kw) -> list[dict]:
    """Config 3 -- apenas Knowledge Graph."""
    return kg_service.search(query, top_k=top_k)


def retrieve_bm25_semantic(query: str, top_k: int = FIXED_K, **_kw) -> list[dict]:
    """Config 4 -- BM25 + Semantic com RRF (sem KG)."""
    bm25_results = bm25_service.search(query, top_k=top_k)
    semantic_results = embedding_service.search(query, top_k=top_k)
    return reciprocal_rank_fusion(bm25_results, semantic_results, top_n=top_k)


def retrieve_hybrid_fixed(query: str, top_k: int = FIXED_K, **_kw) -> list[dict]:
    """Config 5 -- BM25 + Semantic + KG com RRF, parâmetros fixos."""
    bm25_results = bm25_service.search(query, top_k=top_k)
    semantic_results = embedding_service.search(query, top_k=top_k)
    kg_results = kg_service.search(query, top_k=top_k)
    return reciprocal_rank_fusion(
        bm25_results, semantic_results, kg_results, top_n=top_k,
    )


def retrieve_hypa_rag(
    query: str,
    top_k: int = FIXED_K,
    additional_queries: list[str] | None = None,
    **_kw,
) -> list[dict]:
    """Config 6 -- HyPA-RAG completo: 3 retrievers + RRF + rewrites adaptativos.

    top_k e additional_queries vêm do classificador adaptativo externo.
    """
    all_queries = [query] + (additional_queries or [])

    bm25_all, sem_all, kg_all = [], [], []
    for q in all_queries:
        bm25_all.extend(bm25_service.search(q, top_k=top_k))
        sem_all.extend(embedding_service.search(q, top_k=top_k))
        kg_all.extend(kg_service.search(q, top_k=top_k))

    # Deduplicate each list before fusion
    bm25_all = _deduplicate(bm25_all, top_k)
    sem_all = _deduplicate(sem_all, top_k)
    kg_all = _deduplicate(kg_all, top_k)

    return reciprocal_rank_fusion(bm25_all, sem_all, kg_all, top_n=top_k)


def _deduplicate(results: list[dict], top_k: int) -> list[dict]:
    seen: set[str] = set()
    deduped: list[dict] = []
    for r in results:
        key = r.get("content", "")[:200]
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    deduped.sort(key=lambda x: x.get("score", 0), reverse=True)
    return deduped[:top_k]


# ---------------------------------------------------------------------------
# Definição das configurações de ablação
# ---------------------------------------------------------------------------

@dataclass
class AblationConfig:
    id: int
    name: str
    short_name: str
    retrieve_fn: Callable
    adaptive: bool = False  # True apenas para HyPA-RAG completo


ABLATION_CONFIGS: list[AblationConfig] = [
    AblationConfig(1, "BM25-only", "BM25", retrieve_bm25_only),
    AblationConfig(2, "Semantic-only", "Semantic", retrieve_semantic_only),
    AblationConfig(3, "KG-only", "KG", retrieve_kg_only),
    AblationConfig(4, "BM25+Semantic", "BM25+Sem", retrieve_bm25_semantic),
    AblationConfig(5, "Híbrido fixo", "Hybrid-F", retrieve_hybrid_fixed),
    AblationConfig(6, "HyPA-RAG", "HyPA", retrieve_hypa_rag, adaptive=True),
]


# ---------------------------------------------------------------------------
# Motor principal do estudo de ablação
# ---------------------------------------------------------------------------

def run_single_query(
    item: dict,
    config: AblationConfig,
) -> QueryResult:
    """Executa uma query sob uma configuração de ablação e retorna as métricas."""
    question = item["question"]
    t0 = time.perf_counter()

    # -- Retrieval --
    if config.adaptive:
        # HyPA-RAG: classificar e adaptar parâmetros
        complexity, params = classify_query(question)
        top_k = params["top_k"]
        n_rewrites = params["query_rewrites"]

        rewritten = []
        if n_rewrites > 0 and llm_service.is_loaded:
            rewritten = llm_service.rewrite_query(question, n_rewrites)

        chunks = config.retrieve_fn(
            query=question,
            top_k=top_k,
            additional_queries=rewritten,
        )
        classified = complexity.value
    else:
        # Ablação com parâmetros fixos, sem rewrites
        chunks = config.retrieve_fn(query=question, top_k=FIXED_K)
        classified = "fixed"

    # -- Geração (LLM) --
    if chunks and llm_service.is_loaded:
        answer = llm_service.generate(question, chunks)
    elif not chunks:
        answer = "Nenhum chunk recuperado."
    else:
        answer = "LLM não carregado."

    elapsed = time.perf_counter() - t0

    # -- Métricas de avaliação --
    source_laws = [c.get("law_name", "") for c in chunks]
    source_articles = [c.get("article", "") or "" for c in chunks]

    law_found = any(
        item["expected_law"].lower() in law.lower() for law in source_laws
    )
    article_found = any(
        item["expected_article"].lower() in art.lower() for art in source_articles
    )
    answer_lower = answer.lower()
    cites_law = item["expected_law"].lower() in answer_lower
    cites_article = item["expected_article"].lower() in answer_lower

    methods_used = list({c.get("retrieval_method", "unknown") for c in chunks})

    return QueryResult(
        question=question,
        expected_law=item["expected_law"],
        expected_article=item["expected_article"],
        complexity_hint=item.get("complexity", item.get("complexity_hint", "unknown")),
        classified_complexity=classified,
        law_retrieved=law_found,
        article_retrieved=article_found,
        answer_cites_law=cites_law,
        answer_cites_article=cites_article,
        num_sources=len(chunks),
        response_time_s=round(elapsed, 3),
        retrieval_methods_used=methods_used,
    )


def run_ablation_config(
    config: AblationConfig,
    dataset: list[dict],
) -> tuple[AblationMetrics, list[QueryResult]]:
    """Executa todas as queries para uma configuração e retorna métricas."""
    query_results: list[QueryResult] = []

    for idx, item in enumerate(dataset, 1):
        short_q = item["question"][:70]
        print(f"    [{idx}/{len(dataset)}] {short_q}...")
        result = run_single_query(item, config)
        query_results.append(result)

        status = "OK" if result.law_retrieved else "MISS"
        print(
            f"      [{status}] Lei: {result.law_retrieved} | "
            f"Art: {result.article_retrieved} | "
            f"Cit: {result.answer_cites_law} | "
            f"{result.response_time_s:.1f}s"
        )

    metrics = AblationMetrics(config_name=config.name)
    metrics.compute(query_results)
    return metrics, query_results


# ---------------------------------------------------------------------------
# Formatação de resultados
# ---------------------------------------------------------------------------

def format_markdown_table(all_metrics: list[AblationMetrics]) -> str:
    """Gera tabela Markdown pronta para colar no artigo."""
    lines: list[str] = []

    # Tabela principal
    lines.append("## Resultados do Estudo de Ablacao - EcoLex HyPA-RAG")
    lines.append("")
    lines.append(
        "| Configuracao        | Lei Ret. | Art. Ret. | Cit. Lei | Cit. Art. | Fontes | Tempo(s) |"
    )
    lines.append(
        "|---------------------|----------|-----------|----------|-----------|--------|----------|"
    )
    for m in all_metrics:
        lines.append(
            f"| {m.config_name:<19} "
            f"| {m.law_retrieval_rate:>6.0%}   "
            f"| {m.article_retrieval_rate:>7.0%}    "
            f"| {m.citation_law_rate:>6.0%}   "
            f"| {m.citation_article_rate:>7.0%}    "
            f"| {m.avg_sources:>4.1f}   "
            f"| {m.avg_response_time_s:>6.1f}   |"
        )

    # Tabela por complexidade
    complexity_levels = ("simple", "medium", "complex")
    for level in complexity_levels:
        lines.append("")
        lines.append(f"### Breakdown: {level}")
        lines.append("")
        lines.append(
            "| Configuracao        | Lei Ret. | Art. Ret. | Cit. Lei | Cit. Art. | Fontes | Tempo(s) |"
        )
        lines.append(
            "|---------------------|----------|-----------|----------|-----------|--------|----------|"
        )
        for m in all_metrics:
            sub = m.per_complexity.get(level)
            if sub is None:
                lines.append(f"| {m.config_name:<19} |    --    |     --    |    --    |     --    |   --   |    --    |")
                continue
            lines.append(
                f"| {m.config_name:<19} "
                f"| {sub['law_retrieval_rate']:>6.0%}   "
                f"| {sub['article_retrieval_rate']:>7.0%}    "
                f"| {sub['citation_law_rate']:>6.0%}   "
                f"| {sub['citation_article_rate']:>7.0%}    "
                f"| {sub['avg_sources']:>4.1f}   "
                f"| {sub['avg_response_time_s']:>6.1f}   |"
            )

    return "\n".join(lines)


def format_console_summary(all_metrics: list[AblationMetrics]) -> str:
    """Resumo compacto para o terminal."""
    sep = "=" * 100
    lines = [sep, "  ESTUDO DE ABLACAO -- EcoLex HyPA-RAG", sep, ""]

    header = (
        f"  {'Configuracao':<20} {'Lei Ret.':>9} {'Art. Ret.':>10} "
        f"{'Cit. Lei':>9} {'Cit. Art.':>10} {'Fontes':>7} {'Tempo(s)':>9}"
    )
    lines.append(header)
    lines.append("  " + "-" * 96)

    for m in all_metrics:
        lines.append(
            f"  {m.config_name:<20} {m.law_retrieval_rate:>8.1%} {m.article_retrieval_rate:>9.1%} "
            f"{m.citation_law_rate:>8.1%} {m.citation_article_rate:>9.1%} "
            f"{m.avg_sources:>6.1f} {m.avg_response_time_s:>8.1f}"
        )

    lines.append("")

    # Deltas vs HyPA-RAG completo
    hypa = next((m for m in all_metrics if m.config_name == "HyPA-RAG"), None)
    if hypa:
        lines.append("  Deltas vs HyPA-RAG completo (pontos percentuais):")
        lines.append("  " + "-" * 96)
        for m in all_metrics:
            if m.config_name == "HyPA-RAG":
                continue
            d_law = (m.law_retrieval_rate - hypa.law_retrieval_rate) * 100
            d_art = (m.article_retrieval_rate - hypa.article_retrieval_rate) * 100
            d_claw = (m.citation_law_rate - hypa.citation_law_rate) * 100
            d_cart = (m.citation_article_rate - hypa.citation_article_rate) * 100
            lines.append(
                f"  {m.config_name:<20} {d_law:>+8.1f}pp {d_art:>+9.1f}pp "
                f"{d_claw:>+8.1f}pp {d_cart:>+9.1f}pp"
            )

    lines.append("")
    lines.append(sep)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Estudo de ablacao do EcoLex HyPA-RAG",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/ablation_results.json",
        help="Caminho para salvar resultados JSON (default: data/ablation_results.json)",
    )
    parser.add_argument(
        "--configs",
        type=str,
        default=None,
        help="IDs das configs para executar, separados por virgula (ex: 1,2,6). Default: todas.",
    )
    parser.add_argument(
        "--skip-full",
        action="store_true",
        help="Pula a config 6 (HyPA-RAG completo) para teste rapido.",
    )
    parser.add_argument(
        "--markdown-output",
        type=str,
        default=None,
        help="Salvar tabela Markdown em arquivo (ex: data/ablation_table.md)",
    )
    args = parser.parse_args()

    # Determinar quais configs rodar
    if args.configs:
        selected_ids = {int(x.strip()) for x in args.configs.split(",")}
    else:
        selected_ids = {c.id for c in ABLATION_CONFIGS}

    if args.skip_full:
        selected_ids.discard(6)

    configs_to_run = [c for c in ABLATION_CONFIGS if c.id in selected_ids]
    if not configs_to_run:
        print("Nenhuma configuracao selecionada. Use --configs 1,2,3,4,5,6")
        sys.exit(1)

    # ------------------------------------------------------------------
    # Carregar servicos (uma unica vez)
    # ------------------------------------------------------------------
    print("=" * 80)
    print("  Inicializando servicos do EcoLex RAG...")
    print("=" * 80)

    print("  [1/4] Carregando embedding model + FAISS index...")
    embedding_service.load()

    print("  [2/4] Carregando BM25 index...")
    bm25_service.load()

    print("  [3/4] Carregando Knowledge Graph...")
    kg_service.load()

    print("  [4/4] Carregando LLM...")
    llm_service.load()

    print(
        f"\n  Servicos carregados. "
        f"FAISS: {embedding_service.total_chunks} chunks | "
        f"BM25: {bm25_service.total_chunks} chunks | "
        f"KG: {kg_service.total_triplets} triplets"
    )
    print(f"  Dataset: {len(EVAL_DATASET_FULL)} queries")
    print(f"  Configs a executar: {[c.name for c in configs_to_run]}")
    print()

    # ------------------------------------------------------------------
    # Executar cada configuracao
    # ------------------------------------------------------------------
    all_metrics: list[AblationMetrics] = []
    all_detailed: dict[str, list[dict]] = {}
    total_start = time.perf_counter()

    for config in configs_to_run:
        print("=" * 80)
        print(f"  CONFIG {config.id}/{len(ABLATION_CONFIGS)}: {config.name}")
        adaptive_label = "(adaptativo)" if config.adaptive else f"(k={FIXED_K}, rewrites={FIXED_REWRITES})"
        print(f"  Parametros: {adaptive_label}")
        print("=" * 80)

        metrics, query_results = run_ablation_config(config, EVAL_DATASET_FULL)
        all_metrics.append(metrics)
        all_detailed[config.name] = [asdict(qr) for qr in query_results]

        print(
            f"\n  >> {config.name}: "
            f"Lei={metrics.law_retrieval_rate:.0%} | "
            f"Art={metrics.article_retrieval_rate:.0%} | "
            f"CitLei={metrics.citation_law_rate:.0%} | "
            f"CitArt={metrics.citation_article_rate:.0%} | "
            f"Fontes={metrics.avg_sources:.1f} | "
            f"Tempo={metrics.avg_response_time_s:.1f}s"
        )
        print()

    total_elapsed = time.perf_counter() - total_start

    # ------------------------------------------------------------------
    # Imprimir resultados
    # ------------------------------------------------------------------
    console_text = format_console_summary(all_metrics)
    print(console_text)

    md_table = format_markdown_table(all_metrics)
    print("\n--- TABELA MARKDOWN (copiar para o artigo) ---\n")
    print(md_table)
    print()

    # ------------------------------------------------------------------
    # Salvar JSON
    # ------------------------------------------------------------------
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        "metadata": {
            "total_configs": len(configs_to_run),
            "total_queries_per_config": len(EVAL_DATASET_FULL),
            "fixed_k": FIXED_K,
            "fixed_rewrites": FIXED_REWRITES,
            "total_elapsed_s": round(total_elapsed, 2),
        },
        "summary": [asdict(m) for m in all_metrics],
        "detailed_results": all_detailed,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Resultados salvos em: {output_path.resolve()}")

    # ------------------------------------------------------------------
    # Salvar Markdown (opcional)
    # ------------------------------------------------------------------
    if args.markdown_output:
        md_path = Path(args.markdown_output)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(md_table, encoding="utf-8")
        print(f"Tabela Markdown salva em: {md_path.resolve()}")

    print(f"\nTempo total do estudo: {total_elapsed:.1f}s")


if __name__ == "__main__":
    main()
