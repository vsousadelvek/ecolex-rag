# Revisao R2 -- EcoLex RAG: Sistema HyPA-RAG com Legal-BERTimbau para Suporte Explicavel a Decisao em Gestao Ambiental Brasileira

**Artigo submetido ao:** WCAMA 2026 (Workshop de Computacao Aplicada a Gestao do Meio Ambiente e Recursos Naturais) -- CSBC 2026
**Data da revisao R2:** 2026-03-28
**Revisor:** Agente Revisor Senior (Claude Opus 4.6)
**Rodada:** Terceira revisao (pos-correcoes da revisao R1)

---

## Veredito Preliminar: MINOR REVISION (proxima ao aceite)

O artigo apresenta evolucao substancial em relacao as rodadas anteriores. Os problemas criticos de R1 -- 45+ acentos faltantes, 15 palavras coladas, 3 acentos indevidos -- foram corrigidos com sucesso. A formula RRF duplicada foi eliminada (agora aparece apenas uma vez, como eq:rrf_detail na Secao 3.4). O tempo de 96,3s em consultas complexas agora e discutido explicitamente na Secao 5.6 (Discussao). As quatro tabelas de resultados e o exemplo qualitativo estao presentes e corretos.

Contudo, persistem problemas residuais -- menores em gravidade, mas nao triviais -- que impedem o aceite imediato. A maioria sao corrigiveis em menos de uma hora de trabalho.

---

## VERIFICACAO SISTEMATICA DOS ITENS DE R1

### Itens criticos de R1 e status em R2:

| # R1 | Problema | Status R2 | Evidencia |
|------|----------|-----------|-----------|
| 1 | 45+ acentos faltantes | **CORRIGIDO** | Varredura por regex: "climatica", "economicas", "Area", "usuarios", "extensao", "avancado", "vao", "visao", "afirmacao", "interrogacao", "conjuncoes", "indice", "conteudo", "identicos", "metodos", "relacao", "reestruturacoes", "contem" (sem acento), "referencia", "fundamentacao", "tematica", "distribuicao", "fracao" -- nenhuma dessas formas sem acento foi encontrada no corpo do texto |
| 2 | 15 palavras coladas | **CORRIGIDO** | Varredura por regex: "sao[a-z]", "nao[a-z]", "contem[a-z]" -- zero ocorrencias. Todos os padroes "sãogeradas", "nãoinventar", "sãoextraídos", etc. foram eliminados |
| 3 | 3 acentos indevidos (agilidade, formuladas, dinamicamente) | **CORRIGIDO** | "agilidade" aparece corretamente sem acento (L42). "formuladas" e "dinamicamente" nao encontrados com acentos indevidos |
| 6 | Formula RRF duplicada | **CORRIGIDO** | Apenas uma ocorrencia: eq:rrf_detail (L209-212). A Secao 2.2 (L73) agora referencia textualmente a Equacao na Secao 3.4 |
| 5 | Referencia wcama:2025 mal formatada | **PARCIALMENTE CORRIGIDO** | Entrada .bib corrigida para @inproceedings com title/booktitle, mas permanece sem campo `author` (ver item 4 abaixo) |
| 8 | Tempo 96,3s nao mencionado | **CORRIGIDO** | L467: "chegando a 96,3s em media nas consultas complexas devido ao $top\_k = 15$ e 3 \textit{rewrites}" -- discutido explicitamente com justificativa |

**Taxa de resolucao dos itens criticos de R1: 5 de 6 (83%).** O unico item parcialmente pendente e a referencia wcama:2025.

---

## FALHAS ENCONTRADAS NA VERSAO R2

### 1. [INCONSISTENCIA NUMERICA -- Secao 3.3] "Quatro tipos de vinculos" vs. cinco listados

**Status:** NAO CORRIGIDO desde R1 (item 9 de R1).

Linha 194: o texto afirma "as relacoes capturam **quatro** tipos de vinculos", seguido de uma lista \begin{itemize} com **cinco** itens:
1. pertence\_a
2. detalha
3. define
4. definido\_em
5. estabelece\_medida

