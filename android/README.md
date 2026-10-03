# Moon Arcana Android（offline-first）

Web版 `uranai-site` のタロット部分を、サーバー依存を外してAndroid向けに再構成した実装です。

## 方針

- カード抽選・基本解釈: 完全オフライン
- 占い履歴: Android端末内SQLite
- OpenRouter設定: Android Keystoreで生成したAES鍵を使ってAPIキーを暗号化保存
- AI詳細解説: `https://openrouter.ai/api/v1/chat/completions` にだけ通信
- Web版の FastAPI / MySQL / Redis / Weaviate / JWTログイン / PayPay / SMTP / S3 / X API には接続しない
- APIキーをAPKへハードコードしない。利用者が設定画面で自分のOpenRouterキーを入力するBYOK方式

## Web版から移植した内容

現行 `backend/app/tarot_data.py` の大アルカナ22枚の名称、キーワード、日本語基本解釈を端末内データとして移植しています。1枚引きと3枚引きは端末内の乱択だけで動作します。

## ビルド

Android Studioで `android/` をプロジェクトとして開き、Gradle Sync後に `app` を実行してください。JDK 17、Android SDK 35を想定しています。

CLIでビルドする場合はローカルGradleまたはAndroid StudioからGradle Wrapperを生成してから `./gradlew assembleDebug` を実行してください。

## 通信確認

Manifestのネットワーク権限は `INTERNET` のみです。アプリコード中の外部URLはOpenRouterのchat completions endpointだけです。AIボタンを押さない限りネットワーク処理は実行しません。

## 次段階

Web版のカード画像をAndroid drawable/assetsへ同梱すれば、カード画像表示も完全オフライン化できます。手相鑑定を移植する場合も、画像は端末で選択・縮小し、AI鑑定を実行した時だけOpenRouterのマルチモーダルモデルへ送る構成にできます。
