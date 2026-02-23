# Riocloud Reader
通用内容读取器 — 从 30+ 平台获取、转录和解析内容。

## 功能特点

- 🐦 **Twitter/X** — FxTwitter API + Nitter 后备，支持推文、话题、X 文章、资料
- 🟠 **Reddit** — 原生 .json API，支持帖子和评论
- 🎬 **YouTube** — 多语言字幕提取
- 📰 **微信** — 微信公众号文章 (Jina + Playwright 后备)
- 📕 **小红书** — 小红书笔记 (需登录会话)
- 📡 **RSS** — Feedparser 集成
- 💬 **Telegram** — 频道消息 (需 Telethon)
- 🎥 **B站** — 视频元数据 + 字幕
- 🌐 **通用** — 任意 URL via Trafilatura/Jina
- 📓 **NotebookLM** — 上传 + 生成音频概览
- 🤖 **MCP Server** — 暴露为 AI 工具
- 🦞 **OpenClaw Skill** — 原生集成

## 快速开始

```bash
# 安装
pip install git+https://github.com/Riocloud/riocloud-reader.git

# 或安装所有依赖
pip install "riocloud-reader[all] @ git+https://github.com/Riocloud/riocloud-reader.git"
playwright install chromium

# CLI 使用
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=xxx
riocloud-reader https://reddit.com/r/python/comments/xxx

# Python 库使用
from riocloud_reader import Reader

reader = Reader()
content = await reader.read("https://example.com/article")
print(content.title, content.content[:200])
```

## 支持的平台

| 平台 | 支持 | 方法 |
|------|------|------|
| Twitter/X | ✅ | FxTwitter API + Nitter |
| Reddit | ✅ | 原生 .json API |
| YouTube | ✅ | youtube-transcript-api |
| 微信 | ✅ | Jina + Playwright |
| 小红书 | ✅ | Jina + Playwright + 登录 |
| Bilibili | ✅ | API |
| RSS | ✅ | feedparser |
| Telegram | ✅ | Telethon |
| 通用网页 | ✅ | Trafilatura / Jina |

## 架构

```
riocloud_reader/
├── core/           # 路由、存储、配置
├── parsers/        # 平台解析器
├── skills/         # OpenClaw Skill
├── integrations/   # NotebookLM 等
├── mcp/           # MCP 服务器
└── tests/         # 单元测试
```

## 配置

可选环境变量:

- `TG_API_ID` - Telegram API ID (需要 Telegram 支持)
- `TG_API_HASH` - Telegram API Hash
- `GROQ_API_KEY` - Whisper 转录用 (免费)
- `FXTWITTER_API_URL` - 自定义 FxTwitter API 地址

## 许可证

MIT
