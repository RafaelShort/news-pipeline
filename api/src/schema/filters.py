from typing import Optional
import strawberry


@strawberry.input
class SearchFilters:
    query: Optional[str] = None
    topic: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None
    source_name: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    page: int = 1
    page_size: int = 10