A Secao 3.7 (L247) corretamente afirma "cinco padroes estruturais". A Secao 3.3 contradiz isso. Este erro factual sobre o proprio sistema e inaceitavel.

**Correcao:** Alterar "quatro tipos de vinculos" para "cinco tipos de vinculos" na L194.

**Severidade:** Media-alta (erro factual no texto sobre a propria arquitetura).

### 2. [ACENTUACAO RESIDUAL] Acentos faltantes em exemplos de consulta

Tres exemplos de consultas no texto contem palavras sem acento em portugues:

| Linha | Ocorrencia | Correto |
|-------|-----------|---------|
| 157 | ``O que e APP?'' | ``O que **e** APP?'' (correto se intencional -- consulta de usuario) |
| 157 | ``Compare as exigencias de APP e Reserva Legal para propriedade na Amazonia Legal'' | "exig**e**ncias" -> "exig**e**ncias" (OK); "Amaz**o**nia" -> "Amaz**o**nia" (sem acento = erro) |
| 228 | ``O que e APP?'' | Mesma ocorrencia |
| 230 | ``Compare as exigencias de APP e Reserva Legal para propriedade na Amazonia Legal'' | Mesma ocorrencia |

**Analise:** Estes exemplos aparecem como simulacao de consultas de usuarios (entre aspas). Ha duas interpretacoes:
- **Se representam queries reais do sistema:** podem legitimamente nao ter acentos, pois usuarios frequentemente omitem acentos ao digitar.
- **Se sao exemplos do artigo cientifico:** devem seguir a norma culta.

A ambiguidade e o problema. O autor deveria:
- Ou acentuar corretamente ("exigencias" -> "exigencias", "Amazonia" -> "Amazonia") para manter o padrao do texto;
- Ou adicionar uma nota explicando que os exemplos refletem consultas reais sem acentuacao.

**Nota:** "porem" (L175) e "a luz de" (L173) tambem aparecem sem acento, dentro de listas de marcadores linguisticos entre aspas. "porem" deveria ser "porem" (acento circunflexo: "porém"); "a luz de" deveria ser "a luz de" (com crase: "à luz de").

**Severidade:** Baixa (exemplos entre aspas, possivelmente intencional). Mas "porem" sem acento na L175 e claramente um erro, pois esta na descricao do indicador, nao na simulacao de input do usuario.

### 3. [GRAMATICA] "contem" singular onde deveria ser plural (L332)

Linha 332:
> "fracão de consultas cujos resultados **contém** o artigo especifico esperado"

O sujeito e "resultados" (plural). A forma correta e "cont**e**m" (com circumflexo: "contêm"). A linha 331 usa corretamente "contêm" no mesmo contexto:
> "fracão de consultas cujos resultados de recuperacao **contêm** ao menos um chunk da lei esperada"

**Correcao:** L332: "contém" -> "contêm"

**Severidade:** Baixa (erro gramatical pontual, facilmente corrigivel).

### 4. [REFERENCIA] wcama:2025 -- Entrada bibliografica ainda problematica

A entrada .bib foi parcialmente corrigida (agora usa title e booktitle), mas permanece problematica:

```bibtex
@inproceedings{wcama:2025,
  title     = {Anais do {XV} Workshop de Computação ...},
  booktitle = {Anais do {XLV} Congresso da Sociedade Brasileira de Computação},
  year      = {2025},
  publisher = {SBC},
  address   = {Porto Alegre}
}
```

Problemas remanescentes:
- **Sem campo `author`.** Uma entrada @inproceedings exige author. O BibTeX/BibLaTeX gerara warning ou erro dependendo do estilo. O estilo SBC (sbc.bst) provavelmente exige o campo.
- **Semantica incorreta.** @inproceedings e para artigo dentro de conferencia. Citar os anais inteiros deveria usar @proceedings. Ou, preferencialmente, citar um artigo especifico do WCAMA 2025.
- **No texto (L85):** "A edicao de 2025 do WCAMA evidenciou..." -- esta frase cita o evento sem \cite, enquanto L83 usa \cite{wcama:2025}. A inconsistencia sugere que o autor esta indeciso sobre como citar o evento.

