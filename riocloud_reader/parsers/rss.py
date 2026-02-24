# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
RSS Parser — feed parsing via feedparser
"""

import logging
import feedparser

from .base import BaseParser, ParseResult

logger = logging.getLogger("riocloud_reader.parsers.rss")


class RSSParser(BaseParser):
    """Parse RSS/Atom feeds."""
    
    name = "rss"
    
    def can_handle(self, url: str) -> bool:
        url_lower = url.lower()
        return any(x in url_lower for x in [".xml", "/rss", "/feed", "/atom", "feedparser"])
    
    async def parse(self, url: str) -> ParseResult:
        """Parse an RSS feed URL."""
        try:
            feed = feedparser.parse(url)
            
            if not feed.entries:
                return ParseResult.failure(url, "No entries in feed")
            
            # Get first entry
            entry = feed.entries[0]
            
            title = entry.get("title", "Untitled")
            
            # Get content
            if hasattr(entry, "content") and entry.content:
                content = entry.content[0].value
            elif hasattr(entry, "summary"):
                content = entry.summary
            else:
                content = ""
            
            # Get link
            link = entry.get("link", url)
            
            # Get author
            author = ""
            if hasattr(entry, "author"):
                author = entry.author
            elif hasattr(entry, "authors") and entry.authors:
                author = entry.authors[0].get("name", "")
            
            # Get feed title
            feed_title = feed.feed.get("title", "RSS Feed")
            
            content = f"""# {title}

**Source:** {feed_title}
**Author:** {author}
**Link:** {link}

---

{content}
"""
            return ParseResult(
                url=link,
                title=title,
                content=content,
                author=author,
                tags=["rss", "feed"],
            )
            
        except Exception as e:
            return ParseResult.failure(url, f"Failed: {e}")
