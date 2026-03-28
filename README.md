# EcoLex RAG

Sistema HyPA-RAG (Hybrid Parameter-Adaptive Retrieval-Augmented Generation) para suporte explicavel a decisao em gestao ambiental brasileira.

Combina **BM25** (sparse) + **Legal-BERTimbau** (dense) + **Knowledge Graph** com **Reciprocal Rank Fusion** e **Mistral 7B Instruct**, entregando respostas ancoradas na legislacao ambiental brasileira com citacao exata de artigos, paragrafos e incisos.

## Arquitetura

```
Query do gestor
       |
[Classificador de Complexidade]  -->  simples | medio | complexo
       |
[Parametros Adaptativos: k=5/10/15, rewrites=0/1/3]
       |
+-------------+----------------------+-----------------+
|    BM25      |  Legal-BERTimbau     |   Knowledge     |
|  (keywords)  |  + FAISS (semantico) |  Graph (triplets)|
+------+-------+----------+----------+--------+--------+
       |                  |                    |
       +--------> Reciprocal Rank Fusion <-----+
                          |
              [Mistral 7B Instruct FP16]
                          |
             Resposta explicavel + fontes exatas
```

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | FastAPI + Uvicorn |
| RAG Framework | LangChain + HyPA-RAG |
| Sparse Retrieval | BM25 (rank-bm25) |
| Dense Retrieval | Legal-BERTimbau + FAISS |
| Knowledge Graph | Triplets extraidos da estrutura legal (Art, Par., inciso) |
| Fusao | Reciprocal Rank Fusion (RRF) |
| LLM | Mistral 7B Instruct v0.3 (FP16) |
| Avaliacao | Metricas de citacao e retrieval |

## Requisitos

- Python 3.11+
- GPU com >= 16GB VRAM (para Mistral 7B FP16)
- ~14GB de espaco em disco para o modelo

## Instalacao

```bash
git clone https://github.com/vsousadelvek/ecolex-rag.git
cd ecolex-rag

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt

cp .env.example .env
```

## Uso

### 1. Adicionar legislacao

Coloque arquivos `.txt` ou `.pdf` das legislacoes em `data/legislation/`:

```
data/legislation/
  codigo_florestal.txt
  pnma.txt
  snuc.txt
  crimes_ambientais.txt
  conama_357.txt
  conama_430.txt
```

### 2. Ingerir legislacao

```bash
# Ingerir todos os arquivos do diretorio
python -m scripts.ingest

# Ingerir arquivo especifico
python -m scripts.ingest --file data/legislation/codigo_florestal.txt --name "Codigo Florestal - Lei 12.651/2012"
```

### 3. Iniciar API

```bash
uvicorn app.main:app --reload
```

### 4. Consultar

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Qual a largura minima de APP para rios com menos de 10 metros?"}'
```

Resposta:

```json
{
  "answer": "FUNDAMENTACAO LEGAL: Conforme Art. 4, inciso I, alinea 'a' do Codigo Florestal (Lei 12.651/2012), ...",
  "sources": [
    {
      "content": "[Codigo Florestal] Art. 4 ...",
      "law_name": "Codigo Florestal - Lei 12.651/2012",
      "article": "Art. 4",
      "score": 0.847,
      "retrieval_method": "bm25+semantic"
    }
  ],
  "hypa_params": {
    "complexity": "simple",
    "top_k": 5,
    "query_rewrites": 0
  },
  "processing_time_ms": 2340.5
}
```

### 5. Avaliar

```bash
python -m scripts.evaluate
```

Gera metricas sobre 10 consultas de referencia:

- Taxa de recuperacao da lei correta
- Taxa de recuperacao do artigo correto
- Taxa de citacao na resposta
- Distribuicao de complexidade
- Tempo medio de resposta

Resultados salvos em `data/evaluation_results.json`.

## API Endpoints

| Metodo | Rota | Descricao |
|---|---|---|
| POST | `/api/query` | Consulta em linguagem natural |
| POST | `/api/ingest` | Ingestao de nova legislacao |
| GET | `/api/health` | Status dos servicos |
| GET | `/api/legislation` | Lista legislacoes ingeridas |
| GET | `/docs` | Swagger UI |

## HyPA-RAG: Parametros Adaptativos

O sistema classifica cada query em tres niveis de complexidade e ajusta automaticamente os parametros de retrieval:

| Complexidade | top_k | Query Rewrites | Exemplo |
|---|---|---|---|
| Simples | 5 | 0 | "O que e APP?" |
| Media | 10 | 1 | "Qual a faixa de APP para rio de 10m?" |
| Complexa | 15 | 3 | "Compare as exigencias de APP e Reserva Legal para propriedade na Amazonia Legal" |

## Docker

```bash
docker compose up --build
```

## Legislacao suportada

- Codigo Florestal (Lei 12.651/2012)
- Politica Nacional do Meio Ambiente (Lei 6.938/1981)
- SNUC (Lei 9.985/2000)
- Lei de Crimes Ambientais (Lei 9.605/1998)
- Resolucoes CONAMA (357, 430, 302, 303)

## Referencias

- Kalra et al. (2024). *HyPA-RAG: A Hybrid Parameter Adaptive Retrieval-Augmented Generation System for AI Legal and Policy Applications*. arXiv:2409.09046
- Souza & Nogueira (2020). *BERTimbau: Pretrained BERT Models for Brazilian Portuguese*. PROPOR 2020
- Jiang et al. (2023). *Mistral 7B*. arXiv:2310.06825
- Rufimelo et al. (2022). *Legal-BERTimbau*. Semantic Textual Similarity for Portuguese Legal Domain

## Licenca

MIT
