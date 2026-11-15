# 無償の衛星Sentinelの観測計画の基準文書（HLOP）が第4版に。欧州以外のレーダー観測は「12日に1回・片方向」が基本。衛星データで地盤変位のインフラ監視を頼む側は、観測の頻度の約束をどう確かめるか

（note用の下書き。見出し画像は thumbnail.png、図は fig-1.png と fig-2.png を使う）

欧州の地球観測計画コペルニクスのデータ配布サイト（Copernicus Data Space Ecosystem）が2026年11月12日に、Sentinel衛星の運用の基準となる文書「Sentinel High Level Operations Plan（HLOP）」の第4版（Issue 4.0）が公開された、と知らせました[1]。文書そのものの日付は2026年9月15日です[2]。HLOPは、Sentinel-1（レーダー）、Sentinel-2（光学）などの衛星ごとに、どの地域を、どのくらいの頻度で、どの観測モードで撮るかという「観測の方針」を定めた文書で、衛星の構成の変化や利用者の要望に合わせて更新されます[1]。

第4版の中身は、2025年の見直しの結果として、Sentinel-1とSentinel-2の観測シナリオを更新したものです[2]。日本の読者にとって要点は1つです。Sentinel-1のレーダー観測は、欧州では6日ごとに上昇・下降の両方向で撮りますが、欧州以外の陸地では「2機のうち1機で、12日ごとの干渉SAR向けの再観測」が基本の目標とされています[2]。日本は後者に入ります。

この記事では、無償のSentinel-1で地盤変位や災害の監視を頼む側、受け取る側の立場で、この文書をどう使うかを整理します。

（ここに fig-1.png）

## 何が書かれているか

**Sentinel-1の観測は、今は1Cと1Dの2機で続けられています。** 文書は、時系列の連続性を保つため、観測シナリオを現在はSentinel-1CとSentinel-1Dで維持している、と書いています[2]。2機は同じ軌道に180度離れて置かれ、2機の星座（コンステレーション）として6日の回帰周期になります[2]。衛星1機あたりのレーダーの稼働時間の上限は、1A・1Bが合計25分だったのに対し、1C・1Dは30分です[2]。

**欧州以外の陸地は「12日ごと・1機」が基本です。** より優先度の高い観測の方針に含まれない陸地は、干渉幅観測（IW）のVV+VH偏波で定常的に撮られ、「2機のうち1機を使って12日ごとの干渉SAR向けの再観測を提供する」のが基本の目標です[2]。地震や火山の地域についても、欧州では上昇・下降の両方向を毎回撮って6日の干渉SARができるようにする一方、「欧州の外では、基本の観測計画は12日ごとの干渉SAR向けの再観測を確保する」とされています[2]。最近の地震や噴火の影響を受けた地域など、選ばれた優先度の高い地域では、能力の範囲で両方向や6日ごとの観測が行われることがあります[2]。

**観測の計画は、地図とファイルで公開されています。** 観測シナリオは、観測モード、偏波、上昇・下降、再観測の間隔を示す地図の形で公開され、実際の観測の区切り（日時、軌道）はKML形式のファイルとしてSentinel-1、Sentinel-2それぞれの観測計画のページで公開されます[1][2]。観測シナリオは定常運用の中で変わっていくことが見込まれ、日々の変更はESAの裁量で行われる、とも書かれています[2]。

**光学のSentinel-2は、2Bと2Cが基本の構成です。** 2機で5日の回帰周期、中緯度では2〜3日で撮れる、とされています[2]。退役を延ばしているSentinel-2Aは「例外的な一時的な延長の観測」と位置づけられ、文書の時点では2026年12月31日まで、欧州と熱帯のアフリカ・南米は10日ごと、それ以外の地域は20日ごとの再観測です[2]。この延長はその後、2027年末まで延ばすと10月9日に発表されています（10月13日の時事解説で取り上げました）[3]【要確認】。文書の日付は9月15日なので、この延長は反映されていません。

## 発注する側にとっての意味

**「無償のSentinel-1で監視」と書く提案は、日本では「12日に1回、片方向」が前提です。** 日本は文書でいう「欧州の外」です[2]。1地点について、1つの観測方向で12日ごとのデータが基本であり、欧州のような6日ごと・両方向の観測は約束されていません[2]。月に2〜3回の観測で地盤の動きの傾向を追うには十分でも、動きの向きを東西と上下に分けて知るのに要る両方向のデータや、災害直後に数日おきで追う観測は、基本の計画の外です。

