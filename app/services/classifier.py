import re

from app.config import settings
from app.models.schemas import QueryComplexity

LEGAL_TERMS = {
    "app", "arl", "reserva legal", "código florestal", "conama", "snuc",
    "unidade de conservação", "área de preservação", "licenciamento",
    "eia", "rima", "outorga", "recurso hídrico", "pnma", "sisnama",
    "ibama", "icmbio", "desmatamento", "supressão", "vegetação nativa",
    "zona de amortecimento", "corredor ecológico", "servidão ambiental",
    "compensação ambiental", "degradação", "recuperação", "bioma",
    "mata atlântica", "cerrado", "amazônia", "caatinga", "pantanal",
    "mangue", "restinga", "nascente", "topo de morro", "encosta",
    "várzea", "vereda", "rio", "curso d'água", "faixa marginal",
}

COMPARATIVE_MARKERS = {
    "compare", "diferença", "diferente", "versus", "vs", "em relação a",
    "comparando", "confronte", "contraponha",
}

CONDITIONAL_MARKERS = {
    "se", "caso", "quando", "hipótese", "situação", "cenário",
    "supondo", "considerando que", "na hipótese de",
}

MULTI_HOP_MARKERS = {
    "e também", "além disso", "adicionalmente", "cumulativamente",
    "em conjunto com", "combinado com", "à luz de",
    "levando em conta", "considerando",
}


def classify_query(question: str) -> tuple[QueryComplexity, dict]:
    q = question.lower().strip()
    words = q.split()
    word_count = len(words)

    legal_count = sum(1 for term in LEGAL_TERMS if term in q)
    has_comparative = any(m in q for m in COMPARATIVE_MARKERS)
    has_conditional = any(m in q for m in CONDITIONAL_MARKERS)
    has_multi_hop = any(m in q for m in MULTI_HOP_MARKERS)

    question_marks = q.count("?")
    conjunctions = sum(1 for w in words if w in {"e", "ou", "mas", "porém", "contudo"})

    complexity_score = 0
    complexity_score += min(legal_count, 3)  # max 3 pontos por termos legais
    complexity_score += 2 if has_comparative else 0
    complexity_score += 1 if has_conditional else 0
    complexity_score += 2 if has_multi_hop else 0
    complexity_score += 1 if question_marks > 1 else 0
    complexity_score += 1 if conjunctions >= 2 else 0
    complexity_score += 1 if word_count > 30 else 0

    if complexity_score <= 2:
        level = QueryComplexity.SIMPLE
    elif complexity_score <= 5:
        level = QueryComplexity.MEDIUM
    else:
        level = QueryComplexity.COMPLEX

    params = _get_adaptive_params(level)
    params["score"] = complexity_score
    params["features"] = {
        "legal_terms": legal_count,
        "comparative": has_comparative,
        "conditional": has_conditional,
        "multi_hop": has_multi_hop,
        "word_count": word_count,
    }

    return level, params


def _get_adaptive_params(level: QueryComplexity) -> dict:
    config = {
        QueryComplexity.SIMPLE: {
            "top_k": settings.hypa_k_simple,
            "query_rewrites": settings.hypa_rewrites_simple,
        },
        QueryComplexity.MEDIUM: {
            "top_k": settings.hypa_k_medium,
            "query_rewrites": settings.hypa_rewrites_medium,
        },
        QueryComplexity.COMPLEX: {
            "top_k": settings.hypa_k_complex,
            "query_rewrites": settings.hypa_rewrites_complex,
        },
    }
    return config[level]
