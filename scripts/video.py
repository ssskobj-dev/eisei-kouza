#!/usr/bin/env python3
"""講義動画とユースケース解説動画を作る。

使い方：
  python scripts/video.py <動画のid>            video/<id>/script.yaml から動画を作る
  python scripts/video.py <動画のid> --slides   スライドの画像だけ作る（確認用）

必要なもの：
  - ffmpeg、Chromium（図のPNG化と同じ）、Pillow、numpy
  - 合成音声：VOICEVOX（環境変数 VOICEVOX_PY に、voicevox_core の入ったPythonを指定）
    なければ Open JTalk（pyopenjtalk）を使う。どちらも商用で使えるが、利用規約の表記が要る

動画の台本（script.yaml）の形：
  title: 動画の題名
  series: CASEBOOK | CODEX
  kicker: 画面の上に出す短い文字（例：ユースケース解説）
  voice: 13            # VOICEVOXの話者のid
  speed: 1.0
  credits: [ ... ]     # 末尾に出す出典と表記
  scenes:
    - kind: cover | bullets | figure | table | code | prompt | steps | cta
      heading: 見出し
      ...種類ごとの項目（下の各関数を参照）
      say: ナレーション。文は「。」で区切る。1文ごとに字幕になる
"""
import json
import os
import re
import shutil
import subprocess
import sys
import wave
from html import escape
from pathlib import Path

import numpy as np
import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from figures import find_browser
from figures import wrap as _jwrap  # noqa: E402

LANG = "ja"   # build() が台本の lang で設定する


def wrap(text, max_units):
    """折り返し。英語は単語の切れ目で折る。日本語は figures.wrap に任せる。"""
    if LANG != "en":
        return _jwrap(text, max_units)
    max_chars = max(4, int(max_units / 0.56))
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w) if cur else w
    if cur:
        lines.append(cur)
    return lines or [""]


# 画面と説明欄に出る、言語ごとの言葉
L = {
    "ja": {"agenda": "この動画の流れ", "sources": "出典", "verify": "要確認",
           "credit": lambda v: f"音声：{v['credit']}　案内役：{v['name']}",
           "transcript": "動画の全文です。", "chapters": "■ 章立て", "src_head": "■ 出典と表記",
           "foot": ["Satellite to Decision ｜ 地球観測データを、事業の意思決定へ。",
                    "どの衛星会社にも解析会社にも属さない立場で作っています。"],
           # 資格の案内（全動画の最後に入る）
           "cert_heading": "2つの資格が取得できます",
           "cert_sub": "資格の詳細と受験は、概要欄のリンクから",
           "cert_say": lambda a, b: (f"最後にお知らせです。Satellite to Decision では、{a}と{b}の2つの資格を取得できます。"
                                     "学んだことを形にしたい方は、概要欄のリンクから資格のページをご覧ください。ご視聴ありがとうございました。"),
           "cert_desc": lambda a, b: f"🎓 {a}・{b}の2つの資格を取得できます",
           "seo_suffix": "【衛星データ活用】", "seo_keys": ("衛星", "SAR", "Sentinel", "リモートセンシング"),
           "tags": ["衛星データ", "衛星データ活用", "リモートセンシング", "SAR", "Sentinel", "衛星データ解析", "衛星データ解析エンジニア", "衛星データマーケッター", "地球観測"]},
    "en": {"agenda": "In this video", "sources": "Sources", "verify": "To be verified",
           "credit": lambda v: f"Voice: {v['credit']} · Host: {v['name']}",
           "transcript": "Full transcript of the video.", "chapters": "Chapters", "src_head": "Sources and credits",
           "foot": ["Satellite to Decision | From Earth observation data to business decisions.",
                    "Made independently of any satellite operator or analytics company."],
           "cert_heading": "Two certifications you can earn",
           "cert_sub": "Details and exams - see the link in the description",
           "cert_say": lambda a, b: (f"One last thing. At Satellite to Decision you can earn two certifications - {a}, and {b}. "
                                     "If you want to turn what you learned into a credential, see the link in the description. Thanks for watching."),
           "cert_desc": lambda a, b: f"🎓 Earn two certifications: {a} and {b}",
           "seo_suffix": " | Satellite Data", "seo_keys": ("satellite", "SAR", "Sentinel", "remote sensing", "Earth observation"),
           "tags": ["satellite data", "earth observation", "remote sensing", "SAR", "Sentinel", "satellite data analysis", "satellite data analysis engineer", "satellite data marketer", "GIS"]},
}

W, H = 1920, 1080
NAVY, WHITE, ORANGE, SLATE, LINE, MIST, INK = "#0b1524", "#f2f5f7", "#ff6b2c", "#8ea0b8", "#1c2f4f", "#eef2f7", "#1a2433"
FONT = "'Noto Sans CJK JP','Noto Sans JP',sans-serif"
MONO = "'Noto Sans Mono CJK JP','DejaVu Sans Mono',monospace"
FPS = 12.5           # アバターの口の動きの刻み
AVATAR_X, AVATAR_Y, AVATAR_SIZE = 1560, 700, 340
BODY_TOP, BODY_BOTTOM, BODY_LEFT, BODY_RIGHT = 170, 900, 100, 1500   # 本文を置ける範囲（アバターと字幕を避ける）


