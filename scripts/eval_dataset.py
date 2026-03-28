"""Dataset completo de avaliação para o sistema EcoLex RAG.

50 perguntas sobre legislação ambiental brasileira, distribuídas por:
  - Código Florestal (Lei 12.651/2012): 15 perguntas  (CF_001–CF_015)
  - PNMA (Lei 6.938/1981): 8 perguntas                (PNMA_001–PNMA_008)
  - SNUC (Lei 9.985/2000): 8 perguntas                (SNUC_001–SNUC_008)
  - Crimes Ambientais (Lei 9.605/1998): 8 perguntas   (CA_001–CA_008)
  - CONAMA 357/2005: 6 perguntas                       (C357_001–C357_006)
  - CONAMA 430/2011: 5 perguntas                       (C430_001–C430_005)

Complexidade:
  - simple  (20): uma lei, um artigo, resposta direta
  - medium  (18): condicionais, artigo com parágrafos
  - complex (12): multi-hop, cruzamento entre leis, comparativas

Formato de cada entrada (compatível com scripts/evaluate.py):
  - id              : identificador único (prefixo da lei + número)
  - question        : pergunta em linguagem natural
  - ground_truth    : resposta de referência com fundamentação legal
  - expected_law    : nome da lei esperada nas fontes recuperadas
  - expected_article: artigo esperado (ex: "Art. 4")
  - complexity      : "simple" | "medium" | "complex"
  - category        : categoria temática da pergunta

Usado pelos scripts evaluate.py e ablation.py.
"""

