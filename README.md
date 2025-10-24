# OpenTelemetry トレーシングデモ

OpenTelemetry 自動計装を使用した Next.js + Django + MySQL のデモアプリケーション

## アーキテクチャ

- **フロントエンド**: Next.js (App Router) - `http://localhost:3000`
- **バックエンド**: Django REST API - `http://localhost:8000`
- **データベース**: MySQL - `localhost:3306`
- **テレメトリ**: OpenTelemetry Collector - ポート 4317 (gRPC) と 4318 (HTTP)

## データフロー

1. ユーザーが `http://localhost:3000/` にアクセス
2. Next.js が `http://backend:8000/api/users` からデータを取得
3. Django が MySQL にユーザーデータをクエリ（100件のサンプルレコード）
4. すべてのトレースが OpenTelemetry Collector に送信され、デバッグエクスポーターとMackerelエクスポーター経由で出力

## はじめに

### 前提条件

Docker Compose を用いて動作させます。docker と docker-compose がインストールされていることを確認してください。

### アプリケーションの実行方法

以下のコマンドを実行すると [docker-compose.yml](docker-compose.yml) ファイルに定義されたすべてのサービスがビルドおよび起動されます。

```bash
docker compose up --build
```

### アプリケーションへのアクセス

アプリケーションには以下の URL でアクセスできます。バックエンド API 並びに MySQL はフロントエンドの URL から利用されるので、通常は個別にアクセスする必要はありません。フロントエンドのページを開くと、バックエンド API からユーザーデータが取得され表示され、トレースデータが生成されます。

- フロントエンド: http://localhost:3000
- バックエンド API: http://localhost:8000/api/users
- MySQL: localhost:3306 (ユーザー: dbuser, パスワード: dbpassword, データベース: userdb)

### トレースの確認

トレースは OpenTelemetry Collector のコンソール出力に表示されます。アプリケーション実行中にコンソールで `otel-collector-next-django` のログを確認できます。また、Mackerel のダッシュボードでもトレースを確認できます。

### アプリケーションの停止

`Ctrl+C` でアプリケーションを停止できます。

コンテナとボリュームを完全に削除する場合：

```bash
docker compose down -v
```

## プロジェクト構成

```
.
├── docker-compose.yml
├── .env                             # 環境変数（Mackerel API キーなど）
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.js
│   ├── instrumentation.ts          # OpenTelemetry 設定
│   └── app/
│       ├── layout.tsx
│       └── page.tsx                # バックエンド API を呼び出すメインページ
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── config/
│   │   ├── settings.py             # MySQL 設定を含む Django 設定
│   │   └── urls.py                 # URL ルーティング
│   └── users/
│       ├── models.py               # User モデル
│       └── views.py                # API エンドポイント
├── mysql/
│   └── init.sql                    # 初期データ（100 ユーザー）
└── otel-collector/
    └── config.yaml                 # OTEL Collector 設定（デバッグ・Mackerel エクスポーター）
```

## OpenTelemetry 設定

### Next.js (Node.js)

- `@opentelemetry/auto-instrumentations-node` による自動計装
- Collector への OTLP gRPC エクスポーター
- `instrumentation.ts` で設定

### Django (Python)

- `opentelemetry-instrument` CLI による自動計装
- Django と MySQL の計装を含む
- Collector への OTLP エクスポーター

### Collector

- OTLP（gRPC と HTTP）でトレースを受信
- デバッグエクスポーターでコンソールに出力
- Mackerel エクスポーターで Mackerel に送信
- `otel-collector/config.yaml` で設定

## 環境変数設定

プロジェクトルートに `.env` ファイルを作成し、以下の変数を設定してください：

```bash
MACKEREL_APIKEY=your_mackerel_api_key_here
```