# ---------------------------------------------------------------- スライド
def text(x, y, lines, size, fill=INK, weight="normal", lh=1.5, anchor="start", family=FONT):
    if isinstance(lines, str):
        lines = [lines]
    out = []
    for i, line in enumerate(lines):
        out.append(f'<text x="{x}" y="{y + i * size * lh:.0f}" font-size="{size}" font-weight="{weight}" '
                   f'fill="{fill}" text-anchor="{anchor}" font-family="{family}" xml:space="preserve">{escape(line)}</text>')
    return "".join(out)


CURRENT = {}   # 今作っている場面の情報（目次と進み具合を描くために、build() が入れる）


def agenda_panel():
    """右側の目次。今の節を強調し、終わった節は薄くする。"""
    items, cur = CURRENT.get("agenda", []), CURRENT.get("agenda_pos")
    if not items:
        return ""
    x, y0 = 1560, 200
    out = [f'<rect x="{x}" y="{y0 - 50}" width="300" height="{H - 150 - (y0 - 50) - 40}" rx="14" fill="{MIST}"/>',
           text(x + 24, y0, L[LANG]["agenda"], 20, SLATE, "bold")]
    avail = H - 150 - 40 - y0 - 60
    size = 22 if len(items) * (22 * 1.25 + 22) <= avail else 19
    y = y0 + 48
    for i, label in enumerate(items):
        lines = wrap(label, int(236 / (size * 0.95)))[:2]
        state = "now" if i == cur else ("done" if cur is not None and i < cur else "todo")
        if state == "now":
            out.append(f'<rect x="{x + 10}" y="{y - size - 4}" width="280" height="{size * 1.25 * len(lines) + 12:.0f}" rx="8" fill="{ORANGE}"/>')
            out.append(text(x + 28, y, lines, size, NAVY, "bold", lh=1.25))
        elif state == "done":
            out.append(f'<path d="M {x + 22} {y - size * 0.45:.0f} l 6 6 l 11 -12" stroke="{SLATE}" stroke-width="3" fill="none" stroke-linecap="round"/>')
            out.append(text(x + 52, y, lines, size, SLATE, lh=1.25))
        else:
            out.append(f'<circle cx="{x + 30}" cy="{y - size * 0.4:.0f}" r="4" fill="{SLATE}"/>')
            out.append(text(x + 52, y, lines, size, INK, lh=1.25))
        y += size * 1.25 * len(lines) + 20
    return "".join(out)


def progress_bar():
    n, i = CURRENT.get("n", 0), CURRENT.get("i")
    if not n or i is None:
        return ""
    frac = (i + 1) / n
    return (f'<rect x="0" y="120" width="{W}" height="6" fill="{LINE}"/>'
            f'<rect x="0" y="120" width="{W * frac:.0f}" height="6" fill="{ORANGE}"/>'
            f'<text x="{W - 72}" y="{H - 165}" font-size="20" fill="{SLATE}" text-anchor="end" font-family="{MONO}">{i + 1} / {n}</text>')


def frame(kicker, heading, body, series="CASEBOOK", dark=False):
    """共通の枠。上に帯と進み具合、右に目次、下に字幕の帯。"""
    bg = NAVY if dark else "#ffffff"
    out = [f'<rect width="{W}" height="{H}" fill="{bg}"/>']
    if not dark:
        out.append(f'<rect width="{W}" height="120" fill="{NAVY}"/>')
        out.append(progress_bar())
        out.append(agenda_panel())
        out.append(f'<rect x="72" y="46" width="22" height="22" fill="{ORANGE}" transform="rotate(45 83 57)"/>')
        out.append(text(116, 68, series, 26, ORANGE, "600", family=MONO))
        out.append(text(116 + len(series) * 18 + 40, 68, kicker, 26, SLATE, "bold"))
        out.append(text(W - 72, 68, "Satellite to Decision", 26, WHITE, "bold", anchor="end"))
        if heading:
            out.append(text(100, 200, heading, 44, NAVY, "900"))
            out.append(f'<rect x="100" y="222" width="{min(1400, len(heading) * 46)}" height="4" fill="{NAVY}"/>')
    out.append(f'<rect x="0" y="{H - 150}" width="{W}" height="150" fill="{NAVY}"/>')
    out += body
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">{"".join(out)}</svg>')


def logo(x, y, scale):
    return (f'<g transform="translate({x},{y}) scale({scale})"><g transform="translate(-330,-390)">'
            f'<path d="M 492 452 C 610 412, 762 424, 815 522 C 850 592, 812 652, 772 698" fill="none" stroke="{WHITE}" stroke-width="47" stroke-linecap="round"/>'
            f'<circle cx="424" cy="485" r="52" fill="none" stroke="{WHITE}" stroke-width="47"/>'
            f'<rect x="684" y="746" width="160" height="160" fill="{ORANGE}" transform="rotate(45 764 826)"/></g></g>')


