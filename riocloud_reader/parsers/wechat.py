# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
WeChat Parser —微信公众号文章抓取
Two-tier fallback: Jina Reader → Playwright
"""

import logging
from .base import BaseParser, ParseResult, is_wechat_url

logger = logging.getLogger("riocloud_reader.parsers.wechat")


class WeChatParser(BaseParser):
    """Parse WeChat public account articles."""
    
    name = "wechat"
    
    def can_handle(self, url: str) -> bool:
        return is_wechat_url(url)
    
    async def parse(self, url: str) -> ParseResult:
        """Parse a WeChat article URL."""
        
        # Tier 1: Jina Reader
        try:
            data = await self._fetch_via_jina(url)
            if data.get("content"):
                return ParseResult(
                    url=url,
                    title=data.get("title", ""),
                    content=data.get("content", ""),
                    author=data.get("author", ""),
                    tags=["wechat"],
                )
        except Exception as e:
            logger.warning(f"Jina failed: {e}")
        
        # Tier 2: Playwright fallback
        try:
            data = await self._fetch_via_browser(url)
            return ParseResult(
                url=url,
                title=data.get("title", ""),
                content=data.get("content", ""),
                author=data.get("author", ""),
                tags=["wechat"],
            )
        except Exception as e:
            return ParseResult.failure(url, f"All methods failed: {e}")
    
    async def _fetch_via_jina(self, url: str) -> dict:
        """Fetch via Jina Reader."""
        import requests
        
        jina_url = f"https://r.jina.ai/{url}"
        resp = requests.get(jina_url, timeout=30)
        resp.raise_for_status()
        
        text = resp.text
        lines = text.strip().split("\n")
        
        title = ""
        content_lines = []
        
        for line in lines:
            if not title and line.strip():
                title = line.lstrip("#").strip()
            else:
                content_lines.append(line)
        
        return {
            "title": title[:200],
            "content": "\n".join(content_lines).strip(),
            "author": "",
        }
    
    async def _fetch_via_browser(self, url: str) -> dict:
        """Fetch via Playwright headless browser."""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            raise RuntimeError("Playwright not installed")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            page = await context.new_page()
            
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(2000)
            
            title = await page.title()
            
            # Extract content
            content = await page.evaluate("""() => {
                const el = document.querySelector('article') 
                    || document.querySelector('#js_content')
                    || document.querySelector('.rich_media_content')
                    || document.body;
                return el ? el.innerText : '';
            }""")
            
            await browser.close()
            
            return {
                "title": title,
                "content": content.strip(),
                "author": "",
            }
