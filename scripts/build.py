#!/usr/bin/env python3
"""章立てと講座の定義から、点検・メニュー生成・1冊へのまとめを行う。

使い方:
  python scripts/build.py check            章立ての書き間違いを点検する
  python scripts/build.py todo             まだ書かれていない章を一覧する
  python scripts/build.py nav              サイトのメニューと講座ページを作る
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
    return ROOT / "chapters" / part["domain"] / f"{part['id']}.qmd"


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
            errors.append("reports/topics.yaml: name のないテーマがあります")
        tid = topic.get("id")
        if tid:
            if not re.fullmatch(r"[a-z0-9-]+", tid):
                errors.append(f"reports/topics.yaml: id '{tid}' は英小文字、数字、ハイフンだけにしてください")
            if tid in seen:
                errors.append(f"reports/topics.yaml: id '{tid}' が重複しています")
            seen.add(tid)
        for key in topic.get("angles") or []:
            if key not in angles:
                errors.append(f"reports/topics.yaml: 切り口 '{key}' は patterns/report_angles.yaml にありません")

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


def nav():
    """公開する講座ごとに、メニュー（_sidebar.yml）と講座ページを作る。"""
    parts = load_parts()
    sidebars = []
    for c in load_courses():
        if not c.get("public"):
            continue
        page = [f"---\ntitle: \"{c['title']}\"\nformat: html\n---\n"]
        contents = [f"course-{c['id']}.qmd"]
        for sec in c["sections"]:
            page.append(f"\n## {sec['name']}\n")
            items = []
            for pid in sec["parts"]:
                p = parts[pid]
                path = chapter_path(p)
                if path.exists():
                    rel = path.relative_to(ROOT).as_posix()
                    items.append(rel)
                    line = f"- [{p['title']}]({rel})"
                    quiz = ROOT / "quiz" / f"{pid}.qmd"
                    if quiz.exists():
                        line += f"　[ケース問題](quiz/{pid}.qmd)"
                    page.append(line)
                else:
                    page.append(f"- {p['title']}（準備中）")
            if items:
                contents.append({"section": sec["name"], "contents": items})
        (ROOT / f"course-{c['id']}.qmd").write_text("\n".join(page) + "\n", encoding="utf-8")
        sidebars.append({"id": c["id"], "title": c["title"], "contents": contents})
    # 市場レポートのメニュー。テーマごとに、書かれた切り口を並べる
    angles = load("patterns/report_angles.yaml")
    contents = ["reports/index.qmd"]
    for topic in load_topics():
        if not topic.get("id"):
            continue
        items = [f"reports/{topic['id']}/{key}.qmd" for key in angles
                 if (ROOT / "reports" / topic["id"] / f"{key}.qmd").exists()]
        if items:
            contents.append({"section": topic["name"], "contents": items})
    sidebars.append({"id": "reports", "title": "市場レポート", "contents": contents})
    # ユースケースのメニュー。テーマごとに、書かれた記事を並べる
    by_theme = {}
    for u in load_usecases():
        if u.get("slug") and (ROOT / "usecases" / f"{u['slug']}.qmd").exists():
            by_theme.setdefault(u.get("theme", "その他"), []).append(f"usecases/{u['slug']}.qmd")
    contents = ["usecases/index.qmd"] + [{"section": k, "contents": v} for k, v in by_theme.items()]
    sidebars.append({"id": "usecases", "title": "ユースケース", "contents": contents})
    out = {"website": {"sidebar": sidebars}}
    (ROOT / "_sidebar.yml").write_text(
        "# scripts/build.py nav が作るファイル。手で直さない。\n"
        + yaml.safe_dump(out, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"メニューを作りました（講座 {len(sidebars)} 個）")


def load_topics():
    doc = load("reports/topics.yaml") or {}
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
            if not (ROOT / "reports" / topic["id"] / f"{key}.qmd").exists():
                queue.append((topic, key))
    return queue


def reports(limit):
    angles = load("patterns/report_angles.yaml")
    queue = report_queue()
    if not queue:
        print("書くテーマが残っていません。reports/topics.yaml にテーマを足してください")
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
            if not u.get("skip") and not (u.get("slug") and (ROOT / "usecases" / f"{u['slug']}.qmd").exists())]


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
