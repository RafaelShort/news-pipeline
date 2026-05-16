from datetime import datetime, timezone
from typing import Any

from loguru import logger
from pydantic import BaseModel

from src.config import settings
from src.nlp.classifier import TopicClassifier
from src.nlp.ner import NERExtractor
from src.nlp.summarizer import Summarizer


class ProcessedArticle(BaseModel):
    id: str
    title: str
    url: str
    content: str
    summary: str
    summary_generated: str
    published_at: str
    source_name: str
    source_url: str
    language: str
    category: str
    fetched_at: str
    processed_at: str
    entities: list[dict[str, Any]]
    topics: list[dict[str, Any]]
    topic_main: str
    word_count: int


class NLPPipeline:
    """Orquestra todos os modelos NLP."""

    def __init__(self):
        logger.info("⚙️ Inicializando NLP Pipeline...")
        self._ner = NERExtractor(settings.nlp_model_ner)
        self._classifier = TopicClassifier(settings.nlp_model_classifier)
        self._summarizer = Summarizer(settings.nlp_model_summarizer)
        logger.info("✅ NLP Pipeline pronto")

    def process(self, raw: dict) -> ProcessedArticle:
        logger.info(f"⚙️ Processando: {raw['title'][:60]}...")

        text = raw.get("content") or raw.get("summary", "")
        language = raw.get("language", "pt")

        # 1. NER
        entities = self._ner.extract(text, language)

        # 2. Classificação de tópicos
        topics = self._classifier.classify(raw["title"] + " " + text[:512])
        topic_main = topics[0]["topic"] if topics else raw.get("category", "geral")

        # 3. Sumarização
        summary_generated = self._summarizer.summarize(text)

        article = ProcessedArticle(
            id=raw["id"],
            title=raw["title"],
            url=raw["url"],
            content=text,
            summary=raw.get("summary", ""),
            summary_generated=summary_generated,
            published_at=raw["published_at"],
            source_name=raw["source_name"],
            source_url=raw["source_url"],
            language=language,
            category=raw.get("category", "geral"),
            fetched_at=raw["fetched_at"],
            processed_at=datetime.now(timezone.utc).isoformat(),
            entities=entities,
            topics=topics,
            topic_main=topic_main,
            word_count=len(text.split()),
        )

        logger.info(
            f"✅ Processado | "
            f"topic={topic_main} | "
            f"entities={len(entities)} | "
            f"words={article.word_count}"
        )
        return article
