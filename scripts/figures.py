#!/usr/bin/env python3
"""図解を作る。figures/<章のid>.yaml に書いた内容から、SVGの図を出力する。

使い方:
  python scripts/figures.py            全部の図を作る
  python scripts/figures.py <章のid>   その章の図だけ作る
  python scripts/figures.py <記事のフォルダ名>   note記事の図と見出し画像だけ作る（PNGも出す）

図の型（type）は patterns/figures.md を参照。色は design/typst-template.typ と同じ。
"""
import glob
import re
import shutil
import subprocess
import sys
from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
W = 720  # 図の幅。高さは内容に合わせて決まる
PAD = 22

MAIN, DEEP, PALE, INK = "#2b8fd6", "#14609c", "#dcedfa", "#1f2a33"
WARM, WARM_DEEP, WARM_PALE = "#e8943a", "#a85e12", "#fdf0e0"   # 人が行う部分
GRAY, GRAY_PALE = "#8a949c", "#eef1f3"                          # 向かない、対象外
FONT = "'Noto Sans CJK JP','Noto Sans JP','Hiragino Sans','Yu Gothic','Meiryo',sans-serif"

# 役割ごとの色（枠、地、文字）
ROLES = {
    "satellite": (MAIN, PALE, DEEP, "衛星・解析"),
    "human": (WARM, WARM_PALE, WARM_DEEP, "人・現地"),
    "none": (GRAY, GRAY_PALE, INK, ""),
}


# ---------- 文字の部品 ----------

def units(ch):
    """文字の幅。全角を1、半角を0.56として数える。"""
    return 0.56 if ord(ch) < 0x2000 else 1.0


def wrap(text, max_units):
    """折り返す。最後の行に1〜2文字だけ残るときは、幅を少し詰めてやり直す。"""
    lines = wrap_once(text, max_units)
    for shrink in (1, 2, 3):
        if len(lines) < 2 or sum(units(c) for c in lines[-1]) >= 3:
            break
        retry = wrap_once(text, max_units - shrink)
        if len(retry) == len(lines):
            lines = retry
    return lines


def wrap_once(text, max_units):
    """幅に収まるように折り返す。行頭に句読点が来ないようにする。"""
    lines, cur, width = [], "", 0.0
    for ch in str(text):
        w = units(ch)
        if width + w > max_units and cur and ch not in "、。）」』】・ー":
            lines.append(cur)
            cur, width = "", 0.0
        cur += ch
        width += w
    if cur:
        lines.append(cur)
    return lines or [""]


def text(x, y, lines, size=15, fill=INK, weight="normal", anchor="start", lh=1.5):
    """複数行の文字。y は1行目の文字の下端。"""
    if isinstance(lines, str):
        lines = [lines]
    spans = "".join(
        f'<tspan x="{x:.1f}" y="{y + i * size * lh:.1f}">{escape(l)}</tspan>'
        for i, l in enumerate(lines))
    return (f'<text font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{spans}</text>')


def text_h(n_lines, size=15, lh=1.5):
    return n_lines * size * lh


def rect(x, y, w, h, fill, stroke="none", r=10, sw=1.5):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def badge(cx, cy, label, fill=MAIN, r=14):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"/>'
            + text(cx, cy + 5.5, str(label), size=15, fill="#fff", weight="bold", anchor="middle"))


def arrow(x1, y1, x2, y2, color=MAIN, sw=3):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" marker-end="url(#ah-{color[1:]})"/>')


def legend(y, roles):
    """図の下に入れる、色の説明。"""
    out, x = [], PAD
    for role in roles:
        stroke, fill, _, name = ROLES[role]
        out.append(rect(x, y - 12, 16, 16, fill, stroke, r=4))
        out.append(text(x + 23, y + 1, name, size=13, fill=INK))
        x += 23 + len(name) * 13 + 22
    return "".join(out)


def svg(height, body, title):
    markers = "".join(
        f'<marker id="ah-{c[1:]}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" '
        f'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
        for c in (MAIN, WARM, GRAY, DEEP, INK))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height:.0f}" '
            f'font-family="{FONT}" role="img"><title>{escape(title)}</title><defs>{markers}</defs>'
            f'<rect width="{W}" height="{height:.0f}" rx="14" fill="#ffffff" stroke="{PALE}" stroke-width="2"/>'
            f'{body}</svg>\n')


