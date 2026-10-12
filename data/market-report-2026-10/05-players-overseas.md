# 第5章 海外の主要プレイヤー

（「衛星データ利活用市場レポート」2026年10月12日版からの抜き書き。下調べ用のメモで、表は崩れている。数字は必ず出典の原文で確かめる）

第5章

海外の主要プレイヤー

海外の衛星データ企業は、センサーの種類と「誰に売っているか」の2軸で整理すると全体像がつかめます。2025〜2026年は社名変更・買収・上場が相次ぎ、各社の成
長を支えているのは防衛と各国政府の需要です。

この章で学ぶこと
海外プレイヤーを6つのグループに分けて把握する方法
主要企業の衛星、分解能、直近の売上高や受注残
2023年以降の業界再編の流れと、防衛・政府需要への依存の実態
初心者がまず覚えるべき5社

5.1 プレイヤーの分類と全体像

海外プレイヤーは、衛星を持つ5グループと、衛星を持たない解析・プラットフォーム企業の計6グループに分けられます。前者は「上流（データをつくる側）」、後者は
「下流（データを使える形にする側）」と呼ばれます。
1. 高分解能光学の大手：30cm級の画像を撮る大型衛星を運用します。Vantor（旧Maxar Intelligence）、Airbusが代表です。
2. 小型光学コンステレーション：小型衛星を多数並べ、撮影頻度で勝負します。コンステレーション（constellation）とは、連携して動く衛星群のことです。
Planet、BlackSky、Satellogic、中国の長光衛星が該当します。
3. SAR：SAR（合成開口レーダー）は電波で地表を見るセンサーで、夜間や雲の下でも撮れます。ICEYE、Capella Space、Umbraが代表です。
4. 新センサー：ハイパースペクトル（光を数百の細かい波長帯に分けて物質を見分ける）、熱赤外（地表の温度を測る）、温室効果ガス（GHG）観測などです。Pixxel、
constellr、OroraTech、GHGSatが該当します。
5. RF・AIS・気象：画像ではなく電波を受信します。RFは無線信号の発信源の特定、AISは船舶が出す識別信号の受信です。HawkEye 360、Spire Globalが代表です。
6. 解析・プラットフォーム：Esri、Google Earth Engine、Microsoft Planetary Computer、Palantir、UP42、SkyFiなどです。

42 / 190


表5-1 海外の主要プレイヤー一覧（2026年10月時点で確認できた公開情報）
企業
Vantor

国
米

センサー種別
光学

主な衛星・機数
WorldView Legion 6機を含む光学10機

最高分解能
31cm

Airbus Defence and
Space
Planet Labs

欧

光学＋SAR

米

光学30cm、SAR
25cm
40cm級（Pelican）

BlackSky
Satellogic
ICEYE
Capella Space

米
米（アルゼンチン
発）
フィンランド
米

光学、ハイパースペク
トル
光学
光学

Pléiades Neo、Pléiades、SPOT、TerraSARXなど
SuperDove、SkySat、Pelican 10機、
Tanager
Gen-2、Gen-3 5機
NewSat

SAR
SAR

累計76機を打上げ
Acadiaなど軌道上9機

Umbra

米

SAR

Umbra-01〜12を打上げ

16cm
公開情報では今回未
確認
16cm

Pixxel

インド・米

ハイパースペクトル

Firefly 6機

HawkEye 360
Spire Global
長光衛星（Jilin-1）
China Siwei
（SuperView）
SIIS（KOMPSAT）
GHGSat

米
米
中
中

RF
気象、RF、航空
光学、動画
光学、SAR

30機超
2026年に29機を打上げ
117機（2025年8月時点）
14機

韓
加

光学、SAR
GHG（メタン）

KOMPSATシリーズ
12機（2024年10月時点）


35cm
50cm級

公開情報では今回未
確認
（画像ではない）
（画像ではない）
0.5m
公開情報では今回未
確認
30cm（KOMPSAT-7）
（濃度の計測）

