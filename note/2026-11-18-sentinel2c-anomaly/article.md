# 無償の光学衛星Sentinel-2Cに機上の異常、11月17日08時25分（世界時）以降の観測データが取り戻せず。衛星データで作付け確認や遊休農地の判定をする側は、相棒の2Bだけになる期間をどう扱うか

（note用の下書き。見出し画像は thumbnail.png、図は fig-1.png と fig-2.png を使う）

欧州宇宙機関（ESA）が運用する無償の光学衛星Sentinel-2Cで、衛星に積んだ機器の異常（onboard anomaly）が起き、2026年11月17日08時25分（世界時、日本時間では同日17時25分）以降に取得したすべての衛星データが、取り戻せない形で失われました[1]。ESAの運用情報サイトSentinel Onlineと、データの配布元Copernicus Data Space Ecosystem（CDSE）が、同じ日にこの通知を出しています[1][2]。通知の時点で異常は続いていて、その間の観測もさらに影響を受ける可能性があると書かれています[1][2]。原因と復旧の見込みは書かれていません。

この記事では、Sentinel-2の画像で作付けの確認、遊休農地の判定、生育診断を行う自治体・JA・農業法人と、その解析を請ける側の立場で、この通知から何が読めるかを整理します。

（ここに fig-1.png）

## 何が書かれているか

**失われたデータは、あとから取り戻せません。** 通知は「11月17日08時25分（世界時）以降に取得したすべてのデータの、取り戻せない損失」と書いています[1]。Sentinel-1Dで10月に起きた欠測と同じく、あとで再処理しても出てこないデータです。

**異常は通知の時点で続いていて、対策の途中です。** 「異常が続く間は、さらなる観測も影響を受けることがある」「軽減の措置を実施中」と書かれています[1][2]。復旧して通常運用に戻った時点で、あらためて知らせるとしています[1]。日付の約束はありません。

**どの撮影が欠けたかは、運用ダッシュボードで見られます。** 影響を受けた撮影（データテイク）の一覧は、Sentinelの運用ダッシュボードの「Events」のページに載るとしています[1]。通知の本文には、地域や軌道の一覧はありません。

**Sentinel-2Cは、2つの主力機のうちの1つです。** Sentinel-2は、同じ軌道に180度離れて並ぶ2機で運用する設計で、2機そろって赤道で5日に1回、1機だけでは10日に1回の再訪になります[3][4]。Sentinel-2Cは2024年9月5日に打ち上げられ、2025年1月21日に初号機Sentinel-2Aと入れ替わって主力になりました[3][4]。いま主力の2機は2Bと2Cです[3]。

## 発注する側にとっての意味

**日本の上空では、しばらく2Bだけになる期間があり得ます。** 2Aは2025年3月から追加観測を続けていて、その期間は2027年末まで延びました[5]。ただし2Aは2Bから36度離れた位置に置かれ、追加観測で再訪を増やす対象として挙がっているのは、雲の多い欧州と、アフリカ・南米の熱帯域です[3]。日本の圃場を2Aがどれだけ撮っているかは、観測計画で確かめる必要があります。2Cが止まっている間は、同じ条件で撮れる間隔が、設計上は5日から10日に伸びると読めます[3][4]。これに雲の影響が重なるので、11月下旬に使える晴天の画像は、見込みより減る可能性があります。

**11月の農業の業務に、直接かかります。** 秋の遊休農地の判定、交付金の作付け確認の後期の照合、麦の出芽や裸地の確認は、この時期の画像を使います。「11月17日以降の画像で判定する」と仕様に書いている業務は、画像が届くまでの待ち時間を見直す必要があります[1]。

**解析を請ける側は、使った画像の衛星名を納品物に残す理由が1つ増えました。** Sentinel-2の製品名は「S2A_」「S2B_」のように衛星名で始まります[6]。どの衛星の、いつの画像を使ったかが納品物に書いてあれば、「11月17日以降の2Cの画像は入っていない」と、発注者が自分で確かめられます。

**無償データには、観測の約束がありません。** Sentinelの観測計画の基準文書（HLOP）は観測の方針を定めるものです[7]。欠測したときに代わりの撮影をする、という約束はどこにもありません。これは今回の異常に限らず、無償の衛星データを業務に組み込むときの前提です。

