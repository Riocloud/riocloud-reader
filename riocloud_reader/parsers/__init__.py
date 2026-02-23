# -*- coding: utf-8 -*-
"""
Parser factory and router.
"""

from .base import BaseParser
from .twitter import TwitterParser
from .reddit import RedditParser
from .youtube import YouTubeParser
from .wechat import WeChatParser
from .xhs import XHSParser
from .bilibili import BilibiliParser
from .rss import RSSParser
from .telegram import TelegramParser
from .generic import GenericParser


# Parser registry
_PARSERS = {
    "twitter": TwitterParser(),
    "reddit": RedditParser(),
    "youtube": YouTubeParser(),
    "wechat": WeChatParser(),
    "xhs": XHSParser(),
    "bilibili": BilibiliParser(),
    "rss": RSSParser(),
    "telegram": TelegramParser(),
    "generic": GenericParser(),
}


def get_parser(platform: str) -> BaseParser:
    """Get parser for a platform."""
    return _PARSERS.get(platform.lower(), _PARSERS["generic"])


def register_parser(platform: str, parser: BaseParser) -> None:
    """Register a custom parser."""
    _PARSERS[platform.lower()] = parser


__all__ = [
    "BaseParser",
    "TwitterParser",
    "RedditParser", 
    "YouTubeParser",
    "WeChatParser",
    "XHSParser",
    "BilibiliParser",
    "RSSParser",
    "TelegramParser",
    "GenericParser",
    "get_parser",
    "register_parser",
]