**Sugestao concreta:** Substituir @inproceedings por @proceedings com `editor = {{SBC}}`, ou citar um artigo especifico do WCAMA 2025 que trate de RAG/XAI em gestao ambiental.

**Severidade:** Media (pode causar erro de compilacao com sbc.bst; pratica bibliografica nao padrao).

### 5. [REDUNDANCIA] Abstract e Resumo mencionam "54% CAR" duas vezes cada

Este problema foi reportado na R1 (item 11) e **NAO foi corrigido**.

**Abstract (L27):**
> "...with superior performance on medium-complexity queries (54\% CAR) but identified degradation on simple queries (40\% CAR vs. 50\% for BM25-only) [...] **For medium-complexity queries, the system reaches 54\% Citation Article Rate, outperforming all other configurations.**"

**Resumo (L33):**
> "...com desempenho superior em consultas de complexidade media (54\% CAR) mas com degradacao identificada em consultas simples (40\% CAR vs. 50\% do BM25-only) [...] **Em consultas de complexidade media, o sistema atinge 54\% em Citation Article Rate, superando todas as demais configuracoes.**"

O dado "54% CAR em consultas medias" e mencionado duas vezes em cada versao do resumo: primeiro como parentetico e depois como frase completa. Em um Abstract com limite de palavras, esta redundancia despertica ~20 palavras que poderiam transmitir informacao nova.

**Severidade:** Baixa-media (nao e erro factual, mas e desperdicio de espaco e incomoda o leitor atento).

### 6. [LABELS LaTeX] Tres labels contem caracteres acentuados

Este problema foi reportado na R1 (item 16) e **NAO foi corrigido**.

- `\label{tab:parâmetros}` (L223) -- contem 'â'
- `\label{tab:legislações}` (L270) -- contem 'õ' e 'ç'
- `\label{tab:médias}` (L396) -- contem 'é'

Embora pdflatex com inputenc UTF-8 possa processar labels com caracteres acentuados, esta e uma pratica fragil que:
- Pode causar erros em diferentes engines (lualatex, xelatex);
- Pode gerar warnings de "label changed" em recompilacoes;
- E inconsistente com os demais labels do artigo (tab:resultados_gerais, tab:complexas, tab:simples, tab:dataset, fig:arquitetura, eq:complexity, eq:classification, eq:rrf_detail -- todos ASCII).

**Correcao recomendada:**
- `tab:parâmetros` -> `tab:parametros`
- `tab:legislações` -> `tab:legislacoes`
- `tab:médias` -> `tab:medias`

(Incluindo as correspondentes \ref{})

**Severidade:** Baixa (funcional, mas fragil e inconsistente).

### 7. [FIGURA] Figura 1 em verbatim (ASCII art)

Este problema foi reportado desde R0 (item 11/R0, item 15/R1) e permanece inalterado.

A Figura 1 (L98-149) e um diagrama em \begin{verbatim}. Embora funcional, e inaceitavel para camera-ready de conferencia SBC. A figura deve ser convertida para formato vetorial (TikZ, ou PDF gerado por draw.io/Lucidchart).

**Severidade:** Media (aceitavel para rascunho de submissao, inaceitavel para camera-ready).

### 8. [TABELAS] Breakdowns sem colunas Fontes e Tempo

Reportado na R1 (item 7) e **NAO corrigido**.

As tabelas tab:complexas (L371-387), tab:medias (L393-409) e tab:simples (L415-431) contem apenas 4 colunas (Lei Ret., Art. Ret., Cit. Lei, Cit. Art.), enquanto a tab:resultados_gerais (L349-365) contem 6 colunas (incluindo Fontes e Tempo).

Os dados brutos contem essas informacoes:

