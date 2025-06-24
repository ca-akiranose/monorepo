# モノレポ

このリポジトリは、フロントエンド（React）、バックエンド（FastAPI）、データベース定義を含むモノレポ構成です。

## ディレクトリ構成

```
monorepo/
├── apps/                    # アプリケーション
│   ├── frontend/           # フロントエンドアプリケーション (React + Vite)
│   ├── internal-api/       # 内部向けAPI (FastAPI)
│   └── external-api/       # 外部向けAPI (FastAPI)
├── packages/               # 共有パッケージ
│   ├── shared-types/       # 共有型定義
│   ├── shared-utils/       # 共有ユーティリティ
│   └── database/           # データベース関連
│       ├── ddl/           # DDLファイル
│       ├── migrations/    # マイグレーションファイル
│       └── seeds/         # シードデータ
├── tools/                  # 開発ツール
│   ├── scripts/           # ビルド・デプロイスクリプト
│   └── configs/           # 設定ファイル
├── docs/                   # ドキュメント
└── docker/                 # Docker設定
```

## 技術スタック

- **フロントエンド**: React + Vite + TypeScript
- **バックエンド**: FastAPI + Python
- **データベース**: MySQL
- **パッケージ管理**: npm workspaces (フロントエンド)
- **コンテナ**: Docker & Docker Compose

## 開発環境のセットアップ

### 前提条件
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose

### セットアップ手順

```bash
# 1. リポジトリのクローン
git clone <repository-url>
cd monorepo

# 2. フロントエンドの依存関係をインストール
npm install

# 3. Python仮想環境の作成と依存関係のインストール
cd apps/internal-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cd ../external-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Docker Composeで開発環境を起動
docker compose up -d

# 5. データベースのセットアップ
npm run db:setup
```

### 開発サーバーの起動

```bash
# フロントエンド (http://localhost:3000)
cd apps/frontend
npm run dev

# 内部向けAPI (http://localhost:3001)
cd apps/internal-api
uvicorn main:app --reload --host 0.0.0.0 --port 3001

# 外部向けAPI (http://localhost:3002)
cd apps/external-api
uvicorn main:app --reload --host 0.0.0.0 --port 3002
```

## API ドキュメント

- 内部向けAPI: http://localhost:3001/docs
- 外部向けAPI: http://localhost:3002/docs

## データベース管理

```bash
# マイグレーションの実行
npm run db:migrate

# シードデータの投入
npm run db:seed
```

## データベース接続情報

- **ホスト**: localhost
- **ポート**: 3306
- **データベース**: monorepo_dev
- **ユーザー**: root
- **パスワード**: password
