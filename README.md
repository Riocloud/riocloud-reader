# Riocloud Reader

![BSD-2-Clause](https://img.shields.io/badge/License-BSD--2--Clause-blue)

Universal content reader for AI agents. Fetch, transcribe, and digest content from 30+ platforms in seconds.

## Overview

Riocloud Reader is a powerful universal content reader designed for AI agents and developers. It can fetch content from various online platforms, extract text and transcripts, and return structured data that is perfect for LLM ingestion.

Whether you need to read tweets, YouTube videos, Reddit posts, news articles, or content from Chinese platforms like WeChat and Bilibili, Riocloud Reader handles it all with a simple, unified API.

## Key Features

- **Zero Configuration** - Works out of the box for most platforms, no API keys required
- **30+ Platform Support** - Twitter/X, Reddit, YouTube, WeChat, Bilibili, RSS, and more
- **Multi-Format Output** - Returns structured data including title, content, author, timestamps, and metadata
- **Multiple Interfaces** - CLI tool, Python library, MCP server, and OpenClaw skill
- **Cross-Platform** - Works on Linux, macOS, and Windows

## Supported Platforms

### Twitter/X
- Regular tweets with full text
- Long tweets (Twitter Blue)
- X Articles (long-form content)
- Quoted tweets with nested content
- Reply threads (up to 5 via Nitter fallback)
- Profile snapshots including bio and stats
- Engagement metrics (likes, retweets, views, bookmarks)

### Reddit
- Self posts with full markdown body
- Link posts with URL and metadata
- Top comments (up to 15, sorted by score)
- Nested reply threads (up to 3 levels deep)
- Media URLs (images, galleries, videos)
- Post statistics (score, comment count, upvote ratio)
- Flair tags

### YouTube
- Video transcripts in multiple languages
- Video metadata (title, description, channel, duration)
- Support for various URL formats:
  - youtube.com/watch?v=xxx
  - youtu.be/xxx
  - youtube.com/embed/xxx

### WeChat (WeChat Official Accounts)
- Articles from official accounts
- Jina Reader as primary fetcher
- Playwright fallback for anti-scraping pages

### Xiaohongshu (Little Red Book)
- Notes and posts
- Images and media URLs
- Playwright with session for authenticated requests

### Bilibili
- Video metadata
- Subtitles
- Support for bilibili.com and b23.tv short links

### RSS/Atom
- Any standard RSS or Atom feed
- Auto-detection of feed URLs

### Telegram
- Channel messages
- Requires TG_API_ID and TG_API_HASH from my.telegram.org

### Generic (Any URL)
- Any webpage via Trafilatura
- Jina Reader as fallback
- Best effort content extraction

### NotebookLM (Integration)
- Upload content as sources
- Generate Audio Overview (podcast-style)
- Requires Google authentication

## Installation

### Basic Installation

```bash
pip install riocloud-reader
```

### With All Dependencies

```bash
pip install "riocloud-reader[all]"
playwright install chromium
```

### Optional Dependencies

```bash
# Browser support (WeChat, Xiaohongshu)
pip install "riocloud-reader[browser]"

# YouTube transcripts
pip install "riocloud-reader[youtube]"

# Telegram support
pip install "riocloud-reader[telegram]"

# NotebookLM integration
pip install "riocloud-reader[notebooklm]"

# Generic URL parsing
pip install "riocloud-reader[generic]"

# Development and testing
pip install "riocloud-reader[dev]"
```

## Usage

### Command Line Interface

```bash
# Read a single URL
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=dQw4w9WgXcQ
riocloud-reader https://reddit.com/r/python/comments/abc123

# Read multiple URLs
riocloud-reader https://url1.com https://url2.com

# Save output to file
riocloud-reader https://example.com/article --output article.md

# Specify output format
riocloud-reader https://example.com --format json
```

### Python Library

```python
import asyncio
from riocloud_reader import Reader

async def main():
    # Initialize reader
    reader = Reader()
    
    # Read a single URL
    content = await reader.read("https://twitter.com/user/status/123456")
    print(f"Title: {content.title}")
    print(f"Content: {content.content[:500]}")
    
    # Batch read multiple URLs
    results = await reader.read_batch([
        "https://twitter.com/user/status/1",
        "https://reddit.com/r/python/comments/abc",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
    ])
    
    for result in results:
        print(f"URL: {result.url}")
        print(f"Title: {result.title}")

asyncio.run(main())
```

### OpenClaw Skill

```python
from skills.reader import run

# Read content directly into agent memory
result = run("Check out this tweet: https://x.com/elonmusk/status/123456")
result = run("Get the transcript from: https://youtube.com/watch?v=dQw4w9WgXcQ")
```

### MCP Server

Start the MCP server:

```bash
python -m riocloud_reader.mcp
```

Configure in your Claude Desktop config (claude_desktop_config.json):

```json
{
  "mcpServers": {
    "riocloud-reader": {
      "command": "python",
      "args": ["-m", "riocloud_reader.mcp"]
    }
  }
}
```

## Configuration

### Environment Variables

| Variable | Required For | Description |
|----------|--------------|-------------|
| TG_API_ID | Telegram | API ID from my.telegram.org |
| TG_API_HASH | Telegram | API Hash from my.telegram.org |
| GROQ_API_KEY | Whisper | Free API key from console.groq.com |
| FIRECRAWL_API_KEY | Firecrawl | Optional, for paywalled content |
| DEEPREEDER_MEMORY_PATH | Storage | Directory to save content |

### Configuration File

Create a `.env` file:

```bash
cp .env.example .env
# Edit with your credentials
```

## Architecture

```
riocloud_reader/
├── parsers/                  # Platform-specific parsers
│   ├── base.py              # Base parser class and utilities
│   ├── twitter.py           # Twitter/X parser (FxTwitter + Nitter)
│   ├── reddit.py            # Reddit parser (.json API)
│   ├── youtube.py           # YouTube transcript parser
│   ├── wechat.py            # WeChat articles parser
│   ├── xhs.py               # Xiaohongshu parser
│   ├── bilibili.py          # Bilibili parser
│   ├── rss.py               # RSS/Atom feed parser
│   ├── telegram.py          # Telegram channel parser
│   └── generic.py           # Generic URL parser (Trafilatura)
├── core/                     # Core functionality
│   ├── router.py            # URL routing to appropriate parser
│   ├── storage.py           # File I/O utilities
│   └── config.py            # Configuration management
├── skills/                  # OpenClaw skill integration
│   └── reader/              # OpenClaw reader skill
├── integrations/            # Third-party integrations
│   └── notebooklm.py       # NotebookLM API
├── mcp/                     # MCP server
│   └── server.py            # MCP server implementation
├── reader.py                # Main Reader class
├── schema.py                # Data models and schemas
└── cli.py                   # CLI interface
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/Riocloud/riocloud-reader.git
cd riocloud-reader

# Install in development mode
pip install -e ".[dev]"

# Install all optional dependencies
pip install -e ".[all]"
playwright install chromium
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_parsers.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code with Black
black .

# Lint with Ruff
ruff check .

# Fix linting issues
ruff check --fix .
```

## License

BSD 2-Clause License - see LICENSE file for details.

## Support

- Report issues: https://github.com/Riocloud/riocloud-reader/issues
- Documentation: https://github.com/Riocloud/riocloud-reader#readme

## Related Projects

- [x-reader](https://github.com/runesleo/x-reader) - Original universal content reader
- [OpenClaw-DeepReeder](https://github.com/astonysh/OpenClaw-DeepReeder) - OpenClaw's built-in reader
