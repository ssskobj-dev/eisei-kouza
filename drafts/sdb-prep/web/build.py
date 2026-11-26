#!/usr/bin/env python3
"""ch1.src.html の %%IMG:名前%% に img/<名前>.svg を埋め込み、ch1.html を作る。"""
import base64, re
from pathlib import Path
here = Path(__file__).resolve().parent
src = (here / "ch1.src.html").read_text(encoding="utf-8")
def img(m):
    svg = (here.parent / "img" / f"{m.group(1)}.svg").read_bytes()
    return "data:image/svg+xml;base64," + base64.b64encode(svg).decode()
(here / "ch1.html").write_text(re.sub(r"%%IMG:([\w-]+)%%", img, src), encoding="utf-8")
print(here / "ch1.html")
