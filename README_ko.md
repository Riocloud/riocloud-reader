# Riocloud Reader
범용 콘텐츠 리더 — 30개 이상의 플랫폼에서 콘텐츠를 가져오고, 변환하고 분석합니다.

## 기능

- 🐦 **Twitter/X** — FxTwitter API + Nitter 폴백
- 🟠 **Reddit** — 네이티브 .json API
- 🎬 **YouTube** — 다국어 자막
- 📰 **WeChat** —微信公众号 기사 (Jina + Playwright)
- 📕 **Xiaohongshu** —小红书 노트 (로그인 필요)
- 📡 **RSS** — Feedparser
- 💬 **Telegram** — Telethon
- 🎥 **Bilibili** — 비디오 메타데이터
- 🌐 **일반** — Trafilatura / Jina
- 📓 **NotebookLM** — 업로드 + 오디오 생성
- 🤖 **MCP Server** — AI 도구로 노출
- 🦞 **OpenClaw Skill** — 네이티브 통합

## 설치

```bash
pip install git+https://github.com/Riocloud/riocloud-reader.git

# 전체 의존성
pip install "riocloud-reader[all] @ git+https://github.com/Riocloud/riocloud-reader.git"
playwright install chromium

# 사용 예시
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=xxx
```

## 지원 플랫폼

| 플랫폼 | 지원 | 메서드 |
|--------|------|--------|
| Twitter/X | ✅ | FxTwitter API |
| Reddit | ✅ | .json API |
| YouTube | ✅ | youtube-transcript-api |
| WeChat | ✅ | Jina + Playwright |
| Xiaohongshu | ✅ | Jina + Playwright |
| Bilibili | ✅ | API |
| RSS | ✅ | feedparser |
| Telegram | ✅ | Telethon |
| 일반 URL | ✅ | Trafilatura / Jina |

## 아키텍처

```
riocloud_reader/
├── core/           # 라우터, 스토리지, 설정
├── parsers/        # 플랫폼별 파서
├── skills/         # OpenClaw 스킬
├── integrations/   # NotebookLM 등
├── mcp/           # MCP 서버
└── tests/         # 단위 테스트
```

## 라이선스

MIT
