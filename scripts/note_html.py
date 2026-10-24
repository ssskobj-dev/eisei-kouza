#!/usr/bin/env python3
"""note に貼るための HTML を、post.md から作る。
使い方: python scripts/note_html.py <noteのフォルダ名>
1行目に題名、2行目以降に HTML を出す。画像の位置は <p data-img="fig-1.png"></p> で残す。"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
folder = ROOT / "note" / sys.argv[1]
lines = (folder / "post.md").read_text(encoding="utf-8").splitlines()
title, body = lines[0].strip(), lines[1:]


def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\"=>])(https?://[^\s<>）」]+)", r'<a href="\1">\1</a>', t)
    return t


out, buf, mode = [], [], None


def flush():
    global buf, mode
    if not buf:
        mode = None
        return
    if mode == "ul":
        out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in buf) + "</ul>")
    elif mode == "ol":
        out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in buf) + "</ol>")
    else:
        out.append(f"<p>{inline(' '.join(buf))}</p>")
    buf, mode = [], None


for ln in body:
    s = ln.strip()
    if not s:
        flush(); continue
    m = re.fullmatch(r"<<IMG: ([\w.-]+)>>", s)
    if m:
        flush(); out.append(f'<p data-img="{m.group(1)}"></p>'); continue
    if s == "---":
        flush(); out.append("<hr>"); continue
    m = re.match(r"^(#{2,3})\s+(.*)$", s)
    if m:
        flush(); out.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>"); continue
    m = re.match(r"^[-*]\s+(.*)$", s)
    if m:
        if mode != "ul": flush(); mode = "ul"
        buf.append(m.group(1)); continue
    m = re.match(r"^\d+\.\s+(.*)$", s)
    if m:
        if mode != "ol": flush(); mode = "ol"
        buf.append(m.group(1)); continue
    if mode in ("ul", "ol"): flush()
    mode = "p"; buf.append(s)
flush()
print(title)
print("".join(out))
