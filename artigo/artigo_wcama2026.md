# EcoLex RAG: Sistema HyPA-RAG com Legal-BERTimbau para Suporte Explicavel a Decisao em Gestao Ambiental Brasileira

**Delvek da Silva Venceslau de Sousa**

Universidade Federal do Para (UFPA) -- Belem, PA -- Brasil

delvek.sousa@icen.ufpa.br

---

## Resumo

A gestao ambiental brasileira demanda consulta frequente a um corpus legislativo extenso e hierarquicamente complexo, tarefa que impoe desafios significativos a gestores publicos e analistas ambientais. Este trabalho apresenta o EcoLex RAG, um sistema de Geracao Aumentada por Recuperacao com Parametros Hibridos Adaptativos (HyPA-RAG) voltado ao suporte explicavel a decisao em gestao ambiental. A arquitetura proposta integra tres mecanismos de recuperacao -- BM25 (*sparse*), Legal-BERTimbau/FAISS (*dense*) e Knowledge Graph legal -- unificados via Reciprocal Rank Fusion, com parametros adaptativos controlados por um classificador de complexidade de consultas. A geracao de respostas e realizada pelo Mistral 7B Instruct em FP16, com prompts estruturados que exigem citacao exata de artigos, paragrafos e incisos. Um estudo de ablacao com 100 consultas sobre 6 legislacoes demonstrou que a configuracao HyPA-RAG alcanca desempenho competitivo em recuperacao e citacao (65% em Lei Retrieval, 48% em Citation Article Rate) utilizando em media apenas 6,8 fontes, contra 10,0 das configuracoes estaticas, evidenciando eficiencia superior na economia de contexto. Em consultas de complexidade media, o sistema atinge 54% em Citation Article Rate, superando todas as demais configuracoes. Os resultados indicam que a adaptacao parametrica viabiliza sistemas RAG mais eficientes para o dominio juridico-ambiental brasileiro.

**Palavras-chave:** Geracao Aumentada por Recuperacao, Legislacao Ambiental, HyPA-RAG, Legal-BERTimbau, Inteligencia Artificial Explicavel.

---

## Abstract

Brazilian environmental management demands frequent consultation of an extensive and hierarchically complex legislative corpus, a task that poses significant challenges to public administrators and environmental analysts. This paper presents EcoLex RAG, a Hybrid Parameter-Adaptive Retrieval-Augmented Generation (HyPA-RAG) system for explainable decision support in environmental management. The proposed architecture integrates three retrieval mechanisms -- BM25 (sparse), Legal-BERTimbau/FAISS (dense), and a legal Knowledge Graph -- unified via Reciprocal Rank Fusion, with adaptive parameters controlled by a query complexity classifier. Response generation is performed by Mistral 7B Instruct in FP16, with structured prompts requiring exact citation of articles, paragraphs, and clauses. An ablation study with 100 queries across 6 legislative acts demonstrated that the HyPA-RAG configuration achieves competitive retrieval and citation performance (65% Law Retrieval, 48% Citation Article Rate) using on average only 6.8 sources compared to 10.0 in static configurations, evidencing superior context efficiency. For medium-complexity queries, the system reaches 54% Citation Article Rate, outperforming all other configurations. Results indicate that parametric adaptation enables more efficient RAG systems for the Brazilian legal-environmental domain.

**Keywords:** Retrieval-Augmented Generation, Environmental Legislation, HyPA-RAG, Legal-BERTimbau, Explainable Artificial Intelligence.

---

## 1. Introducao

O Brasil detém um dos arcaboucos normativos ambientais mais extensos e sofisticados do planeta, abrangendo desde o Codigo Florestal (Lei 12.651/2012), que disciplina a protecao de Areas de Preservacao Permanente (APP) e Reservas Legais, ate a Politica Nacional do Meio Ambiente (Lei 6.938/1981), que institui o Sistema Nacional do Meio Ambiente (SISNAMA), passando pelo Sistema Nacional de Unidades de Conservacao (Lei 9.985/2000), a Lei de Crimes Ambientais (Lei 9.605/1998) e diversas resolucoes do Conselho Nacional do Meio Ambiente (CONAMA). A estrutura hierarquica dessas normas -- organizadas em artigos, paragrafos, incisos, alineas e dispositivos remissivos entre leis distintas -- impoe uma carga cognitiva substancial a gestores publicos, analistas ambientais e operadores do direito ambiental que necessitam fundamentar suas decisoes em dispositivos legais especificos [Robertson e Zaragoza 2009].

Esse cenario adquire relevancia estrategica inedita no contexto pos-COP30 (Conferencia das Nacoes Unidas sobre Mudancas Climaticas), realizada em Belem do Para em novembro de 2025, evento que reposicionou o Brasil -- e particularmente a regiao amazonica -- no epicentro das discussoes globais sobre governanca climatica e bioeconomia. As metas assumidas pelo pais durante a COP30 exigem, em termos praticos, que orgaos ambientais estaduais e municipais operem com maior agilidade e precisao no enquadramento legal de atividades economicas, licenciamentos e fiscalizacoes. A ausencia de ferramentas computacionais adequadas para consulta inteligente a legislacao constitui, portanto, um gargalo operacional com implicacoes diretas sobre a efetividade da governanca ambiental brasileira.