# ---------- 図の型 ----------

def fig_cards(spec):
    """番号付きのカードを並べる。要点を一覧で見せる。"""
    items, cols = spec["items"], spec.get("columns", 2)
    gap = 14
    cw = (W - PAD * 2 - gap * (cols - 1)) / cols
    inner = cw - 58 - 14
    out, y = [], PAD
    for row_start in range(0, len(items), cols):
        row = items[row_start:row_start + cols]
        laid = []
        for it in row:
            t = wrap(it["title"], inner / 16)
            b = wrap(it.get("text", ""), inner / 13.5) if it.get("text") else []
            laid.append((t, b))
        h = max(text_h(len(t), 16, 1.4) + (text_h(len(b), 13.5) + 4 if b else 0) for t, b in laid) + 30
        for i, (it, (t, b)) in enumerate(zip(row, laid)):
            x = PAD + i * (cw + gap)
            stroke, fill, ink, _ = ROLES[it.get("role", "satellite")]
            out.append(rect(x, y, cw, h, fill, "none"))
            out.append(badge(x + 29, y + 31, it.get("mark", row_start + i + 1), stroke))
            out.append(text(x + 58, y + 34, t, size=16, fill=ink, weight="bold", lh=1.4))
            if b:
                out.append(text(x + 58, y + 34 + text_h(len(t), 16, 1.4) + 4, b, size=13.5))
        y += h + gap
    return y - gap + PAD, "".join(out)


def fig_flow(spec):
    """手順を左から右へ矢印でつなぐ。誰がやるかを色で分ける。"""
    steps = spec["steps"]
    n, gap = len(steps), 26
    bw = (W - PAD * 2 - gap * (n - 1)) / n
    laid = []
    for s in steps:
        t = wrap(s["title"], (bw - 20) / 14.5)
        b = wrap(s["text"], (bw - 20) / 12.5) if s.get("text") else []
        laid.append((t, b))
    h = max(text_h(len(t), 14.5, 1.4) + (text_h(len(b), 12.5, 1.45) + 6 if b else 0) for t, b in laid) + 48
    out, y = [], PAD + 4
    roles = []
    for i, (s, (t, b)) in enumerate(zip(steps, laid)):
        x = PAD + i * (bw + gap)
        role = s.get("who", "satellite")
        if role not in roles:
            roles.append(role)
        stroke, fill, ink, _ = ROLES[role]
        out.append(rect(x, y, bw, h, fill, stroke))
        out.append(badge(x + bw / 2, y + 1, i + 1, stroke))
        out.append(text(x + bw / 2, y + 40, t, size=14.5, fill=ink, weight="bold", anchor="middle", lh=1.4))
        if b:
            out.append(text(x + bw / 2, y + 40 + text_h(len(t), 14.5, 1.4) + 6, b, size=12.5,
                            anchor="middle", lh=1.45))
        if i < n - 1:
            out.append(arrow(x + bw + 5, y + h / 2, x + bw + gap - 8, y + h / 2, DEEP))
    y += h + 30
    out.append(legend(y, roles))
    return y + 8 + PAD - 6, "".join(out)


