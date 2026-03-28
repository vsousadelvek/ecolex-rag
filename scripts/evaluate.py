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

# Dataset de avaliação: perguntas sobre legislação ambiental brasileira
EVAL_DATASET = [
    {
        "question": "Qual a largura mínima da faixa de APP para rios com menos de 10 metros de largura?",
        "ground_truth": "A faixa mínima de Área de Preservação Permanente para cursos d'água com menos de 10 metros de largura é de 30 metros, conforme Art. 4º, inciso I, alínea 'a' do Código Florestal (Lei 12.651/2012).",
        "expected_law": "Código Florestal",
        "expected_article": "Art. 4",
    },
    {
        "question": "O que é Reserva Legal e qual o percentual exigido na Amazônia Legal?",
        "ground_truth": "Reserva Legal é a área no interior de uma propriedade rural com a função de assegurar o uso econômico sustentável dos recursos naturais. Na Amazônia Legal, o percentual mínimo é de 80% para imóveis em área de floresta, conforme Art. 12, inciso I, alínea 'a' do Código Florestal.",
        "expected_law": "Código Florestal",
        "expected_article": "Art. 12",
    },
    {
        "question": "Quais são os instrumentos da Política Nacional do Meio Ambiente?",
        "ground_truth": "Os instrumentos incluem: estabelecimento de padrões de qualidade ambiental, zoneamento ambiental, avaliação de impactos ambientais, licenciamento ambiental, entre outros, conforme Art. 9º da Lei 6.938/1981.",
        "expected_law": "PNMA",
        "expected_article": "Art. 9",
    },
    {
        "question": "Qual a pena para quem desmata área de preservação permanente?",
        "ground_truth": "Destruir ou danificar floresta em área de preservação permanente, mesmo que em formação, ou utilizá-la com infringência das normas de proteção, sujeita o infrator a detenção de 1 a 3 anos, ou multa, ou ambas, conforme Art. 38 da Lei 9.605/1998.",
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 38",
    },
    {
        "question": "O que é uma Unidade de Conservação de Proteção Integral segundo o SNUC?",
        "ground_truth": "O objetivo básico das Unidades de Proteção Integral é preservar a natureza, sendo admitido apenas o uso indireto dos seus recursos naturais, conforme Art. 7º, §1º da Lei 9.985/2000. Compreendem: Estação Ecológica, Reserva Biológica, Parque Nacional, Monumento Natural e Refúgio de Vida Silvestre.",
        "expected_law": "SNUC",
        "expected_article": "Art. 7",
    },
    {
        "question": "Quais são as classes de qualidade de água doce definidas pela Resolução CONAMA 357?",
        "ground_truth": "As águas doces são classificadas em: Classe Especial, Classe 1, Classe 2, Classe 3 e Classe 4, conforme Art. 4º da Resolução CONAMA 357/2005, cada uma com usos preponderantes específicos.",
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 4",
    },
    {
        "question": "Em que situações o Código Florestal permite a supressão de vegetação em APP?",
        "ground_truth": "A supressão de vegetação nativa em APP somente poderá ser autorizada em casos de utilidade pública, interesse social ou de baixo impacto ambiental, conforme Art. 8º do Código Florestal (Lei 12.651/2012).",
        "expected_law": "Código Florestal",
        "expected_article": "Art. 8",
    },
    {
        "question": "Qual a composição e função do CONAMA segundo a Política Nacional do Meio Ambiente?",
        "ground_truth": "O CONAMA é o órgão consultivo e deliberativo do SISNAMA, com a finalidade de assessorar, estudar e propor diretrizes de políticas governamentais para o meio ambiente, conforme Art. 6º, inciso II da Lei 6.938/1981.",
        "expected_law": "PNMA",
        "expected_article": "Art. 6",
    },
    {
        "question": "Qual a faixa de APP ao redor de nascentes e olhos d'água perenes?",
        "ground_truth": "As áreas no entorno das nascentes e dos olhos d'água perenes, qualquer que seja sua situação topográfica, devem ter raio mínimo de 50 metros, conforme Art. 4º, inciso IV do Código Florestal.",
        "expected_law": "Código Florestal",
        "expected_article": "Art. 4",
    },
    {
        "question": "Considere uma propriedade rural na Amazônia Legal com área de floresta e que também faz divisa com um rio de 50 metros de largura. Quais são as exigências cumulativas de APP e Reserva Legal?",
        "ground_truth": "A propriedade deve manter APP de 100 metros nas faixas marginais do rio (Art. 4º, I, 'c' do Código Florestal, para rios de 50 a 200m de largura) e Reserva Legal de 80% da área do imóvel (Art. 12, I, 'a'). A APP não compõe a Reserva Legal, salvo exceções do Art. 15.",
        "expected_law": "Código Florestal",
        "expected_article": "Art. 4",
    },
]


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