No campo da Inteligencia Artificial, a tecnica de Geracao Aumentada por Recuperacao (RAG -- *Retrieval-Augmented Generation*) [Lewis et al. 2020] emergiu como paradigma dominante para a construcao de sistemas de pergunta-resposta fundamentados em bases de conhecimento, mitigando o problema de alucinacao factual em Modelos de Linguagem de Grande Escala (LLMs). Entretanto, a aplicacao direta de arquiteturas RAG convencionais ao dominio juridico-ambiental brasileiro enfrenta tres lacunas fundamentais: (i) modelos de *embedding* genericos nao capturam adequadamente a semantica de termos legais em portugues, como "Area de Preservacao Permanente", "Reserva Legal" ou "outorga de recurso hidrico"; (ii) a ausencia de mecanismos que explorem a estrutura hierarquica intrinseca da legislacao (Lei > Capitulo > Secao > Artigo > Paragrafo > Inciso > Alinea) desperdiça informacao relacional valiosa; e (iii) a rigidez parametrica de sistemas RAG tradicionais -- que operam com valores fixos de documentos recuperados independentemente da complexidade da consulta -- conduz a ineficiencia tanto na economia de contexto quanto na qualidade da resposta.

Recentemente, Kalra et al. (2024) propuseram o HyPA-RAG (*Hybrid Parameter-Adaptive Retrieval-Augmented Generation*), uma arquitetura que combina recuperacao hibrida (sparse + dense + knowledge graph) com adaptacao parametrica baseada na complexidade da consulta, demonstrando resultados promissores no dominio juridico anglofono. Contudo, a transferencia direta dessa arquitetura ao contexto legal brasileiro permanece inexplorada na literatura.

O presente trabalho propoe o **EcoLex RAG**, um sistema HyPA-RAG adaptado ao dominio juridico-ambiental brasileiro, cujas contribuicoes principais sao:

1. **Recuperacao hibrida tripla adaptada ao dominio legal brasileiro**, integrando BM25 (*sparse*), Legal-BERTimbau/FAISS (*dense*) [Rufimelo et al. 2022] e um Knowledge Graph legal com triplets extraidos da estrutura normativa, unificados via Reciprocal Rank Fusion (RRF) [Cormack et al. 2009];
2. **Classificador de complexidade de consultas** baseado em heuristicas juridico-linguisticas, que governa a adaptacao de parametros (top_k e *query rewrites*) por nivel de complexidade (simples, medio, complexo);
3. **Pipeline de geracao explicavel** com Mistral 7B Instruct [Jiang et al. 2023] em FP16, estruturado para produzir respostas com citacao exata de dispositivos legais (artigo, paragrafo, inciso);
4. **Estudo de ablacao abrangente** com 100 consultas distribuidas em tres niveis de complexidade sobre 6 legislacoes ambientais, avaliando sistematicamente a contribuicao de cada componente da arquitetura.

O restante deste artigo esta organizado da seguinte forma: a Secao 2 revisa os trabalhos relacionados; a Secao 3 detalha a metodologia e a arquitetura do sistema; a Secao 4 descreve o protocolo experimental; a Secao 5 apresenta e discute os resultados; e a Secao 6 conclui o trabalho com direcionamentos futuros.

---

## 2. Trabalhos Relacionados

Esta secao situa o EcoLex RAG no panorama da literatura em tres eixos: Geracao Aumentada por Recuperacao, modelos de linguagem para o portugues juridico e aplicacoes de IA na gestao ambiental.

### 2.1. Geracao Aumentada por Recuperacao (RAG)

Lewis et al. (2020) formalizaram o paradigma RAG ao demonstrar que a concatenacao de documentos recuperados de uma base de conhecimento ao *prompt* de um modelo seq2seq (*sequence-to-sequence*) produz respostas mais factuais do que modelos puramente generativos. Desde entao, a arquitetura RAG tornou-se o padrao *de facto* para sistemas de pergunta-resposta em dominios especializados, sendo adotada em contextos medicos, juridicos e financeiros.

A recuperacao *sparse* via BM25 [Robertson e Zaragoza 2009] permanece como *baseline* robusto, particularmente eficaz na correspondencia de termos exatos -- propriedade critica no dominio legal, onde identificadores normativos como "Art. 4o" ou "Resolucao CONAMA 357" constituem tokens de alta especificidade. Paralelamente, a recuperacao *dense* baseada em modelos de *embedding* captura relacoes semanticas que escapam a correspondencia lexica, sendo especialmente util em consultas formuladas em linguagem natural por usuarios nao especializados.

### 2.2. HyPA-RAG: Recuperacao Hibrida com Parametros Adaptativos

Kalra et al. (2024) introduziram o HyPA-RAG (*Hybrid Parameter-Adaptive Retrieval-Augmented Generation*), uma extensao do paradigma RAG que endereça duas limitacoes fundamentais das arquiteturas convencionais. Primeiramente, o HyPA-RAG combina tres modalidades de recuperacao -- *sparse* (BM25), *dense* (*embeddings*) e *graph-based* (Knowledge Graph) -- mediante Reciprocal Rank Fusion (RRF), proposta originalmente por Cormack et al. (2009). Em segundo lugar, a arquitetura classifica cada consulta em niveis de complexidade e adapta dinamicamente os parametros de recuperacao (numero de documentos, reformulacoes de consulta), evitando tanto a subrecuperacao em consultas complexas quanto o desperdicio de contexto em consultas simples. Os autores demonstraram ganhos significativos em benchmarks juridicos em lingua inglesa, particularmente em consultas que exigem raciocinio *multi-hop* entre dispositivos normativos.

A formula do RRF, que constitui o nucleo da fusao de rankings no EcoLex RAG, e definida como:

$$\text{RRF}_{score}(d) = \sum_{r \in R} \frac{1}{k + \text{rank}_r(d)}$$