def slide_cover(s, ctx):
    lines = wrap(s.get("heading") or ctx["title"], 18)[:3]
    size = 84 if len(lines) <= 2 else 70
    body = [f'<circle cx="{W - 100}" cy="{H + 200}" r="700" fill="none" stroke="{LINE}" stroke-width="3"/>',
            f'<circle cx="{W - 100}" cy="{H + 200}" r="900" fill="none" stroke="{LINE}" stroke-width="3"/>',
            logo(200, 150, 0.3),
            f'<rect x="100" y="400" width="26" height="26" fill="{ORANGE}" transform="rotate(45 113 413)"/>',
            text(150, 424, ctx["series"] + "　" + ctx.get("kicker", "") + (f"　{ctx['number']:03d} / {ctx['total']}" if ctx.get("number") else ""), 32, SLATE, "bold", family=MONO),
            text(100, 530, lines, size, WHITE, "900", lh=1.3)]
    if s.get("sub"):
        body.append(text(100, 530 + size * 1.3 * len(lines) + 20, wrap(s["sub"], 34)[:2], 38, SLATE, "bold", lh=1.4))
    body.append(text(100, H - 200, "Satellite to Decision", 34, WHITE, "bold"))
    return frame("", "", body, ctx["series"], dark=True)


def slide_bullets(s, ctx):
    body, y = [], 300
    if s.get("lead"):
        body.append(text(100, y, wrap(s["lead"], 44)[:2], 32, "#4b5b70", lh=1.5))
        y += 110
    n = len(s.get("items", []))
    size = 40 if n <= 4 else 34
    for item in s.get("items", []):
        lines = wrap(item, int(1300 / (size * 0.95)))[:2]
        body.append(f'<rect x="104" y="{y - size + 8}" width="18" height="18" fill="{ORANGE}" transform="rotate(45 113 {y - size + 17})"/>')
        body.append(text(150, y, lines, size, INK, "bold" if s.get("bold") else "normal", lh=1.4))
        y += int(size * 1.4 * len(lines)) + 36
    return frame(ctx["kicker"], s.get("heading", ""), body, ctx["series"])


