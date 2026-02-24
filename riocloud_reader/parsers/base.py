# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
Base parser interface.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import logging
import re
from urllib.parse import urlparse

logger = logging.getLogger("riocloud_reader.parsers")


@dataclass
class ParseResult:
    """Structured output from a parser."""
    
    url: str
    title: str = ""
    content: str = ""
    author: str = ""
    excerpt: str = ""
    tags: list[str] = field(default_factory=list)
    success: bool = True
    error: str = ""
    
    @classmethod
    def failure(cls, url: str, error: str) -> "ParseResult":
        return cls(url=url, success=False, error=error)


class BaseParser(ABC):
    """Abstract base class for all content parsers."""
    
    name: str = "base"
    timeout: int = 30
    max_response_size: int = 10 * 1024 * 1024  # 10MB max response size
    max_content_length: int = 2 * 1024 * 1024  # 2MB max content length
    
    user_agent: str = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    
    def can_handle(self, url: str) -> bool:
        """Check if this parser can handle the URL."""
        return True
    
    @abstractmethod
    async def parse(self, url: str) -> ParseResult:
        """Fetch and parse the content."""
        ...
    
    def _get_headers(self) -> dict:
        """Return default HTTP headers."""
        return {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        return urlparse(url).netloc.lower()


# URL pattern matchers
def is_twitter_url(url: str) -> bool:
    """Check if URL is a Twitter/X URL."""
    return bool(re.search(r"(x\.com|twitter\.com)/[a-zA-Z0-9_]+/status/\d+", url))

def is_reddit_url(url: str) -> bool:
    """Check if URL is a Reddit URL."""
    return "reddit.com" in url.lower() and "/comments/" in url

def is_youtube_url(url: str) -> bool:
    """Check if URL is a YouTube URL."""
    return bool(re.search(r"(youtube\.com|youtu\.be)", url))

def is_wechat_url(url: str) -> bool:
    """Check if URL is a WeChat article URL."""
    return "mp.weixin.qq.com" in url

def is_xhs_url(url: str) -> bool:
    """Check if URL is a Xiaohongshu URL."""
    return bool(re.search(r"(xiaohongshu\.com|xhslink\.com)", url))

def is_bilibili_url(url: str) -> bool:
    """Check if URL is a Bilibili URL."""
    return bool(re.search(r"(bilibili\.com|b23\.tv)", url))

def extract_youtube_video_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    patterns = [
        r'(?:youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return ""


__all__ = [
    "ParseResult",
    "BaseParser",
    "is_twitter_url",
    "is_reddit_url", 
    "is_youtube_url",
    "is_wechat_url",
    "is_xhs_url",
    "is_bilibili_url",
    "extract_youtube_video_id",
]