onde $R$ denota o conjunto de listas de ranking (BM25, semantico, Knowledge Graph), $\text{rank}_r(d)$ e a posicao do documento $d$ na lista $r$, e $k = 60$ e a constante de suavizacao do *paper* original [Cormack et al. 2009]. A fusao por RRF dispensa calibracao de pesos entre modelos heterogeneos, propriedade particularmente vantajosa quando os escores dos diferentes *retrievers* residem em escalas incomparaveis.

### 2.3. Modelos de Linguagem para o Portugues Juridico

O BERTimbau [Souza e Nogueira 2020] estabeleceu o primeiro modelo BERT pre-treinado especificamente para o portugues brasileiro, treinado sobre um corpus de 2,7 bilhoes de tokens extraidos do *BrWaC* (*Brazilian Web as Corpus*). Subsequentemente, Rufimelo et al. (2022) apresentaram o Legal-BERTimbau, uma variante do BERTimbau submetida a treinamento continuo sobre um corpus juridico em portugues, demonstrando ganhos consistentes em tarefas de *Semantic Textual Similarity* (STS) no dominio legal. O modelo `rufimelo/Legal-BERTimbau-sts-base-ma`, com dimensao de *embedding* de 768, e particularmente adequado para a geracao de representacoes vetoriais de trechos legislativos brasileiros, capturando nuances semanticas que modelos genericos nao discriminam.

Para a geracao de respostas, o Mistral 7B [Jiang et al. 2023] emergiu como uma alternativa eficiente a modelos de maior escala, oferecendo desempenho competitivo com LLMs de 13 bilhoes de parametros gracas ao mecanismo de atencao de janela deslizante (*Sliding Window Attention*) e agrupamento de consultas (*Grouped-Query Attention*). A variante Instruct, ajustada via *Reinforcement Learning from Human Feedback* (RLHF), demonstra capacidade superior de seguir instrucoes estruturadas, propriedade essencial para a geracao de respostas com citacao legal obrigatoria.

### 2.4. IA Aplicada a Gestao Ambiental e Explicabilidade

A interseccao entre IA e gestao ambiental tem avancado substancialmente, com aplicacoes que vao desde a deteccao de desmatamento por visao computacional ate a modelagem preditiva de dinamicas climaticas [WCAMA 2025]. Contudo, a vertente de suporte a decisao juridico-ambiental permanece subexplorada. No contexto da governanca publica, a demanda por Inteligencia Artificial Explicavel (XAI -- *Explainable Artificial Intelligence*) tornou-se imperativa: decisoes administrativas fundamentadas em recomendacoes de IA devem ser auditaveis e rastreavéis aos dispositivos normativos que as embasam. Sistemas RAG com citacao de fontes representam, nesse sentido, uma forma nativa de explicabilidade, na medida em que cada afirmacao da resposta pode ser verificada contra o trecho legislativo original.

A edicao de 2025 do WCAMA evidenciou a maturidade da ecoinformatica brasileira e a crescente adocao de tecnicas como RAG e XAI para problemas ambientais, sinalizando que o campo esta receptivo a contribuicoes que integrem processamento de linguagem natural, representacao de conhecimento legal e suporte a decisao governamental.

---

## 3. Metodologia

Esta secao detalha a arquitetura do sistema EcoLex RAG, abordando cada componente do pipeline HyPA-RAG: classificacao de complexidade, recuperacao tripla, fusao de rankings, adaptacao parametrica e geracao de respostas explicaveis.

### 3.1. Visao Geral da Arquitetura

O EcoLex RAG implementa um pipeline HyPA-RAG completo, cujo fluxo de processamento e ilustrado na Figura 1. Uma consulta em linguagem natural ingressada pelo gestor ambiental percorre cinco estagios sequenciais: (1) classificacao de complexidade; (2) adaptacao de parametros; (3) recuperacao tripla com fusao; (4) geracao de resposta com LLM; e (5) entrega de resposta explicavel com fontes exatas.

```
  Consulta do Gestor Ambiental
              |
              v
  +----------------------------+
  | Classificador de           |
  | Complexidade               |
  | (heuristicas linguisticas) |
  +----------------------------+
              |
              v
  +----------------------------+
  | Parametros Adaptativos     |
  | k=5/10/15                  |
  | rewrites=0/1/3             |
  +----------------------------+
              |
    +---------+---------+
    |         |         |
    v         v         v
+--------+ +--------+ +--------+
|  BM25  | | Legal- | | Know-  |
| Okapi  | | BERT-  | | ledge  |
|(sparse)| | imbau  | | Graph  |
|        | | +FAISS | |(triplets|
|        | |(dense) | | legais)|
+---+----+ +---+----+ +---+----+
    |         |         |
    +---------+---------+
              |
              v
  +----------------------------+
  | Reciprocal Rank Fusion     |
  | RRF(d) = Sum 1/(k+rank(d))|
  +----------------------------+
              |
              v
  +----------------------------+
  | Mistral 7B Instruct (FP16) |
  | Prompt: citacao obrigatoria|
  | Estrutura: FUNDAMENTACAO   |
  |   LEGAL > ANALISE >        |
  |   CONCLUSAO                |
  +----------------------------+
              |
              v
  +----------------------------+
  | Resposta Explicavel        |
  | + Fontes com Lei/Art/Par   |
  | + Metadados HyPA           |
  +----------------------------+
```
**Figura 1.** Arquitetura do pipeline HyPA-RAG do EcoLex RAG. A consulta e classificada em tres niveis de complexidade, que governam os parametros adaptativos dos tres *retrievers* operando em paralelo. A fusao via RRF alimenta o LLM com contexto legislativo ranqueado, e a resposta e entregue com citacao obrigatoria de fontes.

### 3.2. Classificador de Complexidade

