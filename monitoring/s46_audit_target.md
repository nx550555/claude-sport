# Session_46 最優先タスク: upset_patterns 全件 ③→④反映監査

## 背景
Session_45 末尾で、Warrington Wolves MISS (A020) 分析結果が `rule_pipeline.json` に登録されていなかったことが発覚 → 補填。ユーザー再指摘で「他にも同じ漏れ試合が無数にありそう」 → 監査スキャンを実施した結果、**33件中 5件のみが rule_pipeline 連動済、28件が未反映**であることが判明。

## 監査スキャン結果（2026-04-20 Session_45末尾実施）

### ✓ rule_linked あり かつ pipeline登録済: 5件
- A014 [tennis_atp]: Kopriva vs Darderi → **R020** (implemented)
- A018 [tennis_atp]: Molcan vs Shapovalov → **R020** (implemented)
- A019 [tennis_atp]: Jodar vs Norrie → **R017** (implemented)
- A020 [super_league]: Warrington at Catalans → **P016** (watching, Session_45補填)
- A025 [tennis_atp]: Darwin vs Bonzi → **P017-candidate** (watching)

### ✗ rule_linked なし or pipeline未登録: 28件
全件について rule_linked=None または candidates配列に対応entry不在。

**スポーツ別内訳**:
- tennis_atp: 9件 (U001/U002/U003/U006/A004/A005/A006/A011/A012)
- tennis_wta: 3件 (U007/A001/A013)
- nhl: 3件 (A002 CAR-PHI / A003 STL-MIN / A021 TBL-MTL G1)
- nrl: 3件 (U005/A007 Storm-Warriors / A008 Roosters-Sharks)
- ufl: 2件 (A009 Storm-Louisville / A010 Stallions-Battlehawks)
- nhl (PO G1): 2件 (A027 PHI-PIT / A028 MIN-DAL)
- nba: 1件 (A026 ORL-DET)
- tennis 他: 2件 (U008 Marozsan-Hurkacz / U009 Rabbitohs-Raiders)
- WTA Madrid Q 新規: 3件 (A022/A023/A024)
- ※ 一部はID未設定（空文字）

---

## Session_46 最優先実行計画

### STEP 1: 監査スキャンの再実行
```bash
python scripts/s45_audit_scan.py  # (要新設) → 最新状況を確認
```

### STEP 2: 28件の一括分類
各エントリーについて以下を判定：
- **A. ルール化可能**: 明確なパターンあり → rule_pipeline に新候補登録
- **B. 既存ルールで説明可能**: 既存 implemented_rules に該当 → rule_linked に既存IDを追記
- **C. ノイズ（ランダム要因）**: パターン見いだせない → 「観察終了」とマーク
- **D. 単発事例（evidence 1件のみ）**: 候補登録せず、将来類似事例蓄積まで観察

### STEP 3: rule_pipeline 追加 + rules_{sport} 実装判断
- 新規 P候補を登録（P018, P019, ... 連番）
- 既存候補の evidence 追加 (current_count +1)
- threshold 到達なら rules_{sport}.json に実装

### STEP 4: upset_patterns.json の整備
- 各エントリーの rule_linked を埋める (A〜D分類反映)
- rule_improvement_candidates の空エントリ 4件を修繕 (title/content補完)
- 既存 upset_id 未設定 ("") を A00x / U00x リネーム

### STEP 5: health_check.py v2 拡張
新規項目追加:
- **項目7**: upset_patterns 全件で rule_linked フィールド存在率 (< 80% で警告)
- **項目8**: rule_improvement_candidates の空エントリ検出

---

## 優先順位（スポーツ別）

高優先度（データ豊富・evidence蓄積しやすい）:
1. **tennis_atp 9件**: 最多件数・既存 R001/R017/R020 の延長として再評価
2. **nhl 5件**: RS/PO 両方あり・L4外部要因多い

中優先度:
3. nrl 3件・tennis_wta 3件

低優先度（単発性高い）:
4. ufl 2件・nba 1件・その他 4件

---

## 見込み成果

28件の精査で：
- 新規 rule_pipeline 候補 **10-15件** 追加見込み
- 既存 implemented_rules の evidence +1〜+3 試合分蓄積
- **rules 実装 2-3件** 新たに昇格する可能性
- Phase2 の UPSET_PICK / Q3出力A / Q4観察 の精度向上

---

## ユーザーへの確認事項（Session_46 開始時）

1. 上記監査を 最優先タスクとして実行開始してよいか
2. 28件の精査は **スポーツ別に順次** か、**全件一括処理** か
3. 分類結果 (A/B/C/D) をユーザーと協議しながら決めるか、一括で Claude 判断で進めるか
