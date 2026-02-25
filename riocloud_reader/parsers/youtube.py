# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
YouTube Parser — fetches transcripts and metadata.

Three-tier fallback:
1. YouTube Transcript API
2. Groq Whisper API (if GROQ_API_KEY set)
3. Error message
"""

import asyncio
import logging
import os
import tempfile

import requests
from bs4 import BeautifulSoup

from .base import BaseParser, ParseResult, is_youtube_url, extract_youtube_video_id

logger = logging.getLogger("riocloud_reader.parsers.youtube")

# Groq Whisper model
GROQ_WHISPER_MODEL = "whisper-large-v3"


class YouTubeParser(BaseParser):
    """Extract transcripts and metadata from YouTube videos."""
    
    name = "youtube"
    preferred_langs = ["en", "zh-Hans", "zh-Hant", "zh", "ja", "ko"]
    
    def can_handle(self, url: str) -> bool:
        return is_youtube_url(url)
    
    async def parse(self, url: str) -> ParseResult:
        """Parse a YouTube URL."""
        video_id = extract_youtube_video_id(url)
        if not video_id:
            return ParseResult.failure(url, "Invalid YouTube URL")
        
        # Get metadata
        title, author, description = await self._fetch_metadata(url)
        
        # Get transcript
        transcript_text, transcript_lang = await self._fetch_transcript(video_id)
        
        content_parts = []
        
        if transcript_lang:
            content_parts.append(f"*Transcript language: {transcript_lang}*\n")
        
        if transcript_text:
            content_parts.append(transcript_text)
        else:
            content_parts.append("> No transcript available for this video.")
        
        if description:
            content_parts.append(f"\n\n---\n\n**Description:**\n{description}")
        
        content = "\n".join(content_parts)
        
        return ParseResult(
            url=url,
            title=title or f"YouTube ({video_id})",
            content=content,
            author=author,
            tags=["youtube", "video"],
        )
    
    async def _fetch_metadata(self, url: str) -> tuple:
        """Fetch video metadata from the page."""
        try:
            resp = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Title
            title = ""
            og_title = soup.find("meta", property="og:title")
            if og_title:
                title = og_title.get("content", "")
            if not title:
                title_tag = soup.find("title")
                title = title_tag.get_text(strip=True) if title_tag else ""
                if title.endswith(" - YouTube"):
                    title = title[:-10].strip()
            
            # Author
            author = ""
            link_author = soup.find("link", attrs={"itemprop": "name"})
            if link_author:
                author = link_author.get("content", "")
            
            # Description
            description = ""
            og_desc = soup.find("meta", property="og:description")
            if og_desc:
                description = og_desc.get("content", "")
            
            return title, author, description
            
        except Exception as e:
            logger.warning(f"Metadata fetch failed: {e}")
            return "", "", ""
    
    async def _fetch_transcript(self, video_id: str) -> tuple:
        """Fetch transcript for a video.
        
        Three-tier fallback:
        1. YouTube Transcript API
        2. Groq Whisper API (if GROQ_API_KEY set)
        3. Return empty
        """
        # Tier 1: YouTube Transcript API
        transcript_text, lang_code = self._fetch_youtube_transcript(video_id)
        if transcript_text:
            return transcript_text, lang_code
        
        # Tier 2: Groq Whisper API
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            # Validate API key format (should start with gsk_)
            if not groq_key.startswith("gsk_"):
                logger.warning("Invalid GROQ_API_KEY format (should start with gsk_)")
            else:
                logger.info("No YouTube transcript, trying Groq Whisper API...")
                transcript_text = await self._fetch_via_whisper(video_id, groq_key)
                if transcript_text:
                    return transcript_text, "en (Whisper)"
        
        # Tier 3: No transcript
        return "", ""
    
    def _fetch_youtube_transcript(self, video_id: str) -> tuple:
        """Fetch transcript via YouTube Transcript API."""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            
            # Create instance and list transcripts
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)
            
            # Try preferred languages
            transcript = None
            lang_code = ""
            
            for lang in self.preferred_langs:
                try:
                    transcript = transcript_list.find_manually_created_transcript([lang])
                    lang_code = lang
                    break
                except:
                    continue
            
            # Auto-generated fallback
            if not transcript:
                for lang in self.preferred_langs:
                    try:
                        transcript = transcript_list.find_generated_transcript([lang])
                        lang_code = f"{lang} (auto)"
                        break
                    except:
                        continue
            
            if transcript:
                entries = transcript.fetch()
                lines = [e.text for e in entries]
                return self._format_transcript(lines), lang_code
            
        except ImportError:
            logger.warning("youtube_transcript_api not installed")
        except Exception as e:
            logger.warning(f"Transcript fetch failed: {e}")
        
        return "", ""
    
    async def _fetch_via_whisper(self, video_id: str, api_key: str) -> str:
        """Transcribe audio via Groq Whisper API.
        
        Downloads audio via yt-dlp and sends to Groq for transcription.
        Requires GROQ_API_KEY environment variable.
        """
        try:
            import yt_dlp
        except ImportError:
            logger.warning("yt-dlp not installed, cannot use Whisper fallback")
            return ""
        
        # Download audio to temp file
        audio_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                audio_path = tmp.name
            
            # Download audio-only (m4a is better quality)
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': audio_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
            }
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._download_audio, video_id, ydl_opts)
            
            # Check if file exists
            if not os.path.exists(audio_path):
                logger.warning("Audio download failed")
                return ""
            
            # Send to Groq Whisper API
            with open(audio_path, "rb") as audio_file:
                files = {"file": ("audio.mp3", audio_file, "audio/mpeg")}
                headers = {"Authorization": f"Bearer {api_key}"}
                data = {"model": GROQ_WHISPER_MODEL}
                
                response = requests.post(
                    "https://api.groq.com/openai/v1/audio/transcriptions",
                    files=files,
                    data=data,
                    headers=headers,
                    timeout=120
                )
            
            if response.status_code == 200:
                result = response.json()
                text = result.get("text", "")
                if text:
                    logger.info(f"Groq Whisper transcription succeeded ({len(text)} chars)")
                    return self._format_transcript(text.split())
                return ""
            else:
                logger.warning(f"Groq API error: {response.status_code} {response.text}")
                return ""
                
        except Exception as e:
            logger.warning(f"Whisper transcription failed: {e}")
            return ""
        finally:
            # Cleanup temp file
            if audio_path and os.path.exists(audio_path):
                try:
                    os.unlink(audio_path)
                except:
                    pass
    
    def _download_audio(self, video_id: str, ydl_opts: dict):
        """Download audio (sync, runs in executor)."""
        import yt_dlp
        url = f"https://www.youtube.com/watch?v={video_id}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
    def _format_transcript(self, lines: list) -> str:
        """Format transcript into paragraphs."""
        if not lines:
            return ""
        
        paragraphs = []
        current = []
        sentence_count = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            current.append(line)
            if any(line.endswith(p) for p in ".!?。！？"):
                sentence_count += 1
            if sentence_count >= 5:
                paragraphs.append(" ".join(current))
                current = []
                sentence_count = 0
        
        if current:
            paragraphs.append(" ".join(current))
        
        return "\n\n".join(paragraphs)
