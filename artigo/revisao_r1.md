# Revisao R1 -- EcoLex RAG: Sistema HyPA-RAG com Legal-BERTimbau para Suporte Explicavel a Decisao em Gestao Ambiental Brasileira

**Artigo submetido ao:** WCAMA 2026 (Workshop de Computacao Aplicada a Gestao do Meio Ambiente e Recursos Naturais) -- CSBC 2026
**Data da revisao R1:** 2026-03-28
**Revisor:** Agente Revisor Senior (Claude Opus 4.6)
**Rodada:** Segunda revisao (pos-correcoes da revisao R0)

---

## Veredito Preliminar: MINOR REVISION

O artigo foi substancialmente melhorado em relacao a versao anterior. As correcoes de maior impacto -- inclusao da Tabela de consultas simples (tab:simples), exemplo qualitativo, discussao honesta sobre degradacao, e ajuste narrativo do Resumo/Abstract -- foram implementadas com competencia. Contudo, persistem problemas de acentuacao residual (dezenas de ocorrencias), erros de espacamento colado entre palavras, inconsistencias menores de coerencia numerica no texto, e a referencia WCAMA 2025 permanece problematica. Nenhuma dessas falhas e fatal, mas sua quantidade cumulativa impede o aceite imediato.

---

## COMPARACAO COM A VERSAO ANTERIOR (R0)

### Itens da R0 que foram CORRIGIDOS com sucesso:

| # R0 | Problema | Status R1 |
|------|----------|-----------|
| 4 | Tabela de consultas simples ausente | CORRIGIDO -- Tabela tab:simples adicionada (L418-438) |
| 5 | Resumo/Abstract superestimava resultados | CORRIGIDO -- Abstract e Resumo agora reportam degradacao em simples (40% CAR vs. 50%) |
| 6 | "Economia de fontes" como virtude acritica | CORRIGIDO -- Discussao (L468-474) apresenta tradeoff honestamente |
| 9 | Referencia "[WCAMA 2025]" invalida | PARCIALMENTE CORRIGIDO -- Agora e \cite{wcama:2025} com entrada .bib, mas a entrada e problematica (ver item 5 abaixo) |
| 12 | Acentuacao ausente | PARCIALMENTE CORRIGIDO -- Maioria restaurada, mas restam dezenas de ocorrencias (ver item 1 abaixo) |
| 15 | Falta de avaliacao qualitativa | CORRIGIDO -- Exemplo qualitativo adicionado (L440-458) com consulta sobre APP |
| 18 | Formula RRF duplicada | NAO CORRIGIDO -- Formula aparece em eq:rrf (L75-78) e eq:rrf_detail (L216-219) |

### Itens da R0 que permanecem ABERTOS:

| # R0 | Problema | Status R1 |
|------|----------|-----------|
| 7 | Classificador de complexidade nao validado | ABERTO -- Reconhecido nas Limitacoes, mas sem alteracao |
| 8 | COP30 -- verificacao factual | ABERTO -- Texto mantido identico |
| 13 | Falta de significancia estatistica | ABERTO -- Nenhum teste reportado |
| 14 | Dataset nao disponibilizado publicamente | ABERTO -- Sem menção de disponibilizacao |
| 16 | Unico LLM testado | ABERTO -- Reconhecido nas Limitacoes |
| 17 | Distribuicao dos 1.714 triplets nao reportada | ABERTO |
| 20 | Tempo de 96,3s em consultas complexas nao discutido | PARCIAL -- Discussao geral de 43,5s existe (L474), mas 96,3s nao e mencionado |

---

## FALHAS ENCONTRADAS NA VERSAO CORRIGIDA

### 1. [ACENTUACAO] Dezenas de acentos AINDA faltantes

A correcao de acentuacao foi aplicada de forma incompleta. As seguintes ocorrencias sem acento persistem no artigo LaTeX (arquivo com \usepackage[utf8]{inputenc}):