| Estrato | HyPA-RAG Fontes | HyPA-RAG Tempo |
|---------|-----------------|----------------|
| Simples | 5,1 | 19,1s |
| Medias | 6,1 | 33,7s |
| Complexas | 10,4 | 96,3s |

Esses dados sao essenciais para a narrativa de tradeoff e para o leitor entender a distribuicao da "economia de fontes" (concentrada nas consultas simples) e o custo temporal (concentrado nas complexas).

**Nota atenuante:** O tempo de 96,3s agora e mencionado no texto da discussao (L467), o que mitiga parcialmente a ausencia da coluna na tabela. Contudo, incluir as colunas nas tabelas e a forma padrao de reportar dados experimentais.

**Severidade:** Media (dados existem e sao parcialmente discutidos no texto, mas a pratica padrao exige que estejam nas tabelas).

---

## VERIFICACAO DE COERENCIA NUMERICA (EXAUSTIVA)

Cruzamento sistematico entre artigo.tex e data/ablation_table.md:

### Tabela tab:resultados_gerais (100 consultas) -- L357-362:

| Config | Lei Ret. | Art. Ret. | Cit. Lei | Cit. Art. | Fontes | Tempo |
|--------|----------|-----------|----------|-----------|--------|-------|
| Artigo: BM25-only | 65% | 70% | 63% | 45% | 10,0 | 26,2 |
| Dados: BM25-only  | 65% | 70% | 63% | 45% | 10,0 | 26,2 |
| Artigo: HyPA-RAG  | 65% | 56% | 65% | 48% | 6,8  | 43,5 |
| Dados: HyPA-RAG   | 65% | 56% | 65% | 48% | 6,8  | 43,5 |

**RESULTADO: TODOS OS 36 VALORES CONFEREM.**

### Tabela tab:complexas (25 consultas) -- L379-384:

| Config | Lei Ret. | Art. Ret. | Cit. Lei | Cit. Art. |
|--------|----------|-----------|----------|-----------|
| Artigo: HyPA-RAG | 64% | 52% | 68% | 52% |
| Dados: HyPA-RAG  | 64% | 52% | 68% | 52% |

**RESULTADO: TODOS OS 24 VALORES CONFEREM.**

### Tabela tab:medias (35 consultas) -- L401-406:

| Config | Lei Ret. | Art. Ret. | Cit. Lei | Cit. Art. |
|--------|----------|-----------|----------|-----------|
| Artigo: HyPA-RAG | 66% | 63% | 63% | 54% |
| Dados: HyPA-RAG  | 66% | 63% | 63% | 54% |

**RESULTADO: TODOS OS 24 VALORES CONFEREM.**

### Tabela tab:simples (40 consultas) -- L423-428:

| Config | Lei Ret. | Art. Ret. | Cit. Lei | Cit. Art. |
|--------|----------|-----------|----------|-----------|
| Artigo: HyPA-RAG | 65% | 52% | 65% | 40% |
| Dados: HyPA-RAG  | 65% | 52% | 65% | 40% |

**RESULTADO: TODOS OS 24 VALORES CONFEREM.**

### Numeros citados no corpo do texto:

