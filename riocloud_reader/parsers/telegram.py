# -*- coding: utf-8 -*-
"""
Telegram Parser — channel messages via Telethon
"""

import logging
from urllib.parse import urlparse

from .base import BaseParser, ParseResult

logger = logging.getLogger("riocloud_reader.parsers.telegram")


class TelegramParser(BaseParser):
    """Parse Telegram channel messages."""
    
    name = "telegram"
    
    def can_handle(self, url: str) -> bool:
        return "t.me" in url or "telegram.org" in url
    
    async def parse(self, url: str) -> ParseResult:
        """Parse a Telegram channel URL."""
        # Extract channel username from URL
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        
        # Handle /s/ posts or direct channel names
        if path.startswith("s/"):
            # It's a post link, need channel info
            return ParseResult.failure(
                url,
                "Post links require API access. Use channel username instead."
            )
        
        channel = path.split("/")[0]
        
        try:
            from telethon import TelegramClient
            
            # This would require API credentials
            # For now, return a placeholder
            return ParseResult(
                url=url,
                title=f"Telegram: {channel}",
                content=f"Telegram channel: {channel}\n\nNote: Full Telegram integration requires API credentials.\nSet TG_API_ID and TG_API_HASH environment variables.",
                author=channel,
                tags=["telegram"],
            )
            
        except ImportError:
            return ParseResult.failure(
                url,
                "Telethon not installed. Run: pip install riocloud-reader[telegram]"
            )
        except Exception as e:
            return ParseResult.failure(url, f"Failed: {e}")
