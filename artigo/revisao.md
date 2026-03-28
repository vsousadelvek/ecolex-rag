# Revisao Critica -- EcoLex RAG: Sistema HyPA-RAG com Legal-BERTimbau para Suporte Explicavel a Decisao em Gestao Ambiental Brasileira

**Artigo submetido ao:** WCAMA 2026 (Workshop de Computacao Aplicada a Gestao do Meio Ambiente e Recursos Naturais) -- CSBC 2026
**Data da revisao:** 2026-03-28
**Revisor:** Agente Revisor Senior (Claude Opus 4.6)

---

## Veredito Preliminar: MAJOR REVISION (com tendencia a aceite condicional)

O artigo apresenta uma proposta relevante e tecnicamente articulada. A arquitetura e bem descrita, o estudo de ablacao e estruturado e a narrativa geral e coerente. Contudo, ha problemas de inconsistencia numerica entre os dados brutos e o texto, lacunas argumentativas na defesa do HyPA-RAG como contribuicao principal, e questoes de completude que precisam ser resolvidas antes de publicacao.

---

## FALHAS CRITICAS

### 1. [INCONSISTENCIA NUMERICA GRAVE] Dados da Tabela 6 (consultas medias) divergem da fonte de dados brutos

**Na Tabela 6 do artigo (consultas medias), o HyPA-RAG reporta:**
- Lei Ret.: 66%, Art. Ret.: 63%, Cit. Lei: 63%, Cit. Art.: 54%

**Nos dados brutos (`data/ablation_table.md`), a linha correspondente e:**
- Lei Ret.: 66%, Art. Ret.: 63%, Cit. Lei: 63%, Cit. Art.: 54%

Os valores da Tabela 6 estao CONSISTENTES com a fonte de dados brutos. Verificacao OK.

### 2. [INCONSISTENCIA NUMERICA GRAVE] Tabela 5 (consultas complexas) -- todos os valores CONFERIDOS

**No artigo (Tabela 5), HyPA-RAG:**
- Lei Ret.: 64%, Art. Ret.: 52%, Cit. Lei: 68%, Cit. Art.: 52%

**Nos dados brutos (`data/ablation_table.md`):**
- Lei Ret.: 64%, Art. Ret.: 52%, Cit. Lei: 68%, Cit. Art.: 52%

Valores consistentes. Verificacao OK.

### 3. [INCONSISTENCIA NUMERICA GRAVE] Tabela 4 (agregada) -- todos os valores CONFERIDOS

**No artigo (Tabela 4), HyPA-RAG:**
- Lei Ret.: 65%, Art. Ret.: 56%, Cit. Lei: 65%, Cit. Art.: 48%, Fontes: 6,8, Tempo: 43,5

**Nos dados brutos:**
- Lei Ret.: 65%, Art. Ret.: 56%, Cit. Lei: 65%, Cit. Art.: 48%, Fontes: 6,8, Tempo: 43,5

Valores consistentes. Verificacao OK.

### 4. [LACUNA GRAVE] Ausencia de dados de consultas simples no artigo

O arquivo `data/ablation_table.md` contem um breakdown para consultas **simples** (40 consultas), mas o artigo NAO apresenta esses dados em nenhuma tabela. O artigo inclui:
- Tabela 4: resultados agregados (100 consultas) -- OK
- Tabela 5: consultas complexas (25 consultas) -- OK
- Tabela 6: consultas medias (35 consultas) -- OK
- **Tabela para consultas simples (40 consultas): AUSENTE**

Isso e particularmente problematico porque as consultas simples sao o maior estrato (40 de 100, ou 40% do dataset), e os dados brutos revelam um fato que o artigo OCULTA (intencionalmente ou nao):

**Nas consultas simples, o HyPA-RAG apresenta QUEDA significativa de desempenho:**
- HyPA-RAG: Art. Ret. = 52%, Cit. Art. = 40% (com 5,1 fontes)
- BM25-only: Art. Ret. = 82%, Cit. Art. = 50% (com 10,0 fontes)
- Hibrido fixo: Art. Ret. = 70%, Cit. Art. = 50% (com 10,0 fontes)

O HyPA-RAG perde 30 pontos percentuais em Article Retrieval e 10 pontos em Citation Article Rate em relacao ao BM25-only nas consultas simples. Essa degradacao e mascarada pela media agregada (Tabela 4) e pela omissao da tabela de consultas simples.

**Acao requerida:** Incluir obrigatoriamente uma tabela com os resultados das consultas simples e discutir honestamente a degradacao causada pela reducao agressiva de top_k=5.

