#!/usr/bin/env python3
"""第1章の図（イラスト入り）を作る。素案。
使い方: python drafts/sdb-prep/illust_ch1.py  →  drafts/sdb-prep/img/*.svg
色はサイトの図（scripts/figures.py）と同じ。絵はすべてこのファイルで描いたもの（外部の素材は使っていない）。
"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent / "img"
MAIN, DEEP, PALE, INK = "#2f5d94", "#0b1524", "#e6edf6", "#1a2433"
WARM, WARM_DEEP, WARM_PALE = "#ff6b2c", "#c2410c", "#ffeee5"
GRAY, GRAY_PALE = "#8a949c", "#eef1f3"
SKY, NIGHT, NIGHT2 = "#dcebf8", "#13233d", "#1d3557"
GREEN, GREEN_D, GROUND = "#5fa35a", "#3e7a3b", "#c9b48a"
SUN, CLOUD = "#ffc23d", "#ffffff"
FONT = "'Noto Sans CJK JP','Noto Sans JP','Hiragino Sans','Yu Gothic','Meiryo',sans-serif"


def svg(w, h, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'font-family="{FONT}" role="img"><title>{title}</title>'
            '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
            '<marker id="ahw" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{WARM}"/></marker>'
            '<marker id="ahy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="#e0a100"/></marker></defs>'
            f'<rect width="{w}" height="{h}" rx="14" fill="#fff"/>{body}</svg>\n')


def t(x, y, s, size=15, weight=400, fill=INK, anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>'


# ---------- 絵の部品 ----------
def satellite(x, y, s=1.0, dish=False, body=MAIN, panel="#3b77b8", rot=0):
    """人工衛星。x,y は胴の中心。"""
    g = [f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">']
    for sx in (-1, 1):  # 太陽電池パネル
        px = 22 if sx > 0 else -62
        g.append(f'<line x1="{14*sx}" y1="0" x2="{22*sx}" y2="0" stroke="{INK}" stroke-width="2.5"/>')
        g.append(f'<rect x="{px}" y="-11" width="40" height="22" rx="2" fill="{panel}" stroke="{INK}" stroke-width="1.8"/>')
        for k in (1, 2, 3):
            g.append(f'<line x1="{px + 10*k}" y1="-11" x2="{px + 10*k}" y2="11" stroke="#9cc3ea" stroke-width="1"/>')
        g.append(f'<line x1="{px}" y1="0" x2="{px+40}" y2="0" stroke="#9cc3ea" stroke-width="1"/>')
    g.append(f'<rect x="-14" y="-16" width="28" height="32" rx="4" fill="{body}" stroke="{INK}" stroke-width="2"/>')
    g.append(f'<rect x="-8" y="-9" width="16" height="6" rx="1.5" fill="#cfe0f2"/>')
    if dish:
        g.append(f'<path d="M-12,16 Q0,34 12,16 Z" fill="#f2f5f7" stroke="{INK}" stroke-width="1.8"/>')
        g.append(f'<line x1="0" y1="16" x2="0" y2="27" stroke="{INK}" stroke-width="1.6"/>')
    else:
        g.append(f'<rect x="-6" y="16" width="12" height="7" rx="1.5" fill="{INK}"/>')
        g.append('<circle cx="0" cy="24" r="3.5" fill="#9cc3ea" stroke="#0b1524" stroke-width="1.2"/>')
    g.append('</g>')
    return "".join(g)


def sun(x, y, r=20):
    rays = "".join(
        f'<line x1="{x + math.cos(a)*(r+5):.1f}" y1="{y + math.sin(a)*(r+5):.1f}" '
        f'x2="{x + math.cos(a)*(r+13):.1f}" y2="{y + math.sin(a)*(r+13):.1f}" stroke="{SUN}" stroke-width="3.5" stroke-linecap="round"/>'
        for a in [i * math.pi / 4 for i in range(8)])
    return rays + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SUN}"/>'


def moon(x, y, r=16, bg=NIGHT):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f6e7a8"/>'
            f'<circle cx="{x + r*0.45}" cy="{y - r*0.3}" r="{r*0.9}" fill="{bg}"/>')


def stars(pts):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" opacity="0.8"/>' for x, y, r in pts)


def cloud(x, y, s=1.0, fill=CLOUD, stroke="#c5d3e2"):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M-40,12 Q-46,-6 -28,-8 Q-24,-26 -4,-22 Q8,-34 24,-20 Q44,-20 42,0 Q52,8 40,14 Z" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"/></g>')


def rain(x, y, n=4, color="#7fb2e5"):
    return "".join(f'<line x1="{x + i*12}" y1="{y + (i % 2)*4}" x2="{x + i*12 - 4}" y2="{y + 12 + (i % 2)*4}" '
                   f'stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>' for i in range(n))


def tree(x, y, s=1.0, color=GREEN):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="-3" y="-4" width="6" height="16" fill="#8a5a2b"/>'
            f'<circle cx="0" cy="-14" r="13" fill="{color}"/><circle cx="-9" cy="-6" r="9" fill="{color}"/>'
            f'<circle cx="9" cy="-6" r="9" fill="{color}"/></g>')


def building(x, y, w=26, h=40, color="#b9c7d6"):
    win = "".join(f'<rect x="{x + 5 + (i % 2)*10}" y="{y - h + 6 + (i // 2)*10}" width="6" height="6" fill="#ffffff"/>'
                  for i in range(int(h / 10) * 2 - 2))
    return f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{color}" stroke="{INK}" stroke-width="1.4"/>' + win


def ground(x, y, w, h=26, fill=GROUND):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'


def field(x, y, w=60):
    rows = "".join(f'<line x1="{x + 4}" y1="{y + 4 + i*5}" x2="{x + w - 4}" y2="{y + 4 + i*5}" stroke="{GREEN_D}" stroke-width="2"/>'
                   for i in range(3))
    return f'<rect x="{x}" y="{y}" width="{w}" height="18" rx="2" fill="#a8d08d"/>' + rows


def mountain(x, y, w=120, h=60):
    return (f'<path d="M{x},{y} L{x + w*0.45},{y - h} L{x + w},{y} Z" fill="#9fb69a" stroke="{GREEN_D}" stroke-width="1.5"/>'
            f'<path d="M{x + w*0.36},{y - h*0.8} L{x + w*0.45},{y - h} L{x + w*0.54},{y - h*0.8} Z" fill="#ffffff"/>')


def badge_x(x, y, r=13):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WARM}"/>'
            f'<path d="M{x-5},{y-5} L{x+5},{y+5} M{x+5},{y-5} L{x-5},{y+5}" stroke="#fff" stroke-width="3" stroke-linecap="round"/>')


def badge_ok(x, y, r=13):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{MAIN}"/>'
            f'<path d="M{x-6},{y} L{x-1},{y+5} L{x+7},{y-5}" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


def wave(x1, y1, x2, y2, wl, amp, color, width=3):
    """(x1,y1)→(x2,y2) の向きに進む正弦波。wl は1波長の長さ（px）。"""
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    pts = []
    n = int(L / 2)
    for i in range(n + 1):
        d = L * i / n
        a = amp * math.sin(2 * math.pi * d / wl)
        pts.append(f"{x1 + ux*d + nx*a:.1f},{y1 + uy*d + ny*a:.1f}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'


# ---------- アイコン（48×48 の箱に描く） ----------
def ic_eye(x, y, c=MAIN):
    return (f'<g transform="translate({x},{y})"><path d="M2,24 Q24,4 46,24 Q24,44 2,24 Z" fill="#fff" stroke="{c}" stroke-width="3"/>'
            f'<circle cx="24" cy="24" r="8" fill="{c}"/><circle cx="27" cy="21" r="2.5" fill="#fff"/></g>')


def ic_move(x, y, c=MAIN):
    return (f'<g transform="translate({x},{y})"><path d="M4,34 L18,28 L30,34 L44,26" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M24,4 L24,20" stroke="{WARM}" stroke-width="3" marker-end="url(#ahw)"/><text x="30" y="16" font-size="11" fill="{WARM}" font-weight="700">cm</text></g>')


def ic_calendar(x, y, c=MAIN):
    cells = "".join(f'<rect x="{8 + (i % 4)*9}" y="{20 + (i // 4)*9}" width="6" height="6" fill="{c if i == 6 else PALE}"/>' for i in range(12))
    return (f'<g transform="translate({x},{y})"><rect x="3" y="7" width="42" height="38" rx="5" fill="#fff" stroke="{c}" stroke-width="3"/>'
            f'<rect x="3" y="7" width="42" height="10" rx="5" fill="{c}"/><line x1="14" y1="3" x2="14" y2="11" stroke="{INK}" stroke-width="3"/>'
            f'<line x1="34" y1="3" x2="34" y2="11" stroke="{INK}" stroke-width="3"/>{cells}</g>')


def ic_ruler(x, y, c=MAIN):
    ticks = "".join(f'<line x1="{8 + i*6}" y1="30" x2="{8 + i*6}" y2="{24 if i % 2 else 20}" stroke="{INK}" stroke-width="1.6"/>' for i in range(7))
    return (f'<g transform="translate({x},{y}) rotate(-20 24 24)"><rect x="2" y="16" width="44" height="16" rx="3" fill="#ffe8a3" stroke="{INK}" stroke-width="2"/>{ticks}</g>')


def ic_magnifier(x, y, c=MAIN):
    return (f'<g transform="translate({x},{y})"><circle cx="20" cy="20" r="13" fill="#fff" stroke="{c}" stroke-width="4"/>'
            f'<line x1="30" y1="30" x2="44" y2="44" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<rect x="14" y="14" width="5" height="5" fill="{c}"/><rect x="20" y="20" width="5" height="5" fill="{c}"/>'
            f'<rect x="20" y="14" width="5" height="5" fill="{PALE}"/><rect x="14" y="20" width="5" height="5" fill="{PALE}"/></g>')


def ic_swath(x, y, c=MAIN):
    return (f'<g transform="translate({x},{y})"><path d="M2,40 Q24,30 46,40 L46,10 Q24,0 2,10 Z" fill="{PALE}" stroke="{c}" stroke-width="2.5"/>'
            f'<path d="M14,6 L34,6 L42,42 L6,42 Z" fill="{c}" opacity="0.35"/>'
            f'<line x1="6" y1="24" x2="42" y2="24" stroke="{INK}" stroke-width="2" marker-start="url(#ah)" marker-end="url(#ah)"/></g>')


def ic_coins(x, y):
    return (f'<g transform="translate({x},{y})">'
            + "".join(f'<ellipse cx="24" cy="{38 - i*7}" rx="15" ry="5" fill="#ffd166" stroke="{INK}" stroke-width="1.8"/>' for i in range(4))
            + f'<text x="24" y="20" font-size="12" font-weight="900" fill="{INK}" text-anchor="middle">¥</text></g>')


# ---------- 図1：2種類 ----------
def fig_two_kinds():
    W, H = 900, 440
    b = []
    # 左：光学（昼）
    lx, ly, pw, ph = 24, 24, 414, 250
    b.append(f'<clipPath id="cl"><rect x="{lx}" y="{ly}" width="{pw}" height="{ph}" rx="12"/></clipPath>')
    b.append(f'<g clip-path="url(#cl)"><rect x="{lx}" y="{ly}" width="{pw}" height="{ph}" fill="{SKY}"/>')
    b.append(sun(lx + 52, ly + 52, 20))
    b.append(ground(lx, ly + ph - 40, pw, 40, "#d9c79e"))
    b.append(field(lx + 40, ly + ph - 34, 70))
    b.append(building(lx + 128, ly + ph - 14, 26, 46))
    b.append(building(lx + 158, ly + ph - 14, 22, 30, "#cfd8e2"))
    b.append(tree(lx + 205, ly + ph - 20, 0.9))
    # 雲で遮られる光
    b.append(cloud(lx + 320, ly + 120, 0.95))
    b.append(f'<line x1="{lx + 70}" y1="{ly + 70}" x2="{lx + 140}" y2="{ly + ph - 56}" stroke="#e0a100" stroke-width="2.5" stroke-dasharray="6 5" marker-end="url(#ahy)"/>')
    b.append(f'<line x1="{lx + 150}" y1="{ly + ph - 60}" x2="{lx + 228}" y2="{ly + 70}" stroke="#e0a100" stroke-width="2.5" stroke-dasharray="6 5" marker-end="url(#ahy)"/>')
    b.append(f'<line x1="{lx + 352}" y1="{ly + 140}" x2="{lx + 330}" y2="{ly + ph - 56}" stroke="#e0a100" stroke-width="2.5" stroke-dasharray="6 5" opacity="0.35"/>')
    b.append(badge_x(lx + 340, ly + 175, 12))
    b.append(t(lx + 362, ly + 180, "雲で", 12, 700, WARM_DEEP))
    b.append(t(lx + 362, ly + 195, "写らない", 12, 700, WARM_DEEP))
    b.append(satellite(lx + 245, ly + 52, 0.95))
    b.append('</g>')
    b.append(f'<rect x="{lx}" y="{ly}" width="{pw}" height="{ph}" rx="12" fill="none" stroke="{MAIN}" stroke-width="2"/>')
    b.append(f'<rect x="{lx + 12}" y="{ly + 12}" width="150" height="0" />')
    # 右：SAR（夜）
    rx = 462
    b.append(f'<clipPath id="cr"><rect x="{rx}" y="{ly}" width="{pw}" height="{ph}" rx="12"/></clipPath>')
    b.append(f'<g clip-path="url(#cr)"><rect x="{rx}" y="{ly}" width="{pw}" height="{ph}" fill="{NIGHT}"/>')
    b.append(stars([(rx + 40, ly + 40, 1.6), (rx + 90, ly + 28, 1.2), (rx + 330, ly + 34, 1.5), (rx + 380, ly + 70, 1.2), (rx + 300, ly + 90, 1)]))
    b.append(moon(rx + 370, ly + 44, 16, NIGHT))
    b.append(ground(rx, ly + ph - 40, pw, 40, "#5b5340"))
    b.append(building(rx + 70, ly + ph - 14, 26, 46, "#6e7f93"))
    b.append(building(rx + 100, ly + ph - 14, 22, 30, "#7d8da0"))
    b.append(tree(rx + 150, ly + ph - 20, 0.9, "#3e6e3b"))
    b.append(f'<path d="M{rx + 230},{ly + ph - 40} q30,-4 60,0 q30,4 60,0" fill="none" stroke="#3d6fa6" stroke-width="5"/>')
    b.append(cloud(rx + 170, ly + 120, 0.95, "#3a4d6b", "#56698a"))
    b.append(rain(rx + 140, ly + 140, 5))
    # 電波（扇形の弧）
    sx, sy = rx + 205, ly + 56
    for k, r in enumerate((40, 70, 100, 130, 160)):
        b.append(f'<path d="M{sx - r*0.55:.0f},{sy + r*0.83:.0f} A{r},{r} 0 0 0 {sx + r*0.55:.0f},{sy + r*0.83:.0f}" '
                 f'fill="none" stroke="{WARM}" stroke-width="3" opacity="{1 - k*0.13:.2f}"/>')
    b.append(f'<line x1="{sx + 60}" y1="{ly + ph - 56}" x2="{sx + 18}" y2="{sy + 26}" stroke="#ffd0b8" stroke-width="2.5" stroke-dasharray="6 5" marker-end="url(#ahw)"/>')
    b.append(badge_ok(rx + 300, ly + 150, 12))
    b.append(t(rx + 318, ly + 147, "雲・夜・雨", 12, 700, "#ffd0b8"))
    b.append(t(rx + 318, ly + 162, "でも届く", 12, 700, "#ffd0b8"))
    b.append(satellite(sx, sy, 0.95, dish=True, body="#e8eef5", panel="#3b77b8"))
    b.append('</g>')
    b.append(f'<rect x="{rx}" y="{ly}" width="{pw}" height="{ph}" rx="12" fill="none" stroke="{WARM}" stroke-width="2"/>')
    # 見出しの札
    b.append(f'<rect x="{lx + 14}" y="{ly + ph - 22 - 4}" width="0" height="0"/>')
    for x0, c, head in ((lx, MAIN, "光学 ＝ 昼間の写真"), (rx, WARM, "SAR ＝ 暗闇の懐中電灯")):
        b.append(f'<rect x="{x0}" y="{ly + ph + 14}" width="{pw}" height="40" rx="10" fill="{c}"/>')
        b.append(t(x0 + pw / 2, ly + ph + 40, head, 18, 800, "#fff", "middle"))
    items_l = ["太陽光の反射を写す。見れば分かる", "近赤外で、作物や水も指標にできる", "雲と夜は撮れない"]
    items_r = ["自分で電波を出し、跳ね返りを受ける", "2回撮ると、地面の動きがcm単位で分かる", "写真ではない。読むのに慣れが要る"]
    for x0, items, c in ((lx, items_l, MAIN), (rx, items_r, WARM)):
        for i, s in enumerate(items):
            yy = ly + ph + 82 + i * 26
            b.append(f'<circle cx="{x0 + 18}" cy="{yy - 5}" r="4" fill="{c}"/>')
            b.append(t(x0 + 32, yy, s, 15))
    b.append(f'<circle cx="450" cy="{ly + ph / 2}" r="20" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    b.append(t(450, ly + ph / 2 + 6, "vs", 16, 800, INK, "middle"))
    return svg(W, H, "衛星データは大きく2種類：光学とSAR", "".join(b))


# ---------- 図2：波長と草木 ----------
def fig_band():
    W, H = 900, 440
    b = []
    cols = [("Lバンド", "約24cm", 80, "だいち2号", 44, "抜ける"), ("Cバンド", "約6cm", 30, "Sentinel-1（無償）", 22, "一部だけ"),
            ("Xバンド", "約3cm", 0, "", 11, "葉で返る")]
    cw = 276
    for i, (name, wl, pct, sat, wpx, verdict) in enumerate(cols):
        x0 = 24 + i * (cw + 12)
        b.append(f'<rect x="{x0}" y="20" width="{cw}" height="400" rx="12" fill="{PALE if i == 0 else GRAY_PALE}"/>')
        b.append(t(x0 + 18, 50, name, 19, 800, MAIN if i == 0 else INK))
        b.append(t(x0 + 110, 50, f"波長 {wl}", 14, 700, GRAY))
        # 空と森
        top, base = 70, 250
        b.append(f'<rect x="{x0 + 14}" y="{top}" width="{cw - 28}" height="{base - top}" rx="8" fill="{SKY}"/>')
        b.append(ground(x0 + 14, base - 22, cw - 28, 22, "#d9c79e"))
        for k in range(5):
            b.append(tree(x0 + 44 + k * 48, base - 22, 1.35, GREEN if k % 2 else GREEN_D))
        # 電波
        sx = x0 + cw / 2
        if i == 0:
            b.append(wave(sx - 30, top + 8, sx + 10, base - 22, wpx, 7, WARM, 3))
            b.append(f'<circle cx="{sx + 10}" cy="{base - 22}" r="5" fill="{WARM}"/>')
        elif i == 1:
            b.append(wave(sx - 50, top + 8, sx - 10, base - 52, wpx, 6, WARM, 3))
            b.append(wave(sx - 10, base - 52, sx + 2, base - 22, wpx, 6, WARM, 2))
            b.append(f'<path d="M{sx - 10},{base - 52} L{sx + 40},{top + 20}" stroke="{WARM}" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ahw)"/>')
        else:
            b.append(wave(sx - 50, top + 8, sx - 12, base - 58, wpx, 5, WARM, 3))
            b.append(f'<path d="M{sx - 12},{base - 58} L{sx + 40},{top + 14}" stroke="{WARM}" stroke-width="2.4" stroke-dasharray="5 4" marker-end="url(#ahw)"/>')
            b.append(badge_x(sx + 52, base - 70, 11))
        b.append(t(x0 + cw - 24, top + 22, verdict, 13, 800, WARM_DEEP, "end"))
        # 割合の棒
        by = 286
        b.append(t(x0 + 18, by, "山地で干渉の質が保てた割合", 12, 700, GRAY))
        b.append(f'<rect x="{x0 + 18}" y="{by + 10}" width="{cw - 36}" height="18" rx="9" fill="#ffffff"/>')
        if pct:
            b.append(f'<rect x="{x0 + 18}" y="{by + 10}" width="{(cw - 36) * pct / 100:.0f}" height="18" rx="9" fill="{MAIN}"/>')
        b.append(t(x0 + 18, by + 66, f"{'約' if pct else ''}{pct}%", 34, 900, MAIN if pct >= 50 else (INK if pct else GRAY)))
        b.append(t(x0 + 18, by + 92, sat if sat else "都市部なら90%以上", 13, 700, INK))
        if i == 2:
            b.append(building(x0 + cw - 70, by + 98, 18, 34))
            b.append(building(x0 + cw - 48, by + 98, 22, 46, "#cfd8e2"))
    b.append(t(24, 436, "出典：国土交通省 道路局「合成開口レーダー（SAR）の道路土構造物の維持管理への活用マニュアル（案）」（2021年7月）", 10.5, 400, GRAY))
    return svg(W, H + 6, "SARの波長で変わる、草木の通り抜け", "".join(b))


# ---------- 図3：細かさ・広さ・頻度 ----------
def fig_triangle():
    W, H = 900, 520
    b = []
    A, B, C = (450, 110), (190, 420), (710, 420)
    b.append(f'<path d="M{A[0]},{A[1]} L{B[0]},{B[1]} L{C[0]},{C[1]} Z" fill="{PALE}" stroke="{MAIN}" stroke-width="3" stroke-dasharray="2 0"/>')
    b.append(t(450, 308, "3つ全部は", 20, 800, INK, "middle"))
    b.append(t(450, 336, "取れない", 20, 800, WARM_DEEP, "middle"))
    b.append(satellite(450, 260, 0.75))
    nodes = [(A, "細かさ", ic_magnifier, "1点が地上の何mか"), (B, "広さ", ic_swath, "1回で撮れる幅"), (C, "頻度", ic_calendar, "同じ場所に戻る回数")]
    for (x, y), name, ic, sub in nodes:
        b.append(f'<circle cx="{x}" cy="{y}" r="46" fill="#fff" stroke="{MAIN}" stroke-width="3"/>')
        b.append(ic(x - 24, y - 30))
        b.append(t(x, y + 34, name, 15, 800, MAIN, "middle"))
        dy = -62 if y < 200 else 72
        b.append(t(x, y + dy, sub, 13, 700, GRAY, "middle"))
    # 辺の説明
    b.append(t(250, 250, "細かくするほど", 14, 700, INK, "middle"))
    b.append(t(250, 270, "幅が狭くなる", 14, 700, WARM_DEEP, "middle"))
    b.append(t(450, 462, "幅が狭いほど、一巡りに日数がかかる", 14, 700, INK, "middle"))
    b.append(t(650, 250, "回数を増やすには", 14, 700, INK, "middle"))
    b.append(t(650, 270, "機数と費用が要る", 14, 700, WARM_DEEP, "middle"))
    b.append(ic_coins(726, 236))
    return svg(W, H, "細かさ、広さ、頻度は同時に手に入らない", "".join(b))


# ---------- 図4：3つの問い ----------
def fig_questions():
    W, H = 900, 400
    b = []
    steps = [
        ("見た目か、動きか", [(ic_eye, "見た目→光学"), (ic_move, "動き→干渉SAR")]),
        ("撮る日を選べるか", [(ic_calendar, "待てる→光学"), (None, "待てない→SAR")]),
        ("草木があるか", [(None, "ある→Lバンド"), (None, "ない→C・Xも可")]),
        ("要る細かさは", [(ic_ruler, "対象の大きさ"), (None, "から何mか")]),
    ]
    cw, gap, x0, y0 = 160, 20, 24, 40
    for i, (head, rows) in enumerate(steps):
        x = x0 + i * (cw + gap)
        b.append(f'<rect x="{x}" y="{y0}" width="{cw}" height="300" rx="14" fill="{WARM_PALE}" stroke="{WARM}" stroke-width="2"/>')
        b.append(f'<circle cx="{x + cw / 2}" cy="{y0}" r="17" fill="{WARM}"/>')
        b.append(t(x + cw / 2, y0 + 6, str(i + 1), 17, 900, "#fff", "middle"))
        # 大きな絵
        cx, cy = x + cw / 2, y0 + 95
        b.append(f'<circle cx="{cx}" cy="{cy}" r="48" fill="#fff"/>')
        if i == 0:
            b.append(ic_eye(cx - 46, cy - 26)); b.append(ic_move(cx - 2, cy - 22))
        elif i == 1:
            b.append(ic_calendar(cx - 46, cy - 24)); b.append(cloud(cx + 22, cy + 2, 0.5)); b.append(rain(cx + 6, cy + 10, 3))
        elif i == 2:
            b.append(tree(cx - 14, cy + 22, 1.4)); b.append(tree(cx + 18, cy + 24, 1.1, GREEN_D))
        else:
            b.append(ic_ruler(cx - 24, cy - 24))
        b.append(t(cx, y0 + 175, head, 16, 800, WARM_DEEP, "middle"))
        for k, (_, s) in enumerate(rows):
            yy = y0 + 210 + k * 36
            b.append(f'<rect x="{x + 12}" y="{yy - 20}" width="{cw - 24}" height="28" rx="14" fill="#fff"/>')
            b.append(t(cx, yy - 1, s, 13.5, 700, INK, "middle"))
        if i < 3:
            b.append(f'<line x1="{x + cw + 2}" y1="{y0 + 95}" x2="{x + cw + gap - 2}" y2="{y0 + 95}" stroke="{INK}" stroke-width="2.5" marker-end="url(#ah)"/>')
    # 結果
    b.append(f'<line x1="{x0 + 4*(cw + gap) - gap + 2}" y1="{y0 + 95}" x2="{x0 + 4*(cw + gap) + 10}" y2="{y0 + 95}" stroke="{INK}" stroke-width="2.5" marker-end="url(#ah)"/>')
    rx = x0 + 4 * (cw + gap) + 14
    rw = W - rx - 24
    b.append(f'<rect x="{rx}" y="{y0}" width="{rw}" height="300" rx="14" fill="{PALE}" stroke="{MAIN}" stroke-width="2"/>')
    b.append(satellite(rx + rw / 2, y0 + 92, 0.52))
    b.append(t(rx + rw / 2, y0 + 175, "衛星と", 15, 800, MAIN, "middle"))
    b.append(t(rx + rw / 2, y0 + 195, "撮り方が", 15, 800, MAIN, "middle"))
    b.append(t(rx + rw / 2, y0 + 215, "決まる", 15, 800, MAIN, "middle"))
    b.append(t(rx + rw / 2, y0 + 252, "事業者に", 12, 700, INK, "middle"))
    b.append(t(rx + rw / 2, y0 + 268, "伝える条件", 12, 700, INK, "middle"))
    b.append(t(24, H - 20, "1〜4は人が決めること。決まると、事業者への相談がそのまま具体的になる", 13, 700, GRAY))
    return svg(W, H, "その仕事に使えるかを決める3つの問い", "".join(b))


# ---------- 図5：よくある誤解 ----------
def fig_myths():
    W, H = 900, 470
    b = []
    myths = [
        ("SARは、雲を越える光学", "写真ではない。|見た目の判別には向かない", "sar"),
        ("細かいほど良い", "幅も回数も減る。|要る細かさを先に決める", "fine"),
        ("撮りたい日に撮れる", "回ってくる周期がある。|光学は雲で写らない", "day"),
        ("干渉SARで沈下量が分かる", "分かるのは、衛星から見た|方向の距離の変化", "insar"),
    ]
    cw, ch = 414, 196
    for i, (myth, truth, kind) in enumerate(myths):
        x = 24 + (i % 2) * (cw + 24)
        y = 24 + (i // 2) * (ch + 22)
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="14" fill="#fff" stroke="{GRAY_PALE}" stroke-width="2"/>')
        # 絵の枠
        b.append(f'<rect x="{x + 14}" y="{y + 14}" width="132" height="{ch - 28}" rx="10" fill="{SKY}"/>')
        ix, iy = x + 80, y + 14 + (ch - 28) / 2
        if kind == "sar":
            b.append(f'<rect x="{x + 14}" y="{y + 14}" width="132" height="{ch - 28}" rx="10" fill="{NIGHT}"/>')
            b.append(satellite(ix, iy - 30, 0.6, dish=True, body="#e8eef5"))
            for r in (22, 36, 50):
                b.append(f'<path d="M{ix - r*0.6:.0f},{iy - 18 + r*0.8:.0f} A{r},{r} 0 0 0 {ix + r*0.6:.0f},{iy - 18 + r*0.8:.0f}" fill="none" stroke="{WARM}" stroke-width="2.4"/>')
            b.append(f'<rect x="{ix - 26}" y="{iy + 44}" width="52" height="16" fill="#3a4d6b"/>')
        elif kind == "fine":
            b.append(ic_magnifier(ix - 30, iy - 40))
            b.append(f'<path d="M{ix - 10},{iy + 18} L{ix + 10},{iy + 18} L{ix + 20},{iy + 56} L{ix - 20},{iy + 56} Z" fill="{MAIN}" opacity="0.4"/>')
            b.append(t(ix, iy + 76, "幅が細い", 11, 700, INK, "middle"))
        elif kind == "day":
            b.append(ic_calendar(ix - 44, iy - 40))
            b.append(cloud(ix + 22, iy + 30, 0.6))
            b.append(satellite(ix + 30, iy - 40, 0.45))
        else:
            b.append(satellite(ix + 30, iy - 46, 0.5, dish=True))
            b.append(ground(x + 14, iy + 30, 132, 40, "#d9c79e"))
            b.append(f'<line x1="{ix + 24}" y1="{iy - 30}" x2="{ix - 14}" y2="{iy + 28}" stroke="{WARM}" stroke-width="3" marker-end="url(#ahw)"/>')
            b.append(f'<line x1="{ix - 40}" y1="{iy + 4}" x2="{ix - 40}" y2="{iy + 28}" stroke="{GRAY}" stroke-width="2.4" stroke-dasharray="4 3" marker-end="url(#ah)"/>')
            b.append(t(ix - 40, iy - 2, "真下", 10, 700, GRAY, "middle"))
        b.append(badge_x(x + 146, y + 22, 14))
        # 文字
        tx = x + 166
        b.append(t(tx, y + 40, "よくある誤解", 11.5, 700, GRAY))
        b.append(t(tx, y + 66, f"「{myth}」", 15.5 if len(myth) > 11 else 17, 800, INK))
        b.append(f'<line x1="{tx}" y1="{y + 88}" x2="{x + cw - 18}" y2="{y + 88}" stroke="{GRAY_PALE}" stroke-width="2"/>')
        b.append(badge_ok(tx + 12, y + 114, 11))
        b.append(t(tx + 30, y + 119, "実は", 13, 800, MAIN))
        for k, w in enumerate(truth.split("|")):
            b.append(t(tx, y + 146 + k * 22, w, 13.5, 500, INK))
    return svg(W, H, "よくある4つの誤解", "".join(b))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, fn in (("two-kinds", fig_two_kinds), ("band-mountain", fig_band), ("triangle", fig_triangle),
                     ("three-questions", fig_questions), ("myths", fig_myths)):
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print(OUT / f"{name}.svg")
