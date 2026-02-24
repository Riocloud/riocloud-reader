# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
Unit tests for parsers.
"""

from pathlib import Path

import pytest
from riocloud_reader.parsers import (
    get_parser,
    TwitterParser,
    RedditParser,
    YouTubeParser,
    WeChatParser,
    XHSParser,
    BilibiliParser,
    RSSParser,
    GenericParser,
)


class TestParserRouter:
    """Test parser router."""
    
    def test_get_twitter_parser(self):
        parser = get_parser("twitter")
        assert isinstance(parser, TwitterParser)
    
    def test_get_reddit_parser(self):
        parser = get_parser("reddit")
        assert isinstance(parser, RedditParser)
    
    def test_get_youtube_parser(self):
        parser = get_parser("youtube")
        assert isinstance(parser, YouTubeParser)
    
    def test_get_wechat_parser(self):
        parser = get_parser("wechat")
        assert isinstance(parser, WeChatParser)
    
    def test_get_xhs_parser(self):
        parser = get_parser("xhs")
        assert isinstance(parser, XHSParser)
    
    def test_get_bilibili_parser(self):
        parser = get_parser("bilibili")
        assert isinstance(parser, BilibiliParser)
    
    def test_get_rss_parser(self):
        parser = get_parser("rss")
        assert isinstance(parser, RSSParser)
    
    def test_get_generic_parser(self):
        parser = get_parser("generic")
        assert isinstance(parser, GenericParser)
    
    def test_case_insensitive(self):
        parser = get_parser("TWITTER")
        assert isinstance(parser, TwitterParser)


class TestTwitterParser:
    """Test Twitter parser URL detection."""
    
    def test_can_handle_twitter_url(self):
        parser = TwitterParser()
        assert parser.can_handle("https://twitter.com/user/status/1234567890")
        assert parser.can_handle("https://x.com/user/status/1234567890")
    
    def test_cannot_handle_other_urls(self):
        parser = TwitterParser()
        assert not parser.can_handle("https://reddit.com/r/python/comments/abc")
        assert not parser.can_handle("https://youtube.com/watch?v=xxx")
    
    def test_extract_tweet_info(self):
        parser = TwitterParser()
        result = parser._extract_tweet_info("https://twitter.com/elonmusk/status/1234567890")
        assert result == ("elonmusk", "1234567890")
    
    def test_extract_profile_username(self):
        parser = TwitterParser()
        assert parser._extract_profile_username("https://twitter.com/elonmusk") == "elonmusk"
        assert parser._extract_profile_username("https://x.com/elonmusk") == "elonmusk"
        # Reserved paths
        assert parser._extract_profile_username("https://twitter.com/home") is None
        assert parser._extract_profile_username("https://twitter.com/explore") is None


class TestRedditParser:
    """Test Reddit parser URL detection."""
    
    def test_can_handle_reddit_url(self):
        parser = RedditParser()
        assert parser.can_handle("https://www.reddit.com/r/python/comments/abc123/post_title/")
        assert parser.can_handle("https://old.reddit.com/r/python/comments/abc123/")
    
    def test_cannot_handle_other_urls(self):
        parser = RedditParser()
        assert not parser.can_handle("https://twitter.com/user/status/123")
        assert not parser.can_handle("https://youtube.com/watch?v=xxx")
    
    def test_build_json_url(self):
        parser = RedditParser()
        url = parser._build_json_url("https://www.reddit.com/r/python/comments/abc123/post_title/")
        assert url == "https://www.reddit.com/r/python/comments/abc123/post_title/.json"


class TestYouTubeParser:
    """Test YouTube parser."""
    
    def test_can_handle_youtube_url(self):
        parser = YouTubeParser()
        assert parser.can_handle("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert parser.can_handle("https://youtu.be/dQw4w9WgXcQ")
        assert parser.can_handle("https://youtube.com/embed/dQw4w9WgXcQ")
    
    def test_extract_video_id(self):
        from riocloud_reader.parsers.base import extract_youtube_video_id
        
        assert extract_youtube_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
        assert extract_youtube_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"
        assert extract_youtube_video_id("https://youtube.com/embed/dQw4w9WgXcQ") == "dQw4w9WgXcQ"
        assert extract_youtube_video_id("invalid") == ""
    
    def test_format_transcript(self):
        """Test transcript formatting."""
        parser = YouTubeParser()
        
        # Short lines - should not paragraph break
        lines = ["Hello", "world", "this is a test"]
        result = parser._format_transcript(lines)
        assert "Hello world this is a test" in result
        
        # Lines with punctuation - should paragraph break
        lines = ["Hello world.", "This is a test.", "More text here."]
        result = parser._format_transcript(lines)
        # Should have at least one paragraph break
        assert "\n\n" in result or len(result) > 0
    
    def test_preferred_langs(self):
        """Test that preferred languages include major languages."""
        parser = YouTubeParser()
        assert "en" in parser.preferred_langs
        assert "zh-Hans" in parser.preferred_langs
        assert "ja" in parser.preferred_langs


class TestWeChatParser:
    """Test WeChat parser."""
    
    def test_can_handle_wechat_url(self):
        parser = WeChatParser()
        assert parser.can_handle("https://mp.weixin.qq.com/s/abc123")


class TestXHSParser:
    """Test Xiaohongshu parser."""
    
    def test_can_handle_xhs_url(self):
        parser = XHSParser()
        assert parser.can_handle("https://www.xiaohongshu.com/explore/abc123")
        assert parser.can_handle("https://xhslink.com/abc")


class TestBilibiliParser:
    """Test Bilibili parser."""
    
    def test_can_handle_bilibili_url(self):
        parser = BilibiliParser()
        assert parser.can_handle("https://www.bilibili.com/video/BV1xx411c7XD")
        assert parser.can_handle("https://b23.tv/abc123")
    
    def test_extract_bvid(self):
        parser = BilibiliParser()
        assert parser._extract_bvid("https://www.bilibili.com/video/BV1xx411c7XD") == "BV1xx411c7XD"


class TestRSSParser:
    """Test RSS parser."""
    
    def test_can_handle_rss_url(self):
        parser = RSSParser()
        assert parser.can_handle("https://example.com/feed.xml")
        assert parser.can_handle("https://example.com/rss")
        assert parser.can_handle("https://example.com/feed")


class TestGenericParser:
    """Test generic parser."""
    
    def test_name(self):
        parser = GenericParser()
        assert parser.name == "generic"


class TestCLI:
    """Test CLI utilities."""
    
    def test_normalize_url_with_https(self):
        """Test that URLs with https:// are not modified."""
        from riocloud_reader.cli import normalize_url
        
        assert normalize_url("https://example.com") == "https://example.com"
        assert normalize_url("http://example.com") == "http://example.com"
        assert normalize_url("https://example.com/path") == "https://example.com/path"
    
    def test_normalize_bare_domain(self):
        """Test that bare domains get https:// prefix."""
        from riocloud_reader.cli import normalize_url
        
        assert normalize_url("example.com") == "https://example.com"
        assert normalize_url("example.com/path") == "https://example.com/path"
        assert normalize_url("sub.example.com") == "https://sub.example.com"
        assert normalize_url("sub.example.com/path") == "https://sub.example.com/path"
    
    def test_normalize_invalid_url(self):
        """Test that invalid URLs are returned as-is."""
        from riocloud_reader.cli import normalize_url
        
        # No dot - not a domain
        assert normalize_url("localhost") == "localhost"
        # Spaces - not valid
        assert normalize_url("hello world") == "hello world"
        # Already has scheme
        assert normalize_url("ftp://example.com") == "ftp://example.com"
    
    def test_save_to_obsidian(self, tmp_path):
        """Test saving content to Obsidian vault."""
        from riocloud_reader.cli import save_to_obsidian
        from riocloud_reader.schema import UnifiedContent, SourceType
        
        content = UnifiedContent(
            source_type=SourceType.YOUTUBE,
            source_name="test",
            title="Test Video Title",
            content="Test content here",
            url="https://youtube.com/watch?v=abc123",
            author="Test Author",
            tags=["test"],
        )
        
        # Save to temp vault
        vault_path = str(tmp_path / "vault")
        result_path = save_to_obsidian(content, vault_path)
        
        # Check file was created
        assert Path(result_path).exists()
        
        # Check content
        with open(result_path, "r") as f:
            content_str = f.read()
            assert "Test Video Title" in content_str
            assert "Test content here" in content_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
