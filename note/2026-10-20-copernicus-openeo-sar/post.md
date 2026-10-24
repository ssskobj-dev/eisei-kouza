コペルニクスの公式クラウドに、SARで収穫の時期と地盤の動きを読む手順が公開。無償で、どこまでできるか

欧州の地球観測計画コペルニクスの公式データ基盤「Copernicus Data Space Ecosystem」が、2026年10月14日と15日に、レーダー衛星 Sentinel-1 のデータを使う解析の手本を2本公開しました[1][2]。1本目は、作物の収穫の時期を広い範囲で見つける手順です[1]。2本目は、地震で地面がどれだけ動いたかを求める手順です[2]。

どちらも、openEO という仕組みで動きます。重い計算はデータのある基盤の側で行い、手元には結果の数値だけを受け取ります[1][2]。衛星の生データを自分の計算機に落として、専門のソフトで処理する必要がない、ということです。

<<IMG: fig-1.png>>

## 何が書かれているか

**収穫の時期は、レーダーの「似ている度合い」の変化で読みます。** 2回の観測がどれだけ似ているかを示す値（コヒーレンス）は、作物が立っていた畑が収穫後に裸の土になると、大きく上がります。手本は、この急な上昇を探して、起きた時期を地図にします[1]。しきい値は使う側が変えられます。ただし発表元は、しきい値による信号はほかの地表の変化にも反応する、と書いています[1]。

**地盤の動きは、2016年のイタリアの地震を例にしています。** 6日間隔のSentinel-1のペアから、干渉画像と、それをほどいた位相、コヒーレンスを基盤の側で作ります。手元では、位相を衛星の視線方向の動きに換算し、信頼の低い画素を除いて、画素ごとの動きの傾向を求めます[2]。

**どちらも「試す段階」と明記されています。** 収穫の手本は、結果は探索的で、業務で使う前に現地の観測や参照データと照合すること、と書いています[1]。地震の手本は、求めた傾向は手順を示すためのもので、確定した地盤の速度ではない、と書いています[2]。仕組みの一部（CWL）は実験的で、使える基盤が限られます[1][2]。

## 発注する側にとっての意味

**「SARの干渉解析は専門ソフトと大きな計算機が要る」という前提が、少し変わります。** 無償データの公式基盤の上で、処理の手順が読める形で公開されました[1][2]。技術者がいる組織なら、事業者の提案を受ける前に、自分の地域の小さな範囲で同じ手順を動かしてみることができます。

**JAや農業法人には、収穫の時期の把握が関係します。** 雲や夜に左右されないレーダーで、広い範囲の畑の収穫の時期を一度に見る手順です[1]。出荷の計画や、作付けと収穫の確認の下調べに向く、と読めます。

**測量・建設コンサルとインフラ管理者には、地震後の変位の手順が関係します。** 事業者から干渉SARの成果を受け取るとき、どの処理を経た数字なのかを比べる物差しになります[2]。

**無償は「小さく試すのは無料」の意味です。** 一般のアカウントには、毎月1万クレジットが無料で付きます。足りなければ購入します[4]。同時に動かせる処理は2つまでです[3]。広い範囲を毎月回す業務では、費用の見積もりが要ります。

<<IMG: fig-2.png>>

## 変わらないこと

- **収穫以外の変化も拾います。** 発表元が自分で書いているとおり、コヒーレンスの急な上昇は、ほかの地表の変化にも反応します[1]。現地の記録と突き合わせる作業は残ります
- **干渉SARの限界は、クラウドでも同じです。** 地震の手本は、ノイズ、大気の影響、コヒーレンスの低下、視線方向の幾何に敏感で、業務で使うには検証と、より完全な処理の方針が要る、と書いています[2]
- **結果の検証は、使う側の仕事です。** 手本は手順を示すもので、精度を保証するものではありません[1][2]。日本の畑や地形で同じように読めるかは、別に確かめる必要があります

## 今、できること

- 技術者がいる組織は、無料のアカウントで、自分の地域の小さな範囲で収穫の時期の手本を動かし、現地の記録と並べてみる
- 干渉SARの提案を受けたら、どのデータから、どの処理を経て、何と照合したかを聞き、公開された手順と比べる
- 仕様書に、検証の方法（現地の観測との照合）と、しきい値などの条件の提示を求める

無償の衛星データの入手の仕方と、無償でも付く条件は、講座の本編で詳しく書いています。Sentinelの衛星の早見表と、成果物の品質の確かめ方もあわせて読めます。

→ 本編：データの入手方法と費用の考え方 https://ssskobj-dev.github.io/eisei-kouza/learn/common/common-data-cost.html

→ Sentinelで見られるユースケースと解析手法 https://ssskobj-dev.github.io/eisei-kouza/learn/sentinel.html

→ 本編：成果物の品質確認と、顧客への説明 https://ssskobj-dev.github.io/eisei-kouza/learn/survey/survey-quality-explain.html

## 出典

1. Copernicus Data Space Ecosystem「New openEO Community Example: Detect Harvest Timing with Sentinel-1 SAR Coherence」（2026年10月14日） https://dataspace.copernicus.eu/news/2026-10-14-new-openeo-community-example-detect-harvest-timing-sentinel-1-sar-coherence
2. Copernicus Data Space Ecosystem「New openEO Community Example: Analyse Earthquake-Induced Deformation with Sentinel-1 Interferograms」（2026年10月15日） https://dataspace.copernicus.eu/news/2026-10-15-new-openeo-community-example-analyse-earthquake-induced-deformation-sentinel-1
3. Copernicus Data Space Ecosystem Documentation「openEO」（Free tier limitations の節） https://documentation.dataspace.copernicus.eu/APIs/openEO/openEO.html
4. Copernicus Data Space Ecosystem Documentation「Credit usage」 https://documentation.dataspace.copernicus.eu/APIs/openEO/credit_usage.html
