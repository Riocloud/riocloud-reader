# Riocloud Reader
Универсальный ридер контента — получение, транскрибация и анализ контента с 30+ платформ.

## Возможности

- 🐦 **Twitter/X** — FxTwitter API + Nitter fallback
- 🟠 **Reddit** — Нативный .json API
- 🎬 **YouTube** — Субтитры на нескольких языках
- 📰 **WeChat** — Статьи WeChat (Jina + Playwright)
- 📕 **Xiaohongshu** — Заметки Xiaohongshu (требуется вход)
- 📡 **RSS** — Feedparser
- 💬 **Telegram** — Telethon
- 🎥 **Bilibili** — Метаданные видео
- 🌐 **Generic** — Trafilatura / Jina
- 📓 **NotebookLM** — Загрузка + генерация аудио
- 🤖 **MCP Server** — Инструменты для ИИ
- 🦞 **OpenClaw Skill** — Нативная интеграция

## Установка

```bash
pip install git+https://github.com/Riocloud/riocloud-reader.git

# Все зависимости
pip install "riocloud-reader[all] @ git+https://github.com/Riocloud/riocloud-reader.git"
playwright install chromium

# Примеры использования
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=xxx
```

## Поддерживаемые платформы

| Платформа | Поддержка | Метод |
|-----------|-----------|-------|
| Twitter/X | ✅ | FxTwitter API |
| Reddit | ✅ | .json API |
| YouTube | ✅ | youtube-transcript-api |
| WeChat | ✅ | Jina + Playwright |
| Xiaohongshu | ✅ | Jina + Playwright |
| Bilibili | ✅ | API |
| RSS | ✅ | feedparser |
| Telegram | ✅ | Telethon |
| Generic URL | ✅ | Trafilatura / Jina |

## Архитектура

```
riocloud_reader/
├── core/           # Роутер, хранилище, конфиг
├── parsers/        # Парсеры для платформ
├── skills/         # OpenClaw скил
├── integrations/   # NotebookLM и др.
├── mcp/           # MCP сервер
└── tests/         # Юнит-тесты
```

## Лицензия

MIT
