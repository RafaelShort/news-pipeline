from loguru import logger
from transformers import pipeline


class Summarizer:
    """Sumariza textos longos com modelo configurável (DistilBART ou T5)."""

    def __init__(self, model_name: str):
        logger.info(f"🧠 Carregando sumarizador: {model_name}")
        self._model_name = model_name
        self._is_t5 = "t5" in model_name.lower()
        self._summarizer = pipeline(
            "summarization",
            model=model_name,
            device=-1,
        )
        logger.info(f"✅ Sumarizador carregado: {model_name}")

    def summarize(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        if not text or len(text.split()) < 50:
            return text.strip()

        try:
            input_text = f"summarize: {text[:800]}" if self._is_t5 else text[:1024]

            result = self._summarizer(
                input_text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True,   # ← garante truncamento automático
            )
            summary = result[0]["summary_text"]
            logger.debug(f"📝 Resumo gerado: {len(summary)} chars")
            return summary

        except Exception as e:
            logger.error(f"❌ Erro na sumarização: {e}")
            return text[:500]
