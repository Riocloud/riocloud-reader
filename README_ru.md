# Riocloud Reader

![BSD-2-Clause](https://img.shields.io/badge/License-BSD--2--Clause-blue)

Универсальный ридер контента для AI-агентов. Получайте, расшифровывайте и систематизируйте контент с 30+ платформ за секунды.

## Обзор

Riocloud Reader — это мощный универсальный ридер контента, разработанный для AI-агентов и разработчиков. Он может получать контент с различных онлайн-платформ, извлекать текст и расшифровки и возвращать структурированные данные, идеально подходящие для LLM.

Независимо от того, нужно ли вам читать твиты, видео с YouTube, посты на Reddit, новостные статьи или контент с китайских платформ, таких как WeChat и Bilibili, Riocloud Reader обрабатывает всё это с помощью простого унифицированного API.

## Ключевые особенности

- **Нулевая настройка** — работает из коробки для большинства платформ, API ключи не требуются
- **Поддержка 30+ платформ** — Twitter/X, Reddit, YouTube, WeChat, Bilibili, RSS и другие
- **Мультиформатный вывод** — возвращает структурированные данные, включая заголовок, контент, автора, временные метки и метаданные
- **Несколько интерфейсов** — CLI инструмент, Python библиотека, MCP сервер и OpenClaw скилл
- **Кроссплатформенность** — работает на Linux, macOS и Windows
- **Усиленная безопасность** — встроенная защита от SSRF, предотвращение обхода путей, безопасные разрешения файлов сессий
- **AI транскрибация** — Groq Whisper fallback для YouTube видео без субтитров
- **Прямая интеграция с Obsidian** — сохранение контента напрямую в ваше хранилище Obsidian
- **Поддержка голых доменов** — используйте `example.com` напрямую в CLI

## Поддерживаемые платформы

### Twitter/X
- Обычные твиты с полным текстом
- Длинные твиты (Twitter Blue)
- X Статьи (длинный контент)
- Цитируемые твиты с вложенным контентом
- Ветки ответов (до 5 через Nitter)
- Снимки профилей с биографией и статистикой
- Показатели вовлечённости (лайки, ретвиты, просмотры, закладки)

### Reddit
- Посты с полным markdown текстом
- Ссылки с URL и метаданными
- Топ комментарии (до 15, по баллам)
- Вложенные ветки ответов (до 3 уровней)
- URL медиафайлов (изображения, галереи, видео)
- Статистика поста (баллы, количество комментариев, процент голосов)
- Теги

### YouTube
- Расшифровки видео на нескольких языках
- Метаданные видео (название, описание, канал, длительность)
- Поддержка различных URL форматов:
  - youtube.com/watch?v=xxx
  - youtu.be/xxx
  - youtube.com/embed/xxx

### WeChat (Официальные аккаунты)
- Статьи из официальных аккаунтов
- Jina Reader как основной метод получения
- Playwright для страниц с защитой от парсинга

### Xiaohongshu (小红书)
- Заметки и посты
- Изображения и URL медиафайлов
- Playwright с сессией для авторизованных запросов

### Bilibili
- Метаданные видео
- Субтитры
- Поддержка bilibili.com и коротких ссылок b23.tv

### RSS/Atom
- Любые стандартные RSS или Atom фиды
- Автоопределение URL фида

### Telegram
- Сообщения каналов
- Требует TG_API_ID и TG_API_HASH от my.telegram.org

### Универсальный (любой URL)
- Любая веб-страница через Trafilatura
- Jina Reader как резервный вариант
- Извлечение контента по возможности

### NotebookLM (Интеграция)
- Загрузка контента как источников
- Генерация Аудио Обзора (подкаст-стиль)
- Требует Google аутентификацию

## Установка

### Базовая установка

```bash
pip install riocloud-reader
```

### Со всеми зависимостями

```bash
pip install "riocloud-reader[all]"
playwright install chromium
```

### Дополнительные зависимости

```bash
# Поддержка браузера (WeChat, Xiaohongshu)
pip install "riocloud-reader[browser]"

# Расшифровки YouTube
pip install "riocloud-reader[youtube]"

# Поддержка Telegram
pip install "riocloud-reader[telegram]"

# Интеграция NotebookLM
pip install "riocloud-reader[notebooklm]"

# Универсальный парсинг URL
pip install "riocloud-reader[generic]"

# Разработка и тестирование
pip install "riocloud-reader[dev]"
```

## Использование

### Интерфейс командной строки

```bash
# Чтение одного URL
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=dQw4w9WgXcQ
riocloud-reader https://reddit.com/r/python/comments/abc123

# Чтение нескольких URL
riocloud-reader https://url1.com https://url2.com

# Сохранение вывода в файл
riocloud-reader https://example.com/article --output article.md

# Указание формата вывода
riocloud-reader https://example.com --format json
```

### Python библиотека

```python
import asyncio
from riocloud_reader import Reader

async def main():
    # Инициализация ридера
    reader = Reader()
    
    # Чтение одного URL
    content = await reader.read("https://twitter.com/user/status/123456")
    print(f"Заголовок: {content.title}")
    print(f"Контент: {content.content[:500]}")
    
    # Пакетное чтение нескольких URL
    results = await reader.read_batch([
        "https://twitter.com/user/status/1",
        "https://reddit.com/r/python/comments/abc",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
    ])
    
    for result in results:
        print(f"URL: {result.url}")
        print(f"Заголовок: {result.title}")

asyncio.run(main())
```

### OpenClaw скилл

```python
from skills.reader import run

# Чтение контента напрямую в память агента
result = run("Посмотри этот твит: https://x.com/elonmusk/status/123456")
result = run("Получи расшифровку: https://youtube.com/watch?v=dQw4w9WgXcQ")
```

### MCP сервер

Запуск MCP сервера:

```bash
python -m riocloud_reader.mcp
```

Настройка в Claude Desktop (claude_desktop_config.json):

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

## Настройка

### Переменные окружения

| Переменная | Требуется | Описание |
|------------|-----------|----------|
| TG_API_ID | Telegram | API ID от my.telegram.org |
| TG_API_HASH | Telegram | API Hash от my.telegram.org |
| GROQ_API_KEY | YouTube Whisper | Бесплатный API ключ от console.groq.com |
| FIRECRAWL_API_KEY | Firecrawl | Опционально, для платного контента |
| DEEPREEDER_MEMORY_PATH | Хранилище | Директория для сохранения контента |
| OBSIDIAN_VAULT | Obsidian | Путь к хранилищу по умолчанию для флага --obsidian |

## Продвинутые функции

### Groq Whisper Fallback для YouTube

Когда у видео YouTube нет субтитров, riocloud-reader автоматически использует Groq Whisper API для расшифровки.

```bash
# Установите ключ Groq API
export GROQ_API_KEY=ваш_groq_api_ключ

# Теперь любое видео YouTube будет расшифровано
riocloud-reader https://youtube.com/watch?v=xxx
```

Получите бесплатный API ключ: https://console.groq.com/

### Поддержка голых доменов

Вы можете использовать имена доменов без префикса https://:

```bash
riocloud-reader example.com
riocloud-reader example.com/путь
riocloud-reader twitter.com/elonmusk/status/123456
```

### Интеграция с хранилищем Obsidian

Сохраняйте контент напрямую в хранилище Obsidian:

```bash
# Сохранить в хранилище Obsidian
riocloud-reader https://youtube.com/watch?v=xxx --obsidian /путь/_к/хранилищу

# Или используйте переменную окружения
export OBSIDIAN_VAULT=/путь/_к/хранилищу
riocloud-reader https://twitter.com/user/status/123
```

Создаёт структуру папок по дате:
```
хранилище/
├── 2026-02/
│   ├── youtube/
│   │   └── dQw4w9WgXcQ_Тестовое_видео.md
│   └── twitter/
│       └── abc123_Твит_пользователя.md
```

### Сессия входа в Twitter

Для лучшего покрытия Twitter/X войдите в систему для сохранения сессии:

```bash
# Сначала войдите (откроется браузер)
riocloud-reader login twitter

# Затем используйте Twitter URL — будет использована сессия если доступна
riocloud-reader https://x.com/user/status/123456
```

Использует трёхуровневое падение: FxTwitter API → Nitter → Playwright сессия

Создайте файл `.env`:

```bash
cp .env.example .env
# Редактируйте ваши учетные данные
```

## Архитектура

```
riocloud_reader/
├── parsers/                  # Парсеры для платформ
│   ├── base.py              # Базовый класс парсера и утилиты
│   ├── twitter.py           # Парсер Twitter/X (FxTwitter + Nitter)
│   ├── reddit.py            # Парсер Reddit (.json API)
│   ├── youtube.py           # Парсер расшифровок YouTube
│   ├── wechat.py            # Парсер статей WeChat
│   ├── xhs.py               # Парсер Xiaohongshu
│   ├── bilibili.py          # Парсер Bilibili
│   ├── rss.py               # Парсер RSS/Atom фидов
│   ├── telegram.py          # Парсер каналов Telegram
│   └── generic.py           # Универсальный парсер URL (Trafilatura)
├── core/                     # Основной функционал
│   ├── router.py            # Маршрутизация URL к парсеру
│   ├── storage.py           # Утилиты для работы с файлами
│   └── config.py            # Управление конфигурацией
├── skills/                   # Интеграция OpenClaw скиллов
│   └── reader/              # Скилл ридера для OpenClaw
├── integrations/            # Сторонние интеграции
│   └── notebooklm.py       # API NotebookLM
├── mcp/                     # MCP сервер
│   └── server.py            # Реализация MCP сервера
├── reader.py                # Главный класс Reader
├── schema.py                # Модели данных и схемы
└── cli.py                   # CLI интерфейс
```

## Разработка

### Настройка среды разработки

```bash
# Клонирование репозитория
git clone https://github.com/Riocloud/riocloud-reader.git
cd riocloud-reader

# Установка в режиме разработки
pip install -e ".[dev]"

# Установка всех опциональных зависимостей
pip install -e ".[all]"
playwright install chromium
```

### Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск конкретного файла тестов
pytest tests/test_parsers.py

# Запуск с подробным выводом
pytest -v
```

### Качество кода

```bash
# Форматирование кода с Black
black .

# Проверка линтером Ruff
ruff check .

# Исправление проблем линтера
ruff check --fix .
```

## Лицензия

BSD 2-Clause License — подробности в файле LICENSE.

## Языки

Этот README доступен на других языках:
- [English](README.md)
- [中文](README_zh.md)
- [Español](README_es.md)
- [日本語](README_ja.md)
- [한국어](README_ko.md)
- [Русский](README_ru.md)

## Поддержка

- Сообщить о проблемах: https://github.com/Riocloud/riocloud-reader/issues
- Документация: https://github.com/Riocloud/riocloud-reader#readme

## Связанные проекты

- [x-reader](https://github.com/runesleo/x-reader) — Оригинальный универсальный ридер контента
- [OpenClaw-DeepReeder](https://github.com/astonysh/OpenClaw-DeepReeder) — Встроенный ридер OpenClaw
