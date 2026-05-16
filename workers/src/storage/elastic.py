from elasticsearch import Elasticsearch, helpers
from loguru import logger

from src.config import settings


INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "id":                 {"type": "keyword"},
            "title":              {"type": "text", "analyzer": "standard"},
            "url":                {"type": "keyword"},
            "content":            {"type": "text", "analyzer": "standard"},
            "summary":            {"type": "text"},
            "summary_generated":  {"type": "text"},
            "published_at":       {"type": "date"},
            "fetched_at":         {"type": "date"},
            "processed_at":       {"type": "date"},
            "source_name":        {"type": "keyword"},
            "source_url":         {"type": "keyword"},
            "language":           {"type": "keyword"},
            "category":           {"type": "keyword"},
            "topic_main":         {"type": "keyword"},
            "word_count":         {"type": "integer"},
            "entities": {
                "type": "nested",
                "properties": {
                    "text":     {"type": "keyword"},
                    "label":    {"type": "keyword"},
                    "label_pt": {"type": "keyword"},
                },
            },
            "topics": {
                "type": "nested",
                "properties": {
                    "topic": {"type": "keyword"},
                    "score": {"type": "float"},
                },
            },
        }
    },
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
    },
}


class ElasticStorage:
    def __init__(self):
        self._es = Elasticsearch(settings.elasticsearch_uri)
        self._index = settings.elasticsearch_index
        self._ensure_index()
        logger.info(
            f"✅ ElasticSearch conectado | "
            f"index={self._index} | "
            f"uri={settings.elasticsearch_uri}"
        )

    def _ensure_index(self):
        if not self._es.indices.exists(index=self._index):
            self._es.indices.create(index=self._index, body=INDEX_MAPPING)
            logger.info(f"📁 Índice criado: {self._index}")
        else:
            logger.debug(f"📁 Índice já existe: {self._index}")

    def save(self, article: dict) -> bool:
        try:
            self._es.index(
                index=self._index,
                id=article["id"],
                document=article,
            )
            logger.debug(f"💾 Salvo no ES: {article['title'][:60]}...")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao salvar no ES: {e}")
            return False