特徴
旧Maxar Intelligence。米政府向けが
主力
光学とSARの両方を持つ欧州の大手
全陸域を毎日撮る。上場EO企業で売
上最大
高頻度の再訪とAI解析の即時配信
低コスト。衛星そのものの販売も行う
世界最大のSARコンステレーション
2025年にIonQが買収
データ販売に特化。オープンデータを
公開
2026年9月に1億ドルを調達
2026年5月にNYSE上場
海事事業を2025年に売却
サブメートル級で世界最大規模
国有の中国航天科技集団（CASC）系
韓国政府衛星の画像を商業販売
施設単位でメタン漏えいを特定

43 / 190


分解能は各社・公的機関の公表値で、撮影条件により変わります。機数は時点が異なるため、厳密な比較ではなく規模感をつかむために使ってください。
出典は章末の一覧と各節の本文に示します。
表の読み方

ポイント 分解能の数字だけで企業を比べないでください。「どれだけ細かく見えるか（分解能）」「どれだけ頻繁に撮れるか（再訪頻度）」「雲や夜でも撮れるか
（センサー種別）」の3点をセットで見ます。

5.2 光学衛星のプレイヤー

光学は「少数の大型衛星で最高画質を出す大手」と「多数の小型衛星で頻度を出す新興」に分かれますが、両者の境界は年々薄れています。新興側が30〜40cm級に上
がり、大手側は機数を増やしているためです。
Vantor（旧Maxar Intelligence、米国）
Vantorは、高分解能光学で最も長い実績を持つ企業です。前身のMaxarは2023年5月に投資ファンドのAdvent Internationalが64億ドルで買収し、同年9月に画像事業
（Maxar Intelligence）と衛星製造事業（Maxar Space Systems）に分割されました。2025年10月、前者がVantor、後者がLanterisへ社名を変え、Maxarの名前は消え
ました（Wikipedia）。Lanterisはその後、月着陸機のIntuitive Machinesが8億ドルで買収しています（Via Satellite、2026年1月）。
衛星は光学10機です。2024年5月〜2025年2月に打ち上げた新世代のWorldView Legion 6機（分解能34cm）と、WorldView-3（同31cm）などの既存機で構成されます
（Polar Geospatial Center）。非上場のため決算は公開されていません。資料を読むときは、2025年10月より前の文書では「Maxar」と書かれている点に注意してくだ
さい。
Airbus Defence and Space（欧州）
Airbusは、光学とSARの両方を自社で持つ欧州最大の事業者です。光学はPléiades Neo（30cm）、Pléiades（50cm）、SPOT（1.5m）の3階層です。SARはTerraSAR-X、
TanDEM-X、スペインのPAZなどを組み合わせ、25〜40cmの分解能を提供します（Airbus）。
次世代機のPléiades Neo Nextは20cm級で、初号機は2028年初めにVega Cロケットで打ち上げる予定です（Airbus、2026年1月）。また、Airbus、Leonardo、Thalesの
3社は宇宙事業を統合する計画を進めています。出資比率は35%、32.5%、32.5%、統合後の売上は約65億ユーロで、規制当局の承認を前提に2027年の稼働を目指して
います（Digital Watch）。
Planet Labs（米国、NYSE上場）

44 / 190


Planetは、地球の全陸域を毎日撮ることを目指す大規模な小型衛星群を運用し、上場している地球観測企業のなかで売上が最大です。2026年1月期（2025年2月〜2026
年1月）の売上は3億770万ドル（前年比26%増）でした。受注残（backlog、契約済みでまだ売上に計上していない金額）は9億40万ドルです（同社決算、2026年3
月）。直近の2026年5〜7月期は売上1億1,610万ドル（同58%増）で、通期見通しは4億3,000万〜4億4,100万ドルです（同社決算、2026年9月）。
表5-2 Planetの衛星シリーズ
シリーズ
SuperDove（PlanetScope）
SkySat
Pelican
Tanager
Owl

表の読み方

役割
全陸域の毎日撮影
高分解能の指定撮影
高分解能の指定撮影
ハイパースペクトル
SuperDoveの次世代

分解能
3〜4m級
公開情報では今回未確認
40cm級。次世代は最大30cm級
公開情報では今回未確認
1m級

状況
運用中。2025年11月に36機を追加
運用中。Pelicanが後継
軌道上10機（2026年7月時点）
2号機を打上げ場へ出荷済み
実証機を2026年末に打上げ予定