O classificador de complexidade constitui o componente que diferencia a abordagem HyPA-RAG de sistemas RAG tradicionais com parametros estaticos. Dado que consultas juridicas variam enormemente em profundidade -- de perguntas factuais diretas ("O que e APP?") a consultas comparativas *multi-hop* ("Compare as exigencias de APP e Reserva Legal para propriedade na Amazonia Legal") --, a adaptacao parametrica permite alocar recursos computacionais proporcionalmente a demanda informacional de cada consulta.

O classificador opera sobre heuristicas linguisticas especificas do dominio juridico-ambiental, computando um *complexity score* $s$ baseado em seis indicadores extraidos da consulta $q$:

Seja $q$ uma consulta tokenizada em palavras $w_1, w_2, \ldots, w_n$. O escore de complexidade e calculado como:

$$s(q) = \min(\lambda_L, 3) + 2 \cdot \mathbb{1}_{C}(q) + \mathbb{1}_{D}(q) + 2 \cdot \mathbb{1}_{M}(q) + \mathbb{1}_{?}(q) + \mathbb{1}_{\wedge}(q) + \mathbb{1}_{|q|>30}$$

onde:
- $\lambda_L = |\{t \in \mathcal{T}_L : t \subset q\}|$ e a contagem de termos legais reconhecidos, limitada a 3, com $\mathcal{T}_L$ sendo o lexico de 36 termos juridico-ambientais (e.g., "reserva legal", "licenciamento", "CONAMA", "outorga", "recurso hidrico");
- $\mathbb{1}_{C}(q)$ indica presenca de marcadores comparativos ("compare", "diferença", "versus");
- $\mathbb{1}_{D}(q)$ indica presenca de marcadores condicionais ("se", "caso", "na hipotese de");
- $\mathbb{1}_{M}(q)$ indica presenca de marcadores *multi-hop* ("adicionalmente", "cumulativamente", "a luz de");
- $\mathbb{1}_{?}(q)$ indica mais de um ponto de interrogacao;
- $\mathbb{1}_{\wedge}(q)$ indica duas ou mais conjuncoes ("e", "ou", "mas", "porem");
- $\mathbb{1}_{|q|>30}$ indica que a consulta excede 30 palavras.

A classificacao final mapeia o escore a tres niveis:

$$\text{complexidade}(q) = \begin{cases} \texttt{simple} & \text{se } s(q) \leq 2 \\ \texttt{medium} & \text{se } 3 \leq s(q) \leq 5 \\ \texttt{complex} & \text{se } s(q) \geq 6 \end{cases}$$

### 3.3. Recuperacao Tripla

O modulo de recuperacao opera simultaneamente tres estrategias complementares para maximizar a cobertura e a precisao na identificacao de trechos legislativos relevantes.

**BM25 Okapi (*sparse*).** O algoritmo BM25 [Robertson e Zaragoza 2009] realiza recuperacao baseada em correspondencia lexica, computando a relevancia de cada *chunk* legislativo em funcao da frequencia dos termos da consulta, ponderada pela frequencia inversa no corpus e pelo comprimento do documento. A tokenizacao e realizada por *whitespace splitting* em *lowercase*, sem *stemming*, preservando a integridade de identificadores normativos (e.g., "Art. 4o", "CONAMA 357"). O indice BM25 e construido sobre 473 *chunks* extraidos de 6 legislacoes, armazenados em formato JSON.

**Legal-BERTimbau + FAISS (*dense*).** A recuperacao densa utiliza o modelo `rufimelo/Legal-BERTimbau-sts-base-ma` [Rufimelo et al. 2022] para gerar *embeddings* de dimensao $d = 768$ para cada *chunk* legislativo. Os vetores sao normalizados via $L_2$ e indexados em uma estrutura FAISS `IndexFlatIP` (*Inner Product*), que computa a similaridade por produto interno (equivalente a similaridade cosseno apos normalizacao). A busca por similaridade retorna os $k$ *chunks* mais proximos ao vetor da consulta no espaco semantico.

**Knowledge Graph Legal (*graph-based*).** O Knowledge Graph (KG) e construido a partir da estrutura hierarquica intrinseca da legislacao brasileira. Um extrator baseado em expressoes regulares processa o texto legislativo e gera triplets no formato $(sujeito, relacao, objeto)$, onde as relacoes capturam quatro tipos de vinculos:
- `pertence_a`: artigo pertence a uma lei;
- `detalha`: paragrafo detalha um artigo;
- `define`: inciso define um conceito dentro de um artigo;
- `definido_em`: conceito legal e definido em um artigo especifico;
- `estabelece_medida`: artigo estabelece medida quantitativa (metros, hectares, percentuais).

A busca no KG opera por correspondencia de termos entre a consulta e os campos dos triplets, com *boost* de 0,3 para *matches* no campo `subject` e 0,2 para *matches* no campo `object`. Cada triplet retornado e formatado como *chunk* textual contendo a relacao e o contexto associado (limitado a 300 caracteres).

### 3.4. Reciprocal Rank Fusion

Os resultados dos tres *retrievers* sao unificados via Reciprocal Rank Fusion (RRF) [Cormack et al. 2009]. Para cada documento $d$ presente em ao menos uma lista de resultados, o escore RRF e calculado como:

$$\text{RRF}_{score}(d) = \sum_{r \in \{BM25, Dense, KG\}} \frac{1}{k + \text{rank}_r(d)}$$

com $k = 60$ (constante de suavizacao padrao). Documentos ausentes em uma lista nao contribuem para a soma. Os documentos fusionados sao ordenados por escore RRF decrescente, e os top-$n$ sao selecionados como contexto para o LLM. A deduplicacao e realizada por identidade dos primeiros 200 caracteres do conteudo, garantindo que *chunks* identicos recuperados por *retrievers* distintos nao sejam contados duplamente. O metadado `retrieval_method` do *chunk* fusionado registra todos os metodos que o recuperaram (e.g., "bm25+semantic"), viabilizando auditoria do pipeline.

