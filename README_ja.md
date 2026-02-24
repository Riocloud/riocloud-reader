# Riocloud Reader

![License](https://img.shields.io/github/license/Riocloud/riocloud-reader)

AIエージェント向け汎用コンテンツリーダー。30以上のプラットフォームからコンテンツを数秒で取得、 транскриプション、整理。

## 概要

Riocloud Readerは、AIエージェントと開発者向けに設計された強力な汎用コンテンツリーダーです。各種オンラインプラットフォームからコンテンツを取得し、テキストとトランスクリプトを抽出し、LLM取込みに完璧な構造化データを返します。

Tweet、YouTube動画、Reddit投稿、記事、またはWeChatやBilibiliなどの中国プラットフォームのコンテンツを読み込む必要がある場合でも、Riocloud Readerはシンプルで統一されたAPIで一切を処理します。

## 主な機能

- **ゼロ設定** - ほとんどのプラットフォームで箱から出してすぐに動作、APIキー不要
- **30以上のプラットフォーム対応** - Twitter/X、Reddit、YouTube、WeChat、Bilibili、RSSなど
- **マルチフォーマット出力** - タイトル、コンテンツ、作者、タイムスタンプ、メタデータを含む構造化データを返す
- **複数のインターフェース** - CLIツール、Pythonライブラリ、MCPサーバー、OpenClawスキル
- **クロスプラットフォーム** - Linux、macOS、Windowsで動作

## 対応プラットフォーム

### Twitter/X
- 全文付きの通常のTweet
- 長いTweet（Twitter Blue）
- X記事（長編コンテンツ）
- ネストされたコンテンツ付きの引用Tweet
- リプライスレッド（Nitterフォールバックで最大5件）
- プロフィール統計を含むプロフィールスナップショット
- エンゲージメント指標（いいね、リポスト、閲覧、ブックマーク）

### Reddit
- 完全なmarkdown本文のセルフポスト
- URLとメタデータ付きのリンクポスト
- 上位コメント（最大15件、スコア順）
- ネストされた返信スレッド（最大3レベル）
- メディアURL（画像ギャラリー、视频）
- 投稿統計（スコア、コメント数、アップボイト率）
- フラグタグ

### YouTube
- 複数の言語での動画トランスクリプト
- 動画メタデータ（タイトル、説明、チャンネル、再生時間）
- さまざまなURL形式をサポート：
  - youtube.com/watch?v=xxx
  - youtu.be/xxx
  - youtube.com/embed/xxx

### WeChat（微信公众号）
- 公众号の記事
- 主な取得方法はJina Reader
- アンチスクレイピングページ用のPlaywrightフォールバック

### 小红書
- ノートと投稿
- 画像とメディアURL
- 認証リクエスト用のセッション付きPlaywright

### Bilibili
- 動画メタデータ
- 字幕
- bilibili.comとb23.tv shortリンクをサポート

### RSS/Atom
- 任意の標準RSSまたはAtomフィード
- フィードURLの自動検出

### Telegram
- チャンネルメッセージ
- my.telegram.orgからTG_API_IDとTG_API_HASHが必要

### ジェネリック（任意のURL）
- Trafilatura経由の任意のWebページ
- Jina Readerをフォールバックとして
- ベストエフォート型のコンテンツ抽出

### NotebookLM（統合）
- ソースとしてコンテンツをアップロード
- オーディオ概要を生成（ポッドキャストスタイル）
- Google認証が必要

## インストール

### 基本的なインストール

```bash
pip install riocloud-reader
```

### すべての依存関係をインストール

```bash
pip install "riocloud-reader[all]"
playwright install chromium
```

### オプションの依存関係

```bash
# ブラウザサポート（WeChat、小红書）
pip install "riocloud-reader[browser]"

# YouTubeトランスクリプト
pip install "riocloud-reader[youtube]"

# Telegramサポート
pip install "riocloud-reader[telegram]"

# NotebookLM統合
pip install "riocloud-reader[notebooklm]"

# ジェネリックURL解析
pip install "riocloud-reader[generic]"

# 開発とテスト
pip install "riocloud-reader[dev]"
```

## 使用方法

### コマンドラインインターフェース

```bash
# 単一のURLを読み込む
riocloud-reader https://twitter.com/user/status/123456
riocloud-reader https://youtube.com/watch?v=dQw4w9WgXcQ
riocloud-reader https://reddit.com/r/python/comments/abc123

# 複数のURLを読み込む
riocloud-reader https://url1.com https://url2.com

# 出力をファイルに保存
riocloud-reader https://example.com/article --output article.md

# 出力形式を指定
riocloud-reader https://example.com --format json
```

### Pythonライブラリ

```python
import asyncio
from riocloud_reader import Reader

async def main():
    # リーダーを初期化
    reader = Reader()
    
    # 单一のURLを読み込む
    content = await reader.read("https://twitter.com/user/status/123456")
    print(f"タイトル: {content.title}")
    print(f"コンテンツ: {content.content[:500]}")
    
    # 複数のURLをバッチ読み込み
    results = await reader.read_batch([
        "https://twitter.com/user/status/1",
        "https://reddit.com/r/python/comments/abc",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
    ])
    
    for result in results:
        print(f"URL: {result.url}")
        print(f"タイトル: {result.title}")

asyncio.run(main())
```

### OpenClawスキル

```python
from skills.reader import run

# エージェントメモリに直接コンテンツを読み込む
result = run("このTweetをチェック: https://x.com/elonmusk/status/123456")
result = run("この動画のトランスクリプトを取得: https://youtube.com/watch?v=dQw4w9WgXcQ")
```

### MCPサーバー

MCPサーバーを起動：

```bash
python -m riocloud_reader.mcp
```

Claude Desktop設定で構成（claude_desktop_config.json）：

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

## 設定

### 環境変数

| 変数 | 必要 | 説明 |
|------|------|------|
| TG_API_ID | Telegram | my.telegram.orgからのAPI ID |
| TG_API_HASH | Telegram | my.telegram.orgからのAPI Hash |
| GROQ_API_KEY | Whisper | console.groq.comからの無料APIキー |
| FIRECRAWL_API_KEY | Firecrawl | オプション、有料コンテンツ用 |
| DEEPREEDER_MEMORY_PATH | ストレージ | コンテンツを保存するディレクトリ |

### 設定ファイル

`.env`ファイルを作成：

```bash
cp .env.example .env
# 認証情報を編集
```

## アーキテクチャ

```
riocloud_reader/
├── parsers/                  # プラットフォーム固有のパーサー
│   ├── base.py              # ベースパーサーとユーティリティ
│   ├── twitter.py           # Twitter/Xパーサー（FxTwitter + Nitter）
│   ├── reddit.py            # Redditパーサー（.json API）
│   ├── youtube.py           # YouTubeトランスクリプトパーサー
│   ├── wechat.py            # WeChat記事パーサー
│   ├── xhs.py               # 小红書パーサー
│   ├── bilibili.py          # Bilibiliパーサー
│   ├── rss.py               # RSS/Atomフィードパーサー
│   ├── telegram.py          # Telegramチャンネルパーサー
│   └── generic.py           # ジェネリックURLパーサー（Trafilatura）
├── core/                     # コア機能
│   ├── router.py            # 適切なパーサーへのURLルーティング
│   ├── storage.py           # ファイルI/Oユーティリティ
│   └── config.py            # 設定管理
├── skills/                   # OpenClawスキル統合
│   └── reader/              # OpenClawリーダースキル
├── integrations/            # サードパーティ統合
│   └── notebooklm.py       # NotebookLM API
├── mcp/                     # MCPサーバー
│   └── server.py            # MCPサーバー実装
├── reader.py                # メインリーダークラス
├── schema.py                # データモデルとスキーマ
└── cli.py                   # CLIインターフェース
```

## 開発

### 開発環境の設定

```bash
# リポジトリをクローン
git clone https://github.com/Riocloud/riocloud-reader.git
cd riocloud-reader

# 開発モードでインストール
pip install -e ".[dev]"

# すべてのオプション依存関係をインストール
pip install -e ".[all]"
playwright install chromium
```

### テストの実行

```bash
# すべてのテストを実行
pytest

# 特定のテストファイルを実行
pytest tests/test_parsers.py

# 詳細出力を付けて実行
pytest -v
```

### コード品質

```bash
# Blackでコードをフォーマット
black .

# Ruffでリント
ruff check .

# リントの問題を修正
ruff check --fix .
```

## ライセンス

BSD 2-Clause License - 詳細はLICENSEファイルを参照してください。

## サポート

- 問題の報告：https://github.com/Riocloud/riocloud-reader/issues
- ドキュメント：https://github.com/Riocloud/riocloud-reader#readme

## 関連プロジェクト

- [x-reader](https://github.com/runesleo/x-reader) - 元の汎用コンテンツリーダー
- [OpenClaw-DeepReeder](https://github.com/astonysh/OpenClaw-DeepReeder) - OpenClaw組み込みリーダー
