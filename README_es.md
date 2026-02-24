# Riocloud Reader

![PyPI](https://img.shields.io/pypi/v/riocloud-reader)
![Python](https://img.shields.io/pypi/pyversions/riocloud-reader)
![License](https://img.shields.io/github/license/Riocloud/riocloud-reader)

Lector de contenido universal para agentes de IA. Obtén, transcribe y organiza contenido de más de 30 plataformas en segundos.

## Descripción general

Riocloud Reader es un potente lector de contenido universal diseñado para agentes de IA y desarrolladores. Puede obtener contenido de varias plataformas en línea, extraer texto y transcripciones, y devolver datos estructurados perfectos para ingestion por LLM.

Ya sea que necesites leer tweets, videos de YouTube, publicaciones de Reddit, artículos de noticias o contenido de plataformas chinas como WeChat y Bilibili, Riocloud Reader lo maneja todo con una API simple y unificada.

## Características principales

- **Cero configuración** - Funciona de inmediato para la mayoría de las plataformas, sin necesidad de claves API
- **Soporte para más de 30 plataformas** - Twitter/X, Reddit, YouTube, WeChat, Bilibili, RSS y más
- **Salida multiformato** - Devuelve datos estructurados incluyendo título, contenido, autor, marcas de tiempo y metadatos
- **Múltiples interfaces** - Herramienta CLI, biblioteca Python, servidor MCP y skill de OpenClaw
- **Multiplataforma** - Funciona en Linux, macOS y Windows

## Plataformas compatibles

### Twitter/X
- Tweets regulares con texto completo
- Tweets largos (Twitter Blue)
- Artículos de X (contenido largo)
- Tweets citados con contenido anidado
- Hilos de respuestas (hasta 5 vía Nitter)
- Capturas de perfil incluyendo bio y estadísticas
- Métricas de engagement (me gusta, retweets, vistas, marcadores)

### Reddit
- Publicaciones propias con cuerpo markdown completo
- Publicaciones de enlaces con URL y metadatos
- Comentarios principales (hasta 15, ordenados por puntuación)
- Hilos de respuestas anidados (hasta 3 niveles)
- URLs de medios (imágenes, galerías, videos)
- Estadísticas de publicación (puntuación, número de comentarios, ratio de votos)
- Etiquetas de categoría

### YouTube
- Transcripciones de video en múltiples idiomas
- Metadatos de video (título, descripción, canal, duración)
- Soporte para varios formatos de URL:
  - youtube.com/watch?v=xxx
  - youtu.be/xxx
  - youtube.com/embed/xxx

### WeChat (Cuentas Oficiales)
- Artículos de cuentas oficiales
- Jina Reader como método de obtención principal
- Playwright alternativo para páginas con anti-scraping

### Xiaohongshu (Libro Rojo Pequeño)
- Notas y publicaciones
- Imágenes y URLs de medios
- Playwright con sesión para solicitudes autenticadas

### Bilibili
- Metadatos de video
- Subtítulos
- Soporte para bilibili.com y enlaces cortos b23.tv

### RSS/Atom
- Cualquier feed RSS o Atom estándar
- Detección automática de URLs de feed

### Telegram
- Mensajes de canales
- Requiere TG_API_ID y TG_API_HASH de my.telegram.org

### Genérico (cualquier URL)
- Cualquier página web vía Trafilatura
- Jina Reader como alternativa
- Extracción de contenido por mejor esfuerzo

### NotebookLM (Integración)
- Subir contenido como fuentes
- Generar Descripción General de Audio (estilo podcast)
- Requiere autenticación de Google

## Instalación

### Instalación básica

```bash
pip install riocloud-reader
```

### Con todas las dependencias

```bash
pip install "riocloud-reader[all]"
playwright install chromium
```

### Dependencias opcionales

```bash
# Soporte de navegador (WeChat, Xiaohongshu)
pip install "riocloud-reader[browser]"

# Transcripciones de YouTube
pip install "riocloud-reader[youtube]"

# Soporte para Telegram
pip install "riocloud-reader[telegram]"

# Integración con NotebookLM
pip install "riocloud-reader[notebooklm]"

# Parsing de URL genérico
pip install "riocloud-reader[generic]"

# Desarrollo y pruebas
pip install "riocloud-reader[dev]"
```

## Uso

### Interfaz de línea de comandos

```bash
# Leer una URL individual
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=dQw4w9WgXcQ
riocloud-reader https://reddit.com/r/python/comments/abc123

# Leer múltiples URLs
riocloud-reader https://url1.com https://url2.com

# Guardar salida en archivo
riocloud-reader https://example.com/article --output article.md

# Especificar formato de salida
riocloud-reader https://example.com --format json
```

### Biblioteca Python

```python
import asyncio
from riocloud_reader import Reader

async def main():
    # Inicializar lector
    reader = Reader()
    
    # Leer una URL individual
    content = await reader.read("https://twitter.com/user/status/123456")
    print(f"Título: {content.title}")
    print(f"Contenido: {content.content[:500]}")
    
    # Lectura por lotes de múltiples URLs
    results = await reader.read_batch([
        "https://twitter.com/user/status/1",
        "https://reddit.com/r/python/comments/abc",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
    ])
    
    for result in results:
        print(f"URL: {result.url}")
        print(f"Título: {result.title}")

asyncio.run(main())
```

### Skill de OpenClaw

```python
from skills.reader import run

# Leer contenido directamente en la memoria del agente
result = run("Mira este tweet: https://x.com/elonmusk/status/123456")
result = run("Obtén la transcripción de: https://youtube.com/watch?v=dQw4w9WgXcQ")
```

### Servidor MCP

Iniciar el servidor MCP:

```bash
python -m riocloud_reader.mcp
```

Configurar en tu Claude Desktop (claude_desktop_config.json):

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

## Configuración

### Variables de entorno

| Variable | Requiere | Descripción |
|----------|----------|-------------|
| TG_API_ID | Telegram | API ID de my.telegram.org |
| TG_API_HASH | Telegram | API Hash de my.telegram.org |
| GROQ_API_KEY | Whisper | Clave API gratuita de console.groq.com |
| FIRECRAWL_API_KEY | Firecrawl | Opcional, para contenido de pago |
| DEEPREEDER_MEMORY_PATH | Almacenamiento | Directorio para guardar contenido |

### Archivo de configuración

Crear un archivo `.env`:

```bash
cp .env.example .env
# Editar con tus credenciales
```

## Arquitectura

```
riocloud_reader/
├── parsers/                  # Parsers específicos por plataforma
│   ├── base.py              # Clase base del parser y utilidades
│   ├── twitter.py           # Parser de Twitter/X (FxTwitter + Nitter)
│   ├── reddit.py            # Parser de Reddit (.json API)
│   ├── youtube.py           # Parser de transcripciones de YouTube
│   ├── wechat.py            # Parser de artículos de WeChat
│   ├── xhs.py               # Parser de Xiaohongshu
│   ├── bilibili.py          # Parser de Bilibili
│   ├── rss.py               # Parser de feeds RSS/Atom
│   ├── telegram.py          # Parser de canales de Telegram
│   └── generic.py           # Parser de URL genérico (Trafilatura)
├── core/                     # Funcionalidad principal
│   ├── router.py            # Enrutamiento de URL al parser apropiado
│   ├── storage.py           # Utilidades de E/S de archivos
│   └── config.py            # Gestión de configuración
├── skills/                   # Integración de skills de OpenClaw
│   └── reader/              # Skill de lector de OpenClaw
├── integrations/            # Integraciones de terceros
│   └── notebooklm.py       # API de NotebookLM
├── mcp/                     # Servidor MCP
│   └── server.py            # Implementación del servidor MCP
├── reader.py                # Clase principal Reader
├── schema.py                # Modelos de datos y esquemas
└── cli.py                   # Interfaz CLI
```

## Desarrollo

### Configurar entorno de desarrollo

```bash
# Clonar repositorio
git clone https://github.com/Riocloud/riocloud-reader.git
cd riocloud-reader

# Instalar en modo desarrollo
pip install -e ".[dev]"

# Instalar todas las dependencias opcionales
pip install -e ".[all]"
playwright install chromium
```

### Ejecutar pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar archivo de prueba específico
pytest tests/test_parsers.py

# Ejecutar con salida detallada
pytest -v
```

### Calidad del código

```formatear código con Black
black .

# Verificar con Ruff
ruff check .

# Corregir problemas de linting
ruff check --fix .
```

## Licencia

Licencia BSD 2-Clause - ver archivo LICENSE para detalles.

## Soporte

- Reportar problemas: https://github.com/Riocloud/riocloud-reader/issues
- Documentación: https://github.com/Riocloud/riocloud-reader#readme

## Proyectos relacionados

- [x-reader](https://github.com/runesleo/x-reader) - Lector de contenido universal original
- [OpenClaw-DeepReeder](https://github.com/astonysh/OpenClaw-DeepReeder) - Lector incorporado de OpenClaw
