# YouTubeへの自動投稿の準備（1回だけ）

所要時間は30分ほど。必要なのは、Googleアカウントと、Pythonの入ったパソコンです。

## 1. YouTubeチャンネルを作る

1. https://www.youtube.com にログインし、右上のアイコン → 「チャンネルを作成」
2. チャンネル名を Satellite to Decision にする
3. YouTube Studio（https://studio.youtube.com）→ 設定 → チャンネル → 「機能の利用資格」で、電話番号の確認をしておく（サムネイルを自分で設定するために必要）

## 2. Google Cloud でプロジェクトを作り、YouTube Data API を有効にする

1. https://console.cloud.google.com を開く（請求先の登録は不要。無料の範囲で使えます）
2. 上の「プロジェクトを選択」→「新しいプロジェクト」→ 名前を satellite-to-decision にして作成
3. 左のメニュー →「APIとサービス」→「ライブラリ」→ YouTube Data API v3 を検索 →「有効にする」

## 3. OAuth の同意画面と、認証の鍵を作る

1. 「APIとサービス」→「OAuth 同意画面」→ ユーザーの種類は「外部」→ 作成
   - アプリ名：Satellite to Decision、サポートメールと連絡先メールに自分のアドレス
   - スコープの追加で、`.../auth/youtube.upload` と `.../auth/youtube` を追加
   - テストユーザーに、投稿に使うGoogleアカウントを追加（これで審査なしに自分だけ使えます）
2. 「認証情報」→「認証情報を作成」→「OAuth クライアント ID」→ 種類は「デスクトップ アプリ」→ 作成
3. 「JSONをダウンロード」で `client_secret.json` を保存する

## 4. 自分のパソコンで、鍵（リフレッシュトークン）を作る

```
pip install google-auth-oauthlib
python scripts/youtube_auth.py client_secret.json
```

ブラウザが開くので、投稿に使うアカウントで許可します。「このアプリは確認されていません」と出たら、「詳細」→「（安全ではないページ）に移動」で進めます（自分で作ったアプリなので問題ありません）。終わると、3つの値が表示されます。

## 5. GitHub に鍵を登録する

1. https://github.com/ssskobj-dev/eisei-kouza/settings/secrets/actions を開く
2. 「New repository secret」で、次の3つを1つずつ登録する
   - `YT_CLIENT_ID`
   - `YT_CLIENT_SECRET`
   - `YT_REFRESH_TOKEN`

公開リポジトリでも、Secrets は外から見えません。`client_secret.json` と表示された値は、リポジトリに入れないでください。

## 6. 試しに1本投稿する

1. https://github.com/ssskobj-dev/eisei-kouza/actions → 左の「video」→「Run workflow」
2. 動画のid に `usecase-chusankan-patrol`、privacy は `unlisted`（限定公開）のまま → Run
3. 15分ほどで終わります。終わると `video/usecase-chusankan-patrol/youtube.json` にURLが入り、リポジトリにコミットされます

## 知っておくこと

- **公開の範囲**：同意画面が「テスト」の状態のままだと、APIから投稿した動画は非公開または限定公開までしか扱えないことがあります。公開にするには、Googleの審査（無料、数日〜数週間）を通すか、YouTubeの画面で手で公開に切り替えます。まずは限定公開で運用し、公開への切り替えは手作業にするのが現実的です
- **上限**：APIの無料枠は1日10,000ユニットで、投稿1本が約1,600ユニットです。1日6本までが目安です
- **テストユーザーの期限**：同意画面が「テスト」のままだと、リフレッシュトークンが7日で切れる場合があります。切れたら手順4をやり直します。切れないようにするには、同意画面を「本番」に切り替えます（審査は、公開の投稿に関わる機能を使わなければ不要なことが多い）
- **処理時間**：GitHub Actions の無料枠は月2,000分です。1本15分なら、月130本まで
