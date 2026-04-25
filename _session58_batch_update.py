"""
Session_58 batch update script
- Phase A 完了: Keys VOID / Musetti HIT / Tsitsipas HIT / Mertens live (HIT 確定版へ昇格)
- Phase B 結果反映:
  - Paul vs Tirante 4/24: MISS (Tirante d. Paul 7-5 6-4 UPSET)
  - Fonseca vs Cilic 4/24: VOID (Cilic WO)
  - Jodar d. de Minaur 6-3 6-1 UPSET
- Phase B 新規 GO:
  - ATP R2 4/25: Khachanov / Auger-Aliassime / Mensik
  - WTA R2 4/25: Mboko
  - NRL R9 4/25-26: Warriors / Manly
- Phase C 新規 SKIP 大量を screening_log で集約
- cumulative.json / dashboard_stats.json / multi_bets.json / BACKLOG / pending_actions 更新
"""

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:\Users\ohwada\Desktop\claude_sport")

def load_json(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# =====================================
# 1. ATP records 更新
# =====================================
atp_path = ROOT / "records/tennis/2026-ATP.json"
atp = load_json(atp_path)
preds = atp['predictions']

# Find and update Paul vs Tirante entry (index 0 of Madrid)
madrid_idx = [i for i,p in enumerate(preds) if 'Madrid' in str(p.get('tournament',''))]
paul_idx = next((i for i in madrid_idx if 'Paul' in str(preds[i].get('match','')) and 'Tirante' in str(preds[i].get('match',''))), None)
if paul_idx is not None:
    p = preds[paul_idx]
    p['result'] = "Tirante d. Paul"
    p['score'] = "7-5 6-4"
    p['prediction_hit'] = False
    p['hit'] = False
    p['actual_ev'] = -1.0
    p['status'] = "completed"
    p['outcome_note'] = "Tirante (ARG clay specialist) UPSET over Paul (USA hardcourt bias). 7-5 6-4. GO @1.42 MISS -1.0u. Session_57 で P012 A034 として事前記録済 → R019 実装 evidence 3/3。"
    p['miss_analysis'] = "Tirante clay specialist endurance 2セットstraight。Paul hardcourt bias + GEN003 での Paul 出場維持確認は正しかったが、Tirante clay pedigree を L1 cElo で捕捉しきれなかった (+15pt 補正 R019 適用しても conf 70% → EV +0%)。R019 本実装により今後同型は CAUTION 降格可能。"
    p['miss_layer'] = "L1_cElo_insufficient_surface_weight"
    p['rule_linked'] = "R019 (clay specialist vs hardcourt bias - 実装済 Session_57)"
    p['session_58_update'] = "結果反映 2026-04-25 JST"
    p['verification_sources'] = ["opencourt.ca Madrid Friday April 24 2026 order of play",
                                  "tennistonic.com/tennis-news/989901 Tirante draw vs Paul"]

# Cilic vs Fonseca - Cilic withdrawal
fonseca_cilic_idx = next((i for i in madrid_idx if 'Fonseca' in str(preds[i].get('match','')) and 'Cilic' in str(preds[i].get('match',''))), None)
if fonseca_cilic_idx is not None:
    p = preds[fonseca_cilic_idx]
    p['result'] = "VOID (Cilic WITHDREW last minute)"
    p['score'] = "W/O"
    p['prediction_hit'] = None
    p['hit'] = None
    p['actual_ev'] = 0.0
    p['void'] = True
    p['void_reason'] = "Cilic last-minute withdrawal (Arantxa Sanchez Court)"
    p['outcome_note'] = "Cilic withdrew at last minute. Fonseca advances W/O to R3 vs Jodar."
    p['session_58_update'] = "VOID 反映 2026-04-25 JST"
    p['verification_sources'] = ["puntodebreak.com Cilic is out at the last minute Fonseca waiting R3"]

# Jodar vs de Minaur - UPSET
jodar_dm_idx = next((i for i in madrid_idx if 'Jodar' in str(preds[i].get('match','')) and 'Minaur' in str(preds[i].get('match',''))), None)
if jodar_dm_idx is not None:
    p = preds[jodar_dm_idx]
    p['result'] = "Jodar d. de Minaur"
    p['score'] = "6-3 6-1"
    p['prediction_hit'] = p.get('predicted_winner','') == 'Rafael Jodar' or 'Jodar' in str(p.get('predicted_winner',''))
    p['hit'] = None  # SKIP no-bet
    p['actual_ev'] = None
    p['status'] = "completed"
    p['type_a_upset_id'] = "A035"
    p['outcome_note'] = "UPSET: Jodar (19yo WC Spain) d. de Minaur (#8) 6-3 6-1 maiden Top-10 win. 34 receiver points vs 19, 61% 1st-serve return, 6 breaks from 13 chances. R009 home WC + R017 連続ラウンドモメンタム (vs R1 Norrie) 適用で Jodar 上方修正の事前兆候あり。"
    p['session_58_update'] = "結果反映 UPSET 2026-04-25 JST"
    p['verification_sources'] = ["atptour.com jodar-de-minaur-madrid-2026-friday",
                                  "sofascore.com Madrid Open Jodar beats de Minaur 6-3 6-1"]

# Add new GO entries for 4/25 (Khachanov, FAA, Mensik)
new_atp_entries = [
    {
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2",
        "date": "2026-04-25",
        "match": "Khachanov K. vs Walton A.",
        "tier": "go",
        "quadrant": "Q1_go",
        "l1_metric": "clay_cElo",
        "l1_data": {"ce_diff": 324.1, "fav": "Karen Khachanov", "dog": "Adam Walton"},
        "predicted_winner": "Karen Khachanov",
        "prediction_confidence": 86,
        "prediction_basis": "cElo +324pt / Walton AUS hardcourt bias (R019 clay specialist 新実装適用 +15pt 補正でさらに強化) / Walton clay R2 debut Masters",
        "odds": {"fav": 1.22, "dog": 4.40},
        "note": "GO: Rec Khachanov @1.22. R019 新実装: Khachanov clay records + Walton hardcourt specialty bias で L1 優位が実態より大きい。",
        "screened_session": "_58",
        "source": "2026-04-24.json",
        "category": "ATP 1000",
        "surface": "clay",
        "rec": "Karen Khachanov",
        "rec_odds": 1.22,
        "ev": 0.056,
        "result": None, "score": None, "prediction_hit": None, "hit": None, "actual_ev": None,
        "rules_applied": ["R001", "R019"]
    },
    {
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2",
        "date": "2026-04-25",
        "match": "Auger-Aliassime F. vs Gaubas V.",
        "tier": "go",
        "quadrant": "Q1_go",
        "l1_metric": "clay_cElo",
        "l1_data": {"ce_diff": 323.9, "fav": "Felix Auger-Aliassime", "dog": "Vilius Gaubas"},
        "predicted_winner": "Felix Auger-Aliassime",
        "prediction_confidence": 86,
        "prediction_basis": "cElo +324pt / FAA 2026 form 上向き / Gaubas 22yo 若手 Madrid Q R1 seed HIT 経験のみ clay masters 経験浅",
        "odds": {"fav": 1.25, "dog": 3.95},
        "note": "GO: Rec FAA @1.25. Q3_output_a 重複 (conf 86%).",
        "screened_session": "_58",
        "source": "2026-04-24.json",
        "category": "ATP 1000",
        "surface": "clay",
        "rec": "Felix Auger-Aliassime",
        "rec_odds": 1.25,
        "ev": 0.082,
        "result": None, "score": None, "prediction_hit": None, "hit": None, "actual_ev": None,
        "rules_applied": ["R001"]
    },
    {
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2",
        "date": "2026-04-25",
        "match": "Mensik J. vs Damm M.",
        "tier": "go",
        "quadrant": "Q1_go",
        "l1_metric": "clay_cElo",
        "l1_data": {"ce_diff": 422.3, "fav": "Jakub Mensik", "dog": "Martin Damm"},
        "predicted_winner": "Jakub Mensik",
        "prediction_confidence": 92,
        "prediction_basis": "cElo +422pt 圧倒 / Damm cElo 1372 Q選手 / Mensik 20yo ブレイクスルー",
        "odds": {"fav": 1.29, "dog": 3.65},
        "note": "GO: Rec Mensik @1.29. Q3_output_a 重複 (conf 92%).",
        "screened_session": "_58",
        "source": "2026-04-24.json",
        "category": "ATP 1000",
        "surface": "clay",
        "rec": "Jakub Mensik",
        "rec_odds": 1.29,
        "ev": 0.186,
        "result": None, "score": None, "prediction_hit": None, "hit": None, "actual_ev": None,
        "rules_applied": ["R001"]
    },
    # CAUTION MARGIN downgrades
    {
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2",
        "date": "2026-04-25",
        "match": "Shapovalov D. vs Budkov Kjaer N.",
        "tier": "caution",
        "quadrant": "Q4_upset_watch",
        "caution_type": "margin",
        "l1_metric": "clay_cElo",
        "l1_data": {"ce_diff": 279.6, "fav": "Denis Shapovalov", "dog": "Nicolai Budkov Kjaer"},
        "predicted_winner": "Denis Shapovalov",
        "prediction_confidence": 72,
        "prediction_basis": "cElo +280pt / Shapovalov 2026 form 不安定 8-8 clay 2-2 / dimers 59% / Budkov Kjaer 17yo Q突破 Opelka 撃破 momentum - L4 form slump -10% 補正",
        "odds": {"fav": 1.55, "dog": 2.47},
        "rec": "Denis Shapovalov", "rec_odds": 1.55, "ev": 0.116,
        "note": "CAUTION_MARGIN (downgrade from GO): form 不安定 + Q突破 dog momentum",
        "screened_session": "_58",
        "result": None, "score": None, "prediction_hit": None, "hit": None, "actual_ev": None
    },
    {
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2",
        "date": "2026-04-25",
        "match": "Ruud C. vs Munar J.",
        "tier": "caution",
        "quadrant": "Q4_upset_watch",
        "caution_type": "margin",
        "l1_metric": "clay_cElo",
        "l1_data": {"ce_diff": 201.6, "fav": "Casper Ruud", "dog": "Jaume Munar"},
        "predicted_winner": "Casper Ruud",
        "prediction_confidence": 70,
        "prediction_basis": "cElo +202pt / Ruud defending champion but Munar スペイン人地元 Madrid (R009 -5% home crowd) / Munar 怪我明け復帰 Shevchenko R1 勝利 momentum / 当季 clay comeback",
        "odds": {"fav": 1.42, "dog": 2.90},
        "rec": "Casper Ruud", "rec_odds": 1.42, "ev": -0.006,
        "note": "CAUTION_MARGIN (downgrade from GO): Munar home WC + recovery momentum + R009 applied.",
        "screened_session": "_58",
        "result": None, "score": None, "prediction_hit": None, "hit": None, "actual_ev": None
    },
    # Q3 output_a only
    {
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2", "date": "2026-04-25",
        "match": "Zverev A. vs Navone M.",
        "tier": "skip", "quadrant": "Q3_mid",
        "l1_metric": "clay_cElo",
        "l1_data": {"ce_diff": 241.0, "fav": "Alexander Zverev", "dog": "Mariano Navone"},
        "predicted_winner": "Alexander Zverev",
        "prediction_confidence": 80,
        "prediction_basis": "cElo +241pt / Zverev #3 seed clay / Navone ARG clay specialist (R019候補) / odds 1.23 market織込済 EV-",
        "odds": {"fav": 1.23, "dog": 4.30},
        "rec": None, "rec_odds": None, "ev": None,
        "note": "Q3_mid: conf 80% EV 織込済 → skip. Session_56 新設 Q3_mid 対象.",
        "screened_session": "_58",
        "result": None, "score": None, "prediction_hit": None, "hit": None, "actual_ev": None
    },
    # ATP 4/25 SKIP entries (simplified - screening_log でも集約)
]
# append
preds.extend(new_atp_entries)

# Update screening log
atp.setdefault('screening_log', []).append({
    "session": "_58", "date": "2026-04-25",
    "source": "2026-04-24.json",
    "matches_screened": {
        "atp_madrid_r2_4_25": 18,
        "new_records": len(new_atp_entries)
    },
    "go_candidates": ["Khachanov @1.22", "Auger-Aliassime @1.25", "Mensik @1.29"],
    "caution_margin": ["Shapovalov @1.55", "Ruud @1.42"],
    "q3_output_a": ["Khachanov", "FAA", "Mensik"],
    "q3_mid": ["Zverev vs Navone 80.0%"],
    "skip_batch": [
        "Nakashima vs Blockx (diff 14.8pt L1 fail)",
        "Davidovich vs Carreno (diff 88.5 L1 fail)",
        "Cerundolo F. vs Hanfmann (diff 119.7 L1 pass but EV -12.79)",
        "Humbert vs Atmane (diff 106.8 L1 pass but conf 64.9 < 75)",
        "Merida vs Moutet (diff 97.6 L1 fail)",
        "Medvedev vs Marozsan (diff 173.3 L1 pass but conf 73.1 L4 clay aversion risk)",
        "Vallejo vs Tien (diff 37.6 L1 fail)",
        "Darderi vs Juan Manuel Cerundolo (diff 104.8 L1 pass but EV -1.75)",
        "Bublik vs Tsitsipas (diff 12.7 L1 fail coin flip)",
        "Cobolli vs Carabelli (diff 85.5 L1 fail)"
    ],
    "notes": "Phase B1 ATP R2 4/25 スクリーニング結果。GO 3件 + CAUTION 2件 + Q3_mid 1件 + SKIP 10件。R019 新実装 evidence A034 (Session_57 Paul MISS) と Tirante d. Paul 4/24 R2 7-5 6-4 で一致確認。"
})

save_json(atp_path, atp)
print(f"ATP updated: {len(preds)} predictions total")

# =====================================
# 2. WTA records 更新
# =====================================
wta_path = ROOT / "records/wta/2026.json"
wta = load_json(wta_path)
madrid_tour = wta['tournaments'][2]
mpreds = madrid_tour['predictions']

# Mertens HIT reflection
mertens_idx = next((i for i,p in enumerate(mpreds) if 'Mertens' in str(p.get('match','')) and 'Eala' in str(p.get('match',''))), None)
if mertens_idx is not None:
    p = mpreds[mertens_idx]
    p['result'] = "Mertens d. Eala"
    p['score'] = "6-2 6-1"
    p['prediction_hit'] = True
    p['hit'] = True
    p['actual_ev'] = 0.37
    p['status'] = "completed"
    p['match_duration'] = "1h 16min"
    p['outcome_note'] = "Mertens 6-2 6-1 dominant (1h16m). GO HIT +0.37u. Eala strong start but Mertens consistent depth and return game prevailed. Next R3 TBD."
    p.pop('live_status_session58', None)
    p['session_58_final'] = "HIT 2026-04-25 JST (JST 朝確定)"
    p['verification_sources'] = [
        "olympics.com Mertens advances to third round straight-sets",
        "manilabulletin.com Alex Eala bows Mertens Madrid Open",
        "justwomenssports.com Eala Falls Mertens Madrid"
    ]

# Add Mboko GO entry (new record)
new_wta_entries = [
    {
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2", "date": "2026-04-25",
        "match": "Mboko V. vs McNally C.",
        "tier": "go", "quadrant": "Q1_go",
        "l1_metric": "clay_cElo_wta",
        "l1_data": {"ce_diff": 248.9, "fav": "Victoria Mboko", "dog": "Caty McNally"},
        "predicted_winner": "Victoria Mboko",
        "prediction_confidence": 80,
        "prediction_basis": "cElo +249pt / Mboko Top10 復帰・R2 bye / McNally R1 勝利 momentum but WTA125 グレード / Mboko clay first 2026 tournament (wisdom teeth後 復帰)",
        "odds": {"fav": 1.33, "dog": 3.45},
        "note": "GO: Rec Mboko @1.33. Q3_mid 境界 (conf 80%)",
        "screened_session": "_58", "source": "2026-04-24.json",
        "rec": "Victoria Mboko", "rec_odds": 1.33, "ev": 0.074,
        "result": None, "score": None, "prediction_hit": None, "hit": None, "actual_ev": None,
        "rules_applied": ["W001"]
    },
    # Q3 output_a
    {
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2", "date": "2026-04-25",
        "match": "Sabalenka A. vs Cristian J.",
        "tier": "skip", "quadrant": "Q3_output_a",
        "l1_metric": "clay_cElo_wta",
        "l1_data": {"ce_diff": 416.5, "fav": "Aryna Sabalenka", "dog": "Jaqueline Cristian"},
        "predicted_winner": "Aryna Sabalenka",
        "prediction_confidence": 92,
        "prediction_basis": "cElo +416pt 圧倒 / Sabalenka #1 seed / Cristian clay Q突破",
        "odds": {"fav": 1.03, "dog": 13.0},
        "rec": None, "rec_odds": None, "ev": None,
        "note": "Q3_output_a conf 92% EV -5.6% (market 織込 1.03)",
        "screened_session": "_58",
        "result": None, "score": None, "prediction_hit": None, "hit": None, "actual_ev": None
    },
    {
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2", "date": "2026-04-25",
        "match": "Swiatek I. vs Li A.",
        "tier": "skip", "quadrant": "Q3_output_a",
        "l1_metric": "clay_cElo_wta",
        "l1_data": {"ce_diff": 331.4, "fav": "Iga Swiatek", "dog": "Ann Li"},
        "predicted_winner": "Iga Swiatek",
        "prediction_confidence": 87,
        "prediction_basis": "cElo +331pt / Swiatek 3x defending champ / Li USA hardcourt bias",
        "odds": {"fav": 1.05, "dog": 9.80},
        "rec": None, "rec_odds": None, "ev": None,
        "note": "Q3_output_a conf 87% EV -8.6%",
        "screened_session": "_58",
        "result": None, "score": None, "prediction_hit": None, "hit": None, "actual_ev": None
    },
    # Q3_mid
    {
        "tournament": "Mutua Madrid Open 2026",
        "round": "R2", "date": "2026-04-25",
        "match": "Pegula J. vs Boulter K.",
        "tier": "skip", "quadrant": "Q3_mid",
        "l1_metric": "clay_cElo_wta",
        "l1_data": {"ce_diff": 248.3, "fav": "Jessica Pegula", "dog": "Katie Boulter"},
        "predicted_winner": "Jessica Pegula",
        "prediction_confidence": 81,
        "prediction_basis": "cElo +248pt / Pegula #3 seed / Boulter clay 経験少",
        "odds": {"fav": 1.14, "dog": 5.60},
        "rec": None, "rec_odds": None, "ev": None,
        "note": "Q3_mid (80-84%) conf 80.7% EV -8.0% 市場織込済",
        "screened_session": "_58",
        "result": None, "score": None, "prediction_hit": None, "hit": None, "actual_ev": None
    },
    # Downgrade Paolini
    {
        "tournament": "Mutua Madrid Open 2026",
        "round": "R3", "date": "2026-04-25",
        "match": "Paolini J. vs Baptiste H.",
        "tier": "skip", "quadrant": "skip",
        "l1_metric": "clay_cElo_wta",
        "l1_data": {"ce_diff": 201.0, "fav": "Jasmine Paolini", "dog": "Hailey Baptiste"},
        "predicted_winner": "Jasmine Paolini",
        "prediction_confidence": 66,
        "prediction_basis": "cElo +201pt / Paolini P007 当季 form slump 53%勝率 前年名声 cElo 過大 / Baptiste WTA125 winner momentum / form slump L4 -10% → conf 66% → SKIP",
        "odds": {"fav": 1.61, "dog": 2.33},
        "rec": None, "rec_odds": None, "ev": None,
        "note": "SKIP (initial GO candidate downgrade). P007 form slump + R3 opponent uncertainty. A007 Sonmez upset の前例があり。",
        "screened_session": "_58",
        "result": None, "score": None, "prediction_hit": None, "hit": None, "actual_ev": None
    },
]
mpreds.extend(new_wta_entries)

# Update screening log
wta.setdefault('screening_log', []).append({
    "session": "_58", "date": "2026-04-25",
    "source": "2026-04-24.json",
    "matches_screened": {"wta_madrid_r2_4_25": 11, "new_records": len(new_wta_entries)},
    "go_candidates": ["Mboko @1.33"],
    "q3_output_a": ["Sabalenka 91.7%", "Swiatek 87.1%"],
    "q3_mid": ["Pegula 80.7%", "Mboko 80.7% (GO 重複)"],
    "skip_batch": [
        "Tauson vs Siniakova (diff 31 L1 fail)",
        "Bencic vs Shnaider (diff -1.1 L1 fail)",
        "Osaka vs Kalinina (diff 7.6 L1 fail)",
        "Andreeva vs Galfi (Galfi cElo unknown)",
        "Jovic vs Fernandez (diff 29 L1 fail)",
        "Bondar vs Samsonova (diff -15.6 L1 fail - fav reversed)",
        "Paolini vs Baptiste R3 (P007 form slump downgrade)"
    ],
    "completed_updates": [
        "Mertens d. Eala 6-2 6-1 GO HIT +0.37u (Session_58 確定)"
    ]
})

save_json(wta_path, wta)
print(f"WTA updated")

# =====================================
# 3. NRL records 更新
# =====================================
nrl_path = ROOT / "records/nrl/2026.json"
nrl = load_json(nrl_path)
nrl_preds = nrl.get('predictions', [])

# Find R9 entries - update existing skip to go for Warriors and Manly
warriors_idx = next((i for i,p in enumerate(nrl_preds) if 'Warriors' in str(p.get('match','')) and 'Dolphins' in str(p.get('match','')) and p.get('round') == 'R9'), None)
if warriors_idx is not None:
    p = nrl_preds[warriors_idx]
    p['tier'] = 'go'
    p['quadrant'] = 'Q1_go'
    p['l1_metric'] = 'pd_per_game'
    p['l1_data'] = {"pd_diff": 16.5, "fav": "NZ Warriors (+12.0/G)", "dog": "Dolphins (-4.5/G)"}
    p['predicted_winner'] = "NZ Warriors"
    p['prediction_confidence'] = 78
    p['prediction_basis'] = "PD/G diff +16.5pt / Warriors 5W2L home / Dolphins 2W4L collapse / Home advantage NZ"
    p['odds'] = {"fav": 1.45, "dog": 2.55}
    p['rec'] = "NZ Warriors"
    p['rec_odds'] = 1.45
    p['ev'] = 0.131
    p['screened_session'] = '_58'
    p['source'] = '2026-04-24.json'
    p['rules_applied'] = p.get('rules_applied', []) + ["U008_modified"]

manly_idx = next((i for i,p in enumerate(nrl_preds) if 'Manly' in str(p.get('match','')) and 'Eels' in str(p.get('match','')) and p.get('round') == 'R9'), None)
if manly_idx is not None:
    p = nrl_preds[manly_idx]
    p['tier'] = 'go'
    p['quadrant'] = 'Q1_go'
    p['l1_metric'] = 'pd_per_game'
    p['l1_data'] = {"pd_diff": 18.3, "fav": "Manly Sea Eagles (+6.33/G)", "dog": "Eels (-12.0/G)"}
    p['predicted_winner'] = "Manly Sea Eagles"
    p['prediction_confidence'] = 80
    p['prediction_basis'] = "PD/G diff +18.3pt / Manly 3W3L home / Eels 3W4L PD-12/G / Eels collapse pattern"
    p['odds'] = {"fav": 1.38, "dog": 2.80}
    p['rec'] = "Manly Sea Eagles"
    p['rec_odds'] = 1.38
    p['ev'] = 0.104
    p['screened_session'] = '_58'
    p['source'] = '2026-04-24.json'

nrl.setdefault('screening_log', []).append({
    "session": "_58", "date": "2026-04-25",
    "source": "2026-04-24.json",
    "matches_screened": {"nrl_r9": 7},
    "go_candidates": ["Warriors @1.45", "Manly @1.38"],
    "q3_output_a": ["Roosters road @1.12 (89.3% market)", "Panthers road @1.17 (85.5% market)"],
    "skip_batch": [
        "Storm vs Rabbitohs (Storm PD/G weaker -0.29 but home odds 1.51 diff-wise fail)",
        "Bulldogs vs Cowboys (diff 0.12 L1 fail)",
        "Storm vs Dolphins 5/1 (L1 fail)"
    ],
    "notes": "Phase C NRL R9. GO 2件昇格 (Warriors / Manly)."
})
save_json(nrl_path, nrl)
print(f"NRL updated")

# =====================================
# 4. NHL records 更新 (G3 結果反映 + CAUTION G4)
# =====================================
# G3 for MTL-TBL/UTA-VGK/ANA-EDM - still pending result, just add screening
nhl_path = ROOT / "records/nhl/2025-26.json"
nhl = load_json(nhl_path)
nhl.setdefault('screening_log', []).append({
    "session": "_58", "date": "2026-04-25",
    "source": "2026-04-24.json",
    "matches_screened": {"nhl_g3_pending": 3, "nhl_g4_new": 5},
    "go_candidates": [],
    "caution_margin": ["PHI G4 @1.83 home close-out 3-0 (L1 xGF% tied but series context EV+19%)"],
    "q4_upset_watch": [
        "ANA home G3 @2.11 (A030 evidence 2/3 type_a_watch)",
        "MTL home G3 @2.01 (A021 young core momentum)"
    ],
    "skip_batch": [
        "UTA-VGK G3 (L1 xGF% 3pt diff fail)",
        "OTT-CAR G4 (xGF 1pt)",
        "MIN-DAL G4 (xGF 0 tied)",
        "BOS-BUF G4 (BOS elim 0-3)",
        "LAK-COL G4 (LAK elim 0-3 COL road close-out EV-)"
    ],
    "notes": "Phase B3 NHL. xGF% strict L1 で GO なし。PHI G4 series 3-0 home close-out を CAUTION_MARGIN として追跡。"
})
save_json(nhl_path, nhl)
print(f"NHL screening log updated")

# =====================================
# 5. NBA records - screening log only (all SKIP)
# =====================================
nba_path = ROOT / "records/nba/2025-26.json"
nba = load_json(nba_path)
nba.setdefault('screening_log', []).append({
    "session": "_58", "date": "2026-04-25",
    "source": "2026-04-24.json",
    "matches_screened": {"nba_g3_g4": 8},
    "go_candidates": [],
    "q4_upset_watch": [
        "LAL @3.70 road G3 sweep attempt (series 2-0 LAL at HOU home - KD 復帰 status)",
        "SAS road @1.70 G3 (Wembanyama concussion G2 status)"
    ],
    "skip_batch": [
        "BOS vs PHI G3 (NRtg diff 6pt but PHI home G2 crushed win momentum - EV-)",
        "HOU-LAL G3 (HOU home +fav market overrate)",
        "DET vs ORL G3 (DET big road fav market織込)",
        "OKC vs PHX G3 (OKC sweep setup market織込 1.22)",
        "ATL vs NYK G3 (ATL 1-1 home slight fav)",
        "MIN vs DEN G4 (slightly unclear series status)",
        "TOR vs CLE G4 (CLE road fav 2-0)"
    ],
    "notes": "Phase B4 NBA PO G3/G4. L1 NRtg 差を market が全て織込済 → 全 SKIP。Q4_upset_watch 2件追跡。"
})
save_json(nba_path, nba)
print(f"NBA screening log updated")

# =====================================
# 6. UFL/AHL/SL records - screening log only
# =====================================
for fn, label, skip_list in [
    (ROOT / "records/ufl/2026.json", "UFL W5",
     ["DC @1.37 road vs Stallions (Basic 78% 未達)",
      "ORL @1.63 home vs STL (conf 61% < 78%)",
      "COL @1.44 road vs HOU (1-3 Aviators W4 UPSET 後 let-down リスク CAUTION)",
      "REN @1.26 home vs LOU (Basic conf 79% 境界 EV -0.46% SKIP)"]),
    (ROOT / "records/ahl/2025-26.json", "AHL PO",
     ["6試合全 SKIP (Basic tier conf <65% EV 市場織込済)"]),
    (ROOT / "records/superleague/2026.json", "SL R9",
     ["Warrington @1.72 (conf 58.1%)",
      "Hull FC @1.66 road (conf 60.2%)",
      "Leeds @1.18 home vs Catalans (conf 84.7% EV +0.1% Basic 78% 未達・EV不足)",
      "Bradford vs HKR (odds 1.00 invalid)",
      "St Helens @1.28 home (conf 78.1% EV +5.0% Basic 7% 未達)"]),
]:
    try:
        d = load_json(fn)
        d.setdefault('screening_log', []).append({
            "session": "_58", "date": "2026-04-25",
            "source": "2026-04-24.json",
            "matches_screened": {label: len(skip_list)},
            "go_candidates": [],
            "skip_batch": skip_list,
            "notes": f"Phase C {label}. 全 SKIP (Basic Tier 閾値未達)."
        })
        save_json(fn, d)
        print(f"{label} screening log updated")
    except Exception as e:
        print(f"{label} ERROR: {e}")

print("\n=== Records update complete ===")
