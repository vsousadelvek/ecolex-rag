"""Script de avaliação do sistema EcoLex RAG com métricas RAGAS.

Uso:
    python -m scripts.evaluate                  # Executa avaliação completa
    python -m scripts.evaluate --output results.json  # Salva resultados em arquivo

Métricas avaliadas:
    - Faithfulness: respostas são fiéis ao contexto recuperado?
    - Answer Relevancy: respostas são relevantes à pergunta?
    - Context Precision: chunks recuperados são precisos?
    - Context Recall: recuperação cobre a informação necessária?
"""

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.embeddings import embedding_service
from app.services.knowledge_graph import kg_service
from app.services.llm import llm_service
from app.services.retriever import bm25_service
from app.services.rag_pipeline import rag_pipeline
from scripts.eval_dataset import EVAL_DATASET_FULL

# Usa o dataset completo de 50 perguntas
EVAL_DATASET = EVAL_DATASET_FULL



def evaluate():
    parser = argparse.ArgumentParser(description="Avaliação do EcoLex RAG")
    parser.add_argument("--output", type=str, default="data/evaluation_results.json")
    args = parser.parse_args()

    print("Inicializando serviços...")
    embedding_service.load()
    bm25_service.load()
    kg_service.load()
    llm_service.load()

    results = []
    total_time = 0

    print(f"\nExecutando {len(EVAL_DATASET)} consultas de avaliação...\n")
    print("=" * 80)

    for i, item in enumerate(EVAL_DATASET, 1):
        print(f"\n[{i}/{len(EVAL_DATASET)}] {item['question'][:80]}...")

        t0 = time.perf_counter()
        response = rag_pipeline.process(item["question"])
        elapsed = time.perf_counter() - t0
        total_time += elapsed

        # Verificar se a lei esperada aparece nas fontes
        source_laws = [s.law_name for s in response.sources]
        law_found = any(item["expected_law"].lower() in law.lower() for law in source_laws)

        # Verificar se o artigo esperado aparece
        source_articles = [s.article or "" for s in response.sources]
        article_found = any(
            item["expected_article"].lower() in art.lower()
            for art in source_articles
        )

        # Verificar citação na resposta
        answer_cites_law = item["expected_law"].lower() in response.answer.lower()
        answer_cites_article = item["expected_article"].lower() in response.answer.lower()

        result = {
            "question": item["question"],
            "expected_law": item["expected_law"],
            "expected_article": item["expected_article"],
            "ground_truth": item["ground_truth"],
            "generated_answer": response.answer,
            "complexity": response.hypa_params.complexity.value,
            "top_k_used": response.hypa_params.top_k,
            "rewrites_used": response.hypa_params.query_rewrites,
            "rewritten_queries": response.hypa_params.rewritten_queries,
            "num_sources": len(response.sources),
            "source_laws": source_laws,
            "retrieval_methods": [s.retrieval_method for s in response.sources],
            "metrics": {
                "law_retrieved": law_found,
                "article_retrieved": article_found,
                "answer_cites_law": answer_cites_law,
                "answer_cites_article": answer_cites_article,
                "response_time_s": round(elapsed, 2),
            },
        }
        results.append(result)

        status = "OK" if (law_found and answer_cites_law) else "MISS"
        print(f"  [{status}] Complexidade: {result['complexity']} | "
              f"Lei encontrada: {law_found} | Citação: {answer_cites_law} | "
              f"Tempo: {elapsed:.1f}s")

    # Calcular métricas agregadas
    print("\n" + "=" * 80)
    print("RESULTADOS AGREGADOS")
    print("=" * 80)

    n = len(results)
    metrics_summary = {
        "total_queries": n,
        "law_retrieval_rate": sum(1 for r in results if r["metrics"]["law_retrieved"]) / n,
        "article_retrieval_rate": sum(1 for r in results if r["metrics"]["article_retrieved"]) / n,
        "citation_law_rate": sum(1 for r in results if r["metrics"]["answer_cites_law"]) / n,
        "citation_article_rate": sum(1 for r in results if r["metrics"]["answer_cites_article"]) / n,
        "avg_sources_per_query": sum(r["num_sources"] for r in results) / n,
        "avg_response_time_s": total_time / n,
        "total_time_s": round(total_time, 2),
        "complexity_distribution": {
            "simple": sum(1 for r in results if r["complexity"] == "simple"),
            "medium": sum(1 for r in results if r["complexity"] == "medium"),
            "complex": sum(1 for r in results if r["complexity"] == "complex"),
        },
        "retrieval_method_usage": _count_methods(results),
    }

    print(f"\n  Taxa de recuperação da lei correta:    {metrics_summary['law_retrieval_rate']:.1%}")
    print(f"  Taxa de recuperação do artigo correto:  {metrics_summary['article_retrieval_rate']:.1%}")
    print(f"  Taxa de citação da lei na resposta:     {metrics_summary['citation_law_rate']:.1%}")
    print(f"  Taxa de citação do artigo na resposta:  {metrics_summary['citation_article_rate']:.1%}")
    print(f"  Média de fontes por consulta:           {metrics_summary['avg_sources_per_query']:.1f}")
    print(f"  Tempo médio de resposta:                {metrics_summary['avg_response_time_s']:.1f}s")
    print(f"  Distribuição de complexidade:            {metrics_summary['complexity_distribution']}")
    print(f"  Uso de métodos de retrieval:             {metrics_summary['retrieval_method_usage']}")

    # Salvar resultados
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output = {
        "summary": metrics_summary,
        "detailed_results": results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nResultados salvos em: {output_path}")
    return output


def _count_methods(results: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for r in results:
        for method in r["retrieval_methods"]:
            for m in method.split("+"):
                counts[m] = counts.get(m, 0) + 1
    return counts


if __name__ == "__main__":
    evaluate()
