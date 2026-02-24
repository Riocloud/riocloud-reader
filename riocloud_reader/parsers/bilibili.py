# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
Bilibili Parser — B站视频解析
"""

import logging
import requests
import re

from .base import BaseParser, ParseResult, is_bilibili_url

logger = logging.getLogger("riocloud_reader.parsers.bilibili")


class BilibiliParser(BaseParser):
    """Parse Bilibili videos."""
    
    name = "bilibili"
    
    def can_handle(self, url: str) -> bool:
        return is_bilibili_url(url)
    
    async def parse(self, url: str) -> ParseResult:
        """Parse a Bilibili URL."""
        bvid = self._extract_bvid(url)
        if not bvid:
            return ParseResult.failure(url, "Invalid Bilibili URL")
        
        try:
            # Get video info via API
            api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
            resp = requests.get(api_url, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            
            if data.get("code") != 0:
                return ParseResult.failure(url, f"API error: {data.get('message')}")
            
            info = data.get("data", {})
            
            title = info.get("title", "")
            author = info.get("owner", {}).get("name", "")
            description = info.get("desc", "")
            duration = info.get("duration", 0)
            view_count = info.get("stat", {}).get("view", 0)
            
            # Format duration
            minutes = duration // 60
            seconds = duration % 60
            duration_str = f"{minutes}:{seconds:02d}"
            
            content = f"""# {title}

**Author:** {author}
**Duration:** {duration_str}
**Views:** {view_count:,}

---

{description}
"""
            return ParseResult(
                url=url,
                title=title,
                content=content,
                author=author,
                tags=["bilibili", "video"],
            )
            
        except Exception as e:
            return ParseResult.failure(url, f"Failed: {e}")
    
    def _extract_bvid(self, url: str) -> str:
        """Extract BVID from URL."""
        match = re.search(r'/(BV[a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        
        # Handle short URLs
        match = re.search(r'b23\.tv/([a-zA-Z0-9]+)', url)
        if match:
            # Need to resolve short URL
            try:
                resp = requests.head(f"https://{match.group(0)}", timeout=10, allow_redirects=True)
                url = resp.url
                match = re.search(r'/(BV[a-zA-Z0-9]+)', url)
                if match:
                    return match.group(1)
            except:
                pass
        
        return ""