### 3.5. Parametros Adaptativos

A adaptacao parametrica constitui o nucleo diferenciador da arquitetura HyPA-RAG em relacao a sistemas RAG convencionais. Com base na classificacao de complexidade da consulta (Secao 3.2), o pipeline ajusta dois parametros: (i) o numero de documentos recuperados por cada *retriever* ($top\_k$) e (ii) o numero de reformulacoes de consulta (*query rewrites*) geradas pelo LLM para ampliar a cobertura lexica e semantica da busca. A Tabela 1 apresenta a configuracao adotada.

**Tabela 1.** Parametros adaptativos do HyPA-RAG por nivel de complexidade.

| Complexidade | $top\_k$ | *Query Rewrites* | Exemplo de consulta |
|:---:|:---:|:---:|:---|
| Simples | 5 | 0 | "O que e APP?" |
| Media | 10 | 1 | "Qual a faixa de APP para rio de 10m?" |
| Complexa | 15 | 3 | "Compare as exigencias de APP e Reserva Legal para propriedade na Amazonia Legal" |

A reducao do $top\_k$ para consultas simples economiza contexto no *prompt* do LLM, diminuindo o custo computacional de inferencia e mitigando o risco de "diluicao" da resposta por *chunks* irrelevantes. As reformulacoes de consulta (*query rewrites*) sao geradas pelo proprio Mistral 7B com temperatura de 0,3, produzindo variacoes linguisticas da pergunta original (e.g., sinonimos de termos legais, reestruturacoes sintaticas) que ampliam o espaco de busca nos *retrievers*.

### 3.6. Geracao com Mistral 7B Instruct

A geracao de respostas e realizada pelo modelo Mistral 7B Instruct v0.3 [Jiang et al. 2023], carregado em precisao FP16 (*float16*) com mapeamento automatico de dispositivo (`device_map="auto"`), exigindo aproximadamente 14 GB de VRAM. O pipeline de geracao utiliza a biblioteca Hugging Face `transformers` com os seguintes hiperparametros: `max_new_tokens=1024`, `temperature=0.1` e `do_sample=True`.

O *prompt* do sistema e estruturado com seis regras obrigatorias que constituem o mecanismo de explicabilidade do EcoLex RAG: (1) responder exclusivamente com base nos trechos legislativos fornecidos; (2) citar a fonte exata (lei, artigo, paragrafo, inciso); (3) declarar explicitamente a insuficiencia de informacao quando aplicavel; (4) utilizar linguagem tecnica acessivel a gestores publicos; (5) estruturar a resposta em FUNDAMENTACAO LEGAL, ANALISE e CONCLUSAO; e (6) nao inventar dispositivos legais ausentes do contexto.

O contexto legislativo e formatado como sequencia de *chunks*, cada um prefixado com os metadados `[lei | artigo]`, limitados a 800 caracteres e ate 3.000 tokens estimados no total, garantindo operacao dentro da janela de contexto do modelo sem exceder a capacidade da VRAM.

### 3.7. Knowledge Graph Legal: Extracao de Triplets

A construcao do Knowledge Graph legal e realizada por um extrator baseado em expressoes regulares que processa o texto integral de cada legislacao. O extrator reconhece cinco padroes estruturais:

1. **Artigos**: padrao `Art.\s*\d+[\w-]*` identifica todos os artigos e associa cada um a lei correspondente via triplet `(Art. X, pertence_a, Lei Y)`;
2. **Paragrafos**: padrao `§\s*\d+°?|Paragrafo unico` identifica paragrafos e os vincula ao artigo pai via `(Art. X, §Y, detalha, Art. X)`;
3. **Incisos**: identificadores romanos (I, II, III, ...) sao extraidos e vinculados ao artigo via `(Art. X, Inciso Y, define, Art. X)`;
4. **Definicoes**: padroes como "entende-se por", "considera-se" e "define-se como" extraem conceitos definidos na legislacao;
5. **Medidas quantitativas**: padroes numericos seguidos de unidades (metros, hectares, percentuais) extraem limites quantitativos estabelecidos pela norma.

Sobre as 6 legislacoes da base de conhecimento, o extrator gerou 1.714 triplets, constituindo uma representacao estruturada das relacoes normativas que complementa a recuperacao textual pura.

---

## 4. Experimentos

Esta secao descreve a base de conhecimento, o *dataset* de avaliacao, as configuracoes de ablacao, as metricas empregadas e o ambiente de *hardware*.

### 4.1. Base de Conhecimento

A base de conhecimento do EcoLex RAG compreende 6 legislacoes ambientais brasileiras, segmentadas em 473 *chunks* textuais e representadas por 1.714 triplets no Knowledge Graph. A Tabela 2 detalha a composicao da base.

**Tabela 2.** Legislacoes que compoem a base de conhecimento do EcoLex RAG.

| Legislacao | Tipo | Escopo Tematico |
|:---|:---:|:---|
| Codigo Florestal (Lei 12.651/2012) | Lei Federal | APP, Reserva Legal, supressao de vegetacao |
| PNMA (Lei 6.938/1981) | Lei Federal | Politica Nacional do Meio Ambiente, SISNAMA, licenciamento |
| SNUC (Lei 9.985/2000) | Lei Federal | Unidades de Conservacao, categorias de manejo |
| Lei de Crimes Ambientais (Lei 9.605/1998) | Lei Federal | Sancoes penais e administrativas ambientais |
| Resolucao CONAMA 357/2005 | Resolucao | Classificacao de corpos d'agua, padroes de qualidade |
| Resolucao CONAMA 430/2011 | Resolucao | Condicoes e padroes de lancamento de efluentes |