| Local | Afirmacao | Fonte | Status |
|-------|-----------|-------|--------|
| Abstract L27 | "65% Law Retrieval and 48% CAR" | tab:resultados_gerais | OK |
| Abstract L27 | "54% CAR" medias | tab:medias HyPA-RAG | OK |
| Abstract L27 | "40% CAR vs. 50%" simples | tab:simples HyPA-RAG (40%) vs BM25-only (50%) | OK |
| Abstract L27 | "6.8 sources vs. 10.0" | tab:resultados_gerais | OK |
| Resumo L33 | Mesmos numeros | Todas as tabelas | OK |
| L457 | "BM25-only 70% ARR" | tab:resultados_gerais | OK |
| L457 | "Semantic-only 53%, KG-only 35%" | tab:resultados_gerais | OK |
| L459 | "Hibrido fixo CLR 66% vs BM25+Semantic 65%" | tab:resultados_gerais | OK |
| L461 | "65% LRR, 48% CAR" HyPA-RAG | tab:resultados_gerais | OK |
| L461 | "Hibrido fixo 65% e 49%" | tab:resultados_gerais | OK |
| L461 | "6,8 fontes contra 10,0" | tab:resultados_gerais | OK |
| L463 | "HyPA-RAG e BM25+Semantic 52% CAR" complexas | tab:complexas | OK |
| L463 | "Hibrido fixo 48%" complexas | tab:complexas | OK |
| L463 | "54% CAR" medias | tab:medias | OK |
| L463 | "Hibrido fixo 49%, BM25+Semantic 46%" medias | tab:medias | OK |
| L465 | "52% ARR" vs "82% BM25-only" e "70% Hibrido fixo" simples | tab:simples | OK |
| L465 | "40% vs 50% BM25-only e Hibrido fixo" simples | tab:simples | OK |
| L467 | "43,5s" media geral | tab:resultados_gerais | OK |
| L467 | "96,3s" complexas | dados brutos (96,3) | OK |
| L467 | "26,2s BM25-only, 23,8s Hibrido fixo" | tab:resultados_gerais | OK |

**VEREDITO DE COERENCIA NUMERICA: APROVADO. Todos os 108 valores nas tabelas e todas as 20+ cifras citadas no texto conferem com as fontes de dados brutas. Nenhuma inconsistencia numerica encontrada.**

---

## VERIFICACAO DE COMPLETUDE

| Requisito | Status | Local |
|-----------|--------|-------|
| Tabela de resultados gerais (100 consultas) | PRESENTE | tab:resultados_gerais (L349-365) |
| Tabela de consultas complexas (25) | PRESENTE | tab:complexas (L371-387) |
| Tabela de consultas medias (35) | PRESENTE | tab:medias (L393-409) |
| Tabela de consultas simples (40) | PRESENTE | tab:simples (L415-431) |
| Exemplo qualitativo | PRESENTE | L433-451 (consulta sobre APP) |
| Discussao honesta de degradacao | PRESENTE | L465 (paragrafo dedicado) |
| Discussao de tempo 96,3s | PRESENTE | L467 |
| Discussao de tradeoff fontes | PRESENTE | L461 com qualificacao |
| Formula RRF (unica ocorrencia) | PRESENTE | eq:rrf_detail (L209-212) |
| Abstract com degradacao reportada | PRESENTE | L27 ("40% CAR vs. 50%") |
| Resumo com degradacao reportada | PRESENTE | L33 ("40% CAR vs. 50%") |

**VEREDITO DE COMPLETUDE: APROVADO com ressalvas.** As 4 tabelas, o exemplo qualitativo e a discussao honesta de tradeoffs estao presentes. A ressalva refere-se as colunas Fontes/Tempo ausentes nos breakdowns.

---

## VERIFICACAO DA FORMULA RRF

- `\label{eq:rrf}`: NAO encontrado (removido corretamente).
- `\label{eq:rrf_detail}`: 1 ocorrencia (L211).
- Formula `RRF_{score}`: 1 ocorrencia (L210).
- Secao 2.2 (L73): agora referencia textualmente "A formula do RRF e formalizada na Equacao~\ref{eq:rrf_detail} (Secao 3.4)."

**VEREDITO: CORRIGIDO. A formula aparece exatamente UMA vez, na Secao 3.4, com referencia textual na Secao 2.2.**

---

## VERIFICACAO DE REFERENCIAS

| Referencia | Citada no texto | Entrada .bib | Status |
|------------|-----------------|--------------|--------|
| robertson:2009 | L40, L67, L190, L457 | Completa | OK |
| lewis:2020 | L44, L65 | Completa | OK |
| kalra:2024 | L46, L71 | Completa | OK |
| cormack:2009 | L51, L73, L207 | Completa | OK |
| rufimelo:2022 | L51, L77, L192 | Completa | OK |
| jiang:2023 | L53, L79, L239 | Completa | OK |
| souza:2020 | L77 | Completa | OK |
| wcama:2025 | L83 | Incompleta (sem author) | PROBLEMATICA |

