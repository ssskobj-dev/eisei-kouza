// 講座のPDFデザイン。色を変えるときは、下の3色を直す。
#let c-main = rgb("#2f5d94")   // 見出しや帯の青
#let c-deep = rgb("#1c2f4f")   // 文字に使う濃い青
#let c-pale = rgb("#e6edf6")   // 帯の地の薄い青
#let c-ink = rgb("#1f2a33")

// 章番号と部番号。scripts/build.py が1冊にまとめるときに入れる。
#let chapter-no = state("chapter-no", none)
#let part-no = state("part-no", none)
#let chapter-sub = state("chapter-sub", none)

// 「第 2 部」「第 4 章」の白い札
#let no-chip(pre, num, post) = box(
  fill: white, radius: 4pt, inset: (x: 7pt, y: 4pt), baseline: 22%,
)[#text(size: 9pt, weight: "bold", fill: c-ink)[#pre]#h(1pt)#text(size: 17pt, weight: "black", fill: c-main)[#num]#h(1pt)#text(size: 9pt, weight: "bold", fill: c-ink)[#post]]

// 薄い青の帯。右側だけ丸くする
#let band(body) = block(
  width: 100%, fill: c-pale, radius: (right: 16pt), inset: (left: 8pt, right: 14pt, y: 7pt),
)[#set par(justify: false, leading: 0.5em); #body]

// ---- 目次の部品 ----
#let toc-part(num, title) = block(above: 1.7em, below: 0.9em, breakable: false)[
  #band[#if num != none [#no-chip("第", num, "部")#h(9pt)]#text(size: 14pt, weight: "bold", fill: c-ink)[#title]]
]

#let toc-chapter(num, title, target) = block(above: 0.85em, below: 0.4em, inset: (left: 1.6em), breakable: false)[
  #set par(justify: false)
  #grid(
    columns: (2.6em, auto, 1fr, auto), column-gutter: 4pt, align: bottom,
    text(fill: c-ink)[#num],
    link(target)[#text(fill: c-ink)[#title]],
    box(width: 100%, inset: (bottom: 2pt))[#text(fill: c-ink.lighten(35%), size: 7pt)[#repeat[#h(1.5pt).#h(1.5pt)]]],
    context text(fill: c-ink)[#counter(page).at(locate(target)).first()],
  )
]

#let toc-chapter-pending(num, title) = block(above: 0.85em, below: 0.4em, inset: (left: 1.6em), breakable: false)[
  #set par(justify: false)
  #set text(fill: c-ink.lighten(50%))
  #grid(
    columns: (2.6em, auto, 1fr, auto), column-gutter: 4pt, align: bottom,
    [#num], [#title], [], text(size: 8pt)[準備中],
  )
]

#let toc-points(items) = block(above: 0.75em, below: 1em, inset: (left: 5.2em))[
  #set par(justify: false, leading: 0.6em)
  #set text(size: 9pt, fill: c-ink.lighten(15%))
  #items.map(i => box[#text(fill: c-main, size: 6pt, baseline: -1pt)[●]#h(3pt)#i]).join(h(9pt))
]