**Palavras sem til (~) -- cedilha ja presente mas til ausente:**
- L42: "climatica" -> "climatica" (falta acento, deveria ser "climática")
- L42: "paisdurante" -> "país durante" (palavra colada + falta acento)
- L42: "ágilidade" -> "agilidade" (acento indevido no 'a' + falta acento correto -- deveria ser "agilidade" sem acento algum)
- L42: "economicas" -> "econômicas"
- L44: "Area" -> "Área" (dentro de aspas ``Area de Preservacao Permanente'')
- L44: "Capitulo" -> "Capítulo"
- L44: "Paragrafo" -> "Parágrafo"
- L44: "Alinea" -> "Alínea"
- L44: "desperdica" -> "desperdiça"
- L48: "sao:" -> "são:"
- L67: "útilem" -> "útil em" (palavra colada + acento incorreto)
- L67: "fórmuladas" -> "formuladas" (acento indevido no 'o')
- L67: "usuarios" -> "usuários"
- L67: "nãoespecializados" -> "não especializados" (colado)
- L71: "extensao" -> "extensão"
- L71: "dinâmicamente" -> "dinamicamente" (acento indevido no 'a')
- L71: "recuperação(" -> "recuperação (" (falta espaco)
- L90: "avancado" -> "avançado"
- L90: "vao" -> "vão"
- L90: "visao" -> "visão"
- L90: "afirmacao" -> "afirmação"
- L181: "interrogacao" -> "interrogação"
- L182: "conjuncoes" -> "conjunções"
- L197: "indice" -> "índice"
- L199: "sãonormalizados" -> "são normalizados" (colado)
- L221: "nãocontribuem" -> "não contribuem" (colado)
- L221: "sãoordenados" -> "são ordenados" (colado)
- L221: "sãoselecionados" -> "são selecionados" (colado)
- L221: "conteudo" -> "conteúdo"
- L221: "identicos" -> "idênticos"
- L221: "nãosejam" -> "não sejam" (colado)
- L221: "metodos" -> "métodos"
- L225: "relacao" -> "relação"
- L242: "sãogeradas" -> "são geradas" (colado)
- L242: "reestruturacoes" -> "reestruturações"
- L248: "nãoinventar" -> "não inventar" (colado)
- L259: "sãoextraídos" -> "são extraídos" (colado)
- L294: "contem" -> "contém"
- L294: "referencia" -> "referência"
- L294: "fundamentacao" -> "fundamentação"
- L294: "tematica" -> "temática"
- L294: "distribuicao" -> "distribuição"
- L298: "Distribuicao" -> "Distribuição" (caption da tabela)
- L316: "sãocobertas" -> "são cobertas" (colado)
- L335: "sãoempregadas" -> "são empregadas" (colado)
- L338-341: "fracao" -> "fração" (4 ocorrencias)
- L339: "contémo" -> "contém o" (colado)

**Total estimado: 45+ ocorrencias residuais.** Isto representa uma correcao incompleta do problema original (150+ foram corrigidos, mas ~45 escaparam).

### 2. [ESPACAMENTO COLADO] Palavras grudadas sistematicamente

Alem dos problemas de acentuacao, ha um padrao sistematico de palavras coladas (sem espaco entre elas), provavelmente originado de uma substituicao automatica que removeu espacos:

| Linha | Ocorrencia | Correto |
|-------|-----------|---------|
| 42 | "paisdurante" | "país durante" |
| 44 | "nãocapturam" | "não capturam" |
| 67 | "útilem" | "útil em" |
| 67 | "nãoespecializados" | "não especializados" |
| 199 | "sãonormalizados" | "são normalizados" |
| 221 | "nãocontribuem" | "não contribuem" |
| 221 | "sãoordenados" | "são ordenados" |
| 221 | "sãoselecionados" | "são selecionados" |
| 221 | "nãosejam" | "não sejam" |
| 242 | "sãogeradas" | "são geradas" |
| 248 | "nãoinventar" | "não inventar" |
| 259 | "sãoextraídos" | "são extraídos" |
| 316 | "sãocobertas" | "são cobertas" |
| 335 | "sãoempregadas" | "são empregadas" |
| 339 | "contémo" | "contém o" |

