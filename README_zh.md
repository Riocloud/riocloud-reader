# Riocloud Reader

![BSD-2-Clause](https://img.shields.io/badge/License-BSD--2--Clause-blue)

面向AI代理的通用内容读取器。几秒钟内从30+平台获取、转录和整理内容。

## 概述

Riocloud Reader是一款功能强大的通用内容读取器，专为AI代理和开发者设计。它可以从各种在线平台获取内容，提取文本和转录稿，并返回非常适合LLM摄入的结构化数据。

无论你需要阅读推文、YouTube视频、Reddit帖子、新闻文章，还是中国平台如微信和B站的内容，Riocloud Reader都能通过简单、统一的API处理一切。

## 主要特性

- **零配置** - 开箱即用，大多数平台无需API密钥
- **支持30+平台** - Twitter/X、Reddit、YouTube、微信、B站、RSS等
- **多格式输出** - 返回结构化数据，包括标题、内容、作者、时间戳和元数据
- **多种接口** - CLI工具、Python库、MCP服务器和OpenClaw技能
- **跨平台** - 支持Linux、macOS和Windows

## 为什么选择 Riocloud Reader?

Riocloud Reader 打通全网主流社交平台的"数据围墙"，不仅能绕过封锁和昂贵的接口限制，还能自动把视频、推文、长文翻译成 Markdown 格式，自动存入 Obsidian，实现真正的全网情报自动化监控。

- **全能采集** - 攻克微信、小红书的封锁难题，实现小红书免扫码长期采集，彻底告别 403 报错。

- **降本增效** - 无需购买昂贵的 Twitter API，通过自动化工具实现自由采集。

- **深度解析** - 集成 AI 语音转文字（Whisper），实现 YouTube 字幕秒出；B 站数据实现结构化提取。

- **实时同步** - 电报（Telegram）情报流实时接入。

- **闭环存储** - 异构数据统一标准化，直接对接 Obsidian，构建你的个人第二大脑。

## 支持的平台

### Twitter/X
- 完整文本的常规推文
- 长推文（Twitter Blue）
- X文章（长篇内容）
- 带嵌套内容的引用推文
- 回复线程（通过Nitter备用最多5条）
- 个人资料快照，包括简介和统计数据
- 参与度指标（点赞、转发、观看、收藏）

### Reddit
- 完整markdown正文的自我帖子
- 带URL和元数据的链接帖子
- 顶部评论（最多15条，按评分排序）
- 嵌套回复线程（最多3层）
- 媒体URL（图片、画廊、视频）
- 帖子统计（评分、评论数、点赞率）
- 标签

### YouTube
- 多语言视频转录稿
- 视频元数据（标题、描述、频道、时长）
- 支持各种URL格式：
  - youtube.com/watch?v=xxx
  - youtu.be/xxx
  - youtube.com/embed/xxx

### 微信公众号
- 公众号文章
- Jina Reader作为主要获取方式
- Playwright备用方案用于反爬取页面

### 小红书
- 笔记和帖子
- 图片和媒体URL
- Playwright配合会话用于认证请求

### B站
- 视频元数据
- 字幕
- 支持bilibili.com和b23.tv短链接

### RSS/Atom
- 任何标准RSS或Atom订阅源
- 自动检测订阅源URL

### Telegram
- 频道消息
- 需要从my.telegram.org获取TG_API_ID和TG_API_HASH

### 通用（任意URL）
- 通过Trafilatura处理任意网页
- Jina Reader作为备用
- 尽最大努力提取内容

### NotebookLM（集成）
- 将内容作为来源上传
- 生成音频概览（播客风格）
- 需要Google认证

## 安装

### 基本安装

```bash
pip install riocloud-reader
```

### 安装所有依赖

```bash
pip install "riocloud-reader[all]"
playwright install chromium
```

### 可选依赖

```bash
# 浏览器支持（微信、小红书）
pip install "riocloud-reader[browser]"

# YouTube转录稿
pip install "riocloud-reader[youtube]"

# Telegram支持
pip install "riocloud-reader[telegram]"

# NotebookLM集成
pip install "riocloud-reader[notebooklm]"

# 通用URL解析
pip install "riocloud-reader[generic]"

# 开发和测试
pip install "riocloud-reader[dev]"
```

## 使用方法

### 命令行界面

```bash
# 读取单个URL
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=dQw4w9WgXcQ
riocloud-reader https://reddit.com/r/python/comments/abc123

# 读取多个URL
riocloud-reader https://url1.com https://url2.com

# 保存输出到文件
riocloud-reader https://example.com/article --output article.md

# 指定输出格式
riocloud-reader https://example.com --format json
```

### Python库

```python
import asyncio
from riocloud_reader import Reader

async def main():
    # 初始化读取器
    reader = Reader()
    
    # 读取单个URL
    content = await reader.read("https://twitter.com/user/status/123456")
    print(f"标题: {content.title}")
    print(f"内容: {content.content[:500]}")
    
    # 批量读取多个URL
    results = await reader.read_batch([
        "https://twitter.com/user/status/1",
        "https://reddit.com/r/python/comments/abc",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
    ])
    
    for result in results:
        print(f"URL: {result.url}")
        print(f"标题: {result.title}")

asyncio.run(main())
```

### OpenClaw技能

```python
from skills.reader import run

# 直接读取内容到代理内存
result = run("查看这条推文: https://x.com/elonmusk/status/123456")
result = run("获取这个视频的转录稿: https://youtube.com/watch?v=dQw4w9WgXcQ")
```

### MCP服务器

启动MCP服务器：

```bash
python -m riocloud_reader.mcp
```

在Claude Desktop配置中配置（claude_desktop_config.json）：

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

## 配置

### 环境变量

| 变量 | 需要 | 描述 |
|------|------|------|
| TG_API_ID | Telegram | 来自my.telegram.org的API ID |
| TG_API_HASH | Telegram | 来自my.telegram.org的API Hash |
| GROQ_API_KEY | Whisper | 来自console.groq.com的免费API密钥 |
| FIRECRAWL_API_KEY | Firecrawl | 可选，用于付费内容 |
| DEEPREEDER_MEMORY_PATH | 存储 | 保存内容的目录 |

### 配置文件

创建`.env`文件：

```bash
cp .env.example .env
# 编辑你的凭证
```

## 架构

```
riocloud_reader/
├── parsers/                  # 平台特定解析器
│   ├── base.py              # 基础解析器类和工具
│   ├── twitter.py           # Twitter/X解析器（FxTwitter + Nitter）
│   ├── reddit.py            # Reddit解析器（.json API）
│   ├── youtube.py           # YouTube转录解析器
│   ├── wechat.py            # 微信文章解析器
│   ├── xhs.py               # 小红书解析器
│   ├── bilibili.py          # B站解析器
│   ├── rss.py               # RSS/Atom订阅解析器
│   ├── telegram.py          # Telegram频道解析器
│   └── generic.py           # 通用URL解析器（Trafilatura）
├── core/                     # 核心功能
│   ├── router.py            # URL路由到适当的解析器
│   ├── storage.py           # 文件I/O工具
│   └── config.py            # 配置管理
├── skills/                   # OpenClaw技能集成
│   └── reader/              # OpenClaw读取技能
├── integrations/            # 第三方集成
│   └── notebooklm.py       # NotebookLM API
├── mcp/                     # MCP服务器
│   └── server.py            # MCP服务器实现
├── reader.py                # 主读取器类
├── schema.py                # 数据模型和模式
└── cli.py                   # CLI接口
```

## 开发

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/Riocloud/riocloud-reader.git
cd riocloud-reader

# 以开发模式安装
pip install -e ".[dev]"

# 安装所有可选依赖
pip install -e ".[all]"
playwright install chromium
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_parsers.py

# 带详细输出运行
pytest -v
```

### 代码质量

```bash
# 使用Black格式化代码
black .

# 使用Ruff检查代码
ruff check .

# 修复代码问题
ruff check --fix .
```

## 许可证

BSD-2-Clause许可证 - 详见LICENSE文件。

## 支持

- 报告问题：https://github.com/Riocloud/riocloud-reader/issues
- 文档：https://github.com/Riocloud/riocloud-reader#readme

## 相关项目

- [x-reader](https://github.com/runesleo/x-reader) - 原始通用内容读取器
- [OpenClaw-DeepReeder](https://github.com/astonysh/OpenClaw-DeepReeder) - OpenClaw内置读取器
