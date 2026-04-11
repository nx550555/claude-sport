━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ベッティング分析システム — フォルダ説明
  C:\Users\ohwada\Desktop\claude_sport\
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【フォルダ構成】
claude_sport/
├── README.txt
├── core/
│   ├── framework.json        共通設定（変更少ない）
│   ├── rules_tennis.json     テニスルール ← 上書き更新
│   └── rules_nhl.json        NHLルール（設計中）
├── records/
│   ├── tennis/
│   │   └── 2026-MC.json      MC2026の全予測・結果 ← 結果を追記
│   └── nhl/                  プレーオフ開始後に追加
├── stats/
│   └── cumulative.json       累積統計 ← 随時更新
└── dashboard/
    └── index.html            ブラウザで開くダッシュボード

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【使い方】

▼ 分析を依頼するとき
  1. rules_tennis.json をclaude.aiにアップロード
  2. 「このルールで今日の試合を分析してください」と送信
  → ルールと設計を全て引き継いで分析してくれます

▼ 結果が出たとき
  1. records/tennis/2026-MC.json を開く
  2. 該当試合の result・score・hit・actual_ev を書き込む
  3. stats/cumulative.json の数字を更新する
  ※ Claudeに「結果を反映して更新版のJSONを出力して」
    と依頼してコピペするのが一番楽です

▼ ルールが更新されたとき（新しい外れがあったとき）
  1. Claudeに「rules_tennis.jsonの更新版を出力して」と依頼
  2. 出力されたJSONを core/rules_tennis.json に上書き保存

▼ ダッシュボードを見るとき
  1. dashboard/index.html をダブルクリック
  2. ブラウザで開く（スマホへコピーしても開けます）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【チャット戦略】

テニスチャット（今のチャット）
  → MC2026が終わったら「テニスチャット2」へ移行
  → rules_tennis.jsonをアップロードして継続

NHLチャット（新規、4月下旬〜）
  → rules_nhl.jsonをアップロードして開始

統合チャット（将来）
  → 両方のrulesファイルを揃えてから合流

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
更新履歴
2026-04-09  v1.0 作成。MC2026 R32検証完了・5ルール学習済み。