### 4.2. Dataset de Avaliacao

O *dataset* de avaliacao foi construido especificamente para este estudo, contendo 100 consultas em linguagem natural sobre as 6 legislacoes da base. Cada entrada do *dataset* contem: (i) a pergunta em linguagem natural; (ii) a resposta de referencia com fundamentacao legal; (iii) a lei esperada nos resultados de recuperacao; (iv) o artigo esperado; (v) o nivel de complexidade; e (vi) a categoria tematica. A distribuicao por complexidade e legislacao e apresentada na Tabela 3.

**Tabela 3.** Distribuicao do *dataset* de avaliacao por complexidade e legislacao.

| Legislacao | Simples | Media | Complexa | Total |
|:---|:---:|:---:|:---:|:---:|
| Codigo Florestal | 6 | 12 | 12 | 30 |
| PNMA | 6 | 5 | 5 | 16 |
| SNUC | 6 | 5 | 5 | 16 |
| Crimes Ambientais | 10 | 3 | 3 | 16 |
| CONAMA 357/2005 | 6 | 6 | 0 | 12 |
| CONAMA 430/2011 | 6 | 4 | 0 | 10 |
| **Total** | **40** | **35** | **25** | **100** |

A preponderancia do Codigo Florestal (30 perguntas) reflete sua centralidade na pratica da gestao ambiental e sua maior complexidade estrutural (artigos com multiplos paragrafos, incisos e alineas). As consultas complexas concentram-se nas leis de maior interrelacao normativa (Codigo Florestal, PNMA, SNUC, Crimes Ambientais), enquanto as resolucoes CONAMA, de escopo mais restrito, sao cobertas por consultas simples e medias.

### 4.3. Configuracoes de Ablacao

O estudo de ablacao avalia 6 configuracoes que isolam e combinam progressivamente os componentes do pipeline, permitindo mensurar a contribuicao individual e sinergica de cada *retriever*:

1. **BM25-only**: apenas recuperacao *sparse* via BM25 Okapi;
2. **Semantic-only**: apenas recuperacao *dense* via Legal-BERTimbau + FAISS;
3. **KG-only**: apenas recuperacao via Knowledge Graph legal;
4. **BM25+Semantic**: fusao via RRF dos *retrievers* BM25 e semantico (sem KG);
5. **Hibrido fixo**: fusao via RRF dos tres *retrievers* com parametros estaticos ($k = 10$, *rewrites* $= 0$);
6. **HyPA-RAG**: fusao via RRF dos tres *retrievers* com parametros adaptativos (Tabela 1).

As configuracoes 1-5 operam com $k = 10$ e 0 *rewrites* em todas as consultas, enquanto a configuracao 6 (HyPA-RAG) adapta estes parametros conforme a complexidade. Todas utilizam o mesmo LLM (Mistral 7B FP16) e o mesmo *prompt* de geracao.

### 4.4. Metricas de Avaliacao

Quatro metricas sao empregadas, abrangendo tanto a etapa de recuperacao quanto a de geracao:

- **Lei Retrieval Rate (LRR)**: fracao de consultas cujos resultados de recuperacao contem ao menos um *chunk* da lei esperada;
- **Article Retrieval Rate (ARR)**: fracao de consultas cujos resultados contem o artigo especifico esperado;
- **Citation Law Rate (CLR)**: fracao de respostas geradas que citam corretamente a lei esperada no corpo textual;
- **Citation Article Rate (CAR)**: fracao de respostas que citam o artigo especifico esperado.

As duas primeiras metricas avaliam a qualidade do *retriever*, enquanto as duas ultimas avaliam a qualidade *end-to-end* do pipeline (recuperacao + geracao). Adicionalmente, reporta-se o numero medio de fontes (Fontes) e o tempo medio de resposta em segundos.

### 4.5. Ambiente de *Hardware*

Todos os experimentos foram conduzidos em uma estacao de trabalho equipada com GPU NVIDIA GeForce RTX 5090 (24 GB VRAM), processador Intel Core Ultra 9 275HX e 64 GB de RAM DDR5. O Mistral 7B Instruct v0.3 foi carregado em precisao FP16, ocupando aproximadamente 14 GB de VRAM. A avaliacao completa (600 execucoes: 100 consultas x 6 configuracoes) consumiu aproximadamente 4,6 horas (16.610 segundos).

---

## 5. Resultados e Discussao

### 5.1. Resultados Gerais

A Tabela 4 apresenta os resultados agregados das 6 configuracoes de ablacao sobre as 100 consultas do *dataset*.

**Tabela 4.** Resultados do estudo de ablacao (metricas agregadas sobre 100 consultas).

| Configuracao | Lei Ret. | Art. Ret. | Cit. Lei | Cit. Art. | Fontes | Tempo(s) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| BM25-only | 65% | 70% | 63% | 45% | 10,0 | 26,2 |
| Semantic-only | 61% | 53% | 61% | 40% | 10,0 | 24,6 |
| KG-only | 56% | 35% | 58% | 31% | 10,0 | 20,3 |
| BM25+Semantic | 65% | 66% | 65% | 48% | 10,0 | 27,6 |
| Hibrido fixo | 65% | 59% | 66% | 49% | 10,0 | 23,8 |
| **HyPA-RAG** | **65%** | 56% | 65% | 48% | **6,8** | 43,5 |

### 5.2. Resultados por Complexidade: Consultas Complexas

A Tabela 5 apresenta o *breakdown* de desempenho para as 25 consultas de complexidade alta, que envolvem raciocinio *multi-hop*, comparacoes entre legislacoes e cenarios condicionais.

