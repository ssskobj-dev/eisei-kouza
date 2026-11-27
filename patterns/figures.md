# 図解の型

図は、`figures/<章のid>.yaml` に内容を書くと、`scripts/figures.py` がSVGにする。手本は `figures/survey-road-slope-screening.yaml`。色とフォントは自動でそろう。

## 型の一覧

| type | 何を見せるか | 使う場面 |
|---|---|---|
| `split` | 左右2つの対比や分担 | 衛星と人の役割分担、できること・できないこと、内製・外注 |
| `cards` | 番号付きの要点の一覧 | 強み、限界、費用の内訳、確認項目 |
| `flow` | 左から右への手順 | 進め方、導入の段取り。誰が行うかを色で分ける |
| `funnel` | 上から下への絞り込み | 全体 → 候補 → 確定 |
| `scale` | 向く条件から向かない条件までの並び | 対象の向き不向き、精度や費用の大小 |
| `sightline` | 衛星SARが測れる向き（固定の図） | 干渉SARの限界を説明する章 |
| `bar` | 横棒のグラフ。大きさの比較（1系列） | 市場規模の推移や比較。予測や見込みの値は `muted: true` で灰色にする。`unit` と `source` は必須 |
| `range` | 推計の幅。小さい値から大きい値までの帯 | 調査会社ごとに数字が違うとき。`low` と `high` を書く。値が1つなら `low` だけ |
| `scene` | 絵のある図解。空・地面・アイコン・電波の線・印を置いた「絵の面」と、見出しの帯、箇条書きを1〜3枚並べる | しくみの説明（電波の跳ね返り、軌道の向き、雲と夜）、対比（`between: vs`）。型にはまらない図はこれで組む。下の「scene の書き方」 |
| `thumbnail` | noteの見出し画像（1280×670） | note記事。`kind` は `news`（時事）、`course`（本編連動）、`guide`（実務メモ）、`report`（市場レポート）、`usecase`（ユースケース） |

色の役割は3つ。`satellite`（青）は衛星や解析が行うこと、`human`（橙）は人や現地が行うこと、`none`（灰）は限界や対象外。

## 1章に入れる図

ユースケース型の章には、次の位置に図を入れる。文章だけの節が2つ続かないようにする。

| 位置 | 型 | 内容 |
|---|---|---|
| 冒頭（判断できるようになること、の直後） | `split` | この章の結論。衛星に任せられること、人が行うこと |
| 使える衛星の強み | `cards` | この用途で効く強み（2〜3枚） |
| 現在の技術的な限界 | `cards`（`role: none`） | 限界の一覧 |
| 限界のうち、仕組みの理解が要るもの | `sightline` など | 1つだけ |
| 現実的な落とし所 | `funnel` か `flow` | 絞り込みの流れ、手順と担当 |
| 始め方と費用感 | `cards` | 費用の内訳 |
| 向いている条件、向いていない条件 | `scale` | 表の前に、最も効く条件を1本の帯で |

基礎型は2〜3枚、実務型は手順の `flow` と確認項目の `cards`、比較型は `split` か `scale` を入れる。

## 書き方の決まり

- 図の中の文字は短くする。題は12字、説明は30字まで。詳しい説明は本文に書く
- 図にだけ書いて本文に書かない情報を作らない（図が読めない人にも伝わるようにする）
- 本文には `![説明](../../figures/<章のid>/<図のid>.svg){fig-alt="図の内容を文章で"}` の形で置く
- `fig-alt` には、図を見なくても内容が分かる文章を書く
- 数字や事実を図に入れるときも、本文と同じく出典が要る
- 写真や衛星画像は、この仕組みでは扱わない。利用条件を確認できたものだけ、別に置く

## 型を増やすとき

`scripts/figures.py` に `fig_<型の名前>` の関数を足し、`TYPES` に登録して、上の一覧に1行足す。

## グラフの決まり（`bar`、`range`）

- 1つのグラフに入れるのは、同じ単位、同じ定義の数字だけ。定義の違う推計は `range` で並べ、ラベルに「何を含むか」を書く
- 実績と、見込みや予測を同じ色にしない。見込みと予測は `muted: true`
- 単位（`unit`）と出どころ（`source`、年を含む）を必ず書く
- 円グラフ、2つの目盛りを持つグラフは作らない


## scene の書き方（絵のある図解）

```yaml
- id: mechanism
  type: scene
  alt: 図を文で説明（必須）
  height: 200          # 絵の面の高さ（px）。省略時 210
  between: vs          # パネルの間に入れる印（省略可）
  panels:
    - title: 災害前：畑は明るい      # 見出しの帯
      role: satellite               # 帯と枠の色（satellite / human / none）
      sky: day                      # 絵の面の地：day（水色）/ night（紺、星）/ plain（役割の色）/ white
      ground: sand                  # 下の帯：sand / grass / water / none
      draw:                         # 置くもの。x, y は絵の面の中の割合（0〜1）、size は px
        - {icon: satellite, x: 0.3, y: 0.2, size: 62}
        - {icon: water, x: 0.42, y: 0.86, size: 120, calm: true}
        - {icon: mountain, x: 0.6, y: 0.5, size: 150, lit: left}     # lit は明るい側
        - {beam: [0.33, 0.36, 0.42, 0.72], style: solid, color: warm}  # 線。style は solid / dashed / dotted / wavy / zigzag。head: false で矢じり無し
        - {label: 抜ける, x: 0.12, y: 0.62, mark: cross, color: warm}  # 短い文字。mark は check / cross / warning
        - {label: 説明の文, x: 0.8, y: 0.5, size: 11.5, units: 7, weight: normal}   # units は折り返す幅（全角の文字数）
      items:                        # 帯の下の箇条書き
        - ざらついた畑や草地は明るく写る
  note: 出典：…
```

- アイコンは `scripts/icons.py` にある名前：satellite、sun、moon、cloud、rain、tree、building、buildings、house、mountain、water、field、ground、magnifier、calendar、ruler、coins、check、cross、warning、eye、person、drone、radar、leaf（葉）、grid（画素のマス目。`cells` に16色で塗り分け）、sheet（表）、rock（岩と裸地）、robot（AI）、shadow（雲の影）。足すときは同じ書き方で1つ関数を足す（100×100 の座標で描く）
- 色は役割名（satellite=青、human=橙、none=灰、warm、white）か色コード
- 文字は短く。絵で分かることを文で繰り返さない。出典は `note` に書く
- 手本：`figures/codex-3-13-flood-mapping.yaml` の `mechanism`（3枚）と `orbit`（2枚、vs）
