from typing import Optional
import strawberry


@strawberry.type
class Entity:
    text: str
    label: str
    label_pt: str


@strawberry.type
class Topic:
    topic: str
    score: float


@strawberry.type
class Article:
    id: str
    title: str
    url: str
    content: str
    summary: str
    summary_generated: str
    published_at: str
    fetched_at: str
    processed_at: str
    source_name: str
    source_url: str
    language: str
    category: str
    topic_main: str
    word_count: int
    entities: list[Entity]
    topics: list[Topic]


@strawberry.type
class FacetBucket:
    key: str
    count: int


@strawberry.type
class Facets:
    topics: list[FacetBucket]
    categories: list[FacetBucket]
    sources: list[FacetBucket]
    languages: list[FacetBucket]


@strawberry.type
class SearchResult:
    articles: list[Article]
    total: int
    page: int
    page_size: int
    facets: Facets


@strawberry.type
class Stats:
    total_articles: int
