"""Session_57 (2026-04-24) Madrid 4/23-24 結果反映スクリプト
PA068 / PA076 / PA069 / PA070 / CE019 / CE020 一括処理
"""
import json
from pathlib import Path

ROOT = Path("C:/Users/ohwada/Desktop/claude_sport")

def load_json(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

def save_json(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# ============ ATP 反映 ============
atp_path = ROOT / "records/tennis/2026-ATP.json"
atp = load_json(atp_path)

atp_updates = {
    108: {  # Popyrin vs Damm 4/23 Q4_upset_watch
        "result": "Damm d. Popyrin",
        "score": "7-6(7) 6-4",
        "prediction_hit": False,
        "outcome_note": "UPSET_realized: Damm (underdog) won. Q4_upset_watch HIT (UPSET detected successfully).",
        "verification_sources": ["atptour.com/en/news/madrid-2026-results", "perfect-tennis.com day-two-recap"],
    },
    109: {  # Tsitsipas vs Kypson 4/23 CAUTION_MARGIN
        "result": "Tsitsipas d. Kypson",
        "score": "3-6 6-7(6) 7-6(4)",
        "prediction_hit": True,
        "hit": None,
        "actual_ev": 0.0,
        "outcome_note": "Tsitsipas rallied from 1 set + 2 points down in 2nd-set TB. CAUTION_MARGIN no-bet / 本命予測HIT. snapped 3-match losing streak.",
        "verification_sources": ["yardbarker.com ATP Madrid Open Day Two Round-Up", "tennistonic.com Tsitsipas outlasts Kypson", "greekcitytimes.com Tsitsipas Madrid Open"],
    },
    111: {  # Vallejo vs Dimitrov 4/23 skip
        "result": "Vallejo d. Dimitrov",
        "score": "6-4 6-4",
        "prediction_hit": True,
        "outcome_note": "predicted Vallejo (WC local) correct. debut upset level but pred_winner matched.",
        "verification_sources": ["atptour.com/en/news/madrid-2026-video-recap-day-2"],
    },
    114: {  # Carabelli vs Monfils 4/23 skip
        "result": "Carabelli d. Monfils",
        "score": "6-3 6-4",
        "prediction_hit": True,
        "outcome_note": "Monfils farewell exit. Carabelli 予測HIT.",
        "verification_sources": ["tennismajors.com Ugo Carabelli sends Monfils into Madrid night"],
    },
    115: {  # Opelka vs Budkov Kjaer 4/23 CAUTION
        "result": "Budkov Kjaer d. Opelka (ret. 5-3)",
        "score": "RET",
        "prediction_hit": False,
        "outcome_note": "Opelka retired at 5-3 due to injury. CAUTION no-bet / 予測MISS (Opelka pred). L4_External: retirement.",
        "miss_layer": "L4_External",
        "miss_analysis": "Opelka injury retirement at 5-3 down. Not a true upset - external factor.",
        "verification_sources": ["yardbarker.com ATP Madrid Day Two Round-Up Opelka retires injured"],
    },
    123: {  # Paul vs Tirante 4/24 GO
        "result": "Tirante d. Paul",
        "score": "6-2 6-4",
        "prediction_hit": False,
        "hit": False,
        "actual_ev": -1.0,
        "outcome_note": "UPSET MISS. Tirante (ARG clay specialist) d. Paul straight sets. P012 clay-specialist vs hardcourt-bias pattern evidence candidate.",
        "miss_layer": "L1_clay_specialist_bias",
        "miss_analysis": "Tirante ARG clay specialist defeated Paul in straight sets. Paul primarily a hard-court player. P012 (clay specialist vs hardcourt) evidence 3/3 候補 — 既存 A011 (Carabelli d. Khachanov) + A024 (Droguet d. Virtanen) と同パターン. 今回が decisive 3件目で R019 implement 判断要.",
        "rule_linked": "P012_candidate",
        "verification_sources": ["atptour.com/en/news/madrid-2026-results", "dimers.com tirante-paul"],
    },
    125: {  # Musetti vs Hurkacz 4/24 CAUTION_WAITING
        "result": "Musetti d. Hurkacz",
        "score": "6-4 7-6",
        "prediction_hit": True,
        "hit": None,
        "actual_ev": 0.0,
        "outcome_note": "Musetti advances firmly in 2 sets. CAUTION_WAITING no-bet (arm injury concern) / 本命予測HIT. Next R3 vs Griekspoor.",
        "verification_sources": ["sport.sky.it Musetti Hurkacz", "corrieredellosport.it", "puntodebreak.com Musetti advances firmly"],
    },
}

for idx, upd in atp_updates.items():
    p = atp["predictions"][idx]
    for k, v in upd.items():
        p[k] = v

atp["last_updated"] = "2026-04-24"

# ============ WTA 反映 ============
wta_path = ROOT / "records/wta/2026.json"
wta = load_json(wta_path)

# Madrid tournament を探す
madrid_idx = None
for i, t in enumerate(wta["tournaments"]):
    if "Madrid" in t.get("name", ""):
        madrid_idx = i
        break

madrid_preds = wta["tournaments"][madrid_idx]["predictions"]

wta_updates = {
    6: {  # Bencic vs Martincova 4/23 Q3_output_a → 実は相手名誤記 Marcinko が正しい
        "match": "Bencic B. vs Marcinko P.",  # CE020 訂正
        "ce_correction": "CE020: opponent name 'Martincova P.' was incorrect. Actual opponent was Petra Marcinko (Croatian, teenager). corrected 2026-04-24.",
        "result": "Bencic d. Marcinko",
        "score": "6-4 6-2",
        "prediction_hit": True,
        "outcome_note": "Q3_output_a HIT. Bencic 5 aces/64% 1stSrv/78% 1stSrvWon / 5 breaks. match 1h24m. daughter's 2nd birthday win.",
        "verification_sources": ["lastwordonsports.com WTA Madrid Best Bets Bencic Marcinko", "tennisuptodate.com Bencic celebrates daughters birthday", "tennistonic.com Bencic prevails over Marcinko", "dimers.com bencic-marcinko"],
    },
    9: {  # Kalinskaya vs Galfi 4/23 Q4_upset_watch caution_margin
        "result": "Galfi d. Kalinskaya",
        "score": "6-3 6-3",
        "prediction_hit": False,
        "hit": None,
        "actual_ev": 0.0,
        "outcome_note": "UPSET_realized (Q4_upset_watch HIT). Galfi WTA No.117 d. seed No.22 Kalinskaya 66 min. Q4 upset detection succeeded.",
        "miss_layer": "L1_small_divergence",
        "miss_analysis": "Galfi previously GO HIT 4/21 Madrid Q Final (vs Vidmanova). Form continuation — Q carrier momentum + Kalinskaya underperformance on clay. Q4_upset_watch の検知パターンとしては UPSET detection の成功例.",
        "rule_linked": "WTA_Q_carrier_momentum",
        "verification_sources": ["WTA official scores", "ubitennis.com WTA Madrid"],
    },
    10: {  # Swiatek vs Snigur 4/23 Q3_output_a
        "result": "Swiatek d. Snigur",
        "score": "6-1 6-2",
        "prediction_hit": True,
        "outcome_note": "Q3_output_a HIT. Swiatek straight-sets dominance.",
        "verification_sources": ["skysports.com Sabalenka Swiatek Madrid", "flashscore.com Madrid roundup"],
    },
    11: {  # Paolini vs Siegemund 4/23 Q4_upset_watch caution_track
        "result": "Paolini d. Siegemund",
        "score": "3-6 6-2 6-4",
        "prediction_hit": True,
        "hit": None,
        "actual_ev": 0.0,
        "outcome_note": "Paolini comeback win 3 sets (lost 1st set). Q4_upset_watch UPSET not realized, fav Paolini HIT.",
        "verification_sources": ["ubitennis.com Paolini comeback", "oasport.it Paolini vince in rimonta"],
    },
    14: {  # Sabalenka vs Stearns 4/23 Q3_output_a
        "result": "Sabalenka d. Stearns",
        "score": "7-5 6-3",
        "prediction_hit": True,
        "outcome_note": "Q3_output_a HIT. Sabalenka 2026 clay-court debut. some rust but advanced.",
        "verification_sources": ["skysports.com Sabalenka clay debut Madrid", "tennis.com Sabalenka 2026 clay-court debut"],
    },
    18: {  # Osaka vs Osorio 4/23 Q4_upset_watch
        "result": "Osaka d. Osorio",
        "score": "6-2 7-5",
        "prediction_hit": True,
        "hit": None,
        "actual_ev": 0.0,
        "outcome_note": "Osaka 2026 first clay win. Q4_upset_watch UPSET not realized, fav Osaka HIT. Osaka advances to R3 vs Kalinina.",
        "verification_sources": ["tennisworldusa.org Naomi Osaka wins first match on clay 2026", "tennistonic.com Osaka ousts Osorio"],
    },
    19: {  # Andreeva vs Udvardy 4/23 Q3_output_a
        "result": "Andreeva d. Udvardy",
        "score": "7-5 6-2",
        "prediction_hit": True,
        "outcome_note": "Q3_output_a HIT. Andreeva most clay wins on tour in 2026.",
        "verification_sources": ["wtatennis.com By the Numbers Andreeva Madrid", "wtatennis.com Andreeva vs Udvardy R64"],
    },
    31: {  # Keys vs Zhang 4/24 GO
        "result": "VOID (Keys WITHDREW due to illness)",
        "score": "W/O",
        "prediction_hit": None,
        "hit": None,  # VOID bet
        "actual_ev": 0.0,
        "outcome_note": "Keys WITHDREW 30 min before her match due to illness. VOID (no bet P&L). Potapova (LL) replaced her. Advisory: R020/GEN003 same-day info check should have flagged earlier if possible.",
        "verification_sources": ["puntodebreak.com Madison Keys withdraws half an hour before match", "wtatennis.com Keys withdraws illness", "koranmanado.co.id Madison Keys Withdraws"],
    },
    35: {  # Mertens vs Eala 4/23→4/24 CE019 訂正 + pending 維持
        "date": "2026-04-24",  # 正しい日付に訂正
        "ce_correction": "CE019: date was incorrectly recorded as 2026-04-23 (Session_52 misclassified). Mertens is seeded (R1 bye) and first match is R2 vs Eala on 2026-04-24. Corrected Session_57 2026-04-24.",
        "round": "R2",  # R1 bye なので初戦は R2
        "outcome_note_pre": "awaiting result 2026-04-24. Eala d. Pavlyuchenkova 6-3 6-3 in R1.",
    },
}

for idx, upd in wta_updates.items():
    p = madrid_preds[idx]
    for k, v in upd.items():
        p[k] = v

wta["last_updated"] = "2026-04-24"

# Save
save_json(atp_path, atp)
save_json(wta_path, wta)

print(f"ATP updated: {len(atp_updates)} entries")
print(f"WTA updated: {len(wta_updates)} entries")
print("Saved successfully.")
