# Tarot AI Site Starter

FastAPI + Next.js + Nginx + MySQL + Redis + Weaviate で構成した、タロット占いサイトのスターターです。

実装済み:

- メールアドレス / パスワードによるユーザー登録とログイン
- JWT 認証
- タロット占い API
- 1ユーザーあたり無料 30 回までの利用制限
- MySQL 永続化
- Redis に最新の占い結果をキャッシュ
- Weaviate へのカード知識シードのフック
- 占いから 2 週間後のフォローアップメール送信
- フィードバック保存と学習メモ生成
- Nginx による `/` と `/api` のリバースプロキシ

## 起動

1. `.env.example` を `.env` にコピーして値を設定
2. 課金機能を使う場合だけ `BILLING_ENABLED=1` にして Stripe 関連の値を設定
3. フォローアップメールを使う場合は SMTP 設定を `.env` に入れる
4. LLM 要約も使う場合は `OPENAI_API_KEY` と `OPENAI_MODEL` を設定
5. 起動

```bash
docker compose --env-file .env up --build
```

MySQL は初回起動時に `.env` の `MYSQL_DATABASE` `MYSQL_USER` `MYSQL_PASSWORD` に合わせて
アプリ用 DB とユーザーを自動作成します。

すでに作成済みの `mysql_data` ボリュームがあり、以前と違う認証情報に変えた場合は
初期化スクリプトは再実行されません。その場合は開発環境でのみ次を実行して DB を作り直してください。

```bash
docker compose down -v
docker compose --env-file .env up --build
```

ブラウザ:

- フロント: `http://localhost`
- API: `http://localhost/api`

フロントエンドは `NEXT_PUBLIC_API_BASE_URL=/api` を前提に、同一オリジンの Nginx 経由で API へ接続します。
外部端末からアクセスする環境では `http://localhost/api` を設定しないでください。
検索エンジンに正しい公開 URL を出すため、`NEXT_PUBLIC_SITE_URL` は公開ドメインに合わせて設定してください。
SSR で翻訳文言を取得するため、`INTERNAL_API_BASE_URL` は通常 `http://backend:8000` のまま使います。

## Stripe Webhook

Stripe CLI を使う例:

```bash
stripe listen --forward-to localhost/api/v1/billing/webhook
```

表示された署名シークレットを `.env` の `STRIPE_WEBHOOK_SECRET` に設定してください。

## 主なエンドポイント

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/readings`
- `GET /api/v1/readings/latest`
- `GET /api/v1/followups/{token}`
- `POST /api/v1/followups/{token}`

## 管理画面でユーザー一覧が見れない場合

- 日本語ページから入る場合は `http://localhost/ja/admin/login` を開いてください
- 管理ログイン成功後は `http://localhost/ja/admin/users` に遷移します
- ログイン後に一覧が出ない場合はブラウザの `localStorage` にある `admin_token` を削除して再ログインしてください
- `.env` の `ADMIN_USERNAME` と `ADMIN_PASSWORD` が現在の値と一致しているか確認してください
- API が生きているか `GET /api/v1/auth/admin/me` と `GET /api/v1/admin/users` を管理者トークン付きで確認してください
- フロント変更後に反映されない場合は `sudo docker compose up -d --build frontend nginx` を実行してフロントと Nginx を再ビルドしてください
- ローカルでは `http://localhost/ja/admin/users` で確認してください。`https://localhost/...` に飛ぶ古い設定が残っている場合も `sudo docker compose up -d --build frontend nginx` で更新してください

## 2週間後フォローアップ

- 占いを 1 件作るごとに、2 週間後送信用のフォローアップを DB に予約します
- バックエンドは `FOLLOWUP_POLL_SECONDS` ごとに送信対象をチェックします
- `SMTP_HOST` と `SMTP_FROM_EMAIL` が設定されている場合のみメール送信します
- メール内リンクのフォームで、当たっていたかと実際の出来事を回答できます
- 回答内容は学習メモとして保存され、`OPENAI_API_KEY` と `OPENAI_MODEL` がある場合は LLM 要約も保存します
- 占い生成時は `allow_learning=true` の回答だけを集計し、当たりやすい傾向を解釈ロジックへ反映します
- 学習集計は `GET /api/v1/learning/insights` で確認できます
- 学習許可済みフィードバックは Weaviate にも保存され、新しい質問時に近い過去事例をベクトル検索して補助コンテキストに使います

## 課金フラグ

- `BILLING_ENABLED=0` のときは課金 UI と課金 API を停止し、利用制限による `402` も返しません
- `BILLING_ENABLED=1` のときだけ Stripe Checkout / Portal / webhook を有効化します
