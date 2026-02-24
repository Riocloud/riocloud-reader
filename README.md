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
- **Security Hardened** - Built-in SSRF protection, path traversal prevention, secure session file permissions
- **AI-Powered Transcription** - Groq Whisper fallback for YouTube videos without captions
- **Direct Obsidian Sync** - Save content directly to your Obsidian vault
- **Bare Domain Support** - Use `example.com` directly in CLI

## Why Riocloud Reader?

Riocloud Reader breaks down data barriers across major social platforms. No more expensive API fees or access restrictions — automatically fetch videos, tweets, and long-form content, translate them to clean Markdown, and sync directly to Obsidian for fully automated intelligence monitoring.

- **Universal Collection** - Solved the blocking issues with WeChat and Xiaohongshu. Supports long-term Xiaohongshu collection without QR code scans. Say goodbye to 403 errors.

- **Cost Effective** - No need to purchase expensive Twitter API. Free automated collection through integrated tools.

- **AI-Powered Analysis** - Integrated Whisper for instant YouTube subtitle transcription. Bilibili data structured extraction.

- **Real-time Sync** - Telegram intelligence feed real-time integration.

- **Seamless Storage** - Heterogeneous data standardized, direct Obsidian integration to build your personal second brain.

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
| GROQ_API_KEY | YouTube Whisper | Free API key from console.groq.com |
| FIRECRAWL_API_KEY | Firecrawl | Optional, for paywalled content |
| DEEPREEDER_MEMORY_PATH | Storage | Directory to save content |
| OBSIDIAN_VAULT | Obsidian | Default vault path for --obsidian flag |
| OBSIDIAN_VAULT | Obsidian | Default vault path for --obsidian flag |

## Advanced Features

### YouTube Groq Whisper Fallback

When YouTube videos don't have captions, riocloud-reader automatically falls back to Groq Whisper API for transcription.

```bash
# Set up Groq API key
export GROQ_API_KEY=your_groq_api_key

# Now any YouTube video will be transcribed
riocloud-reader https://youtube.com/watch?v=xxx
```

Get your free API key at: https://console.groq.com/

### Bare Domain Support

You can use bare domain names without https:// prefix:

```bash
riocloud-reader example.com
riocloud-reader example.com/path
riocloud-reader twitter.com/elonmusk/status/123456
```

### Obsidian Vault Integration

Save content directly to your Obsidian vault:

```bash
# Save to Obsidian vault
riocloud-reader https://youtube.com/watch?v=xxx --obsidian /path/to/vault

# Or use environment variable
export OBSIDIAN_VAULT=/path/to/vault
riocloud-reader https://twitter.com/user/status/123
```

Creates date-based folder structure:
```
vault/
├── 2026-02/
│   ├── youtube/
│   │   └── dQw4w9WgXcQ_Test Video.md
│   └── twitter/
│       └── abc123_Tweet by User.md
```

### Twitter Login Session

For better Twitter/X coverage, log in to preserve session:

```bash
# First, log in (opens browser)
riocloud-reader login twitter

# Then use Twitter URLs - will use session if available
riocloud-reader https://x.com/user/status/123456
```

This uses three-tier fallback: FxTwitter API → Nitter → Playwright with session

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
