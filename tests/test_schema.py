# -*- coding: utf-8 -*-
"""
Unit tests for schema.
"""

import pytest
from riocloud_reader.schema import (
    UnifiedContent,
    UnifiedInbox,
    SourceType,
    MediaType,
)


class TestUnifiedContent:
    """Test UnifiedContent model."""
    
    def test_create_content(self):
        content = UnifiedContent(
            source_type=SourceType.TWITTER,
            source_name="twitter.com",
            title="Test Tweet",
            content="This is test content",
            url="https://twitter.com/user/status/123",
        )
        
        assert content.title == "Test Tweet"
        assert content.source_type == SourceType.TWITTER
        assert content.id != ""
        assert content.fetched_at != ""
    
    def test_auto_id_generation(self):
        content1 = UnifiedContent(
            source_type=SourceType.TWITTER,
            source_name="test",
            title="Test",
            content="Content",
            url="https://example.com/test",
        )
        
        content2 = UnifiedContent(
            source_type=SourceType.TWITTER,
            source_name="test",
            title="Test",
            content="Content",
            url="https://example.com/test",
        )
        
        # Same URL should generate same ID
        assert content1.id == content2.id
    
    def test_to_dict(self):
        content = UnifiedContent(
            source_type=SourceType.YOUTUBE,
            source_name="youtube.com",
            title="Test Video",
            content="Video content",
            url="https://youtube.com/watch?v=xxx",
        )
        
        d = content.to_dict()
        
        assert d["title"] == "Test Video"
        assert d["source_type"] == "youtube"
        assert d["url"] == "https://youtube.com/watch?v=xxx"
    
    def test_from_dict(self):
        data = {
            "source_type": "reddit",
            "source_name": "reddit.com",
            "title": "Test Post",
            "content": "Post content",
            "url": "https://reddit.com/r/test/comments/abc",
            "author": "testuser",
        }
        
        content = UnifiedContent.from_dict(data)
        
        assert content.source_type == SourceType.REDDIT
        assert content.author == "testuser"
    
    def test_word_count_auto(self):
        content = UnifiedContent(
            source_type=SourceType.GENERIC,
            source_name="test",
            title="Test",
            content="one two three four five",
            url="https://example.com",
        )
        
        assert content.word_count == 5
    
    def test_to_markdown(self):
        content = UnifiedContent(
            source_type=SourceType.TWITTER,
            source_name="twitter.com",
            title="Test Tweet",
            content="This is a tweet",
            url="https://twitter.com/user/status/123",
        )
        
        md = content.to_markdown()
        
        assert "---" in md
        assert "title:" in md
        assert "Test Tweet" in md
        assert "This is a tweet" in md


class TestUnifiedInbox:
    """Test UnifiedInbox model."""
    
    def test_add_unique_items(self):
        inbox = UnifiedInbox("/tmp/test_inbox.json")
        
        content1 = UnifiedContent(
            source_type=SourceType.TWITTER,
            source_name="test",
            title="Test",
            content="Content 1",
            url="https://example.com/1",
        )
        
        content2 = UnifiedContent(
            source_type=SourceType.TWITTER,
            source_name="test",
            title="Test",
            content="Content 2",
            url="https://example.com/2",
        )
        
        assert inbox.add(content1) is True
        assert inbox.add(content2) is True
        assert len(inbox.items) == 2
    
    def test_duplicate_ignored(self):
        inbox = UnifiedInbox("/tmp/test_inbox2.json")
        
        content1 = UnifiedContent(
            source_type=SourceType.TWITTER,
            source_name="test",
            title="Test",
            content="Content",
            url="https://example.com/same",
        )
        
        content2 = UnifiedContent(
            source_type=SourceType.TWITTER,
            source_name="test",
            title="Test",
            content="Different content",
            url="https://example.com/same",
        )
        
        inbox.add(content1)
        result = inbox.add(content2)
        
        assert result is False
        assert len(inbox.items) == 1
    
    def test_get_by_source(self):
        inbox = UnifiedInbox("/tmp/test_inbox3.json")
        
        inbox.add(UnifiedContent(
            source_type=SourceType.TWITTER,
            source_name="test",
            title="Tweet",
            content="content",
            url="https://example.com/1",
        ))
        
        inbox.add(UnifiedContent(
            source_type=SourceType.REDDIT,
            source_name="test",
            title="Post",
            content="content",
            url="https://example.com/2",
        ))
        
        twitter_items = inbox.get_by_source(SourceType.TWITTER)
        
        assert len(twitter_items) == 1
        assert twitter_items[0].source_type == SourceType.TWITTER


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
