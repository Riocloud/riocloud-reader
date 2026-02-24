# Riocloud Reader

![PyPI](https://img.shields.io/pypi/v/riocloud-reader)
![Python](https://img.shields.io/pypi/pyversions/riocloud-reader)
![License](https://img.shields.io/github/license/Riocloud/riocloud-reader)

Универсальный инструмент чтения контента для ИИ-агентов. Получайте, транскрибируйте и обрабатывайте контент с 30+ платформ за секунды.

## Обзор

Riocloud Reader — мощный универсальный инструмент чтения контента, разработанный для ИИ-агентов и разработчиков. Он может получать контент с различных онлайн-платформ, извлекать текст и транскрипции и возвращать структурированные данные, идеально подходящие для обработки LLM.

Нужно ли вам читать твиты, видео с YouTube, посты на Reddit, новостные статьи или контент с китайских платформ, таких как WeChat и Bilibili, Riocloud Reader справляется со всем этим через простой унифицированный API.

## Ключевые функции

- **Нулевая настройка** - Работает из коробки для большинства платформ, без API-ключей
- **Поддержка 30+ платформ** - Twitter/X, Reddit, YouTube, WeChat, Bilibili, RSS и многое другое
- **Мультиформатный вывод** - Возвращает структурированные данные: заголовок, контент, автор, временные метки и метаданные
- **Несколько интерфейсов** - CLI-инструмент, Python-библиотека, MCP-сервер и навык OpenClaw
- **Кроссплатформенность** - Работает на Linux, macOS и Windows

## Поддерживаемые платформы

### Twitter/X
- Обычные твиты с полным текстом
- Длинные твиты (Twitter Blue)
- X Articles (длинный контент)
- Цитируемые твиты с вложенным контентом
- Цепочки ответов (до 5 через Nitter)
- Снимки профилей с биографией и статистикой
- Показатели вовлечённости (лайки, ретвиты, просмотры, закладки)

### Reddit
- Посты с полным markdown-текстом
- Посты-ссылки с URL и метаданными
- Топ-комментарии (до 15, по убыванию рейтинга)
- Вложенные цепочки ответов (до 3 уровней)
- URL-адреса медиафайлов (изображения, галереи, видео)
- Статистика поста (очки, количество комментариев, процент upvote)
- Теги

### YouTube
- Транскрипции видео на нескольких языках
- Метаданные видео (название, описание, канал, длительность)
- Поддержка различных форматов URL:
  - youtube.com/watch?v=xxx
  - youtu.be/xxx
  - youtube.com/embed/xxx

### WeChat (Официальные аккаунты WeChat)
- Статьи из официальных аккаунтов
- Jina Reader как основной метод получения
- Playwright для страниц с защитой от парсинга

### Xiaohongshu (小红书)
- Заметки и посты
- URL-адреса изображений и медиа
- Playwright с сессией для авторизованных запросов

### Bilibili
- Метаданные видео
- Субтитры
- Поддержка bilibili.com и коротких ссылок b23.tv

### RSS/Atom
- Любые стандартные RSS- или Atom-ленты
- Автоопределение URL-лент

### Telegram
- Сообщения каналов
- Требует TG_API_ID и TG_API_HASH от my.telegram.org

### Generic (Любой URL)
- Любая веб-страница через Trafilatura
- Jina Reader как запасной вариант
- Извлечение контента по возможности

### NotebookLM (Интеграция)
- Загрузка контента как источников
- Генерация аудиообзора (подкаст-стиль)
- Требует аутентификацию Google

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

# Транскрипции YouTube
pip install "riocloud-reader[youtube]"

# Поддержка Telegram
pip install "riocloud-reader[telegram]"

# Интеграция NotebookLM
pip install "riocloud-reader[notebooklm]"

# Парсинг generic URL
pip install "riocloud-reader[generic]"

# Разработка и тестирование
pip install "riocloud-reader[dev]"
```

## Использование

### Интерфейс командной строки

```bash
# Прочитать один URL
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=dQw4w9WgXcQ
riocloud-reader https://reddit.com/r/python/comments/abc123

# Прочитать несколько URL
riocloud-reader https://url1.com https://url2.com

# Сохранить вывод в файл
riocloud-reader https://example.com/article --output article.md

# Указать формат вывода
riocloud-reader https://example.com --format json
```

### Python-библиотека

```python
import asyncio
from riocloud_reader import Reader

async def main():
    # Инициализировать ридер
    reader = Reader()
    
    # Прочитать один URL
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

### Навык OpenClaw

```python
from skills.reader import run

# Прочитать контент напрямую в память агента
result = run("Посмотри этот твит: https://x.com/elonmusk/status/123456")
result = run("Получи транскрипт: https://youtube.com/watch?v=dQw4w9WgXcQ")
```

### MCP-сервер

Запустить MCP-сервер:

```bash
python -m riocloud_reader.mcp
```

Настроить в конфиге Claude Desktop (claude_desktop_config.json):

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

## Конфигурация

### Переменные окружения

| Переменная | Требуется для | Описание |
|------------|---------------|---------|
| TG_API_ID | Telegram | API ID от my.telegram.org |
| TG_API_HASH | Telegram | API Hash от my.telegram.org |
| GROQ_API_KEY | Whisper | Бесплатный ключ от console.groq.com |
| FIRECRAWL_API_KEY | Firecrawl | Опционально, для платного контента |
| DEEPREEDER_MEMORY_PATH | Хранилище | Папка для сохранения контента |

### Конфигурационный файл

Создайте файл `.env`:

```bash
cp .env.example .env
# Отредактируйте с вашими учетными данными
```

## Архитектура

```
riocloud_reader/
├── parsers/                  # Парсеры для конкретных платформ
│   ├── base.py              # Базовый класс парсера и утилиты
│   ├── twitter.py           # Парсер Twitter/X (FxTwitter + Nitter)
│   ├── reddit.py            # Парсер Reddit (.json API)
│   ├── youtube.py           # Парсер транскрипций YouTube
│   ├── wechat.py            # Парсер статей WeChat
│   ├── xhs.py               # Парсер Xiaohongshu
│   ├── bilibili.py          # Парсер Bilibili
│   ├── rss.py               # Парсер RSS/Atom лент
│   ├── telegram.py          # Парсер каналов Telegram
│   └── generic.py           # Парсер generic URL (Trafilatura)
├── core/                     # Основной функционал
│   ├── router.py            # Маршрутизация URL к парсеру
│   ├── storage.py           # Утилиты для работы с файлами
│   └── config.py            # Управление конфигурацией
├── skills/                   # Интеграция навыков OpenClaw
│   └── reader/              # Навык чтения OpenClaw
├── integrations/            # Сторонние интеграции
│   └── notebooklm.py       # API NotebookLM
├── mcp/                     # MCP-сервер
│   └── server.py            # Реализация MCP-сервера
├── reader.py                # Главный класс Reader
├── schema.py                # Модели данных и схемы
└── cli.py                   # CLI-интерфейс
```

## Разработка

### Настройка окружения разработки

```bash
# Клонировать репозиторий
git clone https://github.com/Riocloud/riocloud-reader.git
cd riocloud-reader

# Установить в режиме разработки
pip install -e ".[dev]"

# Установить все опциональные зависимости
pip install -e ".[all]"
playwright install chromium
```

### Запуск тестов

```bash
# Запустить все тесты
pytest

# Запустить конкретный файл тестов
pytest tests/test_parsers.py

# Запустить с подробным выводом
pytest -v
```

### Качество кода

```bash
# Форматировать код с Black
black .

# Проверять код с Ruff
ruff check .

# Исправлять проблемы
ruff check --fix .
```

## Лицензия

BSD-2-Clause License - подробности в файле LICENSE.

## Поддержка

- Сообщить о проблемах: https://github.com/Riocloud/riocloud-reader/issues
- Документация: https://github.com/Riocloud/riocloud-reader#readme

## Связанные проекты

- [x-reader](https://github.com/runesleo/x-reader) - Оригинальный универсальный инструмент чтения
- [OpenClaw-DeepReeder](https://github.com/astonysh/OpenClaw-DeepReeder) - Встроенный ридер OpenClaw