### 5. [INCONSISTENCIA ARGUMENTATIVA] O Resumo/Abstract superestima os resultados

O Resumo afirma: "a configuracao HyPA-RAG alcanca desempenho competitivo em recuperacao e citacao (65% em Lei Retrieval, 48% em Citation Article Rate)."

Isso e tecnicamente correto mas retorico. O artigo cuidadosamente seleciona as metricas onde o HyPA-RAG empata (Lei Retrieval, Citation Article Rate) e omite que:
- Em **Article Retrieval**, o HyPA-RAG (56%) fica atras do BM25-only (70%), Semantic-only (53% -- empate), BM25+Semantic (66%) e Hibrido fixo (59%).
- Em **Citation Law Rate**, o HyPA-RAG (65%) empata com BM25+Semantic (65%) mas perde para o Hibrido fixo (66%).

Dizer "desempenho competitivo" quando o sistema e o **4o de 6** em Article Retrieval e uma distorcao retorica. O autor deve ser mais preciso no Resumo ou qualificar adequadamente o tradeoff.

### 6. [INCONSISTENCIA ARGUMENTATIVA] "Economia de 32% de fontes" nao e necessariamente uma virtude

A narrativa central e que o HyPA-RAG usa 6,8 fontes vs. 10,0 das configuracoes estaticas (32% menos), mas mantem desempenho "competitivo". Contudo:

- O HyPA-RAG **perde** em Article Retrieval (56% vs. 70% do BM25-only, 66% do BM25+Semantic, 59% do Hibrido fixo).
- A "economia de fontes" e na verdade uma **subrecuperacao** em consultas simples (top_k=5), que **causa** queda de desempenho.
- O argumento de eficiencia so seria valido se houvesse uma restricao real de contexto (janela pequena, custo de API). Com Mistral 7B rodando localmente em FP16, o custo marginal de 3,2 fontes adicionais e negligenciavel.

**Acao requerida:** Reformular o argumento de "economia de fontes" como tradeoff explicito e justificar por que essa economia e desejavel no cenario de uso (se e que e).

### 7. [LACUNA METODOLOGICA] Classificador de complexidade nao e validado

O classificador heuristico (Secao 3.2) e um componente central da arquitetura, mas:
- Nao ha **avaliacao da acuracia do classificador**. Quantas consultas ele classifica corretamente?
- Nao ha **ground truth** de complexidade: quem definiu se cada consulta do dataset e simples/media/complexa? O proprio classificador? Um anotador humano? Se foi o classificador, ha circularidade.
- Nao ha **analise de erros** do classificador: quantas consultas foram classificadas incorretamente e como isso afetou os resultados?
- Os limiares (s <= 2, 3 <= s <= 5, s >= 6) sao arbitrarios e nao justificados.

Esse e um ponto ja reconhecido nas Limitacoes (Secao 5.5), mas deveria ser discutido na analise de resultados, pois o classificador pode ser a causa raiz da degradacao em consultas simples.

### 8. [QUESTAO FACTUAL] COP30 -- Data e verificacao

O artigo afirma que a COP30 foi "realizada em Belem do Para em novembro de 2025". A COP30 de fato esta/esteve programada para Belem em novembro de 2025. O autor deve garantir que, na data de submissao ao WCAMA 2026, essa informacao esteja atualizada com o que efetivamente ocorreu (se houve adiamentos, mudancas de local, etc.).

### 9. [REFERENCIA VAGA] "[WCAMA 2025]" nao e referencia valida

Na Secao 2.4, o texto cita "[WCAMA 2025]" como referencia generica. Isso nao e uma referencia bibliografica aceitavel. Ou se cita um artigo especifico do WCAMA 2025 que trate de IA aplicada a gestao ambiental, ou se remove a citacao.

### 10. [LACUNA NAS REFERENCIAS] Referencia ausente: Kalra et al. (2024)

A referencia [Kalra et al. 2024] esta listada e citada no texto -- OK. Mas verificando a lista de referencias completa, observa-se que:

- **WCAMA 2025** e citado no texto (Secao 2.4) mas NAO consta na lista de referencias. Isso e uma citacao orfã.

### 11. [FORMATO SBC] Verificacao de conformidade