EVAL_DATASET_FULL: list[dict] = [
    # =========================================================================
    # CÓDIGO FLORESTAL (Lei 12.651/2012) — 15 perguntas
    # =========================================================================

    # ── CF – simple (6) ──────────────────────────────────────────────────────
    {
        "id": "CF_001",
        "question": (
            "Qual a largura mínima da faixa de APP para cursos d'água "
            "naturais com menos de 10 metros de largura?"
        ),
        "ground_truth": (
            "A faixa mínima de Área de Preservação Permanente para cursos "
            "d'água naturais com largura inferior a 10 metros é de 30 metros, "
            "medida desde a borda da calha do leito regular, conforme o "
            "Art. 4º, inciso I, alínea 'a' da Lei 12.651/2012 "
            "(Código Florestal)."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 4",
        "complexity": "simple",
        "category": "APP",
    },
    {
        "id": "CF_002",
        "question": (
            "Qual o raio mínimo de APP ao redor de nascentes e olhos "
            "d'água perenes?"
        ),
        "ground_truth": (
            "As áreas no entorno das nascentes e dos olhos d'água perenes, "
            "qualquer que seja sua situação topográfica, devem ter raio "
            "mínimo de 50 metros, conforme Art. 4º, inciso IV da "
            "Lei 12.651/2012."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 4",
        "complexity": "simple",
        "category": "APP",
    },
    {
        "id": "CF_003",
        "question": (
            "Qual o percentual mínimo de Reserva Legal para imóveis rurais "
            "situados em área de floresta na Amazônia Legal?"
        ),
        "ground_truth": (
            "O percentual mínimo de Reserva Legal é de 80% do imóvel "
            "situado em área de florestas na Amazônia Legal, conforme "
            "Art. 12, inciso I, alínea 'a' da Lei 12.651/2012."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 12",
        "complexity": "simple",
        "category": "Reserva Legal",
    },
    {
        "id": "CF_004",
        "question": (
            "O que o Código Florestal define como Área de Preservação "
            "Permanente (APP)?"
        ),
        "ground_truth": (
            "Conforme Art. 3º, inciso II da Lei 12.651/2012, Área de "
            "Preservação Permanente é a área protegida, coberta ou não por "
            "vegetação nativa, com a função ambiental de preservar os "
            "recursos hídricos, a paisagem, a estabilidade geológica e a "
            "biodiversidade, facilitar o fluxo gênico de fauna e flora, "
            "proteger o solo e assegurar o bem-estar das populações humanas."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 3",
        "complexity": "simple",
        "category": "APP",
    },
    {
        "id": "CF_005",
        "question": (
            "Qual o percentual mínimo de Reserva Legal para imóveis "
            "localizados em área de cerrado dentro da Amazônia Legal?"
        ),
        "ground_truth": (
            "Para imóveis situados em área de cerrado na Amazônia Legal, "
            "o percentual mínimo de Reserva Legal é de 35%, conforme "
            "Art. 12, inciso I, alínea 'b' da Lei 12.651/2012."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 12",
        "complexity": "simple",
        "category": "Reserva Legal",
    },
    {
        "id": "CF_006",
        "question": (
            "Qual a largura da faixa de APP para rios que possuem entre "
            "50 e 200 metros de largura?"
        ),
        "ground_truth": (
            "Para cursos d'água com largura entre 50 e 200 metros, a faixa "
            "mínima de APP é de 100 metros, conforme Art. 4º, inciso I, "
            "alínea 'c' da Lei 12.651/2012."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 4",
        "complexity": "simple",
        "category": "APP",
    },

    # ── CF – medium (5) ──────────────────────────────────────────────────────
    {
        "id": "CF_007",
        "question": (
            "Em quais hipóteses o Código Florestal autoriza a supressão "
            "de vegetação nativa em APP?"
        ),
        "ground_truth": (
            "A supressão de vegetação nativa em APP somente poderá ser "
            "autorizada em casos de utilidade pública, de interesse social "
            "ou de baixo impacto ambiental, conforme Art. 8º da "
            "Lei 12.651/2012. O §1º desse artigo exige autorização do "
            "órgão ambiental estadual competente, com adoção de medidas "
            "mitigatórias e compensatórias."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 8",
        "complexity": "medium",
        "category": "APP",
    },
    {
        "id": "CF_008",
        "question": (
            "Em que condições a APP pode ser computada no cálculo do "
            "percentual de Reserva Legal?"
        ),
        "ground_truth": (
            "Conforme Art. 15 da Lei 12.651/2012, é admitido o cômputo "
            "das APPs no cálculo da Reserva Legal desde que: (I) o "
            "benefício não implique conversão de novas áreas para uso "
            "alternativo do solo; (II) a área a ser computada esteja "
            "conservada ou em processo de recuperação; e (III) o "
            "proprietário tenha requerido inclusão do imóvel no Cadastro "
            "Ambiental Rural (CAR)."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 15",
        "complexity": "medium",
        "category": "Reserva Legal",
    },
    {
        "id": "CF_009",
        "question": (
            "Quais são as opções para regularização de déficit de "
            "Reserva Legal previstas no Código Florestal?"
        ),
        "ground_truth": (
            "Conforme Art. 66 da Lei 12.651/2012, o proprietário que "
            "possuía, em 22 de julho de 2008, área de Reserva Legal "
            "inferior ao exigido pode regularizar mediante: (I) recomposição "
            "da Reserva Legal; (II) regeneração natural da vegetação; ou "
            "(III) compensação da Reserva Legal. A recomposição pode ser "
            "feita com plantio intercalado de espécies nativas e exóticas "
            "em sistema agroflorestal, sendo que as exóticas não podem "
            "exceder 50% da área total."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 66",
        "complexity": "medium",
        "category": "Reserva Legal",
    },
    {
        "id": "CF_010",
        "question": (
            "Quais são as regras para áreas rurais consolidadas em APP "
            "de cursos d'água segundo o Código Florestal?"
        ),
        "ground_truth": (
            "Conforme Art. 61-A da Lei 12.651/2012, nas APPs de cursos "
            "d'água é autorizada a continuidade de atividades "
            "agrossilvipastoris, de ecoturismo e de turismo rural em áreas "
            "rurais consolidadas até 22 de julho de 2008. A extensão da "
            "faixa a ser recomposta varia conforme o tamanho do imóvel "
            "em módulos fiscais: para imóveis de até 1 módulo fiscal, "
            "a recomposição é de 5 metros; de 1 a 2 módulos, 8 metros; "
            "de 2 a 4 módulos, 15 metros."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 61-A",
        "complexity": "medium",
        "category": "APP",
    },
    {
        "id": "CF_011",
        "question": (
            "O que prevê o Código Florestal sobre o Programa de Apoio e "
            "Incentivo à Preservação e Recuperação do Meio Ambiente, "
            "incluindo pagamento por serviços ambientais?"
        ),
        "ground_truth": (
            "Conforme Art. 41 da Lei 12.651/2012, o Poder Executivo "
            "federal é autorizado a instituir programa de apoio e incentivo "
            "à conservação, incluindo pagamento ou incentivo a serviços "
            "ambientais como retribuição monetária ou não às atividades de "
            "conservação e melhoria dos ecossistemas (inciso I). Também "
            "prevê compensação por medidas de conservação ambiental e "
            "incentivos para comercialização, inovação e aceleração de "
            "ações de recuperação (incisos II e III)."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 41",
        "complexity": "medium",
        "category": "Instrumentos Econômicos",
    },

    # ── CF – complex (4) ────────────────────────────────────────────────────
    {
        "id": "CF_012",
        "question": (
            "Considere um imóvel rural de 500 hectares na Amazônia Legal, "
            "localizado em área de floresta, com um rio de 80 metros de "
            "largura em sua divisa. Quais são as exigências cumulativas "
            "de APP e Reserva Legal, e quando a APP pode ser computada "
            "na Reserva Legal?"
        ),
        "ground_truth": (
            "O imóvel deve manter: (1) APP de 100 metros nas faixas "
            "marginais do rio, conforme Art. 4º, I, 'c' da Lei 12.651/2012 "
            "(rios de 50 a 200 m de largura); e (2) Reserva Legal de 80% "
            "da área, conforme Art. 12, I, 'a'. A APP pode ser computada "
            "na Reserva Legal somente se atendidas as três condições do "
            "Art. 15: não implicar conversão de novas áreas, a área estar "
            "conservada ou em recuperação, e o imóvel estar inscrito no CAR."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 4",
        "complexity": "complex",
        "category": "APP",
    },
    {
        "id": "CF_013",
        "question": (
            "Quais as diferenças entre os percentuais de Reserva Legal "
            "para diferentes fitofisionomias e regiões do Brasil, e quais "
            "os fundamentos legais de cada um?"
        ),
        "ground_truth": (
            "Conforme Art. 12 da Lei 12.651/2012, os percentuais de "
            "Reserva Legal são: (I) na Amazônia Legal — (a) 80% em área "
            "de florestas, (b) 35% em área de cerrado, (c) 20% em área "
            "de campos gerais; (II) nas demais regiões do país — 20% do "
            "imóvel. A diferenciação reflete a importância ecológica e "
            "fragilidade dos biomas amazônicos."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 12",
        "complexity": "medium",
        "category": "Reserva Legal",
    },
    {
        "id": "CF_014",
        "question": (
            "A supressão de vegetação para uso alternativo do solo requer "
            "quais procedimentos prévios segundo o Código Florestal, e "
            "como isso se relaciona com o licenciamento ambiental da PNMA?"
        ),
        "ground_truth": (
            "Conforme Art. 26 da Lei 12.651/2012, a supressão de vegetação "
            "nativa para uso alternativo do solo depende de autorização do "
            "órgão ambiental estadual competente, com indicação pelo "
            "proprietário do uso alternativo e da localização da Reserva "
            "Legal. O Art. 9º e o Art. 10 da Lei 6.938/1981 (PNMA) "
            "complementam ao exigir licenciamento ambiental para atividades "
            "efetiva ou potencialmente poluidoras e a avaliação de impactos "
            "ambientais como instrumento obrigatório da política ambiental."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 26",
        "complexity": "complex",
        "category": "Uso Alternativo do Solo",
    },
    {
        "id": "CF_015",
        "question": (
            "Compare as faixas de APP exigidas pelo Código Florestal para "
            "rios de diferentes larguras e explique como o conceito de "
            "'área rural consolidada' altera essas exigências."
        ),
        "ground_truth": (
            "Conforme Art. 4º, I da Lei 12.651/2012, as faixas de APP "
            "variam: (a) 30 m para rios até 10 m; (b) 50 m para rios de "
            "10 a 50 m; (c) 100 m para rios de 50 a 200 m; (d) 200 m "
            "para rios de 200 a 600 m; (e) 500 m para rios com mais de "
            "600 m. Porém, o Art. 61-A, que trata de áreas rurais "
            "consolidadas até 22 de julho de 2008, flexibiliza essas "
            "exigências com faixas de recomposição menores, proporcionais "
            "ao tamanho do imóvel em módulos fiscais, variando de 5 a "
            "100 metros dependendo do caso."
        ),
        "expected_law": "Código Florestal",
        "expected_article": "Art. 4",
        "complexity": "complex",
        "category": "APP",
    },

    # =========================================================================
    # PNMA — Política Nacional do Meio Ambiente (Lei 6.938/1981) — 8 perguntas
    # =========================================================================

    # ── PNMA – simple (3) ───────────────────────────────────────────────────
    {
        "id": "PNMA_001",
        "question": (
            "Qual é o objetivo da Política Nacional do Meio Ambiente?"
        ),
        "ground_truth": (
            "Conforme Art. 2º da Lei 6.938/1981, a Política Nacional do "
            "Meio Ambiente tem por objetivo a preservação, melhoria e "
            "recuperação da qualidade ambiental propícia à vida, visando "
            "assegurar condições ao desenvolvimento socioeconômico, aos "
            "interesses da segurança nacional e à proteção da dignidade "
            "da vida humana."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 2",
        "complexity": "simple",
        "category": "Princípios",
    },
    {
        "id": "PNMA_002",
        "question": "Como a Lei 6.938/1981 define 'meio ambiente'?",
        "ground_truth": (
            "Conforme Art. 3º, inciso I da Lei 6.938/1981, meio ambiente "
            "é o conjunto de condições, leis, influências e interações de "
            "ordem física, química e biológica, que permite, abriga e rege "
            "a vida em todas as suas formas."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 3",
        "complexity": "simple",
        "category": "Definições",
    },
    {
        "id": "PNMA_003",
        "question": "Qual a composição e função do CONAMA no SISNAMA?",
        "ground_truth": (
            "Conforme Art. 6º, inciso II da Lei 6.938/1981, o CONAMA "
            "(Conselho Nacional do Meio Ambiente) é o órgão consultivo e "
            "deliberativo do SISNAMA, com a finalidade de assessorar, "
            "estudar e propor ao Conselho de Governo diretrizes de "
            "políticas governamentais para o meio ambiente e os recursos "
            "naturais, e deliberar sobre normas e padrões compatíveis com "
            "o meio ambiente ecologicamente equilibrado."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 6",
        "complexity": "simple",
        "category": "SISNAMA",
    },

    # ── PNMA – medium (3) ───────────────────────────────────────────────────
    {
        "id": "PNMA_004",
        "question": (
            "Quais são os instrumentos da Política Nacional do Meio "
            "Ambiente listados na Lei 6.938/1981?"
        ),
        "ground_truth": (
            "Conforme Art. 9º da Lei 6.938/1981, os instrumentos incluem: "
            "(I) estabelecimento de padrões de qualidade ambiental; "
            "(II) zoneamento ambiental; (III) avaliação de impactos "
            "ambientais; (IV) licenciamento e revisão de atividades "
            "efetiva ou potencialmente poluidoras; (V) incentivos à "
            "produção e instalação de equipamentos para melhoria da "
            "qualidade ambiental; (VI) criação de espaços territoriais "
            "protegidos; (VII) sistema nacional de informações sobre o "
            "meio ambiente; (VIII) Cadastro Técnico Federal de Atividades "
            "e Instrumentos de Defesa Ambiental; entre outros."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 9",
        "complexity": "medium",
        "category": "Instrumentos",
    },
    {
        "id": "PNMA_005",
        "question": (
            "Quais órgãos compõem a estrutura do SISNAMA e qual a função "
            "de cada nível?"
        ),
        "ground_truth": (
            "Conforme Art. 6º da Lei 6.938/1981, o SISNAMA é composto por: "
            "(I) órgão superior — Conselho de Governo, com função de "
            "assessorar o Presidente na formulação da política ambiental; "
            "(II) órgão consultivo e deliberativo — CONAMA; "
            "(III) órgão central — Ministério do Meio Ambiente; "
            "(IV) órgão executor — IBAMA; "
            "(V) órgãos seccionais — órgãos ou entidades estaduais; "
            "(VI) órgãos locais — órgãos ou entidades municipais."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 6",
        "complexity": "medium",
        "category": "SISNAMA",
    },
    {
        "id": "PNMA_006",
        "question": (
            "Qual o regime de responsabilidade civil por danos ambientais "
            "estabelecido pela PNMA e qual a obrigação do poluidor?"
        ),
        "ground_truth": (
            "Conforme Art. 14, §1º da Lei 6.938/1981, o poluidor é "
            "obrigado, independentemente da existência de culpa, a "
            "indenizar ou reparar os danos causados ao meio ambiente e a "
            "terceiros afetados por sua atividade. O Ministério Público "
            "da União e dos Estados terá legitimidade para propor ação de "
            "responsabilidade civil e criminal por danos ao meio ambiente. "
            "Trata-se de responsabilidade civil objetiva."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 14",
        "complexity": "medium",
        "category": "Responsabilidade Civil",
    },

    # ── PNMA – complex (2) ──────────────────────────────────────────────────
    {
        "id": "PNMA_007",
        "question": (
            "Como o licenciamento ambiental previsto na PNMA se relaciona "
            "com a exigência de EIA/RIMA e quais são as etapas do "
            "processo de licenciamento?"
        ),
        "ground_truth": (
            "O Art. 9º, incisos III e IV da Lei 6.938/1981 estabelece a "
            "avaliação de impactos ambientais e o licenciamento como "
            "instrumentos da PNMA. O Art. 10 determina que atividades "
            "utilizadoras de recursos ambientais, efetiva ou potencialmente "
            "poluidoras, dependem de prévio licenciamento do órgão "
            "ambiental competente. O licenciamento compreende três etapas: "
            "Licença Prévia (LP), Licença de Instalação (LI) e Licença de "
            "Operação (LO). O EIA/RIMA é exigido quando a atividade for "
            "potencialmente causadora de significativa degradação ambiental, "
            "servindo de base técnica para a concessão da LP."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 10",
        "complexity": "complex",
        "category": "Licenciamento",
    },
    {
        "id": "PNMA_008",
        "question": (
            "Compare as definições de 'degradação ambiental', 'poluição' "
            "e 'recursos ambientais' na PNMA e explique como essas "
            "definições fundamentam a responsabilidade objetiva do poluidor."
        ),
        "ground_truth": (
            "O Art. 3º da Lei 6.938/1981 define: (II) degradação da "
            "qualidade ambiental como a alteração adversa das "
            "características do meio ambiente; (III) poluição como a "
            "degradação que resulte de atividades que prejudiquem a saúde, "
            "segurança e bem-estar da população, criem condições adversas "
            "às atividades sociais e econômicas, afetem a biota ou lancem "
            "matéria ou energia em desacordo com padrões; (V) recursos "
            "ambientais como a atmosfera, águas, solo, subsolo, fauna e "
            "flora. A amplitude dessas definições fundamenta o Art. 14, "
            "§1º, que institui a responsabilidade civil objetiva: basta "
            "comprovar o dano e o nexo causal com a atividade, sem "
            "necessidade de demonstrar culpa."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 3",
        "complexity": "complex",
        "category": "Definições",
    },

    # =========================================================================
    # SNUC — Sistema Nacional de Unidades de Conservação (Lei 9.985/2000) — 8
    # =========================================================================

    # ── SNUC – simple (3) ───────────────────────────────────────────────────
    {
        "id": "SNUC_001",
        "question": (
            "Quais são os dois grupos de unidades de conservação previstos "
            "no SNUC?"
        ),
        "ground_truth": (
            "Conforme Art. 7º da Lei 9.985/2000, as unidades de conservação "
            "dividem-se em dois grupos: (I) Unidades de Proteção Integral, "
            "cujo objetivo básico é preservar a natureza, admitido apenas "
            "o uso indireto dos recursos naturais (§1º); e (II) Unidades "
            "de Uso Sustentável, cujo objetivo é compatibilizar a "
            "conservação da natureza com o uso sustentável de parcela dos "
            "seus recursos naturais (§2º)."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 7",
        "complexity": "simple",
        "category": "UC",
    },
    {
        "id": "SNUC_002",
        "question": (
            "O que é o plano de manejo de uma unidade de conservação e "
            "quando deve ser elaborado?"
        ),
        "ground_truth": (
            "Conforme Art. 2º, inciso XVII da Lei 9.985/2000, plano de "
            "manejo é o documento técnico que estabelece o zoneamento e "
            "as normas de uso da área e manejo dos recursos naturais da "
            "UC. O Art. 27 determina que as UCs devem dispor de plano de "
            "manejo, que deve ser elaborado no prazo de cinco anos a "
            "partir da data de criação da unidade."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 27",
        "complexity": "simple",
        "category": "Plano de Manejo",
    },
    {
        "id": "SNUC_003",
        "question": (
            "O que é uma zona de amortecimento de unidade de conservação?"
        ),
        "ground_truth": (
            "Conforme Art. 2º, inciso XVIII da Lei 9.985/2000, zona de "
            "amortecimento é o entorno de uma unidade de conservação onde "
            "as atividades humanas estão sujeitas a normas e restrições "
            "específicas, com o propósito de minimizar os impactos "
            "negativos sobre a unidade. O Art. 25 estabelece que as UCs, "
            "exceto APAs e RPPNs, devem possuir uma zona de amortecimento."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 25",
        "complexity": "simple",
        "category": "Zona de Amortecimento",
    },

    # ── SNUC – medium (3) ───────────────────────────────────────────────────
    {
        "id": "SNUC_004",
        "question": (
            "Quais são as categorias de unidades de conservação de "
            "Proteção Integral previstas no SNUC?"
        ),
        "ground_truth": (
            "Conforme Art. 8º da Lei 9.985/2000, o grupo das Unidades de "
            "Proteção Integral é composto por: (I) Estação Ecológica "
            "(Art. 9º); (II) Reserva Biológica (Art. 10); (III) Parque "
            "Nacional (Art. 11); (IV) Monumento Natural (Art. 12); e "
            "(V) Refúgio de Vida Silvestre (Art. 13). Todas têm como "
            "objetivo a preservação da natureza, admitindo apenas uso "
            "indireto dos recursos, com exceção do Monumento Natural e "
            "do Refúgio de Vida Silvestre, que podem ser constituídos em "
            "áreas particulares."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 8",
        "complexity": "medium",
        "category": "UC Proteção Integral",
    },
    {
        "id": "SNUC_005",
        "question": (
            "Quais são as categorias de unidades de conservação de Uso "
            "Sustentável previstas no SNUC?"
        ),
        "ground_truth": (
            "Conforme Art. 14 da Lei 9.985/2000, o grupo das Unidades de "
            "Uso Sustentável é composto por: (I) Área de Proteção "
            "Ambiental — APA (Art. 15); (II) Área de Relevante Interesse "
            "Ecológico — ARIE (Art. 16); (III) Floresta Nacional — FLONA "
            "(Art. 17); (IV) Reserva Extrativista — RESEX (Art. 18); "
            "(V) Reserva de Fauna (Art. 19); (VI) Reserva de "
            "Desenvolvimento Sustentável — RDS (Art. 20); e (VII) Reserva "
            "Particular do Patrimônio Natural — RPPN (Art. 21)."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 14",
        "complexity": "medium",
        "category": "UC Uso Sustentável",
    },
    {
        "id": "SNUC_006",
        "question": (
            "Quais são os requisitos para a criação de uma unidade de "
            "conservação e quais estudos são necessários?"
        ),
        "ground_truth": (
            "Conforme Art. 22 da Lei 9.985/2000, as unidades de "
            "conservação são criadas por ato do Poder Público. A criação "
            "deve ser precedida de estudos técnicos e de consulta pública "
            "que permitam identificar a localização, a dimensão e os "
            "limites mais adequados para a unidade. O §2º estabelece que "
            "para a criação de Estação Ecológica ou Reserva Biológica "
            "não é obrigatória a consulta pública."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 22",
        "complexity": "medium",
        "category": "Criação de UC",
    },

    # ── SNUC – complex (2) ──────────────────────────────────────────────────
    {
        "id": "SNUC_007",
        "question": (
            "Como funciona a compensação ambiental prevista no SNUC "
            "para empreendimentos de significativo impacto ambiental, "
            "e qual a relação com o licenciamento da PNMA?"
        ),
        "ground_truth": (
            "Conforme Art. 36 da Lei 9.985/2000, nos casos de "
            "licenciamento ambiental de empreendimentos de significativo "
            "impacto ambiental (assim considerado pelo órgão ambiental "
            "competente, com fundamento em EIA/RIMA), o empreendedor é "
            "obrigado a apoiar a implantação e manutenção de unidade de "
            "conservação do grupo de Proteção Integral. O montante de "
            "recursos não pode ser inferior a 0,5% dos custos totais de "
            "implantação do empreendimento. Esta obrigação conecta-se ao "
            "Art. 9º, incisos III e IV, e ao Art. 10 da Lei 6.938/1981 "
            "(PNMA), que estabelecem o EIA e o licenciamento como "
            "instrumentos obrigatórios da política ambiental."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 36",
        "complexity": "complex",
        "category": "Compensação Ambiental",
    },
    {
        "id": "SNUC_008",
        "question": (
            "Compare as diferenças entre Parque Nacional e Reserva "
            "Extrativista quanto a posse, uso de recursos e presença "
            "de populações tradicionais."
        ),
        "ground_truth": (
            "O Parque Nacional (Art. 11 da Lei 9.985/2000), de Proteção "
            "Integral, é de posse e domínio públicos, proíbe explorações "
            "ou aproveitamento dos recursos naturais, admite apenas uso "
            "indireto (pesquisa, educação, turismo ecológico) e exige "
            "desapropriação de áreas particulares. A Reserva Extrativista "
            "(Art. 18), de Uso Sustentável, é de domínio público com uso "
            "concedido às populações extrativistas tradicionais, permite "
            "a exploração sustentável dos recursos naturais e proíbe "
            "caça amadora ou profissional e exploração de recursos "
            "minerais. O contraste reflete a distinção do Art. 7º entre "
            "os grupos de Proteção Integral (uso indireto) e Uso "
            "Sustentável (uso direto regulado)."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 11",
        "complexity": "complex",
        "category": "UC Proteção Integral",
    },

    # =========================================================================
    # CRIMES AMBIENTAIS (Lei 9.605/1998) — 8 perguntas
    # =========================================================================

    # ── CA – simple (4) ─────────────────────────────────────────────────────
    {
        "id": "CA_001",
        "question": (
            "Qual a pena para quem pratica maus-tratos contra animais "
            "segundo a Lei de Crimes Ambientais?"
        ),
        "ground_truth": (
            "Conforme Art. 32 da Lei 9.605/1998, praticar ato de abuso, "
            "maus-tratos, ferir ou mutilar animais silvestres, domésticos "
            "ou domesticados, nativos ou exóticos, sujeita o infrator a "
            "pena de detenção de três meses a um ano, e multa. O §1º "
            "prevê as mesmas penas para quem realiza experiência dolorosa "
            "ou cruel em animal vivo, ainda que para fins didáticos ou "
            "científicos, quando existirem recursos alternativos. A pena "
            "é aumentada de um sexto a um terço se ocorre a morte do "
            "animal (§2º)."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 32",
        "complexity": "simple",
        "category": "Crimes Fauna",
    },
    {
        "id": "CA_002",
        "question": (
            "Qual a pena para quem destrói ou danifica floresta em área "
            "de preservação permanente?"
        ),
        "ground_truth": (
            "Conforme Art. 38 da Lei 9.605/1998, destruir ou danificar "
            "floresta considerada de preservação permanente, mesmo que em "
            "formação, ou utilizá-la com infringência das normas de "
            "proteção, sujeita o infrator a pena de detenção de um a "
            "três anos, ou multa, ou ambas as penas cumulativamente."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 38",
        "complexity": "simple",
        "category": "Crimes Flora",
    },
    {
        "id": "CA_003",
        "question": (
            "Qual a pena para quem exerce atividade potencialmente "
            "poluidora sem a devida licença ambiental?"
        ),
        "ground_truth": (
            "Conforme Art. 60 da Lei 9.605/1998, construir, reformar, "
            "ampliar, instalar ou fazer funcionar, em qualquer parte do "
            "território nacional, estabelecimentos, obras ou serviços "
            "potencialmente poluidores, sem licença ou autorização dos "
            "órgãos ambientais competentes, ou contrariando as normas "
            "legais e regulamentares pertinentes, sujeita o infrator a "
            "pena de detenção de um a seis meses, ou multa, ou ambas "
            "cumulativamente."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 60",
        "complexity": "simple",
        "category": "Crimes Poluição",
    },
    {
        "id": "CA_004",
        "question": (
            "Qual a pena prevista na Lei de Crimes Ambientais para quem "
            "mata, persegue ou caça espécime da fauna silvestre sem "
            "autorização?"
        ),
        "ground_truth": (
            "Conforme Art. 29 da Lei 9.605/1998, matar, perseguir, "
            "caçar, apanhar, utilizar espécimes da fauna silvestre, "
            "nativos ou em rota migratória, sem a devida permissão, "
            "licença ou autorização da autoridade competente, ou em "
            "desacordo com a obtida, sujeita o infrator a pena de "
            "detenção de seis meses a um ano, e multa."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 29",
        "complexity": "simple",
        "category": "Crimes Fauna",
    },

    # ── CA – medium (2) ─────────────────────────────────────────────────────
    {
        "id": "CA_005",
        "question": (
            "O que configura o crime de poluição qualificada na Lei de "
            "Crimes Ambientais e quais são as penas?"
        ),
        "ground_truth": (
            "Conforme Art. 54 da Lei 9.605/1998, causar poluição de "
            "qualquer natureza em níveis tais que resultem ou possam "
            "resultar em danos à saúde humana, ou que provoquem a "
            "mortandade de animais ou a destruição significativa da flora, "
            "sujeita o infrator a reclusão de um a quatro anos, e multa. "
            "O §2º estabelece formas qualificadas com pena de reclusão de "
            "um a cinco anos quando: (I) tornar área urbana ou rural "
            "imprópria para ocupação; (II) causar poluição atmosférica que "
            "provoque retirada de moradores; (III) causar poluição hídrica "
            "que torne necessária a interrupção do abastecimento; "
            "(IV) dificultar ou impedir o uso público de praias; "
            "(V) ocorrer lançamento de resíduos sólidos, líquidos ou "
            "gasosos em desacordo com as exigências legais."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 54",
        "complexity": "medium",
        "category": "Crimes Poluição",
    },
    {
        "id": "CA_006",
        "question": (
            "Qual a pena para quem falsifica ou altera dados em "
            "procedimentos administrativos ambientais, e quais condutas "
            "estão abrangidas?"
        ),
        "ground_truth": (
            "Conforme Art. 69-A da Lei 9.605/1998, elaborar ou "
            "apresentar, no licenciamento, concessão florestal ou "
            "qualquer outro procedimento administrativo, estudo, laudo "
            "ou relatório ambiental total ou parcialmente falso ou "
            "enganoso, inclusive por omissão, sujeita o infrator a "
            "reclusão de três a seis anos, e multa. O §1º prevê que, "
            "se o crime é culposo, a pena é de detenção de um a três "
            "anos. O §2º aumenta a pena de um terço a dois terços se "
            "há dano significativo ao meio ambiente em decorrência do "
            "uso da informação falsa."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 69-A",
        "complexity": "medium",
        "category": "Crimes Administrativos",
    },

    # ── CA – complex (2) ────────────────────────────────────────────────────
    {
        "id": "CA_007",
        "question": (
            "Compare as penas para crimes contra a flora em área de "
            "preservação permanente (Art. 38) e em unidade de conservação "
            "de proteção integral (Art. 40) da Lei de Crimes Ambientais, "
            "e explique como os conceitos de APP e UC se complementam."
        ),
        "ground_truth": (
            "O Art. 38 da Lei 9.605/1998 pune com detenção de 1 a 3 anos "
            "e/ou multa quem destrói floresta em APP. O Art. 40 pune "
            "com reclusão de 1 a 5 anos quem causa dano direto ou "
            "indireto a UC de Proteção Integral. A pena mais severa para "
            "UCs reflete o maior grau de proteção dessas áreas. As APPs "
            "(Art. 4º do Código Florestal, Lei 12.651/2012) e as UCs de "
            "Proteção Integral (Art. 8º do SNUC, Lei 9.985/2000) são "
            "instrumentos complementares: as APPs protegem recursos "
            "hídricos e relevo frágil de forma difusa em todo o território, "
            "enquanto as UCs delimitam áreas específicas para preservação "
            "integral da biodiversidade."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 38",
        "complexity": "complex",
        "category": "Crimes Flora",
    },
    {
        "id": "CA_008",
        "question": (
            "Um proprietário rural impede a regeneração natural de "
            "florestas e demais formas de vegetação nativa em sua "
            "propriedade. Qual crime ele comete, qual a pena, e como "
            "essa conduta se relaciona com a obrigação de recomposição "
            "da Reserva Legal no Código Florestal?"
        ),
        "ground_truth": (
            "Conforme Art. 48 da Lei 9.605/1998, impedir ou dificultar "
            "a regeneração natural de florestas e demais formas de "
            "vegetação sujeita o infrator a detenção de seis meses a um "
            "ano, e multa. Essa conduta agrava-se quando o proprietário "
            "tem obrigação legal de recompor a Reserva Legal: o Art. 66 "
            "da Lei 12.651/2012 (Código Florestal) prevê que a "
            "regularização pode ser feita por regeneração natural "
            "(inciso II). Ao impedir essa regeneração, o infrator "
            "comete simultaneamente o crime do Art. 48 e descumpre a "
            "obrigação de regularização do Código Florestal."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 48",
        "complexity": "complex",
        "category": "Crimes Flora",
    },

    # =========================================================================
    # CONAMA 357/2005 — Qualidade da Água — 6 perguntas
    # =========================================================================

    # ── C357 – simple (2) ───────────────────────────────────────────────────
    {
        "id": "C357_001",
        "question": (
            "Como a Resolução CONAMA 357/2005 define água doce, água "
            "salobra e água salina?"
        ),
        "ground_truth": (
            "Conforme Art. 2º da Resolução CONAMA 357/2005: água doce "
            "é aquela com salinidade igual ou inferior a 0,5‰ (inciso I); "
            "água salobra é aquela com salinidade superior a 0,5‰ e "
            "inferior a 30‰ (inciso II); e água salina é aquela com "
            "salinidade igual ou superior a 30‰ (inciso III)."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 2",
        "complexity": "simple",
        "category": "Qualidade Água",
    },
    {
        "id": "C357_002",
        "question": (
            "Quais são as classes de enquadramento de águas doces "
            "previstas na Resolução CONAMA 357/2005?"
        ),
        "ground_truth": (
            "Conforme Art. 4º da Resolução CONAMA 357/2005, as águas "
            "doces são classificadas em: Classe Especial (condições "
            "naturais, abastecimento sem tratamento, preservação do "
            "equilíbrio natural); Classe 1 (abastecimento com "
            "desinfecção, proteção de comunidades aquáticas, recreação "
            "de contato primário); Classe 2 (abastecimento com "
            "tratamento convencional, aquicultura, pesca); Classe 3 "
            "(abastecimento com tratamento convencional ou avançado, "
            "irrigação, pesca); e Classe 4 (navegação e harmonia "
            "paisagística)."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 4",
        "complexity": "simple",
        "category": "Qualidade Água",
    },

    # ── C357 – medium (2) ───────────────────────────────────────────────────
    {
        "id": "C357_003",
        "question": (
            "Quais são as condições e padrões de qualidade para águas "
            "doces de Classe 1 segundo a CONAMA 357/2005?"
        ),
        "ground_truth": (
            "Conforme Art. 5º (com referência aos Arts. 14 e 15) da "
            "Resolução CONAMA 357/2005, as águas doces de Classe 1 devem "
            "atender, entre outras condições: não verificação de efeito "
            "tóxico crônico a organismos; materiais flutuantes virtualmente "
            "ausentes; OD (oxigênio dissolvido) não inferior a 6 mg/L; "
            "DBO até 3 mg/L; turbidez até 40 UNT; pH entre 6,0 e 9,0; "
            "coliformes termotolerantes até 200 NMP/100 mL para "
            "balneabilidade; além de padrões específicos para substâncias "
            "inorgânicas e orgânicas."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 5",
        "complexity": "medium",
        "category": "Padrões Qualidade",
    },
    {
        "id": "C357_004",
        "question": (
            "Quais são as classes de enquadramento para águas salinas "
            "e quais os usos preponderantes de cada classe?"
        ),
        "ground_truth": (
            "Conforme Art. 10 da Resolução CONAMA 357/2005, as águas "
            "salinas são classificadas em: Classe Especial (preservação "
            "dos ambientes aquáticos em UCs de Proteção Integral); "
            "Classe 1 (recreação de contato primário, proteção de "
            "comunidades aquáticas, aquicultura e atividade de pesca); "
            "Classe 2 (pesca amadora, recreação de contato secundário); "
            "e Classe 3 (navegação e harmonia paisagística)."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 10",
        "complexity": "medium",
        "category": "Qualidade Água",
    },

    # ── C357 – complex (2) ──────────────────────────────────────────────────
    {
        "id": "C357_005",
        "question": (
            "Qual a relação entre a classificação dos corpos d'água "
            "da CONAMA 357/2005 e as condições de lançamento de "
            "efluentes da CONAMA 430/2011?"
        ),
        "ground_truth": (
            "A Resolução CONAMA 357/2005 estabelece, em seus Arts. 4º a "
            "13, a classificação dos corpos d'água em função dos usos "
            "preponderantes e define os padrões de qualidade para cada "
            "classe. O Art. 14 dessa resolução trata das condições de "
            "lançamento. A Resolução CONAMA 430/2011 complementa e "
            "atualiza essas condições, detalhando no Art. 5º as "
            "condições de lançamento direto de efluentes e no Art. 16 "
            "os padrões específicos. O princípio é que o lançamento de "
            "efluentes não pode comprometer os padrões de qualidade da "
            "classe do corpo receptor (CONAMA 357), e a zona de mistura "
            "(CONAMA 430, Art. 3º) define o trecho onde se permite a "
            "diluição do efluente."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 14",
        "complexity": "complex",
        "category": "Padrões Qualidade",
    },
    {
        "id": "C357_006",
        "question": (
            "Se um corpo d'água está enquadrado como Classe 2 e recebe "
            "efluentes tratados, quais padrões de qualidade devem ser "
            "mantidos e qual a responsabilidade do empreendedor em caso "
            "de desconformidade, considerando tanto a CONAMA 357 quanto "
            "a PNMA?"
        ),
        "ground_truth": (
            "Conforme Art. 4º da Resolução CONAMA 357/2005, o corpo "
            "d'água Classe 2 deve manter: OD não inferior a 5 mg/L, "
            "DBO até 5 mg/L, turbidez até 100 UNT, coliformes "
            "termotolerantes até 1.000 NMP/100 mL. O lançamento de "
            "efluentes deve observar as condições da CONAMA 430/2011 e "
            "não pode comprometer esses padrões. Em caso de "
            "desconformidade, o empreendedor responde objetivamente por "
            "danos ambientais conforme Art. 14, §1º da Lei 6.938/1981 "
            "(PNMA), independentemente de culpa, devendo indenizar ou "
            "reparar os danos."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 4",
        "complexity": "complex",
        "category": "Padrões Qualidade",
    },

    # =========================================================================
    # CONAMA 430/2011 — Lançamento de Efluentes — 5 perguntas
    # =========================================================================

    # ── C430 – simple (2) ───────────────────────────────────────────────────
    {
        "id": "C430_001",
        "question": (
            "O que a Resolução CONAMA 430/2011 define como corpo "
            "receptor e zona de mistura?"
        ),
        "ground_truth": (
            "Conforme Art. 3º da Resolução CONAMA 430/2011: corpo "
            "receptor é o corpo hídrico que recebe o lançamento de "
            "efluentes; zona de mistura é a região do corpo receptor "
            "onde ocorre a diluição inicial do efluente, definida pelo "
            "órgão ambiental competente, podendo ser dispensada sua "
            "caracterização quando não houver substâncias que "
            "ultrapassem os limites estabelecidos."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 3",
        "complexity": "simple",
        "category": "Efluentes",
    },
    {
        "id": "C430_002",
        "question": (
            "Quais são os principais padrões de lançamento de efluentes "
            "definidos no Art. 16 da CONAMA 430/2011?"
        ),
        "ground_truth": (
            "Conforme Art. 16 da Resolução CONAMA 430/2011, os efluentes "
            "de qualquer fonte poluidora somente poderão ser lançados "
            "diretamente no corpo receptor desde que obedeçam, entre "
            "outros, os seguintes padrões: pH entre 5 e 9; temperatura "
            "inferior a 40 °C; materiais sedimentáveis até 1 mL/L em "
            "teste de 1 hora em cone Imhoff; óleos e graxas minerais "
            "até 20 mg/L e óleos vegetais e gorduras animais até "
            "50 mg/L; ausência de materiais flutuantes; além de limites "
            "específicos para substâncias inorgânicas e orgânicas."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 16",
        "complexity": "simple",
        "category": "Padrões Efluentes",
    },

    # ── C430 – medium (2) ───────────────────────────────────────────────────
    {
        "id": "C430_003",
        "question": (
            "Quais são as condições gerais para lançamento direto de "
            "efluentes em corpos d'água receptores segundo a "
            "CONAMA 430/2011?"
        ),
        "ground_truth": (
            "Conforme Art. 5º da Resolução CONAMA 430/2011, os efluentes "
            "não poderão: conferir ao corpo receptor características em "
            "desacordo com as metas obrigatórias de enquadramento; "
            "causar ou possuir potencial para causar efeitos tóxicos "
            "aos organismos aquáticos no corpo receptor. Os lançamentos "
            "devem atender simultaneamente as condições e padrões de "
            "lançamento de efluentes (Arts. 16 e seguintes) e não "
            "ocasionar a ultrapassagem dos padrões de qualidade da "
            "classe do corpo receptor. O órgão ambiental pode exigir "
            "tecnologia de tratamento ambientalmente adequada."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 5",
        "complexity": "medium",
        "category": "Efluentes",
    },
    {
        "id": "C430_004",
        "question": (
            "Quais são os padrões específicos para lançamento de "
            "efluentes originários de sistemas de tratamento de "
            "esgotos sanitários?"
        ),
        "ground_truth": (
            "Conforme Art. 21 da Resolução CONAMA 430/2011, os efluentes "
            "originários de sistemas de tratamento de esgotos sanitários "
            "devem atender, além das condições gerais (Art. 16), os "
            "seguintes padrões específicos: pH entre 5 e 9; temperatura "
            "inferior a 40 °C; DBO máxima de 120 mg/L ou tratamento com "
            "eficiência mínima de 60% de remoção de DBO, sendo que o "
            "órgão ambiental pode fixar limites mais restritivos; "
            "sólidos sedimentáveis até 1 mL/L; e demais substâncias "
            "em conformidade com os padrões da resolução."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 21",
        "complexity": "medium",
        "category": "Esgotos Sanitários",
    },

    # ── C430 – complex (1) ──────────────────────────────────────────────────
    {
        "id": "C430_005",
        "question": (
            "Uma indústria pretende lançar efluentes em um rio "
            "enquadrado como Classe 2. Considerando a CONAMA 430/2011 "
            "e a CONAMA 357/2005, quais padrões deve observar "
            "simultaneamente e qual a consequência criminal de "
            "lançar sem licença?"
        ),
        "ground_truth": (
            "A indústria deve observar cumulativamente: (1) os padrões "
            "de lançamento de efluentes do Art. 16 da CONAMA 430/2011 "
            "(pH 5–9, temperatura < 40 °C, DBO, substâncias tóxicas); "
            "(2) as condições gerais do Art. 5º da CONAMA 430/2011, "
            "garantindo que o lançamento não comprometa os padrões de "
            "qualidade da Classe 2 (Art. 4º da CONAMA 357/2005: "
            "OD >= 5 mg/L, DBO <= 5 mg/L no corpo receptor); e "
            "(3) obter licenciamento ambiental conforme Art. 10 da "
            "Lei 6.938/1981 (PNMA). Caso lance efluentes sem licença, "
            "incorre no Art. 60 da Lei 9.605/1998, com detenção de um "
            "a seis meses e/ou multa. Se causar poluição com danos à "
            "saúde ou mortandade de animais, aplica-se o Art. 54 com "
            "reclusão de um a cinco anos."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 16",
        "complexity": "complex",
        "category": "Padrões Efluentes",
    },
]


# ---------------------------------------------------------------------------
# Validação interna — executar com:  python -m scripts.eval_dataset
# ---------------------------------------------------------------------------
def _validate_dataset() -> None:
    """Imprime a distribuição do dataset e valida as contagens."""
    from collections import Counter

    total = len(EVAL_DATASET_FULL)
    ids = [item["id"] for item in EVAL_DATASET_FULL]
    laws = Counter(item["expected_law"] for item in EVAL_DATASET_FULL)
    complexities = Counter(item["complexity"] for item in EVAL_DATASET_FULL)
    categories = Counter(item["category"] for item in EVAL_DATASET_FULL)

    errors: list[str] = []

    if total != 50:
        errors.append(f"Total: esperado 50, encontrado {total}")
    if len(ids) != len(set(ids)):
        dupes = [i for i in ids if ids.count(i) > 1]
        errors.append(f"IDs duplicados: {set(dupes)}")
    if complexities["simple"] != 20:
        errors.append(f"Simple: esperado 20, encontrado {complexities['simple']}")
    if complexities["medium"] != 18:
        errors.append(f"Medium: esperado 18, encontrado {complexities['medium']}")
    if complexities["complex"] != 12:
        errors.append(f"Complex: esperado 12, encontrado {complexities['complex']}")
    if laws["Código Florestal"] != 15:
        errors.append(f"CF: esperado 15, encontrado {laws['Código Florestal']}")
    if laws["PNMA"] != 8:
        errors.append(f"PNMA: esperado 8, encontrado {laws['PNMA']}")
    if laws["SNUC"] != 8:
        errors.append(f"SNUC: esperado 8, encontrado {laws['SNUC']}")
    if laws["Crimes Ambientais"] != 8:
        errors.append(f"CA: esperado 8, encontrado {laws['Crimes Ambientais']}")
    if laws["CONAMA 357"] != 6:
        errors.append(f"C357: esperado 6, encontrado {laws['CONAMA 357']}")
    if laws["CONAMA 430"] != 5:
        errors.append(f"C430: esperado 5, encontrado {laws['CONAMA 430']}")

    # Checar chaves obrigatórias em cada item
    required_keys = {
        "id", "question", "ground_truth", "expected_law",
        "expected_article", "complexity", "category",
    }
    for i, item in enumerate(EVAL_DATASET_FULL):
        missing = required_keys - item.keys()
        if missing:
            errors.append(f"Item {i} ({item.get('id', '?')}): faltam chaves {missing}")

    if errors:
        print("FALHA NA VALIDAÇÃO:")
        for e in errors:
            print(f"  - {e}")
        raise SystemExit(1)

    print("EVAL_DATASET_FULL validado com sucesso!")
    print(f"  Total: {total} perguntas")
    print(f"  Por legislação:   {dict(laws)}")
    print(f"  Por complexidade: {dict(complexities)}")
    print(f"  Categorias:       {dict(categories)}")
    print(f"  IDs únicos:       {len(set(ids))}")


if __name__ == "__main__":
    _validate_dataset()
