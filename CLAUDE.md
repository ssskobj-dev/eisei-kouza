# このリポジトリでの作業ルール（Claude向け）

衛星データ実務講座の教材を作るリポジトリ。章立てとパターンから原稿を生成する。

## 「未作成の章を作って」と頼まれたら

1. `python scripts/build.py check` で章立てに誤りがないか確かめる。誤りがあれば直さずに報告する
2. `python scripts/build.py todo` で対象の章を確認する。一度に作るのは3章まで
3. 章ごとに次を読む
   - `syllabus/` の該当部品（goals、must_include、material、strengths、tradeoffs）
   - `patterns/chapter_types/<type>.md`（見出しの並び）
   - `patterns/audiences.yaml` と `patterns/depths.yaml` の該当項目
   - `patterns/strengths.yaml`、`patterns/tradeoffs.yaml` の該当項目
   - `patterns/style.md`（必ず守る）
   - `data/sources.yaml`（タグが合う資料）
4. 資料を実際に読んで裏を取る。足りなければ公的資料を探し、`data/sources.yaml` に追記する
5. 原稿を `chapters/<章立てのファイル名>/<id>.qmd` に書く。手本は `chapters/survey/survey-road-slope-screening.qmd`
6. 図を `figures/<id>.yaml` に書き、`python scripts/figures.py <id>` で作る。型と入れる位置は `patterns/figures.md` に従う。できた図を1枚ずつ見て、文字のはみ出しや重なりがないか確かめる
7. `outputs` に指定された出力を、`patterns/outputs/` の型に従って作る
8. 章立ての `status` を `done` にする
9. `python scripts/build.py check` と `nav` を実行し、通ることを確かめる
10. ブランチを作ってプルリクエストを出す。説明欄に、章ごとの「要確認」の件数と内容を書く

## 守ること

- 出典のない数字、仕様、金額、事例を書かない。確認できなければ【要確認】を付け、章末に理由を書く
- `material` に書かれた現場のメモは、最優先の素材として使う。書かれていない事例を作らない
- 変わりやすい値は `_variables.yml` に置き、本文では `{{< var ... >}}` で参照する
- 特定の事業者やサービスを勧めない
- 他者の資料の文章や図をそのまま使わない
- 料金の比較表、価格の相場、顧客名、会員の情報をこのリポジトリに書かない（公開リポジトリのため）
- main に直接書き込まない。必ずプルリクエストにする

## 頼まれ方の例

- 「survey の未作成の章を2つ作って」
- 「survey-subsidence を infra_owner 向け、overview の深さで作り直して」
- 「survey-road-slope-screening から研修スライドとワークブックを作って」
- 「survey-subsidence の図を増やして」→ `figures/survey-subsidence.yaml` に足す
- 「デザインを変えて」→ `design/` の3ファイル（PDF、サイト）と `scripts/figures.py`（図）の色をそろえて直す
- 「example-custom の講座を1冊にまとめて」→ `python scripts/build.py course example-custom`
- 「新しい分野（水道）の章立てを提案して」→ `syllabus/water.yaml` と `courses/water.yaml` の案を出す