def fig_funnel(spec):
    """上から下へ絞り込まれていく様子。段ごとに数や範囲を示す。"""
    stages = spec["stages"]
    n, sh, gap = len(stages), 62, 10
    fw_top, fw_bottom = 380, 150      # じょうごの上端と下端の幅
    cx = PAD + fw_top / 2 + 6
    out, y = [], PAD
    for i, s in enumerate(stages):
        w1 = fw_top - (fw_top - fw_bottom) * i / n
        w2 = fw_top - (fw_top - fw_bottom) * (i + 1) / n
        stroke, fill, ink, _ = ROLES[s.get("who", "satellite")]
        pts = f"{cx - w1 / 2:.1f},{y} {cx + w1 / 2:.1f},{y} {cx + w2 / 2:.1f},{y + sh} {cx - w2 / 2:.1f},{y + sh}"
        out.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.5" stroke-linejoin="round"/>')
        out.append(text(cx, y + sh / 2 + 7, s["label"], size=17 if len(s["label"]) < 9 else 15,
                        fill=ink, weight="bold", anchor="middle"))
        nx = PAD + fw_top + 34
        out.append(f'<line x1="{cx + (w1 + w2) / 4 + 6:.1f}" y1="{y + sh / 2}" x2="{nx - 10}" y2="{y + sh / 2}" '
                   f'stroke="{stroke}" stroke-width="1.5" stroke-dasharray="3 4"/>')
        t = wrap(s["title"], (W - PAD - nx) / 15)
        b = wrap(s.get("text", ""), (W - PAD - nx) / 13) if s.get("text") else []
        total = text_h(len(t), 15, 1.35) + (text_h(len(b), 13, 1.4) if b else 0)
        ty = y + sh / 2 - total / 2 + 14
        out.append(text(nx, ty, t, size=15, fill=ink, weight="bold", lh=1.35))
        if b:
            out.append(text(nx, ty + text_h(len(t), 15, 1.35), b, size=13, lh=1.4))
        y += sh + gap
    return y - gap + PAD, "".join(out)


def fig_split(spec):
    """左右に分けて、役割や対比を見せる。"""
    left, right = spec["left"], spec["right"]
    gap = 54
    cw = (W - PAD * 2 - gap) / 2
    cols = []
    for side, default in ((left, "satellite"), (right, "human")):
        items = [wrap(i, (cw - 54) / 14) for i in side["items"]]
        h = 62 + sum(text_h(len(i), 14, 1.45) + 9 for i in items) + 8
        cols.append((side, side.get("role", default), items, h))
    h = max(c[3] for c in cols)
    out, y = [], PAD
    for k, (side, role, items, _) in enumerate(cols):
        x = PAD + k * (cw + gap)
        stroke, fill, ink, _ = ROLES[role]
        out.append(rect(x, y, cw, h, fill, "none"))
        out.append(rect(x, y, cw, 42, stroke, "none"))
        out.append(f'<rect x="{x:.1f}" y="{y + 26}" width="{cw:.1f}" height="16" fill="{stroke}"/>')
        out.append(text(x + cw / 2, y + 28, side["title"], size=16, fill="#fff", weight="bold", anchor="middle"))
        iy = y + 70
        for lines in items:
            out.append(f'<circle cx="{x + 24:.1f}" cy="{iy - 5:.1f}" r="4" fill="{stroke}"/>')
            out.append(text(x + 38, iy, lines, size=14, lh=1.45))
            iy += text_h(len(lines), 14, 1.45) + 9
    mid = PAD + cw + gap / 2
    link = spec.get("link", "→")
    out.append(f'<circle cx="{mid}" cy="{y + h / 2}" r="21" fill="#fff" stroke="{DEEP}" stroke-width="2"/>')
    out.append(text(mid, y + h / 2 + 7, link, size=19, fill=DEEP, weight="bold", anchor="middle"))
    y += h
    if spec.get("note"):
        lines = wrap(spec["note"], (W - PAD * 2 - 28) / 14)
        nh = text_h(len(lines), 14) + 16
        y += 14
        out.append(rect(PAD, y, W - PAD * 2, nh, GRAY_PALE, "none", r=8))
        out.append(text(W / 2, y + 26, lines, size=14, weight="bold", anchor="middle"))
        y += nh
    return y + PAD, "".join(out)


