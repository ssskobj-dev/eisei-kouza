"""図解に使う絵（アイコン）の部品。figures.py の scene 型から使う。

どの部品も icon(name, cx, cy, size, color) で SVG の文字列を返す。中心 (cx, cy)、大きさ size（高さの目安、px）。
色は role（satellite=青、human=橙、none=灰）か、色コード。部品の中の固定色（太陽の黄、木の緑、空の水色）はそのまま。
"""

NAVY, BLUE, PALE_BLUE = "#0b1524", "#2f5d94", "#9fb8d8"
ORANGE, ORANGE_DEEP = "#ff6b2c", "#c2410c"
GRAY, GRAY_PALE = "#8a949c", "#cfd6dc"
SUN, SUN_RAY = "#f5b731", "#f5b731"
GREEN, GREEN_DEEP, TRUNK = "#5aa553", "#3b7a3a", "#8a5a2b"
SAND, SAND_DEEP = "#e6d4b0", "#cdb98c"
WATER, WATER_DEEP = "#4f8fd6", "#2f5d94"
CLOUD = "#ffffff"
WHITE = "#ffffff"


def g(cx, cy, size, body, base=100):
    """部品は 100×100 の座標で描き、(cx, cy) を中心に size に拡大縮小する。"""
    s = size / base
    return f'<g transform="translate({cx - size / 2:.1f},{cy - size / 2:.1f}) scale({s:.4f})">{body}</g>'


def satellite(cx, cy, size, color=NAVY):
    panel = BLUE
    body = (
        f'<rect x="2" y="38" width="30" height="22" rx="3" fill="{panel}" stroke="{NAVY}" stroke-width="2"/>'
        f'<rect x="68" y="38" width="30" height="22" rx="3" fill="{panel}" stroke="{NAVY}" stroke-width="2"/>'
        + "".join(f'<line x1="{x}" y1="40" x2="{x}" y2="58" stroke="{NAVY}" stroke-width="1.5"/>' for x in (12, 22, 78, 88))
        + f'<line x1="32" y1="49" x2="38" y2="49" stroke="{NAVY}" stroke-width="3"/>'
        f'<line x1="62" y1="49" x2="68" y2="49" stroke="{NAVY}" stroke-width="3"/>'
        f'<rect x="38" y="32" width="24" height="34" rx="5" fill="{color}"/>'
        f'<rect x="44" y="40" width="12" height="7" rx="2" fill="{WHITE}" opacity="0.85"/>'
        f'<path d="M42,66 L58,66 L50,78 Z" fill="{color}"/>'
        f'<circle cx="50" cy="80" r="4" fill="{WHITE}" stroke="{color}" stroke-width="2"/>'
    )
    return g(cx, cy, size, body)


def sun(cx, cy, size, color=SUN):
    rays = "".join(
        f'<line x1="50" y1="6" x2="50" y2="18" stroke="{color}" stroke-width="5" stroke-linecap="round" transform="rotate({a} 50 50)"/>'
        for a in range(0, 360, 45))
    return g(cx, cy, size, rays + f'<circle cx="50" cy="50" r="22" fill="{color}"/>')


def moon(cx, cy, size, color="#f3e39a"):
    body = f'<path d="M62,14 A36,36 0 1,0 86,62 A28,28 0 1,1 62,14 Z" fill="{color}"/>'
    return g(cx, cy, size, body)


def cloud(cx, cy, size, color=CLOUD, stroke=GRAY_PALE):
    body = (f'<path d="M26,72 A16,16 0 0,1 24,40 A20,20 0 0,1 60,30 A16,16 0 0,1 86,48 A13,13 0 0,1 82,72 Z" '
            f'fill="{color}" stroke="{stroke}" stroke-width="2.5" stroke-linejoin="round"/>')
    return g(cx, cy, size, body)


def rain_cloud(cx, cy, size, color="#5f6f85"):
    drops = "".join(f'<line x1="{x}" y1="78" x2="{x - 6}" y2="96" stroke="{WATER}" stroke-width="4" stroke-linecap="round"/>'
                    for x in (34, 52, 70))
    body = (f'<path d="M26,72 A16,16 0 0,1 24,40 A20,20 0 0,1 60,30 A16,16 0 0,1 86,48 A13,13 0 0,1 82,72 Z" fill="{color}"/>' + drops)
    return g(cx, cy, size, body)


def tree(cx, cy, size, color=GREEN):
    body = (f'<rect x="44" y="66" width="12" height="28" rx="2" fill="{TRUNK}"/>'
            f'<circle cx="50" cy="44" r="26" fill="{color}"/>'
            f'<circle cx="32" cy="56" r="16" fill="{GREEN_DEEP}"/>'
            f'<circle cx="68" cy="56" r="16" fill="{GREEN_DEEP}"/>')
    return g(cx, cy, size, body)