**Total: 15 ocorrencias de palavras coladas.** Isso gera erros de compilacao LaTeX ou, na melhor hipotese, palavras ilegíveis no PDF final.

### 3. [ACENTOS INDEVIDOS] Acentos colocados em posicoes erradas

Tres ocorrencias de acentuacao incorreta (acento presente, mas na posicao errada):

- L42: "ágilidade" -- o acento esta no 'a', mas "agilidade" nao tem acento algum em portugues.
- L67: "fórmuladas" -- o acento esta no 'o', mas "formuladas" nao tem acento.
- L71: "dinâmicamente" -- o acento esta no 'a' de "nâm", mas "dinamicamente" nao tem acento.

Estes sao piores que acentos faltantes, pois demonstram descuido na revisao.

### 4. [COERENCIA NUMERICA] Valores nas tabelas vs. dados brutos -- VERIFICACAO COMPLETA

Cruzamento sistematico entre artigo.tex e data/ablation_table.md:

**Tabela tab:resultados_gerais (100 consultas) -- L357-372:**
| Config | Lei Ret. | Art. Ret. | Cit. Lei | Cit. Art. | Fontes | Tempo |
|--------|----------|-----------|----------|-----------|--------|-------|
| Artigo | 65/70/56/35/66/59/65 | OK | OK | OK | OK | OK |
| Dados  | 65/70/56/35/66/59/65 | OK | OK | OK | OK | OK |

RESULTADO: TODOS OS VALORES CONSISTENTES.

**Tabela tab:complexas (25 consultas) -- L380-394:**
RESULTADO: TODOS OS VALORES CONSISTENTES com dados brutos.

**Tabela tab:medias (35 consultas) -- L400-416:**
RESULTADO: TODOS OS VALORES CONSISTENTES com dados brutos.

**Tabela tab:simples (40 consultas) -- L424-438:**
RESULTADO: TODOS OS VALORES CONSISTENTES com dados brutos.

**Verificacao de numeros citados NO TEXTO:**

- Abstract L27: "65% Law Retrieval and 48% Citation Article Rate" -- CORRETO (tab:resultados_gerais)
- Abstract L27: "54% CAR" para medias -- CORRETO (tab:medias)
- Abstract L27: "40% CAR vs. 50% for BM25-only" para simples -- CORRETO (tab:simples: HyPA-RAG 40%, BM25-only 50%)
- Abstract L27: "6.8 sources compared to 10.0" -- CORRETO (tab:resultados_gerais)
- Resumo L33: mesmos numeros -- CORRETO
- L464: "BM25-only alcanca o melhor Article Retrieval Rate global (70%)" -- CORRETO
- L464: "Semantic-only (53%) e KG-only (35%)" -- CORRETO
- L466: "Hibrido fixo (BM25+Semantic+KG) alcanca Citation Law Rate de 66%, superior aos 65% do BM25+Semantic" -- CORRETO
- L468: "65% em Lei Retrieval e 48% em Citation Article Rate" -- CORRETO
- L468: "Hibrido fixo (65% e 49%) e o BM25+Semantic (65% e 48%)" -- CORRETO
- L468: "6,8 fontes contra 10,0" -- CORRETO
- L470: "HyPA-RAG e o BM25+Semantic empatam em Citation Article Rate (52%)" -- CORRETO (tab:complexas)
- L470: "Hibrido fixo (48%)" -- CORRETO (tab:complexas)
- L470: "54% em Citation Article Rate" para medias -- CORRETO (tab:medias)
- L470: "Hibrido fixo (49%) e o BM25+Semantic (46%)" para medias -- CORRETO (tab:medias)
- L472: "Article Retrieval Rate (52%) em comparacao ao BM25-only (82%) e ao Hibrido fixo (70%)" para simples -- CORRETO (tab:simples)
- L472: "Citation Article Rate tambem sofre (40% vs. 50% do BM25-only e Hibrido fixo)" -- CORRETO (tab:simples)
- L474: "43,5s" -- CORRETO (tab:resultados_gerais), "26,2s do BM25-only e 23,8s do Hibrido fixo" -- CORRETO

