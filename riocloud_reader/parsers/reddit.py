# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
Reddit Parser — uses native .json API (no API key needed).
"""

import json
import logging
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urlparse

from .base import BaseParser, ParseResult, is_reddit_url

logger = logging.getLogger("riocloud_reader.parsers.reddit")


class RedditParser(BaseParser):
    """Parse Reddit posts and comments via native .json API."""
    
    name = "reddit"
    max_comments = 15
    max_depth = 3
    
    user_agent = "RiocloudReader/1.0 (+https://github.com/Riocloud/riocloud-reader)"
    
    def can_handle(self, url: str) -> bool:
        return is_reddit_url(url)
    
    async def parse(self, url: str) -> ParseResult:
        """Parse a Reddit URL."""
        json_url = self._build_json_url(url)
        if not json_url:
            return ParseResult.failure(url, "Invalid Reddit URL format")
        
        try:
            req = urllib.request.Request(
                json_url,
                headers={"User-Agent": self.user_agent, "Accept": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                # Check response size
                content_length = resp.headers.get('Content-Length')
                if content_length and int(content_length) > self.max_response_size:
                    return ParseResult.failure(url, f"Response too large ({content_length} bytes)")
                
                raw_data = resp.read(self.max_response_size)
                data = json.loads(raw_data.decode())
            
            return self._build_result(url, data)
            
        except urllib.error.HTTPError as e:
            if e.code == 429:
                return ParseResult.failure(url, "Rate limited (429)")
            elif e.code == 404:
                return ParseResult.failure(url, "Post not found (404)")
            return ParseResult.failure(url, f"HTTP {e.code}")
        except Exception as e:
            return ParseResult.failure(url, f"Failed: {e}")
    
    def _build_json_url(self, url: str) -> str | None:
        """Convert Reddit URL to .json API URL."""
        if "/comments/" not in url:
            return None
        parsed = urlparse(url)
        path = parsed.path.rstrip("/")
        return f"https://www.reddit.com{path}/.json"
    
    def _build_result(self, url: str, data: list) -> ParseResult:
        """Build ParseResult from Reddit JSON."""
        if not isinstance(data, list) or len(data) < 1:
            return ParseResult.failure(url, "Invalid Reddit JSON structure")
        
        try:
            post = data[0]["data"]["children"][0]["data"]
        except (KeyError, IndexError):
            return ParseResult.failure(url, "Could not parse post data")
        
        title = post.get("title", "Untitled")
        author = post.get("author", "[deleted]")
        subreddit = post.get("subreddit_name_prefixed", "r/unknown")
        score = post.get("score", 0)
        num_comments = post.get("num_comments", 0)
        selftext = post.get("selftext", "")
        flair = post.get("link_flair_text", "")
        
        # Format timestamp
        created_utc = post.get("created_utc", 0)
        timestamp = ""
        if created_utc:
            dt = datetime.fromtimestamp(created_utc, tz=timezone.utc)
            timestamp = dt.strftime("%Y-%m-%d %H:%M UTC")
        
        content_parts = []
        content_parts.append(f"# {title}\n")
        content_parts.append(f"**{subreddit}** · u/{author} · {timestamp}\n")
        
        stats = f"⬆️ {score:,} · 💬 {num_comments:,} comments"
        if flair:
            stats += f" · 🏷️ {flair}"
        content_parts.append(f"{stats}\n")
        content_parts.append("---\n")
        
        if selftext:
            content_parts.append(selftext)
        else:
            post_url = post.get("url", "")
            if post_url:
                content_parts.append(f"🔗 Link: {post_url}")
        
        # Extract comments
        if len(data) >= 2:
            comments = self._extract_comments(data[1])
            if comments:
                content_parts.append("\n\n---\n### Top Comments\n")
                content_parts.extend(comments)
        
        full_content = "\n".join(content_parts)
        
        tags = ["reddit", subreddit.lower()]
        if flair:
            tags.append(flair.lower().replace(" ", "-"))
        
        return ParseResult(
            url=url,
            title=f"[{subreddit}] {title}",
            content=full_content,
            author=f"u/{author}",
            tags=tags,
        )
    
    def _extract_comments(self, comment_data: dict) -> list:
        """Extract top comments from JSON."""
        try:
            children = comment_data["data"]["children"]
        except KeyError:
            return []
        
        comments = []
        for child in children:
            if child.get("kind") != "t1":
                continue
            cdata = child.get("data", {})
            body = cdata.get("body", "")
            if not body or body in ("[deleted]", "[removed]"):
                continue
            
            author = cdata.get("author", "[deleted]")
            score = cdata.get("score", 0)
            
            comments.append(f"**u/{author}** (⬆️ {score:,}):\n> {body}\n")
            
            if len(comments) >= self.max_comments:
                break
        
        return comments
