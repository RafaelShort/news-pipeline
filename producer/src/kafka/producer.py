import json

from kafka import KafkaProducer
from kafka.errors import KafkaError
from loguru import logger

from src.config import settings
from src.feeds.rss_reader import RawArticle


class NewsProducer:
    def __init__(self):
        self._producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8"),
            acks="all",                  
            retries=3,
            max_block_ms=10_000,
        )
        logger.info(
            f"✅ KafkaProducer conectado | "
            f"topic={settings.kafka_topic_raw} | "
            f"brokers={settings.kafka_bootstrap_servers}"
        )

    def publish(self, article: RawArticle) -> bool:
        try:
            future = self._producer.send(
                topic=settings.kafka_topic_raw,
                key=article.id,
                value=article.model_dump(),
            )
            future.get(timeout=5)
            logger.debug(f"Publicado: {article.title[:60]}...")
            return True

        except KafkaError as e:
            logger.error(f"❌ Erro ao publicar artigo {article.id}: {e}")
            return False

    def flush(self):
        self._producer.flush()

    def close(self):
        self._producer.close()
        logger.info("KafkaProducer encerrado")
