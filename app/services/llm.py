import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from loguru import logger

from app.config import settings

SYSTEM_PROMPT = """Você é o EcoLex, um assistente jurídico-ambiental especializado em legislação brasileira.

REGRAS OBRIGATÓRIAS:
1. Responda EXCLUSIVAMENTE com base nos trechos de legislação fornecidos no contexto.
2. SEMPRE cite a fonte exata: nome da lei, artigo, parágrafo e inciso.
3. Se o contexto não contiver informação suficiente, diga explicitamente: "Não encontrei fundamentação legal nos documentos disponíveis para esta consulta."
4. Use linguagem técnica mas acessível a gestores públicos.
5. Estruture a resposta em: FUNDAMENTAÇÃO LEGAL → ANÁLISE → CONCLUSÃO.
6. NUNCA invente artigos, parágrafos ou leis que não estejam no contexto."""

QUERY_TEMPLATE = """<CONTEXTO LEGISLATIVO>
{context}
</CONTEXTO LEGISLATIVO>

<PERGUNTA>
{question}
</PERGUNTA>

Responda citando os artigos e parágrafos exatos da legislação fornecida no contexto."""


class LLMService:
    def __init__(self):
        self._pipeline = None
        self._tokenizer = None

    def load(self):
        dtype_map = {
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
            "float32": torch.float32,
        }
        torch_dtype = dtype_map.get(settings.torch_dtype, torch.float16)

        logger.info(f"Carregando LLM: {settings.model_name} ({settings.torch_dtype})")

        self._tokenizer = AutoTokenizer.from_pretrained(
            settings.model_name, trust_remote_code=True
        )

        model = AutoModelForCausalLM.from_pretrained(
            settings.model_name,
            torch_dtype=torch_dtype,
            device_map="auto",
            trust_remote_code=True,
        )

        self._pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=self._tokenizer,
            torch_dtype=torch_dtype,
            device_map="auto",
        )

        logger.info("LLM carregado com sucesso")

    def generate(self, question: str, context_chunks: list[dict], max_context_tokens: int = 3000) -> str:
        # Limitar contexto para caber na VRAM (24GB RTX 5090)
        chunks_text = []
        total_tokens = 0
        for c in context_chunks:
            chunk_str = f"[{c.get('law_name', 'N/A')} | {c.get('article', 'N/A')}]\n{c['content'][:800]}"
            est_tokens = len(chunk_str.split()) * 1.3
            if total_tokens + est_tokens > max_context_tokens:
                break
            chunks_text.append(chunk_str)
            total_tokens += est_tokens

        context = "\n\n---\n\n".join(chunks_text)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": QUERY_TEMPLATE.format(
                    context=context, question=question
                ),
            },
        ]

        prompt = self._tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        output = self._pipeline(
            prompt,
            max_new_tokens=settings.max_new_tokens,
            temperature=settings.temperature,
            do_sample=settings.temperature > 0,
            return_full_text=False,
        )

        return output[0]["generated_text"].strip()

    def rewrite_query(self, question: str, n_rewrites: int) -> list[str]:
        if n_rewrites == 0:
            return []

        messages = [
            {
                "role": "system",
                "content": "Você é um especialista em reformulação de consultas jurídico-ambientais. "
                "Gere variações da pergunta para melhorar a busca em bases de legislação.",
            },
            {
                "role": "user",
                "content": f"Gere exatamente {n_rewrites} reformulação(ões) da seguinte pergunta. "
                f"Retorne APENAS as reformulações, uma por linha, sem numeração.\n\n"
                f"Pergunta original: {question}",
            },
        ]

        prompt = self._tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        output = self._pipeline(
            prompt,
            max_new_tokens=256,
            temperature=0.3,
            do_sample=True,
            return_full_text=False,
        )

        text = output[0]["generated_text"].strip()
        rewrites = [line.strip() for line in text.split("\n") if line.strip()]
        return rewrites[:n_rewrites]

    @property
    def is_loaded(self) -> bool:
        return self._pipeline is not None


llm_service = LLMService()
