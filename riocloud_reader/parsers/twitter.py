# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
Twitter/X Parser — combines FxTwitter (primary) with Nitter fallback.
"""

import json
import logging
import os
import random
import re
import time
import urllib.error
import urllib.request
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


class TwitterParser(BaseParser):
    """Parse Twitter/X tweets and profiles.
    
    Primary: FxTwitter API (structured JSON)
    Fallback: Nitter HTML scraping
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
        return await self._parse_nitter(url, f"{username}/status/{tweet_id}")
    
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
                data = json.loads(resp.read().decode())
            
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
                data = json.loads(resp.read().decode())
            
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