def fig_scale(spec):
    """向く条件から向かない条件までを、1本の帯の上に並べる。"""
    items = spec["items"]
    x0, x1, y = PAD + 10, W - PAD - 10, PAD + 34
    out = [
        f'<defs><linearGradient id="sg"><stop offset="0" stop-color="{MAIN}"/>'
        f'<stop offset="1" stop-color="{GRAY_PALE}"/></linearGradient></defs>',
        rect(x0, y, x1 - x0, 14, "url(#sg)", "none", r=7),
        text(x0, y - 12, spec.get("left", "向いている"), size=14, fill=DEEP, weight="bold"),
        text(x1, y - 12, spec.get("right", "向いていない"), size=14, fill=GRAY, weight="bold", anchor="end"),
    ]
    n = len(items)
    cw = (x1 - x0) / n
    maxh = 0
    for i, it in enumerate(items):
        cx = x0 + cw * (i + 0.5)
        out.append(f'<circle cx="{cx:.1f}" cy="{y + 7}" r="8" fill="#fff" stroke="{DEEP}" stroke-width="2.5"/>')
        t = wrap(it["title"], (cw - 12) / 14)
        b = wrap(it.get("text", ""), (cw - 12) / 12.5) if it.get("text") else []
        out.append(text(cx, y + 44, t, size=14, weight="bold", anchor="middle", lh=1.4))
        if b:
            out.append(text(cx, y + 44 + text_h(len(t), 14, 1.4) + 3, b, size=12.5, anchor="middle", lh=1.45))
        maxh = max(maxh, text_h(len(t), 14, 1.4) + text_h(len(b), 12.5, 1.45))
    return y + 44 + maxh + PAD - 8, "".join(out)


def fig_sightline(spec):
    """衛星SARが測れる向き。上から見た図。"""
    out = []
    top, h = PAD + 30, 210
    sy = top + h / 2
    ox = PAD + 70
    # 電波の広がり
    out.append(f'<polygon points="{ox + 14},{sy} {W - PAD - 70},{top} {W - PAD - 70},{top + h}" fill="{PALE}" opacity="0.7"/>')
    # 衛星の進む線（ほぼ南北）
    out.append(f'<line x1="{ox}" y1="{top + h}" x2="{ox}" y2="{top + 8}" stroke="{DEEP}" stroke-width="2.5" '
               f'stroke-dasharray="7 6" marker-end="url(#ah-{DEEP[1:]})"/>')
    out.append(text(ox, top - 10, "衛星の進む向き", size=13, fill=DEEP, weight="bold", anchor="middle"))
    out.append(text(ox, top + h + 20, "（ほぼ南北）", size=12.5, fill=DEEP, anchor="middle"))
    # 衛星
    out.append(rect(ox - 30, sy - 9, 60, 18, MAIN, "none", r=3))
    out.append(rect(ox - 11, sy - 15, 22, 30, DEEP, "none", r=4))
    out.append(arrow(ox + 40, sy, ox + 150, sy, MAIN, 3))
    out.append(text(ox + 44, sy - 14, "電波を横向きに", size=13, fill=DEEP, weight="bold"))
    out.append(text(ox + 44, sy + 24, "当てる", size=13, fill=DEEP, weight="bold"))
    # 捉えやすい動き（東西）
    bw, bh = 170, 112
    x1 = ox + 190
    out.append(rect(x1, sy - bh / 2, bw, bh, "#fff", MAIN, sw=2))
    out.append(text(x1 + bw / 2, sy - bh / 2 + 26, "東西の動き", size=15, fill=DEEP, weight="bold", anchor="middle"))
    out.append(f'<line x1="{x1 + 36}" y1="{sy + 2}" x2="{x1 + bw - 36}" y2="{sy + 2}" stroke="{MAIN}" stroke-width="4.5" '
               f'stroke-linecap="round" marker-start="url(#ah-{MAIN[1:]})" marker-end="url(#ah-{MAIN[1:]})"/>')
    out.append(text(x1 + bw / 2, sy + bh / 2 - 14, "○ 捉えやすい", size=14.5, fill=DEEP, weight="bold", anchor="middle"))
    # 捉えにくい動き（南北）
    x2 = x1 + bw + 22
    out.append(rect(x2, sy - bh / 2, bw, bh, "#fff", GRAY, sw=2))
    out.append(text(x2 + bw / 2, sy - bh / 2 + 26, "南北の動き", size=15, fill=INK, weight="bold", anchor="middle"))
    out.append(f'<line x1="{x2 + bw / 2}" y1="{sy - 16}" x2="{x2 + bw / 2}" y2="{sy + 20}" stroke="{GRAY}" stroke-width="4.5" '
               f'stroke-linecap="round" marker-start="url(#ah-{GRAY[1:]})" marker-end="url(#ah-{GRAY[1:]})"/>')
    out.append(text(x2 + bw / 2, sy + bh / 2 - 14, "△ 捉えにくい", size=14.5, fill=GRAY, weight="bold", anchor="middle"))
    # 方位
    nx = W - PAD - 30
    out.append(arrow(nx, top + 62, nx, top + 22, INK, 2.5))
    out.append(text(nx, top + 8, "北", size=14, weight="bold", anchor="middle"))
    # 説明
    note = wrap(spec.get("note", "測れるのは、衛星に近づく動きと遠ざかる動きだけ。"), (W - PAD * 2 - 28) / 14)
    ny = top + h + 36
    nh = text_h(len(note), 14) + 16
    out.append(rect(PAD, ny, W - PAD * 2, nh, GRAY_PALE, "none", r=8))
    out.append(text(W / 2, ny + 26, note, size=14, weight="bold", anchor="middle"))
    return ny + nh + PAD, "".join(out)


