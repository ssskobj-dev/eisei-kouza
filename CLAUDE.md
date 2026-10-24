# このリポジトリでの作業ルール（Claude向け）

Satellite to Decisionの教材を作るリポジトリ。章立てとパターンから原稿を生成する。

## サイトの構造

| フォルダ | シリーズ | 中身 |
|---|---|---|
| `landscape/` | 市場レポート | テーマごとのフォルダに、切り口ごとに1本 |
| `casebook/` | ユースケース集 | 1件につき1本 |
| `learn/` | 学習プログラム | 講座の章（`learn/<分野>/`）とケース問題（`learn/quiz/`） |
| `themes/` | テーマから探す | 自動で作られる。手で書かない |

- シリーズの名前は `_variables.yml` の `series`、テーマは `data/themes.yaml` にある
- 各シリーズの入口（`index.qmd`）、講座のページ（`learn/course-*.qmd`）、`themes/` は `python scripts/build.py nav` が作る。手で書かない、コミットしない
- 記事の「関連する記事」には、最初にテーマのページへのリンクを置く
- 「Sentinelで見られるユースケースと解析手法」（`learn/sentinel.qmd`）も `nav` が作る。もとは `data/sentinel_methods.yaml`（手法の説明と、`data/usecases.yaml` の番号）。手法やユースケースを足すときは、この yaml を直す。数字と仕様には出典の番号を付ける
- 英語版は固定ページだけ（`en/` の下）。`en/index.qmd`、`en/about.qmd`、`en/register.qmd` は手で書く。各シリーズの入口とSentinelの早見表の英語版は `nav` が作る（英語の文は `data/sentinel_methods_en.yaml` と `scripts/build.py` の `english_pages`）。日本語の固定ページを直したら、英語版も合わせて直す。記事は英語にしない
- メニューの英語化、言語の切り替え、有料登録のボタン、押下の記録は `design/track.html`。訪問者数の計測は `design/analytics.html`（Google Analytics 4、同意した人だけ）
- **無料と有料の線**：ユースケース集は全文無料。市場レポートは前半が無料、後半が有料。講座の章は最初の3分の1が無料。Sentinelの早見表は最初の節だけ無料。ケース問題と時事解説は全部無料。切り分けは `design/paywall.lua` が行い、有料の範囲は公開するサイトに出ない（各フォルダの `_metadata.yml` で指定）。記事は全文を書く。PDF、サイト内の検索、一覧の絞り込み、「テーマから探す」は有料版の機能なので、公開するサイトでは作らない
- **noteへの出し方**（シリーズごとに違う。`notefull` が自動で作り分ける）
  - ユースケース集：**全文を公開**（`note/usecase-<slug>/full.md`）
  - 市場レポート：**前半だけ**出し、「ここから先は有料です」とサイトへの誘導を付ける（`note/report-<テーマ>-<切り口>/full.md`）
  - 講座の章：**noteには出さない**（サイトだけ。note用のフォルダも作らない）
  - ユースケース集か市場レポートを書いたら、`python scripts/build.py notefull` を実行し、できた `full.md` も一緒にコミットする
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
9-2. 「公開前の点検」の手順を行う（`python scripts/verify.py`）。**講座の章は note に出さないので、note用のフォルダ（`note/<id>/`）は作らない。`notefull` も実行しない**
10. ブランチ（毎朝の自動実行では `learn/<日付>`）を作ってプルリクエストを出す。説明欄に、章ごとの「要確認」の件数と内容、点検の「印」の一覧を書く

### 毎朝の自動実行で作る章の順番

1回に2章まで。**資格の教材を先に揃える**（衛星データマーケッター2級 → その他）。次の順で、`status: todo` のものを上から選ぶ。`codex-*`（解析教材）は別のタスク「解析教材の章の作成」が作るので、このタスクでは飛ばす。`status: hold` の章は作らない（順番待ち）。全部終わったら、`python scripts/build.py todo` の順に進む。

