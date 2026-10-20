#!/usr/bin/env python3
"""できた動画をYouTubeに投稿する（既定は限定公開）。GitHub Actions から呼ばれる。

使い方：
  python scripts/youtube_upload.py <動画のid> [--privacy unlisted|private|public]

必要な環境変数：YT_CLIENT_ID、YT_CLIENT_SECRET、YT_REFRESH_TOKEN
投稿できたら、video/<id>/youtube.json に動画のidとURLを書く。
"""
import json
import os
import sys
from pathlib import Path

import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT = Path(__file__).resolve().parent.parent
vid = sys.argv[1]
privacy = sys.argv[sys.argv.index("--privacy") + 1] if "--privacy" in sys.argv else "unlisted"
channel = sys.argv[sys.argv.index("--channel") + 1] if "--channel" in sys.argv else "ja"
suffix = "_EN" if channel == "en" else ""
vdir = ROOT / "video" / vid
mp4 = vdir / f"{vid}.mp4"
if not mp4.exists():
    sys.exit(f"動画がありません：{mp4}")

def env(name):
    v = os.environ.get(name, "").strip().strip('"').strip("'")
    if not v:
        sys.exit(f"環境変数 {name} が空です。GitHubのSecretsを確認してください")
    return v

cid = env("YT_CLIENT_ID" + suffix)
print(f"  投稿先チャンネル：{channel}　クライアントID：{cid[:16]}…{cid[-30:]}")
creds = google.oauth2.credentials.Credentials(
    None, refresh_token=env("YT_REFRESH_TOKEN" + suffix), token_uri="https://oauth2.googleapis.com/token",
    client_id=cid, client_secret=env("YT_CLIENT_SECRET" + suffix),
    scopes=["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"])
yt = build("youtube", "v3", credentials=creds)

desc_path = vdir / "description.txt"
description = desc_path.read_text(encoding="utf-8") if desc_path.exists() else ""
title = description.splitlines()[0] if description else vid
tags = []
meta_path = vdir / "meta.json"   # video.py が作る。検索向けの題名とタグ
if meta_path.exists():
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    title = meta.get("title") or title
    tags = meta.get("tags") or []
body = {"snippet": {"title": title[:100], "description": description[:4900], "defaultLanguage": ("en" if channel == "en" else "ja"),
                    "defaultAudioLanguage": ("en" if channel == "en" else "ja"),
                    "tags": tags[:30],
                    "categoryId": "27"},   # 27 = 教育
        "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False}}
req = yt.videos().insert(part="snippet,status", body=body,
                         media_body=MediaFileUpload(str(mp4), chunksize=8 * 1024 * 1024, resumable=True))
res = None
while res is None:
    status, res = req.next_chunk()
    if status:
        print(f"  {int(status.progress() * 100)}%")
yid = res["id"]
thumb = vdir / "thumbnail.png"
if thumb.exists():
    try:
        yt.thumbnails().set(videoId=yid, media_body=MediaFileUpload(str(thumb))).execute()
    except Exception as e:  # サムネイルの設定は、電話番号の確認が済んだチャンネルだけで使える
        print(f"  サムネイルは設定できませんでした（{e.__class__.__name__}）。YouTubeの画面から設定してください")
out = {"id": yid, "url": f"https://youtu.be/{yid}", "privacy": privacy, "title": title}
(vdir / "youtube.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"投稿しました（{privacy}）：{out['url']}")
