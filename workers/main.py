import signal
import sys

from loguru import logger

from src.kafka.consumer import NewsConsumer
from src.nlp.pipeline import NLPPipeline
from src.storage.elastic import ElasticStorage

# ── Logging ──────────────────────────────────────────────────
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
    level="DEBUG",
)

consumer: NewsConsumer | None = None


def shutdown(sig, frame):
    logger.info("🛑 Encerrando worker...")
    if consumer:
        consumer.close()
    sys.exit(0)


def main():
    global consumer

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logger.info("🚀 NLP Worker iniciado")

    pipeline = NLPPipeline()
    storage = ElasticStorage()
    consumer = NewsConsumer()

    processed = 0
    errors = 0

    for raw_article in consumer.consume():
        try:
            processed_article = pipeline.process(raw_article)
            saved = storage.save(processed_article.model_dump())

            if saved:
                processed += 1
                logger.info(
                    f"✅ [{processed}] {processed_article.title[:50]}... "
                    f"| topic={processed_article.topic_main}"
                )
            else:
                errors += 1

        except Exception as e:
            errors += 1
            logger.error(f"❌ Erro ao processar artigo: {e}")


if __name__ == "__main__":
    main()
