#!/usr/bin/env python3
"""動画の台本（video/<id>/script.yaml）の点検。patterns/outputs/video.md の決まりのうち、機械で引っかけられるものを見る。

使い方：
  python scripts/verify_script.py video/<id>/script.yaml ...   指定した台本
  python scripts/verify_script.py --changed                     origin/main から変わった台本
  python scripts/verify_script.py                               未投稿の日本語の台本すべて

「止める」が1つでもあれば終了コード1（プルリクエストの点検で止まる）。「印」は直すのが望ましいが止めない。
"""
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# 言い換えの決まり（左を書かない。右に直す）。日本語の台本だけ
BANNED = [
    (re.compile(r"(使う|同じ|別の|2つの|つの|の)帯(の組|の番号|の取り違え|を読|が違|の幅|の表|と分類|と基準|、基準|を変え|を選|がない|の指数|で暗い|は同じ)|(使う|別の|2つの|同じ)帯(?![域状])"),
     "波長の「帯」は「帯域」と書く（帯状の意味なら「帯状」「帯の形」と書く）"),
    (re.compile(r"短波赤外"), "「短波長赤外」に統一"),
    (re.compile(r"一律にずれ"), "ずらしの誤りは「一律」ではなく「0に向かって縮む」。数字は実際の値で計算して置く"),
]
# 本文の用語が混在していないか（章の中心の用語は1つに決めて通す）
MIXED = [
    (("NDVI",), ("植生の指数", "植生指数")),
    (("NDWI", "MNDWI"), ("水の指数",)),
    (("NBR", "dNBR"), ("焼け跡の指数",)),
]


def scripts_to_check():
    out = []
    for p in sorted((ROOT / "video").glob("*/script.yaml")):
        if (p.parent / "youtube.json").exists() or p.parent.name.endswith("-en"):
            continue
        out.append(p)
    return out


def changed():
    base = os.environ.get("VERIFY_BASE", "origin/main")
    res = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD"], cwd=ROOT, capture_output=True, text=True)
    names = {ROOT / n for n in res.stdout.split()}
    return [p for p in sorted((ROOT / "video").glob("*/script.yaml")) if p in names and not p.parent.name.endswith("-en")]


def overlap(items, say):
    """画面の箇条書きが、ナレーションにそのまま読まれている割合（0〜1）。"""
    if not items or not say:
        return 0.0
    hit = 0
    for it in items:
        core = re.sub(r"[（(].*?[）)]", "", str(it)).strip("。 ")
        core = re.sub(r"[、。・「」]", "", core)
        if len(core) >= 12 and re.sub(r"[、。・「」\s]", "", say).find(core[:max(12, int(len(core) * 0.8))]) >= 0:
            hit += 1
    return hit / len(items)