**観測の頻度は、文書と計画ファイルで確かめられます。** 「Sentinel-1でどのくらいの頻度で撮れますか」という問いに、事業者の経験で答えてもらう必要はありません。HLOPの観測シナリオの地図と、KMLの観測計画で、自分の対象地域が、どの方向で、何日ごとに撮られる予定かを見られます[1][2]。提案書に書かれた頻度が、この公開された計画と合っているかを、発注する側が自分で確かめられる、という意味です。

**大きな地震のあとに観測が増えることはあっても、約束ではありません。** 文書は、最近の地震や噴火の影響を受けた地域などで、能力の範囲で観測を増やすことがある、と書いています[2]。「能力の範囲で」「選ばれた地域」という言い方なので、災害時の計画を無償データだけに頼る設計にはできません。国内の「だいち」や商用のレーダー衛星と組み合わせる前提で、役割分担を決めておくことになります。

**文書は「その時点の方針」で、最新の状態ではありません。** 第4版の日付は9月15日で、Sentinel-2Aの延長の期限は10月の発表で変わっています[2][3]。文書で基本の方針を知り、変更はデータ配布サイトのお知らせと観測計画のファイルで追う、という2段構えが要ります。この講座の時事解説で取り上げてきた、Sentinel-1Dの観測の欠落や処理ソフトの差し戻しも、文書には出てこない日々の変更です。

（ここに fig-2.png）

## 変わらないこと

- **データが無償であることは変わりません。** 文書は観測の方針を定めるもので、配布の条件を変えるものではありません[1]
- **日本の基本の頻度は、第4版でも12日ごと・1機です。** 欧州の外の陸地の基本の目標は、12日ごとの干渉SAR向けの再観測です[2]。1Dが加わっても、欧州並みの6日ごと・両方向にはなっていません
- **観測されても、使えるかは別です。** 干渉SARには、植生や積雪、観測条件の制約があります。頻度は必要条件であって、十分条件ではありません
- **計画は変わります。** 観測シナリオは運用の中で変わることが見込まれ、日々の変更はESAの裁量です[2]。一度確かめた頻度を、そのまま翌年の仕様に書き写せません

## 今、できること

1. 無償のSentinel-1を前提にした監視の提案を受け取ったら、HLOPの観測シナリオの地図と、Sentinel-1の観測計画のKMLで、自分の対象地域の観測方向と間隔を確かめる[1][2]。提案書の「頻度」と合っているかを見る
2. 仕様書に観測の頻度を書くときは、「12日ごと・1方向」を基本の前提として書き、6日ごとや両方向が要るなら、その分は別の衛星で賄う設計にする[2]
3. 災害時の計画では、Sentinel-1の観測が増える「ことがある」を当てにせず、国内の衛星や商用の衛星との役割分担を先に決めておく[2]
4. データ配布サイトのお知らせを見る担当を決める。文書に反映されない変更（延長、欠落、処理ソフトの変更）は、お知らせで出ます[1][3]

→ 本編：衛星データの選び方と調達の実務 https://ssskobj-dev.github.io/eisei-kouza/learn/survey/survey-procurement.html

→ 本編：衛星データで地盤沈下を面で把握する：水準測量と組み合わせ、翌年の路線を決める https://ssskobj-dev.github.io/eisei-kouza/learn/survey/survey-subsidence.html

→ 本編：衛星データの分解能と撮影の間隔：Sentinel-2の画像を数え、使える枚数と対象の画素数を確かめる https://ssskobj-dev.github.io/eisei-kouza/learn/codex/codex-1-3-resolution-revisit.html

→ 時事解説：無償のレーダー衛星Sentinel-1D、10月26〜27日の観測データが取り戻せず https://ssskobj-dev.github.io/eisei-kouza/news/2026-10-30-sentinel1d-outage.html

→ 時事解説：Sentinel-2Aの追加観測が2027年末まで延長 https://ssskobj-dev.github.io/eisei-kouza/news/2026-10-13-sentinel2a-extension.html

## 出典

