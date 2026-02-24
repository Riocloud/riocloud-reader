# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
# Riocloud Reader Skill for OpenClaw
# 
# Usage:
#   Simply send a URL in the conversation
#   The skill will automatically detect and parse the content
#
# Supported platforms:
#   - Twitter/X: tweets, threads, X Articles, profiles
#   - Reddit: posts + comments
#   - YouTube: transcripts
#   - WeChat: public articles
#   - Xiaohongshu: notes
#   - Bilibili: videos
#   - Any URL: generic content extraction

from riocloud_reader import Reader
from riocloud_reader.schema import UnifiedInbox

INBOX_PATH = "./memory/inbox/"

def run(input_text: str) -> str:
    """
    Parse content from URLs in the input text.
    
    Args:
        input_text: Text containing URLs to parse
        
    Returns:
        Parsed content in Markdown format
    """
    import re
    import asyncio
    
    # Extract URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, input_text)
    
    if not urls:
        return "No URLs found in input"
    
    # Initialize reader with inbox
    inbox_path = f"{INBOX_PATH}riocloud-inbox.json"
    inbox = UnifiedInbox(inbox_path)
    reader = Reader(inbox=inbox)
    
    async def fetch_all():
        results = await reader.read_batch(urls)
        return results
    
    results = asyncio.run(fetch_all())
    
    output_parts = []
    
    for content in results:
        output_parts.append(f"## {content.title}")
        output_parts.append(f"**Source:** {content.source_type.value}")
        output_parts.append(f"**URL:** {content.url}")
        output_parts.append("")
        output_parts.append(content.content[:2000])
        
        if len(content.content) > 2000:
            output_parts.append(f"\n... ({(len(content.content) - 2000) // 500} more sections)")
        
        output_parts.append("\n---\n")
    
    # Save inbox
    inbox.save()
    
    return "\n".join(output_parts)


if __name__ == "__main__":
    # Test
    test_input = "Check this out: https://twitter.com/elonmusk/status/1234567890"
    result = run(test_input)
    print(result[:500])