**VEREDITO DE COERENCIA NUMERICA: APROVADO.** Todos os numeros citados no texto conferem com as tabelas e com os dados brutos. Nenhuma inconsistencia numerica foi encontrada.

### 5. [REFERENCIA] wcama:2025 -- Entrada bibliografica problematica

A entrada em references.bib (L63-70):
```bibtex
@inproceedings{wcama:2025,
  author    = {{Anais do XV Workshop de Computação Aplicada à Gestão do Meio Ambiente e Recursos Naturais}},
  title     = {Anais do WCAMA 2025},
  booktitle = {Anais do XLV Congresso da Sociedade Brasileira de Computação (CSBC 2025)},
  year      = {2025},
  publisher = {SBC},
  address   = {Porto Alegre}
}
```

Problemas:
- O campo `author` contem o titulo dos anais, nao um autor. Deveria ser `author = {{SBC}}` ou usar `@proceedings` em vez de `@inproceedings`.
- Citar anais inteiros de um workshop nao e pratica bibliografica padrao. O correto seria citar um artigo especifico publicado no WCAMA 2025, ou, se a intencao e citar o evento como evidencia de tendencia, usar uma nota de rodape ou texto corrido sem \cite.
- No texto (L90), o uso e: "...a deteccao de desmatamento por visao computacional ate a modelagem preditiva de dinamicas climaticas \cite{wcama:2025}." Citar anais inteiros como evidencia de aplicacoes de IA em meio ambiente e impreciso -- nao aponta a qual trabalho especifico se refere.
- No texto (L92), uma segunda menção ao WCAMA 2025 e feita sem \cite, o que e inconsistente.

### 6. [FORMULA DUPLICADA] Equacao RRF aparece duas vezes

A formula do Reciprocal Rank Fusion e definida em:
- eq:rrf (L75-78): $\text{RRF}_{\text{score}}(d) = \sum_{r \in R} \frac{1}{k + \text{rank}_r(d)}$
- eq:rrf_detail (L216-219): $\text{RRF}_{\text{score}}(d) = \sum_{r \in \{BM25, Dense, KG\}} \frac{1}{k + \text{rank}_r(d)}$

A segunda formulacao e ligeiramente mais especifica (enumera os retrievers), mas a redundancia e desnecessaria. Em artigos de conferencia com limite de paginas, cada equacao deve justificar sua presenca. A sugestao e manter apenas eq:rrf_detail na Secao 3.4 (onde e operacionalmente usada) e descrever o RRF textualmente na Secao 2.2, referenciando a equacao na Secao 3.4.

### 7. [TABELAS INCOMPLETAS] Tabelas tab:complexas, tab:medias e tab:simples nao incluem Fontes e Tempo

A Tabela tab:resultados_gerais (L357-372) inclui 6 colunas: Lei Ret., Art. Ret., Cit. Lei, Cit. Art., Fontes e Tempo. As tres tabelas de breakdown (tab:complexas, tab:medias, tab:simples) incluem apenas 4 colunas (sem Fontes e Tempo).

Os dados brutos em ablation_table.md CONTEM esses valores:
- Simples: HyPA-RAG usa 5,1 fontes, 19,1s
- Medias: HyPA-RAG usa 6,1 fontes, 33,7s
- Complexas: HyPA-RAG usa 10,4 fontes, 96,3s

Estas informacoes sao criticas porque:
- Mostram que a "economia de fontes" e concentrada nas consultas simples (5,1 vs. 10,0), nao e uniforme.
- Revelam que o HyPA-RAG consome 96,3s em consultas complexas -- dado ausente do artigo e relevante para viabilidade pratica.
- O leitor nao tem como deduzir a distribuicao de fontes por estrato sem essas colunas.

