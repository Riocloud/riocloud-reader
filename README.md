# Riocloud Reader

![GitHub](https://img.shields.io/github/stars/Riocloud/riocloud-reader)
![License](https://img.shields.io/github/license/Riocloud/riocloud-reader)
![Python](https://img.shields.io/pypi/pyversions/3.10+-brightgreen)

Universal content reader — fetch, transcribe, and digest content from 30+ platforms. Combines the best of [x-reader](https://github.com/runesleo/x-reader) and [OpenClaw-DeepReeder](https://github.com/astonysh/OpenClaw-DeepReeder).

## Supported Platforms

| Platform | Text Fetch | Video/Audio Transcript | API Key Required | Notes |
|----------|:---------:|:----------------------:|:----------------:|-------|
| 🐦 **Twitter/X** | ✅ | — | ❌ | FxTwitter API + Nitter fallback |
| 🟠 **Reddit** | ✅ | — | ❌ | Native .json API |
| 🎬 **YouTube** | ✅ | ✅ | ❌ | transcripts in multiple languages |
| 📰 **WeChat** (微信公众号) | ✅ | — | ❌ | Jina + Playwright fallback |
| 📕 **Xiaohongshu** (小红书) | ✅ | — | ❌ | Playwright with session |
| 📕 **Bilibili** (B站) | ✅ | ✅ | ❌ | Video metadata + subtitles |
| 📡 **RSS/Atom** | ✅ | — | ❌ | feedparser |
| 💬 **Telegram** | ✅ | — | ✅ | Telethon (requires API credentials) |
| 🌐 **Generic (any URL)** | ✅ | — | ❌ | Trafilatura + Jina Reader |
| 📓 **NotebookLM** | — | ✅ | ✅ | Google authentication |

### Platform Details

#### 🐦 Twitter/X
- Regular tweets with engagement stats (likes, RTs, views, bookmarks)
- Long tweets (Twitter Blue)
- X Articles (long-form content)
- Quoted tweets (nested content)
- Reply threads (up to 5 via Nitter fallback)
- Profile snapshots

#### 🟠 Reddit
- Self posts (full markdown body)
- Link posts (URL + metadata)
- Top comments (up to 15, sorted by score)
- Nested reply threads (up to 3 levels deep)
- Media URLs (images, galleries, videos)
- Post stats (score, comment count, upvote ratio)
- Flair tags

#### 🎬 YouTube
- Video transcripts in multiple languages
- Metadata (title, description, channel)
- Support for `youtube.com`, `youtu.be`, `youtube.com/embed`

#### 📰 WeChat (微信公众号)
- Articles from official accounts
- Jina Reader as primary fetcher
- Playwright fallback for anti-scraping pages

#### 📕 Xiaohongshu (小红书)
- Notes and posts
- Images and media URLs
- Playwright with session for authenticated requests

#### 📕 Bilibili (B站)
- Video metadata
- Subtitles
- Support for `bilibili.com` and `b23.tv` short links

#### 📡 RSS/Atom
- Any standard RSS or Atom feed
- Auto-detection of feed URLs

#### 💬 Telegram
- Channel messages
- Requires `TG_API_ID` and `TG_API_HASH` from my.telegram.org

#### 🌐 Generic (Any URL)
- Any webpage via Trafilatura
- Jina Reader as fallback
- Best effort content extraction

#### 📓 NotebookLM (Integration)
- Upload content as sources
- Generate Audio Overview (podcast-style)
- Requires Google authentication

## Installation

### Basic Install
```bash
pip install git+https://github.com/Riocloud/riocloud-reader.git
```

### With All Dependencies
```bash
pip install "riocloud-reader[all] @ git+https://github.com/Riocloud/riocloud-reader.git"
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

# Development
pip install "riocloud-reader[dev]"
```

## Usage

### CLI
```bash
# Single URL
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=dQw4w9WgXcQ
riocloud-reader https://reddit.com/r/python/comments/abc123

# Multiple URLs
riocloud-reader https://url1.com https://url2.com

# Save to file
riocloud-reader https://example.com/article --output article.md
```

### Python Library
```python
import asyncio
from riocloud_reader import Reader

async def main():
    reader = Reader()
    
    # Single URL
    content = await reader.read("https://twitter.com/user/status/123456")
    print(content.title)
    print(content.content[:500])
    
    # Batch
    results = await reader.read_batch([
        "https://twitter.com/user/status/1",
        "https://reddit.com/r/python/comments/abc",
    ])

asyncio.run(main())
```

### OpenClaw Skill
```python
from skills.reader import run

# Read content directly into agent memory
result = run("Check out this: https://x.com/elonmusk/status/123456")
```

### MCP Server
```bash
# Start MCP server
python -m riocloud_reader.mcp

# Configure in claude_desktop_config.json
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

| Variable | Required | Description |
|----------|:--------:|-------------|
| `TG_API_ID` | Telegram only | From my.telegram.org |
| `TG_API_HASH` | Telegram only | From my.telegram.org |
| `GROQ_API_KEY` | Whisper only | Free from console.groq.com |
| `FIRECRAWL_API_KEY` | Optional | For paywalled content |
| `DEEPREEDER_MEMORY_PATH` | Optional | Where to save content |

### .env File
```bash
cp .env.example .env
# Edit with your credentials
```

## Architecture

```
riocloud_reader/
├── parsers/
│   ├── base.py          # Base parser + ParseResult
│   ├── twitter.py       # Twitter/X (FxTwitter + Nitter)
│   ├── reddit.py        # Reddit (.json API)
│   ├── youtube.py       # YouTube transcripts
│   ├── wechat.py        # WeChat articles
│   ├── xhs.py           # Xiaohongshu
│   ├── bilibili.py      # Bilibili
│   ├── rss.py           # RSS/Atom
│   ├── telegram.py      # Telegram channels
│   └── generic.py       # Any URL (Trafilatura)
├── core/
│   ├── router.py        # URL → Parser routing
│   ├── storage.py       # File I/O
│   └── config.py        # Settings
├── skills/
│   └── reader/          # OpenClaw skill
├── integrations/
│   └── notebooklm.py   # NotebookLM API
├── mcp/
│   └── server.py        # MCP server
├── reader.py            # Main Reader class
└── schema.py           # Data models
```

## Development

```bash
# Clone and install
git clone https://github.com/Riocloud/riocloud-reader.git
cd riocloud-reader
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
ruff check --fix .
```

## License

MIT — [Riocloud](https://riocloud.io)
