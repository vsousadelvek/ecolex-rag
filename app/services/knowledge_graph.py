import json
import re
from pathlib import Path

from loguru import logger

from app.config import settings


class LegalKnowledgeGraph:
    """Knowledge Graph baseado na estrutura hierárquica da legislação brasileira.

    Extrai triplets no formato (sujeito, relação, objeto) a partir da
    estrutura legal: Lei → Capítulo → Seção → Artigo → Parágrafo → Inciso → Alínea.
    """

    def __init__(self):
        self._triplets: list[dict] = []
        self._entity_index: dict[str, list[int]] = {}  # entity -> triplet indices

    def load(self):
        kg_path = Path(settings.kg_index_path)
        if kg_path.exists():
            with open(kg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._triplets = data.get("triplets", [])
            self._rebuild_entity_index()
            logger.info(f"Knowledge Graph carregado: {len(self._triplets)} triplets")
        else:
            logger.info("Knowledge Graph vazio inicializado")

    def save(self):
        kg_path = Path(settings.kg_index_path)
        kg_path.parent.mkdir(parents=True, exist_ok=True)
        with open(kg_path, "w", encoding="utf-8") as f:
            json.dump(
                {"triplets": self._triplets},
                f,
                ensure_ascii=False,
                indent=2,
            )
        logger.info(f"Knowledge Graph salvo: {len(self._triplets)} triplets")

    def extract_triplets(self, text: str, law_name: str) -> list[dict]:
        triplets = []

        # Extrair artigos e seus conteúdos
        article_pattern = re.compile(
            r"(Art\.\s*\d+[\w-]*\.?)\s*(.*?)(?=Art\.\s*\d+[\w-]*\.?|\Z)",
            re.DOTALL | re.IGNORECASE,
        )

        for match in article_pattern.finditer(text):
            article_id = match.group(1).strip().rstrip(".")
            article_body = match.group(2).strip()

            # Triplet: artigo pertence à lei
            triplets.append({
                "subject": article_id,
                "relation": "pertence_a",
                "object": law_name,
                "context": article_body[:300],
            })

            # Extrair parágrafos
            para_pattern = re.compile(
                r"(§\s*\d+[°º]?\.?|Parágrafo\s+único\.?)\s*(.*?)(?=§\s*\d+|Parágrafo\s+único|Art\.\s*\d+|\Z)",
                re.DOTALL | re.IGNORECASE,
            )
            for para in para_pattern.finditer(article_body):
                para_id = para.group(1).strip()
                para_body = para.group(2).strip()
                triplets.append({
                    "subject": f"{article_id}, {para_id}",
                    "relation": "detalha",
                    "object": article_id,
                    "context": para_body[:300],
                })

            # Extrair incisos (I, II, III... ou I -, II -)
            inciso_pattern = re.compile(
                r"((?:^|\n)\s*(?:X{0,3}(?:IX|IV|V?I{0,3}))\s*[-–—\.)])\s*(.*?)(?=\n\s*(?:X{0,3}(?:IX|IV|V?I{0,3}))\s*[-–—\.\)]|\Z)",
                re.DOTALL,
            )
            for inc in inciso_pattern.finditer(article_body):
                inciso_id = inc.group(1).strip()
                inciso_body = inc.group(2).strip()
                if len(inciso_body) > 10:
                    triplets.append({
                        "subject": f"{article_id}, {inciso_id}",
                        "relation": "define",
                        "object": article_id,
                        "context": inciso_body[:300],
                    })

            # Extrair conceitos definidos (ex: "entende-se por", "considera-se")
            definitions = re.findall(
                r"(?:entende-se por|considera-se|define-se como)\s+(.+?)(?:[:,;.])",
                article_body,
                re.IGNORECASE,
            )
            for defn in definitions:
                defn = defn.strip()
                if len(defn) > 3:
                    triplets.append({
                        "subject": defn,
                        "relation": "definido_em",
                        "object": f"{law_name}, {article_id}",
                        "context": article_body[:300],
                    })

            # Extrair medidas numéricas (ex: "30 (trinta) metros", "50m")
            measures = re.findall(
                r"(\d+)\s*(?:\([^)]+\)\s*)?(?:metros?|m\b|hectares?|ha\b|%|por cento)",
                article_body,
                re.IGNORECASE,
            )
            for measure in measures:
                triplets.append({
                    "subject": article_id,
                    "relation": "estabelece_medida",
                    "object": f"{measure} (unidade em contexto)",
                    "context": article_body[:300],
                })

        self._triplets.extend(triplets)
        self._rebuild_entity_index()
        return triplets

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        scored = []
        for i, triplet in enumerate(self._triplets):
            text = f"{triplet['subject']} {triplet['relation']} {triplet['object']} {triplet['context']}".lower()
            text_terms = set(text.split())

            overlap = len(query_terms & text_terms)
            if overlap == 0:
                continue

            score = overlap / max(len(query_terms), 1)

            # boost para matches no subject ou object
            if any(t in triplet["subject"].lower() for t in query_terms):
                score += 0.3
            if any(t in triplet["object"].lower() for t in query_terms):
                score += 0.2

            scored.append({
                "content": f"[{triplet['subject']}] --{triplet['relation']}--> [{triplet['object']}]\n{triplet['context']}",
                "law_name": triplet.get("object", "").split(",")[0] if "pertence_a" in triplet["relation"] else self._get_law_from_triplet(triplet),
                "article": triplet["subject"] if triplet["subject"].startswith("Art") else None,
                "score": score,
                "retrieval_method": "knowledge_graph",
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def _get_law_from_triplet(self, triplet: dict) -> str:
        subject = triplet["subject"]
        for t in self._triplets:
            if t["subject"] == subject and t["relation"] == "pertence_a":
                return t["object"]
        obj = triplet.get("object", "")
        if "Lei" in obj or "Resolução" in obj:
            return obj.split(",")[0]
        return "N/A"

    def _rebuild_entity_index(self):
        self._entity_index.clear()
        for i, t in enumerate(self._triplets):
            for entity in [t["subject"].lower(), t["object"].lower()]:
                if entity not in self._entity_index:
                    self._entity_index[entity] = []
                self._entity_index[entity].append(i)

    @property
    def total_triplets(self) -> int:
        return len(self._triplets)


kg_service = LegalKnowledgeGraph()