def slide_figure(s, ctx):
    path = ROOT / s["image"]
    png = path if path.suffix == ".png" else path.with_suffix(".png")
    if not png.exists():
        from figures import to_png
        to_png(path)
    img = Image.open(png)
    maxw, maxh = (BODY_RIGHT - BODY_LEFT), (BODY_BOTTOM - 280)
    scale = min(maxw / img.width, maxh / img.height, 1.0)
    w, h = int(img.width * scale), int(img.height * scale)
    x = BODY_LEFT + (maxw - w) // 2
    body = [f'<image x="{x}" y="270" width="{w}" height="{h}" xlink:href="{png.resolve().as_uri()}"/>']
    if s.get("caption"):
        body.append(text(BODY_LEFT + maxw // 2, 270 + h + 48, s["caption"], 28, "#4b5b70", "bold", anchor="middle"))
    return frame(ctx["kicker"], s.get("heading", ""), body, ctx["series"])


def slide_table(s, ctx):
    cols = s["columns"]
    rows = s["rows"]
    widths = s.get("widths") or [1 / len(cols)] * len(cols)
    total = BODY_RIGHT - BODY_LEFT
    xs, acc = [], BODY_LEFT
    for wdt in widths:
        xs.append(acc)
        acc += total * wdt
    size = 30 if len(rows) <= 5 else 26
    y = 290
    body = [f'<rect x="{BODY_LEFT}" y="{y - 46}" width="{total}" height="66" fill="{MIST}"/>']
    for x, c in zip(xs, cols):
        body.append(text(x + 18, y, c, size, NAVY, "bold"))
    y += 70
    for row in rows:
        cells = [wrap(str(c), int(total * wdt / (size * 0.95)) - 1)[:3] for c, wdt in zip(row, widths)]
        nlines = max(len(c) for c in cells)
        for x, c in zip(xs, cells):
            body.append(text(x + 18, y, c, size, INK, lh=1.35))
        y += int(size * 1.35 * nlines) + 26
        body.append(f'<rect x="{BODY_LEFT}" y="{y - size - 6}" width="{total}" height="2" fill="#d5dde8"/>')
    return frame(ctx["kicker"], s.get("heading", ""), body, ctx["series"])


def slide_code(s, ctx):
    lines = s["code"].rstrip("\n").split("\n")
    hl = set(s.get("highlight", []))
    size = 26 if len(lines) <= 16 else 22
    lh = size * 1.45
    y0 = 290
    boxw = 980 if s.get("notes") else BODY_RIGHT - BODY_LEFT
    body = [f'<rect x="{BODY_LEFT}" y="{y0 - 40}" width="{boxw}" height="{int(lh * len(lines)) + 50}" rx="12" fill="{NAVY}"/>']
    for i, line in enumerate(lines, 1):
        yy = y0 + (i - 1) * lh
        if i in hl:
            body.append(f'<rect x="{BODY_LEFT + 10}" y="{yy - size + 4}" width="{boxw - 20}" height="{lh}" rx="6" fill="{ORANGE}" opacity="0.28"/>')
            body.append(f'<rect x="{BODY_LEFT + 10}" y="{yy - size + 4}" width="8" height="{lh}" fill="{ORANGE}"/>')
        body.append(text(BODY_LEFT + 30, yy, f"{i:>2}  ", size, SLATE, family=MONO))
        body.append(text(BODY_LEFT + 30 + size * 2.4, yy, line, size, WHITE, family=MONO))
    if s.get("notes"):
        nx, ny = BODY_LEFT + boxw + 40, y0
        for note in s["notes"]:
            body.append(f'<rect x="{nx}" y="{ny - 30}" width="14" height="14" fill="{ORANGE}" transform="rotate(45 {nx + 7} {ny - 23})"/>')
            ls = wrap(note, 15)[:4]
            body.append(text(nx + 30, ny, ls, 28, INK, "bold", lh=1.35))
            ny += int(28 * 1.35 * len(ls)) + 36
    return frame(ctx["kicker"], s.get("heading", ""), body, ctx["series"])


def slide_prompt(s, ctx):
    """AIへの指示文を、吹き出しの形で見せる。"""
    ls = []
    for para in s["text"].strip().split("\n"):
        ls += wrap(para, 42) or [""]
    size = 30 if len(ls) <= 12 else 26
    hgt = int(size * 1.45 * len(ls)) + 70
    body = [f'<rect x="{BODY_LEFT}" y="260" width="1300" height="{hgt}" rx="18" fill="{MIST}" stroke="{SLATE}" stroke-width="2"/>',
            f'<rect x="{BODY_LEFT}" y="260" width="12" height="{hgt}" fill="{ORANGE}"/>',
            text(BODY_LEFT + 40, 300, s.get("label", "AIへの指示文"), 24, "#c2410c", "bold", family=MONO),
            text(BODY_LEFT + 40, 350, ls, size, INK, lh=1.45)]
    return frame(ctx["kicker"], s.get("heading", ""), body, ctx["series"])


def slide_steps(s, ctx):
    body, y = [], 300
    n = len(s["items"])
    size = 36 if n <= 5 else 30
    for i, item in enumerate(s["items"], 1):
        lines = wrap(item, int(1250 / (size * 0.95)))[:2]
        body.append(f'<circle cx="{BODY_LEFT + 30}" cy="{y - size * 0.35}" r="28" fill="{ORANGE}"/>')
        body.append(text(BODY_LEFT + 30, y - size * 0.35 + 11, str(i), 30, NAVY, "900", anchor="middle"))
        body.append(text(BODY_LEFT + 90, y, lines, size, INK, lh=1.4))
        y += int(size * 1.4 * len(lines)) + 34
    return frame(ctx["kicker"], s.get("heading", ""), body, ctx["series"])


def slide_cta(s, ctx):
    """締めの画面。呼びかけは1つだけ（action と url）。"""
    lines = wrap(s.get("heading", ""), 20)[:2]
    body = [f'<circle cx="{W - 100}" cy="{H + 200}" r="700" fill="none" stroke="{LINE}" stroke-width="3"/>',
            text(100, 300, lines, 64, WHITE, "900", lh=1.3)]
    y = 300 + 64 * 1.3 * len(lines) + 60
    if s.get("action"):
        al = wrap(s["action"], 30)[:2]
        bw = min(1400, int(44 * 0.98 * max(len(x) for x in al)) + 100)
        body.append(f'<rect x="100" y="{y - 56}" width="{bw}" height="{44 * 1.4 * len(al) + 36:.0f}" rx="18" fill="{ORANGE}"/>')
        body.append(text(150, y, al, 44, NAVY, "900", lh=1.4))
        y += 44 * 1.4 * len(al) + 70
    if s.get("url"):
        body.append(text(100, y, s["url"], 32, WHITE, "bold", family=MONO))
    if s.get("credits"):
        cy = H - 190 - 30 * len(s["credits"])
        body.append(text(100, cy, s["credits"], 22, SLATE, lh=1.4))
    return frame("", "", body, ctx["series"], dark=True)


def slide_cert(s, ctx):
    """資格の案内（全動画の最後）。2つの資格を大きなカードで見せる。"""
    body = [f'<circle cx="{W - 100}" cy="{H + 200}" r="700" fill="none" stroke="{LINE}" stroke-width="3"/>',
            text(100, 230, wrap(s["heading"], 22)[:1], 64, WHITE, "900")]
    cards = s.get("items", [])[:2]
    cw, ch, gap, y0 = 800, 300, 60, 330
    for n, name in enumerate(cards):
        x = 100 + n * (cw + gap)
        body.append(f'<rect x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="24" fill="{WHITE}"/>')
        body.append(f'<rect x="{x}" y="{y0}" width="16" height="{ch}" rx="8" fill="{ORANGE}"/>')
        nl = wrap(name, 14)[:2]
        body.append(text(x + 60, y0 + ch / 2 - 26 * (len(nl) - 1) + 18, nl, 52, NAVY, "900", lh=1.3))
    if s.get("sub"):
        body.append(text(100, y0 + ch + 90, wrap(s["sub"], 34)[:1], 34, SLATE, "bold"))
    if s.get("url"):
        body.append(text(100, y0 + ch + 150, s["url"], 30, WHITE, "bold", family=MONO))
    return frame("", "", body, ctx["series"], dark=True)


SLIDES = {"cover": slide_cover, "bullets": slide_bullets, "figure": slide_figure, "table": slide_table,
          "code": slide_code, "prompt": slide_prompt, "steps": slide_steps, "cta": slide_cta, "cert": slide_cert}


def cert_scene(ctx):
    """資格の案内の場面を作る。_variables.yml の cert から名前とアドレスを取る。"""
    v = yaml.safe_load((ROOT / "_variables.yml").read_text(encoding="utf-8")).get("cert", {})
    en = LANG == "en"
    a = v.get("analysis_en" if en else "analysis", "Satellite Data Analysis" if en else "衛星データ解析")
    b = v.get("business_en" if en else "business", "Satellite Data Business" if en else "衛星データビジネス")
    url = v.get("url_en" if en else "url", "")
    return {"kind": "cert", "heading": L[LANG]["cert_heading"], "items": [a, b], "sub": L[LANG]["cert_sub"],
            "url": url.replace("https://", ""), "url_full": url, "say": L[LANG]["cert_say"](a, b), "_names": (a, b)}


def svg_to_png(svg, png):
    browser = find_browser()
    html = png.with_suffix(".html")
    html.write_text(f'<html><body style="margin:0">{svg}</body></html>', encoding="utf-8")
    subprocess.run([browser, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={W},{H + 200}", f"--screenshot={png}", html.resolve().as_uri()],
                   capture_output=True, timeout=120)
    html.unlink()
    Image.open(png).crop((0, 0, W, H)).save(png)


# ---------------------------------------------------------------- アバター
def avatar_svg(mouth, blink):
    """案内役。ブランドの記号（紺の円、白い輪と軌道の線、オレンジのひし形）がそのまま顔になる。
    軌道の線が口で、0（閉じる）1（半開き）2（開く）。"""
    s = AVATAR_SIZE
    k = s / 340
    gap = {0: 0, 1: 10, 2: 22}[mouth] * k
    eyes = (f'<path d="M {92*k} {125*k} Q {110*k} {112*k} {128*k} {125*k}" stroke="{WHITE}" stroke-width="{12*k}" fill="none" stroke-linecap="round"/>'
            f'<path d="M {212*k} {125*k} Q {230*k} {112*k} {248*k} {125*k}" stroke="{WHITE}" stroke-width="{12*k}" fill="none" stroke-linecap="round"/>') if blink else (
            f'<circle cx="{110*k}" cy="{125*k}" r="{18*k}" fill="none" stroke="{WHITE}" stroke-width="{14*k}"/>'
            f'<circle cx="{230*k}" cy="{125*k}" r="{18*k}" fill="none" stroke="{WHITE}" stroke-width="{14*k}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s} {s}" width="{s}" height="{s}">'
            f'<circle cx="{170*k}" cy="{170*k}" r="{160*k}" fill="{NAVY}"/>'
            f'<circle cx="{170*k}" cy="{170*k}" r="{160*k}" fill="none" stroke="{ORANGE}" stroke-width="{6*k}"/>'
            f'{eyes}'
            f'<path d="M {110*k} {205*k - gap} C {140*k} {235*k + gap}, {200*k} {235*k + gap}, {230*k} {205*k - gap}" fill="none" stroke="{WHITE}" stroke-width="{14*k}" stroke-linecap="round"/>'
            f'<rect x="{156*k}" y="{252*k}" width="{28*k}" height="{28*k}" fill="{ORANGE}" transform="rotate(45 {170*k} {266*k})"/></svg>')


def build_avatar_frames(workdir):
    browser = find_browser()
    out = {}
    for mouth in (0, 1, 2):
        for blink in (0, 1):
            png = workdir / f"avatar_{mouth}{blink}.png"
            html = png.with_suffix(".html")
            html.write_text(f'<html><body style="margin:0;background:transparent">{avatar_svg(mouth, blink)}</body></html>', encoding="utf-8")
            subprocess.run([browser, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                            f"--window-size={AVATAR_SIZE},{AVATAR_SIZE + 200}", f"--screenshot={png}", html.resolve().as_uri()],
                           capture_output=True, timeout=60)
            html.unlink()
            Image.open(png).convert("RGBA").crop((0, 0, AVATAR_SIZE, AVATAR_SIZE)).save(png)
            out[(mouth, blink)] = png
    return out


def mouth_track(wav_path):
    """音の大きさから、口の開き具合（0〜2）を刻みごとに決める。"""
    with wave.open(str(wav_path)) as w:
        sr, n = w.getframerate(), w.getnframes()
        data = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32)
    hop = int(sr / FPS)
    rms = np.array([np.sqrt(np.mean(data[i:i + hop] ** 2)) if len(data[i:i + hop]) else 0 for i in range(0, len(data), hop)])
    ref = np.percentile(rms[rms > 0], 85) if (rms > 0).any() else 1
    track = []
    for i, r in enumerate(rms):
        level = 2 if r > ref * 0.55 else (1 if r > ref * 0.2 else 0)
        blink = 1 if (i % int(FPS * 3.7) == 0 and i > 0) else 0
        track.append((level, blink))
    return track


# ---------------------------------------------------------------- 音声と字幕
def split_sentences(say):
    if LANG == "en":
        parts = re.split(r"(?<=[.!?])\s+", say.replace("\n", " "))
    else:
        parts = re.split(r"(?<=[。！？])", say.replace("\n", ""))
    return [p.strip() for p in parts if p.strip()]


def pick_voice(ctx, vid):
    """台本の voice（名前）から声を決める。なければ、同じ言語の一覧から動画のidで1つ選ぶ。"""
    import hashlib
    roster = yaml.safe_load((ROOT / "video" / "voices.yaml").read_text(encoding="utf-8"))["voices"]
    lang = ctx.get("lang", "ja")
    same = [v for v in roster if v.get("lang", "ja") == lang] or roster
    want = ctx.get("voice")
    if want not in (None, "", "random"):
        for v in roster:
            if want == v.get("name") or want == v.get("id"):
                return v
    return same[int(hashlib.md5(vid.encode()).hexdigest(), 16) % len(same)]


def synth(text_, out_wav, ctx):
    voice = ctx["_voice"]
    if voice.get("engine") == "piper":
        model = Path(os.environ.get("PIPER_VOICE_DIR", str(ROOT / "piper_voices"))) / (voice["model"] + ".onnx")
        subprocess.run([sys.executable, str(ROOT / "scripts" / "piper_tts.py"), str(model), text_, str(out_wav), str(ctx.get("speed", 1.0))],
                       capture_output=True, text=True, timeout=600)
        if out_wav.exists():
            return
    vv = os.environ.get("VOICEVOX_PY")
    if vv:
        env = dict(os.environ)
        env["LD_LIBRARY_PATH"] = os.environ.get("VOICEVOX_LIB", "") + ":" + env.get("LD_LIBRARY_PATH", "")
        r = subprocess.run([vv, str(ROOT / "scripts" / "voicevox_tts.py"), str(ctx["_voice"]["id"]), text_, str(out_wav), str(ctx.get("speed", 1.0)), str(ctx["_voice"].get("pitch", 0))],
                           capture_output=True, text=True, env=env, timeout=600)
        if out_wav.exists():
            return
        print(r.stderr[-500:])
    import pyopenjtalk
    import scipy.io.wavfile as sw
    x, sr = pyopenjtalk.tts(text_, speed=ctx.get("speed", 1.0))
    sw.write(str(out_wav), sr, x.astype(np.int16))


def sound_logo(out, sr):
    """2秒のサウンドロゴ。上がる2音（軌道の線のイメージ）と、短い締めの音（ひし形）。"""
    t = np.arange(int(sr * 2.0)) / sr
    def tone(f, start, dur, amp):
        env = np.clip((t - start) / 0.02, 0, 1) * np.clip((start + dur - t) / (dur * 0.6), 0, 1)
        return amp * env * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t))
    x = tone(523.25, 0.05, 0.5, 0.22) + tone(783.99, 0.38, 0.6, 0.22) + tone(1046.5, 0.78, 0.9, 0.18)
    x = (x / max(1e-6, np.abs(x).max()) * 0.5 * 32767).astype(np.int16)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(x.tobytes())