上の行ほど「広く・頻繁に」、Pelicanは「狭く・細かく」撮る衛星です。出典はPlanet（2025年11月）、NextBigFuture（Owl発表の報道）、上記の決算資料

です。
成長の原動力は「衛星サービス」と呼ぶ新しい契約形態です。画像を売るのではなく、顧客専用の衛星や撮影容量をまるごと提供します。日本のスカパーJSATとは2億
3,000万ドルの契約を結び（Via Satellite）、その後ドイツ、スウェーデンとも同種の契約を結びました。
BlackSky（米国、NYSE上場）
BlackSkyは、同じ場所を1日に何度も撮る「高頻度」と、撮影からAI解析までの速さを売りにしています。2025年の売上は1億660万ドル（前年比約4%増）、受注残は3
億4,500万ドルでした（同社決算、2026年2月）。2026年4〜6月期は売上3,330万ドル（同50%増）に加速し、通期見通しは1億3,000万〜1億5,000万ドルです（同社決
算、2026年8月）。新世代のGen-3衛星（分解能35cm）は2026年9月に5機目が稼働しました（defence-industry.eu）。
Satellogic（米国、Nasdaq上場）
Satellogicは、アルゼンチン発の低コスト光学衛星メーカー兼データ事業者で、法人の所在を米国に移しました。2025年の売上は1,770万ドル（前年比38%増）と小規模
です（同社決算、2026年3月）。ただし2026年4〜6月期は1,590万ドル（同259%増）に急伸し、初めて営業黒字になりました。軌道上の衛星1機を外国の防衛顧客に
1,200万ドルで売却するなど、衛星そのものの販売が伸びています。全球を毎日1m分解能で撮る新コンステレーション「Merlin」の初打上げを2026年10〜12月期に予定
しています（同社決算、2026年8月）。

45 / 190


コラム 「主権型」契約とは何か 最近の決算資料には sovereign（主権）という言葉が頻出します。自国専用の衛星や撮影枠を持ちたい政府に対し、企業が衛星
の製造・打上げ・運用をまとめて提供する契約です。他国の政策変更で画像の供給が止まるリスクを避けたい、という各国の事情が背景にあります。Planet、
ICEYE、Satellogic、BlackSkyがいずれもこの型の契約を増やしています。

5.3 SAR衛星のプレイヤー

商業SARは、フィンランドのICEYEが規模で抜け出し、米国ではCapella、Umbra、ICEYEの米国法人の3社が政府調達の枠を固めました。2026年8月、米国の国家偵察局
（NRO、偵察衛星を担当する政府機関）はこの3社と商業SAR画像の調達契約を結んでいます。当初5社が参加した評価プログラムを通過したのがこの3社でした（Via
Satellite、2026年8月）。
ICEYE（フィンランド、非上場）
ICEYEは、同社によれば世界最大のSARコンステレーションを運用する企業です。2026年7月時点で累計76機を打ち上げ、最新のGen4衛星は最大16cmの分解能を持ちま
す（同社発表、2026年7月）。2026年6月には総額10億ユーロ超の資金調達（うち新規発行は4.5億ユーロ）を発表し、企業評価額は100億ユーロを超えました。同時に公
表された2025年の業績は、売上2.5億ユーロ超、EBITDA（利払い・税・償却前利益）1億ユーロ超、受注残15億ユーロ超です（Pulse 2.0、2026年6月）。
特徴は、画像の販売に加えて衛星そのものを各国の軍や政府に販売する点です。欧州の7つの政府が同社から専用システムを調達しており、ポーランド軍には契約から
12か月で納入しました。年間50機の生産能力を持ちます。
Capella Space（米国、IonQ傘下）
Capellaは米国の商業SARの先駆けで、2025年に量子コンピューター企業のIonQに買収されました。買収は2025年5月7日に発表され、全額株式交換で評価額は約3億
1,800万ドルでした（Via Satellite）。同年7月15日に完了しています。IonQは、衛星を使った量子鍵配送（量子技術による暗号鍵の共有）ネットワークの構築を買収の目
的に挙げています（IonQ）。軌道上の衛星は9機で、最新機は2026年3月に打ち上げたAcadia-10です（KeepTrack）。買収後もCapellaの名前でSAR事業を続けています。
Umbra（米国、非上場）
Umbraは、解析サービスを持たず、SARデータの販売に特化している点が特徴です。2015年創業で、カリフォルニア州サンタバーバラに本社を置きます。2021年から
2026年1月までに12機を打ち上げました。2023年8月に16cm分解能の画像を公表し、通常の製品は0.25〜1mです。無償で使えるオープンデータも公開しており、SARを
初めて触る人の練習材料になります（eoPortal）。2025年8月には衛星の機器を外販する事業部を立ち上げました（Umbra）。売上高は公開情報では確認できません。