def building(cx, cy, size, color=PALE_BLUE):
    wins = "".join(f'<rect x="{x}" y="{y}" width="9" height="9" fill="{WHITE}"/>'
                   for x in (24, 40, 56) for y in (20, 36, 52, 68))
    body = f'<rect x="14" y="8" width="60" height="88" rx="3" fill="{color}" stroke="{NAVY}" stroke-width="2"/>' + wins
    return g(cx, cy, size, body)


def buildings(cx, cy, size, color=PALE_BLUE):
    body = (f'<rect x="4" y="30" width="38" height="66" rx="3" fill="{color}" stroke="{NAVY}" stroke-width="2"/>'
            f'<rect x="50" y="10" width="46" height="86" rx="3" fill="{color}" stroke="{NAVY}" stroke-width="2"/>'
            + "".join(f'<rect x="{x}" y="{y}" width="7" height="8" fill="{WHITE}"/>' for x in (12, 26) for y in (40, 56, 72))
            + "".join(f'<rect x="{x}" y="{y}" width="8" height="9" fill="{WHITE}"/>' for x in (58, 72, 86) for y in (20, 38, 56, 74)))
    return g(cx, cy, size, body)


def mountain(cx, cy, size, color=SAND_DEEP, lit="left"):
    """山。lit は明るい側（衛星が電波を当てる側）。left なら左の面が明るく、右の面が影。"""
    bright, dark = "#d9c79b", "#7d6a4d"
    lf, rf = (bright, dark) if lit == "left" else (dark, bright)
    body = (f'<path d="M0,96 L42,16 L42,96 Z" fill="{lf}"/>'
            f'<path d="M42,16 L100,96 L42,96 Z" fill="{rf}"/>'
            f'<path d="M0,96 L42,16 L100,96" fill="none" stroke="{NAVY}" stroke-width="2" stroke-linejoin="round" opacity="0.35"/>')
    return g(cx, cy, size, body)


def water(cx, cy, size, color=WATER, calm=True):
    if calm:
        body = (f'<rect x="0" y="40" width="100" height="40" rx="6" fill="{color}"/>'
                f'<line x1="14" y1="54" x2="50" y2="54" stroke="{WHITE}" stroke-width="3" stroke-linecap="round" opacity="0.6"/>'
                f'<line x1="60" y1="64" x2="86" y2="64" stroke="{WHITE}" stroke-width="3" stroke-linecap="round" opacity="0.6"/>')
    else:
        body = (f'<rect x="0" y="40" width="100" height="40" rx="6" fill="{color}"/>'
                f'<path d="M6,56 q8,-10 16,0 t16,0 t16,0 t16,0 t16,0 t16,0" fill="none" stroke="{WHITE}" stroke-width="3.5" opacity="0.8"/>')
    return g(cx, cy, size, body)


def field(cx, cy, size, color=GREEN):
    rows = "".join(f'<line x1="10" y1="{y}" x2="90" y2="{y}" stroke="{GREEN_DEEP}" stroke-width="3" stroke-dasharray="6 5"/>'
                   for y in (40, 52, 64, 76))
    body = f'<rect x="4" y="30" width="92" height="54" rx="6" fill="{color}" opacity="0.75"/>' + rows
    return g(cx, cy, size, body)


def ground(cx, cy, size, color=SAND):
    return g(cx, cy, size, f'<rect x="0" y="40" width="100" height="40" fill="{color}"/>')


def magnifier(cx, cy, size, color=BLUE):
    body = (f'<circle cx="42" cy="42" r="28" fill="{WHITE}" stroke="{color}" stroke-width="8"/>'
            f'<line x1="63" y1="63" x2="90" y2="90" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>'
            f'<rect x="30" y="30" width="10" height="10" fill="{color}"/><rect x="44" y="44" width="10" height="10" fill="{color}"/>')
    return g(cx, cy, size, body)


def calendar(cx, cy, size, color=BLUE):
    dots = "".join(f'<rect x="{x}" y="{y}" width="9" height="9" rx="2" fill="{PALE_BLUE}"/>' for x in (18, 34, 50, 66) for y in (46, 62, 78))
    body = (f'<rect x="8" y="18" width="84" height="76" rx="8" fill="{WHITE}" stroke="{NAVY}" stroke-width="3"/>'
            f'<rect x="8" y="18" width="84" height="20" rx="8" fill="{color}"/>'
            f'<rect x="24" y="8" width="8" height="18" rx="3" fill="{NAVY}"/><rect x="68" y="8" width="8" height="18" rx="3" fill="{NAVY}"/>'
            + dots + f'<rect x="50" y="62" width="9" height="9" rx="2" fill="{color}"/>')
    return g(cx, cy, size, body)