def concat_wavs(wavs, gap, out):
    frames, sr, sw = [], None, None
    for p in wavs:
        with wave.open(str(p)) as w:
            sr, sw = w.getframerate(), w.getsampwidth()
            frames.append(w.readframes(w.getnframes()))
            frames.append(b"\x00" * int(sr * gap) * sw)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(sw)
        w.setframerate(sr)
        w.writeframes(b"".join(frames))


def wav_len(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def ass_time(t):
    h, m = divmod(t, 3600)
    m, s = divmod(m, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Noto Sans CJK JP,52,&H00F7F5F2,&H00FFFFFF,&H00241509,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,2,100,100,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


# ---------------------------------------------------------------- 組み立て
def build(vid, slides_only=False):
    vdir = ROOT / "video" / vid
    ctx = yaml.safe_load((vdir / "script.yaml").read_text(encoding="utf-8"))
    global LANG
    LANG = ctx.get("lang", "ja")
    ctx["_voice"] = pick_voice(ctx, vid)
    print(f"声：{ctx['_voice']['name']}（{ctx['_voice']['credit']}）")
    for s in ctx["scenes"]:
        if s["kind"] == "cta":
            s.setdefault("credits", [])
            s["credits"] = [c for c in s["credits"] if "VOICEVOX" not in c and "Piper" not in c] + [L[LANG]["credit"](ctx["_voice"])]
    work = vdir / "_work"
    work.mkdir(exist_ok=True)
    scenes = ctx["scenes"]
    # 資格の案内を、必ず最後に入れる（台本に無くても自動で足す。cert: false で外せる）
    if ctx.get("cert", True) and not any(sc["kind"] == "cert" for sc in scenes):
        for sc in scenes:   # 締めの「ご視聴ありがとうございました」は、資格の案内の側で言う（二重に言わない）
            if sc["kind"] == "cta" and sc.get("say"):
                sc["say"] = re.sub(r"\s*(ご視聴ありがとうございました[。！]?|Thanks for watching[.!]?)\s*$", "", sc["say"].strip())
        scenes.append(cert_scene(ctx))
    body_idx = [i for i, sc in enumerate(scenes) if sc["kind"] not in ("cover", "cta", "cert")]
    agenda = [sc.get("heading", "") for i, sc in enumerate(scenes) if i in body_idx]
    for i, s in enumerate(scenes):
        CURRENT.clear()
        CURRENT.update({"n": len(scenes), "i": i, "agenda": agenda,
                        "agenda_pos": body_idx.index(i) if i in body_idx else None})
        png = work / f"slide_{i:02d}.png"
        svg_to_png(SLIDES[s["kind"]](s, ctx), png)
    print(f"スライド {len(scenes)} 枚")
    if slides_only:
        return
    # 案内役の顔は、既定では出さない（口が動くだけの顔は学習の助けにならないため。台本に avatar: true で出せる）
    avatars = build_avatar_frames(work) if ctx.get("avatar") or any(sc.get("avatar") for sc in scenes) else None
    parts, scene_starts, scene_lengths = [], [], []
    for i, s in enumerate(scenes):
        say = s.get("say", "")
        sentences = split_sentences(say)
        # 字幕の開始は、実際の音声に合わせる：冒頭（サウンドロゴ2秒か無音0.5秒）＋その後の間0.35秒
        lead_dur = 2.0 if i == 0 else 0.5
        wavs, times, t = [], [], lead_dur + 0.35
        for j, sent in enumerate(sentences):
            wv = work / f"s{i:02d}_{j:02d}_{ctx['_voice'].get('id', ctx['_voice']['name'])}.wav"
            if not wv.exists():
                synth(sent, wv, ctx)
            d = wav_len(wv)
            times.append((t, t + d, sent))
            t += d + 0.35
            wavs.append(wv)
        audio = work / f"audio_{i:02d}.wav"
        lead = work / "lead.wav"
        with wave.open(str(wavs[0])) as w0:
            sr0, sw0 = w0.getframerate(), w0.getsampwidth()
        if i == 0:
            sound_logo(lead, sr0)   # 最初の場面だけ、決まった音で始める
        else:
            with wave.open(str(lead), "wb") as w:
                w.setnchannels(1); w.setsampwidth(sw0); w.setframerate(sr0); w.writeframes(b"\x00" * int(sr0 * 0.5) * sw0)
        concat_wavs([lead] + wavs, 0.35, audio)
        scene_starts.append(sum(scene_lengths))
        scene_lengths.append(wav_len(audio) + 0.4)
        total = wav_len(audio) + 0.4
        # 字幕
        ass = work / f"sub_{i:02d}.ass"
        ev = []
        for a, b, sent in times:
            ls = wrap(sent, 30)[:2]
            joined = "\\N".join(ls)
            ev.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b + 0.3)},Sub,,0,0,0,,{joined}")
        ass.write_text(ASS_HEAD + "\n".join(ev) + "\n", encoding="utf-8")
        # アバターの口
        out = work / f"scene_{i:02d}.mp4"
        show_avatar = s.get("avatar", ctx.get("avatar", False)) and s["kind"] not in ("cover", "cta")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "25", "-i", f"slide_{i:02d}.png"]
        if show_avatar:
            track = mouth_track(audio)
            lst = work / f"avatar_{i:02d}.txt"
            lines = [f"file '{avatars[(level, blink)].name}'\nduration {1 / FPS:.4f}" for level, blink in track]
            lines.append(f"file '{avatars[(0, 0)].name}'\nduration 0.5")
            lst.write_text("\n".join(lines) + "\n", encoding="utf-8")
            cmd += ["-f", "concat", "-safe", "0", "-i", lst.name, "-i", audio.name,
                    "-filter_complex", f"[0:v][1:v]overlay={AVATAR_X}:{AVATAR_Y}:shortest=1[a];[a]ass={ass.name}[v]", "-map", "[v]", "-map", "2:a"]
        else:
            cmd += ["-i", audio.name, "-filter_complex", f"[0:v]ass={ass.name}[v]", "-map", "[v]", "-map", "1:a"]
        cmd += ["-t", f"{total:.2f}",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-r", "25",
               "-c:a", "aac", "-b:a", "128k", out.name]
        r = subprocess.run(cmd, cwd=work, capture_output=True, text=True)
        if r.returncode:
            print(r.stderr[-800:])
            sys.exit(1)
        parts.append(out)
        print(f"  場面 {i + 1}/{len(scenes)}：{total:.0f}秒")
    lst = work / "all.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")
    final = vdir / f"{vid}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst.name, "-c", "copy", str(final.resolve())],
                   cwd=work, check=True)
    write_companions(vid, vdir, ctx, scenes, scene_starts, body_idx, agenda, work)
    print(f"できました：{final.relative_to(ROOT)}（{wav_len_mp4(final):.0f}秒）")