（ここに fig-2.png）

## 変わらないこと

- **11月17日より前の画像は、そのまま使えます。** 通知が対象にしているのは、17日08時25分（世界時）以降に取得したデータです[1]。すでに手元にある画像や、過去の時系列には影響しません
- **2Bの観測は、この通知の対象ではありません。** 2Bでは10月20〜22日に位置ずれの問題がありましたが、別の事象です[8]。今回の通知は2Cだけを対象にしています[1]
- **雲の制約は、衛星の数が戻っても残ります。** 日本の11月は晴天の日が限られます。衛星が2機でも、雲の下の圃場は見えません
- **原因と期間は、わかっていません。** 通知は「機上の異常」と書くだけで、原因と復旧の見込みを示していません[1][2]。長引くか、すぐ戻るかは、現時点では書けません
- **Sentinel-2が止まったわけではありません。** 失われたのは2Cの一部の期間のデータで、2Bと2Aの観測は通知の対象外です[1]

## 今、できること

1. **自治体・JAの担当**：11月17日以降の画像を使う予定の業務（遊休農地の判定、作付け確認の照合、麦の出芽の確認）を書き出し、画像が届くまでの待ち時間を1〜2週間ほど見直す。現地確認の日程を、画像の到着に合わせて動かせるようにしておく
2. **解析を請ける側**：手元の11月17日以降の画像のうち、製品名が「S2C_」で始まるものが納品物に入っていないかを確かめる[6]。運用ダッシュボードの「Events」で、対象地域の撮影が欠けていないかを見る[1]
3. **両者**：仕様書と報告書に、使った画像の衛星名と取得日時を書く欄を設ける。欠測が起きたときに、どの画像で判定したかを後から追えるようにする[6]
4. **両者**：Sentinel Onlineの続報を確かめる。復旧の通知が出れば、通常運用に戻った日付がわかる[1]

→ 本編：衛星データの分解能と撮影の間隔：Sentinel-2の画像を数え、使える枚数と対象の画素数を確かめる https://ssskobj-dev.github.io/eisei-kouza/learn/codex/codex-1-3-resolution-revisit.html

→ 本編：衛星データの時系列解析：Sentinel-2の1年分の植生指数を筆ごとに並べ、雲の日を除き、欠けた日をつながず、作物の暦と照らす https://ssskobj-dev.github.io/eisei-kouza/learn/codex/codex-2-11-time-series.html

→ 本編：無料の衛星データの入手：Sentinel-2とLandsatを場所と期間で探し、雲の割合で絞り、利用の条件を付けて保存する https://ssskobj-dev.github.io/eisei-kouza/learn/codex/codex-1-5-open-data-access.html

→ ユースケース集：遊休農地の調査で、現地に行く農地を衛星で絞る https://ssskobj-dev.github.io/eisei-kouza/casebook/yukyu-nochi-screening.html

→ ユースケース集：交付金の作付け確認を、衛星の「ずれ」で絞る https://ssskobj-dev.github.io/eisei-kouza/casebook/sakutsuke-check.html

→ 時事解説：Sentinel-2Aの追加観測が2027年末まで延長 https://ssskobj-dev.github.io/eisei-kouza/news/2026-10-13-sentinel2a-extension.html

→ 時事解説：無償の光学衛星Sentinel-2B、10月20〜22日の画像に大きな位置ずれ https://ssskobj-dev.github.io/eisei-kouza/news/2026-11-04-sentinel2b-geolocation.html

→ 時事解説：無償の衛星Sentinelの観測計画の基準文書（HLOP）が第4版に https://ssskobj-dev.github.io/eisei-kouza/news/2026-11-16-sentinel-hlop4.html

## 出典

