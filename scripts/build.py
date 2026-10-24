#!/usr/bin/env python3
"""章立てと講座の定義から、点検・メニュー生成・1冊へのまとめを行う。

使い方:
  python scripts/build.py check            章立ての書き間違いを点検する
  python scripts/build.py todo             まだ書かれていない章を一覧する
  python scripts/build.py nav              メニューと、自動で作るページ（各シリーズの入口、講座、テーマ）を作る
  python scripts/build.py course <講座id>  講座を1つの文書にまとめる（研修テキスト用）
  python scripts/build.py reports [本数]   次に書く市場レポート（テーマと切り口）を一覧する
  python scripts/build.py usecases [本数]  次に書くユースケースの記事を一覧する
"""
import math
import re
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TYPES = {p.stem for p in (ROOT / "patterns/chapter_types").glob("*.md")}
OUTPUTS = {p.stem for p in (ROOT / "patterns/outputs").glob("*.md")}


def load(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def load_parts():
    """全部品を id で引ける辞書にする。defaults を各部品に補う。"""
    parts = {}
    for f in sorted((ROOT / "syllabus").glob("*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        defaults = doc.get("defaults", {})
        for p in doc.get("parts", []):
            merged = {**defaults, **p, "domain": f.stem}
            if merged["id"] in parts:
                raise SystemExit(f"id が重複しています: {merged['id']}")
            parts[merged["id"]] = merged
    return parts


def load_courses():
    return [yaml.safe_load(f.read_text(encoding="utf-8"))
            for f in sorted((ROOT / "courses").glob("*.yaml"))]


def chapter_path(part):
    return ROOT / "learn" / part["domain"] / f"{part['id']}.qmd"


def check():
    parts = load_parts()
    audiences = load("patterns/audiences.yaml")
    depths = load("patterns/depths.yaml")
    strengths = load("patterns/strengths.yaml")
    tradeoffs = load("patterns/tradeoffs.yaml")
    errors = []

    def need(pid, field, value, allowed):
        if value not in allowed:
            errors.append(f"{pid}: {field} の '{value}' は patterns にありません")

    for pid, p in parts.items():
        need(pid, "type", p.get("type"), TYPES)
        need(pid, "audience", p.get("audience"), audiences)
        need(pid, "depth", p.get("depth"), depths)
        for s in p.get("strengths", []):
            need(pid, "strengths", s, strengths)
        for t in p.get("tradeoffs", []):
            need(pid, "tradeoffs", t, tradeoffs)
        for o in p.get("outputs", []):
            need(pid, "outputs", o, OUTPUTS)
        if p.get("status") not in ("todo", "done", "hold"):
            errors.append(f"{pid}: status は todo、done、hold のどれかにしてください（hold＝順番待ち。作らない）")
        if p.get("status") == "done" and not chapter_path(p).exists():
            errors.append(f"{pid}: status が done ですが原稿がありません")

    for s in strengths.values():
        for t in s.get("tradeoffs", []):
            if t not in tradeoffs:
                errors.append(f"strengths.yaml: 落とし所 '{t}' がありません")

    for c in load_courses():
        ov = c.get("override", {})
        if "audience" in ov:
            need(c["id"], "override.audience", ov["audience"], audiences)
        if "depth" in ov:
            need(c["id"], "override.depth", ov["depth"], depths)
        for sec in c["sections"]:
            for pid in sec["parts"]:
                if pid not in parts:
                    errors.append(f"講座 {c['id']}: 部品 '{pid}' が章立てにありません")

    angles = load("patterns/report_angles.yaml")
    seen = set()
    for topic in load_topics():
        if not topic.get("name"):
            errors.append("landscape/topics.yaml: name のないテーマがあります")
        tid = topic.get("id")
        if tid:
            if not re.fullmatch(r"[a-z0-9-]+", tid):
                errors.append(f"landscape/topics.yaml: id '{tid}' は英小文字、数字、ハイフンだけにしてください")
            if tid in seen:
                errors.append(f"landscape/topics.yaml: id '{tid}' が重複しています")
            seen.add(tid)
        for key in topic.get("angles") or []:
            if key not in angles:
                errors.append(f"landscape/topics.yaml: 切り口 '{key}' は patterns/report_angles.yaml にありません")

    theme_list = (load("data/themes.yaml") or {}).get("themes", [])
    theme_names = {th["name"] for th in theme_list}
    topic_ids = {x.get("id") for x in load_topics()}
    course_ids = {c["id"] for c in load_courses()}
    for th in theme_list:
        for tid in th.get("landscape", []):
            if tid not in topic_ids:
                errors.append(f"data/themes.yaml: 市場レポートのテーマ '{tid}' が landscape/topics.yaml にありません")
        for cid in th.get("courses", []):
            if cid not in course_ids:
                errors.append(f"data/themes.yaml: 講座 '{cid}' が courses/ にありません")
    for u in load_usecases():
        if u.get("theme") and u["theme"] not in theme_names:
            errors.append(f"data/usecases.yaml: テーマ '{u['theme']}' が data/themes.yaml にありません（{u.get('name')}）")

    slugs = set()
    for u in load_usecases():
        if not u.get("name"):
            errors.append("data/usecases.yaml: name のない行があります")
        slug = u.get("slug")
        if slug:
            if not re.fullmatch(r"[a-z0-9-]+", slug):
                errors.append(f"data/usecases.yaml: slug '{slug}' は英小文字、数字、ハイフンだけにしてください")
            if slug in slugs:
                errors.append(f"data/usecases.yaml: slug '{slug}' が重複しています")
            slugs.add(slug)

    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print(f"問題ありません（部品 {len(parts)} 個、講座 {len(load_courses())} 個）")


def todo():
    for pid, p in load_parts().items():
        if p["status"] == "todo":
            print(f"{pid}\t{p['type']}\t{p['audience']}\t{p['depth']}\t{p['title']}")


def front_matter(path):
    """記事の冒頭の設定（題名など）を読む。"""
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return yaml.safe_load(text[3:end]) or {}
    return {}


def full_title(path):
    fm = front_matter(path)
    return fm.get("title", path.stem) + (f"：{fm['subtitle']}" if fm.get("subtitle") else "")


SERIES_DESC = {
    "learn/index.qmd": "衛星データの解析と活用を学ぶプログラム。光学とSARの違い、Sentinelの無料データ、植生指数、変化検出、地盤変位、浸水、費用の考え方、調達の実務。講座にはケース問題付き。",
    "landscape/index.qmd": "衛星データの市場レポート。市場規模の推計と出どころ、主なプレイヤー、海外の活用事例、インフラ監視・農業・防災など分野ごとの市場動向を、コンサルタントと発注する側の目で整理します。",
    "casebook/index.qmd": "衛星データの活用事例。遊休農地の調査、地盤変位・地盤沈下の監視、災害の被害把握、インフラ管理・モニタリング、海洋、森林など。実証か本格運用か、限界、無料の衛星でどこまでできるか、費用の概算まで。",
    "news/index.qmd": "衛星データのニュースと時事解説。宇宙機関や省庁の発表、制度や調達の動きを、発注する側の目で読みます。",
}


def write_page(rel, title, subtitle, body, extra=""):
    """自動で作るページを書き出す。extra には、一覧の設定や、古いアドレスからの転送を書く。"""
    if "paywall:" not in extra:
        extra = "paywall: false\n" + extra   # 自動で作るページは、指定がなければ全部を見せる
    if "description:" not in extra and rel in SERIES_DESC:
        extra += f'description: "{SERIES_DESC[rel]}"\n'   # 入口ページの説明文（検索結果に出る）
    head = f'---\ntitle: "{title}"\nsubtitle: "{subtitle}"\nformat: html\n{extra}---\n\n'
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(head + body.rstrip() + "\n", encoding="utf-8")


LISTING = """paywall: false
listing:
  contents: "{contents}"
  type: default
  sort: "date desc"
  categories: false
  fields: [date, title, subtitle, description]
  date-format: "YYYY年M月D日"
  page-size: 30
  filter-ui: false
"""


NEWS_DIR = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")


def news_pages():
    """note/<日付>-<話題>/article.md から、サイトの時事解説のページ（news/<同じ名前>.qmd）を作る。
    note用の下書きを、そのままサイトにも載せるための変換。要確認の節は編集用のメモなので載せない。"""
    made = []
    out_dir = ROOT / "news"
    out_dir.mkdir(exist_ok=True)
    for old in out_dir.glob("*.qmd"):
        old.unlink()
    for folder in sorted((ROOT / "note").iterdir()):
        m = NEWS_DIR.match(folder.name)
        src = folder / "article.md"
        if not (m and src.exists()):
            continue
        lines = src.read_text(encoding="utf-8").splitlines()
        title = next((l[2:].strip() for l in lines if l.startswith("# ")), folder.name)
        body, skip = [], False
        for l in lines:
            if l.startswith("# ") or l.startswith("（note用の下書き") or "（リンクを入れる）" in l:
                continue
            if l.startswith("## "):
                skip = l[3:].strip().startswith("要確認")
            if skip:
                continue
            fig = re.fullmatch(r"（ここに (fig-\d+)\.png）", l.strip())
            if fig:
                name = fig.group(1)
                ext = "svg" if (folder / f"{name}.svg").exists() else "png"
                if (folder / f"{name}.{ext}").exists():
                    body.append(f"![](../note/{folder.name}/{name}.{ext}){{fig-alt=\"図\"}}")
                continue
            body.append(re.sub(r"(?<![<(\[])(https?://[^\s<>）」]+)", r"<\1>", l))
        text = "\n".join(body).strip()
        first = next((l for l in body if l.strip() and not l.startswith(("#", "!", "-", "（"))), "")
        desc = re.sub(r"\[\d+\]|\*\*", "", first).replace('"', "”")[:110]
        thumb = f"../note/{folder.name}/thumbnail.png"
        extra = f'date: {m.group(1)}\ndescription: "{desc}"\ncategories: [時事解説]\n'
        if (folder / "thumbnail.png").exists():
            extra += f'image: "{thumb}"\n'
        head = f'---\ntitle: "{title}"\nformat: html\n{extra}---\n\n'
        (out_dir / f"{folder.name}.qmd").write_text(head + text + "\n", encoding="utf-8")
        made.append(folder.name)
    return made


def sentinel_page(series, cases_done):
    """Sentinelで見られるユースケースの一覧と、解析手法の早見表（learn/sentinel.qmd）を作る。"""
    doc = load("data/sentinel_methods.yaml")
    rows = {u["no"]: u for u in load_usecases()}
    done = {u["no"]: u["slug"] for u in cases_done}
    b = ["無償で使える欧州の衛星 Sentinel を例に、ユースケースごとに「どの衛星の、どの解析手法を使うか」をまとめます。"
         "手法の数は多くありません。同じ手法が、分野をまたいで使われています。", "",
         "## Sentinelの4つの衛星", "",
         "| 衛星 | 種類 | 見えるもの | 撮り方 |", "|---|---|---|---|"]
    b += [f"| {x['name']} | {x['kind']} | {x['sees']} | {x['spec']} |" for x in doc["satellites"]]
    b += ["", ': {tbl-colwidths="[15,17,30,38]"}']
    b += ["", "## ユースケースと解析手法の対応", "",
          "| 解析手法 | 使う衛星 | 答えられる問い | ユースケースの例 |", "|---|---|---|---|"]
    b += [f"| [{m['name']}](#{m['id']}) | {m['satellite']} | {m['answers']} | {m['examples']} |" for m in doc["methods"]]
    total = 0
    for m in doc["methods"]:
        b += ["", f"## {m['name']} {{#{m['id']}}}", "", f"**使う衛星**：{m['satellite']}", "",
              f"**答えられる問い**：{m['answers']}", ""]
        if m.get("steps"):
            b += ["**解析の流れ**", ""] + [f"{i}. {x}" for i, x in enumerate(m["steps"], 1)] + [""]
        if m.get("weak"):
            b += ["**苦手なこと**", ""] + [f"- {x}" for x in m["weak"]] + [""]
        if m.get("note"):
            b += [m["note"], ""]
        b += ["**この手法を使うユースケース**", "", "| ユースケース | 使うデータ | 段階 | 地域 |", "|---|---|---|---|"]
        for no in m["cases"]:
            u = rows[no]
            name = f"[{u['name']}](../casebook/{done[no]}.qmd)" if no in done else u["name"]
            region = {"両方": "国内・海外"}.get(u["region"], u["region"])
            b.append(f"| {name} | {u['data']} | {u['stage']} | {region} |")
            total += 1
        b += ["", ': {tbl-colwidths="[36,40,10,14]"}']
    b += ["", "## 出典", ""] + [f"{i}. {x}" for i, x in enumerate(doc["sources"], 1)]
    b += ["", "各ユースケースの出典は、[" + series["casebook"]["short"] + "](../casebook/index.qmd)の個別の記事に載せています。", "",
          "## 要確認", "",
          "- 番号のない「解析の流れ」と「苦手なこと」は、一般的な手順と、各ユースケースの下調べをもとにまとめたものです。個別の記事を公開するときに、出典と照らし合わせます",
          "- ユースケースの一覧は下調べの段階のものを含みます。リンクのあるものが、記事として公開済みです",
          "- 衛星の機数や撮影の間隔は、運用の状況で変わります"]
    write_page("learn/sentinel.qmd", "Sentinelで見られるユースケースと解析手法",
               "ユースケース別に、使う衛星と解析の流れを早見表で", "\n".join(b),
               "toc-depth: 2\npaywall: true\npaywall-sections: 1\n")
    return total, doc


EN_HEAD = 'lang: en\ntoc-title: On this page\n'
EN_STAGE = {"商用": "Commercial", "実証": "Pilot", "研究": "Research"}
EN_REGION = {"国内": "Japan", "海外": "Overseas", "両方": "Japan and overseas"}
EN_LISTING = """listing:
  contents:
{contents}
  type: default
  sort: "date desc"
  fields: [date, title, subtitle]
  date-format: "D MMM YYYY"
  page-size: 30
"""


def english_pages(series, cases_done):
    """英語版の固定ページのうち、自動で作るもの（en/ の各シリーズの入口と、Sentinelの早見表）を作る。
    記事そのものは日本語のまま。英語の文は data/sentinel_methods_en.yaml と、この関数の中にある。"""
    ja = load("data/sentinel_methods.yaml")
    en = load("data/sentinel_methods_en.yaml")
    rows = {u["no"]: u for u in load_usecases()}
    done = {u["no"]: u["slug"] for u in cases_done}
    methods = [dict(en["methods"][m["id"]], id=m["id"], cases=m["cases"]) for m in ja["methods"]]

    b = ["Using the free European Sentinel satellites as the example, this page shows which satellite and which "
         "analysis method each use case relies on. There are only a handful of methods, and the same ones are used across sectors.", "",
         "## The four Sentinel satellites", "",
         "| Satellite | Type | What it sees | How it observes |", "|---|---|---|---|"]
    b += [f"| {x['name']} | {x['kind']} | {x['sees']} | {x['spec']} |" for x in en["satellites"]]
    b += ["", ': {tbl-colwidths="[15,17,30,38]"}', "", "## Use cases and methods at a glance", "",
          "| Method | Satellite | Question it answers | Example use cases |", "|---|---|---|---|"]
    b += [f"| [{m['name']}](#{m['id']}) | {m['satellite']} | {m['answers']} | {m['examples']} |" for m in methods]
    total = 0
    for m in methods:
        b += ["", f"## {m['name']} {{#{m['id']}}}", "", f"**Satellite**: {m['satellite']}", "",
              f"**Question it answers**: {m['answers']}", ""]
        if m.get("steps"):
            b += ["**How the analysis works**", ""] + [f"{i}. {x}" for i, x in enumerate(m["steps"], 1)] + [""]
        if m.get("weak"):
            b += ["**Limitations**", ""] + [f"- {x}" for x in m["weak"]] + [""]
        if m.get("note"):
            b += [m["note"], ""]
        b += ["**Use cases that rely on this method**", "", "| Use case | Data used | Stage | Region |", "|---|---|---|---|"]
        for no in m["cases"]:
            name, data = en["cases"][no]
            if no in done:
                name = f"[{name}](../../casebook/{done[no]}.qmd) (in Japanese)"
            u = rows[no]
            b.append(f"| {name} | {data} | {EN_STAGE.get(u['stage'], u['stage'])} | {EN_REGION.get(u['region'], u['region'])} |")
            total += 1
        b += ["", ': {tbl-colwidths="[36,40,10,14]"}']
    b += ["", "## Sources", ""] + [f"{i}. {x}" for i, x in enumerate(en["sources"], 1)]
    b += ["", "## To be verified", "",
          "- Steps and limitations without a source number are summaries based on common practice and on our background research for each use case. They will be checked against the sources when each article is published",
          "- The list includes use cases that are still at the research-note stage. Linked items have a published article (in Japanese)",
          "- The number of satellites in operation and the revisit interval change over time"]
    write_page("en/learn/sentinel.qmd", "Use Cases and Analysis Methods with Sentinel",
               "Which satellite and which method, by use case", "\n".join(b),
               EN_HEAD + "toc-depth: 2\npaywall: true\npaywall-sections: 1\nfilters:\n  - ../../design/paywall.lua\n")

    method_rows = "\n".join(f"| [{m['name']}](sentinel.qmd#{m['id']}) | {m['satellite']} | {m['examples']} |" for m in methods)
    note = "Articles in this series are written in Japanese. The list below links to the Japanese pages."
    write_page("en/learn/index.qmd", series["learn"]["brand"], series["learn"]["en"],
               "Learn satellite data analysis by use case. Start from what you want to know, such as flooding, farmland, "
               "ground motion, forests or water quality, then follow the satellite, the analysis steps and the limitations.\n\n"
               "## Learn by use case\n\n"
               f"Using the free European Sentinel satellites as the example, {total} use cases are grouped by analysis method.\n\n"
               "| Method | Satellite | Example use cases |\n|---|---|---|\n" + method_rows + "\n\n"
               "[Open the full list of use cases and methods](sentinel.qmd)\n\n"
               "## Courses\n\nStructured courses with figures and case questions are available in Japanese.\n\n"
               "- [Courses (in Japanese)](../../learn/index.qmd)", EN_HEAD)
    for key, globs, lead in (
        ("landscape", ['"../../landscape/*/*.qmd"'],
         "Market guides by sector. Each sector is covered from eight angles, including global and Japanese market size, "
         "case studies, key players and barriers to adoption. Market figures are shown with their source, scope and year."),
        ("casebook", ['"../../casebook/*.qmd"', '"!../../casebook/index.qmd"'],
         "One article per use case, drawn from research and from announcements by companies and public bodies. "
         "Every article follows the same order: the case, limits as of 2026, how it fits into operations, "
         "data that supports decisions, and how to think about cost."),
        ("news", ['"../../news/*.qmd"', '"!../../news/index.qmd"'],
         "Commentary on announcements about satellite data, written from the buyer's side: what changes, and what does not."),
    ):
        contents = "\n".join(f"    - {g}" for g in globs)
        write_page(f"en/{key}/index.qmd", series[key]["brand"] if key != "news" else "News Commentary",
                   series[key]["en"] if key != "news" else "Reading announcements from the buyer's side",
                   lead + "\n\n" + note, EN_HEAD + EN_LISTING.format(contents=contents))
    return total


PAID_TAIL = ("関連する記事", "出典", "要確認")
PAID_MARK = "――――― ここから有料（noteでは、この行の位置に有料ラインを置く。この行は消す） ―――――"


def paid_start(heads, ratio=None):
    """有料にする最初の節の番号を返す。決め方は design/paywall.lua と同じにしておく。"""
    for n, h in enumerate(heads):
        if "{.paid}" in h:
            return max(n, 1)
    if ratio:
        return max(math.ceil(len(heads) * ratio), 1)
    for n, h in enumerate(heads):
        if h.startswith("（仮）"):
            return max(n, 1)
    return max(len(heads) // 2, 1)


def envideos():
    """英語の事例動画の、作る候補を出す。公開済みのユースケース（海外・両方）で、まだ英語動画が無いもの。"""
    cases = [u for u in load_usecases()
             if u.get("slug") and u.get("region") in ("海外", "両方")
             and (ROOT / "casebook" / f"{u['slug']}.qmd").exists()]
    todo = [u for u in cases if not (ROOT / "video" / f"usecase-{u['slug']}-en" / "script.yaml").exists()]
    print(f"公開済みの海外・両方の事例 {len(cases)} 件、英語動画の未作成 {len(todo)} 件")
    for u in todo[:12]:
        print(f"  usecase-{u['slug']}-en　{u['name']}（{u['region']}）")
    if not todo:
        print("  未作成はありません")


def enreports():
    """英語の市場レポート動画（海外向け）の、作る候補を出す。
    report_angles.yaml で en_video: true を付けた切り口 × topics.yaml のテーマで、
    まだ英語動画（video/report-<テーマid>-<切り口>-en/script.yaml）が無いもの。"""
    angles = load("patterns/report_angles.yaml")
    en_angles = [k for k, v in angles.items() if v.get("en_video")]
    queue = []
    for topic in load_topics():
        if not topic.get("id"):
            continue
        for key in topic.get("angles") or en_angles:
            if key not in en_angles:
                continue
            folder = f"report-{topic['id']}-{key}-en"
            if not (ROOT / "video" / folder / "script.yaml").exists():
                queue.append((topic, key))
    print(f"海外向けの切り口 {len(en_angles)} 種、英語の市場レポート動画の未作成 {len(queue)} 本")
    for topic, key in queue[:12]:
        print(f"  report-{topic['id']}-{key}-en　{topic['name']}：{angles[key]['name']}")
    if not queue:
        print("  未作成はありません")


def javideos():
    """日本語の動画の、作る候補を出す。
    講義動画：公開済みの講座の章（learn/<シリーズ>/<id>.qmd）で、video/lecture-<id>/script.yaml が無いもの。
    事例動画：公開済みのユースケース記事（casebook/<slug>.qmd）で、video/usecase-<slug>/script.yaml が無いもの。"""
    chapters = [p for p in sorted((ROOT / "learn").glob("*/*.qmd"))
                if p.parent.name != "quiz" and p.name != "index.qmd" and not p.name.startswith("course-")]
    lec_todo = [p for p in chapters if not (ROOT / "video" / f"lecture-{p.stem}" / "script.yaml").exists()]
    cases = [p for p in sorted((ROOT / "casebook").glob("*.qmd")) if p.name != "index.qmd"]
    case_todo = [p for p in cases if not (ROOT / "video" / f"usecase-{p.stem}" / "script.yaml").exists()]
    print(f"講義動画：公開済みの章 {len(chapters)} 本、未作成 {len(lec_todo)} 本")
    for p in lec_todo[:8]:
        print(f"  lecture-{p.stem}　{full_title(p)}")
    print(f"事例動画：公開済みの記事 {len(cases)} 本、未作成 {len(case_todo)} 本")
    for p in case_todo[:8]:
        print(f"  usecase-{p.stem}　{full_title(p)}")



def cert():
    """資格の分野ごとに、教材の章が公開済みか（learn/<domain>/<id>.qmd があるか）を出す。"""
    parts = load_parts()
    cmap = load("data/cert_map.yaml") or {}
    for key, c in cmap.items():
        print(f"== {c['name']} ==")
        for lv in c.get("levels", []):
            done_n = total = 0
            for d in lv.get("domains", []):
                rows = []
                for pid in d.get("parts", []):
                    p = parts.get(pid)
                    ok = bool(p) and chapter_path(p).exists()
                    rows.append(("○" if ok else ("…" if p and p.get("status") == "hold" else "×")) + pid)
                    total += 1; done_n += ok
                print(f"  {lv['level']} {d['name']}: " + " ".join(rows))
            print(f"  {lv['level']} 公開 {done_n} / {total} 章")


def cert_map_fragment():
    """cert.qmd に差し込む「シラバスと教材の対応」（_cert_map.qmd）を作る。nav から呼ぶ。"""
    parts = load_parts()
    cmap = load("data/cert_map.yaml") or {}
    out = []
    for key, c in cmap.items():
        out += [f"### {c['name']}", ""]
        for lv in c.get("levels", []):
            out += [f"**{lv['level']}**", "", "| 分野 | 教材の章 |", "|---|---|"]
            for d in lv.get("domains", []):
                cells = []
                for pid in d.get("parts", []):
                    p = parts.get(pid)
                    if p and chapter_path(p).exists():
                        rel = chapter_path(p).relative_to(ROOT).as_posix()
                        cells.append(f"[{p['title'].split('：')[0]}]({rel})")
                    elif p:
                        cells.append(f"{p['title'].split('：')[0]}（準備中）")
                out.append(f"| {d['name']} | " + "、".join(cells) + " |")
            out.append("")
    (ROOT / "_cert_map.qmd").write_text("\n".join(out) + "\n", encoding="utf-8")



def noteready():
    """noteに貼れる形（post.md）を作る。編集用のメモ、未記入のリンク、「要確認」の節を外し、
    図の位置を「<<IMG: ファイル名>>」にして、どこで画像を挿入するかが分かるようにする。
    対象：時事解説（note/<日付>-<話題>/article.md）と、記事の note 版（full.md があるフォルダ）。"""
    made = []
    for folder in sorted((ROOT / "note").iterdir()):
        if not folder.is_dir():
            continue
        src = folder / "full.md" if (folder / "full.md").exists() else folder / "article.md"
        if not src.exists():
            continue
        lines = src.read_text(encoding="utf-8").splitlines()
        title = next((l[2:].strip() for l in lines if l.startswith("# ")), folder.name)
        body, skip = [], False
        for l in lines:
            if l.startswith("# ") or l.startswith("（note用の下書き") or l.startswith("（noteに貼る") \
               or "（リンクを入れる）" in l:
                continue
            if l.startswith("## "):
                skip = l[3:].strip().startswith("要確認")
            if skip:
                continue
            fig = re.fullmatch(r"（ここに (fig-\d+)\.png）", l.strip())
            if fig:
                body.append(f"<<IMG: {fig.group(1)}.png>>")
                continue
            fig2 = re.fullmatch(r"（ここに図：([\w.-]+)[ 　]+(.*)）", l.strip())
            if fig2:
                body.append(f"<<IMG: {fig2.group(1)}.png>>")
                continue
            body.append(l)
        text = re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip()
        (folder / "post.md").write_text(f"{title}\n\n{text}\n", encoding="utf-8")
        made.append(folder.name)
    print(f"noteに貼れる形を {len(made)} 本作りました（各フォルダの post.md。1行目が題名）")


def notefull():
    """note に貼る本文（full.md）を作る。シリーズごとに出し方が違う（利用者の方針、2026-10-24）。

    ユースケース集：全文を公開する（有料ラインなし）
    市場レポート  ：前半だけを出し、以下は有料であることとサイトへの誘導を付ける
    講座          ：noteには出さない（サイトだけ）
    """
    variables = load("_variables.yml")

    def var(m):
        v = variables
        for key in m.group(1).split("."):
            v = v[key]
        return str(v)

    made = []
    # (記事, noteのフォルダ名, 出し方)  mode: "full"＝全文、"teaser"＝前半＋サイトへ誘導
    targets = [(p, f"usecase-{p.stem}", "full") for p in sorted((ROOT / "casebook").glob("*.qmd")) if p.name != "index.qmd"]
    targets += [(p, f"report-{p.parent.name}-{p.stem}", "teaser") for p in sorted((ROOT / "landscape").glob("*/*.qmd"))]
    # 講座の章は note に出さない
    for path, folder, mode in targets:
        ratio = None
        fm = front_matter(path)
        text = path.read_text(encoding="utf-8")
        body = text[text.find("\n---", 3) + 4:]
        parts = re.split(r"(?m)^## ", body)
        intro, sections = parts[0], [x for x in parts[1:]]
        content = [x for x in sections if not x.split("\n", 1)[0].strip().startswith(PAID_TAIL)]
        tail = [x for x in sections if x.split("\n", 1)[0].strip().startswith(("関連する記事", "出典"))]
        site = variables["site"]
        if mode == "full":
            out = [f"# {full_title(path)}", "",
                   "（noteに貼る全文。全部を公開する。図は、サイトの記事の図を使う）", ""]
            if intro.strip():
                out.append(intro.strip() + "\n")
            for sec in content + tail:
                out.append("## " + sec.rstrip() + "\n")
        else:   # teaser：前半だけ出して、続きはサイトへ
            start = paid_start([x.split("\n", 1)[0].strip() for x in content], ratio)
            page = site["url"].rstrip("/") + "/" + path.relative_to(ROOT).with_suffix(".html").as_posix()
            out = [f"# {full_title(path)}", "",
                   "（noteに貼る前半。続きはサイトの有料版。図は、サイトの記事の図を使う）", ""]
            if intro.strip():
                out.append(intro.strip() + "\n")
            for sec in content[:start]:
                out.append("## " + sec.rstrip() + "\n")
            out += ["---", "",
                    "## ここから先は有料です", "",
                    f"この記事の続き（{'、'.join(x.split(chr(10), 1)[0].strip() for x in content[start:]) or '後半'}）は、"
                    f"{site['name']} の有料版でお読みいただけます。",
                    "",
                    f"▶ 続きを読む：{page}", "",
                    f"月額{variables['paid']['price']}円で、市場レポートの全文、ユースケース集、学習プログラム、"
                    "テーマ別の絞り込みがすべて読めます。", ""]
            for sec in tail:
                out.append("## " + sec.rstrip() + "\n")
        doc = "\n".join(out)
        doc = re.sub(r"\{\{<\s*var\s+([\w.]+)\s*>\}\}", var, doc)
        doc = re.sub(r"!\[([^\]]*)\]\(([^)]*)\)(\{[^}]*\})?", lambda m: f"（ここに図：{Path(m.group(2)).stem}　{m.group(1)}）", doc)
        doc = re.sub(r"\\\[(\d+)\\\]", r"[\1]", doc)
        doc = re.sub(r"(?m)^(#+ .*?)\s*\{[^}]*\}\s*$", r"\1", doc)
        doc = re.sub(r"<(https?://[^>]+)>", r"\1", doc)
        doc = re.sub(r"\]\(\.\./[^)]*\)", "]（サイト内のページ）", doc)
        dest = ROOT / "note" / folder
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "full.md").write_text(doc.rstrip() + "\n", encoding="utf-8")
        made.append(folder)
    print(f"note用の全文を {len(made)} 本作りました：" + "、".join(made))


THEME_STUB = """::: {.s2d-paywall}
**「テーマから探す」は、有料版の機能です。**

分野ごとに、市場レポート、ユースケース、学習プログラムの記事をまとめて見られます。

<p class="s2d-paywall-cta"><a class="s2d-button" data-s2d-register="paywall" href="/register.html">サイトに有料登録する</a></p>
:::
"""

def nav():
    """メニュー（_sidebar.yml）と、自動で作るページ（各シリーズの入口、講座、テーマ）を作る。"""
    parts = load_parts()
    series = load("_variables.yml")["series"]
    angles = load("patterns/report_angles.yaml")
    topics = [x for x in load_topics() if x.get("id")]
    cases = [u for u in load_usecases()
             if u.get("slug") and (ROOT / "casebook" / f"{u['slug']}.qmd").exists()]
    sidebars = []

    # ---- 学習プログラム：講座ごとのページと、入口のページ ----
    course_lines = []
    public_courses = [c for c in load_courses() if c.get("public")]
    for c in public_courses:
        page, contents = [], [f"learn/course-{c['id']}.qmd"]
        done = total = 0
        for sec in c["sections"]:
            page.append(f"\n## {sec['name']}\n")
            if sec.get("lead"):
                page.append(sec["lead"] + "\n")
            items = []
            for pid in sec["parts"]:
                part = parts[pid]
                path = chapter_path(part)
                total += 1
                if path.exists():
                    done += 1
                    rel = path.relative_to(ROOT / "learn").as_posix()
                    items.append("learn/" + rel)
                    line = f"- [{part['title']}]({rel})"
                    if (ROOT / "learn" / "quiz" / f"{pid}.qmd").exists():
                        line += f"　[ケース問題](quiz/{pid}.qmd)"
                    page.append(line)
                else:
                    page.append(f"- {part['title']}（準備中）")
            if items:
                contents.append({"section": sec["name"], "contents": items})
        main, _, sub = c["title"].partition("（")
        write_page(f"learn/course-{c['id']}.qmd", main, sub.rstrip("）"), "\n".join(page),
                   f'aliases:\n  - /course-{c["id"]}.html\n')
        sidebars.append({"id": c["id"], "title": c["title"], "contents": contents})
        course_lines.append(f"- [{c['title']}](course-{c['id']}.qmd)　公開 {done} 章 / 全 {total} 章")
    n_sentinel, sdoc = sentinel_page(series, cases)
    method_rows = "\n".join(f"| [{m['name']}](sentinel.qmd#{m['id']}) | {m['satellite']} | {m['examples']} |"
                            for m in sdoc["methods"])
    write_page("learn/index.qmd", series["learn"]["ja"], series["learn"]["brand"] + "　" + series["learn"].get("lead", ""),
               "衛星データの解析を、ユースケース別に学べます。浸水、農地、地盤の動き、森林、水質など、"
               "知りたいことから入り、使う衛星、解析の流れ、苦手なことの順で身につけます。\n\n"
               "## ユースケース別に学ぶ\n\n"
               f"無償で使える欧州の衛星 Sentinel を例に、{n_sentinel}件のユースケースを、解析手法ごとに整理しました。"
               "手法の名前から、解析の流れとユースケースの一覧に進めます。\n\n"
               "| 解析手法 | 使う衛星 | ユースケースの例 |\n|---|---|---|\n" + method_rows + "\n\n"
               "[Sentinelで見られるユースケースと解析手法の一覧を開く](sentinel.qmd)\n\n"
               "## 講座で体系的に学ぶ\n\n"
               "使い道ごとに、欲しい成果、強み、限界、現実的な落とし所の順で学ぶ講座です。章には図とケース問題が付いています。\n\n"
               + "\n".join(course_lines))
    sidebars.append({"id": "learn", "title": series["learn"]["short"],
                     "contents": ["learn/index.qmd", "learn/sentinel.qmd"]})

    # ---- 市場レポート ----
    write_page("landscape/index.qmd", series["landscape"]["ja"], series["landscape"]["brand"] + "　" + series["landscape"].get("lead", ""),
               "衛星データの利活用を、分野ごとに整理しています。1つの分野を、次の8つの切り口で1本ずつ書いています。\n\n"
               + "、".join(a["name"] for a in angles.values()) + "\n\n"
               "市場規模の数字は、出どころ、対象の範囲、年を添えています。調査会社によって推計に幅があるときは、"
               "1つに決めず、幅のまま示しています。各レポートの前半は無料で読めます。後半は有料です。",
               LISTING.format(contents="*/*.qmd") + "aliases:\n  - /reports/index.html\n")
    contents = ["landscape/index.qmd"]
    n_guides = 0
    for topic in topics:
        items = [f"landscape/{topic['id']}/{key}.qmd" for key in angles
                 if (ROOT / "landscape" / topic["id"] / f"{key}.qmd").exists()]
        n_guides += len(items)
        if items:
            contents.append({"section": topic["name"], "contents": items})
    sidebars.append({"id": "landscape", "title": series["landscape"]["short"], "contents": contents})

    # ---- ユースケース集 ----
    write_page("casebook/index.qmd", series["casebook"]["ja"], series["casebook"]["brand"] + "　" + series["casebook"].get("lead", ""),
               "衛星データの使い道を、1つずつ取り上げます。研究事例と、企業や官公庁の発表から拾ったものです。"
               "どの記事も、同じ順番で書いています。\n\n"
               "事例、2026年時点の限界、業務に入れるときの想定、意思決定に使えるデータ、費用の考え方、向き不向き\n\n"
               "費用は、公開されている金額だけを、出どころと条件を添えて書いています。"
               "各レポートの前半（事例と限界まで）は無料で読めます。後半は有料です。",
               LISTING.format(contents="*.qmd") + "aliases:\n  - /usecases/index.html\n")
    by_theme = {}
    for u in cases:
        by_theme.setdefault(u.get("theme", "その他"), []).append(f"casebook/{u['slug']}.qmd")
    sidebars.append({"id": "casebook", "title": series["casebook"]["short"],
                     "contents": ["casebook/index.qmd"] + [{"section": k, "contents": v} for k, v in by_theme.items()]})

    # ---- テーマから探す：テーマごとに、3つのシリーズを束ねる ----
    themes = (load("data/themes.yaml") or {}).get("themes", [])
    all_cases = [u for u in load_usecases() if not u.get("skip")]
    index_lines = []
    for th in themes:
        body = [th.get("lead", ""), "", f"## {series['landscape']['short']}", ""]
        rows = []
        for tid in th.get("landscape", []):
            for key in angles:
                path = ROOT / "landscape" / tid / f"{key}.qmd"
                if path.exists():
                    rows.append(f"- [{full_title(path)}](../landscape/{tid}/{key}.qmd)")
        body += rows or ["準備中です。"]
        body += ["", f"## {series['casebook']['short']}", ""]
        mine = [u for u in cases if u.get("theme") == th["name"]]
        planned = len([u for u in all_cases if u.get("theme") == th["name"]])
        body += [f"- [{full_title(ROOT / 'casebook' / (u['slug'] + '.qmd'))}](../casebook/{u['slug']}.qmd)" for u in mine]
        body += ["", f"このテーマのユースケースは全{planned}件です。公開済みは{len(mine)}件で、順に追加しています。"]
        body += ["", f"## {series['learn']['short']}", ""]
        mine_courses = [c for c in public_courses if c["id"] in th.get("courses", [])]
        body += [f"- [{c['title']}](../learn/course-{c['id']}.qmd)" for c in mine_courses] or ["準備中です。"]
        kws = seo_theme_words(th["id"])
        th_title = (f"{SEO_HEAD} " + "・".join(kws[:3]) + f"｜{th['name']}") if kws else th["name"]
        th_desc = (f"{SEO_HEAD}の{th['name']}分野：" + "、".join(f"{SEO_HEAD} {k}" for k in kws[:5])
                   + "。市場レポート、活用事例、学習プログラムをまとめて見られます。") if kws else ""
        write_page(f"themes/{th['id']}.qmd", th_title, f"テーマから探す：{th['name']}", THEME_STUB,
                   extra=(f'description: "{th_desc}"\n' if th_desc else ""))
        index_lines.append(f"- [{th['name']}]({th['id']}.qmd)　ユースケース {len(mine)} / {planned} 件"
                           + ("、市場レポートあり" if rows else "") + ("、講座あり" if mine_courses else ""))
    write_page("themes/index.qmd", "テーマから探す", "分野ごとに、市場レポート、ユースケース、学習プログラムをまとめて見る", THEME_STUB)
    sidebars.append({"id": "themes", "title": "テーマから探す",
                     "contents": ["themes/index.qmd"] + [f"themes/{th['id']}.qmd" for th in themes]})

    # ---- 時事解説：note用の下書きから、サイトのページを作る ----
    news = news_pages()
    write_page("news/index.qmd", series["news"]["ja"], series["news"]["brand"] + "　" + series["news"].get("lead", ""),
               "衛星データに関する発表を取り上げ、発注する側にとっての意味を書きます。"
               "ニュースの要約ではなく、何が変わり、何が変わらないかを整理します。発表元の資料をもとに書いています。",
               LISTING.format(contents="*.qmd"))
    sidebars.append({"id": "news", "title": series["news"]["short"],
                     "contents": ["news/index.qmd"] + [f"news/{n}.qmd" for n in reversed(news)]})

    english_pages(series, cases)

    out = {"website": {"sidebar": sidebars}}
    (ROOT / "_sidebar.yml").write_text(
        "# scripts/build.py nav が作るファイル。手で直さない。\n"
        + yaml.safe_dump(out, allow_unicode=True, sort_keys=False), encoding="utf-8")
    cert_map_fragment()
    print(f"メニューとページを作りました（講座 {len(public_courses)}、テーマ {len(themes)}、"
          f"市場レポート {n_guides} 本、ユースケース {len(cases)} 本、時事解説 {len(news)} 本）")



SEO_HEAD = "衛星データ"


def seo_theme_words(theme_id):
    """data/seo_keywords.yaml から、テーマの検索語（衛星データの後ろに付く語）を返す。"""
    doc = load("data/seo_keywords.yaml") or {}
    return list((doc.get("themes") or {}).get(theme_id) or [])

def load_topics():
    doc = load("landscape/topics.yaml") or {}
    return [x for x in (doc.get("topics") or []) if not x.get("skip")]


def report_queue():
    """まだ書かれていない市場レポートを、書く順に並べる。テーマは表の上から、切り口は定義の順。"""
    angles = load("patterns/report_angles.yaml")
    queue = []
    for topic in load_topics():
        if not topic.get("id"):
            queue.append((topic, None))       # id がまだない。最初に作るときに付ける
            continue
        for key in topic.get("angles") or list(angles):
            if not (ROOT / "landscape" / topic["id"] / f"{key}.qmd").exists():
                queue.append((topic, key))
    return queue


def reports(limit):
    angles = load("patterns/report_angles.yaml")
    queue = report_queue()
    if not queue:
        print("書くテーマが残っていません。landscape/topics.yaml にテーマを足してください")
        return
    shown = 0
    for topic, key in queue:
        if key is None:
            print(f"（id 未設定）\t{topic['name']}\t→ id を付けてから、切り口を上から順に書く")
        else:
            print(f"{topic['id']}\t{key}\t{topic['name']}：{angles[key]['name']}")
        shown += 1
        if shown >= limit:
            break
    print(f"残り {len([q for q in queue if q[1]])} 本（id 未設定のテーマを除く）")


def load_usecases():
    doc = load("data/usecases.yaml") or {}
    return doc.get("usecases") or []


def usecase_queue():
    """まだ記事になっていないユースケースを、表の順に並べる。"""
    return [u for u in load_usecases()
            if not u.get("skip") and not (u.get("slug") and (ROOT / "casebook" / f"{u['slug']}.qmd").exists())]


def usecases(limit):
    queue = usecase_queue()
    if not queue:
        print("書くユースケースが残っていません。data/usecases.yaml に足してください")
        return
    for u in queue[:limit]:
        print(f"{u.get('no', '-')}\t{u['name']}\t{u.get('theme', '')}\t{u.get('stage', '')}\t{u.get('region', '')}")
    print(f"残り {len(queue)} 本")


def strip_front_matter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text


def typ(s):
    """Typstの文字列として安全に埋め込む。"""
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def course(course_id):
    """講座を1冊にまとめる。目次、部の扉、章番号が付く。custom/ は公開されず、git にも入らない。"""
    parts = load_parts()
    c = next((x for x in load_courses() if x["id"] == course_id), None)
    if c is None:
        raise SystemExit(f"講座 '{course_id}' がありません")
    # サイトの設定に頼らず、この1ファイルだけでPDFにできるようにする
    # 題名の末尾の（…向け）は、表紙で副題として小さく出す
    m = re.match(r"^(.*?)（(.+)）$", c["title"])
    main, sub = (m.group(1), m.group(2)) if m else (c["title"], None)
    head = (f"---\ntitle: \"{main}\"\n" + (f"subtitle: \"{sub}\"\n" if sub else "")
            + "kouza-book: true\nlang: ja\n"
            "format:\n  typst:\n    toc: false\n    papersize: a4\n"
            "    mainfont: \"Noto Sans CJK JP\"\n    shift-heading-level-by: 0\n"
            "    template-partials:\n      - ../design/typst-template.typ\n"
            "      - ../design/typst-show.typ\n---\n")
    variables = load("_variables.yml")

    def fill_var(match):
        value = variables
        for key in match.group(1).split("."):
            value = value[key]
        return str(value)

    toc = ["```{=typst}", '#heading(level: 3, outlined: false)[目次]']
    body = []
    missing = []
    for i, sec in enumerate(c["sections"], start=1):
        m = re.match(r"^第\s*\d+\s*部\s*(.*)$", sec["name"])
        part_no = str(i) if m else None
        part_title = m.group(1) if m else sec["name"]
        no = typ(part_no) if part_no else "none"
        toc.append(f"#toc-part({no}, [#{typ(part_title)}])")
        part_at = len(body)   # 部の扉は、章の一覧がそろってから差し込む
        body.append("")
        rows = []
        for j, pid in enumerate(sec["parts"], start=1):
            p = parts[pid]
            num = f"{i}-{j}"
            path = chapter_path(p)
            if not path.exists():
                missing.append(pid)
                toc.append(f"#toc-chapter-pending({typ(num)}, [#{typ(p['title'])}])")
                rows.append((num, p["title"], "none", p.get("must_include", [])[:4]))
                continue
            rows.append((num, p["title"], f"<{pid}>", p.get("must_include", [])[:4]))
            toc.append(f"#toc-chapter({typ(num)}, [#{typ(p['title'])}], <{pid}>)")
            points = p.get("must_include", [])
            if points:
                toc.append("#toc-points((" + "".join(f"[#{typ(x)}], " for x in points) + "))")
            text = strip_front_matter(path.read_text(encoding="utf-8"))
            # 図を、まとめた文書の隣に写して参照する（PDFは隣のフォルダしか読めない）
            text = text.replace("](../../figures/", "](figures/")
            src = ROOT / "figures" / pid
            if src.is_dir():
                shutil.copytree(src, ROOT / "custom" / "figures" / pid, dirs_exist_ok=True)
            text = re.sub(r"\{\{<\s*var\s+([\w.\-]+)\s*>\}\}", fill_var, text)
            # 章の中の見出しを1段下げて、章の題名を見出しにする
            text = "\n".join("#" + l if l.startswith("#") else l for l in text.splitlines())
            # 同じ見出しが章ごとに出てくるので、自動で付く目印を外す
            text = re.sub(r"^(#{2,} .*?)\s*$", r"\1 {.unnumbered .unlisted}", text, flags=re.M)
            # 題名の「：」より後ろは、副題として小さく出す
            head_main, _, head_sub = p["title"].partition("：")
            sub = typ(head_sub) if head_sub else "none"
            body.append(f"\n```{{=typst}}\n#chapter-no.update({typ(num)})\n"
                        f"#chapter-sub.update({sub})\n```\n\n"
                        f"## {head_main} {{#{pid}}}\n\n{text}\n")
        lead = f"[#{typ(sec['lead'])}]" if sec.get("lead") else "none"
        names = "(" + "".join(f"[#{typ(s['name'])}], " for s in c["sections"]) + ")"
        chapters = "(" + "".join(
            f"({typ(n)}, [#{typ(ti)}], {tg}, ({''.join(f'[#{typ(x)}], ' for x in pts)})), "
            for n, ti, tg, pts in rows) + ")"
        body[part_at] = (f"\n```{{=typst}}\n#part-no.update({no})\n"
                         f"#part-page({no}, [#{typ(part_title)}], {lead}, {i - 1}, {names}, {chapters})\n```\n")
    toc.append("```")
    dest = ROOT / "custom"
    dest.mkdir(exist_ok=True)
    (dest / f"{course_id}.qmd").write_text(head + "\n".join(toc) + "\n" + "\n".join(body), encoding="utf-8")
    print(f"custom/{course_id}.qmd を作りました")
    print(f"PDFにする: quarto render custom/{course_id}.qmd --to typst")
    if missing:
        print("まだ原稿がない部品: " + ", ".join(missing))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "check":
        check()
    elif cmd == "todo":
        todo()
    elif cmd == "nav":
        nav()
    elif cmd == "noteready":
        noteready()
    elif cmd == "notefull":
        notefull()
    elif cmd == "envideos":
        envideos()
    elif cmd == "enreports":
        enreports()
    elif cmd == "javideos":
        javideos()
    elif cmd == "cert":
        cert()
    elif cmd == "usecases":
        usecases(int(sys.argv[2]) if len(sys.argv) > 2 else 3)
    elif cmd == "reports":
        reports(int(sys.argv[2]) if len(sys.argv) > 2 else 2)
    elif cmd == "course" and len(sys.argv) > 2:
        course(sys.argv[2])
    else:
        print(__doc__)
