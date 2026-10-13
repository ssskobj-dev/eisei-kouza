#!/usr/bin/env python3
"""記事の機械的な点検。公開前に、誤りになりやすい箇所を止める、または印を付ける。

使い方：
  python scripts/verify.py                 全部の記事を点検する
  python scripts/verify.py --changed       main と比べて、変わった記事だけを点検する
  python scripts/verify.py --links         出典のアドレスが開けるかも調べる（時間がかかる）
  python scripts/verify.py casebook/a.qmd  指定した記事だけを点検する

結果は2種類。
  止める  ：直すまで公開しない誤り。1つでもあれば、終了コード1で終わる
  印      ：人が見て判断する箇所。公開は止めない

点検できるのは形だけ。出典の中身と本文が合っているかは、人と、別の確認の手順で確かめる。
"""
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATED = {"index.qmd", "sentinel.qmd"}
# 数字と単位。出典の番号が近くにないと、印を付ける
NUMBER = re.compile(r"\d[\d,.]*\s*(?:円|万円|億円|兆円|ドル|%|％|件|筆|ha|ヘクタール|km|m|cm|mm|日|か月|年度|倍|割|機|か所|箇所|社|人)")
CITE = re.compile(r"\\?\[(\d+)\\?\]")


def articles():
    out = []
    for pattern in ("casebook/*.qmd", "landscape/*/*.qmd", "learn/*/*.qmd", "note/*/article.md"):
        for p in sorted(ROOT.glob(pattern)):
            if p.name in GENERATED or p.name.startswith("course-") or "/quiz/" in p.as_posix():
                continue
            out.append(p)
    return out


def changed_files():
    base = os.environ.get("VERIFY_BASE", "origin/main")
    res = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD"], cwd=ROOT, capture_output=True, text=True)
    names = {ROOT / n for n in res.stdout.split()}
    return [p for p in articles() if p in names]


def split_sections(text):
    """本文を「## 見出し」ごとに分ける。冒頭の設定（---で囲まれた部分）は除く。"""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        text = text[end + 4:] if end != -1 else text
    sections, name, buf = {}, "", []
    for line in text.splitlines():
        if line.startswith("## "):
            sections[name] = "\n".join(buf)
            name, buf = line[3:].split("{")[0].strip(), []
        else:
            buf.append(line)
    sections[name] = "\n".join(buf)
    return sections


def check(path, links=False):
    stop, mark = [], []
    sections = split_sections(path.read_text(encoding="utf-8"))
    src_text = sections.get("出典")
    body = "\n".join(v for k, v in sections.items() if k not in ("出典", "要確認"))
    is_note = path.name == "article.md"

    # --- 出典 ---
    sources = {}
    summary_note = is_note and not re.match(r"\d{4}-\d{2}-\d{2}-", path.parent.name)
    if src_text is None and summary_note:
        mark.append("サイトの記事の要約です。出典はサイトの記事の側で点検します")
        sources = None
    elif src_text is None:
        stop.append("「出典」の節がありません")
    else:
        for line in src_text.splitlines():
            m = re.match(r"\s*(\d+)\.\s+(.*)", line)
            if m:
                sources[int(m.group(1))] = m.group(2)
        if not sources:
            stop.append("「出典」に、番号付きの資料が1つもありません")
        for n, s in sources.items():
            if not re.search(r"https?://", s) and not re.search(r"出典\d", s):  # 「出典1の目次」のような参照は可
                stop.append(f"出典{n}にアドレスがありません")
    if sources is None:
        return stop, mark
    cited = {int(n) for n in CITE.findall(body)}
    for n in sorted(cited - set(sources)):
        stop.append(f"本文に [{n}] がありますが、出典に{n}番がありません")
    for n in sorted(set(sources) - cited):
        mark.append(f"出典{n}は、本文のどこからも引かれていません")

    # --- 要確認 ---
    n_flag = body.count("【要確認】")
    if n_flag and "要確認" not in sections:
        stop.append("本文に【要確認】がありますが、理由を書く「要確認」の節がありません")
    if "要確認" in sections:
        items = [l for l in sections["要確認"].splitlines() if l.lstrip().startswith("- ")]
        mark.append(f"要確認が{len(items)}件あります（本文中の印は{n_flag}か所）")

    # --- 書きかけ ---
    if not is_note:
        for word in ("（リンクを入れる）", "TODO", "（ここに"):
            if word in body:
                stop.append(f"書きかけの印「{word}」が残っています")
    if re.search(r"\[\^\d+\]", body):
        stop.append("脚注の記法（[^1]）が使われています。\\[1\\] の形にしてください")

    # --- 出典の番号が近くにない数字 ---
    prev = ""
    for para in re.split(r"\n\s*\n", body):
        before, prev = prev, para
        if para.lstrip().startswith(("![", "|", ":::", "<", "```")):
            continue
        # 箇条書きは、直前の文（「資料には次のように書かれています[1]」など）の番号も見る
        near = para + ("\n" + before if para.lstrip().startswith(("-", "1.")) else "")
        if NUMBER.search(para) and not CITE.search(near) and "仮定：" not in para and "【要確認】" not in para:
            first = NUMBER.search(para)
            snippet = para.strip().replace("\n", " ")
            start = max(0, snippet.find(first.group(0)) - 25)
            mark.append(f"出典の番号がない数字：「…{snippet[start:start + 60]}…」")

    # --- 出典のアドレスが開けるか ---
    if links:
        for n, s in sources.items():
            for url in re.findall(r"https?://[^\s<>）」]+", s):
                status = fetch(url)
                if status != "ok":
                    mark.append(f"出典{n}のアドレスが開けませんでした（{status}）：{url}")
    return stop, mark


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (link check; Satellite to Decision)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            return "ok" if res.status < 400 else str(res.status)
    except Exception as e:  # サイト側が機械からの接続を断ることも多いので、止めずに印にする
        return getattr(e, "code", None) and str(e.code) or type(e).__name__


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    links = "--links" in sys.argv
    if args:
        targets = [ROOT / a for a in args]
    elif "--changed" in sys.argv:
        targets = changed_files()
    else:
        targets = articles()
    lines, n_stop, n_mark = ["# 記事の点検結果", ""], 0, 0
    if not targets:
        lines.append("点検する記事はありませんでした。")
    for p in targets:
        stop, mark = check(p, links)
        n_stop += len(stop)
        n_mark += len(mark)
        state = "止める" if stop else ("印あり" if mark else "問題なし")
        lines += [f"## {p.relative_to(ROOT).as_posix()}（{state}）", ""]
        lines += [f"- **止める**：{x}" for x in stop] + [f"- 印：{x}" for x in mark] + [""]
    lines.insert(2, f"記事 {len(targets)} 本、止める {n_stop} 件、印 {n_mark} 件\n")
    report = "\n".join(lines)
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(report + "\n")
    sys.exit(1 if n_stop else 0)


if __name__ == "__main__":
    main()