### 8. [TEXTO] Tempo de 96,3s em consultas complexas NAO discutido

A discussao sobre tempo (L474) menciona apenas "43,5s" (media geral) e justifica como aceitavel para consulta deliberativa. Contudo, o tempo de 96,3s para consultas complexas -- mais que o dobro do segundo mais lento (BM25+Semantic, 47,0s) -- nao e mencionado em lugar algum. Para um sistema de suporte a decisao, quase 2 minutos de espera por consulta complexa e um dado relevante que deve ser discutido e justificado.

### 9. [SECAO 3.3] Quatro vs. cinco tipos de vinculos no KG

Na Secao 3.3 (L201), o texto afirma: "as relacoes capturam **quatro** tipos de vinculos". Entretanto, a lista que se segue (L203-208) contem **cinco** itens:
1. pertence_a
2. detalha
3. define
4. definido_em
5. estabelece_medida

Incongruencia entre o texto ("quatro") e a lista (cinco). Nota: a Secao 3.7 (L254-262) corretamente afirma "cinco padroes estruturais", mas a Secao 3.3 contradiz isso.

### 10. [ABSTRACT/RESUMO] Frase sobre economia de fontes e sintaticamente truncada

No Abstract (L27), a frase:
> "...using on average only 6.8 sources compared to 10.0 in static configurations, evidencing superior context efficiency. For medium-complexity queries..."

O trecho "using on average only 6.8 sources compared to 10.0 in static configurations" esta sintaticamente desconectado -- e um participio absoluto sem sujeito claro que interrompe o fluxo entre a clausula sobre degradacao e a clausula sobre "superior context efficiency". O mesmo problema ocorre no Resumo (L33).

### 11. [ABSTRACT/RESUMO] Redundancia na mencao de consultas medias

Tanto o Abstract quanto o Resumo mencionam "54% CAR em consultas medias" DUAS VEZES cada:
- Abstract: "...with superior performance on medium-complexity queries (54% CAR)" e depois "For medium-complexity queries, the system reaches 54% Citation Article Rate, outperforming all other configurations."
- Resumo: "desempenho superior em consultas de complexidade media (54% CAR)" e depois "Em consultas de complexidade media, o sistema atinge 54% em Citation Article Rate, superando todas as demais configuracoes."

Repetir o mesmo dado duas vezes em ~150 palavras e desperdicar espaco precioso do Abstract/Resumo.

### 12. [ESTRUTURA SECAO] Numeracao de subsecoes na Secao 3

A Secao 3 possui 7 subsecoes (3.1 a 3.7), o que e excessivo. Em particular:
- Secao 3.3 (Recuperacao Tripla) ja descreve o KG em detalhes.
- Secao 3.7 (Knowledge Graph Legal: Extracao de Triplets) repete informacoes sobre o KG com nivel de detalhe adicional (padroes regex).

O resultado e que o KG e discutido em dois lugares distintos (3.3 e 3.7), quebrando o fluxo logico. O conteudo de 3.7 deveria ser integrado a 3.3 ou colocado como subsecao dentro de 3.3.

### 13. [SIGNIFICANCIA ESTATISTICA] Sem melhoria em relacao a R0

O artigo continua fazendo afirmacoes como "superando todas as demais configuracoes" (L33, L470) sem qualquer teste de significancia. Com 35 consultas medias, a diferenca entre HyPA-RAG (54% CAR) e Hibrido fixo (49% CAR) corresponde a ~1,75 consultas. Isso pode ser artefato amostral.

A revisao anterior (R0, item 13) ja exigiu reconhecimento explicito ou teste estatistico. A Secao 5.6 (Limitacoes) nao aborda este ponto.

### 14. [DATASET] Disponibilizacao publica nao mencionada

