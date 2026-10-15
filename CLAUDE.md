# このリポジトリでの作業ルール（Claude向け）

Satellite to Decisionの教材を作るリポジトリ。章立てとパターンから原稿を生成する。

## サイトの構造

| フォルダ | シリーズ | 中身 |
|---|---|---|
| `landscape/` | 市場ガイド | テーマごとのフォルダに、切り口ごとに1本 |
| `casebook/` | ユースケース集 | 1件につき1本 |
| `learn/` | 学習プログラム | 講座の章（`learn/<分野>/`）とケース問題（`learn/quiz/`） |
| `themes/` | テーマから探す | 自動で作られる。手で書かない |

- シリーズの名前は `_variables.yml` の `series`、テーマは `data/themes.yaml` にある
- 各シリーズの入口（`index.qmd`）、講座のページ（`learn/course-*.qmd`）、`themes/` は `python scripts/build.py nav` が作る。手で書かない、コミットしない
- 記事の「関連する記事」には、最初にテーマのページへのリンクを置く
- 「Sentinelで見られるユースケースと解析手法」（`learn/sentinel.qmd`）も `nav` が作る。もとは `data/sentinel_methods.yaml`（手法の説明と、`data/usecases.yaml` の番号）。手法やユースケースを足すときは、この yaml を直す。数字と仕様には出典の番号を付ける
- 英語版は固定ページだけ（`en/` の下）。`en/index.qmd`、`en/about.qmd`、`en/register.qmd` は手で書く。各シリーズの入口とSentinelの早見表の英語版は `nav` が作る（英語の文は `data/sentinel_methods_en.yaml` と `scripts/build.py` の `english_pages`）。日本語の固定ページを直したら、英語版も合わせて直す。記事は英語にしない
- メニューの英語化、言語の切り替え、有料登録のボタン、押下の記録は `design/track.html`。訪問者数の計測は `design/analytics.html`（Google Analytics 4、同意した人だけ）
- **無料と有料の線**：ユースケース集と市場ガイドは前半が無料、後半が有料。講座の章は最初の3分の1が無料。Sentinelの早見表は最初の節だけ無料。ケース問題と時事解説は全部無料。切り分けは `design/paywall.lua` が行い、有料の範囲は公開するサイトに出ない（各フォルダの `_metadata.yml` で指定）。記事は全文を書く。PDF、サイト内の検索、一覧の絞り込み、「テーマから探す」は有料版の機能なので、公開するサイトでは作らない
- 有料の範囲がある記事を書いたら、`python scripts/build.py notefull` を実行し、できた `note/<フォルダ>/full.md`（noteで売るための全文）も一緒にコミットする
- `news/`（時事解説）も `nav` が `note/<日付>-<話題>/article.md` から作る

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
5. 原稿を `learn/<章立てのファイル名>/<id>.qmd` に書く。手本は `learn/survey/survey-road-slope-screening.qmd`
6. 図を `figures/<id>.yaml` に書き、`python scripts/figures.py <id>` で作る。型と入れる位置は `patterns/figures.md` に従う。できた図を1枚ずつ見て、文字のはみ出しや重なりがないか確かめる
7. `outputs` に指定された出力を、`patterns/outputs/` の型に従って作る
8. 章立ての `status` を `done` にする
9. `python scripts/build.py check` と `nav` を実行し、通ることを確かめる
9-2. 「公開前の点検」の手順を行う（`python scripts/verify.py`、note用フォルダの `sns.md` の作成）。続けて `python scripts/build.py notefull` を実行し、できた `note/<id>/full.md` も一緒にコミットする
10. ブランチ（毎朝の自動実行では `learn/<日付>`）を作ってプルリクエストを出す。説明欄に、章ごとの「要確認」の件数と内容、点検の「印」の一覧を書く

### 毎朝の自動実行で作る章の順番

1回に2章まで。検定の問題の材料が足りない分野（調達と費用、基礎）を先に作る。次の順で、`status: todo` のものを上から選ぶ。全部終わったら、`python scripts/build.py todo` の順に進む。

1. `common-data-cost`（データの入手方法と費用の考え方）
2. `survey-procurement`（衛星データの選び方と調達の実務）
3. `agri-cost-benefit`（費用対効果の測り方）
4. `survey-proposal-pricing`（提案書、仕様書、見積もりの作り方）
5. `agri-municipal-spec`（自治体が衛星サービスを導入するときの仕様書）
6. `survey-quality-explain`（成果物の品質確認と、顧客への説明）
7. `common-strengths-limits`、`common-optical-sar`、`common-vs-other-means`（基礎）

