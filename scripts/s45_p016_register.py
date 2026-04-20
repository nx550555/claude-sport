"""
Session_45 補遺: P016 の正式登録 + rules_superleague.json 新設
Warrington Wolves (A020) 分析結果を実システムに反映
"""
import json
from pathlib import Path

BASE = Path(r"C:\Users\ohwada\Desktop\claude_sport")

# ---- (A) rule_pipeline.json に P016 正式登録 ----
rp_path = BASE / "core" / "rule_pipeline.json"
rp = json.load(open(rp_path, encoding="utf-8-sig"))

p016 = {
    "candidate_id": "P016",
    "status": "watching",
    "target_rule_file": "core/rules_superleague.json (新設) / core/rules_nrl.json (暫定準拠)",
    "proposed_rule_id": "SL002",
    "title": "Super League: Catalans 仏国ホーム補正強化 (-5% → -7〜-10%)",
    "description": (
        "Super League の Catalans Dragons (仏国 Perpignan ベース) のホーム試合で、英国チームが遠征する場合、"
        "現行 Basic Tier のdefault home advantage (+3%) では不足。"
        "観客・移動疲労・芝質・天候など複合要因で仏国ホーム補正を -7%〜-10% に強化。"
        "対象: 英国本拠地チーム (Leeds, Warrington, Wigan, St Helens 等) が Stade Gilbert Brutus に遠征するケース。"
    ),
    "trigger_threshold": 2,
    "current_count": 1,
    "evidence": [
        {
            "id": "A020",
            "match": "Warrington Wolves at Catalans Dragons SL R8 2026-04-19",
            "pattern": (
                "Warrington GO @1.64 (conf 83% / EV +36.1%) → MISS. "
                "Catalans 38-22 勝利 (Dodd hat-trick). "
                "1st half Warrington 16-10 リード → 2nd half Catalans 5トライ連取で崩壊. "
                "UF3 (UF01 France home / UF02 Dodd個人爆発 / UFA04 travel fatigue) + div 10pp. "
                "UPSET_PICK閾値(UF≥3+div≥15pp)未達だが CAUTION格下げが妥当だった"
            ),
            "tag": "superleague_catalans_home_uk_visitor_upset",
            "sources": [
                "records/superleague/2026.json games[1]",
                "stats/upset_patterns.json A020"
            ]
        }
    ],
    "tag_matches": [
        "superleague_catalans_home_uk_visitor_upset",
        "rugby_continental_crossing_home"
    ],
    "note": (
        "2件目 evidence が揃ったら SL002 として実装。実装時は rules_superleague.json を新設し、"
        "英国チーム vs Catalans (Stade Gilbert Brutus 開催) 時に fav confidence から -7% 減点、"
        "2nd half崩壊リスク factor を追加。evidence 2件目候補: Catalans vs Wigan (スケジュール確認要), "
        "Catalans vs St Helens 等。"
    )
}

candidates = rp.setdefault("candidates", [])
existing_ids = {c.get("candidate_id") for c in candidates}
if "P016" not in existing_ids:
    candidates.append(p016)
    print("P016 candidates に追加完了")
else:
    print("P016 既に存在。スキップ")

rp["last_updated"] = "2026-04-20"
rp["updated_session"] = "_45"

with open(rp_path, 'w', encoding='utf-8') as f:
    json.dump(rp, f, ensure_ascii=False, indent=2)

# ---- (B) rules_superleague.json 新設 (NRL準拠 + SL独自 watching ルール) ----
sl_rules_path = BASE / "core" / "rules_superleague.json"
sl_rules = {
    "sport": "rugby_league",
    "league": "Super League",
    "country": "UK + France (Catalans)",
    "tier": "basic",
    "version": "v1.0",
    "created": "2026-04-20 Session_45",
    "inheritance": {
        "base": "core/rules_nrl.json",
        "note": "NRL Basic Tier ルールを全面継承。SL独自補正は below の additions セクションのみ。"
    },
    "L1_metric": "PD/G (得失点差/試合)",
    "L1_threshold": {
        "go": "PD/G diff >= 6pt (NRL同)",
        "screening_note": "Super League は 11試合規模のシーズンのためサンプル小。PD/G ≥6pt でも Basic Tier 閾値 (conf≥78% AND EV>+7%) を維持"
    },
    "additions_over_nrl": {
        "SL001": {
            "title": "Super League早期シーズン信頼度上限 (R1-R6)",
            "description": "シーズン序盤はPD/Gサンプルが小さく評価ブレが大きいため、R1-R6 は信頼度上限を 78% に制限 (Basic Tier 標準 +3pp厳格化)。",
            "status": "active_v1.0",
            "applies_to": "rounds 1-6"
        },
        "SL002_candidate": {
            "title": "Catalans 仏国ホーム補正強化 (-7% to -10%)",
            "description": (
                "Catalans Dragons のホーム試合 (Stade Gilbert Brutus / Perpignan) で英国本拠地チームが遠征する場合、"
                "英国チームの confidence から -7%〜-10% 減点。"
                "複合要因: 移動疲労 (UK→FR 遠距離遠征)、気候 (地中海 vs 英国寒冷)、"
                "芝質 (ハードグラウンド傾向)、観客アウェイ感。"
            ),
            "status": "watching (rule_pipeline P016)",
            "evidence": 1,
            "threshold": 2,
            "evidence_ref": "A020 Warrington vs Catalans R8 2026-04-19 MISS",
            "activation_note": "2件目 evidence 到達で active化。現状は Basic Tier default home advantage のみ適用。"
        }
    },
    "screening_checklist": {
        "pre_screening": [
            "L1: 両チームの PD/G 算出 (rugby-league.com statistics)",
            "L2: 直近5試合フォーム (win rate, average margin)",
            "L3: H2H (過去3シーズン)",
            "L4: 怪我・出場停止・移動疲労",
            "L4_bonus_for_Catalans_game: **Catalans home vs UK visitor の場合 P016 発動候補として UF02 travel fatigue + UF01 venue advantage を必ずチェック**"
        ]
    },
    "rules_applied_history": [
        {
            "date": "2026-04-19",
            "match": "Warrington @ Catalans R8",
            "rules_triggered": ["default_home_advantage (+3%)"],
            "rules_should_have_triggered": ["SL002_candidate (-7%)"],
            "result": "MISS -1.0u. SL002候補化の根拠 (A020)."
        }
    ],
    "last_updated": "2026-04-20 Session_45"
}

if not sl_rules_path.exists():
    with open(sl_rules_path, 'w', encoding='utf-8') as f:
        json.dump(sl_rules, f, ensure_ascii=False, indent=2)
    print("rules_superleague.json 新規作成完了")
else:
    print("rules_superleague.json 既存。スキップ")

# ---- (C) framework.json の sports_active_note 更新 ----
fw_path = BASE / "core" / "framework.json"
fw = json.load(open(fw_path, encoding="utf-8-sig"))
if "rules_files" in fw:
    fw["rules_files"]["super_league"] = "core/rules_superleague.json (v1.0 新設・NRL準拠 + SL独自補正)"
fw["last_updated"] = "2026-04-20"
with open(fw_path, 'w', encoding='utf-8') as f:
    json.dump(fw, f, ensure_ascii=False, indent=2)
print("framework.json rules_files 更新完了")

print("\n=== 反映サマリ ===")
print(f"  rule_pipeline P016 登録: OK")
print(f"  rules_superleague.json 新設: OK (SL001 active + SL002_candidate watching)")
print(f"  framework.json rules_files: OK")
