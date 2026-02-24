# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
Twitter/X Parser — combines FxTwitter (primary) with Nitter and Playwright fallback.

Three-tier fallback:
1. FxTwitter API (primary)
2. Nitter HTML scraping
3. Playwright with session (if available)
"""

import asyncio
import json
import logging
import os
import random
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from .base import BaseParser, ParseResult, is_twitter_url

logger = logging.getLogger("riocloud_reader.parsers.twitter")

# Known public Nitter instances
_NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.woodland.cafe",
    "https://nitter.kavin.rocks",
]

# Session directory for Twitter
SESSION_DIR = Path.home() / ".riocloud-reader" / "sessions"


class TwitterParser(BaseParser):
    """Parse Twitter/X tweets and profiles.
    
    Three-tier fallback:
    1. FxTwitter API (primary)
    2. Nitter HTML scraping
    3. Playwright with session (if available)
    """
    
    name = "twitter"
    
    def can_handle(self, url: str) -> bool:
        return is_twitter_url(url)
    
    async def parse(self, url: str) -> ParseResult:
        """Parse a Twitter URL."""
        tweet_info = self._extract_tweet_info(url)
        
        if not tweet_info:
            # Try as profile
            username = self._extract_profile_username(url)
            if username:
                return await self._parse_profile(url, username)
            return ParseResult.failure(url, "Invalid tweet URL format")
        
        username, tweet_id = tweet_info
        
        # Try FxTwitter first
        result = await self._parse_fxtwitter(url, username, tweet_id)
        if result.success:
            return result
        
        # Fallback to Nitter
        logger.warning(f"FxTwitter failed, trying Nitter: {result.error}")
        result = await self._parse_nitter(url, f"{username}/status/{tweet_id}")
        if result.success:
            return result
        
        # Fallback to Playwright with session
        logger.warning("Nitter failed, trying Playwright with session")
        return await self._parse_via_browser(url)
    
    def _extract_tweet_info(self, url: str) -> tuple[str, str] | None:
        """Extract (username, tweet_id) from URL."""
        match = re.search(
            r"(?:x\.com|twitter\.com)/([a-zA-Z0-9_]{1,15})/status/(\d+)",
            url
        )
        if match:
            return match.group(1), match.group(2)
        return None
    
    def _extract_profile_username(self, url: str) -> str | None:
        """Extract username from profile URL."""
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.split("/") if p]
        if len(path_parts) != 1:
            return None
        username = path_parts[0]
        reserved = {"home", "explore", "search", "messages", "notifications", "settings", "i"}
        if username.lower() in reserved:
            return None
        if re.fullmatch(r"[a-zA-Z0-9_]{1,15}", username):
            return username
        return None
    
    async def _parse_fxtwitter(self, url: str, username: str, tweet_id: str) -> ParseResult:
        """Fetch via FxTwitter API."""
        api_url = f"https://api.fxtwitter.com/{username}/status/{tweet_id}"
        
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                # Check response size limit
                raw_data = resp.read(self.max_response_size)
                data = json.loads(raw_data.decode())
            
            if data.get("code") != 200:
                return ParseResult.failure(url, f"FxTwitter error: {data.get('message')}")
            
            return self._build_result(url, data)
            
        except Exception as e:
            return ParseResult.failure(url, f"FxTwitter failed: {e}")
    
    async def _parse_profile(self, url: str, username: str) -> ParseResult:
        """Parse X profile."""
        api_url = f"https://api.fxtwitter.com/{username}"
        
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                # Check response size limit
                raw_data = resp.read(self.max_response_size)
                data = json.loads(raw_data.decode())
            
            if data.get("code") != 200:
                return ParseResult.failure(url, f"FxTwitter error")
            
            user = data.get("user", {})
            content = f"""# X Profile: @{user.get('screen_name', username)}

**Name:** {user.get('name', '')}
**Bio:** {user.get('description', '')}
**Location:** {user.get('location', '')}
**Joined:** {user.get('joined', '')}

## Stats
- Followers: {user.get('followers', 0):,}
- Following: {user.get('following', 0):,}
- Tweets: {user.get('tweets', 0):,}