**VEREDITO: 7 de 8 referencias validas. wcama:2025 permanece problematica.**

---

## LISTA DE PROBLEMAS (NUMERADA, POR SEVERIDADE)

### Importantes (exigem correcao antes do aceite)

1. **"Quatro tipos de vinculos" vs. cinco listados (L194)** -- erro factual sobre a propria arquitetura, nao corrigido desde R1.
2. **Referencia wcama:2025 sem campo `author`** -- pode causar erro de compilacao com sbc.bst. Entrada semanticamente incorreta (@inproceedings para anais inteiros).
3. **Redundancia no Abstract/Resumo** -- "54% CAR" mencionado duas vezes em cada versao, desperdicando espaco.
4. **"contem" singular (L332)** -- deveria ser "contem" (plural: "contêm"), concordando com "resultados".
5. **"porem" sem acento (L175)** -- na descricao de indicador linguistico, deveria ser "porém".
6. **"a luz de" sem crase (L173)** -- na descricao de indicador, deveria ser "à luz de".

### Recomendados (melhoram a qualidade, nao impedem aceite)

7. **Tabelas de breakdown sem colunas Fontes e Tempo** -- dados existem nos brutos e sao parcialmente discutidos no texto.
8. **Labels LaTeX com acentos** (tab:parametros, tab:legislacoes, tab:medias) -- pratica fragil, inconsistente com demais labels.
9. **Exemplos de consulta sem acentos** (L157, L228, L230) -- "Amazonia" sem til, "exigencias" sem acento. Ambiguidade sobre intencionalidade.
10. **Figura 1 em verbatim** -- aceitavel para submissao, inaceitavel para camera-ready.
11. **KG discutido em dois lugares** (Secoes 3.3 e 3.7) -- seria mais limpo consolidar, mas a divisao atual e defensavel (3.3 = descricao funcional, 3.7 = detalhes de extracao).

### Observacoes (cosmeticas / nao impedem aceite)

12. **Significancia estatistica** -- persistente desde R0, reconhecido nas Limitacoes. Dado o escopo WCAMA, nao e bloqueante, mas afirmacoes como "superando todas as demais configuracoes" (L33, L463) deveriam ser qualificadas.
13. **Dataset nao disponibilizado publicamente** -- persistente desde R0. Nao e requisito do WCAMA, mas fortaleceria o artigo.
14. **Alternancia de idioma nos termos tecnicos** -- persistente desde R1, menor em impacto.

---

## QUESTIONAMENTOS DIRETOS AO AUTOR

Q1. O item "quatro tipos de vinculos" (L194) vs. cinco itens na lista foi reportado na R1 e permanece inalterado. E um erro trivial de corrigir. Por que nao foi corrigido?

Q2. A redundancia do "54% CAR" no Abstract/Resumo tambem foi reportada na R1 (item 11) e permanece. A segunda mencao ("For medium-complexity queries, the system reaches 54% Citation Article Rate, outperforming all other configurations") e identica a informacao ja fornecida no parentetico. Sugiro remover a segunda ocorrencia e usar o espaco para informacao adicional (e.g., o tempo de resposta ou a quantidade de fontes).

Q3. A ausencia do campo `author` na referencia wcama:2025 sera um erro de compilacao com o estilo SBC? O autor testou a compilacao com sbc.bst?

---

## AVALIACAO GERAL

