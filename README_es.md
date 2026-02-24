# Riocloud Reader

![PyPI](https://img.shields.io/pypi/v/riocloud-reader)
![Python](https://img.shields.io/pypi/pyversions/riocloud-reader)
![License](https://img.shields.io/github/license/Riocloud/riocloud-reader)

Lector de contenido universal para agentes de IA. Obtén, transcribe y digiere contenido de más de 30 plataformas en segundos.

## Descripción

Riocloud Reader es un potente lector de contenido universal diseñado para agentes de IA y desarrolladores. Puede obtener contenido de varias plataformas en línea, extraer texto y transcripciones, y devolver datos estructurados perfectos para la ingestión de LLM.

Ya necesites leer tweets, videos de YouTube, publicaciones de Reddit, artículos de noticias o contenido de plataformas chinas como WeChat y Bilibili, Riocloud Reader lo maneja todo a través de una API simple y unificada.

## Características Principales

- **Cero Configuración** - Funciona de inmediato para la mayoría de las plataformas, sin necesidad de claves API
- **Soporte para más de 30 plataformas** - Twitter/X, Reddit, YouTube, WeChat, Bilibili, RSS y más
- **Salida Multi-Formato** - Devuelve datos estructurados incluyendo título, contenido, autor, marcas de tiempo y metadatos
- **Múltiples Interfaces** - Herramienta CLI, biblioteca Python, servidor MCP y skill de OpenClaw
- **Multiplataforma** - Funciona en Linux, macOS y Windows

## Plataformas Soportadas

### Twitter/X
- Tweets regulares con texto completo
- Tweets largos (Twitter Blue)
- X Articles (contenido largo)
- Tweets citados con contenido anidado
- Hilos de respuestas (hasta 5 mediante fallback de Nitter)
- Capturas de perfil con biografía y estadísticas
- Métricas de engagement (likes, retweets, vistas, marcadores)

### Reddit
- Publicaciones propias con cuerpo markdown completo
- Publicaciones de enlace con URL y metadatos
- Mejores comentarios (hasta 15, ordenados por puntuación)
- Hilos de respuestas anidados (hasta 3 niveles)
- URLs de medios (imágenes, galerías, videos)
- Estadísticas de publicación (puntuación, número de comentarios, proporción de upvotes)
- Etiquetas de categoría

### YouTube
- Transcripciones de video en múltiples idiomas
- Metadatos de video (título, descripción, canal, duración)
- Soporte para varios formatos de URL:
  - youtube.com/watch?v=xxx
  - youtu.be/xxx
  - youtube.com/embed/xxx

### WeChat (Cuentas Oficiales de WeChat)
- Artículos de cuentas oficiales
- Jina Reader como método principal de obtención
- Fallback de Playwright para páginas con protección contra scraping

### Xiaohongshu (Libro Rojo Pequeño)
- Notas y publicaciones
- URLs de imágenes y medios
- Playwright con sesión para solicitudes autenticadas

### Bilibili
- Metadatos de video
- Subtítulos
- Soporte para bilibili.com y enlaces cortos b23.tv

### RSS/Atom
- Cualquier fuente RSS o Atom estándar
- Detección automática de URLs de fuentes

### Telegram
- Mensajes de canales
- Requiere TG_API_ID y TG_API_HASH de my.telegram.org

### Genérico (Cualquier URL)
- Cualquier página web a través de Trafilatura
- Jina Reader como fallback
- Extracción de contenido por mejor esfuerzo

### NotebookLM (Integración)
- Subir contenido como fuentes
- Generar descripción de audio (estilo podcast)
- Requiere autenticación de Google

## Instalación

### Instalación Básica

```bash
pip install riocloud-reader
```

### Con Todas las Dependencias

```bash
pip install "riocloud-reader[all]"
playwright install chromium
```

### Dependencias Opcionales

```bash
# Soporte de navegador (WeChat, Xiaohongshu)
pip install "riocloud-reader[browser]"

# Transcripciones de YouTube
pip install "riocloud-reader[youtube]"

# Soporte de Telegram
pip install "riocloud-reader[telegram]"

# Integración con NotebookLM
pip install "riocloud-reader[notebooklm]"

# Parseo de URLs genéricas
pip install "riocloud-reader[generic]"

# Desarrollo y pruebas
pip install "riocloud-reader[dev]"
```

## Uso

### Interfaz de Línea de Comandos

```bash
# Leer una URL única
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
    
    # Leer una URL única
    content = await reader.read("https://twitter.com/user/status/123456")
    print(f"Título: {content.title}")
    print(f"Contenido: {content.content[:500]}")
    
    # Leer múltiples URLs en lote
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

# Leer contenido directamente en memoria del agente
result = run("Mira este tweet: https://x.com/elonmusk/status/123456")
result = run("Obtén la transcripción de: https://youtube.com/watch?v=dQw4w9WgXcQ")
```

### Servidor MCP

Iniciar el servidor MCP:

```bash
python -m riocloud_reader.mcp
```

Configurar en tu configuración de Claude Desktop (claude_desktop_config.json):

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

### Variables de Entorno

| Variable | Requiere | Descripción |
|----------|----------|-------------|
| TG_API_ID | Telegram | API ID de my.telegram.org |
| TG_API_HASH | Telegram | API Hash de my.telegram.org |
| GROQ_API_KEY | Whisper | Clave API gratuita de console.groq.com |
| FIRECRAWL_API_KEY | Firecrawl | Opcional, para contenido de pago |
| DEEPREEDER_MEMORY_PATH | Almacenamiento | Directorio para guardar contenido |

### Archivo de Configuración

Crear archivo `.env`:

```bash
cp .env.example .env
# Editar con tus credenciales
```

## Arquitectura

```
riocloud_reader/
├── parsers/                  # Analizadores específicos por plataforma
│   ├── base.py              # Clase base del analizador y utilidades
│   ├── twitter.py           # Analizador de Twitter/X (FxTwitter + Nitter)
│   ├── reddit.py            # Analizador de Reddit (.json API)
│   ├── youtube.py           # Analizador de transcripciones de YouTube
│   ├── wechat.py            # Analizador de artículos de WeChat
│   ├── xhs.py               # Analizador de Xiaohongshu
│   ├── bilibili.py          # Analizador de Bilibili
│   ├── rss.py               # Analizador de feeds RSS/Atom
│   ├── telegram.py          # Analizador de canales de Telegram
│   └── generic.py           # Analizador de URLs genéricas (Trafilatura)
├── core/                     # Funcionalidad principal
│   ├── router.py            # Enrutamiento de URL al analizador apropiado
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

### Configurar Entorno de Desarrollo

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

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar archivo de prueba específico
pytest tests/test_parsers.py

# Ejecutar con salida detallada
pytest -v
```

### Calidad de Código

```formatear código con Black
black .

# Verificar con Ruff
ruff check .

# Corregir problemas de linting
ruff check --fix .
```

## Licencia

Licencia MIT - consulta el archivo LICENSE.

## Soporte

- Reportar problemas: https://github.com/Riocloud/riocloud-reader/issues
- Documentación: https://github.com/Riocloud/riocloud-reader#readme

## Proyectos Relacionados

- [x-reader](https://github.com/runesleo/x-reader) - Lector de contenido universal original
- [OpenClaw-DeepReeder](https://github.com/astonysh/OpenClaw-DeepReeder) - Lector incorporado de OpenClaw
