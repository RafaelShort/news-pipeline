from typing import Any

from elasticsearch import Elasticsearch
from loguru import logger

from src.config import settings


class ElasticSearch:
    def __init__(self):
        self._es = Elasticsearch(settings.elasticsearch_uri)
        self._index = settings.elasticsearch_index
        logger.info(
            f"✅ ElasticSearch conectado | "
            f"index={self._index}"
        )

    def search(
        self,
        query: str | None = None,
        topic: str | None = None,
        category: str | None = None,
        language: str | None = None,
        source_name: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> dict[str, Any]:
        must = []
        filters = []

        # ── Full-text search ──────────────────────────────────
        if query:
            must.append({
                "multi_match": {
                    "query": query,
                    "fields": ["title^3", "content", "summary_generated"],
                    "fuzziness": "AUTO",
                }
            })

        # ── Filtros exatos ────────────────────────────────────
        if topic:
            filters.append({"term": {"topic_main": topic}})
        if category:
            filters.append({"term": {"category": category}})
        if language:
            filters.append({"term": {"language": language}})
        if source_name:
            filters.append({"term": {"source_name": source_name}})

        # ── Filtro por data ───────────────────────────────────
        if from_date or to_date:
            date_range: dict[str, Any] = {}
            if from_date:
                date_range["gte"] = from_date
            if to_date:
                date_range["lte"] = to_date
            filters.append({"range": {"published_at": date_range}})

        body = {
            "query": {
                "bool": {
                    "must": must if must else [{"match_all": {}}],
                    "filter": filters,
                }
            },
            "sort": [{"published_at": {"order": "desc"}}],
            "from": (page - 1) * page_size,
            "size": page_size,
            # ── Agregações para faceted search ────────────────
            "aggs": {
                "by_topic": {
                    "terms": {"field": "topic_main", "size": 10}
                },
                "by_category": {
                    "terms": {"field": "category", "size": 10}
                },
                "by_source": {
                    "terms": {"field": "source_name", "size": 10}
                },
                "by_language": {
                    "terms": {"field": "language", "size": 5}
                },
            },
        }

        response = self._es.search(index=self._index, body=body)
        return response

    def get_by_id(self, article_id: str) -> dict[str, Any] | None:
        try:
            result = self._es.get(index=self._index, id=article_id)
            return result["_source"]
        except Exception:
            return None

    def get_stats(self) -> dict[str, Any]:
        count = self._es.count(index=self._index)
        return {"total_articles": count["count"]}
