from loguru import logger
from transformers import pipeline


TOPICS = [
    "política",
    "economia",
    "tecnologia",
    "saúde",
    "esportes",
    "entretenimento",
    "ciência",
    "educação",
    "segurança",
    "meio ambiente",
    "mundo",
]


class TopicClassifier:
    """Classifica o tópico principal do artigo via zero-shot."""

    def __init__(self, model_name: str):
        logger.info(f"🧠 Carregando classificador: {model_name}")
        self._classifier = pipeline(
            "zero-shot-classification",
            model=model_name,
            device=-1,          # CPU; troque para 0 se tiver GPU
        )
        logger.info(f"✅ Classificador carregado: {model_name}")

    def classify(self, text: str, top_k: int = 3) -> list[dict]:
        if not text or not text.strip():
            return []

        try:
            result = self._classifier(
                text[:1024],    # limita tokens
                candidate_labels=TOPICS,
                multi_label=False,
            )

            topics = [
                {"topic": label, "score": round(score, 4)}
                for label, score in zip(
                    result["labels"][:top_k],
                    result["scores"][:top_k],
                )
            ]

            logger.debug(f"🏷️ Tópico principal: {topics[0]['topic']} ({topics[0]['score']})")
            return topics

        except Exception as e:
            logger.error(f"❌ Erro na classificação: {e}")
            return []
