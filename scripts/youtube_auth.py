#!/usr/bin/env python3
"""YouTubeへ自動投稿するための鍵（リフレッシュトークン）を、自分のパソコンで1回だけ作る。

使い方（自分のパソコンで）：
  pip install google-auth-oauthlib
  python scripts/youtube_auth.py client_secret.json

ブラウザが開くので、投稿先のチャンネルを持つGoogleアカウントで許可する。
終わると、GitHubのSecretsに登録する3つの値が表示される。この値は人に見せない。
"""
import json
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(0)
flow = InstalledAppFlow.from_client_secrets_file(sys.argv[1], SCOPES)
creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")
client = json.load(open(sys.argv[1]))["installed"]
print("\n次の3つを、GitHubのリポジトリの Settings → Secrets and variables → Actions に登録してください。\n")
print("YT_CLIENT_ID      =", client["client_id"])
print("YT_CLIENT_SECRET  =", client["client_secret"])
print("YT_REFRESH_TOKEN  =", creds.refresh_token)
