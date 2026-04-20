# Session_45: NBA/NHL G1 結果を一括記録 + multi_bets output_a 更新 + upset_patterns 追加
import json
from pathlib import Path

BASE = Path(r"C:\Users\ohwada\Desktop\claude_sport")

# =========================
# 1. NBA records に G1 結果追加
# =========================
nba_path = BASE / "records" / "nba" / "2025-26.json"
nba = json.load(open(nba_path, encoding="utf-8-sig"))
games = nba.setdefault("games", [])

nba_g1_results = [
    # (match, date, fav_team, fav_odds, dog_team, dog_odds, winner, score, go_pick_conf, tier, output_a_rank)
    ("CLE vs TOR G1", "2026-04-18", "Cleveland Cavaliers", 1.27, "Toronto Raptors", 3.8, "Cleveland Cavaliers", "126-113", 75, "go_candidate_market_only", None),
    ("BOS vs PHI G1", "2026-04-19", "Boston Celtics", 1.11, "Philadelphia 76ers", 6.4, "Boston Celtics", "blowout 32pt margin (franchise record)", 86, "output_a", 9),
    ("SAS vs POR G1", "2026-04-20", "San Antonio Spurs", 1.18, "Portland Trail Blazers", 5.8, "San Antonio Spurs", "Wembanyama 35pts Spurs franchise playoff record", 87, "go_active_PA017", None),
    ("DEN vs MIN G1", "2026-04-19", "Denver Nuggets", 1.39, "Minnesota Timberwolves", 3.05, "Denver Nuggets", "Jokic+Murray 55pts 18reb 18ast", 68, "skip_market", None),
    ("NYK vs ATL G1", "2026-04-20", "New York Knicks", 1.45, "Atlanta Hawks", 2.8, "New York Knicks", "113-102", 66, "skip_market", None),
    ("DET vs ORL G1", "2026-04-19", "Detroit Pistons", 1.22, "Orlando Magic", 4.2, "Orlando Magic", "112-101 UPSET", 78, "go_candidate_UPSET", None),
    ("OKC vs PHX G1", "2026-04-20", "Oklahoma City Thunder", 1.04, "Phoenix Suns", 10.0, "Oklahoma City Thunder", "119-84 blowout, SGA 25pts 7ast 2blk", 91, "output_a", 11),
    ("LAL vs HOU G1", "2026-04-20", "Houston Rockets", 1.51, "Los Angeles Lakers", 2.5, None, "pending", 63, "skip_market", None),
]

added = 0
for m, d, fav, fo, dog, do, winner, score, conf, tier_cat, oa_rank in nba_g1_results:
    # 重複確認
    exists = any(g.get("match","")==m and g.get("date","")==d for g in games)
    if exists:
        continue
    pred_hit = (winner == fav) if winner else None
    entry = {
        "match": m,
        "date": d,
        "round": "Playoffs R1 G1",
        "sport": "nba",
        "favorite": fav,
        "fav_odds": fo,
        "dog": dog,
        "dog_odds": do,
        "predicted_winner": fav,
        "prediction_confidence": conf,
        "tier": tier_cat,
        "result": winner,
        "score": score,
        "prediction_hit": pred_hit,
        "rec": None, "rec_odds": None, "ev": None,
        "hit": None, "actual_ev": None,
        "source": "Session_45 WebSearch (NBA.com/ESPN) 一次確認",
        "notes": "DET MISS = UPSET (Orlando upset Detroit fav @1.22). Others all fav HIT. Output-A candidates (BOS/SAS/OKC) 3/3 HIT confirmed."
    }
    if tier_cat == "output_a":
        entry["output_a_rank"] = oa_rank
    games.append(entry)
    added += 1

# NBA summary 更新
s = nba.setdefault("summary", {})
s["last_updated"] = "2026-04-20 Session_45"
nba["last_updated"] = "2026-04-20"

with open(nba_path, 'w', encoding='utf-8') as f:
    json.dump(nba, f, ensure_ascii=False, indent=2)
print(f"NBA: +{added} G1 results")

# =========================
# 2. NHL records に G1 結果追加
# =========================
nhl_path = BASE / "records" / "nhl" / "2025-26.json"
nhl = json.load(open(nhl_path, encoding="utf-8-sig"))
nhl_games = nhl.setdefault("games", [])

nhl_g1_results = [
    ("BUF vs BOS G1", "2026-04-20", "Buffalo Sabres", 1.59, "Boston Bruins", 2.32, "Buffalo Sabres", "4-3", 60, "skip_market"),
    ("CAR vs OTT G1", "2026-04-20", "Carolina Hurricanes", 1.68, "Ottawa Senators", 2.25, "Carolina Hurricanes", "2-0 shutout", 57, "skip_market"),
    ("PIT vs PHI G1", "2026-04-20", "Pittsburgh Penguins", 1.68, "Philadelphia Flyers", 2.25, "Philadelphia Flyers", "3-2 UPSET", 57, "skip_market_UPSET"),
    ("DAL vs MIN G1", "2026-04-20", "Dallas Stars", 1.79, "Minnesota Wild", 2.08, "Minnesota Wild", "6-1 BLOWOUT UPSET", 53, "pickem_UPSET"),
    ("VGK vs UTA G1", "2026-04-20", "Vegas Golden Knights", 1.63, "Utah Mammoth", 2.24, "Vegas Golden Knights", "4-2", 58, "skip_market"),
    ("EDM vs ANA G1", "2026-04-20", "Edmonton Oilers", 1.58, "Anaheim Ducks", 2.46, None, "pending (late 4/20)", 60, "skip_market"),
]