| Criterio | Nota R0 | Nota R1 | Nota R2 | Comentario R2 |
|:---|:---:|:---:|:---:|:---|
| Originalidade | 7 | 7 | 7 | Inalterada -- adaptacao valida do HyPA-RAG ao dominio brasileiro |
| Rigor metodologico | 5 | 6 | 6.5 | Leve melhoria pela discussao de 96,3s; ainda sem significancia estatistica |
| Clareza da escrita | 8 | 6 | 8.5 | **RECUPERADA** -- acentuacao corrigida, palavras coladas eliminadas, texto fluido e tecnico |
| Qualidade dos experimentos | 6 | 7 | 7 | Inalterada -- 4 tabelas + exemplo qualitativo |
| Relevancia para o WCAMA | 9 | 9 | 9 | Inalterada -- excelente adequacao tematica |
| Completude | 6 | 7.5 | 8 | Melhoria pela discussao de 96,3s; faltam Fontes/Tempo nos breakdowns |
| Reproducibilidade | 5 | 5 | 5 | Inalterada -- dataset nao disponibilizado |
| Impacto potencial | 7 | 7 | 7 | Inalterado |
| Honestidade dos resultados | 5 | 8 | 8.5 | Leve melhoria pela discussao explicita de 96,3s com justificativa |
| Consistencia interna | -- | -- | 7 | "Quatro vs. cinco" vinculos persiste; redundancia no Abstract/Resumo |
| **NOTA GERAL** | **6.5** | **7.0** | **8.0 / 10** | **Minor Revision. Artigo proximo ao aceite; problemas residuais sao menores e corrigiveis rapidamente.** |

---

## COMPARACAO R0 -> R1 -> R2

| Aspecto | R0 | R1 | R2 | Evolucao R1->R2 |
|---------|----|----|-----|-----------------|
| Veredito | MAJOR REVISION | MINOR REVISION | MINOR REVISION (proximo aceite) | Estavel, com melhoria qualitativa |
| Nota geral | 6.5 | 7.0 | 8.0 | +1.0 |
| Itens criticos pendentes | 7 | 6 | 6 (todos menores) | Severidade reduzida drasticamente |
| Acentuacao | 150+ erros | 45+ erros | ~5 residuais em exemplos | **Problema essencialmente resolvido** |
| Palavras coladas | Nao verificado | 15 ocorrencias | 0 ocorrencias | **Resolvido** |
| Formula RRF | Duplicada | Duplicada | Unica | **Resolvido** |
| Tempo 96,3s | Omitido | Omitido | Discutido (L467) | **Resolvido** |
| Coerencia numerica | OK | OK | OK | Mantida impecavel |
| Maior melhoria R2 | -- | -- | Acentuacao restaurada (+2.5 pontos em Clareza) | -- |
| Maior fraqueza R2 | -- | -- | "Quatro vs. cinco" nao corrigido; redundancia Abstract | -- |

---

## VEREDITO FINAL

### MINOR REVISION

**Justificativa:** O artigo evoluiu de forma consistente ao longo de tres rodadas de revisao. A versao R2 resolve os problemas mais graves das rodadas anteriores: a acentuacao esta essencialmente correta (restam ~5 ocorrencias residuais em exemplos entre aspas, de intencionalidade discutivel), as palavras coladas foram eliminadas, a formula RRF aparece uma unica vez, o tempo de 96,3s e discutido, e a coerencia numerica permanece impecavel.

Os problemas remanescentes sao menores em comparacao as rodadas anteriores:
- O erro "quatro vs. cinco" e trivial de corrigir (trocar uma palavra).
- A redundancia no Abstract e eliminavel em 2 minutos.
- A referencia wcama:2025 precisa de ajuste no .bib.
- "contem" -> "contem" e uma correcao de um caractere.
- "porem" e "a luz de" sao correcoes pontuais.

**O artigo nao atinge 8.5 para aceite imediato** (nota 8.0) devido a persistencia de itens reportados em R1 que nao foram corrigidos (notavelmente "quatro vs. cinco" e a redundancia no Abstract). Contudo, a distancia para o aceite e pequena e as correcoes necessarias sao realizaveis em menos de 30 minutos.

**Recomendacao:** Corrigir os 6 itens "Importantes" listados acima. Apos correcao, o artigo estara em condicoes de aceite para o WCAMA 2026 sem necessidade de nova rodada completa de revisao.

**Prognostico:** Com as correcoes dos itens 1-6, a nota subiria para ~8.5-9.0 (ACEITAR).
