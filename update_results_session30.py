#!/usr/bin/env python3
"""
Session_30: 試合結果更新スクリプト
- NHL CAR@NYI 2-1 HIT (CAUTION) + COL@CGY 3-1 HIT (SKIP/N016)
- UFL DC vs STL CAUTION更新 (Ta'amu確認 + L1データ追加)
- NRL Warriors/Titans GO確認 + Broncos/Tigers REVOKED確認注記
"""
import json
import os

BASE = r"C:\Users\ohwada\Desktop\claude_sport"

# ─────────────────────────────────────────────
# 1. NHL 2025-26.json 更新
# ─────────────────────────────────────────────
nhl_path = os.path.join(BASE, "records", "nhl", "2025-26.json")
with open(nhl_path, "r", encoding="utf-8-sig") as f:
    nhl = json.load(f)

# 1a. サマリ更新 (prediction tracking)
nhl["summary"]["prediction_total"] = 8
nhl["summary"]["prediction_hit"] = 6
nhl["summary"]["prediction_hit_rate"] = round(6/8, 3)
nhl["summary"]["prediction_pending"] = 0
nhl["summary"]["note"] = (
    "bet実績(GO tier): 2/2 100% +1.863u。"
    "予測精度(全L1通過試合): 6/8 75.0%（retroactive含む）。"
    "4/15追加: CAR@NYI CAR 2-1 HIT + COL@CGY COL 3-1 HIT（両試合ともSKIP/CAUTION、ベットなし）"
)

# 1b. pending_gamesから結果入りのゲームエントリを作成
car_nyi_result = {
    "date": "2026-04-15",
    "date_et": "2026-04-14",
    "match": "Carolina Hurricanes @ New York Islanders",
    "home": "New York Islanders",
    "away": "Carolina Hurricanes",
    "venue": "UBS Arena, Elmont NY",
    "tier": "caution",
    "predicted_winner": "Carolina Hurricanes",
    "prediction_confidence": 78,
    "prediction_basis": "xGF% CAR 56.0 vs NYI 48.0, diff 8pt. CAR RS1位確定。NYI PO圏外消化試合。",
    "prediction_hit": True,
    "rec": "Carolina Hurricanes",
    "rec_odds": 1.90,
    "ev_est": 42.5,
    "l1_metric": "xGF% (MoneyPuck 2026-04-14)",
    "l1_data": {
        "CAR_xGF": 56.0,
        "NYI_xGF": 48.0,
        "diff": 8.0
    },
    "adjustments": {
        "CAR_away": "-5% (N004)",
        "NYI_eliminated": "+5% (N008: NYI PO圏外・消化試合)"
    },
    "goalie_actual": "Brandon Bussi(CAR) 28sv / David Rittich(NYI)",
    "goalie_note": "Andersen先発予告→実際はBussi先発。Bussi RS 31-6-2 好成績。予測通りCAR勝利。",
    "result": "Carolina Hurricanes",
    "score": "2-1",
    "hit": None,
    "actual_ev": None,
    "miss_layer": None,
    "rules_applied": ["N001", "N004", "N006", "N008", "N016"],
    "note": (
        "CAUTION tier（ゴーリー確認前）→ベット未実施。予測HIT。"
        "CAR 2-1 NYI: Ehlers 1P(1G), Jankowski 3P決勝, Horvat NYI 1G。"
        "CARはRS東地区1位フィニッシュ。Bussiが28セーブの好守。"
    )
}

col_cgy_result = {
    "date": "2026-04-15",
    "date_et": "2026-04-14",
    "match": "Calgary Flames @ Colorado Avalanche",
    "home": "Colorado Avalanche",
    "away": "Calgary Flames",
    "tier": "skip",
    "predicted_winner": "Colorado Avalanche",
    "prediction_confidence": 80,
    "prediction_basis": "xGF% COL 56.0 vs CGY 47.0, diff 9pt。N016適用: Blackwood先発（Georgiev温存）→SKIP判断。",
    "prediction_hit": True,
    "rec": None,
    "rec_odds": None,
    "ev": None,
    "l1_metric": "xGF% (MoneyPuck 2026-04-14)",
    "l1_data": {
        "COL_xGF": 56.0,
        "CGY_xGF": 47.0,
        "diff": 9.0
    },
    "n016_result": "N016正しく機能。Blackwood先発確認→SKIP。結果: COL 3-1で勝利。N016はbet回避だが予測としてHIT。COL完全主力出場なしでも地力差が出た。",
    "result": "Colorado Avalanche",
    "score": "3-1",
    "hit": None,
    "actual_ev": None,
    "miss_layer": None,
    "rules_applied": ["N001", "N004", "N006", "N008", "N016"],
    "note": (
        "N016でSKIP（Blackwood先発確認済・Georgiev温存）。"
        "COL 3-1 CGY: Landeskog決勝, Lehkonen 1G, MacKinnon 53G目(リーグトップ), Makar 3A(7試合ぶり復帰)。"
        "COL 119pts（フランチャイズ記録タイ）。RS最終。CGY 消化試合。"
    )
}

# 1c. gamesに追加、pending_gamesをクリア
nhl["games"].append(car_nyi_result)
nhl["games"].append(col_cgy_result)
nhl["pending_games"] = []

with open(nhl_path, "w", encoding="utf-8") as f:
    json.dump(nhl, f, ensure_ascii=False, indent=2)
print("[1] NHL 2025-26.json 更新完了")