1. Copernicus Data Space Ecosystem「Sentinel High Level Operations Plan updated to version 4.0」（2026年11月12日） https://dataspace.copernicus.eu/news/2026-11-12-sentinel-high-level-operations-plan-updated-version-40
2. ESA「Sentinel High Level Operations Plan」Issue 4.0（COPE-S1OP-EOPG-PL-15-0020、2026年9月15日、PDF） https://sentiwiki.copernicus.eu/web/document-library （文書庫の「Sentinel High Level Operations Plan」）
3. Copernicus Sentinel Online「Sentinel-2A Extension Campaign to Continue Until the End of 2027」（2026年10月9日） https://sentinels.copernicus.eu/-/sentinel-2a-extension-campaign-to-continue-until-the-end-of-2027

## 要確認

公開前に、原文と照合してください。

- 公開の知らせの日付（2026年11月12日）、「the reference document for operating the Copernicus Sentinel missions」、観測の方針（どの地域を、どの頻度で、どのモードで）、更新の理由（衛星の構成の変化、利用者の要望、運用の教訓）、Sentinel-1・2の観測計画が別に公開されていることは、出典1の記載です
- 文書の日付（Date of Issue 15/09/2026）と文書番号、「Issue 4 provides further updates of the Sentinel-1 and Sentinel-2 observation scenarios」「as a result of the 2025 revision process」（1.2節）は、出典2の記載です
- 「The observation scenario is currently maintained with Sentinel-1C and Sentinel-1D」「in order to provide continuity of the time series」、180度（mean anomaly delta of 180 deg）、6日の回帰周期（4.3.2.2節）、稼働時間の上限（1A・1Bは合計25分、1C・1Dは30分。4.3.2.1節）は、出典2の記載です。25分・30分が「1周回あたり」の上限かどうかは、原文で確かめてください。本文では「衛星1機あたりの上限」とだけ書いています
- 「Land masses not covered by higher-priority observation strategies are routinely acquired in IWS VV+VH mode」「The baseline objective is to provide a 12-day interferometric revisit using one of the two satellites」（9.2.5節）、欧州の地震・火山地域は両方向で6日の干渉SAR、「Outside Europe, the baseline acquisition plan ensures 12 days interferometric revisit」、「selected high-priority areas, such as regions affected by recent earthquakes or volcanic eruptions」（9.2.6節）は、出典2の記載です。「能力の範囲で」は、この節の趣旨を訳した言い方です。原文の語を確かめてください
- 観測シナリオが地図（モード、偏波、上昇・下降、再観測の間隔）とKMLで公開されること（9.3節）、「The observation scenario is anticipated to evolve during the course of routine operations」（9.1節）、「day-to-day routine changes during full operations will be done at the discretion of ESA」（8.4節）は、出典2の記載です
- Sentinel-2の基本の構成（2Bと2C。4.3.3.2節）、5日の回帰周期と中緯度で2〜3日、Sentinel-2Aの「exceptional」「temporary extension campaign」、2025年3月13日からの延長、文書の時点で2026年12月31日まで、欧州と熱帯のアフリカ・南米は10日ごと、それ以外は20日ごと（10.3節）は、出典2の記載です
- 【要確認】Sentinel-2Aの延長が2027年末まで延びたこと（出典3、2026年10月9日）は、10月13日の時事解説で確かめた内容を引いています。この下書きを作る環境からは出典3のページを開き直せませんでした。公開前に出典3を開いて確かめてください
- 「日本は欧州の外に入る」は、文書の区分（欧州と欧州の外）からの読みです。文書は日本について個別には書いていません。日本の個別の観測計画は、観測シナリオの地図とKMLで確かめてください
- 「月に2〜3回の観測で傾向を追うには十分」「動きの向きを分けて知るには両方向のデータが要る」「国内の衛星や商用の衛星と組み合わせる」は、この記事での読みと助言で、出典にそのままの記述はありません。「干渉SARには植生や積雪、観測条件の制約がある」は、出典にはない一般的な補足です
- 出典2のアドレスは文書庫のページです。PDFへの直接のアドレスは長い識別子を含むので、文書庫から「Sentinel High Level Operations Plan」を開く形にしています
- この下書きは、原文（英語）を機械で読み取った内容をもとに書いています。数字と言い回しを原文で確かめてください