Source: {url}
"""
            return ParseResult(
                url=url,
                title=f"X Profile @{username}",
                content=content,
                author=f"@{username}",
                tags=["twitter", "profile"],
            )
            
        except Exception as e:
            return ParseResult.failure(url, f"Failed: {e}")
    
    def _build_result(self, url: str, data: dict) -> ParseResult:
        """Build ParseResult from FxTwitter response."""
        tweet = data.get("tweet", {})
        author = tweet.get("author", {})
        
        screen_name = author.get("screen_name", "")
        name = author.get("name", "")
        text = tweet.get("text", "")
        created_at = tweet.get("created_at", "")
        
        # Stats
        stats = f"❤️ {tweet.get('likes', 0):,} · 🔁 {tweet.get('retweets', 0):,} · 👁️ {tweet.get('views', 0):,}"
        
        content_parts = [f"**@{screen_name}** ({name})\n"]
        content_parts.append(f"🕐 {created_at}\n")
        content_parts.append(f"📊 {stats}\n\n")
        content_parts.append("---\n\n")
        content_parts.append(text)
        
        # Quote tweet
        if tweet.get("quote"):
            qt = tweet["quote"]
            qt_author = qt.get("author", {}).get("screen_name", "")
            qt_text = qt.get("text", "")
            content_parts.append(f"\n\n---\n### Quoted Tweet\n> **@{qt_author}**: {qt_text}")
        
        # Media
        media = tweet.get("media", {}).get("all", [])
        if media:
            content_parts.append("\n\n---\n### Media\n")
            for item in media:
                m_type = item.get("type", "")
                m_url = item.get("url", "")
                if m_type == "photo":
                    content_parts.append(f"![Image]({m_url})\n")
        
        full_content = "\n".join(content_parts)
        
        tags = ["twitter"]
        if tweet.get("article"):
            tags.append("x-article")
        if tweet.get("quote"):
            tags.append("quote-tweet")
        
        return ParseResult(
            url=url,
            title=f"Tweet by @{screen_name}",
            content=full_content,
            author=f"@{screen_name}",
            tags=tags,
        )
    
    async def _parse_nitter(self, url: str, path: str) -> ParseResult:
        """Fallback: parse via Nitter."""
        import requests
        
        instances = random.sample(_NITTER_INSTANCES, min(2, len(_NITTER_INSTANCES)))
        
        for instance in instances:
            nitter_url = f"{instance}/{path}"
            try:
                resp = requests.get(nitter_url, headers=self._get_headers(), timeout=self.timeout)
                resp.raise_for_status()
                
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(resp.text, "html.parser")
                
                tweet_div = soup.find("div", class_="tweet-content")
                if not tweet_div:
                    continue
                
                content = tweet_div.get_text(separator="\n", strip=True)
                author_tag = soup.find("a", class_="fullname")
                author = author_tag.get_text(strip=True) if author_tag else ""
                
                return ParseResult(
                    url=url,
                    title=f"Tweet by {author}",
                    content=content,
                    author=author,
                    tags=["twitter", "nitter"],
                )
            except Exception as e:
                logger.warning(f"Nitter {instance} failed: {e}")
                continue
        
        return ParseResult.failure(url, "All parsers failed")
    
    async def _parse_via_browser(self, url: str) -> ParseResult:
        """Third-tier fallback: parse via Playwright with session.
        
        Requires Twitter session file at ~/.riocloud-reader/sessions/twitter.json
        Run: riocloud-reader login twitter
        """
        session_path = SESSION_DIR / "twitter.json"
        
        if not session_path.exists():
            return ParseResult.failure(
                url,
                "Twitter session not found. Run: riocloud-reader login twitter"
            )
        
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            return ParseResult.failure(url, "Playwright not installed")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                storage_state=str(session_path)
            )
            page = await context.new_page()
            
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(2000)
            
            # X-specific selectors for tweet content
            data = await page.evaluate("""() => {
                const article = document.querySelector('article[role="article"]');
                if (!article) return null;
                
                // Get text content
                const textEl = article.querySelector('[data-testid="tweetText"]');
                const text = textEl ? textEl.innerText : '';
                
                // Get author
                const authorEl = article.querySelector('[data-testid="User-Name"]');
                const author = authorEl ? authorEl.innerText.split('\\n')[0] : '';
                
                return { text, author };
            }""")
            
            await browser.close()
            
            if data and data.get("text"):
                return ParseResult(
                    url=url,
                    title=f"Tweet by {data.get('author', 'unknown')}",
                    content=data.get("text", ""),
                    author=data.get("author", ""),
                    tags=["twitter", "playwright"],
                )
            
            return ParseResult.failure(url, "Failed to extract tweet via Playwright")


async def login_twitter(headless: bool = False):
    """Login to Twitter and save session.
    
    Usage:
        riocloud-reader --login twitter
        riocloud-reader --login twitter --headless
    """
    import time
    
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    session_path = SESSION_DIR / "twitter.json"
    
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Playwright not installed. Run: pip install playwright")
        return
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        await page.goto("https://twitter.com/home", wait_until="domcontentloaded")
        
        if headless:
            # Headless: save QR screenshot for scanning
            qr_path = SESSION_DIR / "twitter_qr.png"
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
        
        # Save session with restrictive permissions
        await context.storage_state(path=str(session_path))
        import os
        os.chmod(str(session_path), 0o600)
        print(f"Session saved to {session_path}")
        
        await browser.close()