# ─────────────────────────────────────────────
# 2. UFL 2026.json 更新 - DC vs STL CAUTION更新
# ─────────────────────────────────────────────
ufl_path = os.path.join(BASE, "records", "ufl", "2026.json")
with open(ufl_path, "r", encoding="utf-8-sig") as f:
    ufl = json.load(f)

for g in ufl["games"]:
    if g.get("match") == "DC Defenders @ St. Louis Battlehawks":
        g["l1_data"] = {
            "DC_PD_per_game": 16.7,
            "STL_PD_per_game": -2.0,
            "diff": 18.7,
            "threshold": 4.0,
            "l1_pass": True,
            "source": "UFL standings after Week 3 (theufl.com)"
        }
        g["standings_w3"] = {
            "DC": "2-1, PF=99, PA=49, Diff=+50",
            "STL": "2-1, PF=65, PA=71, Diff=-6"
        }
        g["qb_status"] = {
            "DC": "Jordan Ta'amu confirmed (W3: 15/27 173yd 1TD, 45-7 blowout win)。MVP of 2025 UFL Championship。",
            "STL": "Harrison Frost (came off bench W3: 9/15 148yd 3TD comeback 34-30 vs Stallions)"
        }
        g["confidence"] = 78
        g["ev_est"] = 12.3
        g["ev_calc"] = "(0.78 x 1.44) - 1 = +12.3%"
        g["caution_reason"] = (
            "conf 78% < Week4 threshold 80% (U008). "
            "L1 PASS: PD/G diff 18.7 (DC+16.7 vs STL-2.0). "
            "DC away -4% (U004). "
            "Ta'amu confirmed (W3 active). "
            "EV+12.3% (market 1.44). "
            "STL at home + Week3 comeback ability. "
            "Upgrade from 'QB unconfirmed' CAUTION to 'analyzed CAUTION'."
        )
        g["note"] = (
            "CAUTION: DC Defenders (away) vs St. Louis Battlehawks (home). "
            "L1 PASS (PD/G diff 18.7 > threshold 4). "
            "DC has best PD in league (+16.7/G). "
            "But DC is away (-4%), and conf 78% < W4 required 80%. "
            "STL showed resilience (W3 comeback 34-30 from 30-20 deficit). "
            "Ta'amu confirmed as DC starter. "
            "Monitor for any lineup/injury news closer to game."
        )
        g["rules_applied"] = ["GEN001", "U001", "U004", "U008"]
        break

with open(ufl_path, "w", encoding="utf-8") as f:
    json.dump(ufl, f, ensure_ascii=False, indent=2)
print("[2] UFL 2026.json 更新完了 (DC vs STL CAUTION分析)")

# ─────────────────────────────────────────────
# 3. NRL 2026.json 更新 - チームリスト確認注記
# ─────────────────────────────────────────────
nrl_path = os.path.join(BASE, "records", "nrl", "2026.json")
with open(nrl_path, "r", encoding="utf-8-sig") as f:
    nrl = json.load(f)

for g in nrl["pending_games"]:
    if g.get("match") == "NZ Warriors vs Gold Coast Titans":
        # team_lists情報を追加
        g["team_lists_r7"] = {
            "NZW": (
                "Kurt Capewell returns from 5-game calf injury (significant +). "
                "Marata Niukore moves to bench. "
                "Tanner Stowers-Smith OUT (hamstring). "
                "Nicoll-Klokstad(neck)/Barnett(thumb) in reserves - availability uncertain."
            ),
            "GCT": (
                "No changes to 19-man squad after big win over Eels. "
                "Klese Haas in extended squad (returning from leg injury). "
                "Squad stable."
            )
        }
        g["team_list_assessment"] = (
            "Warriors: Capewell復帰はプラス要因。軽傷者数名は懸念あるが主力に影響なし。"
            "Titans: 変更なし、安定継続。GO維持 (NZW PD/G+8.7 vs GCT -8.0, diff 16.7)。"
        )
        g["go_confirmed"] = True
        print("[3a] NRL Warriors/Titans team list注記追加")

    if g.get("match") == "Wests Tigers vs Brisbane Broncos" and g.get("tier") == "revoked":
        g["revoke_confirmed"] = True
        g["team_lists_r7"] = {
            "WST": (
                "Luai returns from knee injury (R3以来欠場). "
                "Taylan May returns from shoulder injury at centre. "
                "Starting lineup: Luai(5/8) + Doueihi(HB)."
            ),
            "BRI": (
                "Adam Reynolds returns from adductor injury (halfback). "
                "Pat Carrigan SUSPENDED (key prop/captain). "
                "Reece Walsh OUT (injury). "
                "Cory Paix OUT (specialist ruling). "
                "Xavier Willison replaces Carrigan at lock."
            )
        }
        g["revoke_note_updated"] = (
            "Revoke confirmed by R7 team lists: "
            "Luai+May return (Tigers strength up) AND Carrigan/Walsh/Paix all OUT (Broncos weakened). "
            "市場: Tigers 1.52 / Broncos 2.55 (大幅転換). "
            "元のGEN002アラートはPD/G帰属ミスではなくスクワッド実力差だった。REVOKE正解。"
        )
        print("[3b] NRL Broncos/Tigers revoke確認注記追加")

with open(nrl_path, "w", encoding="utf-8") as f:
    json.dump(nrl, f, ensure_ascii=False, indent=2)
print("[3] NRL 2026.json 更新完了")

print("\n=== 全更新完了 ===")
print("次ステップ: python sync_sport_cards.py を実行してダッシュボード反映")
