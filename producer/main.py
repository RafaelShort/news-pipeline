import signal
import sys
import time

import schedule
from loguru import logger

from src.config import settings
from src.feeds.rss_reader import fetch_feed
from src.feeds.sources import RSS_SOURCES
from src.kafka.producer import NewsProducer

# Logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
    level="DEBUG",
)

producer: NewsProducer | None = None


def fetch_and_publish():
    """Lê todos os feeds RSS e publica no Kafka."""
    logger.info("Iniciando ciclo de coleta de feeds...")
    total_published = 0
    total_errors = 0

    for source in RSS_SOURCES:
        for article in fetch_feed(source):
            success = producer.publish(article)
            if success:
                total_published += 1
            else:
                total_errors += 1

    producer.flush()
    logger.info(
        f"✅ Ciclo concluído | "
        f"publicados={total_published} | "
        f"erros={total_errors}"
    )


def shutdown(sig, frame):
    logger.info("🛑 Encerrando producer...")
    if producer:
        producer.close()
    sys.exit(0)


def main():
    global producer

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logger.info("News Producer iniciado")
    producer = NewsProducer()

    # Primeira execução imediata
    fetch_and_publish()

    # Agendar execuções periódicas
    interval = settings.rss_fetch_interval
    schedule.every(interval).seconds.do(fetch_and_publish)
    logger.info(f"⏱️ Agendado para rodar a cada {interval}s")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
