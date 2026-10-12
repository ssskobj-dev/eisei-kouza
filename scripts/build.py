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
        if p.get("status") not in ("todo", "done"):
            errors.append(f"{pid}: status は todo か done にしてください")
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
                errors.append(f"data/themes.yaml: 市場ガイドのテーマ '{tid}' が landscape/topics.yaml にありません")
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


def write_page(rel, title, subtitle, body, extra=""):
    """自動で作るページを書き出す。extra には、一覧の設定や、古いアドレスからの転送を書く。"""
    head = f'---\ntitle: "{title}"\nsubtitle: "{subtitle}"\nformat: html\n{extra}---\n\n'
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(head + body.rstrip() + "\n", encoding="utf-8")


LISTING = """listing:
  contents: "{contents}"
  type: default
  sort: "date desc"
  categories: true
  fields: [date, title, subtitle, description, categories]
  date-format: "YYYY年M月D日"
  page-size: 30
  filter-ui: [title, description]
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
               "toc-depth: 2\n")
    return total, doc


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
    write_page("learn/index.qmd", series["learn"]["brand"], series["learn"]["ja"],
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

    # ---- 市場ガイド ----
    write_page("landscape/index.qmd", series["landscape"]["brand"], series["landscape"]["ja"],
               "衛星データの利活用を、分野ごとに整理しています。1つの分野を、次の8つの切り口で1本ずつ書いています。\n\n"
               + "、".join(a["name"] for a in angles.values()) + "\n\n"
               "市場規模の数字は、出どころ、対象の範囲、年を添えています。調査会社によって推計に幅があるときは、"
               "1つに決めず、幅のまま示しています。右の分類から、分野や切り口で絞り込めます。",
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
    write_page("casebook/index.qmd", series["casebook"]["brand"], series["casebook"]["ja"],
               "衛星データの使い道を、1つずつ取り上げます。研究事例と、企業や官公庁の発表から拾ったものです。"
               "どの記事も、同じ順番で書いています。\n\n"
               "事例、2026年時点の限界、業務に入れるときの想定、意思決定に使えるデータ、費用の考え方、向き不向き\n\n"
               "費用は、公開されている金額だけを、出どころと条件を添えて書いています。"
               "右の分類から、テーマ、段階（研究、実証、商用）、国内と海外で絞り込めます。",
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
        write_page(f"themes/{th['id']}.qmd", th["name"], "テーマから探す", "\n".join(body))
        index_lines.append(f"- [{th['name']}]({th['id']}.qmd)　ユースケース {len(mine)} / {planned} 件"
                           + ("、市場ガイドあり" if rows else "") + ("、講座あり" if mine_courses else ""))
    write_page("themes/index.qmd", "テーマから探す", "分野ごとに、市場ガイド、ユースケース、学習プログラムをまとめて見る",
               "関心のある分野を選ぶと、その分野の記事をシリーズをまたいで一覧できます。\n\n" + "\n".join(index_lines))
    sidebars.append({"id": "themes", "title": "テーマから探す",
                     "contents": ["themes/index.qmd"] + [f"themes/{th['id']}.qmd" for th in themes]})

    # ---- 時事解説：note用の下書きから、サイトのページを作る ----
    news = news_pages()
    write_page("news/index.qmd", series["news"]["brand"], series["news"]["ja"],
               "衛星データに関する発表を取り上げ、発注する側にとっての意味を書きます。"
               "ニュースの要約ではなく、何が変わり、何が変わらないかを整理します。発表元の資料をもとに書いています。",
               LISTING.format(contents="*.qmd"))
    sidebars.append({"id": "news", "title": series["news"]["short"],
                     "contents": ["news/index.qmd"] + [f"news/{n}.qmd" for n in reversed(news)]})

    out = {"website": {"sidebar": sidebars}}
    (ROOT / "_sidebar.yml").write_text(
        "# scripts/build.py nav が作るファイル。手で直さない。\n"
        + yaml.safe_dump(out, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"メニューとページを作りました（講座 {len(public_courses)}、テーマ {len(themes)}、"
          f"市場ガイド {n_guides} 本、ユースケース {len(cases)} 本、時事解説 {len(news)} 本）")


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
    elif cmd == "usecases":
        usecases(int(sys.argv[2]) if len(sys.argv) > 2 else 3)
    elif cmd == "reports":
        reports(int(sys.argv[2]) if len(sys.argv) > 2 else 2)
    elif cmd == "course" and len(sys.argv) > 2:
        course(sys.argv[2])
    else:
        print(__doc__)
