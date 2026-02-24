# Riocloud Reader

![BSD-2-Clause](https://img.shields.io/badge/License-BSD--2--Clause-blue)

AI 에이전트를 위한 범용 콘텐츠 리더. 30개 이상의 플랫폼에서 몇 초 만에 콘텐츠를 가져오고, 전사하고, 정리합니다.

## 개요

Riocloud Reader는 AI 에이전트와 개발자를 위해 설계된 강력한 범용 콘텐츠 리더입니다. 다양한 온라인 플랫폼에서 콘텐츠를 가져오고, 텍스트와 전사를 추출하며, LLM 수집에 완벽한 구조화된 데이터를 반환합니다.

트위터, 유튜브 영상, 레딧 게시물, 뉴스 기사를 읽어야 하거나 위챗과 빌리빌리와 같은 중국 플랫폼의 콘텐츠가 필요하든, Riocloud Reader는 간단하고 통일된 API로的一切을 처리합니다.

## 주요 기능

- **제로 구성** - 대부분의 플랫폼에서 즉시 사용 가능, API 키 불필요
- **30개 이상 플랫폼 지원** - Twitter/X, Reddit, YouTube, 위챗, 빌리빌리, RSS 등
- **다양한 형식 출력** - 제목, 콘텐츠, 작성자, 타임스탬프 및 메타데이터를 포함하는 구조화된 데이터 반환
- **다양한 인터페이스** - CLI 도구, Python 라이브러리, MCP 서버, OpenClaw 스킬
- **크로스 플랫폼** - Linux, macOS, Windows에서 작동
- **보안 강화** - 기본 제공 SSRF 보호, 경로 탐색 방지, 안전한 세션 파일 권한
- **AI 전사** - 자막 없는 YouTube 동영상에 대한 Groq Whisper 폴백
- **Obsidian 직접 통합** - 콘텐츠를 Obsidian 볼트에 직접 저장
- **베어 도메인 지원** - CLI에서 `example.com`을 직접 사용

## 지원 플랫폼

### Twitter/X
- 전체 텍스트가 포함된 일반 트윗
- 긴 트윗 (Twitter Blue)
- X 아티클 (장문 콘텐츠)
- 중첩 콘텐츠가 포함된 인용 트윗
- 답글 스레드 (Nitter 폴백을 통해 최대 5개)
- 프로필 통계가 포함된 프로필 스냅샷
- 참여 지표 (좋아요, 리트윗, 조회, 북마크)

### Reddit
- 전체 마크다운 본문이 있는 셀프 게시물
- URL과 메타데이터가 포함된 링크 게시물
- 상위 댓글 (최대 15개, 점수순)
- 중첩된 답글 스레드 (최대 3단계)
- 미디어 URL (이미지, 갤러리, 비디오)
- 게시물 통계 (점수, 댓글 수,赞成율)
- 플레어 태그

### YouTube
- 여러 언어의 비디오 전사
- 비디오 메타데이터 (제목, 설명, 채널, 재생 시간)
- 다양한 URL 형식 지원:
  - youtube.com/watch?v=xxx
  - youtu.be/xxx
  - youtube.com/embed/xxx

### 위챗 (공식 계정)
- 공식 계정의 기사
- Jina Reader를 기본 가져오기로 사용
- 반스크래핑 페이지용 Playwright 폴백

### 샤오홍 Shu (샤오홍 Shu)
- 노트와 게시물
- 이미지와 미디어 URL
- 인증 요청용 세션이 있는 Playwright

### 빌리빌리
- 비디오 메타데이터
- 자막
- bilibili.com 및 b23.tv 단축 링크 지원

### RSS/Atom
- 모든 표준 RSS 또는 Atom 피드
- 피드 URL 자동 감지

### 텔레그램
- 채널 메시지
- my.telegram.org에서 TG_API_ID 및 TG_API_HASH 필요

### 일반 (모든 URL)
- Trafilatura를 통한 모든 웹페이지
- Jina Reader를 폴백으로
- 최선의 노력을 다한 콘텐츠 추출

### NotebookLM (통합)
- 소스로 콘텐츠 업로드
- 오디오 개요 생성 (팟캐스트 스타일)
- Google 인증 필요

## 설치

### 기본 설치

```bash
pip install riocloud-reader
```

### 모든 종속성 설치

```bash
pip install "riocloud-reader[all]"
playwright install chromium
```

### 선택적 종속성

```bash
# 브라우저 지원 (위챗, 샤오홍 Shu)
pip install "riocloud-reader[browser]"

# 유튜브 전사
pip install "riocloud-reader[youtube]"

# 텔레그램 지원
pip install "riocloud-reader[telegram]"

# NotebookLM 통합
pip install "riocloud-reader[notebooklm]"

# 일반 URL 파싱
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
result = run("이 비디오의 전사 가져오기: https://youtube.com/watch?v=dQw4w9WgXcQ")
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
| TG_API_ID | 텔레그램 | my.telegram.org의 API ID |
| TG_API_HASH | 텔레그램 | my.telegram.org의 API 해시 |
| GROQ_API_KEY | YouTube Whisper | console.groq.com의 무료 API 키 |
| FIRECRAWL_API_KEY | Firecrawl | 선택, 유료 콘텐츠용 |
| DEEPREEDER_MEMORY_PATH | 스토리지 | 콘텐츠를 저장할 디렉토리 |
| OBSIDIAN_VAULT | Obsidian | --obsidian 플래그의 기본 볼트 경로 |

## 고급 기능

### YouTube Groq Whisper 폴백

YouTube 동영상에 자막이 없는 경우 riocloud-reader는 자동으로 Groq Whisper API를 사용하여 전사를 수행합니다.

```bash
# Groq API 키 설정
export GROQ_API_KEY=당신의_groq_api_키

# 이제 모든 YouTube 동영상이 전사됩니다
riocloud-reader https://youtube.com/watch?v=xxx
```

무료 API 키 받기: https://console.groq.com/

### 베어 도메인 지원

https:// 접두사 없이 베어 도메인 이름을 사용할 수 있습니다:

```bash
riocloud-reader example.com
riocloud-reader example.com/경로
riocloud-reader twitter.com/elonmusk/status/123456
```

### Obsidian 볼트 통합

콘텐츠를 Obsidian 볼트에 직접 저장:

```bash
# Obsidian 볼트에 저장
riocloud-reader https://youtube.com/watch?v=xxx --obsidian /경로/到/볼트

# 또는 환경 변수 사용
export OBSIDIAN_VAULT=/경로/_to/vault
riocloud-reader https://twitter.com/user/status/123
```

날짜 기반 폴더 구조 생성:
```
볼트/
├── 2026-02/
│   ├── youtube/
│   │   └── dQw4w9WgXcQ_테스트_동영상.md
│   └── twitter/
│       └── abc123_사용자_트윗.md
```

### Twitter 로그인 세션

더 나은 Twitter/X 커버리지를 위해 세션을 유지하기 위해 로그인:

```bash
# 먼저, 로그인 (브라우저 열림)
riocloud-reader login twitter

# 그런 다음 Twitter URL 사용 - 사용 가능한 경우 세션 사용
riocloud-reader https://x.com/user/status/123456
```

3단계 폴백 사용: FxTwitter API → Nitter → Playwright 세션

`.env` 파일 생성:

```bash
cp .env.example .env
# 자격 증명 편집
```

## 아키텍처

```
riocloud_reader/
├── parsers/                  # 플랫폼별 파서
│   ├── base.py              # 기본 파서 및 유틸리티
│   ├── twitter.py           # Twitter/X 파서 (FxTwitter + Nitter)
│   ├── reddit.py            # Reddit 파서 (.json API)
│   ├── youtube.py           # YouTube 전사 파서
│   ├── wechat.py            # 위챗 기사 파서
│   ├── xhs.py               # 샤오홍 Shu 파서
│   ├── bilibili.py          # 빌리빌리 파서
│   ├── rss.py               # RSS/Atom 피드 파서
│   ├── telegram.py          # 텔레그램 채널 파서
│   └── generic.py           # 일반 URL 파서 (Trafilatura)
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
├── reader.py                # 기본 리더 클래스
├── schema.py                # 데이터 모델 및 스키마
└── cli.py                   # CLI 인터페이스
```

## 개발

### 개발 환경 설정

```bash
# 저장소 복제
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

BSD 2-Clause License - 자세한 내용은 LICENSE 파일을 참조하세요.

## 언어

이 README는 다른 언어로도 제공됩니다:
- [English](README.md)
- [中文](README_zh.md)
- [Español](README_es.md)
- [日本語](README_ja.md)
- [한국어](README_ko.md)
- [Русский](README_ru.md)

## 보안 업데이트 (v1.1.0)

### 경로 탐색 보호
- 디렉터리 탐색 공격을 방지하는 `validate_safe_path()` 함수 추가
- `--output`, `--inbox`, `--obsidian` CLI 인자 검증
- 안전한 디렉터리(~, ., ./output, /tmp)로 파일 작업 제한

### DoS 방지
- `max_response_size`(10MB) 및 `max_content_length`(2MB) 제한 추가
- Reddit, Twitter 파서에서 응답 크기 검사
- 무한 HTTP 응답으로 인한 메모리 고갈 방지

### 입력 검증
- GROQ_API_KEY 형식 검증(`gsk_`로 시작해야 함)
- 모든 파서에서 제목 자르기 일관성 유지

## 지원

- 문제 보고: https://github.com/Riocloud/riocloud-reader/issues
- 문서: https://github.com/Riocloud/riocloud-reader#readme

## 관련 프로젝트

- [x-reader](https://github.com/runesleo/x-reader) - 원래 범용 콘텐츠 리더
- [OpenClaw-DeepReeder](https://github.com/astonysh/OpenClaw-DeepReeder) - OpenClaw 내장 리더