nhl_added = 0
for m, d, fav, fo, dog, do, winner, score, conf, tier_cat in nhl_g1_results:
    exists = any(g.get("match","")==m and g.get("date","")==d for g in nhl_games)
    if exists:
        continue
    pred_hit = (winner == fav) if winner else None
    entry = {
        "match": m, "date": d, "round": "Stanley Cup Playoffs R1 G1",
        "sport": "nhl",
        "favorite": fav, "fav_odds": fo, "dog": dog, "dog_odds": do,
        "predicted_winner": fav,
        "prediction_confidence": conf,
        "tier": tier_cat,
        "result": winner, "score": score,
        "prediction_hit": pred_hit,
        "rec": None, "rec_odds": None, "ev": None,
        "hit": None, "actual_ev": None,
        "source": "Session_45 WebSearch (NHL.com) 一次確認"
    }
    nhl_games.append(entry)
    nhl_added += 1

nhl["last_updated"] = "2026-04-20"
with open(nhl_path, 'w', encoding='utf-8') as f:
    json.dump(nhl, f, ensure_ascii=False, indent=2)
print(f"NHL: +{nhl_added} G1 results")

# =========================
# 3. upset_patterns に 3件 UPSET 追加
# =========================
up_path = BASE / "stats" / "upset_patterns.json"
up = json.load(open(up_path, encoding="utf-8-sig"))
cu = up.setdefault("confirmed_upsets", [])

new_upsets = [
    {
        "upset_id": "A026", "date": "2026-04-19", "sport": "nba",
        "tournament": "NBA Playoffs R1", "round": "G1",
        "match": "Orlando Magic @ Detroit Pistons",
        "market_favorite": "Detroit Pistons", "fav_odds": 1.22, "dog_odds": 4.2,
        "result": "Orlando 112-101 Detroit (only road G1 win of that day)",
        "uf_count": 2,
        "uf_factors": {
            "UF02": "Orlando Banchero 23pts 9reb Paolo breakout",
            "UFA02": "Detroit young playoff inexperience vs Orlando previous R1 experience"
        },
        "market_divergence_pp": 35,
        "upset_pick_feasibility": "UF2 + 35pp - borderline UPSET_PICK (UF不足だが乖離大きい). DEToverrated / ORL underrated gap.",
        "rule_linked": None
    },
    {
        "upset_id": "A027", "date": "2026-04-20", "sport": "nhl",
        "tournament": "Stanley Cup Playoffs R1", "round": "G1",
        "match": "Philadelphia Flyers @ Pittsburgh Penguins",
        "market_favorite": "Pittsburgh Penguins", "fav_odds": 1.68, "dog_odds": 2.25,
        "result": "Philadelphia 3-2 Pittsburgh",
        "uf_count": 2,
        "uf_factors": {
            "UFH04": "PIT regular season late slump (Crosby age)",
            "UFA02": "PHI young energy + rivalry motivation"
        },
        "market_divergence_pp": 16,
        "upset_pick_feasibility": "UF2 + 16pp - borderline. CAUTION no-bet would have been right.",
        "rule_linked": None
    },
    {
        "upset_id": "A028", "date": "2026-04-20", "sport": "nhl",
        "tournament": "Stanley Cup Playoffs R1", "round": "G1",
        "match": "Minnesota Wild @ Dallas Stars",
        "market_favorite": "Dallas Stars", "fav_odds": 1.79, "dog_odds": 2.08,
        "result": "Minnesota 6-1 Dallas (BLOWOUT UPSET)",
        "uf_count": 3,
        "uf_factors": {
            "UF02": "MIN 5v5 xGF% advantage (MoneyPuck data noted in Session_32)",
            "UFH04": "DAL regular season fade / goaltending injury?",
            "UFA03": "MIN goalie hot start (6-1 score suggests complete domination)"
        },
        "market_divergence_pp": 9,
        "upset_pick_feasibility": "UF3 + 9pp < 15pp. Below UPSET_PICK but MIN high-xGF% noted in advance. CAUTION格妥当。",
        "rule_linked": None
    }
]

existing_ids = {u.get("upset_id") for u in cu}
ups_added = 0
for nu in new_upsets:
    if nu["upset_id"] not in existing_ids:
        cu.append(nu)
        ups_added += 1

up["last_updated"] = "2026-04-20 Session_45"
with open(up_path, 'w', encoding='utf-8') as f:
    json.dump(up, f, ensure_ascii=False, indent=2)
print(f"upset_patterns: +{ups_added} upsets")

# =========================
# 4. multi_bets.json session_45 の output_a 結果更新
# =========================
mb_path = BASE / "records" / "multi_bets.json"
mb = json.load(open(mb_path, encoding="utf-8-sig"))
for sess in mb["sessions"]:
    if sess.get("session_id") == "_45":
        # BOS(rank9) / SAS(rank10) / OKC(rank11) 更新
        result_map = {
            "ボストン セルティックス": ("hit", "BOS blowout 32pt margin"),
            "サンアントニオ スパーズ": ("hit", "SAS Wembanyama 35pts franchise record"),
            "オクラホマシティ サンダー": ("hit", "OKC 119-84 blowout"),
        }
        for oa in sess.get("output_a_candidates", []):
            rec = oa.get("recommendation")
            if rec in result_map:
                oa["result"], oa["actual"] = result_map[rec]
                oa["prediction_hit"] = True
        # summary 追記
        sess["session_45_g1_summary"] = {
            "output_a_decided": 3,
            "output_a_hit": 3,
            "output_a_miss": 0,
            "output_a_pending": 15,
            "note": "NBA G1 3 output-A candidates all HIT. Market-fav at conf>=85% validated."
        }
        break

with open(mb_path, 'w', encoding='utf-8') as f:
    json.dump(mb, f, ensure_ascii=False, indent=2)
print("multi_bets.json session_45 output_a updated (3/3 HIT)")