1. ESA Sentinel Online「Copernicus Sentinel-2C Data Unavailability on 17 November 2026」（2026年11月17日） https://sentinels.copernicus.eu/web/sentinel/-/copernicus-sentinel-2c-data-unavailability-on-17-november-2026
2. Copernicus Data Space Ecosystem「Copernicus Sentinel-2C Data Unavailability on 17 November 2026」（2026年11月17日） https://dataspace.copernicus.eu/news/2026-11-17-copernicus-sentinel-2c-data-unavailability-17-november-2026
3. ESA SentiWiki「S2 Mission」（解説ページ。衛星の体制、再訪、打ち上げ日、2Aの追加観測） https://sentiwiki.copernicus.eu/web/s2-mission
4. Copernicus Data Space Ecosystem「Sentinel-2」（解説ページ。再訪、2Cの運用開始日） https://documentation.dataspace.copernicus.eu/Data/SentinelMissions/Sentinel2.html
5. Copernicus Data Space Ecosystem「Sentinel-2A Extension Campaign to Continue Until the End of 2027」（2026年10月9日） https://dataspace.copernicus.eu/news/2026-10-9-sentinel-2a-extension-campaign-continue-until-end-2027
6. ESA SentiWiki「S2 Products」（製品名の規則） https://sentiwiki.copernicus.eu/web/s2-products
7. Copernicus Data Space Ecosystem「Sentinel High Level Operations Plan updated to version 4.0」（2026年11月12日） https://dataspace.copernicus.eu/news/2026-11-12-sentinel-high-level-operations-plan-updated-version-40
8. Copernicus Data Space Ecosystem「Temporary Geolocation Issue Affecting Sentinel-2B Products」（2026年11月3日） https://dataspace.copernicus.eu/news/2026-11-3-temporary-geolocation-issue-affecting-sentinel-2b-products

## 要確認

公開前に、原文と照合してください。

- **続報の有無**：この下書きは2026年11月18日（日本時間）早朝の時点の通知に基づいています。公開前に、出典1・2のページと Sentinel Online の新着に、復旧の通知や更新（原因、復旧日時、影響を受けた撮影の一覧）が出ていないか確かめてください。出ていれば、冒頭と「変わらないこと」の「原因と期間は、わかっていません」を書き換えてください
- 「11月17日08時25分（世界時）以降に取得したすべてのデータの、取り戻せない損失」「異常が続く間は、さらなる観測も影響を受けることがある」「軽減の措置を実施中」「復旧後にあらためて知らせる」「影響を受けた撮影は運用ダッシュボードのEventsに載る」は、出典1・2の英文（unrecoverable loss of all data acquired since 17 November 2026 at 08:25 UTC／Further acquisitions may be affected while the anomaly persists／Mitigation measures are being implemented）の、この記事での訳です
- 日本時間「同日17時25分」は、世界時08時25分からこの記事で換算しました（＋9時間）
- 「2機で赤道5日、1機で10日の再訪」「180度離れて並ぶ」は出典3・4の記載です。日本（中緯度）の実際の再訪は軌道の重なりで短くなり、出典4は中緯度で2〜3日と書いています。本文の「5日から10日に伸びる」は、設計上の数字で書いています
- 「2Cは2024年9月5日打ち上げ、2025年1月21日に2Aと入れ替わって運用」「2Aは2Bから36度離れた位置」「追加観測で再訪を増やす対象は欧州とアフリカ・南米の熱帯域」は出典3の記載です。2Aの追加観測が日本をどれだけ撮っているかは、この記事では確かめていません。「観測計画で確かめる必要がある」と書いています
- 「2Aの追加観測は2027年末まで」は出典5の記載です
- 「製品名は衛星名で始まる（S2A_、S2B_）」は出典6の記載です。出典6の例示には S2C はありませんが、同じ規則で「S2C_」が付きます。原文の表記を確かめてください
- 「HLOPは観測の方針を定めるもので、欠測時の代わりの撮影を約束するものではない」は、出典7の記載からの、この記事での読みです。原文にそのままの文はありません
- 「2Bの10月20〜22日の位置ずれ」は出典8の記載です
- 「秋の遊休農地の判定、作付け確認の後期の照合、麦の出芽の確認」「待ち時間を1〜2週間ほど見直す」は、読者の業務に当てはめたこの記事での補足で、出典にはありません。1〜2週間は、再訪が5日から10日に伸びることと雲の影響を踏まえた目安です
- 「Sentinel-1Dで10月に起きた欠測と同じく」は、この記事の過去回（2026年10月30日）を指しています
- この下書きは、原文を機械で読み取った内容をもとに書いています。数字と言い回しを原文で確かめてください
