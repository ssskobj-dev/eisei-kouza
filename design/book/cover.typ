// 本の表紙。Kindle用（PNG 1600x2560 相当）と、印刷用（表1・背・表4をつないだPDF）を1つの元から作る。
#let c-main = rgb("#2b5a8c")
#let c-deep = rgb("#1d3e63")
#let c-pale = rgb("#dbe6f3")
#let c-ink = rgb("#1b1f24")
#let title = sys.inputs.at("title", default: "衛星データマーケッター\n公式テキスト").replace("\\n", "\n")
#let subtitle = sys.inputs.at("subtitle", default: "2級・1級")
#let tagline = sys.inputs.at("tagline", default: "衛星データを「使う側」の判断力を証明する")
#let lines = sys.inputs.at("lines", default: "強みと限界を、場面で言い分ける|調達と費用の、どこにお金がかかるか|提案の筋、仕様書、検収、効果の説明|巻末：ケース問題 70問と解説").split("|")
#let brand = "Satellite to Decision"
#let publisher = "Spacify合同会社"
#let blurb = sys.inputs.at("blurb", default: "衛星データは「買えば使える」ものではありません。何が測れて何が測れないか、費用がどこにかかるか、結果をどう顧客に説明するか。この本は、衛星会社にも解析会社にも属さない立場から、仕事で衛星データを使う人・勧める人が、場面を示されて判断できるようになるための教科書です。資格「衛星データマーケッター」2級・1級の公式テキスト。")

#let front(w, ph) = box(width: w, height: ph, fill: white, clip: true)[
  #place(top + left, block(width: w, height: ph * 0.42, fill: c-main))
  #place(top + left, dx: w * 0.08, dy: ph * 0.07)[
    #text(size: ph * 0.016, weight: "bold", fill: white)[#brand]
  ]
  #place(top + left, dx: w * 0.08, dy: ph * 0.46)[
    #set par(leading: 0.5em)
    #block(width: w * 0.84)[
      #text(size: ph * 0.047, weight: "black", fill: c-ink)[#title]
      #v(ph * 0.012)
      #text(size: ph * 0.028, weight: "bold", fill: c-deep)[#subtitle]
      #v(ph * 0.02)
      #block(fill: c-pale, radius: 6pt, inset: (x: 10pt, y: 6pt))[#text(size: ph * 0.017, weight: "bold", fill: c-deep)[#tagline]]
      #v(ph * 0.03)
      #for l in lines [
        #box(fill: c-main, width: 6pt, height: 6pt, radius: 1pt, baseline: -1pt) #h(5pt) #text(size: ph * 0.015, fill: c-ink)[#l] \
      ]
    ]
  ]
  #place(bottom + left, dx: w * 0.08, dy: -ph * 0.05)[
    #text(size: ph * 0.014, weight: "bold", fill: c-deep)[#publisher]
  ]
]

#let back(w, ph) = box(width: w, height: ph, fill: c-main, clip: true)[
  #place(top + left, dx: w * 0.1, dy: ph * 0.12)[
    #set par(leading: 0.8em, justify: true)
    #block(width: w * 0.8)[
      #text(size: ph * 0.02, weight: "bold", fill: white)[この本で、できるようになること]
      #v(ph * 0.02)
      #text(size: ph * 0.0135, fill: white)[#blurb]
      #v(ph * 0.04)
      #for l in lines [
        #box(fill: white, width: 6pt, height: 6pt, radius: 1pt, baseline: -1pt) #h(5pt) #text(size: ph * 0.014, fill: white, weight: "bold")[#l] \
      ]
    ]
  ]
  #place(bottom + left, dx: w * 0.1, dy: -ph * 0.16)[
    #block(width: w * 0.8)[
      #text(size: ph * 0.013, fill: white)[#brand　#publisher \ https://ssskobj-dev.github.io/eisei-kouza/]
    ]
  ]
  // ISBNのバーコードは KDP が右下に自動で置く（約 2in × 1.2in を空けておく）
  #place(bottom + right, dx: -0.25in, dy: -0.25in, block(width: 2in, height: 1.2in, fill: white))
]

#let mode = sys.inputs.at("mode", default: "kindle")

#if mode == "kindle" {
  // Kindle: 1600x2560 px 相当。1px=0.75pt
  set page(width: 1200pt, height: 1920pt, margin: 0pt)
  front(1200pt, 1920pt)
} else {
  // 印刷：表4 + 背 + 表1、周囲に塗り足し 0.125in
  let trim-w = 7.17in
  let trim-h = 10.12in
  let bleed = 0.125in
  let pages = int(sys.inputs.at("pages", default: "253"))
  let spine = pages * 0.002347in   // プレミアムカラー（白紙）の1ページあたりの厚み
  set page(width: trim-w * 2 + spine + bleed * 2, height: trim-h + bleed * 2, margin: 0pt, fill: c-main)
  place(top + left, dx: 0pt, dy: 0pt, back(trim-w + bleed, trim-h + bleed * 2))
  place(top + left, dx: trim-w + bleed, dy: 0pt, box(width: spine, height: trim-h + bleed * 2, fill: c-deep)[
    #place(center + horizon, rotate(90deg, reflow: true)[#text(size: 13pt, weight: "bold", fill: white)[#title.replace("\n", "　") #h(1em) #subtitle]])
  ])
  place(top + left, dx: trim-w + bleed + spine, dy: 0pt, box(width: trim-w + bleed, height: trim-h + bleed * 2, clip: true)[
    #place(top + left, dx: 0pt, dy: 0pt, front(trim-w + bleed, trim-h + bleed * 2))
  ])
}