開いたままのプルリクエストに同じ章があれば、その章は飛ばす。`material`（現場のメモ）が空の章は、公的な資料だけで書き、書かれていない事例を作らない。金額や相場は、出典のある公開の数字だけを書く。

## 「今日のnote記事を作って」と頼まれたら（毎朝の自動実行も同じ）

1. `data/news_sources.yaml` の情報源を調べ、`patterns/outputs/news.md` の基準を満たす話題を選ぶ。最大3本。基準を満たす話題が足りなければ、本数を減らす。1つもなければ作らず、その旨を報告して終わる
2. 話題ごとに、発表元の資料を読んで `note/<日付>-<話題>/article.md` を書く
3. 同じフォルダに `figures.yaml` を書き、`python scripts/figures.py <フォルダ名>` で見出し画像と図（PNG）を作る。できた画像を1枚ずつ見て、文字のはみ出しや切れがないか確かめる
4. 「公開前の点検」の手順を行う（`python scripts/verify.py`、`sns.md` の作成）。結果の「印」の一覧をプルリクエストの説明欄に貼る
4-2. `python scripts/build.py nav` を実行し、サイトの時事解説のページ（`news/`、自動で作られる）ができることを確かめる。`article.md` の形は `patterns/outputs/news.md` の「サイトへの掲載」に従う
5. ブランチ `note/<日付>` を作り、プルリクエストを出す。説明欄に、記事ごとの題名、出典、要確認の件数を書く
6. 最後に、作った本数と題名、プルリクエストの場所を短く報告する

noteへの投稿は人が行う。Claudeは投稿しない。プルリクエストが main に入ると、同じ記事がサイトの「時事解説」に公開される（要確認の節は載らない）。

## 「今日の市場レポートを作って」と頼まれたら（毎朝の自動実行も同じ）

1. `python scripts/build.py check` を通す。次に `python scripts/build.py reports 2` で、次に書く2本（テーマと切り口）を確かめる
2. `landscape/topics.yaml` に `id` のないテーマがあれば、英小文字の短い `id` を付ける（例：農業 → `agri`）。それ以外の行は書き換えない
3. 書くテーマが残っていなければ、作らずに「テーマが残っていません。`landscape/topics.yaml` に足してください」と報告して終わる
4. 1本ごとに `patterns/outputs/report.md` の手順どおりに書く。下調べは `data/market-report-2026-10/` の該当する章。**数字と事例は、必ず出典の原文を開いて確かめる**
5. 図を `figures/report-<テーマのid>-<切り口>.yaml` に書き、`python scripts/figures.py report-<テーマのid>-<切り口>` で作る。1枚ずつ見て確かめる
6. note用の要約を `note/report-<テーマのid>-<切り口>/` に作る（`article.md` と `figures.yaml`。`python scripts/figures.py report-<テーマのid>-<切り口>` で、見出し画像と図のPNGもできる）
7. `python scripts/build.py check` と `nav` を通す
8. ブランチ `landscape/<日付>` を作り、プルリクエストを出す。説明欄に、記事ごとの題名、主な出典、要確認の件数と内容を書く
9. 最後に、作った本数と題名、残りの本数、プルリクエストの場所を短く報告する

市場レポートの読者はコンサルタント。価格表、有料の報告書の中身、非公開の契約金額は書かない。

## 「今日のユースケースの記事を作って」と頼まれたら（毎朝の自動実行も同じ）

1. `python scripts/build.py check` を通す。次に `python scripts/build.py usecases 3` で、次に書く3本を確かめる
2. 書くものが残っていなければ、作らずに「ユースケースが残っていません。`data/usecases.yaml` に足してください」と報告して終わる
3. 1本ごとに `patterns/outputs/usecase_article.md` の手順どおりに書く。`data/usecases.yaml` の行は下調べ。**出典を開いて確かめる。限界と費用は、出典にあることを優先する**
4. 記事を書いたら、`data/usecases.yaml` の該当する行に `slug:` を足す。ほかの行は書き換えない
4-2. 「公開前の点検」の手順を行う（`python scripts/verify.py`、note用フォルダの `sns.md` の作成）。結果の「印」の一覧をプルリクエストの説明欄に貼る
5. 図を `figures/usecase-<slug>.yaml` に書き、`python scripts/figures.py usecase-<slug>` で作る。1枚ずつ見て確かめる
6. note用の要約を `note/usecase-<slug>/` に作る（`article.md` と `figures.yaml`）。同じコマンドで、見出し画像と図のPNGもできる
7. `python scripts/build.py check` と `nav` を通す
8. ブランチ `casebook/<日付>` を作り、プルリクエストを出す。説明欄に、記事ごとの題名、主な出典、要確認の件数と内容を書く
9. 最後に、作った本数と題名、残りの本数、プルリクエストの場所を短く報告する