O artigo esta em Markdown, nao em LaTeX com o template SBC. Para submissao ao WCAMA/CSBC, e obrigatorio usar o template LaTeX da SBC (disponivel em https://www.sbc.org.br/). Considerando que este Markdown e provavelmente um rascunho a ser convertido, os seguintes pontos devem ser observados na conversao:

- **Limite de paginas:** O WCAMA tipicamente aceita artigos de 10-12 paginas no formato SBC. O conteudo atual parece adequado em extensao.
- **Figuras:** A "Figura 1" esta em ASCII art. Na versao final, deve ser uma figura vetorial (PDF/EPS) de qualidade adequada.
- **Equacoes:** As equacoes estao em notacao LaTeX ($...$, $$...$$), o que facilita a conversao.
- **Acentuacao:** O texto NAO possui acentos em portugues (e.g., "Gestao" em vez de "Gestao", "Geracao" em vez de "Geracao"). Se isso e intencional para o Markdown, deve ser corrigido na versao LaTeX.
- **Resumo e Abstract:** Ambos estao presentes -- OK para SBC.
- **Palavras-chave / Keywords:** Presentes -- OK.
- **Afiliacao do autor:** Presente, mas falta o co-orientador/orientador se houver. O WCAMA tipicamente exige a indicacao de todos os autores e suas afiliacoes. Se este for um trabalho de dissertacao, o orientador deve constar como co-autor.

### 12. [LINGUAGEM] Ausencia sistematica de acentuacao

Todo o texto esta sem acentos graficos:
- "Gestao" -> "Gestao" (sem acento no original)
- "Geracao" -> "Geracao"
- "decisao" -> "decisao"
- "Explicavel" -> "Explicavel"

Embora isso possa ser uma limitacao do formato Markdown/encoding, e um problema serio se o texto final for submetido assim. Na conversao para LaTeX com UTF-8, todos os acentos devem ser restaurados.

### 13. [RIGOR METODOLOGICO] Falta de significancia estatistica

- Com apenas 25 consultas complexas e 35 medias, diferencas de 1-2 pontos percentuais (como 49% vs. 48%) estao dentro da margem de variacao de uma unica consulta. Nenhum teste estatistico e reportado.
- Uma unica consulta em 25 corresponde a 4 pontos percentuais. Afirmar que o HyPA-RAG "supera" o Hibrido fixo em consultas complexas (52% vs. 48%) com base em 1 consulta de diferenca e estatisticamente indefensavel.

**Acao requerida:** Reconhecer explicitamente que as diferencas entre configuracoes sao frequentemente de 1-2 consultas e que, dado o tamanho do dataset, nao se pode afirmar superioridade estatistica. Alternativamente, realizar testes de significancia (McNemar, bootstrap confidence intervals).

### 14. [RIGOR METODOLOGICO] Dataset de 100 consultas construido pelos proprios autores

O dataset nao e padronizado, nao e publico, e nao foi anotado por terceiros independentes. Isso levanta questoes de:
- **Viés de confirmacao:** As consultas podem ter sido (inconscientemente) formuladas para favorecer a arquitetura proposta.
- **Nao-reprodutibilidade:** Sem acesso ao dataset, ninguem pode replicar os resultados.
- **Questionamento ja parcialmente abordado nas Limitacoes (Secao 5.5)**, mas merece enfase maior.

**Acao requerida:** Disponibilizar o dataset publicamente (e.g., como material suplementar ou repositorio GitHub). O repositorio ja existe (https://github.com/vsousadelvek/ecolex-rag.git), entao incluir o dataset la seria trivial.

### 15. [COMPLETUDE] Falta de avaliacao qualitativa

O artigo nao apresenta nenhum exemplo de resposta gerada pelo sistema. Para um sistema de suporte a decisao, mostrar ao menos 1-2 exemplos de respostas (com a estrutura FUNDAMENTACAO LEGAL > ANALISE > CONCLUSAO) e essencial para que o leitor julgue a qualidade pratica do sistema.

### 16. [RIGOR METODOLOGICO] Unico LLM testado

O pipeline inteiro e avaliado com um unico LLM (Mistral 7B). A contribuicao do artigo e sobre a arquitetura de recuperacao (HyPA-RAG), mas a metrica principal (Citation Article Rate) depende tanto do retriever quanto do gerador. Sem testar ao menos um segundo LLM, e impossivel isolar a contribuicao da recuperacao adaptativa da capacidade do gerador.

Isso ja consta nas Limitacoes e trabalhos futuros, mas enfraquece significativamente as conclusoes.

### 17. [CLAREZA] A relacao entre Knowledge Graph e fusao e subexplorada

A Secao 3.3 descreve cinco tipos de relacoes no KG, mas:
- Nao ha quantificacao: quantos triplets de cada tipo foram gerados? Dos 1.714 triplets, qual a distribuicao?
- A Secao 5.4 afirma que o KG contribui na fusao (Hibrido fixo 66% CLR vs. 65% do BM25+Semantic), mas uma diferenca de 1% em 100 consultas e literalmente 1 consulta. Isso nao e evidencia.

### 18. [REDUNDANCIA NA FORMULA RRF]

A formula do RRF e apresentada DUAS vezes: na Secao 2.2 (equacao na revisao da literatura) e na Secao 3.4 (metodologia). A primeira ocorrencia pode ser mantida como contextualizacao teorica, mas a repeticao na Secao 3.4 e redundante. Sugere-se manter apenas na Secao 3.4 e referenciar a definicao na Secao 2.2 de forma textual.

### 19. [LINGUAGEM] Citacao de artigo no passado vs. presente

O artigo oscila entre presente ("O EcoLex RAG implementa", "O classificador opera") e passado ("demonstrou que"). Para um artigo cientifico, o presente deve ser usado para descrever a arquitetura e o passado para descrever resultados experimentais. A maioria do texto segue essa convencao, mas ha inconsistencias pontuais.

### 20. [QUESTAO TECNICA] Tempo de resposta do HyPA-RAG nas consultas complexas

Os dados brutos revelam que o tempo medio do HyPA-RAG nas consultas complexas e de **96,3 segundos** -- mais que o dobro do segundo mais lento (BM25+Semantic com 47,0s). Este dado NAO aparece no artigo (ja que a tabela de breakdown simples foi omitida e a de complexas nao inclui Fontes/Tempo).

Na discussao (Secao 5.4), o texto menciona "43,5s" como tempo medio geral, mas oculta que consultas complexas levam ~1,5 minuto. Isso deve ser discutido.

---

## SUGESTOES DE MELHORIA

### Alta Prioridade (obrigatorias para aceite)

1. **Incluir Tabela 7 com resultados de consultas simples** e discutir honestamente a degradacao de desempenho com top_k=5.
2. **Incluir colunas de Fontes e Tempo nas Tabelas 5, 6 e na nova Tabela 7**, como feito na Tabela 4. Os dados brutos possuem esses valores.
3. **Corrigir a narrativa do Resumo/Abstract** para nao superestimar "desempenho competitivo" -- qualificar o tradeoff.
4. **Remover ou substituir a citacao "[WCAMA 2025]"** por uma referencia completa a um artigo especifico.
5. **Disponibilizar o dataset de 100 consultas** publicamente no repositorio GitHub.
6. **Adicionar 1-2 exemplos qualitativos** de respostas geradas pelo sistema.
7. **Discutir o tempo de 96,3s** nas consultas complexas e suas implicacoes praticas.

### Media Prioridade (fortemente recomendadas)

8. **Reconhecer a ausencia de significancia estatistica** nas diferencas entre configuracoes, dada a escala do dataset.
9. **Reportar a distribuicao dos 1.714 triplets** por tipo de relacao no KG.
10. **Eliminar a duplicacao da formula RRF** entre Secoes 2.2 e 3.4.
11. **Discutir a validacao do classificador de complexidade**: quem definiu o ground truth de complexidade das 100 consultas?
12. **Incluir orientador como co-autor** se este for trabalho de mestrado (pratica padrao em venues brasileiras).

### Baixa Prioridade (cosmeticas)

13. Corrigir todos os acentos na versao LaTeX final.
14. Converter a Figura 1 de ASCII art para figura vetorial.
15. Uniformizar o uso de tempos verbais (presente para arquitetura, passado para resultados).
16. O paragrafo sobre COP30 na Introducao e na Conclusao, embora relevante para contextualizacao, beira o "fluff". Considerar comprimir para 1-2 frases em vez de um paragrafo inteiro em cada secao.

---

## PONTOS FORTES

1. **Arquitetura bem projetada e descrita com rigor.** O pipeline HyPA-RAG e apresentado com clareza suficiente para reproducao. A formalizacao matematica do classificador de complexidade (Secao 3.2) e um ponto positivo.
2. **Estudo de ablacao estruturado.** As 6 configuracoes de ablacao sao bem escolhidas e permitem isolar a contribuicao de cada componente.
3. **Relevancia pratica indiscutivel.** O problema de consulta a legislacao ambiental brasileira e real, relevante e adequado ao escopo do WCAMA.
4. **Revisao da literatura competente.** A Secao 2 contextualiza bem o trabalho em relacao ao HyPA-RAG original, Legal-BERTimbau e RAG.
5. **Honestidade parcial nas limitacoes.** A Secao 5.5 reconhece limitacoes relevantes (dataset, LLM unico, classificador heuristico).
6. **Metricas de avaliacao adequadas.** As 4 metricas (LRR, ARR, CLR, CAR) cobrem tanto a recuperacao quanto a geracao.

---

## PONTOS FRACOS

1. **Omissao seletiva de dados desfavoraveis.** A ausencia da tabela de consultas simples, onde o HyPA-RAG performa significativamente pior, e o problema mais grave do artigo.
2. **Argumento central fragilizado.** A "economia de fontes" e o selling point do HyPA-RAG, mas vem acompanhada de queda de desempenho em 3 de 4 metricas. O tradeoff nao e apresentado honestamente.
3. **Tamanho insuficiente do dataset.** 100 consultas (sendo apenas 25 complexas) nao permitem conclusoes robustas. Diferencas de 1 consulta alteram os percentuais em 4%.
4. **Falta de significancia estatistica.** Nenhum teste e reportado, mas afirmacoes de "superioridade" sao feitas.
5. **Unico LLM.** Impossivel separar contribuicao do retriever vs. gerador.
6. **Tempo de resposta elevado.** 96,3s para consultas complexas e 43,5s na media nao sao discutidos adequadamente.
7. **Referencia orfã.** "[WCAMA 2025]" citada no texto mas ausente da lista de referencias.

---

## QUESTIONAMENTOS DIRETOS AO AUTOR

Q1. Por que a tabela de resultados das consultas simples foi omitida, sendo este o maior estrato do dataset (40/100)?

Q2. Dado que o BM25-only supera o HyPA-RAG em Article Retrieval (70% vs. 56%) e Citation Article Rate (45% vs. 48% -- empate pratico), e o HyPA-RAG e o mais lento (43,5s vs. 26,2s), qual e exatamente o cenario pratico em que um gestor ambiental deveria preferir o HyPA-RAG ao BM25-only?

Q3. O ground truth de complexidade das 100 consultas (simples/media/complexa) foi definido pelo classificador heuristico ou por anotacao humana independente? Se foi pelo classificador, a avaliacao e circular.

Q4. Com que criterio os limiares do classificador (s <= 2, 3 <= s <= 5, s >= 6) foram definidos? Foram testadas outras particoes?

Q5. O dataset de 100 consultas sera disponibilizado publicamente?

Q6. Por que o artigo nao inclui ao menos um exemplo de resposta gerada, dado que a explicabilidade e uma das contribuicoes alegadas?

Q7. A diferenca de 1% entre Hibrido fixo (66% CLR) e BM25+Semantic (65% CLR) e usada para argumentar que "o KG adiciona informacao estrutural complementar". O autor reconhece que isso corresponde a 1 consulta em 100?

---

## AVALIACAO GERAL

| Criterio | Nota (1-10) | Comentario |
|:---|:---:|:---|
| Originalidade | 7 | Adaptacao valida do HyPA-RAG ao dominio brasileiro, mas nao ha inovacao arquitetural significativa |
| Rigor metodologico | 5 | Omissao de dados, ausencia de testes estatisticos, dataset pequeno e nao validado externamente |
| Clareza da escrita | 8 | Texto bem estruturado, tecnico e fluido; linguagem academica adequada |
| Qualidade dos experimentos | 6 | Ablacao bem desenhada, mas dataset insuficiente e ausencia de dados de consultas simples |
| Relevancia para o WCAMA | 9 | Excelente adequacao tematica: IA + legislacao ambiental brasileira |
| Completude | 6 | Faltam tabela de consultas simples, exemplos qualitativos, e discussao de tempos por complexidade |
| Reproducibilidade | 5 | Codigo disponivel no GitHub, mas dataset nao e publico e alguns detalhes de implementacao faltam |
| Impacto potencial | 7 | Ferramenta util se desenvolvida alem do prototipo academico |
| **NOTA GERAL** | **6.5 / 10** | **Major Revision necessaria. Artigo promissor com lacunas criticas de transparencia nos resultados.** |

---

## NOTA FINAL DO REVISOR

O artigo tem merito cientifico e esta bem inserido no escopo do WCAMA. A arquitetura e relevante e o problema e real. Contudo, a omissao seletiva de dados desfavoraveis (tabela de consultas simples), a narrativa excessivamente otimista sobre a "economia de fontes" (que na verdade mascara subrecuperacao), e a ausencia de significancia estatistica comprometem a credibilidade dos resultados. Com as correcoes indicadas -- especialmente a inclusao honesta de todos os dados e a qualificacao adequada dos tradeoffs -- o artigo tem potencial para aceite no WCAMA 2026.

A recomendacao e: **MAJOR REVISION** -- enderecando obrigatoriamente os itens 1-7 de alta prioridade antes de resubmissao.
