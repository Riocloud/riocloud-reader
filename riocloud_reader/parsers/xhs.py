# -*- coding: utf-8 -*-
"""
Xiaohongshu Parser — 小红书笔记抓取
Three-tier: Jina → Playwright + session → error
"""

import logging
from pathlib import Path

from .base import BaseParser, ParseResult, is_xhs_url

logger = logging.getLogger("riocloud_reader.parsers.xhs")


SESSION_DIR = Path.home() / ".riocloud-reader" / "sessions"


class XHSParser(BaseParser):
    """Parse Xiaohongshu notes."""
    
    name = "xhs"
    
    def can_handle(self, url: str) -> bool:
        return is_xhs_url(url)
    
    async def parse(self, url: str) -> ParseResult:
        """Parse a Xiaohongshu URL."""
        
        # Tier 1: Jina Reader
        try:
            data = await self._fetch_via_jina(url)
            if data.get("content"):
                return ParseResult(
                    url=url,
                    title=data.get("title", ""),
                    content=data.get("content", ""),
                    author=data.get("author", ""),
                    tags=["xiaohongshu"],
                )
        except Exception as e:
            logger.warning(f"Jina failed: {e}")
        
        # Tier 2: Playwright with session
        session_path = SESSION_DIR / "xhs.json"
        
        if not session_path.exists():
            return ParseResult.failure(
                url,
                "XHS blocked. Run: riocloud-reader login xhs"
            )
        
        try:
            data = await self._fetch_via_browser(url, session_path)
            return ParseResult(
                url=url,
                title=data.get("title", ""),
                content=data.get("content", ""),
                author=data.get("author", ""),
                tags=["xiaohongshu"],
            )
        except Exception as e:
            return ParseResult.failure(url, f"Failed: {e}")
    
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
    
    async def _fetch_via_browser(self, url: str, session_path: Path) -> dict:
        """Fetch via Playwright with saved session."""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            raise RuntimeError("Playwright not installed")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                storage_state=str(session_path)
            )
            page = await context.new_page()
            
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(2000)
            
            title = await page.title()
            
            content = await page.evaluate("""() => {
                const el = document.querySelector('.note-content') 
                    || document.querySelector('#detail-desc')
                    || document.body;
                return el ? el.innerText : '';
            }""")
            
            await browser.close()
            
            return {
                "title": title,
                "content": content.strip(),
                "author": "",
            }


async def login_xhs():
    """Login to Xiaohongshu and save session."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Playwright not installed. Run: pip install playwright")
        return
    
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    session_path = SESSION_DIR / "xhs.json"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        await page.goto("https://www.xiaohongshu.com/explore", wait_until="domcontentloaded")
        print("Please log in manually...")
        print("After logging in, press Enter here...")
        input()
        
        await context.storage_state(path=str(session_path))
        print(f"Session saved to {session_path}")
        
        await browser.close()
