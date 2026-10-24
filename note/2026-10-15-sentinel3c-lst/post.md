Sentinel-3Cが初画像を送信。無償の地表面温度は、暑さや渇きの監視にどこまで使えるか

欧州の地球観測計画コペルニクスの衛星 Sentinel-3C が、打ち上げ後の最初の画像と計測結果を送ってきました。2026年10月13日に、コペルニクスの公式サイトで公開されています[1]。

Sentinel-3Cは、2026年9月14日（現地時間）に南米の仏領ギアナからVega Cロケットで打ち上げられた、Sentinel-3シリーズの3機目の衛星です[2]。Sentinel-3は、海と陸の色、海面と地表の温度、海面の高さを測る衛星で、データは無償で公開されています[2]。

その前の10月7日には、Sentinel-3の「地表面温度」のデータが、専門のソフトなしにブラウザで見られるようになったことも発表されました[4]。この記事では、2つの発表をあわせて、農業や自治体の暑さ対策にどこまで使えるのか、何に使えないのかを整理します。

<<IMG: fig-1.png>>

## 何が書かれているか

**初画像は、色のセンサーと高度計から。** 海と陸の色を見るセンサー（OLCI）がイタリア、北極、カリブ海を撮り、レーダーで高さを測る高度計（SRAL）がグリーンランドの氷床と海面を計測しました[1]。

**役目は、古い衛星との交代です。** 先に飛んでいる Sentinel-3A（2016年打ち上げ）と 3B（2018年打ち上げ）は、どちらも設計寿命を超えて動いています[3]。3Cは、軌道上の試験の後に3Aの主な役目を引き継ぎ、2機体制を保ちます[3]。次の Sentinel-3D は2029年の打ち上げが見込まれています[3]。

**地表面温度が、ブラウザで見られます。** 温度を見るセンサー（SLSTR）から作る地表面温度のデータが、コペルニクスのブラウザで使えるようになりました。細かさは1kmで、観測は1日2回、現地の太陽時でおよそ10時と22時です。温度のほかに、不確かさ、雲の確率、植生の指標（NDVI）が入っています。用途として、農業、公衆衛生、水文（水の循環の把握）が挙げられています[4]。

## 発注する側にとっての意味

**無償の温度データの供給が、2030年代まで続く見通しになりました。** 3Cが3Aと交代し、3Dが2029年に続く計画です[3]。数年にわたって温度を見続ける業務を組むとき、データが途中で止まる心配が1つ減ります。

**提案を受ける前に、自分で見て試せます。** ブラウザで表示できるので[4]、自分の地域の温度の分布を、事業者の提案を受ける前に自分の目で確かめられます。

**使えるのは「面」の比較です。** 1kmの細かさは[4]、市町村の中で暑い所と涼しい所を比べる、地域の乾き具合の推移を見る、といった用途に向きます。1画素が1km四方なので、1枚の田や1本の道路の温度は分からない、と読めます。

<<IMG: fig-2.png>>

## 変わらないこと

発表元が自分で書いている限界が、3つあります。

- **地表面温度は、気温ではありません。** 欧州委員会の資料は「土壌の温度であり、気温と混同しないこと」と書いています[2]。データの説明も、気象のデータの気温とは別のものだと念を押しています[4]。熱中症の警戒に使う気温と、そのまま置き換えることはできません
- **雲の下は、雲の温度が出ます。** ブラウザの表示では雲を除く処理をしていないので、雲のかかった場所には雲の温度が表示されます[4]。一緒に入っている「雲の確率」で、信用できる画素を選ぶ必要があります
- **午後の最も暑い時間帯は、撮っていません。** 観測は現地の太陽時でおよそ10時と22時の2回です[4]。日中の観測は午前中なので、午後の高温の時間帯の値ではない、と読めます

もう1つ、Sentinel-3Cはまだ試験の段階です。欧州の気象衛星機関（EUMETSAT）による運用は、軌道上の試験が終わってからです[2]。初画像が公開されても、業務で使うデータが今すぐ変わるわけではありません。

## 今、できること

- コペルニクスのブラウザで、自分の地域の地表面温度を表示し、雲の確率と並べて、使えそうな日を見る
- 近くの気象観測所の気温と並べて、地表面温度との差を把握する。気温の代わりではなく、何の指標として使えるかを考える
- 温度データを使う提案を受けたら、衛星とセンサー、細かさ、観測の時刻、雲の扱いを仕様に書いてもらう

無償の衛星データの入手の仕方と、無償でも付く条件は、講座の本編で詳しく書いています。Sentinelの衛星の早見表もあわせて読めます。

→ 本編：データの入手方法と費用の考え方 https://ssskobj-dev.github.io/eisei-kouza/learn/common/common-data-cost.html

→ Sentinelで見られるユースケースと解析手法 https://ssskobj-dev.github.io/eisei-kouza/learn/sentinel.html

## 出典

1. Copernicus Sentinel Online「Sentinel-3C returns its first views of Earth」（2026年10月13日） https://sentinels.copernicus.eu/web/sentinel/-/sentinel-3c-returns-its-first-views-of-earth
2. 欧州委員会 防衛産業・宇宙総局「Countdown to Launch: Copernicus Sentinel-3C Takes Flight on 14 September」（2026年7月30日） https://defence-industry-space.ec.europa.eu/countdown-launch-copernicus-sentinel-3c-takes-flight-14-september-2026-07-30_en
3. 欧州連合宇宙プログラム庁（EUSPA）「OBSERVER: New satellite to carry the Copernicus Sentinel-3 record into the next decade」（2026年8月27日） https://eu-space.europa.eu/news/observer-new-satellite-carry-copernicus-sentinel-3-record-next-decade
4. Copernicus Sentinel Online「Sentinel-3 Level-2 Land Surface Temperature now available in Copernicus Browser」（2026年10月7日） https://sentinels.copernicus.eu/web/sentinel/-/sentinel-3-level-2-land-surface-temperature-now-available-in-copernicus-browser
