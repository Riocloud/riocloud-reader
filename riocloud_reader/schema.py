# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
Unified content schema for Riocloud Reader.

Defines the standard data format for all content sources.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum
import hashlib
import json


class SourceType(str, Enum):
    """Content source types."""
    TELEGRAM = "telegram"
    RSS = "rss"
    BILIBILI = "bilibili"
    XIAOHONGSHU = "xhs"
    TWITTER = "twitter"
    WECHAT = "wechat"
    YOUTUBE = "youtube"
    REDDIT = "reddit"
    GENERIC = "generic"
    MANUAL = "manual"


class MediaType(str, Enum):
    """Media types."""
    TEXT = "text"
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"


class Priority(str, Enum):
    """Content priority levels."""
    HOT = "hot"
    QUALITY = "quality"
    DEEP = "deep"
    NORMAL = "normal"
    LOW = "low"


@dataclass
class UnifiedContent:
    """Unified content format across all platforms."""

    # === Required ===
    source_type: SourceType
    source_name: str
    title: str
    content: str
    url: str

    # === Auto-generated ===
    id: str = ""
    fetched_at: str = ""

    # === Media ===
    media_type: MediaType = MediaType.TEXT
    media_url: Optional[str] = None

    # === Engagement ===
    likes: int = 0
    retweets: int = 0
    views: int = 0
    comments: int = 0

    # === Metadata ===
    author: str = ""
    tags: List[str] = field(default_factory=list)
    excerpt: str = ""
    word_count: int = 0

    # === Processing state ===
    processed: bool = False

    def __post_init__(self):
        if not self.id:
            self.id = hashlib.md5(self.url.encode()).hexdigest()[:12]
        if not self.fetched_at:
            self.fetched_at = datetime.now().isoformat()
        if not self.excerpt and self.content:
            self.excerpt = self.content[:200] + "..." if len(self.content) > 200 else self.content
        if not self.word_count:
            self.word_count = len(self.content.split())

    def to_dict(self) -> dict:
        d = asdict(self)
        d['source_type'] = self.source_type.value
        d['media_type'] = self.media_type.value
        return d

    @classmethod
    def from_dict(cls, data: dict) -> 'UnifiedContent':
        if isinstance(data.get('source_type'), str):
            data['source_type'] = SourceType(data['source_type'])
        if isinstance(data.get('media_type'), str):
            data['media_type'] = MediaType(data['media_type'])
        known = {f.name for f in cls.__dataclass_fields__.values()}
        data = {k: v for k, v in data.items() if k in known}
        return cls(**data)

    def to_markdown(self) -> str:
        """Convert to Markdown with YAML frontmatter."""
        frontmatter = f"""---
title: "{self.title}"
source_url: {self.url}
domain: {self.url.split('/')[2] if '//' in self.url else 'unknown'}
parser: {self.source_type.value}
ingested_at: {self.fetched_at}
content_hash: sha256:{hashlib.sha256(self.content.encode()).hexdigest()[:16]}...
word_count: {self.word_count}
---

# {self.title}

"""
        return frontmatter + self.content


class UnifiedInbox:
    """JSON-based content inbox with dedup."""

    def __init__(self, filepath: str = "inbox.json"):
        self.filepath = filepath
        self.items: List[UnifiedContent] = []
        self.load()

    def load(self):
        import os
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.items = [UnifiedContent.from_dict(d) for d in data]
            except (json.JSONDecodeError, IOError):
                self.items = []

    def save(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([item.to_dict() for item in self.items], f,
                      ensure_ascii=False, indent=2)

    def add(self, item: UnifiedContent) -> bool:
        if any(i.id == item.id for i in self.items):
            return False
        self.items.append(item)
        return True

    def get_by_source(self, source_type: SourceType) -> List[UnifiedContent]:
        return [i for i in self.items if i.source_type == source_type]