def fmt_num(v):
    """数字を、桁区切り付きで書く。小数は必要なときだけ。"""
    return f"{v:,.0f}" if float(v).is_integer() else f"{v:,.1f}"


def chart_frame(spec, body_h):
    """グラフの題名と、下の出どころ。戻り値は（上端のy、全体の高さ、部品）。"""
    out, y = [], PAD + 6
    if spec.get("title"):
        out.append(text(PAD, y + 14, spec["title"], size=16, weight="bold"))
        y += 26
    if spec.get("unit"):
        out.append(text(PAD, y + 12, f"単位：{spec['unit']}", size=12.5, fill=GRAY))
        y += 20
    top = y + 12
    bottom = top + body_h
    src = wrap("出どころ：" + spec["source"], (W - PAD * 2) / 12) if spec.get("source") else []
    if src:
        out.append(text(PAD, bottom + 26, src, size=12, fill=GRAY, lh=1.45))
    return top, bottom + (22 + text_h(len(src), 12, 1.45) if src else 0) + PAD - 4, out


def fig_bar(spec):
    """横棒のグラフ。大きさを比べる。1系列だけ。値は棒の右に書く。"""
    items = spec["items"]
    label_w = min(250, max(sum(units(c) for c in i["label"]) for i in items) * 14 + 10)
    row, bar_h = 44, 20
    top, height, out = chart_frame(spec, len(items) * row)
    x0 = PAD + label_w + 10
    vmax = max(i["value"] for i in items)
    span = W - PAD - x0 - 120          # 値の文字を書く場所を右に残す
    out.append(f'<line x1="{x0}" y1="{top - 4}" x2="{x0}" y2="{top + len(items) * row - 6}" stroke="{GRAY}" stroke-width="1"/>')
    for k, it in enumerate(items):
        cy = top + k * row + row / 2 - 5
        w = max(3, span * it["value"] / vmax)
        fill = GRAY if it.get("muted") else MAIN     # 予測や参考値は灰色にする
        out.append(text(x0 - 12, cy + 5, wrap(it["label"], label_w / 14)[:2], size=14, anchor="end", lh=1.2))
        out.append(f'<path d="M{x0},{cy - bar_h / 2} h{w - 4:.1f} a4,4 0 0 1 4,4 v{bar_h - 8} a4,4 0 0 1 -4,4 h-{w - 4:.1f} z" fill="{fill}"/>')
        label = fmt_num(it["value"]) + (f"　{it['note']}" if it.get("note") else "")
        out.append(text(x0 + w + 8, cy + 5, label, size=14, weight="bold"))
    return height, "".join(out)