// ---- 部の扉 ----
// num: この部の番号（なければ none）、all-parts: 全部の部の名前、
// chapters: (番号, 題名, 飛び先のラベルか none, キーワードの配列) の配列
#let part-page(num, title, lead, index, all-parts, chapters) = {
  pagebreak(weak: true)
  // 上：いま全体のどこにいるか
  grid(
    columns: (1fr,) * all-parts.len(), column-gutter: 5pt,
    ..all-parts.enumerate().map(((i, name)) => {
      let on = i == index
      block(
        width: 100%, radius: 5pt, inset: (x: 8pt, y: 6pt),
        fill: if on { c-main } else { c-pale },
      )[#set par(justify: false)
        #text(size: 8pt, weight: "bold", fill: if on { white } else { c-deep.lighten(25%) })[#name]]
    })
  )
  v(16mm)
  // 中：大きな番号と題名
  grid(
    columns: (auto, 1fr), column-gutter: 14pt, align: horizon,
    if num != none {
      block(fill: c-main, radius: 10pt, inset: (x: 13pt, y: 10pt))[
        #text(size: 10pt, weight: "bold", fill: white)[第]#h(2pt)#text(size: 38pt, weight: "black", fill: white)[#num]#h(2pt)#text(size: 10pt, weight: "bold", fill: white)[部]
      ]
    },
    block[#set par(justify: false, leading: 0.5em)
      #text(size: 25pt, weight: "black", fill: c-ink)[#title]],
  )
  heading(level: 1)[#title]
  v(4mm)
  line(length: 100%, stroke: 2.5pt + c-main)
  if lead != none {
    v(3mm)
    block(width: 88%)[#set par(leading: 0.95em); #text(size: 11pt)[#lead]]
  }
  v(11mm)
  // 下：この部の章
  text(size: 9pt, weight: "bold", fill: c-main)[この部で学ぶこと]
  v(1mm)
  for (no, name, target, points) in chapters {
    let ready = target != none
    block(
      width: 100%, breakable: false, above: 7pt, below: 0pt,
      fill: if ready { c-pale.lighten(45%) } else { luma(247) },
      radius: 8pt, inset: (x: 12pt, y: 10pt),
    )[
      #set par(justify: false, leading: 0.55em)
      #grid(
        columns: (3.4em, 1fr, auto), column-gutter: 8pt, align: (left + horizon, left + horizon, right + horizon),
        text(size: 15pt, weight: "black", fill: if ready { c-main } else { c-ink.lighten(60%) })[#no],
        [
          #text(size: 11pt, weight: "bold", fill: if ready { c-ink } else { c-ink.lighten(45%) })[
            #if ready { link(target)[#name] } else { name }
          ]
          #if points.len() > 0 [
            #v(-3pt)
            #text(size: 8pt, fill: if ready { c-deep } else { c-ink.lighten(55%) })[#points.join("　・　")]
          ]
        ],
        if ready {
          context box(fill: white, radius: 9pt, inset: (x: 9pt, y: 4pt))[
            #text(size: 9pt, weight: "bold", fill: c-deep)[#counter(page).at(locate(target)).first() ページ]
          ]
        } else {
          text(size: 8pt, fill: c-ink.lighten(55%))[準備中]
        },
      )
    ]
  }
  pagebreak(weak: true)
}

// ---- 本体 ----
#let article(
  title: none,
  subtitle: none,
  book: false,
  paper: "a4",
  lang: "ja",
  font: ("Noto Sans CJK JP",),
  fontsize: 10pt,
  doc,
) = {
  // 1冊にまとめたときは 部=1、章=2、節=3。
  // 章だけのときは、Quartoが見出しを1段上げるので 節=1。
  let sec = if book { 3 } else { 1 }

  set page(
    paper: paper,
    margin: (x: 22mm, top: 26mm, bottom: 24mm),
    header: context {
      if counter(page).get().first() > 1 or not book {
        set text(size: 8pt, fill: c-deep, weight: "bold")
        block(width: 100%, stroke: (bottom: 2pt + c-pale), inset: (bottom: 4pt))[
          #box(fill: c-main, width: 7pt, height: 7pt, baseline: 0.5pt)#h(5pt)#title
        ]
      }
    },
    footer: context {
      let dot(c) = box(circle(radius: 2.6pt, fill: c), baseline: -1.5pt)
      align(center)[
        #dot(c-pale)#h(3pt)#dot(c-main.lighten(45%))#h(4pt)#box(fill: c-main, radius: 7pt, inset: (x: 13pt, y: 3pt), baseline: 3pt)[#text(fill: white, size: 9pt, weight: "bold")[#counter(page).display()]]#h(4pt)#dot(c-main.lighten(45%))#h(3pt)#dot(c-pale)
      ]
    },
  )
  set text(lang: lang, font: font, size: fontsize, fill: c-ink)
  set par(justify: true, leading: 0.85em)
  show par: set block(spacing: 1.15em)
  set list(marker: text(fill: c-main, size: 6pt, baseline: 1.5pt)[●], indent: 0.4em, body-indent: 0.6em)
  set enum(indent: 0.4em, body-indent: 0.6em)
  show link: set text(fill: c-deep)
  show strong: set text(fill: c-ink, weight: "bold")

  // 表：見出し行を薄い青、行の下に細い線
  set table(
    inset: (x: 8pt, y: 7pt),
    stroke: (x, y) => (bottom: 0.6pt + c-main.lighten(55%)),
    fill: (x, y) => if y == 0 { c-pale },
  )
  set table.hline(stroke: 1pt + c-main)
  show table.cell.where(y: 0): set text(weight: "bold", fill: c-deep)
  show table: set par(justify: false, leading: 0.6em)
  show table: set text(size: 9pt)

  // 図：幅いっぱいに置き、説明は小さく
  show figure: set block(above: 1.5em, below: 1.5em)
  show figure.caption: set text(size: 8.5pt, fill: c-deep, weight: "bold")
  set figure(numbering: none, gap: 0.7em)
  show image: set block(width: 100%)

  // 部の扉（part-page が描く。見出し自体は、しおり用に見えない形で置く）
  show heading.where(level: 1): it => if book { box(width: 0pt, height: 0pt) } else { it }

  // 章の題名（1冊にまとめたとき）
  show heading.where(level: 2): it => if book {
    pagebreak(weak: true)
    block(below: 1.6em)[
      #context band[#grid(
        columns: (auto, 1fr), column-gutter: 10pt, align: horizon,
        if chapter-no.get() != none { no-chip("", chapter-no.get(), "") },
        block(inset: (y: 3pt))[
          #text(size: 16pt, weight: "bold", fill: c-ink)[#it.body]
          #if chapter-sub.get() != none [
            #v(-4pt)
            #text(size: 10.5pt, weight: "bold", fill: c-deep)[#chapter-sub.get()]
          ]
        ],
      )]
    ]
  } else { it }

  // 節の見出し：青い四角と下線
  // 前の節との間に1行分の空きを入れる。
  // 見出しだけがページの下に取り残されないよう、見出しの下に3行分の場所を確保してから詰め直す。
  show heading.where(level: sec): it => {
    v(20pt)
    block(width: 100%, breakable: false, below: 0pt)[
      #block(
        width: 100%, stroke: (bottom: 1.2pt + c-main), inset: (bottom: 5pt),
      )[#box(fill: c-main, width: 9pt, height: 9pt, radius: 1.5pt, baseline: 0.5pt)#h(7pt)#text(size: 12.5pt, weight: "bold", fill: c-deep)[#it.body]]
      #v(42pt)
    ]
    v(-42pt)
    v(11.5pt, weak: true)   // 見出しと本文の間。直後の段落の空きと重なっても増えない
  }

  show heading.where(level: sec + 1): it => block(above: 1.4em, below: 0.8em)[
    #text(size: 10.5pt, weight: "bold", fill: c-deep)[#it.body]
  ]

  if book {
    // 表紙
    page(header: none, footer: none, margin: 0pt)[
      #block(width: 100%, height: 38%, fill: c-main)[]
      #block(inset: (x: 26mm, top: 14mm))[
        #set par(justify: false, leading: 0.6em)
        #text(size: 10pt, weight: "bold", fill: c-main)[Satellite to Decision]
        #v(4mm)
        #text(size: 24pt, weight: "black", fill: c-ink)[#title]
        #if subtitle != none [
          #v(1mm)
          #text(size: 13pt, weight: "bold", fill: c-deep)[#subtitle]
        ]
        #v(6mm)
        #block(fill: c-pale, radius: (right: 12pt), inset: (x: 12pt, y: 7pt))[#text(size: 11pt, fill: c-deep, weight: "bold")[強み、限界、現実的な落とし所]]
      ]
    ]
    counter(page).update(1)
  } else if title != none {
    // 章だけのPDFの題名
    block(below: 1.4em)[
      #band[#block(inset: (x: 4pt, y: 5pt))[
        #text(size: 16pt, weight: "bold", fill: c-ink)[#title]
        #if subtitle != none [
          #v(-4pt)
          #text(size: 10.5pt, weight: "bold", fill: c-deep)[#subtitle]
        ]
      ]]
    ]
  }

  doc
}
