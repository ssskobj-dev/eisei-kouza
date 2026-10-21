#!/usr/bin/env python3
"""YouTube の動画を削除する（重複して投稿した分の始末に使う）。

使い方：
  python scripts/youtube_delete.py --channel ja|en <動画ID> [<動画ID> ...]

鍵は youtube_upload.py と同じ環境変数（YT_CLIENT_ID 等、英語は *_EN）。
削除は取り消せない。video/*/youtube.json に記録されている（残す）IDは、安全のため削除しない。
"""
import argparse
import json
import os
from pathlib import Path

import google.oauth2.credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("ids", nargs="+")
ap.add_argument("--channel", default="ja")
a = ap.parse_args()
suffix = "_EN" if a.channel == "en" else ""
env = lambda k: (os.environ.get(k) or "").strip().strip('"').strip("'")
creds = google.oauth2.credentials.Credentials(
    None, refresh_token=env("YT_REFRESH_TOKEN" + suffix), token_uri="https://oauth2.googleapis.com/token",
    client_id=env("YT_CLIENT_ID" + suffix), client_secret=env("YT_CLIENT_SECRET" + suffix),
    scopes=["https://www.googleapis.com/auth/youtube"])
yt = build("youtube", "v3", credentials=creds)
keep = set()
for p in ROOT.glob("video/*/youtube.json"):
    try:
        keep.add(json.loads(p.read_text(encoding="utf-8")).get("id"))
    except Exception:
        pass
for vid in a.ids:
    if vid in keep:
        print(f"残す動画なので削除しません：{vid}")
        continue
    try:
        yt.videos().delete(id=vid).execute()
        print(f"削除しました：https://youtu.be/{vid}")
    except Exception as e:
        print(f"削除できませんでした：{vid}（{e.__class__.__name__}: {str(e)[:160]}）")