def hms(t):
    m, sec = divmod(int(t), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"


def seo_title(ctx, vid):
    """YouTube 用の題名。検索されやすいように、キーワード（衛星／satellite など）を必ず含め、長さを抑える。
    台本の yt_title があればそれを使う。無ければ title を使い、キーワードが無ければ末尾に足す。"""
    t = (ctx.get("yt_title") or ctx["title"]).strip()
    keys = L[LANG]["seo_keys"]
    if not any(k.lower() in t.lower() for k in keys):
        t = t + L[LANG]["seo_suffix"]
    limit = 40 if LANG == "ja" else 70
    if len(t) > limit:
        print(f"注意：題名が長めです（{len(t)}字、目安 {limit}字以内）。検索結果で切れることがあります：{t}")
    return t[:100]


def write_companions(vid, vdir, ctx, scenes, starts, body_idx, agenda, work):
    """動画と一緒に使うもの：説明欄（章立て、リンク、表記）、全文、サムネイル。"""
    site = yaml.safe_load((ROOT / "_variables.yml").read_text(encoding="utf-8"))["site"]
    cta = next((sc for sc in scenes if sc["kind"] == "cta"), {})
    link = cta.get("url_full") or cta.get("url", "")
    if link and "utm_" not in link:
        link = ("https://" if not link.startswith("http") else "") + link + ("&" if "?" in link else "?") + f"utm_source=youtube&utm_medium=video&utm_campaign={vid}"
    chapters = [f"{hms(starts[i])} {scenes[i].get('heading') or ctx['title']}" for i in range(len(scenes))]
    yt_title = seo_title(ctx, vid)
    cert = next((sc for sc in scenes if sc["kind"] == "cert"), None)
    desc = [yt_title, ""]
    if ctx.get("summary"):
        desc += [ctx["summary"], ""]
    if cta.get("action"):
        desc += [f"▶ {cta['action']}", link, ""]
    if cert:
        a, b = cert["_names"]
        cert_link = cert.get("url_full", "")
        if cert_link and "utm_" not in cert_link:
            cert_link += ("&" if "?" in cert_link else "?") + f"utm_source=youtube&utm_medium=video&utm_campaign={vid}&utm_content=cert"
        desc += [L[LANG]["cert_desc"](a, b), cert_link, ""]
    desc += [L[LANG]["chapters"]] + chapters + [""]
    if cta.get("credits"):
        desc += [L[LANG]["src_head"]] + cta["credits"] + [""]
    desc += L[LANG]["foot"]
    (vdir / "description.txt").write_text("\n".join(desc) + "\n", encoding="utf-8")
    try:
        seo = yaml.safe_load((ROOT / "data" / "seo_keywords.yaml").read_text(encoding="utf-8")) or {}
        seo_tags = [("衛星データ " + w if LANG == "ja" else "satellite data " + w) for w in ((seo.get("video") or {}).get(LANG) or [])]
    except Exception:
        seo_tags = []
    tags = list(dict.fromkeys(list(ctx.get("tags") or []) + L[LANG]["tags"] + seo_tags + [t for t in (ctx.get("kicker"), ctx.get("series")) if t]))
    (vdir / "meta.json").write_text(json.dumps({"title": yt_title, "tags": tags[:30]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tr = [f"# {ctx['title']}", "", L[LANG]["transcript"], ""]
    for sc in scenes:
        if sc.get("heading") and sc["kind"] not in ("cover",):
            tr.append(f"## {sc['heading']}\n")
        tr.append(sc.get("say", "").strip() + "\n")
    (vdir / "transcript.md").write_text("\n".join(tr), encoding="utf-8")
    # サムネイル：短い文（4語以内）を大きく
    thumb = ctx.get("thumb") or ctx["title"]
    lines = wrap(thumb, 10)[:2]
    size = 150 if len(lines) == 1 else 120
    body = [f'<rect width="{W}" height="{H}" fill="{NAVY}"/>',
            f'<circle cx="{W - 100}" cy="{H + 200}" r="700" fill="none" stroke="{LINE}" stroke-width="4"/>',
            f'<circle cx="{W - 100}" cy="{H + 200}" r="900" fill="none" stroke="{LINE}" stroke-width="4"/>',
            logo(1620, 230, 0.42),
            f'<rect x="100" y="150" width="14" height="{size * 1.25 * len(lines) + 40:.0f}" fill="{ORANGE}" transform="translate(0,{H/2 - size * 1.25 * len(lines) / 2 - 20 - 150})"/>',
            text(150, H / 2 - size * 1.25 * len(lines) / 2 + size * 0.85, lines, size, WHITE, "900", lh=1.25),
            text(100, H - 120, ctx["series"] + ("　" + ctx.get("kicker", "")) + (f"　{ctx['number']:03d}" if ctx.get("number") else ""), 36, ORANGE, "bold", family=MONO),
            text(W - 100, H - 120, "Satellite to Decision", 36, WHITE, "bold", anchor="end")]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">{"".join(body)}</svg>')
    svg_to_png(svg, vdir / "thumbnail.png")


def wav_len_mp4(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(p)], capture_output=True, text=True)
    return float(json.loads(r.stdout)["format"]["duration"])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    build(sys.argv[1], "--slides" in sys.argv)
