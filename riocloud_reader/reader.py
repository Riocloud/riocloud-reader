# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
Riocloud Reader — Universal content reader that combines x-reader and DeepReader.
"""

import asyncio
import logging
from urllib.parse import urlparse
from typing import Optional, List

from .schema import UnifiedContent, UnifiedInbox
from .parsers import get_parser

logger = logging.getLogger("riocloud_reader")


class Reader:
    """
    Universal content reader.
    
    Routes URLs to platform-specific parsers and returns unified content.
    """

    def __init__(self, inbox: Optional[UnifiedInbox] = None):
        self.inbox = inbox

    def _detect_platform(self, url: str) -> str:
        """Detect platform from URL."""
        domain = urlparse(url).netloc.lower().replace("www.", "")
        
        # Twitter/X
        if "x.com" in domain or "twitter.com" in domain:
            return "twitter"
        
        # Reddit
        if "reddit.com" in domain or "old.reddit.com" in domain:
            return "reddit"
        
        # YouTube
        if "youtube.com" in domain or "youtu.be" in domain:
            return "youtube"
        
        # WeChat
        if "mp.weixin.qq.com" in domain:
            return "wechat"
        
        # Xiaohongshu
        if "xiaohongshu.com" in domain or "xhslink.com" in domain:
            return "xhs"
        
        # Bilibili
        if "bilibili.com" in domain or "b23.tv" in domain:
            return "bilibili"
        
        # Telegram
        if "t.me" in domain or "telegram.org" in domain:
            return "telegram"
        
        # RSS
        if url.endswith(".xml") or "/rss" in url or "/feed" in url or "/atom" in url:
            return "rss"
        
        # Default to generic
        return "generic"

    async def read(self, url: str) -> UnifiedContent:
        """
        Fetch content from any URL and return as UnifiedContent.
        
        Args:
            url: The URL to fetch and parse.
            
        Returns:
            UnifiedContent object with the parsed content.
        """
        # Ensure URL has scheme
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        platform = self._detect_platform(url)
        logger.info(f"[{platform}] Fetching: {url[:60]}...")

        try:
            # Get the appropriate parser
            parser = get_parser(platform)
            
            # Parse the URL
            result = await parser.parse(url)
            
            # Convert ParseResult to UnifiedContent
            content = UnifiedContent(
                source_type=platform,
                source_name=result.author or urlparse(url).netloc,
                title=result.title,
                content=result.content,
                url=url,
                author=result.author,
                tags=result.tags,
                excerpt=result.excerpt,
            )
            
            # Save to inbox if configured
            if self.inbox:
                if self.inbox.add(content):
                    self.inbox.save()
                    logger.info(f"Saved to inbox: {content.title[:50]}")

            return content

        except Exception as e:
            logger.error(f"[{platform}] Failed: {e}")
            raise

    async def read_batch(self, urls: List[str]) -> List[UnifiedContent]:
        """Fetch multiple URLs concurrently."""
        tasks = [self.read(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        contents = []
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                logger.error(f"Batch failed for {url}: {result}")
            else:
                contents.append(result)

        return contents


# Convenience function for synchronous usage
def read_sync(url: str) -> UnifiedContent:
    """Synchronous wrapper for Reader.read()."""
    return asyncio.run(Reader().read(url))