def ruler(cx, cy, size, color="#f3d35a"):
    ticks = "".join(f'<line x1="{x}" y1="40" x2="{x}" y2="{52 if i % 2 else 58}" stroke="{NAVY}" stroke-width="2.5"/>'
                    for i, x in enumerate(range(16, 90, 9)))
    body = f'<rect x="6" y="36" width="88" height="30" rx="4" fill="{color}" stroke="{NAVY}" stroke-width="3"/>' + ticks
    return g(cx, cy, size, body)


def coins(cx, cy, size, color="#f3d35a"):
    body = "".join(
        f'<ellipse cx="50" cy="{y}" rx="34" ry="12" fill="{color}" stroke="{ORANGE_DEEP}" stroke-width="2.5"/>'
        for y in (78, 64, 50, 36)) + f'<text x="50" y="42" font-size="16" font-weight="bold" fill="{ORANGE_DEEP}" text-anchor="middle">¥</text>'
    return g(cx, cy, size, body)


def check(cx, cy, size, color=BLUE):
    body = (f'<circle cx="50" cy="50" r="46" fill="{color}"/>'
            f'<path d="M28,52 L44,68 L74,34" fill="none" stroke="{WHITE}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')
    return g(cx, cy, size, body)


def cross(cx, cy, size, color=ORANGE):
    body = (f'<circle cx="50" cy="50" r="46" fill="{color}"/>'
            f'<path d="M32,32 L68,68 M68,32 L32,68" fill="none" stroke="{WHITE}" stroke-width="12" stroke-linecap="round"/>')
    return g(cx, cy, size, body)


def warning(cx, cy, size, color=ORANGE):
    body = (f'<path d="M50,6 L96,90 L4,90 Z" fill="{color}" stroke-linejoin="round"/>'
            f'<rect x="44" y="34" width="12" height="30" rx="4" fill="{WHITE}"/><circle cx="50" cy="76" r="7" fill="{WHITE}"/>')
    return g(cx, cy, size, body)


def eye(cx, cy, size, color=BLUE):
    body = (f'<path d="M4,50 Q50,8 96,50 Q50,92 4,50 Z" fill="{WHITE}" stroke="{color}" stroke-width="6"/>'
            f'<circle cx="50" cy="50" r="18" fill="{color}"/><circle cx="50" cy="50" r="8" fill="{NAVY}"/>')
    return g(cx, cy, size, body)


def person(cx, cy, size, color=ORANGE):
    body = (f'<circle cx="50" cy="26" r="18" fill="{color}"/>'
            f'<path d="M14,96 Q14,56 50,56 Q86,56 86,96 Z" fill="{color}"/>')
    return g(cx, cy, size, body)


def drone(cx, cy, size, color=NAVY):
    body = (f'<rect x="36" y="42" width="28" height="18" rx="5" fill="{color}"/>'
            f'<line x1="22" y1="50" x2="36" y2="50" stroke="{color}" stroke-width="4"/><line x1="64" y1="50" x2="78" y2="50" stroke="{color}" stroke-width="4"/>'
            f'<ellipse cx="18" cy="48" rx="16" ry="4" fill="{PALE_BLUE}"/><ellipse cx="82" cy="48" rx="16" ry="4" fill="{PALE_BLUE}"/>'
            f'<circle cx="50" cy="64" r="5" fill="{WHITE}" stroke="{color}" stroke-width="2"/>')
    return g(cx, cy, size, body)


def radar_waves(cx, cy, size, color=ORANGE, n=3):
    """電波の広がり（同心の弧）。上から下へ広がる向き。"""
    body = "".join(f'<path d="M{50 - r},{20 + r * 0.55} A{r},{r * 0.55} 0 0,0 {50 + r},{20 + r * 0.55}" fill="none" '
                   f'stroke="{color}" stroke-width="5" stroke-linecap="round"/>' for r in (16, 30, 44)[:n])
    return g(cx, cy, size, body)


def house(cx, cy, size, color=PALE_BLUE):
    body = (f'<path d="M50,10 L94,48 L82,48 L82,92 L18,92 L18,48 L6,48 Z" fill="{color}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
            f'<rect x="42" y="60" width="16" height="32" fill="{NAVY}"/>')
    return g(cx, cy, size, body)


ICONS = {
    "satellite": satellite, "sun": sun, "moon": moon, "cloud": cloud, "rain": rain_cloud, "tree": tree,
    "building": building, "buildings": buildings, "mountain": mountain, "water": water, "field": field, "ground": ground,
    "magnifier": magnifier, "calendar": calendar, "ruler": ruler, "coins": coins, "check": check, "cross": cross,
    "warning": warning, "eye": eye, "person": person, "drone": drone, "radar": radar_waves, "house": house,
}


def icon(name, cx, cy, size, color=None, **kw):
    fn = ICONS[name]
    return fn(cx, cy, size, color, **kw) if color else fn(cx, cy, size, **kw)
