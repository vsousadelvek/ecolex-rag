"""Dataset completo de avaliacao para o sistema EcoLex RAG.

100 perguntas sobre legislacao ambiental brasileira, distribuidas por:
  - Codigo Florestal (Lei 12.651/2012): 30 perguntas  (CF_001-CF_030)
  - PNMA (Lei 6.938/1981): 16 perguntas                (PNMA_001-PNMA_016)
  - SNUC (Lei 9.985/2000): 16 perguntas                (SNUC_001-SNUC_016)
  - Crimes Ambientais (Lei 9.605/1998): 16 perguntas   (CA_001-CA_016)
  - CONAMA 357/2005: 12 perguntas                       (C357_001-C357_012)
  - CONAMA 430/2011: 10 perguntas                       (C430_001-C430_010)

Complexidade:
  - simple  (40): uma lei, um artigo, resposta direta
  - medium  (35): condicionais, artigo com paragrafos
  - complex (25): multi-hop, cruzamento entre leis, comparativas

Formato de cada entrada (compativel com scripts/evaluate.py):
  - id              : identificador unico (prefixo da lei + numero)
  - question        : pergunta em linguagem natural
  - ground_truth    : resposta de referencia com fundamentacao legal
  - expected_law    : nome da lei esperada nas fontes recuperadas
  - expected_article: artigo esperado (ex: "Art. 4")
  - complexity      : "simple" | "medium" | "complex"
  - category        : categoria tematica da pergunta

Usado pelos scripts evaluate.py e ablation.py.
"""

