# Riocloud Reader
 универсальный内容リーダー — 30以上のプラットフォームからコンテンツを取得・ транскрибирует

## 機能

- 🐦 **Twitter/X** — FxTwitter API + Nitter フォールバック
- 🟠 **Reddit** — ネイティブ .json API
- 🎬 **YouTube** — 字幕（マルチ言語）
- 📰 **WeChat** — 微信公众号記事 (Jina + Playwright)
- 📕 **Xiaohongshu** — 小红書ノート（ログイン要）
- 📡 **RSS** — Feedparser
- 💬 **Telegram** — Telethon
- 🎥 **Bilibili** — 動画メタデータ
- 🌐 **通用** — Trafilatura / Jina
- 📓 **NotebookLM** — アップロード + オーディオ生成
- 🤖 **MCP Server** — AI ツールとして公開
- 🦞 **OpenClaw Skill** — ネイティブ統合

## インストール

```bash
pip install git+https://github.com/Riocloud/riocloud-reader.git

# 全依存関係
pip install "riocloud-reader[all] @ git+https://github.com/Riocloud/riocloud-reader.git"
playwright install chromium

# 使用例
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=xxx
```

## 対応プラットフォーム

| プラットフォーム | 対応 | メソッド |
|-----------------|------|---------|
| Twitter/X | ✅ | FxTwitter API |
| Reddit | ✅ | .json API |
| YouTube | ✅ | youtube-transcript-api |
| WeChat | ✅ | Jina + Playwright |
| Xiaohongshu | ✅ | Jina + Playwright |
| Bilibili | ✅ | API |
| RSS | ✅ | feedparser |
| Telegram | ✅ | Telethon |
| 汎用URL | ✅ | Trafilatura / Jina |

## アーキテクチャ

```
riocloud_reader/
├── core/           # ルーター、ストレージ、設定
├── parsers/        # プラットフォーム固有パーサー
├── skills/         # OpenClawスキル
├── integrations/   # NotebookLMなど
├── mcp/           # MCPサーバー
└── tests/         # ユニットテスト
```

## ライセンス

MIT
