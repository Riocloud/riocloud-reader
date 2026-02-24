# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
Xiaohongshu Parser — 小红书笔记抓取
Three-tier: Jina → Playwright + session → error
"""

import asyncio
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
        """Parse a Xiaohongshu URL.
        
        Fixed: Add xsec_token warning and session expiry detection.
        Based on x-reader: https://github.com/runesleo/x-reader/commit/36c1ae5
        """
        
        # Check for xsec_token - warn if missing
        if "xsec_token" not in url and "xiaohongshu.com/explore/" in url:
            logger.warning("[XHS] URL missing xsec_token, likely to get 404")
        
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
        """Fetch via Playwright with saved session.
        
        Fixed: Use XHS-specific selectors (#detail-title, #detail-desc, .bottom-container)
        instead of generic .content which hits comment divs.
        Based on x-reader: https://github.com/runesleo/x-reader/commit/36c1ae5
        """
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            raise RuntimeError("Playwright not installed. Run: pip install playwright")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                storage_state=str(session_path)
            )
            page = await context.new_page()
            
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # XHS SPA needs the note container to render
            try:
                await page.wait_for_selector("#noteContainer", timeout=8000)
            except Exception:
                logger.warning("[XHS] #noteContainer not found within 8s, proceeding anyway")
            await page.wait_for_timeout(1000)
            
            # XHS-specific selectors to avoid comment content mixing with main content
            data = await page.evaluate("""() => {
                const title = document.querySelector('#detail-title');
                const desc = document.querySelector('#detail-desc');
                const meta = document.querySelector('.bottom-container');
                const author = document.querySelector('.author-wrapper .username')
                    || document.querySelector('.interaction-container');
                return {
                    title: title ? title.innerText.trim() : '',
                    content: [
                        desc ? desc.innerText.trim() : '',
                        meta ? meta.innerText.trim() : '',
                    ].filter(Boolean).join('\\n\\n'),
                    author: author ? author.innerText.trim().split('\\n')[0] : '',
                };
            }""")
            
            await browser.close()
            
            # Session expiry detection: XHS redirects to /explore or login page
            final_url = page.url
            if final_url != url:
                if final_url.rstrip("/").endswith("/explore") or "login" in final_url:
                    raise RuntimeError(
                        f"XHS session expired (redirected to {final_url}). "
                        "Run: riocloud-reader login xhs"
                    )
            
            return {
                "title": data.get("title", ""),
                "content": data.get("content", ""),
                "author": data.get("author", ""),
            }


async def login_xhs(headless: bool = False):
    """Login to Xiaohongshu and save session.
    
    Fixed: Add headless mode with QR screenshot + cookie polling.
    Based on x-reader: https://github.com/runesleo/x-reader/commit/36c1ae5
    """
    import os
    import time
    
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Playwright not installed. Run: pip install playwright")
        return
    
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    session_path = SESSION_DIR / "xhs.json"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        await page.goto("https://www.xiaohongshu.com/explore", wait_until="domcontentloaded")
        
        if headless:
            # Headless: save QR screenshot for scanning
            qr_path = SESSION_DIR / "xhs_qr.png"
            await page.wait_for_timeout(3000)
            await page.screenshot(path=str(qr_path))
            print(f"QR screenshot saved to: {qr_path}")
            print("Open this image and scan the QR code with your phone.")
            
            # Poll for cookie change (login detection)
            initial_cookies = len(await context.cookies())
            timeout = 300  # 5 min
            start = time.time()
            logged_in = False
            
            while time.time() - start < timeout:
                await asyncio.sleep(3)
                current_cookies = len(await context.cookies())
                if current_cookies > initial_cookies + 2:
                    logger.info(f"Cookie count changed: {initial_cookies} -> {current_cookies}")
                    await asyncio.sleep(2)  # Wait for cookies to settle
                    logged_in = True
                    break
            
            if not logged_in:
                print("Login timed out. No session saved.")
                await browser.close()
                return
        else:
            # Visible: let user log in manually
            print("Please log in manually in the browser...")
            print("After logging in, close the browser or press Enter here...")
            try:
                await page.wait_for_event("close", timeout=300000)
            except KeyboardInterrupt:
                pass
        
        # Save session with restrictive permissions (contains auth tokens)
        await context.storage_state(path=str(session_path))
        os.chmod(str(session_path), 0o600)
        print(f"Session saved to {session_path}")
        
        await browser.close()