A revisao anterior (R0, item 14) solicitou a disponibilizacao publica do dataset de 100 consultas. O artigo nao menciona disponibilizacao, apesar de ja existir um repositorio GitHub (https://github.com/vsousadelvek/ecolex-rag.git, citado indiretamente). Para um workshop como o WCAMA, onde a reprodutibilidade e valorizada, esta omissao e uma fraqueza.

### 15. [FORMATO SBC] Figura 1 em ASCII art (verbatim)

A Figura 1 (L102-160) e um diagrama em \begin{verbatim}, renderizado em fonte monoespadada. Embora funcional para visualizacao, isto e inaceitavel para submissao final a conferencia. O template SBC espera figuras vetoriais (PDF/EPS) ou, no minimo, imagens rasterizadas de alta qualidade. A figura em verbatim:
- Nao escala corretamente com o zoom do PDF.
- Tem aparencia amadora.
- Pode ultrapassar as margens do template SBC dependendo da fonte.

### 16. [LATEX] Label com caractere acentuado

Os labels tab:parâmetros (L230), tab:legislações (L277) e tab:médias (L403) contem caracteres acentuados (â, õ, é). Embora o LaTeX com UTF-8 possa processar isso, e uma pratica fragil que pode causar erros em diferentes engines (pdflatex vs. lualatex vs. xelatex) ou em sistemas de cross-referencing. A pratica padrao e usar labels ASCII: tab:parametros, tab:legislacoes, tab:medias.

### 17. [LINGUAGEM] Alternancia inconsistente entre ingles e portugues em termos tecnicos

O artigo oscila entre:
- "Lei Retrieval Rate (LRR)" / "Article Retrieval Rate (ARR)" -- ingles
- "Cit. Lei" / "Cit. Art." -- abreviacao em portugues nas tabelas
- "Citation Law Rate" / "Citation Article Rate" -- ingles no texto
- "Lei Ret." / "Art. Ret." -- abreviacao mista nas tabelas

Essa inconsistencia nao e grave, mas e desnecessaria. Sugestao: definir uma vez as metricas em portugues com o nome ingles entre parenteses, e usar consistentemente a mesma abreviacao em tabelas e texto.

### 18. [CONTEUDO] Contribuicao do KG superestimada

Na discussao (L466): "o Hibrido fixo (BM25+Semantic+KG) alcanca Citation Law Rate de 66%, superior aos 65% do BM25+Semantic (sem KG), indicando que os triplets do KG adicionam informacao estrutural complementar que melhora a capacidade do LLM de citar legislacoes corretamente."

Uma diferenca de 1% em 100 consultas = 1 consulta. Afirmar que o KG "adiciona informacao estrutural complementar" com base em 1 consulta de diferenca e estatisticamente indefensavel. O texto deveria qualificar: "sugere, embora sem significancia estatistica, que..."

### 19. [CONTEUDO] Afirmacao no Resumo/Abstract sobre "superior performance on medium-complexity queries" sem qualificacao

O Abstract afirma "with superior performance on medium-complexity queries (54% CAR)" como se fosse um resultado robusto. Entretanto:
- A diferenca para o segundo colocado (Hibrido fixo, 49%) e de 5 pontos percentuais, mas sobre apenas 35 consultas.
- Nao ha intervalo de confianca nem teste de hipotese.
- O Resumo em portugues replica o mesmo problema.

A afirmacao deveria ser qualificada: "...suggesting superior performance..." ou "...indicating a tendency toward superior performance...".

### 20. [LATEX] Potenciais erros de compilacao

Verificando o LaTeX, os seguintes pontos podem gerar warnings ou erros:
- L339: "contémo" -- se o LaTeX processar isso como uma unica palavra, pode gerar word break incorreto.
- Palavras coladas como "sãoempregadas", "nãocapturam" etc. serao renderizadas como uma unica palavra sem espaco, tornando o texto ilegivel.
- Labels com acentos (item 16) podem gerar warnings de "label changed" em recompilacoes.

---

## QUESTIONAMENTOS DIRETOS AO AUTOR

Q1. A correcao de acentuacao foi realizada por script automatico? O padrao de erros (palavras coladas, acentos em posicoes erradas) sugere substituicao por regex com falhas de captura. Recomendo revisar manualmente todo o texto apos a correcao automatica.

Q2. Por que as colunas Fontes e Tempo foram omitidas das tabelas de breakdown (tab:complexas, tab:medias, tab:simples) quando os dados estao disponíveis? A distribuicao de fontes por complexidade (5,1/6,1/10,4) e o tempo de 96,3s em consultas complexas sao informacoes essenciais para a narrativa de tradeoff.

Q3. Na Secao 3.3 (L201), o texto afirma "quatro tipos de vinculos" mas lista cinco. Qual e o correto?

Q4. O dataset de 100 consultas sera disponibilizado como material suplementar ou no repositorio GitHub? A ausencia de disponibilizacao compromete a reprodutibilidade.

Q5. O autor considera substituir a citacao generica aos Anais do WCAMA 2025 por uma referencia a um artigo especifico que exemplifique as aplicacoes de IA em gestao ambiental mencionadas no texto?

Q6. Dado que a diferenca entre HyPA-RAG e Hibrido fixo em CAR geral e de 1 ponto percentual (48% vs. 49%), e que o HyPA-RAG e o mais lento (43,5s vs. 23,8s), qual e o argumento concreto para preferir o HyPA-RAG ao Hibrido fixo em um cenario de producao?

---

## LISTA DE PROBLEMAS (NUMERADA)

### Criticos (impedem aceite)

1. **45+ acentos faltantes ou incorretos** no texto LaTeX (item 1 acima).
2. **15 ocorrencias de palavras coladas** sem espaco (item 2 acima).
3. **3 acentos indevidos** em posicoes erradas (item 3 acima).

### Importantes (exigem correcao antes do aceite)

4. **Incongruencia "quatro vs. cinco" tipos de vinculos no KG** (item 9).
5. **Referencia wcama:2025 mal formatada** -- campo author incorreto, citacao imprecisa (item 5).
6. **Tabelas de breakdown sem colunas Fontes e Tempo** (item 7).
7. **Tempo de 96,3s em consultas complexas nao mencionado** (item 8).
8. **Redundancia no Abstract/Resumo** -- 54% CAR mencionado duas vezes (item 11).
9. **Formula RRF duplicada** entre Secoes 2.2 e 3.4 (item 6).
10. **Abstract sintaticamente truncado** na frase sobre economia de fontes (item 10).

### Recomendados (melhoram a qualidade)

11. **Labels LaTeX com caracteres acentuados** -- trocar por ASCII (item 16).
12. **Figura 1 em verbatim** -- substituir por figura vetorial (item 15).
13. **KG discutido em dois lugares** (Secoes 3.3 e 3.7) -- consolidar (item 12).
14. **Contribuicao do KG superestimada** -- qualificar a diferenca de 1% (item 18).
15. **Afirmacoes sem significancia estatistica** -- qualificar "superior performance" (itens 13, 19).
16. **Disponibilizacao publica do dataset** nao mencionada (item 14).
17. **Alternancia de idioma nos termos tecnicos** -- padronizar (item 17).

---

## SUGESTOES DE MELHORIA (PRIORIZADAS)

### Prioridade 1 -- Obrigatorias para aceite

1. Executar revisao manual completa de acentuacao, palavra por palavra. Nao confiar apenas em substituicao automatica.
2. Corrigir todas as 15 ocorrencias de palavras coladas (lista no item 2).
3. Corrigir os 3 acentos indevidos (item 3).
4. Corrigir "quatro tipos" para "cinco tipos" na Secao 3.3 (L201).
5. Reformatar a referencia wcama:2025 ou substitui-la por artigo especifico.

### Prioridade 2 -- Fortemente recomendadas

6. Adicionar colunas Fontes e Tempo nas tabelas tab:complexas, tab:medias e tab:simples.
7. Discutir o tempo de 96,3s em consultas complexas na Secao 5.5 (Discussao de tempo).
8. Remover duplicacao do "54% CAR" no Abstract e Resumo.
9. Eliminar a segunda equacao RRF (eq:rrf, L75-78), mantendo apenas eq:rrf_detail.
10. Corrigir a frase truncada no Abstract/Resumo sobre economia de fontes.
11. Trocar labels com acentos por labels ASCII.

### Prioridade 3 -- Cosmeticas / para versao camera-ready

12. Substituir Figura 1 (verbatim) por diagrama vetorial.
13. Consolidar discussao do KG (Secoes 3.3 e 3.7).
14. Qualificar afirmacoes de superioridade com ressalva estatistica.
15. Adicionar nota sobre disponibilidade do dataset e codigo.
16. Padronizar nomes das metricas em tabelas e texto.

---

## AVALIACAO GERAL

| Criterio | Nota R0 | Nota R1 | Comentario |
|:---|:---:|:---:|:---|
| Originalidade | 7 | 7 | Inalterada -- adaptacao valida do HyPA-RAG ao dominio brasileiro |
| Rigor metodologico | 5 | 6 | Melhoria pela transparencia em consultas simples; ainda sem significancia estatistica |
| Clareza da escrita | 8 | 6 | REBAIXADA devido a 45+ erros de acentuacao e 15 palavras coladas -- texto ilegivel em trechos |
| Qualidade dos experimentos | 6 | 7 | Melhoria pela inclusao de tab:simples e exemplo qualitativo |
| Relevancia para o WCAMA | 9 | 9 | Inalterada -- excelente adequacao tematica |
| Completude | 6 | 7.5 | Tabelas completas agora; faltam Fontes/Tempo nos breakdowns e tempo de 96,3s |
| Reproducibilidade | 5 | 5 | Inalterada -- dataset nao disponibilizado |
| Impacto potencial | 7 | 7 | Inalterado |
| Honestidade dos resultados | 5 | 8 | MELHORIA SIGNIFICATIVA -- tradeoffs agora discutidos honestamente |
| **NOTA GERAL** | **6.5** | **7.0 / 10** | **Minor Revision. Artigo substancialmente melhorado, mas erros de portugues impedem aceite imediato.** |

---

## VEREDITO FINAL

### MINOR REVISION

**Justificativa:** O artigo evoluiu significativamente entre R0 e R1. As correcoes mais importantes -- transparencia sobre degradacao em consultas simples, exemplo qualitativo, narrativa honesta de tradeoff -- foram implementadas com competencia e demonstram maturidade cientifica do autor. A coerencia numerica esta impecavel (todos os valores cruzados conferem). A estrutura argumentativa e agora equilibrada entre pontos fortes e limitacoes.

Contudo, a quantidade de erros de portugues residuais (45+ acentos, 15 palavras coladas, 3 acentos indevidos) e inaceitavel para publicacao. Estes sao erros de surface-level que nao exigem reestruturacao do conteudo -- apenas revisao cuidadosa do texto. Uma passada manual completa + correcao dos 5 itens de Prioridade 1 seria suficiente para aceite.

**Recomendacao:** Aceite condicional apos correcao dos itens de Prioridade 1 (obrigatorios) e Prioridade 2 (fortemente recomendados). Nao ha necessidade de nova rodada completa de revisao se os erros forem puramente linguisticos.

---

## NOTA COMPARATIVA R0 vs. R1

| Aspecto | R0 | R1 | Evolucao |
|---------|----|----|----------|
| Veredito | MAJOR REVISION | MINOR REVISION | Melhoria de 1 nivel |
| Nota geral | 6.5 | 7.0 | +0.5 |
| Itens criticos R0 resolvidos | -- | 5 de 7 (71%) | Boa taxa de resolucao |
| Novos problemas encontrados | -- | Acentuacao residual (grave) | Problema tecnico, nao conceitual |
| Maior melhoria | -- | Honestidade nos resultados | De 5 para 8 |
| Maior regressao | -- | Clareza da escrita (acentuacao) | De 8 para 6 |

O artigo esta no caminho certo. Uma revisao final focada em portugues e nos itens de Prioridade 1 e 2 elevaria o trabalho a nivel de aceite para o WCAMA 2026.
