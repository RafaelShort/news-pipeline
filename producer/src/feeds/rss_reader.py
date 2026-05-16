import hashlib
from datetime import datetime, timezone
from typing import Generator

import feedparser
from loguru import logger
from pydantic import BaseModel


class RawArticle(BaseModel):
    id: str
    title: str
    url: str
    content: str
    summary: str
    published_at: str
    source_name: str
    source_url: str
    language: str
    category: str
    fetched_at: str


def _generate_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()


def _parse_date(entry: feedparser.FeedParserDict) -> str:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        return dt.isoformat()
    return datetime.now(timezone.utc).isoformat()


def _extract_content(entry: feedparser.FeedParserDict) -> str:
    if hasattr(entry, "content") and entry.content:
        return entry.content[0].get("value", "")
    if hasattr(entry, "summary"):
        return entry.summary
    return ""


def fetch_feed(source: dict) -> Generator[RawArticle, None, None]:
    """Lê um feed RSS e gera RawArticles."""
    url = source["url"]
    logger.info(f"📡 Lendo feed: {source['name']} | {url}")

    try:
        feed = feedparser.parse(url)

        if feed.bozo and not feed.entries:
            logger.warning(f"⚠️ Feed malformado ou vazio: {url}")
            return

        logger.info(f"✅ {len(feed.entries)} artigos encontrados em {source['name']}")

        for entry in feed.entries:
            link = getattr(entry, "link", None)
            title = getattr(entry, "title", "")

            if not link or not title:
                continue

            content = _extract_content(entry)
            summary = getattr(entry, "summary", content[:500])

            yield RawArticle(
                id=_generate_id(link),
                title=title,
                url=link,
                content=content,
                summary=summary,
                published_at=_parse_date(entry),
                source_name=source["name"],
                source_url=url,
                language=source["language"],
                category=source["category"],
                fetched_at=datetime.now(timezone.utc).isoformat(),
            )

    except Exception as e:
        logger.error(f"❌ Erro ao ler feed {url}: {e}")