46 / 190


表5-3 商業SAR主要3社の比較
項目
本拠
資本
衛星
公表された最高分解能
事業の特徴

表の読み方

い。

ICEYE
フィンランド
非上場（評価額100億ユーロ超）
累計76機を打上げ
16cm
データ販売＋衛星の販売

Capella Space
米国
IonQ（NYSE上場）の子会社
軌道上9機
公開情報では今回未確認
データ販売。量子通信との統合を計画

Umbra
米国
非上場
累計12機を打上げ
16cm
データ販売に特化。機器の外販も開始

衛星数は「累計打上げ数」と「軌道上の機数」が混在しています。SAR小型衛星は寿命が数年のため、累計と現役の数は大きく異なる点に注意してくださ

5.4 新センサーとRFのプレイヤー

光学とSARで「見える」ようになった次の競争は、物質・温度・ガス・電波といった「目に見えないもの」の計測です。この分野は企業規模がまだ小さく、資金調達の
ニュースが実力を測る主な手がかりになります。
表5-4 新センサー・RF分野の主な企業
企業
Pixxel
constellr
OroraTech
GHGSat
HawkEye 360
Spire Global

国
インド・米
独
独
加
米
米

何を測るか
ハイパースペクトル
熱赤外（地表面温度）
熱赤外（山火事検知）
メタンなど温室効果ガス
RF（電波の発信源）
気象、RF、航空機位置

直近の動き
2026年9月に1億ドルを調達。Firefly衛星6機を運用
2026年2月に3,700万ユーロを調達
2026年5月にギリシャ政府向け4機を打上げ
2024年10月時点で12機。2年で21機に増やす計画
2026年5月にNYSE上場
2025年4月に海事事業を売却

「何を測るか」が用途を決めます。たとえばメタンはエネルギー企業の漏えい管理、熱赤外は農業の水管理や山火事対応に使われます。出典は以下の本文
に示します。
表の読み方


47 / 190


Pixxelは累計1億9,500万ドルを調達し、後継機Honeybeeの初打上げを2027年に予定しています。米NROから2023年にデータ供給契約を得ています（TNW、2026年9
月）。constellrは防衛・政府からの引き合いが急増したと説明しています（constellr）。OroraTechがギリシャに納めた衛星群は、山火事検知専用の国家衛星システムと
して運用されています（Wikipedia）。GHGSatは油ガス井、埋立地、炭鉱などの施設ごとにメタンの排出を検出します（SpaceQ）。2026年時点の機数は公開情報では確
認できませんでした。
HawkEye 360は、衛星で電波の発信源を特定するRF分野の代表的な企業です。2026年5月7日にニューヨーク証券取引所へ上場し、4億1,600万ドルを調達しました。初
日終値での時価総額は32億ドルです。2025年の売上は1億1,770万ドル（2024年は6,760万ドル）、受注残は約3億300万ドルで、顧客は米政府と同盟国に集中しています
（Dealroom）。
Spire Globalは、多数の超小型衛星で気象データや航空機の位置情報を集めています。2025年4月、船舶追跡の海事事業をデータ企業Kplerに約2億3,350万ドルで売却
し、負債を全額返済しました（Spire）。2025年の売上は7,160万ドル（海事を除くと5,060万ドル）、2026年の見通しは7,500万〜8,500万ドルです（同社決算、2026年8
月）。

5.5 アジアのプレイヤー（中国・韓国・インド）

