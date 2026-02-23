# -*- coding: utf-8 -*-
"""
Generic Parser — handles any URL via Trafilatura or Jina fallback
"""

import logging
import requests

from .base import BaseParser, ParseResult

logger = logging.getLogger("riocloud_reader.parsers.generic")


class GenericParser(BaseParser):
    """Parse any generic URL via Trafilatura or Jina fallback."""
    
    name = "generic"
    
    async def parse(self, url: str) -> ParseResult:
        """Parse a generic URL."""
        
        # Try Trafilatura first
        try:
            result = await self._fetch_trafilatura(url)
            if result.success:
                return result
            logger.warning(f"Trafilatura failed: {result.error}")
        except ImportError:
            logger.info("Trafilatura not available, using Jina fallback")
        
        # Fallback to Jina
        return await self._fetch_jina(url)
    
    async def _fetch_trafilatura(self, url: str) -> ParseResult:
        """Fetch via Trafilatura."""
        try:
            from trafilatura import fetch_url, extract
            
            html = fetch_url(url)
            if not html:
                return ParseResult.failure(url, "No content fetched")
            
            result = extract(html, output_format="markdown")
            if not result:
                return ParseResult.failure(url, "Extraction failed")
            
            # Get title
            from trafilatura import metadata
            meta = metadata.extraction_metadata(html)
            title = meta.get("title", "") if meta else ""
            
            return ParseResult(
                url=url,
                title=title or "Untitled",
                content=result,
                tags=["generic"],
            )
            
        except ImportError:
            raise
        except Exception as e:
            return ParseResult.failure(url, f"Trafilatura error: {e}")
    
    async def _fetch_jina(self, url: str) -> ParseResult:
        """Fallback: fetch via Jina Reader."""
        try:
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
            
            content = "\n".join(content_lines).strip()
            
            if not content:
                return ParseResult.failure(url, "Empty content")
            
            return ParseResult(
                url=url,
                title=title or "Untitled",
                content=content,
                tags=["generic", "jina"],
            )
            
        except Exception as e:
            return ParseResult.failure(url, f"Jina failed: {e}")
