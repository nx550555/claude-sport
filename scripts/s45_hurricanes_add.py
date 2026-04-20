"""
Session_45 補遺: 4/18 Chiefs 22-17 Hurricanes (R10 golden-point) 記録漏れの補填
"""
import json
from pathlib import Path

BASE = Path(r"C:\Users\ohwada\Desktop\claude_sport")
sr_path = BASE / "records" / "superrugby" / "2026.json"
d = json.load(open(sr_path, encoding="utf-8-sig"))

entry = {
    "match": "Chiefs vs Hurricanes",
    "date": "2026-04-18",
    "round": "R10",
    "venue": "FMG Stadium Waikato (Chiefs home)",
    "tier": "skip",
    "tier_category": "basic",
    "l1_metric": "market_implied_probability + PD/G context",
    "l1_data": "Chiefs @1.72 (market 58% / margin-adj 55%) vs Hurricanes @2.05 (market 49% / margin-adj 46%). Div ≈ 9pp",
    "predicted_winner": "Chiefs",
    "prediction_confidence": 55,
    "prediction_basis": "市場 Chiefs pickem-favorite (@1.72). Chiefs home + 過去5戦でHurricanes 3勝2敗の中で、Hurricanes 5連勝+成績6-1でupset候補扱いもあったが market は Chiefs 有利評価。pickem 帯 55% confidence.",
    "quadrant": "skip",
    "rules_applied": ["market_implied_only", "no_L1_depth (scope: SRP record限定記録漏れ補填)"],
    "adjustments": "事前分析記録漏れ → 結果確認時(Session_45補遺)に後追い記録。",
    "rec": None, "rec_odds": None, "ev": None,
    "result": "Chiefs",
    "score": "22-17 (Golden point OT)",
    "prediction_hit": True,
    "hit": None, "actual_ev": None,
    "outcome_note": (
        "Chiefs 22-17 Hurricanes. 経過: HT Hurricanes 12-3 (Lakai/Moorby tries) → 72分 Hurricanes 17-10 "
        "→ Chiefs late try (Carter offload → Sinkinson) → 17-17 FT → OT 5分 Wallace Sititi が "
        "Damian McKenzie の charged-down drop-kick を拾ってtry. Chiefs captain Luke Jacobson の100試合記念。"
    ),
    "key_observations": {
        "fav_prediction_hit": True,
        "late_game_pattern": "Hurricanes 9pt lead from HT → blown in late 8min. 終盤の momentum shift パターン。",
        "ot_decision_point": "Golden point OT で決着。5分未満で結論 → L4 external factor (個人プレーの一閃) が結果を左右",
        "home_advantage_note": "Chiefs home FMG Waikato での接戦勝利. home advantage + 5連勝Hurricanesのroad streak終焉",
        "market_verdict": "Pickem @1.72 vs @2.05 の評価は正しかった。fav HIT.",
        "no_upset": "UPSET ではない (本命 Chiefs勝利). upset_patterns への登録不要."
    },
    "session_added": "_45",
    "session_note": "Super Rugby R10 (4/18) が 2026-04-19.json / 2026-04-20.json のどちらにも含まれておらず、Session_43/44/45 で記録漏れ。ユーザー指摘(Session_45末尾)で発覚・補填。"
}

# games 配列 に追加 (重複チェック)
games = d.setdefault("games", [])
exists = any(g.get("match","")==entry["match"] and g.get("date","")==entry["date"] for g in games)
if exists:
    print("既に記録済み。スキップ")
else:
    games.append(entry)
    print(f"games 配列に追加: {entry['match']} {entry['date']}")

# screening_log に補遺エントリ
sl = d.setdefault("screening_log", [])
sl.append({
    "date": "2026-04-20",
    "session": "_45_supplement",
    "scope": "Session_45 補遺: R10 Chiefs vs Hurricanes (4/18) 記録漏れ補填",
    "issue": "2026-04-19.json / 2026-04-20.json で Super Rugby R10 試合は upcoming に含まれておらず (R11 4/24-26 からの記載のみ)。ユーザー自然観戦で認識していた 4/18 Hurricanes 負けが分析記録に未存在と発覚。",
    "action": "WebSearch で一次情報確認 (rugbyisthegame / rnz / super.rugby) → 事後記録として games に追加。fav予測 HIT 確定。",
    "improvement": "補遺: 主要リーグの完了試合 (R10 等) が JSON に含まれていない場合、定期的に WebSearch でレビュー → records 追加する運用改善案。rule_pipeline / health_check.py の新チェック項目候補として記録。"
})

# summary 更新
s = d.setdefault("summary", {})
s["last_updated"] = "2026-04-20 Session_45 補遺"
d["last_updated"] = "2026-04-20"

with open(sr_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("records/superrugby/2026.json 更新完了")
print(f"games: {len(games)} / screening_log: {len(sl)}")