**Tabela 5.** Desempenho nas 25 consultas complexas (*multi-hop*, comparativas).

| Configuracao | Lei Ret. | Art. Ret. | Cit. Lei | Cit. Art. |
|:---|:---:|:---:|:---:|:---:|
| BM25-only | 68% | 60% | 68% | 40% |
| Semantic-only | 60% | 48% | 64% | 44% |
| KG-only | 60% | 20% | 64% | 36% |
| BM25+Semantic | 64% | 52% | 68% | 52% |
| Hibrido fixo | 64% | 36% | 72% | 48% |
| **HyPA-RAG** | 64% | 52% | 68% | **52%** |

### 5.3. Resultados por Complexidade: Consultas Medias

A Tabela 6 apresenta os resultados para as 35 consultas de complexidade media, tipicamente envolvendo condicionais e artigos com paragrafos.

**Tabela 6.** Desempenho nas 35 consultas de complexidade media (condicionais, paragrafos).

| Configuracao | Lei Ret. | Art. Ret. | Cit. Lei | Cit. Art. |
|:---|:---:|:---:|:---:|:---:|
| BM25-only | 66% | 63% | 63% | 43% |
| Semantic-only | 60% | 43% | 60% | 34% |
| KG-only | 57% | 31% | 54% | 23% |
| BM25+Semantic | 66% | 63% | 66% | 46% |
| Hibrido fixo | 66% | 63% | 66% | 49% |
| **HyPA-RAG** | 66% | 63% | 63% | **54%** |

### 5.4. Discussao

Os resultados do estudo de ablacao permitem extrair cinco constatacoes fundamentais sobre a dinamica dos componentes do EcoLex RAG.

**Superioridade do BM25 para termos legais exatos.** A configuracao BM25-only alcanca o melhor Article Retrieval Rate global (70%), superando em larga margem as abordagens Semantic-only (53%) e KG-only (35%). Este resultado e esperado e corrobora a literatura [Robertson e Zaragoza 2009]: identificadores normativos como "Art. 4o" e "CONAMA 357" sao tokens de alta especificidade cuja correspondencia lexica exata e mais eficaz do que a proximidade no espaco de *embeddings*. A recuperacao *dense*, por sua vez, captura relacoes semanticas uteis mas dilui a precisao ao trazer *chunks* tematicamente proximos porem normativamente distintos.

**Knowledge Graph isolado e limitado, mas contribui na fusao.** O KG-only apresenta o pior desempenho em todas as metricas (56% LRR, 35% ARR, 31% CAR), evidenciando que a recuperacao puramente baseada em correspondencia de termos nos triplets e insuficiente para cobrir a diversidade lexica das consultas. Contudo, sua contribuicao na fusao tripla e perceptivel: o Hibrido fixo (BM25+Semantic+KG) alcanca Citation Law Rate de 66%, superior aos 65% do BM25+Semantic (sem KG), indicando que os triplets do KG adicionam informacao estrutural complementar que melhora a capacidade do LLM de citar legislacoes corretamente.

**HyPA-RAG alcanca desempenho competitivo com significativa economia de fontes.** A constatacao central deste estudo reside na comparacao entre o HyPA-RAG e as configuracoes estaticas em termos de eficiencia. O HyPA-RAG atinge 65% em Lei Retrieval e 48% em Citation Article Rate -- valores competitivos com o Hibrido fixo (65% e 49%) e o BM25+Semantic (65% e 48%) -- utilizando em media apenas **6,8 fontes** contra 10,0 das demais configuracoes. Esta reducao de 32% no numero de fontes traduz-se em: (i) menor consumo de tokens na janela de contexto do LLM; (ii) menor custo computacional de inferencia; e (iii) menor risco de diluicao da resposta por *chunks* irrelevantes. A adaptacao parametrica permite que consultas simples ($k = 5$, 0 *rewrites*) operem de forma leve, enquanto consultas complexas ($k = 15$, 3 *rewrites*) recebem cobertura ampliada.

**Empate em consultas complexas, superioridade em consultas medias.** Nas 25 consultas complexas (Tabela 5), o HyPA-RAG e o BM25+Semantic empatam em Citation Article Rate (52%), ambos superando o Hibrido fixo (48%). Este resultado sugere que, para consultas que exigem raciocinio *multi-hop*, a combinacao de BM25 com recuperacao semantica e o fator determinante, e a inclusao do KG na fusao nao prejudica o desempenho quando os parametros sao adaptados. Nas 35 consultas medias (Tabela 6), o HyPA-RAG atinge **54% em Citation Article Rate**, superando todas as demais configuracoes -- incluindo o Hibrido fixo (49%) e o BM25+Semantic (46%). A reformulacao de consulta ($n = 1$ para complexidade media) e a calibracao de $k = 10$ emergem como a combinacao mais eficaz para este estrato de dificuldade, indicando que a adaptacao parametrica agrega maior valor precisamente no espectro intermediario de complexidade, onde nem os parametros minimos nem os maximos sao otimos.

**Tradeoff entre tempo de resposta e adaptabilidade.** O HyPA-RAG apresenta o maior tempo medio de resposta (43,5s), contra 26,2s do BM25-only e 23,8s do Hibrido fixo. Este incremento e atribuivel ao custo computacional das reformulacoes de consulta via LLM (para consultas medias e complexas) e ao $k$ elevado em consultas complexas. Entretanto, dado que o cenario de uso primario e a consulta deliberativa por gestores ambientais -- e nao a interacao conversacional em tempo real --, um tempo de resposta na faixa de 40-50 segundos permanece aceitavel para o dominio de aplicacao.