def fig_range(spec):
    """推計の幅。出どころごとに、小さい値から大きい値までを1本の帯で示す。"""
    items = spec["items"]
    label_w = min(250, max(sum(units(c) for c in i["label"]) for i in items) * 14 + 10)
    row = 46
    top, height, out = chart_frame(spec, len(items) * row + 26)
    x0 = PAD + label_w + 10
    x1 = W - PAD - 30
    vmax = max(i.get("high", i["low"]) for i in items) * 1.08
    sx = lambda v: x0 + (x1 - x0) * v / vmax
    base = top + len(items) * row
    out.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="{GRAY}" stroke-width="1"/>')
    for frac in (0, 0.5, 1):
        v = vmax / 1.08 * frac
        out.append(f'<line x1="{sx(v):.1f}" y1="{top - 4}" x2="{sx(v):.1f}" y2="{base}" stroke="{GRAY_PALE}" stroke-width="1"/>')
        out.append(text(sx(v), base + 18, fmt_num(v), size=12, fill=GRAY, anchor="middle"))
    for k, it in enumerate(items):
        cy = top + k * row + row / 2 - 4
        lo, hi = it["low"], it.get("high", it["low"])
        out.append(text(x0 - 12, cy + 5, wrap(it["label"], label_w / 14)[:2], size=14, anchor="end", lh=1.2))
        if hi > lo:
            out.append(rect(sx(lo), cy - 7, sx(hi) - sx(lo), 14, MAIN, "none", r=7))
            label = f"{fmt_num(lo)}〜{fmt_num(hi)}"
        else:
            out.append(f'<circle cx="{sx(lo):.1f}" cy="{cy}" r="7" fill="{MAIN}"/>')
            label = fmt_num(lo)
        if it.get("note"):
            label += f"　{it['note']}"
        tx = sx(hi) + 12
        anchor = "start"
        if tx + len(label) * 12 > W - PAD:      # 右にはみ出すときは、帯の上に書く
            tx, anchor = sx(hi), "end"
            out.append(text(tx, cy - 13, label, size=13, weight="bold", anchor=anchor))
        else:
            out.append(text(tx, cy + 5, label, size=13, weight="bold", anchor=anchor))
    return height, "".join(out)


def fig_thumbnail(spec):
    """noteの見出し画像（1280×670）。題名を大きく入れる。図ではなく、完成したSVGを返す。"""
    tw, th = 1280, 670
    kinds = {"news": ("時事解説", MAIN, DEEP), "course": ("講座", DEEP, MAIN),
             "guide": ("実務メモ", WARM, WARM_DEEP), "report": ("市場レポート", DEEP, MAIN)}
    label, c1, c2 = kinds[spec.get("kind", "news")]
    lines = wrap(spec["title"], 15)[:3]
    size = 76 if len(lines) <= 2 else 66
    out = [
        f'<rect width="{tw}" height="{th}" fill="#ffffff"/>',
        f'<rect width="{tw}" height="{th}" fill="{PALE}" opacity="0.55"/>',
        f'<rect x="0" y="0" width="34" height="{th}" fill="{c1}"/>',
        f'<circle cx="{tw - 90}" cy="{th + 40}" r="330" fill="{c1}" opacity="0.13"/>',
        f'<circle cx="{tw + 40}" cy="110" r="210" fill="{c1}" opacity="0.10"/>',
        rect(96, 78, 40 + len(label) * 34, 62, c1, "none", r=31),
        text(116 + len(label) * 17, 121, label, size=34, fill="#fff", weight="bold", anchor="middle"),
    ]
    if spec.get("tag"):
        out.append(text(96 + 40 + len(label) * 34 + 26, 121, spec["tag"], size=32, fill=c2, weight="bold"))
    ty = 268 if len(lines) <= 2 else 250
    out.append(text(96, ty, lines, size=size, fill=INK, weight="900", lh=1.34))
    if spec.get("sub"):
        sy = ty + size * 1.34 * (len(lines) - 1) + 78
        out.append(rect(96, sy - 46, 14, 58, c1, "none", r=4))
        out.append(text(128, sy, wrap(spec["sub"], 28)[:1], size=36, fill=c2, weight="bold"))
    out.append(text(tw - 70, th - 52, spec.get("brand", "衛星データ実務講座"), size=28, fill=DEEP, weight="bold", anchor="end"))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {tw} {th}" width="{tw}" height="{th}" '
            f'font-family="{FONT}" role="img"><title>{escape(spec["title"])}</title>{"".join(out)}</svg>\n')