アジアでは、中国が機数で世界最大級の商業光学コンステレーションを持ち、韓国は政府衛星の画像販売、インドは新興企業の育成という異なる道を進んでいます。日
本企業にとっては競合であると同時に、調達先や提携先の候補でもあります。
中国：長光衛星（Jilin-1）とChina Siwei（SuperView）
長光衛星技術（Chang Guang Satellite Technology）は吉林省の企業で、「吉林1号（Jilin-1）」を運用します。2025年8月時点で117機が軌道上にあり、サブメートル級
（1m未満の分解能）の商業コンステレーションとして世界最大と報じられています（21世紀経済報道、2025年8月）。最高分解能は0.5mで、動画撮影衛星やハイパース
ペクトル衛星も含みます（Wikipedia）。将来の計画機数は資料によって138機と300機の2通りがあり、確定値は公開情報では確認できません。
China Siwei（中国四維）は、国有の中国航天科技集団（CASC）の系列企業です。SuperView（高景）シリーズ14機を運用し、さらに18機を追加する計画です
（Wikipedia）。中国勢の画像は、経済安全保障の観点から、日本や欧米の政府案件では採用できない場合があります。案件ごとに調達ルールを確認してください。
韓国：SIIS（KOMPSAT）
SI Imaging Services（SIIS）は、韓国の政府衛星KOMPSAT（アリラン）シリーズの画像を世界に販売する企業です。最新のKOMPSAT-7は2025年12月2日に打ち上げら
れ、分解能は白黒30cm、カラー1.2mです。2026年7月1日から本運用に入る計画が示されています（Geoimage、2026年3月）。政府が開発費を負担した衛星を民間が販
売する形で、日本の政府衛星の商業利用を考える際の参考になります。
インド：Pixxel、GalaxEyeなど

48 / 190


インドは、宇宙分野の民間開放を進める政府機関IN-SPACeのもとで新興企業が育っています。Pixxelが主導し、Dhruva Space、PierSight、SatSureが加わる企業連合
は、官民連携方式で12機の国家地球観測コンステレーションを構築する事業者に選ばれました（TNW）。ベンガルールのGalaxEyeは2026年5月3日、SARと光学センサー
を1機に載せた衛星「Mission Drishti」（約190kg、分解能1.2〜3.6m）を打ち上げ、2029年までに8〜12機へ増やす計画です（Drishti IAS）。

5.6 解析・プラットフォームのプレイヤー

衛星を持たない企業も、衛星データ市場の重要なプレイヤーです。利用者の多くは衛星会社から直接画像を買うのではなく、これらの企業のソフトウェアやクラウドを
通じてデータに触れるからです。役割は大きく5つに分かれます。
表5-5 解析・プラットフォーム企業の類型
類型
GIS（地理情報システム）ソフト
クラウド解析基盤
データ統合・意思決定基盤
マーケットプレイス
解析専業・垂直統合

表の読み方

代表例
Esri
Google Earth Engine、Microsoft Planetary Computer
Palantir
UP42、SkyFi
Privateer（Orbital Insight）、EarthDaily（Descartes Labs）

何をしているか
地図上でデータを重ね、分析・共有するソフトを提供
大量の衛星データとクラウドの計算資源をセットで提供
衛星データを他の情報と統合し、防衛や企業の判断に使う
複数の衛星会社の画像をまとめて検索・注文できる
AI解析で業種別の答えを提供。自社衛星を持つ例もある

上の3類型は「道具」を提供し、下の2類型は「データや答え」を届けます。クライアントがどの段階で困っているかによって、紹介すべき相手が変わりま

す。
Google Earth Engine：80ペタバイト超、30年分以上の衛星画像と地理データを備えたクラウド解析基盤です。商用利用が可能で、学術・研究目的は無償です
（Google）。
Microsoft Planetary Computer：企業向けの「Planetary Computer Pro」は、自社の地理空間データをAzure上で管理・検索・配信するサービスです。STAC（衛
星データの目録を記述する標準仕様）に対応します（Microsoft Learn）。
Palantir：衛星会社と組み、撮影指示から解析までを自社のデータ基盤に取り込んでいます。2022年にはSatellogicと5年間の提携を結びました（Business Wire）。
UP42：Airbusが育てたマーケットプレイスで、2025年7月にサウジアラビアのNeo Space Groupへの売却が完了しました（GeoConnexion）。
SkyFi：米テキサス州オースティンの企業で、50社超の画像提供元と提携します。2026年1月に1,270万ドルを調達しました（Evertiq）。