1. `marketer-read-results`（解析結果の読み方）
2. `marketer-accuracy-field-check`（精度の条件と、現地確認の役割）
3. `marketer-policy-procurement`（制度と国の調達の方針）
4. `marketer-workflow-fit`（業務の流れのどこに入れ、何を決める材料にするか）
5. `marketer-market-proposal`（市場の動きと提案の筋）
6. 残りの `survey-*`、`agri-*`、`common-*` の todo
7. マーケッター2級が揃ったら（`python scripts/build.py cert` で 2級 が全部 ○）、`syllabus/marketer.yaml` の1級（`hold`）を `todo` に変えてから続ける

### 「解析教材の章を作って」と頼まれたら（毎朝の自動実行「解析教材の章の作成」も同じ）

衛星データ解析エンジニアの教材（`syllabus/codex.yaml`、章の型 `codex`）。上の「未作成の章を作って」と同じ手順で、次の点だけ違う。

- 対象は `codex-*` の `status: todo` だけ。`courses/codex.yaml` の並び順（第0部から）に作る。1回に2章まで
- **テキストベース**：コードは「AIへの指示文」と「誤りを仕込んだ抜粋（10行以内、擬似コードでよい）」で示す。実行環境を前提にしない。動くことを保証する文を書かない
- 衛星の仕様（波長帯の番号、処理の段階の名前）は公式資料で確かめて出典を付ける。確かめられなければ【要確認】
- 図は `figures/<id>.yaml` に1〜2枚（しくみの図、おかしな結果の例）
- ケース問題（`learn/quiz/<id>.qmd`）は、誤りを仕込んだコードか結果から問題を見つける形で、四肢択一1問＋短答1問
- 2級（第0〜3部）が揃ったら（`python scripts/build.py cert`）、`syllabus/codex.yaml` の1級（`hold`）を `todo` に変えてから続ける
- ブランチは `learn/<日付>-codex`

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
6. 英語チャンネルへの投稿は自動。台本が main に入ると、`video` ワークフロー（毎時の見回り）が未投稿の台本を見つけて動画を生成し、英語チャンネルに**公開（public）**で投稿する。こちらから投稿操作はしない
7. 作った本数と題名、プルリクエストのURLを短く報告する

## 「今日の英語の市場レポート動画を作って」と頼まれたら（毎朝の自動実行も同じ）

1. `python scripts/build.py enreports` で、作る候補（海外向けの切り口で英語動画が未作成）を確かめる。1回に1本。無ければ作らず報告して終わる
2. 先頭の候補を1つ選ぶ。その切り口の `sources`（`patterns/report_angles.yaml`）が指す `data/market-report-2026-10/` の章を下調べとして読む
3. **出典の原文を開いて、数字・年・出どころを確かめる**。下調べメモの数字をそのまま写さない。確かめられない数字は台本から外す（字幕には出さない）。足りなければ公的資料や発表元を探す
4. `video/report-<テーマid>-<切り口>-en/script.yaml` を、`patterns/outputs/video.md` の「英語の市場レポート動画」と手本に従って書く（英語、US発音の声、`series: MARKET`、図は使わず表・手順・箇条書きで）
5. `python scripts/video.py report-<テーマid>-<切り口>-en --slides` でスライドだけ作り、文字のはみ出しや折り返しを1枚ずつ見て直す
6. ブランチ `video-en/<日付>` を作って台本をコミットし、プッシュしてプルリクエストを出す。説明欄に、題名・切り口・確かめた主な出典（原文のURL）・確かめられず外した数字を書く
7. 英語チャンネルへの投稿は自動。台本が main に入ると、`video` ワークフロー（毎時の見回り）が未投稿の台本を見つけて動画を生成し、英語チャンネルに**公開（public）**で投稿する。こちらから投稿操作はしない
8. 作った本数と題名、プルリクエストのURLを短く報告する