TYPES = {
    "thumbnail": fig_thumbnail,
    "bar": fig_bar,
    "range": fig_range,
    "cards": fig_cards,
    "flow": fig_flow,
    "funnel": fig_funnel,
    "split": fig_split,
    "scale": fig_scale,
    "sightline": fig_sightline,
}


def find_browser():
    """PNGへの変換に使うブラウザを探す。なければ None。"""
    # 画面の枠を持たない版を優先する（普通の版は、下が切れた画像になる）
    for pattern in ("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell",
                    "/opt/pw-browsers/chromium-*/chrome-linux/chrome"):
        found = sorted(glob.glob(pattern))
        if found:
            return found[-1]
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        if shutil.which(name):
            return shutil.which(name)
    return None


def to_png(svg_path, scale=2):
    """SVGをPNGにする（noteはSVGを貼れないため）。同じ場所に同じ名前で保存する。"""
    browser = find_browser()
    if not browser:
        print(f"  PNGを作れませんでした（ブラウザがありません）: {svg_path.name}")
        return False
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_path.read_text(encoding="utf-8"))
    w, h = int(float(m.group(1))), int(float(m.group(2)))
    png = svg_path.with_suffix(".png")
    page = svg_path.with_suffix(".html")
    page.write_text(f'<html><body style="margin:0"><img src="{svg_path.name}" '
                    f'style="display:block;width:{w}px;height:{h}px"></body></html>', encoding="utf-8")
    subprocess.run(
        [browser, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
         f"--window-size={w},{h + 200}", f"--force-device-scale-factor={scale}",
         f"--screenshot={png}", page.resolve().as_uri()],
        capture_output=True, timeout=90)
    page.unlink()
    if not png.exists():
        print(f"  PNGを作れませんでした: {svg_path.name}")
        return False
    # 下に付けた余白を切り取る
    try:
        from PIL import Image
        img = Image.open(png)
        img.crop((0, 0, w * scale, h * scale)).save(png)
    except ImportError:
        print(f"  Pillowがないため、下に余白が残っています: {png.name}（pip install pillow）")
    return True


def render(spec_file, dest, png):
    doc = yaml.safe_load(spec_file.read_text(encoding="utf-8")) or {}
    dest.mkdir(exist_ok=True)
    count = 0
    for fig in doc.get("figures", []):
        if fig["type"] not in TYPES:
            raise SystemExit(f"{spec_file}: 図の型 '{fig['type']}' は patterns/figures.md にありません")
        result = TYPES[fig["type"]](fig)
        if isinstance(result, str):          # 見出し画像は完成したSVG
            content = result
        else:
            content = svg(result[0], result[1], fig.get("alt", fig["id"]))
        path = dest / f"{fig['id']}.svg"
        path.write_text(content, encoding="utf-8")
        if png:
            to_png(path)
        count += 1
    return count


def build(only=None):
    """章の図（figures/<章のid>.yaml）と、note記事の図（note/<記事>/figures.yaml）を作る。"""
    count = 0
    for f in sorted((ROOT / "figures").glob("*.yaml")):
        if only and f.stem != only:
            continue
        count += render(f, ROOT / "figures" / f.stem, png=False)
    # note記事の図は、貼り付けられるようにPNGも作る
    for f in sorted((ROOT / "note").glob("*/figures.yaml")):
        if only and f.parent.name != only:
            continue
        count += render(f, f.parent, png=True)
    print(f"図を {count} 個作りました")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else None)
