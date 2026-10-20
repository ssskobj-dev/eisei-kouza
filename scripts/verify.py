#!/usr/bin/env python3
"""記事の機械的な点検。公開前に、誤りになりやすい箇所を止める、または印を付ける。

使い方：
  python scripts/verify.py                 全部の記事を点検する
  python scripts/verify.py --changed       main と比べて、変わった記事だけを点検する
  python scripts/verify.py --links         出典のアドレスが開けるかも調べる（時間がかかる）
  python scripts/verify.py casebook/a.qmd  指定した記事だけを点検する

結果は2種類。
  止める  ：直すまで公開しない。1つでもあれば、終了コード1で終わる
  印      ：気づきとして残す。公開は止めない

点検は緩め。止めるのは「読者に見せられない状態」（書きかけ、崩れる記法）と、
「マーケティング効果が見込みにくい内容」（下の4項目のうち1つ以下しか満たさない）だけ。
出典の形の崩れは印にとどめる（公開は止めない）。

マーケティングの4項目（根拠：実用的な内容は共有される＝Berger & Milkman 2012、冒頭で得が分かる、具体的な数字、持ち帰れる行動）
  1. 結論・得が冒頭にある   ：最初の節に「分かること／結論／要点」があるか、冒頭に具体的な数字がある
  2. 具体的な数字がある     ：本文に数字が1つ以上
  3. 持ち帰れる行動がある   ：「示唆／要点／手順／次の一歩」などの節か、番号付きの手順か、3つ以上の箇条書き
  4. 題名が具体的           ：8字以上で、数字か具体的な対象を含む（「〜について」「〜とは」だけの題名は×）
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


def title_of(path, text):
    """題名を取る。qmd は冒頭の title:、note の article.md は1行目の「# 題名」。"""
    m = re.search(r'(?m)^title:\s*["\']?(.+?)["\']?\s*$', text[:2000])
    if m:
        return m.group(1).strip()
    m = re.search(r"(?m)^#\s+(.+)$", text)
    return m.group(1).strip() if m else ""


LEAD_WORDS = ("分かること", "わかること", "結論", "要点", "答え", "ポイント", "この記事", "まとめ")
ACTION_WORDS = ("示唆", "要点", "手順", "チェック", "次の一歩", "やること", "提案", "使い方", "進め方",
                "宿題", "ステップ", "向く", "判断", "組み立て", "一緒に", "まとめ", "考え方", "方法")
VAGUE_TITLE = re.compile(r"(について|とは|の話|入門|概要|基礎|まとめ)$")


def marketing(path, sections, body):
    """マーケティング効果の4項目を点検する。1つ以下なら止める、2〜3なら印。"""
    text = path.read_text(encoding="utf-8")
    title = title_of(path, text)
    names = [k for k in sections if k]          # 節の名前（本文の順）
    intro = sections.get("", "")
    first_two = " ".join(names[:2])
    missing = []

    # 1. 結論・得が冒頭にある
    lead_ok = any(w in first_two for w in LEAD_WORDS) or bool(re.search(r"\d", intro[:300]))
    if not lead_ok:
        missing.append("冒頭に結論・読者の得（分かること／結論／要点、または具体的な数字）")

    # 2. 具体的な数字がある
    if not re.search(r"\d", body):
        missing.append("本文に具体的な数字")

    # 3. 持ち帰れる行動がある
    action_ok = any(any(w in n for w in ACTION_WORDS) for n in names) \
        or re.search(r"(?m)^\s*1\.\s", body) is not None \
        or len(re.findall(r"(?m)^\s*-\s", body)) >= 3
    if not action_ok:
        missing.append("持ち帰れる行動（示唆／手順／次の一歩の節、または手順の箇条書き）")

    # 4. 題名が具体的
    title_ok = len(title) >= 8 and not (VAGUE_TITLE.search(title) and not re.search(r"\d", title) and len(title) < 14)
    if not title_ok:
        missing.append(f"具体的な題名（いま：「{title or '（題名なし）'}」）")

    score = 4 - len(missing)
    if score <= 1:
        return [f"マーケティング効果が見込みにくい（{score}/4）。足りないもの：" + "、".join(missing)], []
    if missing:
        return [], [f"マーケティング点検 {score}/4。あると良いもの：" + "、".join(missing)]
    return [], []


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
        mark.append("「出典」の節がありません")
    else:
        for line in src_text.splitlines():
            m = re.match(r"\s*(\d+)\.\s+(.*)", line)
            if m:
                sources[int(m.group(1))] = m.group(2)
        if not sources:
            mark.append("「出典」に、番号付きの資料が1つもありません")
        for n, s in sources.items():
            if not re.search(r"https?://", s) and not re.search(r"出典\d", s):  # 「出典1の目次」のような参照は可
                mark.append(f"出典{n}にアドレスがありません")
    if sources is not None:
        cited = {int(n) for n in CITE.findall(body)}
        for n in sorted(cited - set(sources)):
            mark.append(f"本文に [{n}] がありますが、出典に{n}番がありません")
        for n in sorted(set(sources) - cited):
            mark.append(f"出典{n}は、本文のどこからも引かれていません")

    # --- マーケティング効果（緩めの点検の主軸） ---
    m_stop, m_mark = marketing(path, sections, body)
    stop += m_stop
    mark += m_mark
    if sources is None:
        return stop, mark

    # --- 要確認 ---
    n_flag = body.count("【要確認】")
    if n_flag and "要確認" not in sections:
        mark.append("本文に【要確認】がありますが、理由を書く「要確認」の節がありません")
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