def check(path):
    stop, mark = [], []
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"YAML が読めません：{e}"], []
    if doc.get("lang", "ja") != "ja":
        return [], []
    scenes = doc.get("scenes", [])
    if not scenes:
        return ["scenes がありません"], []
    text_all = "\n".join(str(s.get("say", "")) + "\n" + "\n".join(map(str, s.get("items", []) or [])) for s in scenes)
    heads = [s.get("heading", "") for s in scenes]

    # 1. 決まりに反する語
    for pat, why in BANNED:
        for i, s in enumerate(scenes):
            blob = str(s.get("say", "")) + "\n" + "\n".join(map(str, s.get("items", []) or [])) + "\n" + "\n".join("\n".join(map(str, r)) for r in (s.get("rows") or []))
            m = pat.search(blob)
            if m:
                ctx = blob[max(0, m.start() - 10):m.end() + 10].replace("\n", " ")
                stop.append(f"場面{i + 1}「{s.get('heading', '')}」：{why}（…{ctx}…）")
                break

    # 2. 用語の混在
    for abbrs, longs in MIXED:
        a = sum(text_all.count(x) for x in abbrs)
        l = sum(text_all.count(x) for x in longs)
        if a and l and min(a, l) >= 3:
            mark.append(f"用語が混在：{'/'.join(abbrs)}（{a}回）と{'/'.join(longs)}（{l}回）。初出で説明して1つに統一する")

    # 3. できるようになること：章の用語（英字の略語か、章の題の語）と数字
    for i, s in enumerate(scenes):
        if "できるようになること" in str(s.get("heading", "")):
            items = s.get("items", []) or []
            has_term = any(re.search(r"[A-Z][A-Za-z0-9]{2,}|σ0|dB", str(it)) for it in items)
            has_num = any(re.search(r"\d", str(it)) for it in items)
            if not has_term:
                mark.append("「できるようになること」に章の用語（NDVI、InSAR、SCL、σ0 など）が無い")
            if not has_num:
                mark.append("「できるようになること」に具体の数字（目安、画素の大きさ、何本 など）が無い")
            for it in items:
                if len(str(it)) > 75:
                    mark.append(f"「できるようになること」の項目が長い（{len(str(it))}字。2行＝75字以内）：{str(it)[:30]}…")

    # 4. 具体例：しくみ・理由の場面に「たとえば」が無い
    for i, s in enumerate(scenes):
        h = str(s.get("heading", ""))
        if any(k in h for k in ("しくみ", "なぜ", "理由")) and not re.search(r"たとえば|例えば|計算してみ|具体的に", str(s.get("say", ""))):
            mark.append(f"場面{i + 1}「{h}」：具体例（「たとえば」）が無い")

    # 5. 画面の箇条書きをナレーションが丸読みしていないか
    for i, s in enumerate(scenes):
        if s.get("kind") in ("bullets", "steps") and s.get("items"):
            r = overlap(s["items"], str(s.get("say", "")))
            if r >= 0.8 and len(s["items"]) >= 3:
                mark.append(f"場面{i + 1}「{s.get('heading', '')}」：画面の箇条書きをナレーションがほぼそのまま読んでいる（{int(r * 100)}%）。画面は要点、ナレーションは理由と例に分ける")

    # 6. コードの場面：擬似コードと明示しているか
    for i, s in enumerate(scenes):
        if s.get("kind") == "code" and "宿題" not in str(s.get("heading", "")):
            blob = str(s.get("heading", "")) + str(s.get("code", "")) + str(s.get("say", ""))
            if "擬似コード" not in blob:
                mark.append(f"場面{i + 1}「{s.get('heading', '')}」：「説明用の擬似コード」と明示する（実在の関数に見える）")

    # 7. 表紙：結論を先に短く
    cover = scenes[0] if scenes[0].get("kind") == "cover" else None
    if cover:
        say = str(cover.get("say", ""))
        first_ans = re.search(r"答えは[、，](.{0,200}?)[。]", say)
        if first_ans and len(first_ans.group(1)) > 60:
            mark.append(f"表紙：「答えは…」の1文が長い（{len(first_ans.group(1))}字）。結論を短く言い、作業は分けて後から")

    # 9. 英語の読み：ナレーションに、video/readings.yaml（と台本の readings:）で読みに直らない英語が残っていないか
    #    残っていると合成音声が1文字ずつつづりを読む（「Band」→「ビー、エー、エヌ、ディー」）。patterns/outputs/video.md の 16
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from video import speakable
        unread = {}
        for i, s in enumerate(scenes):
            spoken = speakable(str(s.get("say", "")), {"readings": doc.get("readings")})
            for w in re.findall(r"[A-Za-z][A-Za-z0-9_\-]*", spoken):
                if re.fullmatch(r"[A-D]", w):       # 選択肢の A〜D は「エー」と読める
                    continue
                unread.setdefault(w, i + 1)
        if unread:
            words = "、".join(f"{w}（場面{n}）" for w, n in list(unread.items())[:12])
            stop.append(f"ナレーションに読みの無い英語があります。video/readings.yaml か台本の readings: に日本語の読みを足す：{words}")
    except Exception as e:  # video.py が読めない環境でも点検は続ける
        mark.append(f"英語の読みの点検ができませんでした：{e}")

    # 8. 作例の数字に計算の根拠（credits）があるか
    cta = next((s for s in scenes if s.get("kind") == "cta"), None)
    creds = "\n".join(map(str, (cta or {}).get("credits", []) or []))
    if re.search(r"作例|例として置いた", creds) is None and re.search(r"たとえば.*\d", text_all):
        mark.append("作例の数字がありますが、締めの credits に「作例」「例として置いた値」と計算の根拠が書かれていません")

    return stop, mark


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        targets = [ROOT / a for a in args]
    elif "--changed" in sys.argv:
        targets = changed()
    else:
        targets = scripts_to_check()
    lines, n_stop, n_mark = ["# 台本の点検結果", ""], 0, 0
    if not targets:
        lines.append("点検する台本はありませんでした。")
    for p in targets:
        stop, mark = check(p)
        n_stop += len(stop)
        n_mark += len(mark)
        state = "止める" if stop else ("印あり" if mark else "問題なし")
        lines += [f"## {p.relative_to(ROOT).as_posix()}（{state}）", ""]
        lines += [f"- **止める**：{x}" for x in stop] + [f"- 印：{x}" for x in mark] + [""]
    lines.insert(2, f"台本 {len(targets)} 本、止める {n_stop} 件、印 {n_mark} 件\n")
    report = "\n".join(lines)
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(report + "\n")
    sys.exit(1 if n_stop else 0)


if __name__ == "__main__":
    main()