## 「今日の英語の事例動画を作って」と頼まれたら（毎朝の自動実行も同じ）

1. `python scripts/build.py envideos` で、作る候補（公開済み・海外/両方・英語動画が未作成）を確かめる。1回に1本。無ければ作らず報告して終わる
2. 先頭の候補を1つ選ぶ。もとの日本語記事（`casebook/<slug>.qmd`）と `data/usecases.yaml` の行を読む。`source_url` を開いて、事例・数字・費用を確かめる
3. `video/usecase-<slug>-en/script.yaml` を、`patterns/outputs/video.md` の「英語の事例動画」と手本に従って書く（英語、US発音の声、図は使わず表・手順で）
4. `python scripts/video.py usecase-<slug>-en --slides` でスライドだけ作り、文字のはみ出しや折り返しを1枚ずつ見て直す（動画の生成と投稿は GitHub 側で行うので、ここでは作らない）
5. ブランチ `video-en/<日付>` を作って台本をコミットし、プッシュしてプルリクエストを出す。説明欄に、題名・もとの事例・主な出典・要確認を書く
6. 英語チャンネルへの投稿は、利用者がプルリクエストを確認・マージしたあと、Actions の video ワークフローで `video_id: usecase-<slug>-en`、`channel: en`、`privacy: unlisted` を実行する（限定公開で上がり、公開は利用者が切り替える）
7. 作った本数と題名、プルリクエストのURLを短く報告する

## 公開前の点検（どの記事にも共通）

記事を書いたら、プルリクエストを出す前に必ず実行する。

1. `python scripts/verify.py <書いた記事のファイル>` を実行する
2. 「止める」が出たら、直してからやり直す。直せないときは、その記事を出さずに報告する
3. 「印」のうち「出典の番号がない数字」は、1つずつ出典と照らし合わせる。出典にあれば番号を付ける。なければ消すか【要確認】を付ける
4. 残った「印」の一覧を、プルリクエストの説明欄に貼る（人が見るのは、この一覧だけで済むようにする）
5. note用のフォルダには、`patterns/outputs/sns.md` の型で `sns.md` も作る

プルリクエストでは、同じ点検が自動で動く（`.github/workflows/check.yml`）。失敗していたら直す。

## 守ること

- 出典のない数字、仕様、金額、事例を書かない。確認できなければ【要確認】を付け、章末に理由を書く
- `material` に書かれた現場のメモは、最優先の素材として使う。書かれていない事例を作らない
- 変わりやすい値は `_variables.yml` に置き、本文では `{{< var ... >}}` で参照する
- 特定の事業者やサービスを勧めない
- 他者の資料の文章や図をそのまま使わない
- 公開されている金額（官公庁の事業費、公式サイトの料金、発表された契約額）は、出典、年度、条件を添えて書いてよい。見積もり、非公開の価格表、有料の報告書の中身、顧客名、会員の情報は書かない（公開リポジトリのため）
- main に直接書き込まない。必ずプルリクエストにする

## 頼まれ方の例

- 「survey の未作成の章を2つ作って」
- 「survey-subsidence を infra_owner 向け、overview の深さで作り直して」
- 「survey-road-slope-screening から研修スライドとワークブックを作って」
- 「survey-subsidence の図を増やして」→ `figures/survey-subsidence.yaml` に足す
- 「デザインを変えて」→ `design/` の3ファイル（PDF、サイト）と `scripts/figures.py`（図）の色をそろえて直す
- 「example-custom の講座を1冊にまとめて」→ `python scripts/build.py course example-custom`
- 「新しい分野（水道）の章立てを提案して」→ `syllabus/water.yaml` と `courses/water.yaml` の案を出す
