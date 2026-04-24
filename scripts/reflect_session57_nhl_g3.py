"""Session_57 NHL G3 結果反映 + date 訂正 (CE021/CE022)"""
import json
from pathlib import Path

ROOT = Path("C:/Users/ohwada/Desktop/claude_sport")

nhl_path = ROOT / "records/nhl/2025-26.json"
with open(nhl_path, encoding="utf-8-sig") as f:
    d = json.load(f)

updates = {
    53: {  # BOS vs BUF G3 → BUF 3-1 BOS (UPSET)
        "result": "Buffalo Sabres 3-1 Boston Bruins",
        "score": "3-1",
        "winner": "Buffalo Sabres",
        "prediction_hit": False,
        "hit": None,
        "actual_ev": 0.0,
        "outcome_note": "SKIP no-bet / 予測MISS. BUF took 2-1 series lead at TD Garden. Byram/Tuch/Ostlund(EN) scored. Lyon 24 saves for BUF in first start of series. Jeannot sole Bruins goal. This follows BOS G2 rebound HIT → G3 road UPSET continues series volatility.",
        "miss_layer": "L1_xGF_vs_motivation",
        "miss_analysis": "BOS home favorite 但し G2 home rebound (P027 候補 evidence) 成立済み。G3 で BUF が再度 take control (BUF G1 UPSET winner). road team advantage + goaltending duel variance. P027 は G2 のみで成立しており G3 継続性は別パターン。G3 home rebound rule は形成されず。",
        "rule_linked": None,
        "verification_sources": ["nhl.com buffalo-sabres-boston-bruins-game-3-recap-april-23-2026", "nesn.com Bruins vs Sabres Final Score Boston Falls", "nbcsportsboston.com Alex Lyon shines"],
    },
    54: {  # OTT vs CAR G3 → CAR 2-1 OTT (caution_margin)
        "result": "Carolina Hurricanes 2-1 Ottawa Senators",
        "score": "2-1",
        "winner": "Carolina Hurricanes",
        "prediction_hit": False,
        "hit": None,
        "actual_ev": 0.0,
        "outcome_note": "CAUTION_MARGIN no-bet / 予測MISS. OTT home fav だが CAR 3-0 series lead。Stankoven franchise first player 3G in streak + Blake GWG 17:29. Hurricanes on brink of elimination OTT.",
        "miss_layer": "L4_home_motivation_insufficient",
        "miss_analysis": "OTT home G3 + CAR road sweeping momentum. home bounce 期待したが CAR 3-0 sweep 濃厚. P027 home rebound 理論の反例 (OTT は G1/G2 両方 road で MISS してた前提で G3 home 期待したが CAR のシリーズ支配力が上回った)。",
        "rule_linked": None,
        "verification_sources": ["nhl.com carolina-hurricanes-ottawa-senators-game-3-recap-april-23-2026", "espn.com 401869783 hurricanes-senators"],
    },
    55: {  # LAK vs COL G3 → COL 4-2 LAK
        "result": "Colorado Avalanche 4-2 Los Angeles Kings",
        "score": "4-2",
        "winner": "Colorado Avalanche",
        "prediction_hit": True,
        "hit": None,
        "actual_ev": 0.0,
        "outcome_note": "SKIP no-bet / 予測HIT. COL 3-0 series lead 準スウィープ達成 (road G3 win). Lehkonen 1G/1A + Landeskog/Makar/Nelson G. Wedgewood 24 saves. LAK home advantage 通じず.",
        "verification_sources": ["nhl.com colorado-avalanche-los-angeles-kings-game-3-recap-april-23-2026"],
    },
    59: {  # MIN vs DAL G3 → DAL 4-3 MIN 2OT (date 4/26→4/23 訂正 CE022)
        "date": "2026-04-23",
        "ce_correction": "CE022: date was incorrectly recorded as 2026-04-26 (session data input error). Actual game was played 2026-04-22 ET = 2026-04-23 JST. Corrected Session_57 2026-04-24.",
        "result": "Dallas Stars 4-3 Minnesota Wild (2OT)",
        "score": "4-3 (2OT)",
        "winner": "Dallas Stars",
        "prediction_hit": False,
        "hit": None,
        "actual_ev": 0.0,
        "outcome_note": "SKIP no-bet / 予測MISS. DAL 2-1 series lead (BOS-BUF型). Johnston scored 6th GWG before age 23. PP decisive in 2OT. MIN G1 UPSET 後の G2/G3 は DAL 連取 → A028 反動パターン. P027 evidence candidate (G1 UPSET 後 G2 fav home rebound + G3 継続).",
        "miss_layer": "L1_series_reversion",
        "miss_analysis": "MIN G1 UPSET 6-1 の過剰反応補正。G2 DAL rebound 済、G3 road DAL 2OT で確定。これは P027 (G1 UPSET 後の G2 home rebound +3〜+5%) が G3 road でも継続する示唆. P025 N021 xGF priority は G1 では正解だったが G2/G3 では seed が戻る。",
        "rule_linked": "P027_candidate_extension",
        "verification_sources": ["nhl.com dallas-stars-minnesota-wild-game-3-recap-april-22-2026", "espn.com 401869782"],
    },
    60: {  # PHI vs PIT G3 → PHI 5-2 PIT (date 4/26→4/23 訂正 CE021)
        "date": "2026-04-23",
        "ce_correction": "CE021: date was incorrectly recorded as 2026-04-26 (session data input error). Actual game was played 2026-04-22 ET = 2026-04-23 JST. Corrected Session_57 2026-04-24.",
        "result": "Philadelphia Flyers 5-2 Pittsburgh Penguins",
        "score": "5-2",
        "winner": "Philadelphia Flyers",
        "prediction_hit": True,
        "hit": None,
        "actual_ev": 0.0,
        "outcome_note": "SKIP no-bet / 予測HIT. PHI 3-0 series lead 準スウィープ. Zegras 1G/1A + Cates 1G/1A + Ristolainen/Seeler G. PHI young energy/rivalry/Crosby fade (P018/P019) 3連続成立. P018 evidence 3件目 → N019 implement 判断候補.",
        "rule_linked": "P018_evidence_3rd_candidate",
        "verification_sources": ["nhl.com pittsburgh-penguins-philadelphia-flyers-game-3-recap-april-22-2026", "pensburgh.com Game 3 Recap", "espn.com 401869796"],
    },
}

for idx, upd in updates.items():
    g = d["games"][idx]
    for k, v in upd.items():
        g[k] = v

d["last_updated"] = "2026-04-24"

with open(nhl_path, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"NHL G3 updated: {len(updates)} entries")
