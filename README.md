# Riocloud Reader

![PyPI](https://img.shields.io/pypi/v/riocloud-reader)
![Python](https://img.shields.io/pypi/pyversions/riocloud-reader)
![License](https://img.shields.io/github/license/Riocloud/riocloud-reader)

Universal content reader for AI agents — fetch, transcribe, and digest content from 30+ platforms in seconds.

## Why Riocloud Reader?

Ever wished your AI agent could read content from the web? Riocloud Reader makes it happen. Paste any URL — tweet, YouTube video, Reddit post, or article — and get clean, structured content instantly.

- ⚡ **Zero config** — Works out of the box, no API keys needed for most platforms
- 🌐 **30+ platforms** — Twitter/X, Reddit, YouTube, WeChat, Bilibili, RSS, and more
- 🧠 **AI-ready** — Structured output perfect for LLM ingestion
- 🔌 **Multi-integration** — CLI, Python library, MCP server, OpenClaw skill

## Supported Platforms

| Platform | Text | Transcript | API Key |
|----------|:----:|:----------:|:-------:|
| 🐦 Twitter/X | ✅ | — | ❌ |
| 🟠 Reddit | ✅ | — | ❌ |
| 🎬 YouTube | ✅ | ✅ | ❌ |
| 📰 WeChat | ✅ | — | ❌ |
| 📕 Xiaohongshu | ✅ | — | ❌ |
| 📕 Bilibili | ✅ | ✅ | ❌ |
| 📡 RSS | ✅ | — | ❌ |
| 💬 Telegram | ✅ | — | ✅ |
| 🌐 Generic | ✅ | — | ❌ |
| 📓 NotebookLM | — | ✅ | ✅ |

## Quick Start

```bash
# Install
pip install riocloud-reader

# CLI - read any URL
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=dQw4w9WgXcQ
riocloud-reader https://reddit.com/r/python/comments/abc

# Python - integrate into your app
from riocloud_reader import Reader

reader = Reader()
content = await reader.read("https://example.com/article")
print(content.title, content.content[:200])
```

## Features

### 🐦 Twitter/X
- Tweets, threads, X Articles, profiles
- Engagement stats (likes, RTs, views, bookmarks)
- Fallback to Nitter for difficult cases

### 🟠 Reddit
- Posts with full markdown
- Top comments (up to 15)
- Nested reply threads

### 🎬 YouTube
- Multi-language transcripts
- Video metadata

### 📰 WeChat + 📕 Xiaohongshu + 📕 Bilibili
- Chinese platform support
- Articles, notes, videos

### 📡 RSS/Atom
- Any standard feed

### 🔌 Integrations

**OpenClaw:**
```python
from skills.reader import run
result = run("https://x.com/elonmusk/status/123")
```

**MCP Server:**
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

## Installation Options

```bash
# Basic
pip install riocloud-reader

# With all features
pip install "riocloud-reader[all]"
playwright install chromium

# Specific features
pip install "riocloud-reader[youtube]"   # YouTube transcripts
pip install "riocloud-reader[telegram]" # Telegram support
pip install "riocloud-reader[notebooklm]" # NotebookLM integration
```

## Configuration

| Variable | Required | Description |
|----------|:--------:|-------------|
| `TG_API_ID` | Telegram | From my.telegram.org |
| `TG_API_HASH` | Telegram | From my.telegram.org |
| `GROQ_API_KEY` | Whisper | Free from console.groq.com |

## Built with ❤️ by [Riocloud](https://riocloud.io)

MIT License