49 / 190


Orbital Insight：衛星画像のAI解析の草分けで、2024年5月に宇宙状況把握のPrivateerに買収されました（Pulse 2.0）。その後の事業状況は公開情報では確認できま
せん。
EarthDaily Analytics：カナダの企業で、2024年10月に解析企業Descartes Labsを買収しました（Payload）。自社衛星も持ち、2026年5月に6機を打ち上げていま
す。各衛星は22の波長帯で観測します（EarthDaily）。
Esri：GISソフト「ArcGIS」の提供元です。詳細な事業数値は今回の調査では確認できませんでした。
コンサルの視点 クライアントに衛星データ活用を提案するとき、最初に決めるのは「どの衛星会社から買うか」ではなく「どの基盤の上で使うか」です。クラ
イアントがすでにArcGISやAzure、Google Cloudを使っているなら、その上で動く選択肢から検討すると導入の負担が小さくなります。

5.7 業績の比較と業界再編

上場企業の数字を並べると、市場の規模感と勢いがわかります。上場企業で最大のPlanetでも年間売上は3億ドル台であり、衛星データ販売はまだ「小さくて伸びてい
る」産業です。
表5-6 主要企業の直近業績（公表値）
企業
Planet Labs
HawkEye 360
BlackSky
Spire Global
Satellogic
ICEYE（非上場）

直近通期の売上
3億770万ドル（2026年1月期）
1億1,770万ドル（2025年）
1億660万ドル（2025年）
7,160万ドル（2025年）
1,770万ドル（2025年）
2.5億ユーロ超（2025年）

直近四半期の売上（前年同期比）
1億1,610万ドル（+58%、2026年5〜7月）
4,980万ドル（+87%、2026年4〜6月）
3,330万ドル（+50%、2026年4〜6月）
1,800万ドル（-6%、2026年4〜6月）
1,590万ドル（+259%、2026年4〜6月）
非公表

受注残など
8億1,490万ドル
2億9,220万ドル
3億4,500万ドル（2025年末）
公開情報では確認できません
8,070万ドル
15億ユーロ超

2026年度の会社見通し
4億3,000万〜4億4,100万ドル
2億1,500万〜2億2,000万ドル
1億3,000万〜1億5,000万ドル
7,500万〜8,500万ドル
公開情報では確認できません
非公表

受注残が年間売上の何倍あるかを見ると、数年先までの売上の見通しやすさがわかります。各社で決算期と受注残の定義が異なるため、厳密な横比較には
向きません。HawkEye 360の四半期値はQuartrの要約による二次情報です。そのほかは5.2〜5.4節で示した各社の決算資料に基づきます。
業界再編の流れ
表の読み方


50 / 190


2023年以降の再編は、「投資ファンドによる老舗の解体」「異業種による買収」「防衛需要を追い風にした上場・大型調達」の3つの動きで説明できます。
表5-7 業界再編の年表（2023〜2026年）
時期
2023年5月
2024年5月
2024年10月
2025年4月
2025年7月
2025年7月
2025年10月
2026年1月
2026年5月
2026年6月
2026年7月
2027年（目標）

出来事
AdventがMaxarを64億ドルで買収。同年9月に2社へ分割
PrivateerがOrbital Insightを買収
EarthDailyがDescartes Labsを買収
Spireが海事事業をKplerへ売却（約2億3,350万ドル）
IonQがCapella Spaceの買収を完了
Neo Space GroupがUP42の買収を完了
Maxar IntelligenceがVantor、Maxar Space SystemsがLanterisに改称
Intuitive MachinesがLanterisを8億ドルで買収完了
HawkEye 360がNYSE上場（4億1,600万ドル調達）
ICEYEが10億ユーロ超の資金調達、評価額100億ユーロ超
MDA Spaceが仏CLSの約70%を約5.67億ユーロで取得すると発表
Airbus・Leonardo・Thalesの宇宙事業統合会社が稼働

