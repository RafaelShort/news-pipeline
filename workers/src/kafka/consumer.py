import json

from kafka import KafkaConsumer
from kafka.errors import KafkaError
from loguru import logger

from src.config import settings


class NewsConsumer:
    def __init__(self):
        self._consumer = KafkaConsumer(
            settings.kafka_topic_raw,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id=settings.kafka_group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=False,   # commit manual após processamento
            max_poll_records=10,
        )
        logger.info(
            f"✅ KafkaConsumer conectado | "
            f"topic={settings.kafka_topic_raw} | "
            f"group={settings.kafka_group_id}"
        )

    def consume(self):
        """Gera mensagens do Kafka indefinidamente."""
        logger.info("👂 Aguardando mensagens...")
        try:
            for message in self._consumer:
                yield message.value
                self._consumer.commit()
        except KafkaError as e:
            logger.error(f"❌ Erro no consumer: {e}")
            raise

    def close(self):
        self._consumer.close()
        logger.info("🔌 KafkaConsumer encerrado")
