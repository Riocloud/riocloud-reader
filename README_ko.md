# Riocloud Reader

![PyPI](https://img.shields.io/pypi/v/riocloud-reader)
![Python](https://img.shields.io/pypi/pyversions/riocloud-reader)
![License](https://img.shields.io/github/license/Riocloud/riocloud-reader)

AI 에이전트를 위한 범용 콘텐츠 리더. 30개 이상의 플랫폼에서 몇 초 만에 콘텐츠를 가져오고, 전사하고, 요약합니다.

## 개요

Riocloud Reader는 AI 에이전트와 개발자를 위해 설계된 강력한 범용 콘텐츠 리더입니다. 다양한 온라인 플랫폼에서 콘텐츠를 가져오고, 텍스트와 자막을 추출하며, LLM 섭취에 완벽한 구조화된 데이터를 반환합니다.

트위터 게시물, YouTube 비디오, Reddit 게시물, 뉴스 기사를 읽어야 하든, WeChat 및 Bilibili과 같은 중국 플랫폼의 콘텐츠를 읽어야 하든, Riocloud Reader는 간단하고 통합된 API로 모든 것을 처리합니다.

## 주요 기능

- **제로 설정** - 대부분의 플랫폼은 API 키 없이 즉시 작동
- **30개 이상 플랫폼 지원** - Twitter/X, Reddit, YouTube, WeChat, Bilibili, RSS 등
- **다양한 형식 출력** - 제목, 콘텐츠, 작성자, 타임스탬프, 메타데이터를 포함한 구조화된 데이터 반환
- **다중 인터페이스** - CLI 도구, Python 라이브러리, MCP 서버, OpenClaw 스킬
- **크로스 플랫폼** - Linux, macOS, Windows에서 작동

## 지원 플랫폼

### Twitter/X
- 전체 텍스트가 포함된 일반 트윗
- 긴 트윗 (Twitter Blue)
- X Articles (장문 콘텐츠)
- 중첩된 콘텐츠가 포함된 인용 트윗
- 답글 스레드 (Nitter 폴백을 통해 최대 5개)
- 프로필 스냅샷 (바이오 및 통계 포함)
- 참여 지표 (좋아요, 리트윗, 조회수, 북마크)

### Reddit
- 전체 마크다운 본문이 있는 자기 게시물
- URL 및 메타데이터가 있는 링크 게시물
- 상위 댓글 (최대 15개, 점수 순)
- 중첩된 답글 스레드 (최대 3단계)
- 미디어 URL (이미지, 갤러리, 비디오)
- 게시물 통계 (점수, 댓글 수,赞成 비율)
- 플레어 태그

### YouTube
- 다국어 비디오 자막
- 비디오 메타데이터 (제목, 설명, 채널, 재생 시간)
- 다양한 URL 형식 지원:
  - youtube.com/watch?v=xxx
  - youtu.be/xxx
  - youtube.com/embed/xxx

### WeChat (微信公众号)
- 공식 계정 기사
- Jina Reader를 주요 가져오기 방법으로
- 스크래핑 방지 페이지의 Playwright 폴백

### Xiaohongshu (小红书)
- 노트 및 게시물
- 이미지 및 미디어 URL
- 인증 요청을 위한 세션이 있는 Playwright

### Bilibili
- 비디오 메타데이터
- 자막
- bilibili.com 및 b23.tv 단축 링크 지원

### RSS/Atom
- 모든 표준 RSS 또는 Atom 피드
- 피드 URL 자동 감지

### Telegram
- 채널 메시지
- my.telegram.org의 TG_API_ID 및 TG_API_HASH 필요

### 범용 (모든 URL)
- Trafilatura를 통한 모든 웹페이지
- Jina Reader 폴백
- 최선의 노력으로 콘텐츠 추출

### NotebookLM (통합)
- 소스로 콘텐츠 업로드
- 오디오 개요 생성 (팟캐스트 스타일)
- Google 인증 필요

## 설치

### 기본 설치

```bash
pip install riocloud-reader
```

### 모든 종속성과 함께

```bash
pip install "riocloud-reader[all]"
playwright install chromium
```

### 선택적 종속성

```bash
# 브라우저 지원 (WeChat, Xiaohongshu)
pip install "riocloud-reader[browser]"

# YouTube 자막
pip install "riocloud-reader[youtube]"

# Telegram 지원
pip install "riocloud-reader[telegram]"

# NotebookLM 통합
pip install "riocloud-reader[notebooklm]"

# 범용 URL 파싱
pip install "riocloud-reader[generic]"

# 개발 및 테스트
pip install "riocloud-reader[dev]"
```

## 사용법

### 명령줄 인터페이스

```bash
# 단일 URL 읽기
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=dQw4w9WgXcQ
riocloud-reader https://reddit.com/r/python/comments/abc123

# 여러 URL 읽기
riocloud-reader https://url1.com https://url2.com

# 출력을 파일에 저장
riocloud-reader https://example.com/article --output article.md

# 출력 형식 지정
riocloud-reader https://example.com --format json
```

### Python 라이브러리

```python
import asyncio
from riocloud_reader import Reader

async def main():
    # 리더 초기화
    reader = Reader()
    
    # 단일 URL 읽기
    content = await reader.read("https://twitter.com/user/status/123456")
    print(f"제목: {content.title}")
    print(f"콘텐츠: {content.content[:500]}")
    
    # 여러 URL 배치로 읽기
    results = await reader.read_batch([
        "https://twitter.com/user/status/1",
        "https://reddit.com/r/python/comments/abc",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
    ])
    
    for result in results:
        print(f"URL: {result.url}")
        print(f"제목: {result.title}")

asyncio.run(main())
```

### OpenClaw 스킬

```python
from skills.reader import run

# 에이전트 메모리에 직접 콘텐츠 읽기
result = run("이 트윗 확인: https://x.com/elonmusk/status/123456")
result = run("이 비디오 자막 가져오기: https://youtube.com/watch?v=dQw4w9WgXcQ")
```

### MCP 서버

MCP 서버 시작:

```bash
python -m riocloud_reader.mcp
```

Claude Desktop 구성에서 구성 (claude_desktop_config.json):

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

## 구성

### 환경 변수

| 변수 | 필요 | 설명 |
|------|------|------|
| TG_API_ID | Telegram | my.telegram.org의 API ID |
| TG_API_HASH | Telegram | my.telegram.org의 API 해시 |
| GROQ_API_KEY | Whisper | console.groq.com의 무료 API 키 |
| FIRECRAWL_API_KEY | Firecrawl | 선택 사항, 유료 콘텐츠용 |
| DEEPREEDER_MEMORY_PATH | 스토리지 | 콘텐츠를 저장할 디렉토리 |

### 구성 파일

`.env` 파일 생성:

```bash
cp .env.example .env
# 자격 증명으로 편집
```

## 아키텍처

```
riocloud_reader/
├── parsers/                  # 플랫폼별 파서
│   ├── base.py              # 기본 파서 클래스 및 유틸리티
│   ├── twitter.py           # Twitter/X 파서 (FxTwitter + Nitter)
│   ├── reddit.py            # Reddit 파서 (.json API)
│   ├── youtube.py           # YouTube 자막 파서
│   ├── wechat.py            # WeChat 기사 파서
│   ├── xhs.py               # Xiaohongshu 파서
│   ├── bilibili.py          # Bilibili 파서
│   ├── rss.py               # RSS/Atom 피드 파서
│   ├── telegram.py          # Telegram 채널 파서
│   └── generic.py           # 범용 URL 파서 (Trafilatura)
├── core/                     # 핵심 기능
│   ├── router.py            # 적절한 파서로 URL 라우팅
│   ├── storage.py           # 파일 I/O 유틸리티
│   └── config.py            # 구성 관리
├── skills/                   # OpenClaw 스킬 통합
│   └── reader/              # OpenClaw 리더 스킬
├── integrations/            # 서드파티 통합
│   └── notebooklm.py       # NotebookLM API
├── mcp/                     # MCP 서버
│   └── server.py            # MCP 서버 구현
├── reader.py                # 기본 Reader 클래스
├── schema.py                # 데이터 모델 및 스키마
└── cli.py                   # CLI 인터페이스
```

## 개발

### 개발 환경 설정

```bash
# 저장소克隆
git clone https://github.com/Riocloud/riocloud-reader.git
cd riocloud-reader

# 개발 모드로 설치
pip install -e ".[dev]"

# 모든 선택적 종속성 설치
pip install -e ".[all]"
playwright install chromium
```

### 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/test_parsers.py

# 상세 출력으로 실행
pytest -v
```

### 코드 품질

```bash
# Black으로 코드 포맷
black .

# Ruff로 린트
ruff check .

# 린트 문제 수정
ruff check --fix .
```

## 라이선스

BSD-2-Clause 라이선스 - LICENSE 파일을 참조하세요.

## 지원

- 문제 보고: https://github.com/Riocloud/riocloud-reader/issues
- 문서: https://github.com/Riocloud/riocloud-reader#readme

## 관련 프로젝트

- [x-reader](https://github.com/runesleo/x-reader) - 원래 범용 콘텐츠 리더
- [OpenClaw-DeepReeder](https://github.com/astonysh/OpenClaw-DeepReeder) - OpenClaw 내장 리더