意味
最大手が非上場化され、画像と製造が分かれた
解析専業の草分けが独立を終えた
解析と自社衛星の垂直統合
負債返済のための事業切り出し
量子技術企業という異業種が参入
中東資本がプラットフォームを取得
Maxarブランドが消滅
旧Maxarの製造部門が月面企業の傘下に
RF分野の企業が株式市場へ
欧州の防衛宇宙企業への資金集中
カナダ大手が欧州の解析事業へ進出（完了は2026年末〜2027年初の見込み）
欧州の宇宙産業が1社に集約される可能性

古い資料の社名が現在のどの会社に当たるかを確かめるときに使ってください。MDA・CLSの案件はInvest Ottawa掲載の発表文、そのほかは各節の出典に
よります。なお、2025〜2026年に主要な地球観測企業が破綻した事例は、今回の調査では確認できませんでした。
防衛・政府需要への依存
海外の衛星データ企業の成長は、民間企業向けではなく、防衛と政府向けが支えています。各社の決算資料に並ぶ契約先を見ると、その傾向は明らかです。
Planetが2026年5〜7月期に挙げた主な成約は、ドイツ政府、米国家地理空間情報局（NGA）、欧州の防衛・情報機関、ルワンダ宇宙庁などです。
BlackSkyの同期の成約は、NRO、NGA、米宇宙軍、海外の防衛顧客が中心です。
HawkEye 360は、売上が米政府と同盟国との契約に大きく集中していると報じられています。
表の読み方


51 / 190


ICEYEは、欧州7か国の政府が同社の衛星システムを調達しています。
ただし、売上に占める防衛・政府の比率を、今回確認した決算リリースは数値で示していません。正確な比率が必要なときは、各社の年次報告書（Form 10-K）を確認
してください。
この依存には表と裏があります。政府契約は金額が大きく複数年にわたるため、衛星への先行投資を回収しやすくなります。一方で、予算や政策の変更に業績が左右さ
れます。たとえば2025年3月には、米政府がウクライナへの情報提供を一時制限し、Maxar（当時）が運用する画像提供プログラムが数日間止まりました
（Wikipedia）。欧州やアジアの政府が自国専用の衛星を求める背景には、こうした供給途絶への懸念があると考えられます。
コンサルの視点 海外企業の成長率をそのまま「民間市場の拡大」と読み替えないでください。伸びているのは主に防衛・政府向けです。民間クライアント向け
の市場規模を語るときは、顧客の内訳まで確かめた数字を使います。

5.8 まず押さえる5社

初心者は、Vantor、Airbus、Planet、ICEYE、BlackSkyの5社を最初に覚えてください。この5社で「高分解能光学」「光学＋SARの総合」「高頻度光学」「SAR」「即時性
とAI」という主要な競争軸をひととおり説明できます。
表5-8 まず押さえる5社

企業
Vantor
Airbus Defence and Space
Planet Labs
ICEYE
BlackSky

一言でいうと
30cm級光学の老舗（旧Maxar）
光学とSARを持つ欧州の総合大手
毎日撮る小型衛星群
SARの最大手
高頻度撮影とAI解析の即時配信

覚える理由
高分解能画像の基準。旧社名が資料に頻出する
欧州の調達案件で必ず名前が出る。統合計画に注目
上場EO企業で売上最大。決算資料が業界の教科書になる
衛星そのものを国に売る「主権型」モデルの代表
「画像」ではなく「分析結果」を売る方向性の代表

5社を覚えたら、次に「この5社に無いもの」として、ハイパースペクトル（Pixxel）、RF（HawkEye 360）、プラットフォーム（Google Earth Engine、Esri）
を足していくと整理しやすくなります。
表の読み方


52 / 190


ポイント この業界は社名と資本関係の変化が速いため、企業情報は「いつ時点か」を必ず確認します。本章の数値は2026年10月時点の公開情報です。提案書
に使う前に、各社の最新の決算資料で更新してください。

この章のまとめ
海外プレイヤーは、高分解能光学、小型光学コンステレーション、SAR、新センサー、RF・AIS、解析・プラットフォームの6グループで整理できます。
上場企業で最大のPlanetの売上は3億770万ドル（2026年1月期）で、受注残は8億ドルを超えます。非上場のICEYEは2025年に売上2.5億ユーロを超えました。
2025年にはMaxar IntelligenceがVantorへ改称し、Capella SpaceはIonQに買収されました。2026年にはHawkEye 360が上場しました。
各社の成長を支えているのは防衛・政府需要です。衛星や撮影容量を国に提供する「主権型」契約が広がっています。
まずVantor、Airbus、Planet、ICEYE、BlackSkyの5社を覚え、そこから他のセンサーとプラットフォームへ広げます。

