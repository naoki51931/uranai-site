# AGENTS.md

このリポジトリで管理画面のユーザー一覧が見れないと報告された場合は、まず次を確認すること。

- 日本語導線は `/ja/admin/login` から入り、ログイン成功後は `/ja/admin/users` に遷移する
- 管理画面の認証は通常ユーザーの `token` ではなく `localStorage.admin_token` を使う
- `admin_token` が壊れている場合は削除して再ログインする
- `.env` の `ADMIN_USERNAME` `ADMIN_PASSWORD` を確認する
- バックエンドの `GET /v1/auth/admin/me` と `GET /v1/admin/users` が管理者 Bearer token で `200` を返すか確認する
- フロント変更が見えない場合は `sudo docker compose up -d --build frontend nginx` で frontend と nginx を更新する
- ローカル確認は `http://localhost/ja/admin/users` を使う。`https://localhost/...` へ 301 される場合は nginx の古い設定が残っているので再ビルド対象に nginx も含める