### 5.5. Limitacoes

Os resultados apresentados devem ser interpretados a luz de tres limitacoes reconhecidas. Primeiramente, o *dataset* de 100 consultas foi construido especificamente para este estudo e nao constitui um *benchmark* padronizado da area, impedindo comparacoes diretas com outros sistemas. A construcao de *benchmarks* publicos para RAG juridico em portugues permanece como lacuna relevante na comunidade. Em segundo lugar, a avaliacao empregou um unico LLM (Mistral 7B), e o desempenho do pipeline pode variar significativamente com modelos de diferentes capacidades (e.g., Llama 3, GPT-4). Terceiro, o classificador de complexidade opera exclusivamente sobre heuristicas linguisticas, sem treinamento supervisionado; um classificador aprendido poderia capturar padroes mais sutis de complexidade. Por fim, o corpus de 6 legislacoes, embora representativo dos marcos legais ambientais mais consultados, nao abrange a totalidade do arcabouco normativo (e.g., decretos regulamentadores, normativas estaduais, portarias do IBAMA).

---

## 6. Conclusao

Este trabalho apresentou o EcoLex RAG, um sistema HyPA-RAG adaptado ao dominio juridico-ambiental brasileiro que integra recuperacao tripla (BM25 + Legal-BERTimbau/FAISS + Knowledge Graph legal), fusao via Reciprocal Rank Fusion e adaptacao parametrica governada por um classificador de complexidade de consultas. O estudo de ablacao com 100 consultas sobre 6 legislacoes demonstrou que a adaptacao parametrica permite ao sistema manter desempenho competitivo em metricas de recuperacao e citacao enquanto opera com 32% menos fontes do que configuracoes estaticas, evidenciando eficiencia superior na gestao da janela de contexto do LLM. O resultado mais expressivo concentrou-se no estrato de consultas de complexidade media, onde o HyPA-RAG alcancou 54% em Citation Article Rate, superando todas as demais configuracoes.

As contribuicoes deste trabalho estendem-se em tres direcoes: (i) a demonstracao empirica de que a adaptacao parametrica e uma estrategia viavel para otimizar sistemas RAG no dominio legal brasileiro; (ii) a validacao do Legal-BERTimbau como modelo de *embedding* adequado para recuperacao semantica de trechos legislativos em portugues; e (iii) a proposta de um pipeline de geracao explicavel cuja estrutura de citacao obrigatoria (lei, artigo, paragrafo) alinha o sistema com os requisitos de transparencia e auditabilidade da administracao publica.

No contexto pos-COP30, em que o Brasil assume compromissos climaticos que demandam governanca ambiental agil e tecnicamente fundamentada, ferramentas como o EcoLex RAG representam uma ponte necessaria entre o arcabouco normativo e a pratica administrativa. A capacidade de consultar legislacao ambiental em linguagem natural e receber respostas explicaveis, com citacao exata de dispositivos legais, tem potencial para democratizar o acesso a informacao juridica e qualificar o processo decisorio de gestores publicos em todos os niveis federativos.

Como trabalhos futuros, destacam-se: (i) o *fine-tuning* do LLM em corpora juridico-ambientais brasileiros, visando melhorar a qualidade das citacoes e a fidelidade ao texto legislativo; (ii) a expansao da base de conhecimento para incluir decretos regulamentadores, normativas estaduais e portarias do IBAMA e ICMBio; (iii) a substituicao do classificador heuristico por um modelo aprendido supervisionadamente; (iv) a avaliacao com multiplos LLMs (Llama 3, Sabia, GPT-4) para mensurar o impacto do modelo generativo no desempenho *end-to-end*; e (v) a validacao do sistema com gestores ambientais em contexto operacional real, avaliando usabilidade, confianca nas respostas e impacto no tempo de tomada de decisao.

---

## Referencias

Cormack, G. V., Clarke, C. L. A. e Buettcher, S. (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods. In *Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR '09)*, p. 758-759. ACM.

Jiang, A. Q., Sablayrolles, A., Mensch, A., Bamford, C., Chaplot, D. S., Casas, D. de las, Bressand, F., Lengyel, G., Lample, G., Saulnier, L., Lavaud, L. R., Lachaux, M.-A., Stock, P., Scao, T. L., Lavril, T., Wang, T., Lacroix, T. e Sayed, W. E. (2023). Mistral 7B. *arXiv preprint arXiv:2310.06825*.

Kalra, R., Beshaj, L., Massey, T. e Grossman, R. (2024). HyPA-RAG: A Hybrid Parameter Adaptive Retrieval-Augmented Generation System for AI Legal and Policy Applications. *arXiv preprint arXiv:2409.09046*.

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Kuttler, H., Lewis, M., Yih, W., Rocktaschel, T., Riedel, S. e Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. In *Advances in Neural Information Processing Systems (NeurIPS 2020)*, v. 33, p. 9459-9474.

Robertson, S. e Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. *Foundations and Trends in Information Retrieval*, v. 3, n. 4, p. 333-389.

Rufimelo, M., Abrantes, A., Santos, A. F. e Ribeiro, B. (2022). Legal-BERTimbau: Pretrained BERT Models for Semantic Textual Similarity in the Portuguese Legal Domain. In *Proceedings of the 13th Language Resources and Evaluation Conference (LREC 2022)*, p. 1334-1340. European Language Resources Association.

Souza, F. e Nogueira, R. (2020). BERTimbau: Pretrained BERT Models for Brazilian Portuguese. In *Proceedings of the 9th Brazilian Conference on Intelligent Systems (BRACIS 2020)*, Lecture Notes in Computer Science, v. 12319, p. 403-417. Springer.