確認問題

1. クライアントが持ってきた2024年の資料に「Maxarの画像を使用」と書かれています。現在の調達先はどの会社ですか。また、衛星製造部門はどうなりましたか。
ヒント：表5-7の2023年、2025年10月、2026年1月の行を見ます。
2. 雲が多い地域のインフラを週に複数回監視したいという相談を受けました。どのグループの企業が候補になりますか。理由も述べてください。 ヒント：5.1節の分類
で、雲の下でも撮れるセンサーを探します。
3. 「海外の衛星データ企業は年50%で成長しているので、民間向け市場も同じ速さで伸びる」という主張の問題点を指摘してください。 ヒント：5.7節の「防衛・政府
需要への依存」で、成約先の顔ぶれを確認します。

出典

Planet Reports Financial Results for Fourth Quarter and Full Fiscal Year 2026（SEC提出資料）
Planet Reports Financial Results for Second Quarter of Fiscal Year 2027（SEC提出資料）
Planet Launches High-Resolution Pelican-5, Pelican-6 Satellites and 36 SuperDoves
Planet's new Owl satellites for 1-meter resolution imaging（NextBigFuture）
SKY Perfect JSAT is Planet's Customer for New LEO Constellation（Via Satellite）
BlackSky Reports Fourth Quarter and Full Year 2025 Results
BlackSky Reports Second Quarter 2026 Results（SEC提出資料）


BlackSky captures first imagery from fifth Gen-3 satellite（defence-industry.eu）
Spire Global Announces Second Quarter 2026 Results（SEC提出資料）
Spire Global Completes Sale of Maritime Business; Debt Eliminated
Satellogic Reports Fourth Quarter and Full Year 2025 Financial Results
Satellogic Reports Second Quarter 2026 Financial Results（SEC提出資料）
HawkEye 360 raises $416M as investors pile into defence tech IPOs（Dealroom）
HawkEye 360 Q2 2026 earnings summary（Quartr）
53 / 190


Vantor (company)（Wikipedia）
Vantor Satellite Constellation（Polar Geospatial Center）
Intuitive Machines Completes Lanteris Space Systems Acquisition（Via Satellite）
Our optical and radar satellite imagery（Airbus）
The first Airbus Pléiades Neo Next satellite will be launched early 2028（Airbus）
Airbus, Leonardo and Thales merge space units for 2027 launch（Digital Watch）
ICEYE launches four new satellites aboard Transporter-17
ICEYE: €1 Billion Funding Round（Pulse 2.0）
Quantum Computing Company IonQ to Acquire Capella Space（Via Satellite）
IonQ Completes Acquisition of Capella Space
Capella constellation（KeepTrack）
Capella, Iceye US, and Umbra Receive NRO Commercial SAR Contracts（Via Satellite）
Umbra SAR Constellation（eoPortal）
Umbra press releases
Pixxel raises $100M（TNW）
constellr snaps up €37M


OroraTech（Wikipedia）
GHGSat to launch 9 more satellites before 2027（SpaceQ）
Chang Guang leads innovative development of China's commercial remote sensing satellites
（21世紀経済報道）
Jilin-1（Wikipedia）
China Siwei（Wikipedia）
KOMPSAT-7 first images revealed（Geoimage）
GalaxEye Launched Mission Drishti（Drishti IAS）
Google Earth Engine
Microsoft Planetary Computer Pro overview（Microsoft Learn）
Satellogic Announces Strategic Partnership With Palantir Technologies（Business Wire）
Neo Space Group completes acquisition of UP42（GeoConnexion）
SkyFi raises $12.7M（Evertiq）
Privateer Raises $56.5 Million And Acquires Orbital Insight（Pulse 2.0）
EarthDaily Analytics buys Descartes Labs（Payload）
EarthDaily: six satellites launched
MDA Space enters firm offer to acquire majority stake in France's CLS（Invest Ottawa）

54 / 190


