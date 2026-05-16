from typing import Optional

import strawberry
from loguru import logger

from src.schema.filters import SearchFilters
from src.schema.types import (
    Article,
    Entity,
    FacetBucket,
    Facets,
    SearchResult,
    Stats,
    Topic,
)
from src.storage.elastic import ElasticSearch

es = ElasticSearch()


def _parse_article(source: dict) -> Article:
    return Article(
        id=source.get("id", ""),
        title=source.get("title", ""),
        url=source.get("url", ""),
        content=source.get("content", ""),
        summary=source.get("summary", ""),
        summary_generated=source.get("summary_generated", ""),
        published_at=source.get("published_at", ""),
        fetched_at=source.get("fetched_at", ""),
        processed_at=source.get("processed_at", ""),
        source_name=source.get("source_name", ""),
        source_url=source.get("source_url", ""),
        language=source.get("language", ""),
        category=source.get("category", ""),
        topic_main=source.get("topic_main", ""),
        word_count=source.get("word_count", 0),
        entities=[
            Entity(
                text=e.get("text", ""),
                label=e.get("label", ""),
                label_pt=e.get("label_pt", ""),
            )
            for e in source.get("entities", [])
        ],
        topics=[
            Topic(
                topic=t.get("topic", ""),
                score=t.get("score", 0.0),
            )
            for t in source.get("topics", [])
        ],
    )


def _parse_facets(aggs: dict) -> Facets:
    def buckets(agg_key: str) -> list[FacetBucket]:
        return [
            FacetBucket(key=b["key"], count=b["doc_count"])
            for b in aggs.get(agg_key, {}).get("buckets", [])
        ]

    return Facets(
        topics=buckets("by_topic"),
        categories=buckets("by_category"),
        sources=buckets("by_source"),
        languages=buckets("by_language"),
    )


@strawberry.type
class Query:

    @strawberry.field
    def search(self, filters: SearchFilters) -> SearchResult:
        logger.info(
            f"🔍 Search | query={filters.query} | "
            f"topic={filters.topic} | page={filters.page}"
        )

        response = es.search(
            query=filters.query,
            topic=filters.topic,
            category=filters.category,
            language=filters.language,
            source_name=filters.source_name,
            from_date=filters.from_date,
            to_date=filters.to_date,
            page=filters.page,
            page_size=filters.page_size,
        )

        hits = response["hits"]
        articles = [_parse_article(h["_source"]) for h in hits["hits"]]
        total = hits["total"]["value"]
        facets = _parse_facets(response.get("aggregations", {}))

        return SearchResult(
            articles=articles,
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            facets=facets,
        )

    @strawberry.field
    def article(self, id: str) -> Optional[Article]:
        logger.info(f"🔍 Article by ID: {id}")
        source = es.get_by_id(id)
        if not source:
            return None
        return _parse_article(source)

    @strawberry.field
    def stats(self) -> Stats:
        data = es.get_stats()
        return Stats(total_articles=data["total_articles"])