EVAL_DATASET_FULL: list[dict] = [
    # =========================================================================
    # CODIGO FLORESTAL (Lei 12.651/2012) -- 30 perguntas
    # =========================================================================

    # -- CF - simple (6 existentes) ------------------------------------------
    {
        "id": "CF_001",
        "question": (
            "Qual a largura minima da faixa de APP para cursos d'agua "
            "naturais com menos de 10 metros de largura?"
        ),
        "ground_truth": (
            "A faixa minima de Area de Preservacao Permanente para cursos "
            "d'agua naturais com largura inferior a 10 metros e de 30 metros, "
            "medida desde a borda da calha do leito regular, conforme o "
            "Art. 4o, inciso I, alinea 'a' da Lei 12.651/2012 "
            "(Codigo Florestal)."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 4",
        "complexity": "simple",
        "category": "APP",
    },
    {
        "id": "CF_002",
        "question": (
            "Qual o raio minimo de APP ao redor de nascentes e olhos "
            "d'agua perenes?"
        ),
        "ground_truth": (
            "As areas no entorno das nascentes e dos olhos d'agua perenes, "
            "qualquer que seja sua situacao topografica, devem ter raio "
            "minimo de 50 metros, conforme Art. 4o, inciso IV da "
            "Lei 12.651/2012."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 4",
        "complexity": "simple",
        "category": "APP",
    },
    {
        "id": "CF_003",
        "question": (
            "Qual o percentual minimo de Reserva Legal para imoveis rurais "
            "situados em area de floresta na Amazonia Legal?"
        ),
        "ground_truth": (
            "O percentual minimo de Reserva Legal e de 80% do imovel "
            "situado em area de florestas na Amazonia Legal, conforme "
            "Art. 12, inciso I, alinea 'a' da Lei 12.651/2012."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 12",
        "complexity": "simple",
        "category": "Reserva Legal",
    },
    {
        "id": "CF_004",
        "question": (
            "O que o Codigo Florestal define como Area de Preservacao "
            "Permanente (APP)?"
        ),
        "ground_truth": (
            "Conforme Art. 3o, inciso II da Lei 12.651/2012, Area de "
            "Preservacao Permanente e a area protegida, coberta ou nao por "
            "vegetacao nativa, com a funcao ambiental de preservar os "
            "recursos hidricos, a paisagem, a estabilidade geologica e a "
            "biodiversidade, facilitar o fluxo genico de fauna e flora, "
            "proteger o solo e assegurar o bem-estar das populacoes humanas."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 3",
        "complexity": "simple",
        "category": "APP",
    },
    {
        "id": "CF_005",
        "question": (
            "Qual o percentual minimo de Reserva Legal para imoveis "
            "localizados em area de cerrado dentro da Amazonia Legal?"
        ),
        "ground_truth": (
            "Para imoveis situados em area de cerrado na Amazonia Legal, "
            "o percentual minimo de Reserva Legal e de 35%, conforme "
            "Art. 12, inciso I, alinea 'b' da Lei 12.651/2012."
        ),
        "expected_law": "Codigo Florestal",
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
            "Para cursos d'agua com largura entre 50 e 200 metros, a faixa "
            "minima de APP e de 100 metros, conforme Art. 4o, inciso I, "
            "alinea 'c' da Lei 12.651/2012."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 4",
        "complexity": "simple",
        "category": "APP",
    },

    # -- CF - medium (5 existentes) ------------------------------------------
    {
        "id": "CF_007",
        "question": (
            "Em quais hipoteses o Codigo Florestal autoriza a supressao "
            "de vegetacao nativa em APP?"
        ),
        "ground_truth": (
            "A supressao de vegetacao nativa em APP somente podera ser "
            "autorizada em casos de utilidade publica, de interesse social "
            "ou de baixo impacto ambiental, conforme Art. 8o da "
            "Lei 12.651/2012. O par.1o desse artigo exige autorizacao do "
            "orgao ambiental estadual competente, com adocao de medidas "
            "mitigatorias e compensatorias."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 8",
        "complexity": "medium",
        "category": "APP",
    },
    {
        "id": "CF_008",
        "question": (
            "Em que condicoes a APP pode ser computada no calculo do "
            "percentual de Reserva Legal?"
        ),
        "ground_truth": (
            "Conforme Art. 15 da Lei 12.651/2012, e admitido o computo "
            "das APPs no calculo da Reserva Legal desde que: (I) o "
            "beneficio nao implique conversao de novas areas para uso "
            "alternativo do solo; (II) a area a ser computada esteja "
            "conservada ou em processo de recuperacao; e (III) o "
            "proprietario tenha requerido inclusao do imovel no Cadastro "
            "Ambiental Rural (CAR)."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 15",
        "complexity": "medium",
        "category": "Reserva Legal",
    },
    {
        "id": "CF_009",
        "question": (
            "Quais sao as opcoes para regularizacao de deficit de "
            "Reserva Legal previstas no Codigo Florestal?"
        ),
        "ground_truth": (
            "Conforme Art. 66 da Lei 12.651/2012, o proprietario que "
            "possuia, em 22 de julho de 2008, area de Reserva Legal "
            "inferior ao exigido pode regularizar mediante: (I) recomposicao "
            "da Reserva Legal; (II) regeneracao natural da vegetacao; ou "
            "(III) compensacao da Reserva Legal. A recomposicao pode ser "
            "feita com plantio intercalado de especies nativas e exoticas "
            "em sistema agroflorestal, sendo que as exoticas nao podem "
            "exceder 50% da area total."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 66",
        "complexity": "medium",
        "category": "Reserva Legal",
    },
    {
        "id": "CF_010",
        "question": (
            "Quais sao as regras para areas rurais consolidadas em APP "
            "de cursos d'agua segundo o Codigo Florestal?"
        ),
        "ground_truth": (
            "Conforme Art. 61-A da Lei 12.651/2012, nas APPs de cursos "
            "d'agua e autorizada a continuidade de atividades "
            "agrossilvipastoris, de ecoturismo e de turismo rural em areas "
            "rurais consolidadas ate 22 de julho de 2008. A extensao da "
            "faixa a ser recomposta varia conforme o tamanho do imovel "
            "em modulos fiscais: para imoveis de ate 1 modulo fiscal, "
            "a recomposicao e de 5 metros; de 1 a 2 modulos, 8 metros; "
            "de 2 a 4 modulos, 15 metros."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 61-A",
        "complexity": "medium",
        "category": "APP",
    },
    {
        "id": "CF_011",
        "question": (
            "O que preve o Codigo Florestal sobre o Programa de Apoio e "
            "Incentivo a Preservacao e Recuperacao do Meio Ambiente, "
            "incluindo pagamento por servicos ambientais?"
        ),
        "ground_truth": (
            "Conforme Art. 41 da Lei 12.651/2012, o Poder Executivo "
            "federal e autorizado a instituir programa de apoio e incentivo "
            "a conservacao, incluindo pagamento ou incentivo a servicos "
            "ambientais como retribuicao monetaria ou nao as atividades de "
            "conservacao e melhoria dos ecossistemas (inciso I). Tambem "
            "preve compensacao por medidas de conservacao ambiental e "
            "incentivos para comercializacao, inovacao e aceleracao de "
            "acoes de recuperacao (incisos II e III)."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 41",
        "complexity": "medium",
        "category": "Instrumentos Economicos",
    },

    # -- CF - complex (4 existentes) -----------------------------------------
    {
        "id": "CF_012",
        "question": (
            "Considere um imovel rural de 500 hectares na Amazonia Legal, "
            "localizado em area de floresta, com um rio de 80 metros de "
            "largura em sua divisa. Quais sao as exigencias cumulativas "
            "de APP e Reserva Legal, e quando a APP pode ser computada "
            "na Reserva Legal?"
        ),
        "ground_truth": (
            "O imovel deve manter: (1) APP de 100 metros nas faixas "
            "marginais do rio, conforme Art. 4o, I, 'c' da Lei 12.651/2012 "
            "(rios de 50 a 200 m de largura); e (2) Reserva Legal de 80% "
            "da area, conforme Art. 12, I, 'a'. A APP pode ser computada "
            "na Reserva Legal somente se atendidas as tres condicoes do "
            "Art. 15: nao implicar conversao de novas areas, a area estar "
            "conservada ou em recuperacao, e o imovel estar inscrito no CAR."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 4",
        "complexity": "complex",
        "category": "APP",
    },
    {
        "id": "CF_013",
        "question": (
            "Quais as diferencas entre os percentuais de Reserva Legal "
            "para diferentes fitofisionomias e regioes do Brasil, e quais "
            "os fundamentos legais de cada um?"
        ),
        "ground_truth": (
            "Conforme Art. 12 da Lei 12.651/2012, os percentuais de "
            "Reserva Legal sao: (I) na Amazonia Legal -- (a) 80% em area "
            "de florestas, (b) 35% em area de cerrado, (c) 20% em area "
            "de campos gerais; (II) nas demais regioes do pais -- 20% do "
            "imovel. A diferenciacao reflete a importancia ecologica e "
            "fragilidade dos biomas amazonicos."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 12",
        "complexity": "medium",
        "category": "Reserva Legal",
    },
    {
        "id": "CF_014",
        "question": (
            "A supressao de vegetacao para uso alternativo do solo requer "
            "quais procedimentos previos segundo o Codigo Florestal, e "
            "como isso se relaciona com o licenciamento ambiental da PNMA?"
        ),
        "ground_truth": (
            "Conforme Art. 26 da Lei 12.651/2012, a supressao de vegetacao "
            "nativa para uso alternativo do solo depende de autorizacao do "
            "orgao ambiental estadual competente, com indicacao pelo "
            "proprietario do uso alternativo e da localizacao da Reserva "
            "Legal. O Art. 9o e o Art. 10 da Lei 6.938/1981 (PNMA) "
            "complementam ao exigir licenciamento ambiental para atividades "
            "efetiva ou potencialmente poluidoras e a avaliacao de impactos "
            "ambientais como instrumento obrigatorio da politica ambiental."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 26",
        "complexity": "complex",
        "category": "Uso Alternativo do Solo",
    },
    {
        "id": "CF_015",
        "question": (
            "Compare as faixas de APP exigidas pelo Codigo Florestal para "
            "rios de diferentes larguras e explique como o conceito de "
            "'area rural consolidada' altera essas exigencias."
        ),
        "ground_truth": (
            "Conforme Art. 4o, I da Lei 12.651/2012, as faixas de APP "
            "variam: (a) 30 m para rios ate 10 m; (b) 50 m para rios de "
            "10 a 50 m; (c) 100 m para rios de 50 a 200 m; (d) 200 m "
            "para rios de 200 a 600 m; (e) 500 m para rios com mais de "
            "600 m. Porem, o Art. 61-A, que trata de areas rurais "
            "consolidadas ate 22 de julho de 2008, flexibiliza essas "
            "exigencias com faixas de recomposicao menores, proporcionais "
            "ao tamanho do imovel em modulos fiscais, variando de 5 a "
            "100 metros dependendo do caso."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 4",
        "complexity": "complex",
        "category": "APP",
    },

    # -- CF - NOVAS (CF_016 a CF_030) ----------------------------------------

    # CF_016 - simple - Art. 3 (area rural consolidada)
    {
        "id": "CF_016",
        "question": (
            "O que o Codigo Florestal define como 'area rural consolidada'?"
        ),
        "ground_truth": (
            "Conforme Art. 3o, inciso IV da Lei 12.651/2012, area rural "
            "consolidada e a area de imovel rural com ocupacao antropica "
            "preexistente a 22 de julho de 2008, com edificacoes, "
            "benfeitorias ou atividades agrossilvipastoris, admitida, "
            "neste ultimo caso, a adocao do regime de pousio."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 3",
        "complexity": "simple",
        "category": "Definicoes",
    },
    # CF_017 - simple - Art. 3 (pousio)
    {
        "id": "CF_017",
        "question": (
            "Como o Codigo Florestal define 'pousio' e qual o prazo "
            "maximo permitido?"
        ),
        "ground_truth": (
            "Conforme Art. 3o, inciso XXIV da Lei 12.651/2012, pousio e "
            "a pratica de interrupcao temporaria de atividades ou usos "
            "agricolas, pecuarios ou silviculturais, por no maximo 5 anos, "
            "para possibilitar a recuperacao da capacidade de uso ou da "
            "estrutura fisica do solo."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 3",
        "complexity": "simple",
        "category": "Definicoes",
    },
    # CF_018 - simple - Art. 3 (manejo sustentavel)
    {
        "id": "CF_018",
        "question": (
            "O que o Codigo Florestal define como 'manejo sustentavel'?"
        ),
        "ground_truth": (
            "Conforme Art. 3o, inciso VII da Lei 12.651/2012, manejo "
            "sustentavel e a administracao da vegetacao natural para a "
            "obtencao de beneficios economicos, sociais e ambientais, "
            "respeitando-se os mecanismos de sustentacao do ecossistema "
            "objeto do manejo e considerando-se, cumulativa ou "
            "alternativamente, a utilizacao de multiplas especies "
            "madeireiras ou nao, de multiplos produtos e subprodutos da "
            "flora, bem como a utilizacao de outros bens e servicos."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 3",
        "complexity": "simple",
        "category": "Definicoes",
    },
    # CF_019 - simple - Art. 9 (acesso a APP)
    {
        "id": "CF_019",
        "question": (
            "O Codigo Florestal permite o acesso de pessoas e animais "
            "as APPs para obtencao de agua?"
        ),
        "ground_truth": (
            "Conforme Art. 9o da Lei 12.651/2012, e permitido o acesso "
            "de pessoas e animais as Areas de Preservacao Permanente para "
            "obtencao de agua e para realizacao de atividades de baixo "
            "impacto ambiental."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 9",
        "complexity": "simple",
        "category": "APP",
    },
    # CF_020 - simple - Art. 29 (registro no CAR)
    {
        "id": "CF_020",
        "question": (
            "O que e o Cadastro Ambiental Rural (CAR) e qual a obrigacao "
            "de inscricao segundo o Codigo Florestal?"
        ),
        "ground_truth": (
            "Conforme Art. 29 da Lei 12.651/2012, e criado o Cadastro "
            "Ambiental Rural (CAR), no ambito do Sistema Nacional de "
            "Informacao sobre Meio Ambiente (SINIMA), registro publico "
            "eletronico de ambito nacional, obrigatorio para todos os "
            "imoveis rurais, com a finalidade de integrar as informacoes "
            "ambientais das propriedades e posses rurais, compondo base "
            "de dados para controle, monitoramento, planejamento ambiental "
            "e economico e combate ao desmatamento."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 29",
        "complexity": "simple",
        "category": "CAR",
    },
    # CF_021 - medium - Art. 5 (APP em areas urbanas)
    {
        "id": "CF_021",
        "question": (
            "O Codigo Florestal preve a possibilidade de delimitacao de "
            "APPs em areas urbanas? Quais as condicoes?"
        ),
        "ground_truth": (
            "Conforme Art. 5o da Lei 12.651/2012, na implantacao de "
            "reservatorio d'agua artificial destinado a geracao de energia "
            "ou abastecimento publico, e obrigatoria a aquisicao, "
            "desapropriacao ou instituicao de servidao administrativa "
            "pelo empreendedor das Areas de Preservacao Permanente criadas "
            "em seu entorno, conforme estabelecido no licenciamento "
            "ambiental, observando-se a faixa minima de 30 metros e "
            "maxima de 100 metros em area rural, e a faixa minima de "
            "15 metros e maxima de 30 metros em area urbana."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 5",
        "complexity": "medium",
        "category": "APP",
    },
    # CF_022 - medium - Art. 6 (reservatorios artificiais)
    {
        "id": "CF_022",
        "question": (
            "Quais as regras para APP no entorno de reservatorios "
            "artificiais de agua que nao decorram de barramento de "
            "cursos d'agua naturais?"
        ),
        "ground_truth": (
            "Conforme Art. 4o, par.1o da Lei 12.651/2012, nao sera "
            "exigida Area de Preservacao Permanente no entorno de "
            "reservatorios artificiais de agua que nao decorram de "
            "barramento ou represamento de cursos d'agua naturais. "
            "Ja o Art. 6o estabelece que o Chefe do Poder Executivo "
            "podera, para fins de preservacao, declarar de interesse "
            "social areas cobertas com florestas ou outras formas de "
            "vegetacao como APP quando destinadas a conter a erosao do "
            "solo e mitigar riscos de enchentes e deslizamentos de terra."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 6",
        "complexity": "medium",
        "category": "APP",
    },
    # CF_023 - medium - Art. 7 (regime de protecao)
    {
        "id": "CF_023",
        "question": (
            "Qual o regime de protecao das APPs e qual a obrigacao do "
            "proprietario em caso de supressao irregular da vegetacao?"
        ),
        "ground_truth": (
            "Conforme Art. 7o da Lei 12.651/2012, a vegetacao situada "
            "em Area de Preservacao Permanente devera ser mantida pelo "
            "proprietario da area, possuidor ou ocupante a qualquer "
            "titulo, pessoa fisica ou juridica, de direito publico ou "
            "privado. O par.1o determina que, tendo ocorrido supressao "
            "de vegetacao situada em APP, o proprietario e obrigado a "
            "promover a recomposicao da vegetacao, ressalvados os usos "
            "autorizados nesta Lei. O par.2o estabelece que a obrigacao "
            "de recomposicao tem natureza real e e transmitida ao "
            "sucessor no caso de transferencia de dominio ou posse."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 7",
        "complexity": "medium",
        "category": "APP",
    },
    # CF_024 - medium - Art. 17 (conservacao na RL)
    {
        "id": "CF_024",
        "question": (
            "Quais sao as obrigacoes do proprietario quanto a conservacao "
            "da vegetacao na area de Reserva Legal?"
        ),
        "ground_truth": (
            "Conforme Art. 17 da Lei 12.651/2012, a Reserva Legal deve "
            "ser conservada com cobertura de vegetacao nativa pelo "
            "proprietario do imovel rural, possuidor ou ocupante a qualquer "
            "titulo, pessoa fisica ou juridica, de direito publico ou "
            "privado. O par.1o admite a exploracao economica da Reserva "
            "Legal mediante manejo sustentavel, previamente aprovado pelo "
            "orgao competente do SISNAMA. O par.3o veda o corte raso da "
            "vegetacao na Reserva Legal e obriga a recomposicao em caso "
            "de supressao irregular apos julho de 2008."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 17",
        "complexity": "medium",
        "category": "Reserva Legal",
    },
    # CF_025 - medium - Art. 18 (localizacao da RL)
    {
        "id": "CF_025",
        "question": (
            "Quais criterios o orgao ambiental deve observar para aprovar "
            "a localizacao da Reserva Legal no imovel rural?"
        ),
        "ground_truth": (
            "Conforme Art. 18 da Lei 12.651/2012, a area de Reserva "
            "Legal devera ser registrada no orgao ambiental competente "
            "por meio de inscricao no CAR. O par.2o estabelece que o "
            "orgao ambiental estadual devera aprovar a localizacao da "
            "Reserva Legal apos inclusao do imovel no CAR, considerando: "
            "(I) o plano de bacia hidrografica; (II) o Zoneamento "
            "Ecologico-Economico; (III) a formacao de corredores "
            "ecologicos com outra Reserva Legal, com APP, com UC ou "
            "com outra area legalmente protegida; e (IV) as areas de "
            "maior importancia para a conservacao da biodiversidade e "
            "de maior fragilidade ambiental."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 18",
        "complexity": "medium",
        "category": "Reserva Legal",
    },
    # CF_026 - medium - Art. 31 (areas de inclinacao 25-45 graus)
    {
        "id": "CF_026",
        "question": (
            "Qual a protecao conferida pelo Codigo Florestal para areas "
            "com inclinacao entre 25 e 45 graus?"
        ),
        "ground_truth": (
            "Conforme Art. 11 da Lei 12.651/2012, em areas de inclinacao "
            "entre 25 e 45 graus, serao permitidos o manejo florestal "
            "sustentavel e o exercicio de atividades agrossilvipastoris, "
            "bem como a manutencao da infraestrutura fisica associada ao "
            "desenvolvimento das atividades, observadas boas praticas "
            "agronomicas, sendo vedada a conversao de novas areas, "
            "excetuadas as hipoteses de utilidade publica e interesse "
            "social. O Art. 31 complementa ao afirmar que a protecao "
            "dessas areas e de aplicacao imediata."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 11",
        "complexity": "simple",
        "category": "APP",
    },
    # CF_027 - complex - Art. 13 (manguezais) + Art. 11 (topos de morro)
    {
        "id": "CF_027",
        "question": (
            "Compare a protecao conferida pelo Codigo Florestal aos "
            "manguezais e aos topos de morro como APPs: quais os "
            "criterios de cada um e em que se diferenciam?"
        ),
        "ground_truth": (
            "Os manguezais sao protegidos em toda a sua extensao como APP "
            "pelo Art. 4o, inciso VII da Lei 12.651/2012. O Art. 8o, "
            "par.2o permite obras de infraestrutura em manguezais para "
            "viabilizar a atividade pesqueira, se de interesse social. "
            "Ja os topos de morro sao protegidos pelo Art. 4o, inciso IX, "
            "que considera APP as areas no topo de morros, montes, "
            "montanhas e serras, com altura minima de 100 metros e "
            "inclinacao media maior que 25 graus, nas areas delimitadas "
            "a partir da curva de nivel correspondente a 2/3 da altura "
            "minima da elevacao. A diferenca fundamental e que os "
            "manguezais sao protegidos integralmente por sua importancia "
            "ecologica costeira, enquanto os topos de morro dependem "
            "de criterios geometricos de altitude e inclinacao."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 4",
        "complexity": "complex",
        "category": "APP",
    },
    # CF_028 - complex - Art. 14 (uso restrito) + Art. 35 (conducao)
    {
        "id": "CF_028",
        "question": (
            "O Codigo Florestal preve areas de uso restrito? Quais sao "
            "e qual a relacao com a conducao de especies nativas nas "
            "areas de Reserva Legal?"
        ),
        "ground_truth": (
            "Conforme Art. 10 da Lei 12.651/2012, nos pantanais e "
            "planicies pantaneiras e permitida a exploracao ecologicamente "
            "sustentavel, devendo-se considerar as recomendacoes tecnicas "
            "dos orgaos oficiais de pesquisa. O Art. 11 define areas "
            "entre 25 e 45 graus como de uso restrito. Quanto a conducao "
            "de especies nativas, o Art. 35 estabelece que o manejo "
            "florestal sustentavel da vegetacao da Reserva Legal com "
            "proposito comercial depende de autorizacao do orgao "
            "competente e deve observar: (I) nao descaracterizar a "
            "cobertura vegetal e nao prejudicar a conservacao da "
            "vegetacao nativa; e (II) assegurar a manutencao da "
            "diversidade das especies. A conducao de especies nativas "
            "regenerantes pode ser combinada com uso restrito em "
            "pantanais desde que respeitada a aptidao ecologica da area."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 10",
        "complexity": "complex",
        "category": "Uso Restrito",
    },
    # CF_029 - complex - Art. 44 (CRA)
    {
        "id": "CF_029",
        "question": (
            "O que e a Cota de Reserva Ambiental (CRA), como e instituida "
            "e em que situacoes pode ser utilizada para compensacao de "
            "Reserva Legal?"
        ),
        "ground_truth": (
            "Conforme Art. 44 da Lei 12.651/2012, e instituida a Cota "
            "de Reserva Ambiental (CRA), titulo nominativo representativo "
            "de area com vegetacao nativa, existente ou em processo de "
            "recuperacao. A CRA pode ser emitida mediante: (I) requerimento "
            "do proprietario de imovel inserido no CAR, nos termos do "
            "Art. 29; (II) area equivalente a Reserva Legal instituida "
            "voluntariamente sobre a vegetacao que exceder os percentuais "
            "exigidos pelo Art. 12; (III) area protegida na forma de "
            "RPPN; ou (IV) area existente ou em processo de recuperacao "
            "sob servidao ambiental. A CRA pode ser utilizada para "
            "compensar Reserva Legal de outro imovel conforme Art. 66, "
            "par.5o, desde que ambas as areas estejam no mesmo bioma."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 44",
        "complexity": "complex",
        "category": "Instrumentos Economicos",
    },
    # CF_030 - complex - Art. 78-A (PRA)
    {
        "id": "CF_030",
        "question": (
            "O que e o Programa de Regularizacao Ambiental (PRA) previsto "
            "no Codigo Florestal, quais suas condicoes e qual a relacao "
            "com a suspensao de sancoes por desmatamento irregular?"
        ),
        "ground_truth": (
            "Conforme Art. 59 da Lei 12.651/2012, a Uniao, os Estados "
            "e o Distrito Federal deverao implantar Programas de "
            "Regularizacao Ambiental (PRA) que permitam aos proprietarios "
            "ou possuidores de imoveis rurais a adequacao as normas do "
            "Codigo Florestal. O Art. 78-A estabelece que, apos a "
            "publicacao desta Lei e ate o termino do prazo de adesao ao "
            "PRA, as autuacoes e sancoes por infracoess cometidas antes "
            "de 22 de julho de 2008, relativas a supressao irregular de "
            "vegetacao em APP, Reserva Legal e uso restrito, ficam "
            "suspensas. A adesao ao PRA e a regularizacao efetiva "
            "convertem as multas em servicos de preservacao, melhoria "
            "e recuperacao da qualidade do meio ambiente, vinculando o "
            "proprietario ao cumprimento do termo de compromisso."
        ),
        "expected_law": "Codigo Florestal",
        "expected_article": "Art. 59",
        "complexity": "complex",
        "category": "Regularizacao Ambiental",
    },

    # =========================================================================
    # PNMA -- Politica Nacional do Meio Ambiente (Lei 6.938/1981) -- 16
    # =========================================================================

    # -- PNMA - simple (3 existentes) ----------------------------------------
    {
        "id": "PNMA_001",
        "question": (
            "Qual e o objetivo da Politica Nacional do Meio Ambiente?"
        ),
        "ground_truth": (
            "Conforme Art. 2o da Lei 6.938/1981, a Politica Nacional do "
            "Meio Ambiente tem por objetivo a preservacao, melhoria e "
            "recuperacao da qualidade ambiental propicia a vida, visando "
            "assegurar condicoes ao desenvolvimento socioeconomico, aos "
            "interesses da seguranca nacional e a protecao da dignidade "
            "da vida humana."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 2",
        "complexity": "simple",
        "category": "Principios",
    },
    {
        "id": "PNMA_002",
        "question": "Como a Lei 6.938/1981 define 'meio ambiente'?",
        "ground_truth": (
            "Conforme Art. 3o, inciso I da Lei 6.938/1981, meio ambiente "
            "e o conjunto de condicoes, leis, influencias e interacoes de "
            "ordem fisica, quimica e biologica, que permite, abriga e rege "
            "a vida em todas as suas formas."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 3",
        "complexity": "simple",
        "category": "Definicoes",
    },
    {
        "id": "PNMA_003",
        "question": "Qual a composicao e funcao do CONAMA no SISNAMA?",
        "ground_truth": (
            "Conforme Art. 6o, inciso II da Lei 6.938/1981, o CONAMA "
            "(Conselho Nacional do Meio Ambiente) e o orgao consultivo e "
            "deliberativo do SISNAMA, com a finalidade de assessorar, "
            "estudar e propor ao Conselho de Governo diretrizes de "
            "politicas governamentais para o meio ambiente e os recursos "
            "naturais, e deliberar sobre normas e padroes compativeis com "
            "o meio ambiente ecologicamente equilibrado."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 6",
        "complexity": "simple",
        "category": "SISNAMA",
    },

    # -- PNMA - medium (3 existentes) ----------------------------------------
    {
        "id": "PNMA_004",
        "question": (
            "Quais sao os instrumentos da Politica Nacional do Meio "
            "Ambiente listados na Lei 6.938/1981?"
        ),
        "ground_truth": (
            "Conforme Art. 9o da Lei 6.938/1981, os instrumentos incluem: "
            "(I) estabelecimento de padroes de qualidade ambiental; "
            "(II) zoneamento ambiental; (III) avaliacao de impactos "
            "ambientais; (IV) licenciamento e revisao de atividades "
            "efetiva ou potencialmente poluidoras; (V) incentivos a "
            "producao e instalacao de equipamentos para melhoria da "
            "qualidade ambiental; (VI) criacao de espacos territoriais "
            "protegidos; (VII) sistema nacional de informacoes sobre o "
            "meio ambiente; (VIII) Cadastro Tecnico Federal de Atividades "
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
            "Quais orgaos compoem a estrutura do SISNAMA e qual a funcao "
            "de cada nivel?"
        ),
        "ground_truth": (
            "Conforme Art. 6o da Lei 6.938/1981, o SISNAMA e composto por: "
            "(I) orgao superior -- Conselho de Governo, com funcao de "
            "assessorar o Presidente na formulacao da politica ambiental; "
            "(II) orgao consultivo e deliberativo -- CONAMA; "
            "(III) orgao central -- Ministerio do Meio Ambiente; "
            "(IV) orgao executor -- IBAMA; "
            "(V) orgaos seccionais -- orgaos ou entidades estaduais; "
            "(VI) orgaos locais -- orgaos ou entidades municipais."
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
            "estabelecido pela PNMA e qual a obrigacao do poluidor?"
        ),
        "ground_truth": (
            "Conforme Art. 14, par.1o da Lei 6.938/1981, o poluidor e "
            "obrigado, independentemente da existencia de culpa, a "
            "indenizar ou reparar os danos causados ao meio ambiente e a "
            "terceiros afetados por sua atividade. O Ministerio Publico "
            "da Uniao e dos Estados tera legitimidade para propor acao de "
            "responsabilidade civil e criminal por danos ao meio ambiente. "
            "Trata-se de responsabilidade civil objetiva."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 14",
        "complexity": "medium",
        "category": "Responsabilidade Civil",
    },

    # -- PNMA - complex (2 existentes) --------------------------------------
    {
        "id": "PNMA_007",
        "question": (
            "Como o licenciamento ambiental previsto na PNMA se relaciona "
            "com a exigencia de EIA/RIMA e quais sao as etapas do "
            "processo de licenciamento?"
        ),
        "ground_truth": (
            "O Art. 9o, incisos III e IV da Lei 6.938/1981 estabelece a "
            "avaliacao de impactos ambientais e o licenciamento como "
            "instrumentos da PNMA. O Art. 10 determina que atividades "
            "utilizadoras de recursos ambientais, efetiva ou potencialmente "
            "poluidoras, dependem de previo licenciamento do orgao "
            "ambiental competente. O licenciamento compreende tres etapas: "
            "Licenca Previa (LP), Licenca de Instalacao (LI) e Licenca de "
            "Operacao (LO). O EIA/RIMA e exigido quando a atividade for "
            "potencialmente causadora de significativa degradacao ambiental, "
            "servindo de base tecnica para a concessao da LP."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 10",
        "complexity": "complex",
        "category": "Licenciamento",
    },
    {
        "id": "PNMA_008",
        "question": (
            "Compare as definicoes de 'degradacao ambiental', 'poluicao' "
            "e 'recursos ambientais' na PNMA e explique como essas "
            "definicoes fundamentam a responsabilidade objetiva do poluidor."
        ),
        "ground_truth": (
            "O Art. 3o da Lei 6.938/1981 define: (II) degradacao da "
            "qualidade ambiental como a alteracao adversa das "
            "caracteristicas do meio ambiente; (III) poluicao como a "
            "degradacao que resulte de atividades que prejudiquem a saude, "
            "seguranca e bem-estar da populacao, criem condicoes adversas "
            "as atividades sociais e economicas, afetem a biota ou lancem "
            "materia ou energia em desacordo com padroes; (V) recursos "
            "ambientais como a atmosfera, aguas, solo, subsolo, fauna e "
            "flora. A amplitude dessas definicoes fundamenta o Art. 14, "
            "par.1o, que institui a responsabilidade civil objetiva: basta "
            "comprovar o dano e o nexo causal com a atividade, sem "
            "necessidade de demonstrar culpa."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 3",
        "complexity": "complex",
        "category": "Definicoes",
    },

    # -- PNMA - NOVAS (PNMA_009 a PNMA_016) ---------------------------------

    # PNMA_009 - simple - Art. 4 (acao governamental)
    {
        "id": "PNMA_009",
        "question": (
            "Quais sao os objetivos da acao governamental para manutencao "
            "do equilibrio ecologico previstos na PNMA?"
        ),
        "ground_truth": (
            "Conforme Art. 4o da Lei 6.938/1981, a Politica Nacional do "
            "Meio Ambiente visara: (I) a compatibilizacao do "
            "desenvolvimento economico-social com a preservacao da "
            "qualidade do meio ambiente e do equilibrio ecologico; "
            "(II) a definicao de areas prioritarias de acao governamental "
            "relativa a qualidade e ao equilibrio ecologico; "
            "(III) ao estabelecimento de criterios e padroes de qualidade "
            "ambiental e de normas relativas ao uso e manejo de recursos "
            "ambientais; (IV) ao desenvolvimento de pesquisas e "
            "tecnologias orientadas para o uso racional de recursos "
            "ambientais; entre outros objetivos."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 4",
        "complexity": "simple",
        "category": "Principios",
    },
    # PNMA_010 - simple - Art. 5 (diretrizes)
    {
        "id": "PNMA_010",
        "question": (
            "Quais sao as diretrizes da Politica Nacional do Meio Ambiente?"
        ),
        "ground_truth": (
            "Conforme Art. 5o da Lei 6.938/1981, as diretrizes da PNMA "
            "serao formuladas em normas e planos, destinados a orientar "
            "a acao dos Governos da Uniao, dos Estados, do Distrito "
            "Federal, dos Territorios e dos Municipios no que se "
            "relaciona com a preservacao da qualidade ambiental e "
            "manutencao do equilibrio ecologico, observados os "
            "principios estabelecidos no Art. 2o desta Lei."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 5",
        "complexity": "simple",
        "category": "Diretrizes",
    },
    # PNMA_011 - simple - Art. 8 (competencias do CONAMA)
    {
        "id": "PNMA_011",
        "question": (
            "Quais sao as competencias do CONAMA previstas na PNMA?"
        ),
        "ground_truth": (
            "Conforme Art. 8o da Lei 6.938/1981, compete ao CONAMA: "
            "(I) estabelecer normas e criterios para o licenciamento de "
            "atividades efetiva ou potencialmente poluidoras; "
            "(II) determinar a realizacao de estudos das alternativas e "
            "das possiveis consequencias ambientais de projetos publicos "
            "ou privados; (III) decidir, como ultima instancia "
            "administrativa, sobre multas e outras penalidades impostas "
            "pelo IBAMA; (IV) homologar acordos visando a transformacao "
            "de penalidades pecuniarias em obrigacao de executar medidas "
            "de interesse para a protecao ambiental; (V) determinar a "
            "perda ou restricao de beneficios fiscais concedidos pelo "
            "Poder Publico; (VI) estabelecer normas e padroes nacionais "
            "de controle da poluicao; (VII) estabelecer normas, criterios "
            "e padroes relativos ao controle e a manutencao da qualidade "
            "do meio ambiente."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 8",
        "complexity": "simple",
        "category": "SISNAMA",
    },
    # PNMA_012 - medium - Art. 10 par.1 (IBAMA licenciamento supletivo)
    {
        "id": "PNMA_012",
        "question": (
            "Em quais situacoes o IBAMA pode atuar supletivamente no "
            "licenciamento ambiental?"
        ),
        "ground_truth": (
            "Conforme Art. 10, par.1o da Lei 6.938/1981 (com a redacao "
            "dada pela Lei Complementar 140/2011), compete ao IBAMA o "
            "licenciamento de atividades e empreendimentos: (I) localizados "
            "ou desenvolvidos conjuntamente no Brasil e em pais limitrofe; "
            "(II) localizados ou desenvolvidos no mar territorial, "
            "plataforma continental ou zona economica exclusiva; "
            "(III) localizados ou desenvolvidos em terras indigenas; "
            "(IV) localizados ou desenvolvidos em unidades de conservacao "
            "instituidas pela Uniao; (V) de carater militar; "
            "(VI) destinados a pesquisar, lavrar, produzir, beneficiar, "
            "transportar, armazenar e dispor material radioativo. "
            "Alem disso, o IBAMA pode atuar supletivamente quando o "
            "orgao estadual for inepto ou omisso."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 10",
        "complexity": "medium",
        "category": "Licenciamento",
    },
    # PNMA_013 - medium - Art. 11 (penalidades)
    {
        "id": "PNMA_013",
        "question": (
            "Quais sao as penalidades administrativas previstas na PNMA "
            "para infracoes ambientais?"
        ),
        "ground_truth": (
            "Conforme Art. 14 da Lei 6.938/1981, as penalidades "
            "administrativas para infracoes ambientais incluem: (I) multa "
            "simples ou diaria; (II) perda ou restricao de incentivos e "
            "beneficios fiscais concedidos pelo Poder Publico; "
            "(III) perda ou suspensao de participacao em linhas de "
            "financiamento em estabelecimentos oficiais de credito; e "
            "(IV) suspensao de sua atividade. Essas sancoes sao aplicadas "
            "sem prejuizo das penalidades previstas na legislacao federal, "
            "estadual e municipal e independem da obrigacao de reparar "
            "os danos causados."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 14",
        "complexity": "medium",
        "category": "Sancoes",
    },
    # PNMA_014 - medium - Art. 12 (responsabilidade do agente financiador)
    {
        "id": "PNMA_014",
        "question": (
            "Qual a obrigacao das entidades e orgaos de financiamento "
            "e incentivos governamentais em relacao ao meio ambiente "
            "segundo a PNMA?"
        ),
        "ground_truth": (
            "Conforme Art. 12 da Lei 6.938/1981, as entidades e orgaos "
            "de financiamento e incentivos governamentais condicionarao "
            "a aprovacao de projetos habilitados a esses beneficios ao "
            "licenciamento e ao cumprimento das normas, dos criterios "
            "e dos padroes expedidos pelo CONAMA. O paragrafo unico "
            "estabelece que as entidades bancarias e os estabelecimentos "
            "oficiais de credito devem fazer constar dos projetos a "
            "realizacao de obras e aquisicao de equipamentos destinados "
            "ao controle de degradacao ambiental e a melhoria da "
            "qualidade do meio ambiente."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 12",
        "complexity": "medium",
        "category": "Instrumentos",
    },
    # PNMA_015 - complex - Art. 7 + Art. 13 (inclusao no PNMA e poder de policia)
    {
        "id": "PNMA_015",
        "question": (
            "Como a PNMA estrutura o poder de policia ambiental e de "
            "que forma as atividades empresariais sao incluidas no "
            "controle da Politica Nacional?"
        ),
        "ground_truth": (
            "O Art. 7o da Lei 6.938/1981 (revogado e absorvido por "
            "legislacao posterior) previa a inclusao no PNMA de atividades "
            "empresariais de ambito nacional. O Art. 13 determina que o "
            "Poder Executivo incentivara as atividades voltadas ao meio "
            "ambiente, e que os orgaos, entidades e programas do Poder "
            "Publico, destinados ao incentivo de pesquisas cientificas "
            "e tecnologicas, considererao, entre suas metas prioritarias, "
            "o desenvolvimento de pesquisas voltadas a utilizacao racional "
            "e a protecao dos recursos ambientais. Em termos de poder de "
            "policia, o Art. 14 e o Art. 10 conferem aos orgaos do "
            "SISNAMA a competencia fiscalizatoria sobre atividades "
            "potencialmente poluidoras, incluindo a aplicacao de sancoes "
            "administrativas e a exigencia de licenciamento previo."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 13",
        "complexity": "complex",
        "category": "Poder de Policia",
    },
    # PNMA_016 - complex - Art. 4 + Art. 9 + Art. 14
    {
        "id": "PNMA_016",
        "question": (
            "De que forma os objetivos (Art. 4), os instrumentos (Art. 9) "
            "e as sancoes (Art. 14) da PNMA se articulam para formar "
            "um sistema coerente de protecao ambiental?"
        ),
        "ground_truth": (
            "O Art. 4o da Lei 6.938/1981 estabelece os objetivos da "
            "PNMA, como a compatibilizacao do desenvolvimento com a "
            "preservacao e a imposicao ao poluidor da obrigacao de "
            "recuperar danos (inciso VII). O Art. 9o concretiza esses "
            "objetivos por meio de instrumentos como zoneamento ambiental, "
            "avaliacao de impactos, licenciamento, padroes de qualidade "
            "e Cadastro Tecnico Federal. O Art. 14 fecha o ciclo "
            "estabelecendo sancoes para quem descumpre as normas: multa, "
            "perda de incentivos fiscais, suspensao de financiamento "
            "e suspensao de atividade, alem da responsabilidade civil "
            "objetiva (par.1o). Essa estrutura de objetivos-instrumentos-"
            "sancoes garante que a legislacao nao seja meramente "
            "declaratoria, pois dispoe de ferramentas de controle previo "
            "(licenciamento, EIA) e repressivo (multas, responsabilidade "
            "civil) para assegurar a efetividade da protecao ambiental."
        ),
        "expected_law": "PNMA",
        "expected_article": "Art. 4",
        "complexity": "complex",
        "category": "Principios",
    },

    # =========================================================================
    # SNUC -- Sistema Nacional de Unidades de Conservacao (Lei 9.985/2000) -- 16
    # =========================================================================

    # -- SNUC - simple (3 existentes) ----------------------------------------
    {
        "id": "SNUC_001",
        "question": (
            "Quais sao os dois grupos de unidades de conservacao previstos "
            "no SNUC?"
        ),
        "ground_truth": (
            "Conforme Art. 7o da Lei 9.985/2000, as unidades de conservacao "
            "dividem-se em dois grupos: (I) Unidades de Protecao Integral, "
            "cujo objetivo basico e preservar a natureza, admitido apenas "
            "o uso indireto dos recursos naturais (par.1o); e (II) Unidades "
            "de Uso Sustentavel, cujo objetivo e compatibilizar a "
            "conservacao da natureza com o uso sustentavel de parcela dos "
            "seus recursos naturais (par.2o)."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 7",
        "complexity": "simple",
        "category": "UC",
    },
    {
        "id": "SNUC_002",
        "question": (
            "O que e o plano de manejo de uma unidade de conservacao e "
            "quando deve ser elaborado?"
        ),
        "ground_truth": (
            "Conforme Art. 2o, inciso XVII da Lei 9.985/2000, plano de "
            "manejo e o documento tecnico que estabelece o zoneamento e "
            "as normas de uso da area e manejo dos recursos naturais da "
            "UC. O Art. 27 determina que as UCs devem dispor de plano de "
            "manejo, que deve ser elaborado no prazo de cinco anos a "
            "partir da data de criacao da unidade."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 27",
        "complexity": "simple",
        "category": "Plano de Manejo",
    },
    {
        "id": "SNUC_003",
        "question": (
            "O que e uma zona de amortecimento de unidade de conservacao?"
        ),
        "ground_truth": (
            "Conforme Art. 2o, inciso XVIII da Lei 9.985/2000, zona de "
            "amortecimento e o entorno de uma unidade de conservacao onde "
            "as atividades humanas estao sujeitas a normas e restricoes "
            "especificas, com o proposito de minimizar os impactos "
            "negativos sobre a unidade. O Art. 25 estabelece que as UCs, "
            "exceto APAs e RPPNs, devem possuir uma zona de amortecimento."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 25",
        "complexity": "simple",
        "category": "Zona de Amortecimento",
    },

    # -- SNUC - medium (3 existentes) ----------------------------------------
    {
        "id": "SNUC_004",
        "question": (
            "Quais sao as categorias de unidades de conservacao de "
            "Protecao Integral previstas no SNUC?"
        ),
        "ground_truth": (
            "Conforme Art. 8o da Lei 9.985/2000, o grupo das Unidades de "
            "Protecao Integral e composto por: (I) Estacao Ecologica "
            "(Art. 9o); (II) Reserva Biologica (Art. 10); (III) Parque "
            "Nacional (Art. 11); (IV) Monumento Natural (Art. 12); e "
            "(V) Refugio de Vida Silvestre (Art. 13). Todas tem como "
            "objetivo a preservacao da natureza, admitindo apenas uso "
            "indireto dos recursos, com excecao do Monumento Natural e "
            "do Refugio de Vida Silvestre, que podem ser constituidos em "
            "areas particulares."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 8",
        "complexity": "medium",
        "category": "UC Protecao Integral",
    },
    {
        "id": "SNUC_005",
        "question": (
            "Quais sao as categorias de unidades de conservacao de Uso "
            "Sustentavel previstas no SNUC?"
        ),
        "ground_truth": (
            "Conforme Art. 14 da Lei 9.985/2000, o grupo das Unidades de "
            "Uso Sustentavel e composto por: (I) Area de Protecao "
            "Ambiental -- APA (Art. 15); (II) Area de Relevante Interesse "
            "Ecologico -- ARIE (Art. 16); (III) Floresta Nacional -- FLONA "
            "(Art. 17); (IV) Reserva Extrativista -- RESEX (Art. 18); "
            "(V) Reserva de Fauna (Art. 19); (VI) Reserva de "
            "Desenvolvimento Sustentavel -- RDS (Art. 20); e (VII) Reserva "
            "Particular do Patrimonio Natural -- RPPN (Art. 21)."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 14",
        "complexity": "medium",
        "category": "UC Uso Sustentavel",
    },
    {
        "id": "SNUC_006",
        "question": (
            "Quais sao os requisitos para a criacao de uma unidade de "
            "conservacao e quais estudos sao necessarios?"
        ),
        "ground_truth": (
            "Conforme Art. 22 da Lei 9.985/2000, as unidades de "
            "conservacao sao criadas por ato do Poder Publico. A criacao "
            "deve ser precedida de estudos tecnicos e de consulta publica "
            "que permitam identificar a localizacao, a dimensao e os "
            "limites mais adequados para a unidade. O par.2o estabelece que "
            "para a criacao de Estacao Ecologica ou Reserva Biologica "
            "nao e obrigatoria a consulta publica."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 22",
        "complexity": "medium",
        "category": "Criacao de UC",
    },

    # -- SNUC - complex (2 existentes) ---------------------------------------
    {
        "id": "SNUC_007",
        "question": (
            "Como funciona a compensacao ambiental prevista no SNUC "
            "para empreendimentos de significativo impacto ambiental, "
            "e qual a relacao com o licenciamento da PNMA?"
        ),
        "ground_truth": (
            "Conforme Art. 36 da Lei 9.985/2000, nos casos de "
            "licenciamento ambiental de empreendimentos de significativo "
            "impacto ambiental (assim considerado pelo orgao ambiental "
            "competente, com fundamento em EIA/RIMA), o empreendedor e "
            "obrigado a apoiar a implantacao e manutencao de unidade de "
            "conservacao do grupo de Protecao Integral. O montante de "
            "recursos nao pode ser inferior a 0,5% dos custos totais de "
            "implantacao do empreendimento. Esta obrigacao conecta-se ao "
            "Art. 9o, incisos III e IV, e ao Art. 10 da Lei 6.938/1981 "
            "(PNMA), que estabelecem o EIA e o licenciamento como "
            "instrumentos obrigatorios da politica ambiental."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 36",
        "complexity": "complex",
        "category": "Compensacao Ambiental",
    },
    {
        "id": "SNUC_008",
        "question": (
            "Compare as diferencas entre Parque Nacional e Reserva "
            "Extrativista quanto a posse, uso de recursos e presenca "
            "de populacoes tradicionais."
        ),
        "ground_truth": (
            "O Parque Nacional (Art. 11 da Lei 9.985/2000), de Protecao "
            "Integral, e de posse e dominio publicos, proibe exploracoes "
            "ou aproveitamento dos recursos naturais, admite apenas uso "
            "indireto (pesquisa, educacao, turismo ecologico) e exige "
            "desapropriacao de areas particulares. A Reserva Extrativista "
            "(Art. 18), de Uso Sustentavel, e de dominio publico com uso "
            "concedido as populacoes extrativistas tradicionais, permite "
            "a exploracao sustentavel dos recursos naturais e proibe "
            "caca amadora ou profissional e exploracao de recursos "
            "minerais. O contraste reflete a distincao do Art. 7o entre "
            "os grupos de Protecao Integral (uso indireto) e Uso "
            "Sustentavel (uso direto regulado)."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 11",
        "complexity": "complex",
        "category": "UC Protecao Integral",
    },

    # -- SNUC - NOVAS (SNUC_009 a SNUC_016) ----------------------------------

    # SNUC_009 - simple - Art. 4 (objetivos do SNUC)
    {
        "id": "SNUC_009",
        "question": (
            "Quais sao os objetivos do Sistema Nacional de Unidades "
            "de Conservacao?"
        ),
        "ground_truth": (
            "Conforme Art. 4o da Lei 9.985/2000, o SNUC tem como "
            "objetivos: (I) contribuir para a manutencao da diversidade "
            "biologica e dos recursos geneticos; (II) proteger as "
            "especies ameacadas de extincao; (III) contribuir para a "
            "preservacao e a restauracao da diversidade de ecossistemas "
            "naturais; (IV) promover o desenvolvimento sustentavel a "
            "partir dos recursos naturais; (V) promover a utilizacao dos "
            "principios e praticas de conservacao no processo de "
            "desenvolvimento; (VI) proteger paisagens naturais e pouco "
            "alteradas de notavel beleza cenica; (VII) proteger as "
            "caracteristicas de natureza geologica, geomorfologica, "
            "espeleologica, paleontologica e cultural relevantes; entre "
            "outros."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 4",
        "complexity": "simple",
        "category": "Objetivos SNUC",
    },
    # SNUC_010 - simple - Art. 5 (diretrizes do SNUC)
    {
        "id": "SNUC_010",
        "question": (
            "Quais sao as principais diretrizes do SNUC?"
        ),
        "ground_truth": (
            "Conforme Art. 5o da Lei 9.985/2000, o SNUC sera regido "
            "por diretrizes que: (I) assegurem que no conjunto das UCs "
            "estejam representadas amostras significativas e "
            "ecologicamente viaveis das diferentes populacoes, habitats "
            "e ecossistemas do territorio nacional e das aguas "
            "jurisdicionais; (II) assegurem os mecanismos e "
            "procedimentos necessarios ao envolvimento da sociedade no "
            "estabelecimento e na revisao da politica nacional de UCs; "
            "(III) assegurem a participacao efetiva das populacoes locais "
            "na criacao, implantacao e gestao das UCs; entre outras."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 5",
        "complexity": "simple",
        "category": "Diretrizes SNUC",
    },
    # SNUC_011 - simple - Art. 9 (Estacao Ecologica)
    {
        "id": "SNUC_011",
        "question": (
            "O que e uma Estacao Ecologica e quais atividades sao "
            "permitidas nela?"
        ),
        "ground_truth": (
            "Conforme Art. 9o da Lei 9.985/2000, a Estacao Ecologica "
            "tem como objetivo a preservacao da natureza e a realizacao "
            "de pesquisas cientificas. E de posse e dominio publicos e "
            "as areas particulares incluidas em seus limites serao "
            "desapropriadas. E proibida a visitacao publica, exceto "
            "com objetivo educacional, conforme plano de manejo. "
            "A pesquisa cientifica depende de autorizacao previa do "
            "orgao responsavel e esta sujeita a condicoes e restricoes "
            "estabelecidas por este e no plano de manejo."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 9",
        "complexity": "simple",
        "category": "UC Protecao Integral",
    },
    # SNUC_012 - medium - Art. 15 (APA)
    {
        "id": "SNUC_012",
        "question": (
            "O que e uma Area de Protecao Ambiental (APA) e quais sao "
            "suas caracteristicas quanto a propriedade e uso do solo?"
        ),
        "ground_truth": (
            "Conforme Art. 15 da Lei 9.985/2000, a Area de Protecao "
            "Ambiental e uma area em geral extensa, com um certo grau "
            "de ocupacao humana, dotada de atributos abioticos, bioticos, "
            "esteticos ou culturais especialmente importantes para a "
            "qualidade de vida e o bem-estar das populacoes humanas. "
            "A APA e constituida por terras publicas ou privadas (par.1o). "
            "Respeitados os limites constitucionais, podem ser "
            "estabelecidas normas e restricoes para a utilizacao de uma "
            "propriedade privada localizada em APA (par.2o). As condicoes "
            "para pesquisa e visitacao publica serao estabelecidas pelo "
            "orgao gestor (par.3o). A APA dispora de Conselho presidido "
            "pelo orgao responsavel pela administracao (par.5o)."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 15",
        "complexity": "medium",
        "category": "UC Uso Sustentavel",
    },
    # SNUC_013 - medium - Art. 17 (FLONA)
    {
        "id": "SNUC_013",
        "question": (
            "O que e uma Floresta Nacional (FLONA) e como sao tratadas "
            "as populacoes tradicionais nessa categoria?"
        ),
        "ground_truth": (
            "Conforme Art. 17 da Lei 9.985/2000, a Floresta Nacional e "
            "uma area com cobertura florestal de especies "
            "predominantemente nativas e tem como objetivo basico o uso "
            "multiplo sustentavel dos recursos florestais e a pesquisa "
            "cientifica, com enfase em metodos para exploracao sustentavel "
            "de florestas nativas. E de posse e dominio publicos, e as "
            "areas particulares incluidas devem ser desapropriadas "
            "(par.1o). A visitacao publica e permitida, condicionada as "
            "normas do plano de manejo (par.2o). A pesquisa e permitida "
            "e incentivada (par.3o). Admite-se a permanencia de "
            "populacoes tradicionais que a habitam quando de sua "
            "criacao, em conformidade com o plano de manejo (par.4o)."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 17",
        "complexity": "medium",
        "category": "UC Uso Sustentavel",
    },
    # SNUC_014 - medium - Art. 28 (visitacao publica)
    {
        "id": "SNUC_014",
        "question": (
            "Como o SNUC regula a visitacao publica nas unidades de "
            "conservacao?"
        ),
        "ground_truth": (
            "Conforme Art. 28 da Lei 9.985/2000, sao proibidas nas UCs "
            "quaisquer alteracoes, atividades ou modalidades de utilizacao "
            "em desacordo com seus objetivos, o plano de manejo e seus "
            "regulamentos. A visitacao em Estacoes Ecologicas e Reservas "
            "Biologicas esta restrita ao carater educacional (Arts. 9o "
            "e 10). Nos Parques Nacionais, a visitacao publica esta "
            "sujeita as normas do plano de manejo e do orgao responsavel "
            "(Art. 11, par. unico). Nas UCs de Uso Sustentavel como APAs, "
            "FLONAs e RESEX, a visitacao e permitida conforme o plano "
            "de manejo da unidade."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 28",
        "complexity": "medium",
        "category": "Visitacao",
    },
    # SNUC_015 - complex - Art. 18 (RESEX) + Art. 20 (RDS) + Art. 30 (populacoes)
    {
        "id": "SNUC_015",
        "question": (
            "Compare a Reserva Extrativista (RESEX) e a Reserva de "
            "Desenvolvimento Sustentavel (RDS) quanto ao dominio, "
            "objetivos e tratamento de populacoes tradicionais, e como "
            "o Art. 30 do SNUC se aplica a ambas?"
        ),
        "ground_truth": (
            "A RESEX (Art. 18 da Lei 9.985/2000) e uma area utilizada "
            "por populacoes extrativistas tradicionais, de dominio "
            "publico com uso concedido por contrato, cujo objetivo e "
            "proteger os meios de vida e a cultura dessas populacoes. "
            "A RDS (Art. 20) tambem e de dominio publico, mas se "
            "distingue por abrigar populacoes tradicionais cuja existencia "
            "baseia-se em sistemas sustentaveis de exploracao dos recursos "
            "naturais, desenvolvidos ao longo de geracoes e adaptados as "
            "condicoes ecologicas locais. Em ambas, e admitida a "
            "exploracoes de componentes dos ecossistemas naturais em "
            "regime de manejo sustentavel. O Art. 30 estabelece que as "
            "populacoes tradicionais residentes em UCs nas quais sua "
            "permanencia nao seja permitida serao indenizadas ou "
            "compensadas e realocadas. Na RESEX e na RDS, ao contrario, "
            "a permanencia e assegurada por contrato de concessao de "
            "direito real de uso."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 18",
        "complexity": "complex",
        "category": "UC Uso Sustentavel",
    },
    # SNUC_016 - complex - Art. 10 (REBIO) + Art. 11 (Parque Nacional)
    {
        "id": "SNUC_016",
        "question": (
            "Compare a Reserva Biologica e o Parque Nacional quanto "
            "aos objetivos, regime de visitacao e possibilidade de "
            "pesquisa cientifica, indicando os fundamentos legais."
        ),
        "ground_truth": (
            "A Reserva Biologica (Art. 10 da Lei 9.985/2000) tem como "
            "objetivo a preservacao integral da biota e demais atributos "
            "naturais existentes em seus limites, sem interferencia "
            "humana direta ou modificacoes ambientais, excetuando-se as "
            "medidas de recuperacao de ecossistemas alterados e as acoes "
            "de manejo necessarias. A visitacao publica e proibida, "
            "exceto com objetivo educacional (par.2o). A pesquisa "
            "cientifica depende de autorizacao previa (par.3o). O Parque "
            "Nacional (Art. 11) tem como objetivo a preservacao de "
            "ecossistemas naturais de grande relevancia ecologica e "
            "beleza cenica, possibilitando pesquisas cientificas e "
            "atividades de educacao e interpretacao ambiental, recreacao "
            "em contato com a natureza e turismo ecologico. A visitacao "
            "publica e permitida conforme plano de manejo (par. unico). "
            "Assim, ambas sao de Protecao Integral (Art. 8o), mas o "
            "Parque Nacional e mais aberto a visitacao e turismo, "
            "enquanto a REBIO e a mais restritiva das categorias."
        ),
        "expected_law": "SNUC",
        "expected_article": "Art. 10",
        "complexity": "complex",
        "category": "UC Protecao Integral",
    },

    # =========================================================================
    # CRIMES AMBIENTAIS (Lei 9.605/1998) -- 16 perguntas
    # =========================================================================

    # -- CA - simple (4 existentes) ------------------------------------------
    {
        "id": "CA_001",
        "question": (
            "Qual a pena para quem pratica maus-tratos contra animais "
            "segundo a Lei de Crimes Ambientais?"
        ),
        "ground_truth": (
            "Conforme Art. 32 da Lei 9.605/1998, praticar ato de abuso, "
            "maus-tratos, ferir ou mutilar animais silvestres, domesticos "
            "ou domesticados, nativos ou exoticos, sujeita o infrator a "
            "pena de detencao de tres meses a um ano, e multa. O par.1o "
            "preve as mesmas penas para quem realiza experiencia dolorosa "
            "ou cruel em animal vivo, ainda que para fins didaticos ou "
            "cientificos, quando existirem recursos alternativos. A pena "
            "e aumentada de um sexto a um terco se ocorre a morte do "
            "animal (par.2o)."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 32",
        "complexity": "simple",
        "category": "Crimes Fauna",
    },
    {
        "id": "CA_002",
        "question": (
            "Qual a pena para quem destroi ou danifica floresta em area "
            "de preservacao permanente?"
        ),
        "ground_truth": (
            "Conforme Art. 38 da Lei 9.605/1998, destruir ou danificar "
            "floresta considerada de preservacao permanente, mesmo que em "
            "formacao, ou utiliza-la com infringencia das normas de "
            "protecao, sujeita o infrator a pena de detencao de um a "
            "tres anos, ou multa, ou ambas as penas cumulativamente."
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
            "poluidora sem a devida licenca ambiental?"
        ),
        "ground_truth": (
            "Conforme Art. 60 da Lei 9.605/1998, construir, reformar, "
            "ampliar, instalar ou fazer funcionar, em qualquer parte do "
            "territorio nacional, estabelecimentos, obras ou servicos "
            "potencialmente poluidores, sem licenca ou autorizacao dos "
            "orgaos ambientais competentes, ou contrariando as normas "
            "legais e regulamentares pertinentes, sujeita o infrator a "
            "pena de detencao de um a seis meses, ou multa, ou ambas "
            "cumulativamente."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 60",
        "complexity": "simple",
        "category": "Crimes Poluicao",
    },
    {
        "id": "CA_004",
        "question": (
            "Qual a pena prevista na Lei de Crimes Ambientais para quem "
            "mata, persegue ou caca especime da fauna silvestre sem "
            "autorizacao?"
        ),
        "ground_truth": (
            "Conforme Art. 29 da Lei 9.605/1998, matar, perseguir, "
            "cacar, apanhar, utilizar especimes da fauna silvestre, "
            "nativos ou em rota migratoria, sem a devida permissao, "
            "licenca ou autorizacao da autoridade competente, ou em "
            "desacordo com a obtida, sujeita o infrator a pena de "
            "detencao de seis meses a um ano, e multa."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 29",
        "complexity": "simple",
        "category": "Crimes Fauna",
    },

    # -- CA - medium (2 existentes) ------------------------------------------
    {
        "id": "CA_005",
        "question": (
            "O que configura o crime de poluicao qualificada na Lei de "
            "Crimes Ambientais e quais sao as penas?"
        ),
        "ground_truth": (
            "Conforme Art. 54 da Lei 9.605/1998, causar poluicao de "
            "qualquer natureza em niveis tais que resultem ou possam "
            "resultar em danos a saude humana, ou que provoquem a "
            "mortandade de animais ou a destruicao significativa da flora, "
            "sujeita o infrator a reclusao de um a quatro anos, e multa. "
            "O par.2o estabelece formas qualificadas com pena de reclusao de "
            "um a cinco anos quando: (I) tornar area urbana ou rural "
            "impropria para ocupacao; (II) causar poluicao atmosferica que "
            "provoque retirada de moradores; (III) causar poluicao hidrica "
            "que torne necessaria a interrupcao do abastecimento; "
            "(IV) dificultar ou impedir o uso publico de praias; "
            "(V) ocorrer lancamento de residuos solidos, liquidos ou "
            "gasosos em desacordo com as exigencias legais."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 54",
        "complexity": "medium",
        "category": "Crimes Poluicao",
    },
    {
        "id": "CA_006",
        "question": (
            "Qual a pena para quem falsifica ou altera dados em "
            "procedimentos administrativos ambientais, e quais condutas "
            "estao abrangidas?"
        ),
        "ground_truth": (
            "Conforme Art. 69-A da Lei 9.605/1998, elaborar ou "
            "apresentar, no licenciamento, concessao florestal ou "
            "qualquer outro procedimento administrativo, estudo, laudo "
            "ou relatorio ambiental total ou parcialmente falso ou "
            "enganoso, inclusive por omissao, sujeita o infrator a "
            "reclusao de tres a seis anos, e multa. O par.1o preve que, "
            "se o crime e culposo, a pena e de detencao de um a tres "
            "anos. O par.2o aumenta a pena de um terco a dois tercos se "
            "ha dano significativo ao meio ambiente em decorrencia do "
            "uso da informacao falsa."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 69-A",
        "complexity": "medium",
        "category": "Crimes Administrativos",
    },

    # -- CA - complex (2 existentes) -----------------------------------------
    {
        "id": "CA_007",
        "question": (
            "Compare as penas para crimes contra a flora em area de "
            "preservacao permanente (Art. 38) e em unidade de conservacao "
            "de protecao integral (Art. 40) da Lei de Crimes Ambientais, "
            "e explique como os conceitos de APP e UC se complementam."
        ),
        "ground_truth": (
            "O Art. 38 da Lei 9.605/1998 pune com detencao de 1 a 3 anos "
            "e/ou multa quem destroi floresta em APP. O Art. 40 pune "
            "com reclusao de 1 a 5 anos quem causa dano direto ou "
            "indireto a UC de Protecao Integral. A pena mais severa para "
            "UCs reflete o maior grau de protecao dessas areas. As APPs "
            "(Art. 4o do Codigo Florestal, Lei 12.651/2012) e as UCs de "
            "Protecao Integral (Art. 8o do SNUC, Lei 9.985/2000) sao "
            "instrumentos complementares: as APPs protegem recursos "
            "hidricos e relevo fragil de forma difusa em todo o territorio, "
            "enquanto as UCs delimitam areas especificas para preservacao "
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
            "Um proprietario rural impede a regeneracao natural de "
            "florestas e demais formas de vegetacao nativa em sua "
            "propriedade. Qual crime ele comete, qual a pena, e como "
            "essa conduta se relaciona com a obrigacao de recomposicao "
            "da Reserva Legal no Codigo Florestal?"
        ),
        "ground_truth": (
            "Conforme Art. 48 da Lei 9.605/1998, impedir ou dificultar "
            "a regeneracao natural de florestas e demais formas de "
            "vegetacao sujeita o infrator a detencao de seis meses a um "
            "ano, e multa. Essa conduta agrava-se quando o proprietario "
            "tem obrigacao legal de recompor a Reserva Legal: o Art. 66 "
            "da Lei 12.651/2012 (Codigo Florestal) preve que a "
            "regularizacao pode ser feita por regeneracao natural "
            "(inciso II). Ao impedir essa regeneracao, o infrator "
            "comete simultaneamente o crime do Art. 48 e descumpre a "
            "obrigacao de regularizacao do Codigo Florestal."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 48",
        "complexity": "complex",
        "category": "Crimes Flora",
    },

    # -- CA - NOVAS (CA_009 a CA_016) ----------------------------------------

    # CA_009 - simple - Art. 30 (exportar peles sem licenca)
    {
        "id": "CA_009",
        "question": (
            "Qual a pena para quem exporta peles e couros de anfibios "
            "e repteis sem a devida autorizacao?"
        ),
        "ground_truth": (
            "Conforme Art. 30 da Lei 9.605/1998, exportar para o "
            "exterior peles e couros de anfibios e repteis em bruto, "
            "sem a autorizacao da autoridade ambiental competente, "
            "sujeita o infrator a pena de reclusao de um a tres anos, "
            "e multa."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 30",
        "complexity": "simple",
        "category": "Crimes Fauna",
    },
    # CA_010 - simple - Art. 33 (pesca em periodo proibido)
    {
        "id": "CA_010",
        "question": (
            "Qual a pena para quem pesca em periodo no qual a pesca "
            "seja proibida ou em lugares interditados?"
        ),
        "ground_truth": (
            "Conforme Art. 34 da Lei 9.605/1998, pescar em periodo no "
            "qual a pesca seja proibida ou em lugares interditados por "
            "orgao competente sujeita o infrator a pena de detencao de "
            "um ano a tres anos, ou multa, ou ambas as penas "
            "cumulativamente. Incorre nas mesmas penas quem pesca "
            "especies que devam ser preservadas ou especimes com "
            "tamanhos inferiores aos permitidos, ou pesca quantidades "
            "superiores as permitidas, ou emprega apetrechos, "
            "tecnicas e metodos nao permitidos."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 34",
        "complexity": "simple",
        "category": "Crimes Fauna",
    },
    # CA_011 - simple - Art. 42 (fabricar balao de fogo)
    {
        "id": "CA_011",
        "question": (
            "Qual a pena para quem fabrica, vende, transporta ou solta "
            "baloes que possam provocar incendios em florestas?"
        ),
        "ground_truth": (
            "Conforme Art. 42 da Lei 9.605/1998, fabricar, vender, "
            "transportar ou soltar baloes que possam provocar incendios "
            "nas florestas e demais formas de vegetacao, em areas "
            "urbanas ou qualquer tipo de assentamento humano, sujeita "
            "o infrator a pena de detencao de um a tres anos, ou multa, "
            "ou ambas as penas cumulativamente."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 42",
        "complexity": "simple",
        "category": "Crimes Flora",
    },
    # CA_012 - simple - Art. 50 (destruir plantas de ornamentacao)
    {
        "id": "CA_012",
        "question": (
            "Qual a pena prevista na Lei de Crimes Ambientais para quem "
            "destroi ou danifica plantas de ornamentacao em logradouros "
            "publicos ou em propriedade privada alheia?"
        ),
        "ground_truth": (
            "Conforme Art. 49 da Lei 9.605/1998, destruir, danificar, "
            "lesar ou maltratar, por qualquer modo ou meio, plantas de "
            "ornamentacao de logradouros publicos ou em propriedade "
            "privada alheia sujeita o infrator a pena de detencao de "
            "tres meses a um ano, ou multa, ou ambas as penas "
            "cumulativamente. O par. unico preve que, se o crime for "
            "culposo, a pena sera de um a seis meses, ou multa."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 49",
        "complexity": "simple",
        "category": "Crimes Flora",
    },
    # CA_013 - medium - Art. 41 (provocar incendio em mata)
    {
        "id": "CA_013",
        "question": (
            "Qual a pena para quem provoca incendio em mata ou floresta, "
            "e quais as circunstancias que podem atenuar a pena?"
        ),
        "ground_truth": (
            "Conforme Art. 41 da Lei 9.605/1998, provocar incendio em "
            "mata ou floresta sujeita o infrator a reclusao de dois a "
            "quatro anos, e multa. O par. unico preve que se o crime "
            "e culposo, a pena e de detencao de seis meses a um ano, "
            "e multa. A forma culposa, portanto, constitui significativa "
            "atenuacao, aplicavel quando o incendio resulta de "
            "negligencia, imprudencia ou impericia do agente, sem "
            "intencao direta de provocar o fogo."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 41",
        "complexity": "medium",
        "category": "Crimes Flora",
    },
    # CA_014 - medium - Art. 46 (receber madeira sem licenca)
    {
        "id": "CA_014",
        "question": (
            "Quais condutas relativas a madeira, lenha, carvao e outros "
            "produtos de origem vegetal sao tipificadas como crime "
            "ambiental e qual a pena?"
        ),
        "ground_truth": (
            "Conforme Art. 46 da Lei 9.605/1998, receber ou adquirir, "
            "para fins comerciais ou industriais, madeira, lenha, carvao "
            "e outros produtos de origem vegetal, sem exigir a exibicao "
            "de autorizacao do vendedor, outorgada pela autoridade "
            "competente, e sem munir-se da via que devera acompanhar o "
            "produto ate final beneficiamento, sujeita o infrator a pena "
            "de detencao de seis meses a um ano, e multa. O par. unico "
            "incrimina tambem quem vende, expoe a venda, tem em "
            "deposito, transporta ou guarda madeira, lenha, carvao e "
            "outros produtos de origem vegetal, sem licenca valida para "
            "todo o tempo da viagem ou do armazenamento, outorgada pela "
            "autoridade competente."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 46",
        "complexity": "medium",
        "category": "Crimes Flora",
    },
    # CA_015 - medium - Art. 55 (extracao mineral sem licenca)
    {
        "id": "CA_015",
        "question": (
            "Qual a pena para quem realiza atividade de extracao mineral "
            "sem a competente autorizacao, e quais as consequencias se "
            "houver recuperacao da area degradada?"
        ),
        "ground_truth": (
            "Conforme Art. 55 da Lei 9.605/1998, executar pesquisa, "
            "lavra ou extracao de recursos minerais sem a competente "
            "autorizacao, permissao, concessao ou licenca, ou em "
            "desacordo com a obtida, sujeita o infrator a pena de "
            "detencao de seis meses a um ano, e multa. O par. unico "
            "preve que incorre nas mesmas penas quem deixa de recuperar "
            "a area pesquisada ou explorada, nos termos da autorizacao, "
            "permissao, licenca, concessao ou determinacao do orgao "
            "competente."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 55",
        "complexity": "medium",
        "category": "Crimes Mineracao",
    },
    # CA_016 - complex - Art. 56 (substancia toxica) + Art. 52 (UC)
    {
        "id": "CA_016",
        "question": (
            "Compare as penas para quem produz, processa ou comercializa "
            "substancia toxica sem licenca (Art. 56) e para quem penetra "
            "em UC conduzindo substancias nocivas (Art. 52). Como esses "
            "tipos penais se complementam na protecao ambiental?"
        ),
        "ground_truth": (
            "O Art. 56 da Lei 9.605/1998 pune com reclusao de um a "
            "quatro anos e multa quem produzir, processar, embalar, "
            "importar, exportar, comercializar, fornecer, transportar, "
            "armazenar, guardar, ter em deposito ou usar produto ou "
            "substancia toxica, perigosa ou nociva a saude humana ou "
            "ao meio ambiente, em desacordo com as exigencias legais. "
            "O Art. 52 pune com detencao de seis meses a um ano e multa "
            "quem penetrar em UC conduzindo substancias ou instrumentos "
            "proprios para caca ou para exploracao de produtos ou "
            "subprodutos florestais, sem licenca da autoridade competente. "
            "Os tipos se complementam: o Art. 56 pune o manuseio irregular "
            "de substancias toxicas em ambito geral, enquanto o Art. 52 "
            "agrega protecao especifica ao espaco das UCs, criminalizando "
            "a mera introducao de substancias nocivas, independentemente "
            "de dano efetivo, como medida preventiva de protecao "
            "territorial."
        ),
        "expected_law": "Crimes Ambientais",
        "expected_article": "Art. 56",
        "complexity": "complex",
        "category": "Crimes Poluicao",
    },

    # =========================================================================
    # CONAMA 357/2005 -- Qualidade da Agua -- 12 perguntas
    # =========================================================================

    # -- C357 - simple (2 existentes) ----------------------------------------
    {
        "id": "C357_001",
        "question": (
            "Como a Resolucao CONAMA 357/2005 define agua doce, agua "
            "salobra e agua salina?"
        ),
        "ground_truth": (
            "Conforme Art. 2o da Resolucao CONAMA 357/2005: agua doce "
            "e aquela com salinidade igual ou inferior a 0,5 por mil (inciso I); "
            "agua salobra e aquela com salinidade superior a 0,5 por mil e "
            "inferior a 30 por mil (inciso II); e agua salina e aquela com "
            "salinidade igual ou superior a 30 por mil (inciso III)."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 2",
        "complexity": "simple",
        "category": "Qualidade Agua",
    },
    {
        "id": "C357_002",
        "question": (
            "Quais sao as classes de enquadramento de aguas doces "
            "previstas na Resolucao CONAMA 357/2005?"
        ),
        "ground_truth": (
            "Conforme Art. 4o da Resolucao CONAMA 357/2005, as aguas "
            "doces sao classificadas em: Classe Especial (condicoes "
            "naturais, abastecimento sem tratamento, preservacao do "
            "equilibrio natural); Classe 1 (abastecimento com "
            "desinfeccao, protecao de comunidades aquaticas, recreacao "
            "de contato primario); Classe 2 (abastecimento com "
            "tratamento convencional, aquicultura, pesca); Classe 3 "
            "(abastecimento com tratamento convencional ou avancado, "
            "irrigacao, pesca); e Classe 4 (navegacao e harmonia "
            "paisagistica)."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 4",
        "complexity": "simple",
        "category": "Qualidade Agua",
    },

    # -- C357 - medium (2 existentes) ----------------------------------------
    {
        "id": "C357_003",
        "question": (
            "Quais sao as condicoes e padroes de qualidade para aguas "
            "doces de Classe 1 segundo a CONAMA 357/2005?"
        ),
        "ground_truth": (
            "Conforme Art. 5o (com referencia aos Arts. 14 e 15) da "
            "Resolucao CONAMA 357/2005, as aguas doces de Classe 1 devem "
            "atender, entre outras condicoes: nao verificacao de efeito "
            "toxico cronico a organismos; materiais flutuantes virtualmente "
            "ausentes; OD (oxigenio dissolvido) nao inferior a 6 mg/L; "
            "DBO ate 3 mg/L; turbidez ate 40 UNT; pH entre 6,0 e 9,0; "
            "coliformes termotolerantes ate 200 NMP/100 mL para "
            "balneabilidade; alem de padroes especificos para substancias "
            "inorganicas e organicas."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 5",
        "complexity": "medium",
        "category": "Padroes Qualidade",
    },
    {
        "id": "C357_004",
        "question": (
            "Quais sao as classes de enquadramento para aguas salinas "
            "e quais os usos preponderantes de cada classe?"
        ),
        "ground_truth": (
            "Conforme Art. 10 da Resolucao CONAMA 357/2005, as aguas "
            "salinas sao classificadas em: Classe Especial (preservacao "
            "dos ambientes aquaticos em UCs de Protecao Integral); "
            "Classe 1 (recreacao de contato primario, protecao de "
            "comunidades aquaticas, aquicultura e atividade de pesca); "
            "Classe 2 (pesca amadora, recreacao de contato secundario); "
            "e Classe 3 (navegacao e harmonia paisagistica)."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 10",
        "complexity": "medium",
        "category": "Qualidade Agua",
    },

    # -- C357 - complex (2 existentes) ---------------------------------------
    {
        "id": "C357_005",
        "question": (
            "Qual a relacao entre a classificacao dos corpos d'agua "
            "da CONAMA 357/2005 e as condicoes de lancamento de "
            "efluentes da CONAMA 430/2011?"
        ),
        "ground_truth": (
            "A Resolucao CONAMA 357/2005 estabelece, em seus Arts. 4o a "
            "13, a classificacao dos corpos d'agua em funcao dos usos "
            "preponderantes e define os padroes de qualidade para cada "
            "classe. O Art. 14 dessa resolucao trata das condicoes de "
            "lancamento. A Resolucao CONAMA 430/2011 complementa e "
            "atualiza essas condicoes, detalhando no Art. 5o as "
            "condicoes de lancamento direto de efluentes e no Art. 16 "
            "os padroes especificos. O principio e que o lancamento de "
            "efluentes nao pode comprometer os padroes de qualidade da "
            "classe do corpo receptor (CONAMA 357), e a zona de mistura "
            "(CONAMA 430, Art. 3o) define o trecho onde se permite a "
            "diluicao do efluente."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 14",
        "complexity": "complex",
        "category": "Padroes Qualidade",
    },
    {
        "id": "C357_006",
        "question": (
            "Se um corpo d'agua esta enquadrado como Classe 2 e recebe "
            "efluentes tratados, quais padroes de qualidade devem ser "
            "mantidos e qual a responsabilidade do empreendedor em caso "
            "de desconformidade, considerando tanto a CONAMA 357 quanto "
            "a PNMA?"
        ),
        "ground_truth": (
            "Conforme Art. 4o da Resolucao CONAMA 357/2005, o corpo "
            "d'agua Classe 2 deve manter: OD nao inferior a 5 mg/L, "
            "DBO ate 5 mg/L, turbidez ate 100 UNT, coliformes "
            "termotolerantes ate 1.000 NMP/100 mL. O lancamento de "
            "efluentes deve observar as condicoes da CONAMA 430/2011 e "
            "nao pode comprometer esses padroes. Em caso de "
            "desconformidade, o empreendedor responde objetivamente por "
            "danos ambientais conforme Art. 14, par.1o da Lei 6.938/1981 "
            "(PNMA), independentemente de culpa, devendo indenizar ou "
            "reparar os danos."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 4",
        "complexity": "complex",
        "category": "Padroes Qualidade",
    },

    # -- C357 - NOVAS (C357_007 a C357_012) ----------------------------------

    # C357_007 - simple - Art. 3 (definicoes com limites de salinidade)
    {
        "id": "C357_007",
        "question": (
            "Quais sao os limites de salinidade que distinguem aguas "
            "doces, salobras e salinas na CONAMA 357/2005?"
        ),
        "ground_truth": (
            "Conforme Art. 2o da Resolucao CONAMA 357/2005: aguas doces "
            "possuem salinidade igual ou inferior a 0,5 por mil; aguas "
            "salobras possuem salinidade superior a 0,5 por mil e inferior "
            "a 30 por mil; aguas salinas possuem salinidade igual ou "
            "superior a 30 por mil. Esses limites sao fundamentais para "
            "determinar quais padroes de qualidade se aplicam, ja que "
            "cada tipo de agua (doce, salobra, salina) possui classes "
            "e parametros distintos na resolucao."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 2",
        "complexity": "simple",
        "category": "Qualidade Agua",
    },
    # C357_008 - simple - Art. 6 (classes de agua salobra)
    {
        "id": "C357_008",
        "question": (
            "Quais sao as classes de enquadramento de aguas salobras "
            "na CONAMA 357/2005 e seus usos preponderantes?"
        ),
        "ground_truth": (
            "Conforme Art. 6o da Resolucao CONAMA 357/2005, as aguas "
            "salobras sao classificadas em: Classe Especial (preservacao "
            "dos ambientes aquaticos em UCs de Protecao Integral); "
            "Classe 1 (recreacao de contato primario, protecao das "
            "comunidades aquaticas, aquicultura e atividade de pesca, "
            "abastecimento apos tratamento convencional ou avancado, "
            "irrigacao); Classe 2 (pesca amadora e recreacao de contato "
            "secundario); e Classe 3 (navegacao e harmonia paisagistica)."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 6",
        "complexity": "simple",
        "category": "Qualidade Agua",
    },
    # C357_009 - medium - Art. 12 (enquadramento dos corpos d'agua)
    {
        "id": "C357_009",
        "question": (
            "O que e o enquadramento dos corpos d'agua e qual seu "
            "objetivo segundo a CONAMA 357/2005?"
        ),
        "ground_truth": (
            "Conforme Art. 12 da Resolucao CONAMA 357/2005 (com base "
            "no Art. 9o, I da Lei 9.433/1997), o enquadramento dos corpos "
            "d'agua corresponde ao estabelecimento da meta ou objetivo "
            "de qualidade da agua (classe) a ser obrigatoriamente "
            "alcancado ou mantido em um segmento de corpo d'agua, de "
            "acordo com os usos preponderantes pretendidos, ao longo "
            "do tempo. O enquadramento visa assegurar as aguas qualidade "
            "compativel com os usos mais exigentes a que forem "
            "destinadas e diminuir os custos de combate a poluicao das "
            "aguas mediante acoes preventivas permanentes."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 12",
        "complexity": "medium",
        "category": "Enquadramento",
    },
    # C357_010 - medium - Art. 24 (competencia de enquadramento)
    {
        "id": "C357_010",
        "question": (
            "A quem compete a proposta de enquadramento dos corpos d'agua "
            "e qual o procedimento segundo a CONAMA 357/2005?"
        ),
        "ground_truth": (
            "Conforme Art. 38 da Resolucao CONAMA 357/2005, o "
            "enquadramento dos corpos de agua sera definido pelos "
            "Conselhos Estaduais de Recursos Hidricos, mediante "
            "proposta das Agencias de Agua ou dos orgaos gestores de "
            "recursos hidricos. O processo deve considerar: o diagnostico "
            "do uso e da ocupacao do solo e dos recursos hidricos na "
            "bacia hidrografica; a identificacao e avaliacao dos "
            "impactos ambientais existentes; o prognostico da qualidade "
            "da agua; e a realizacao de consulta publica. Os corpos "
            "de agua que nao tiverem enquadramento serao considerados "
            "como de Classe 2."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 38",
        "complexity": "medium",
        "category": "Enquadramento",
    },
    # C357_011 - complex - Art. 30 (padroes de lancamento) + Art. 32 (monitoramento)
    {
        "id": "C357_011",
        "question": (
            "Como se articulam os padroes de lancamento de efluentes e "
            "o monitoramento dos corpos d'agua na CONAMA 357/2005, e "
            "qual o papel do orgao ambiental nesse controle?"
        ),
        "ground_truth": (
            "A CONAMA 357/2005 estabelece nos Arts. 24 a 34 as condicoes "
            "e padroes de lancamento de efluentes, determinando que "
            "qualquer fonte potencial ou efetivamente poluidora somente "
            "podera lancar efluentes nos corpos d'agua desde que obedeça "
            "as condicoes e padroes previstos. O Art. 34 especifica "
            "parametros inorganicos e organicos maximos. O monitoramento "
            "e tratado no Art. 8o, par.4o e Art. 9o, par.3o, que "
            "determinam que os orgaos competentes deverao monitorar a "
            "qualidade da agua em consonancia com os parametros de cada "
            "classe. O orgao ambiental competente pode, a qualquer "
            "momento, acrescentar condicoes e padroes, exigir tecnologia "
            "ambientalmente adequada e economicamente viavel para "
            "tratamento dos efluentes, e determinar ao empreendedor "
            "o automonitoramento com cronograma definido."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 34",
        "complexity": "complex",
        "category": "Padroes Qualidade",
    },
    # C357_012 - complex - Art. 7 (classes agua salina) + Art. 4 + Art. 6
    {
        "id": "C357_012",
        "question": (
            "Compare as classes de enquadramento para aguas doces, "
            "salobras e salinas na CONAMA 357/2005, indicando as "
            "semelhancas e diferencas entre os sistemas de classificacao "
            "e os usos preponderantes."
        ),
        "ground_truth": (
            "A CONAMA 357/2005 classifica as aguas doces (Art. 4o) em "
            "Classe Especial e Classes 1 a 4; as aguas salobras (Art. 6o) "
            "em Classe Especial e Classes 1 a 3; e as aguas salinas "
            "(Art. 7o) tambem em Classe Especial e Classes 1 a 3. Todas "
            "as categorias possuem Classe Especial para preservacao de "
            "ambientes aquaticos em UCs de Protecao Integral. As "
            "semelhancas incluem a gradacao de usos mais nobres (Classe 1: "
            "recreacao de contato primario, protecao aquatica) a menos "
            "exigentes (Classe 3 ou 4: navegacao). As diferencas residem "
            "nos parametros especificos: aguas doces possuem limites de "
            "OD, DBO, coliformes por classe; aguas salobras e salinas "
            "possuem parametros adaptados a seus ambientes estuarinos "
            "e marinhos. A Classe 4, exclusiva das aguas doces, destina-se "
            "apenas a navegacao e harmonia paisagistica."
        ),
        "expected_law": "CONAMA 357",
        "expected_article": "Art. 7",
        "complexity": "complex",
        "category": "Qualidade Agua",
    },

    # =========================================================================
    # CONAMA 430/2011 -- Lancamento de Efluentes -- 10 perguntas
    # =========================================================================

    # -- C430 - simple (2 existentes) ----------------------------------------
    {
        "id": "C430_001",
        "question": (
            "O que a Resolucao CONAMA 430/2011 define como corpo "
            "receptor e zona de mistura?"
        ),
        "ground_truth": (
            "Conforme Art. 3o da Resolucao CONAMA 430/2011: corpo "
            "receptor e o corpo hidrico que recebe o lancamento de "
            "efluentes; zona de mistura e a regiao do corpo receptor "
            "onde ocorre a diluicao inicial do efluente, definida pelo "
            "orgao ambiental competente, podendo ser dispensada sua "
            "caracterizacao quando nao houver substancias que "
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
            "Quais sao os principais padroes de lancamento de efluentes "
            "definidos no Art. 16 da CONAMA 430/2011?"
        ),
        "ground_truth": (
            "Conforme Art. 16 da Resolucao CONAMA 430/2011, os efluentes "
            "de qualquer fonte poluidora somente poderao ser lancados "
            "diretamente no corpo receptor desde que obedecam, entre "
            "outros, os seguintes padroes: pH entre 5 e 9; temperatura "
            "inferior a 40 oC; materiais sedimentaveis ate 1 mL/L em "
            "teste de 1 hora em cone Imhoff; oleos e graxas minerais "
            "ate 20 mg/L e oleos vegetais e gorduras animais ate "
            "50 mg/L; ausencia de materiais flutuantes; alem de limites "
            "especificos para substancias inorganicas e organicas."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 16",
        "complexity": "simple",
        "category": "Padroes Efluentes",
    },

    # -- C430 - medium (2 existentes) ----------------------------------------
    {
        "id": "C430_003",
        "question": (
            "Quais sao as condicoes gerais para lancamento direto de "
            "efluentes em corpos d'agua receptores segundo a "
            "CONAMA 430/2011?"
        ),
        "ground_truth": (
            "Conforme Art. 5o da Resolucao CONAMA 430/2011, os efluentes "
            "nao poderao: conferir ao corpo receptor caracteristicas em "
            "desacordo com as metas obrigatorias de enquadramento; "
            "causar ou possuir potencial para causar efeitos toxicos "
            "aos organismos aquaticos no corpo receptor. Os lancamentos "
            "devem atender simultaneamente as condicoes e padroes de "
            "lancamento de efluentes (Arts. 16 e seguintes) e nao "
            "ocasionar a ultrapassagem dos padroes de qualidade da "
            "classe do corpo receptor. O orgao ambiental pode exigir "
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
            "Quais sao os padroes especificos para lancamento de "
            "efluentes originarios de sistemas de tratamento de "
            "esgotos sanitarios?"
        ),
        "ground_truth": (
            "Conforme Art. 21 da Resolucao CONAMA 430/2011, os efluentes "
            "originarios de sistemas de tratamento de esgotos sanitarios "
            "devem atender, alem das condicoes gerais (Art. 16), os "
            "seguintes padroes especificos: pH entre 5 e 9; temperatura "
            "inferior a 40 oC; DBO maxima de 120 mg/L ou tratamento com "
            "eficiencia minima de 60% de remocao de DBO, sendo que o "
            "orgao ambiental pode fixar limites mais restritivos; "
            "solidos sedimentaveis ate 1 mL/L; e demais substancias "
            "em conformidade com os padroes da resolucao."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 21",
        "complexity": "medium",
        "category": "Esgotos Sanitarios",
    },

    # -- C430 - complex (1 existente) ----------------------------------------
    {
        "id": "C430_005",
        "question": (
            "Uma industria pretende lancar efluentes em um rio "
            "enquadrado como Classe 2. Considerando a CONAMA 430/2011 "
            "e a CONAMA 357/2005, quais padroes deve observar "
            "simultaneamente e qual a consequencia criminal de "
            "lancar sem licenca?"
        ),
        "ground_truth": (
            "A industria deve observar cumulativamente: (1) os padroes "
            "de lancamento de efluentes do Art. 16 da CONAMA 430/2011 "
            "(pH 5-9, temperatura < 40 oC, DBO, substancias toxicas); "
            "(2) as condicoes gerais do Art. 5o da CONAMA 430/2011, "
            "garantindo que o lancamento nao comprometa os padroes de "
            "qualidade da Classe 2 (Art. 4o da CONAMA 357/2005: "
            "OD >= 5 mg/L, DBO <= 5 mg/L no corpo receptor); e "
            "(3) obter licenciamento ambiental conforme Art. 10 da "
            "Lei 6.938/1981 (PNMA). Caso lance efluentes sem licenca, "
            "incorre no Art. 60 da Lei 9.605/1998, com detencao de um "
            "a seis meses e/ou multa. Se causar poluicao com danos a "
            "saude ou mortandade de animais, aplica-se o Art. 54 com "
            "reclusao de um a cinco anos."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 16",
        "complexity": "complex",
        "category": "Padroes Efluentes",
    },

    # -- C430 - NOVAS (C430_006 a C430_010) ----------------------------------

    # C430_006 - simple - Art. 4 (fontes poluidoras)
    {
        "id": "C430_006",
        "question": (
            "O que a CONAMA 430/2011 considera como fontes poluidoras "
            "sujeitas as suas disposicoes?"
        ),
        "ground_truth": (
            "Conforme Art. 2o da Resolucao CONAMA 430/2011, esta "
            "resolucao dispoe sobre condicoes, parametros, padroes e "
            "diretrizes para gestao do lancamento de efluentes em corpos "
            "de agua receptores, alterando parcialmente e complementando "
            "a Resolucao CONAMA 357/2005. O Art. 4o estabelece que os "
            "efluentes de qualquer fonte poluidora somente poderao ser "
            "lancados diretamente nos corpos receptores apos o devido "
            "tratamento e desde que obedecam as condicoes, padroes e "
            "exigencias dispostos na resolucao e em outras normas "
            "aplicaveis. Fonte poluidora e qualquer atividade, sistema, "
            "processo, operacao, maquinaria, equipamento ou dispositivo "
            "movel ou nao, que origine ou possa originar a emissao de "
            "poluentes."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 4",
        "complexity": "simple",
        "category": "Efluentes",
    },
    # C430_007 - simple - Art. 6 (lancamento indireto)
    {
        "id": "C430_007",
        "question": (
            "O que a CONAMA 430/2011 preve sobre o lancamento indireto "
            "de efluentes?"
        ),
        "ground_truth": (
            "Conforme Art. 6o da Resolucao CONAMA 430/2011, o lancamento "
            "indireto de efluentes no corpo receptor devera observar o "
            "disposto nesta Resolucao quando verificada a inexistencia "
            "de legislacao ou normas especificas, disposicoes do orgao "
            "ambiental competente, bem como diretrizes da operadora de "
            "sistemas de coleta e tratamento de esgotos sanitarios. "
            "Os efluentes lancados nas redes coletoras de esgotos "
            "deverao atender a normatizacao da concessionaria do servico "
            "publico de esgotamento sanitario."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 6",
        "complexity": "simple",
        "category": "Efluentes",
    },
    # C430_008 - medium - Art. 8 (padroes ecotoxicologicos)
    {
        "id": "C430_008",
        "question": (
            "O que a CONAMA 430/2011 preve sobre ensaios "
            "ecotoxicologicos para efluentes e qual a sua importancia "
            "para o controle da poluicao?"
        ),
        "ground_truth": (
            "Conforme Art. 18 da Resolucao CONAMA 430/2011, o orgao "
            "ambiental competente podera exigir a realizacao de ensaios "
            "ecotoxicologicos para avaliar os efeitos dos efluentes "
            "sobre organismos aquaticos representativos do corpo receptor. "
            "Os testes de toxicidade aguda e cronica devem utilizar "
            "organismos aquaticos de pelo menos dois niveis troficos "
            "diferentes. Essa exigencia complementa os padroes "
            "quimicos do Art. 16, pois substancias individuais podem "
            "atender aos limites numericos, mas seus efeitos "
            "sinergicos ou combinados podem causar toxicidade "
            "significativa, o que so e detectavel por ensaios "
            "biologicos."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 18",
        "complexity": "medium",
        "category": "Ecotoxicologia",
    },
    # C430_009 - medium - Art. 22 (monitoramento)
    {
        "id": "C430_009",
        "question": (
            "Quais sao as obrigacoes de monitoramento dos efluentes "
            "previstas na CONAMA 430/2011 e quem pode determina-las?"
        ),
        "ground_truth": (
            "Conforme Art. 23 da Resolucao CONAMA 430/2011, o orgao "
            "ambiental competente podera, a qualquer momento, exigir "
            "a melhor tecnologia de tratamento de efluentes e adicionar "
            "condicoes e padroes para o lancamento, inclusive "
            "cronograma de implantacao. O Art. 24 determina que a "
            "responsabilidade pelo monitoramento da qualidade dos "
            "efluentes lancados e do empreendedor. O orgao ambiental "
            "devera estabelecer a frequencia, os parametros e os "
            "metodos de amostragem e analise. Os resultados de "
            "monitoramento devem ser mantidos pelo empreendedor a "
            "disposicao das autoridades ambientais por um periodo "
            "minimo de cinco anos."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 24",
        "complexity": "complex",
        "category": "Monitoramento",
    },
    # C430_010 - complex - Art. 19 + Art. 21 (sistemas de tratamento)
    {
        "id": "C430_010",
        "question": (
            "Compare os padroes de lancamento para efluentes industriais "
            "(Art. 16) e para efluentes de sistemas de tratamento de "
            "esgotos sanitarios (Art. 21) na CONAMA 430/2011, explicando "
            "por que os limites sao diferentes e quando se aplica a "
            "DBO maxima de 120 mg/L."
        ),
        "ground_truth": (
            "Os efluentes industriais devem atender os padroes do "
            "Art. 16 da CONAMA 430/2011, incluindo pH entre 5 e 9, "
            "temperatura inferior a 40 oC, materiais sedimentaveis "
            "ate 1 mL/L, oleos e graxas minerais ate 20 mg/L, alem "
            "de limites especificos para substancias inorganicas e "
            "organicas. Para efluentes de sistemas de tratamento de "
            "esgotos sanitarios, o Art. 21 estabelece padroes "
            "diferenciados: DBO maxima de 120 mg/L ou eficiencia minima "
            "de 60% de remocao. A diferenca justifica-se porque esgotos "
            "sanitarios possuem composicao predominantemente organica "
            "e biodegradavel, enquanto efluentes industriais podem "
            "conter substancias toxicas e recalcitrantes que exigem "
            "limites mais restritivos por parametro. O Art. 21, par.1o "
            "permite ao orgao ambiental fixar limites mais restritivos "
            "que 120 mg/L de DBO quando estudos de capacidade de "
            "suporte do corpo receptor assim indicarem."
        ),
        "expected_law": "CONAMA 430",
        "expected_article": "Art. 21",
        "complexity": "complex",
        "category": "Padroes Efluentes",
    },
]


# ---------------------------------------------------------------------------
# Validacao interna -- executar com:  python -m scripts.eval_dataset
# ---------------------------------------------------------------------------
def _validate_dataset() -> None:
    """Imprime a distribuicao do dataset e valida as contagens."""
    from collections import Counter

    total = len(EVAL_DATASET_FULL)
    ids = [item["id"] for item in EVAL_DATASET_FULL]
    laws = Counter(item["expected_law"] for item in EVAL_DATASET_FULL)
    complexities = Counter(item["complexity"] for item in EVAL_DATASET_FULL)
    categories = Counter(item["category"] for item in EVAL_DATASET_FULL)

    errors: list[str] = []

    if total != 100:
        errors.append(f"Total: esperado 100, encontrado {total}")
    if len(ids) != len(set(ids)):
        dupes = [i for i in ids if ids.count(i) > 1]
        errors.append(f"IDs duplicados: {set(dupes)}")
    if complexities["simple"] != 40:
        errors.append(f"Simple: esperado 40, encontrado {complexities['simple']}")
    if complexities["medium"] != 35:
        errors.append(f"Medium: esperado 35, encontrado {complexities['medium']}")
    if complexities["complex"] != 25:
        errors.append(f"Complex: esperado 25, encontrado {complexities['complex']}")
    if laws["Codigo Florestal"] != 30:
        errors.append(f"CF: esperado 30, encontrado {laws['Codigo Florestal']}")
    if laws["PNMA"] != 16:
        errors.append(f"PNMA: esperado 16, encontrado {laws['PNMA']}")
    if laws["SNUC"] != 16:
        errors.append(f"SNUC: esperado 16, encontrado {laws['SNUC']}")
    if laws["Crimes Ambientais"] != 16:
        errors.append(f"CA: esperado 16, encontrado {laws['Crimes Ambientais']}")
    if laws["CONAMA 357"] != 12:
        errors.append(f"C357: esperado 12, encontrado {laws['CONAMA 357']}")
    if laws["CONAMA 430"] != 10:
        errors.append(f"C430: esperado 10, encontrado {laws['CONAMA 430']}")

    # Checar chaves obrigatorias em cada item
    required_keys = {
        "id", "question", "ground_truth", "expected_law",
        "expected_article", "complexity", "category",
    }
    for i, item in enumerate(EVAL_DATASET_FULL):
        missing = required_keys - item.keys()
        if missing:
            errors.append(f"Item {i} ({item.get('id', '?')}): faltam chaves {missing}")

    if errors:
        print("FALHA NA VALIDACAO:")
        for e in errors:
            print(f"  - {e}")
        raise SystemExit(1)

    print("EVAL_DATASET_FULL validado com sucesso!")
    print(f"  Total: {total} perguntas")
    print(f"  Por legislacao:   {dict(laws)}")
    print(f"  Por complexidade: {dict(complexities)}")
    print(f"  Categorias:       {dict(categories)}")
    print(f"  IDs unicos:       {len(set(ids))}")


if __name__ == "__main__":
    _validate_dataset()