## 「今日の日本語の講義動画を作って」と頼まれたら（毎朝の自動実行も同じ）

1. `python scripts/build.py javideos` の「講義動画」で、作る候補（公開済みの章で、動画が未作成）を確かめる。1回に1本。無ければ作らず報告して終わる
2. 先頭の候補を1つ選ぶ。章の原稿（`learn/<シリーズ>/<章のid>.qmd`）、同じ章のケース問題（`learn/quiz/<章のid>.qmd`）、章の図（`figures/<章のid>.yaml`）を読む。`{{< var >}}` の値は `_variables.yml` で確かめる
3. `video/lecture-<章のid>/script.yaml` を、`patterns/outputs/video.md` の「日本語の講義動画」「題名（SEO）と、資格の案内」と手本に従って書く（もち子の声、「一緒にやってみよう」と「宿題」を必ず入れる。題名はキーワードを先頭近くに・40字以内。資格の案内は自動で最後に入る）
4. `python scripts/video.py lecture-<章のid> --slides` でスライドだけ作り、文字のはみ出しや折り返しを1枚ずつ見て直す（動画の生成と投稿は GitHub 側で自動）
5. ブランチ `learn/<日付>-video` を作って台本をコミットし、プッシュしてプルリクエストを出す（講座の章から作るので `learn/` の下。自動マージの対象）。説明欄に、題名・もとの章・宿題に使ったケース問題を書く。マージ（自動）後、日本語チャンネルに public で投稿される
6. 作った本数と題名、プルリクエストのURLを短く報告する

## 「今日の日本語の事例動画を作って」と頼まれたら（毎朝の自動実行も同じ）

1. `python scripts/build.py javideos` の「事例動画」で、作る候補（公開済みの記事で、動画が未作成）を確かめる。1回に1本。無ければ作らず報告して終わる
2. 先頭の候補を1つ選ぶ。記事（`casebook/<slug>.qmd`）と `data/usecases.yaml` の行、図（`figures/<slug>.yaml`）を読む。`source_url` を開いて、事例・数字・費用を確かめる
3. `video/usecase-<slug>/script.yaml` を、`patterns/outputs/video.md` の「日本語の事例動画」「題名（SEO）と、資格の案内」と手本に従って書く（もち子の声。題名はキーワードを先頭近くに・40字以内。資格の案内は自動で最後に入る）
4. `python scripts/video.py usecase-<slug> --slides` でスライドだけ作り、文字のはみ出しや折り返しを1枚ずつ見て直す
5. ブランチ `casebook/<日付>-video` を作って台本をコミットし、プッシュしてプルリクエストを出す（事例記事から作るので `casebook/` の下。自動マージの対象）。説明欄に、題名・もとの事例・主な出典を書く。マージ（自動）後、日本語チャンネルに public で投稿される
6. 作った本数と題名、プルリクエストのURLを短く報告する

## 公開前の点検（どの記事にも共通）

記事を書いたら、プルリクエストを出す前に必ず実行する。点検は緩め。主軸は**マーケティング効果**（`patterns/style.md` の4項目）。

1. `python scripts/verify.py <書いた記事のファイル>` を実行する
2. 「止める」が出たら、直してからやり直す。止まるのは、書きかけ・崩れる記法と、マーケティングの4項目を1つ以下しか満たさない記事だけ
3. 「マーケティング点検 n/4」の印が出たら、足りない項目を直して 4/4 にする（冒頭の結論、具体的な数字、持ち帰れる行動、具体的な題名）
4. 残った「印」（出典の形の崩れ、出典の番号がない数字など）は、気づいた範囲で直す。直せなくても公開は止めない
5. 「印」の一覧を、プルリクエストの説明欄に貼る
6. note に出す記事（ユースケース集、市場レポート、時事解説）は、note用のフォルダに `patterns/outputs/sns.md` の型で `sns.md` も作る。**講座の章は note に出さないので不要**

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
