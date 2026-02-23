# Riocloud Reader
![PyPI Version](https://img.shields.io/pypi/v/riocloud-reader)
![Python Version](https://img.shields.io/python version/3.10+)
![License](https://img.shields.io/badge/License-MIT-green)

Universal content reader — fetch, transcribe, and digest content from 30+ platforms. Combines the best of x-reader and DeepReader.

## Features

- 🐦 **Twitter/X** — FxTwitter API + Nitter fallback, supports tweets, threads, X Articles, profiles
- 🟠 **Reddit** — Native .json API, posts + comments + nested replies
- 🎬 **YouTube** — Transcripts in multiple languages
- 📰 **WeChat** — 微信公众号 articles (Jina + Playwright fallback)
- 📕 **Xiaohongshu** — 小红书 notes (with login session)
- 📡 **RSS** — Feedparser integration
- 💬 **Telegram** — Channel messages via Telethon
- 🎥 **Bilibili** — Video metadata + subtitles
- 🌐 **Generic** — Any URL via Trafilatura/Jina
- 📓 **NotebookLM** — Upload + generate Audio Overview
- 🤖 **MCP Server** — Expose as AI tools
- 🦞 **OpenClaw Skill** — Native integration

## Quick Start

```bash
# Install
pip install git+https://github.com/Riocloud/riocloud-reader.git

# Or with all dependencies
pip install "riocloud-reader[all] @ git+https://github.com/Riocloud/riocloud-reader.git"
playwright install chromium

# Use as CLI
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=xxx
riocloud-reader https://reddit.com/r/python/comments/xxx

# Use as Python library
from riocloud_reader import Reader

reader = Reader()
content = await reader.read("https://example.com/article")
print(content.title, content.content[:200])
```

## Documentation

- [English](README.md)
- [中文](README_zh.md)
- [日本語](README_ja.md)
- [한국어](README_ko.md)
- [Русский](README_ru.md)

## Architecture

```
riocloud_reader/
├── core/           # Router, storage, config
├── parsers/        # Platform-specific parsers
├── skills/         # OpenClaw skill
├── integrations/   # NotebookLM, etc.
├── mcp/           # MCP server
└── tests/         # Unit tests
```

## License

MIT
