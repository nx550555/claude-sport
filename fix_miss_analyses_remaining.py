#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
残りのMISS分析を完成させるスクリプト
- Fonseca vs Rinderknech (MC2026 R32 CAUTION/miss)
- Marozsan vs Hurkacz (MC2026 R32 CAUTION/miss)
- NRL Rabbitohs vs Raiders (R6/miss) - match_stats追加 + 分析深掘り
"""
import json

# ─── ATP JSON 更新 ─────────────────────────────────────────────────────────────
atp_path = r"C:\Users\ohwada\Desktop\claude_sport\records\tennis\2026-ATP.json"
with open(atp_path, encoding="utf-8-sig") as f:
    atp = json.load(f)

for pred in atp["predictions"]:
    m = pred.get("match", "")

    # ── 1) Fonseca vs Rinderknech ──────────────────────────────────────────────
    if "Fonseca" in m and "Rinderknech" in m and pred.get("round") == "R32":
        pred["miss_layer"] = "L2_MarketCorrect_ValueBetLost"
        pred["miss_analysis"] = (
            "【スコア】Fonseca 7-5 4-6 6-3 (2h32min)。"
            "【確認済みスタッツ（WebSearch複数ソース）】"
            "総Pts: Fonseca 99 vs Rinderknech 97 (差わずか2pt)。"
            "Fonseca: ウィナー50本, エース3本, DF3本, 1stサーブ率68%, "
            "1stサーブPts獲得70%(50/71), 2ndサーブPts獲得58%(19/33), "
            "BP変換3/7(43%)。"
            "【CAUTION BET 性質の整理】"
            "rec=Rinderknech(アンダードッグ) @3.50。市場implied prob=28.6%。"
            "モデル推定Rinderknech勝率≈41%(EV=43.5%から逆算)。"
            "「edge=12.4pp(41%-28.6%)」の価値賭け戦略。"
            "【敗因3層分析】"
            "(1) L2_MarketCorrect（主因）: 市場が正確だった。"
            "Fonsecaの1stサーブPts70%はRinderknechのリターンを無力化。"
            "クレーでのFonsecaの適応力は19歳にして市場が既に価格設定済み。"
            "(2) 総Pts99-97は競合性を示す—モデルが「Rinderknech競争力あり」と判断したこと自体は間違っていない。"
            "勝敗を分けたのはビッグポイント(BP変換3/7)での精度差。"
            "(3) 価値賭けの本質的リスク: expected valueがプラスでも個別試合は負ける。"
            "43.5%のEVは長期期待値であり、この1試合では実現しなかった。"
            "【ルール対応】"
            "CAUTIONベットの期待値計算は正常機能。"
            "若手選手(19歳)に対する市場プライシングの精度を再評価すること—"
            "Fonsecaはこの後R16/QFも勝ち抜き市場評価の正確さが証明された。"
            "R012適用条件(当大会2勝以上)はR32の時点では未達→R012の射程外。"
            "この種の価値賭けは統計的には継続で問題なし(個別MISSは許容範囲)。"
        )
        pred["match_stats"] = {
            "fonseca_total_pts": 99,
            "rinderknech_total_pts": 97,
            "fonseca_winners": 50,
            "fonseca_aces": 3,
            "fonseca_double_faults": 3,
            "fonseca_1st_serve_pct": 68.0,
            "fonseca_1st_serve_pts_won_pct": "70% (50/71)",
            "fonseca_2nd_serve_pts_won_pct": "58% (19/33)",
            "fonseca_bp_converted": "3/7 (43%)",
            "duration": "2h32min",
            "sets": "7-5 4-6 6-3",
            "source": "WebSearch (Tennis Tonic / The Stats Zone confirmed)"
        }
        print(f"[OK] Fonseca/Rinderknech miss_analysis + match_stats 更新")

    # ── 2) Marozsan vs Hurkacz ─────────────────────────────────────────────────
    if "Marozsan" in m and "Hurkacz" in m:
        pred["miss_layer"] = "L3_PRPlayerUnderestimated"
        pred["miss_analysis"] = (
            "【スコア】Hurkacz 6-2 6-3 (71分)。"
            "【確認済みスタッツ（WebSearch複数ソース）】"
            "Hurkacz: 総64pts, エース7本, DF0本, "
            "1stサーブPts獲得81%(21/26), 2ndサーブPts獲得71%(15/21), "
            "ウィナー21本, UE14本, BP変換3/8(38%), BP与えず(0回)。"
            "Marozsan: 総43pts, ウィナー14本, UE33本(!)。"
            "H2H: Hurkacz 2-0 (Shanghai2023 + MC2026)。"
            "【⚠️ データ整合性フラグ】"
            "confidence=90%、EV=2.1%、rec_odds=1.73 → EV=0.021の場合、"
            "推定勝率=(1+0.021)/1.73=59.0%。"
            "confidence=90%は「分析の確信度」であり「勝率」ではない可能性。"
            "実際の推定勝率≈59%(Marozsan) vs 市場implied57.8%(=1/1.73)="
            "わずか1.2ppのedge—実質ほぼイーブンの推奨だった。"
            "【敗因3層分析】"
            "(1) L3_PRPlayerUnderestimated（主因）: "
            "HurkaczのPR(Protected Ranking)は長期離脱後の復帰を示すが、"
            "実際のパフォーマンスは全く衰えていなかった。"
            "81%の1stサーブPts獲得はBP機会すら与えない圧倒的な支配を実現。"
            "「PR=弱体化」という前提が誤りだった。"
            "(2) Marozsan完全崩壊（副因）: UE33本 vs ウィナー14本は自滅型の敗戦。"
            "Hurkaczのアグレッシブサーブにリズムを完全に乱された。"
            "クレースペシャリストとして期待したMarozsanの優位性が全く発現しなかった。"
            "(3) H2H警告サイン無視: 直近H2H Hurkacz 2-0の事実(Shanghai2023含む)は"
            "「Hurkaczの対Marozsan優位性」を示していたが、PR status で過小評価した。"
            "【ルール対応】"
            "新規追加検討: PR選手は「体調不良リスク」より「シードなし=アップセット狙い必死」"
            "のほうが支配的。PR選手が上位シード相手ではなく下位相手に対面する場合は"
            "むしろDO NOT BET AGAINST（SKIP）とすべき。"
            "Vacherot vs Hurkacz (R16)ではHurkaczに対してVacherotをGOとしHIT—"
            "これはR13が正しく機能した例。R32でも同様の扱いが必要だった。"
        )
        pred["match_stats"] = {
            "hurkacz_total_pts": 64,
            "marozsan_total_pts": 43,
            "hurkacz_aces": 7,
            "hurkacz_double_faults": 0,
            "hurkacz_1st_serve_pts_won_pct": "81% (21/26)",
            "hurkacz_2nd_serve_pts_won_pct": "71% (15/21)",
            "hurkacz_winners": 21,
            "hurkacz_ufe": 14,
            "hurkacz_bp_converted": "3/8 (38%)",
            "hurkacz_bp_faced": 0,
            "marozsan_winners": 14,
            "marozsan_ufe": 33,
            "h2h_hurkacz_lead": "2-0 (Shanghai2023, MC2026)",
            "duration": "71min",
            "data_flag": "conf=90%はモデル確信度を示す可能性あり。EV=2.1%+odds=1.73から逆算した推定勝率≈59%が実態。",
            "source": "WebSearch (Polsat Sport / fakta.co / multiple confirmed)"
        }
        print(f"[OK] Marozsan/Hurkacz miss_analysis + match_stats 更新")

with open(atp_path, "w", encoding="utf-8") as f:
    json.dump(atp, f, ensure_ascii=False, indent=4)
print("[OK] 2026-ATP.json 保存完了")

# ─── NRL JSON 更新 ──────────────────────────────────────────────────────────────
nrl_path = r"C:\Users\ohwada\Desktop\claude_sport\records\nrl\2026.json"
with open(nrl_path, encoding="utf-8-sig") as f:
    nrl = json.load(f)

for game in nrl["games"]:
    if "Rabbitohs" in game["match"] and "Raiders" in game["match"]:
        game["miss_layer"] = "L3_DespDespert_NeutralVenue"
        game["miss_analysis"] = (
            "【最終スコア】Raiders 36 - Rabbitohs 34。"
            "【確認済みスタッツ（NRL.com/NRLニュース）】"
            "HT: Raiders 24 - Rabbitohs 4 (前半完全支配)。"
            "Raiders scorers: Savelio Tamale(40m独走), Kaeo Weekes, "
            "Hudson Young, Ethan Strange (計5-6T)。"
            "Rabbitohs scorers: Cody Walker, Alex Johnston, Jack Wighton "
            "(後半猛反撃=30pts)。観衆33,404名(Perth Optus Stadium)。"
            "【敗因3層分析】"
            "(1) L3_DespDespert（主因・未検出）: Raiders(1-4)の絶体絶命の追い詰められ感が"
            "前半の超高強度プレーを生んだ。PD/G -13.8/試合の数字はシーズン消化後の累積値—"
            "「もはや後がない」1試合への集中度は統計に反映されない。"
            "Ethan Strange/Hudson Youngのコネクションが前半4TRY連取の中核。"
            "(2) L1過信（副因）: PD/G diff 17.3(SOU +3.5 vs CAN -13.8)は5試合小サンプル。"
            "Raidersの実力はW5終了時点では過小評価されていた可能性。"
            "5試合のうち大敗試合が複数あり、PD/Gの代表性が低かった。"
            "(3) 中立地ペナルティ未評価（副因）: Perth開催はRabbitohs本拠地からの長距離移動。"
            "Raidersには関係なし(ホームでもなくアウェーでもない)。"
            "Rabbitohs side: 移動疲弊+Perth特有の固い地面への適応時間不足。"
            "【Rabbitohs後半の猛追について】"
            "34-24から試合最終盤に34-34同点まで迫るも最終的に36-34。"
            "デスパレートエフェクトはRabbitohs後半にも発現—「崖っぷち」Raiders vs "
            "「追いかける側」Rabbitohs の両チームに異なる形でモチベーション影響。"
            "【ルール対応】"
            "NRL早期シーズン推奨にL3確認項目追加が必要: "
            "①対戦相手の今季W-L record とデスパレート度 ②長距離移動の非対称性 "
            "③小サンプル(5試合以下)でのPD/G信頼性補正。"
        )
        game["match_stats"] = {
            "halftime": "Raiders 24 - Rabbitohs 4",
            "fulltime": "Raiders 36 - Rabbitohs 34",
            "raiders_scorers": ["Savelio Tamale (40m pickup)", "Kaeo Weekes", "Hudson Young", "Ethan Strange"],
            "rabbitohs_scorers": ["Cody Walker", "Alex Johnston", "Jack Wighton"],
            "crowd": 33404,
            "venue": "Optus Stadium, Perth (neutral)",
            "raiders_season_record_at_time": "1-4",
            "rabbitohs_season_record_at_time": "3-1",
            "source": "NRL.com / LeagueUnlimited confirmed"
        }
        print(f"[OK] NRL Rabbitohs/Raiders miss_analysis + match_stats 更新")

with open(nrl_path, "w", encoding="utf-8") as f:
    json.dump(nrl, f, ensure_ascii=False, indent=4)
print("[OK] 2026-NRL.json 保存完了")

# ─── upset_patterns.json 更新 ─────────────────────────────────────────────────
upset_path = r"C:\Users\ohwada\Desktop\claude_sport\stats\upset_patterns.json"
with open(upset_path, encoding="utf-8-sig") as f:
    ups = json.load(f)

existing_ids = [u["id"] for u in ups.get("confirmed_upsets", [])]

new_upsets = []

# U008: Marozsan vs Hurkacz
if "U008" not in existing_ids:
    new_upsets.append({
        "id": "U008",
        "date": "2026-04-08",
        "tournament": "Monte-Carlo Masters",
        "round": "R32",
        "match": "Marozsan F. vs Hurkacz H.(PR)",
        "predicted": "Marozsan",
        "actual_winner": "Hurkacz",
        "score": "6-2 6-3",
        "upset_type": "PR_PlayerDomination",
        "miss_layer": "L3_PRPlayerUnderestimated",
        "pattern": "Protected Ranking選手が完全回復済み。PR=弱体化という前提を完全否定。"
                   "Hurkacz 81%/71% serve pts won、0 BPs faced、UE14 vs Marozsan UE33。"
                   "H2H Hurkacz 2-0も無視。",
        "key_stats": {
            "hurkacz_1st_serve_pts_won": "81%",
            "hurkacz_bp_faced": 0,
            "marozsan_ufe": 33,
            "margin": "6-2 6-3 (71min)"
        },
        "tag": "atp_pr_player_recovery",
        "rule_created": None,
        "rule_candidate": "P008_PR_player_correction"
    })
    print("[OK] U008 追加 (Marozsan/Hurkacz)")

# U009: NRL Raiders vs Rabbitohs
if "U009" not in existing_ids:
    new_upsets.append({
        "id": "U009",
        "date": "2026-04-11",
        "tournament": "NRL 2026 Round 6",
        "match": "South Sydney Rabbitohs vs Canberra Raiders",
        "predicted": "South Sydney Rabbitohs",
        "actual_winner": "Canberra Raiders",
        "score": "36-34",
        "upset_type": "DespDespert_NeutralVenue",
        "miss_layer": "L3_DespDespert_NeutralVenue",
        "pattern": "崖っぷちチーム(1-4)が前半24-4で圧倒。小サンプルPD/G(-13.8/G)が実態を反映していなかった。"
                   "中立地Perth開催でRabbitohs移動疲弊。デスパレートエフェクトは統計外。",
        "key_stats": {
            "halftime": "Raiders 24 - Rabbitohs 4",
            "raiders_record_at_time": "1-4",
            "pd_diff_predicted": 17.3,
            "sample_size_games": 5
        },
        "tag": "nrl_desperate_underdog",
        "rule_created": None,
        "rule_candidate": "NRL_R_new: desperate_underdog_correction"
    })
    print("[OK] U009 追加 (NRL Raiders/Rabbitohs)")

if new_upsets:
    ups["confirmed_upsets"].extend(new_upsets)
    with open(upset_path, "w", encoding="utf-8") as f:
        json.dump(ups, f, ensure_ascii=False, indent=4)
    print("[OK] upset_patterns.json 保存完了")
else:
    print("[SKIP] U008/U009 既存済み")

# ─── rule_pipeline.json 更新 (P008追加) ──────────────────────────────────────
pipeline_path = r"C:\Users\ohwada\Desktop\claude_sport\core\rule_pipeline.json"
with open(pipeline_path, encoding="utf-8-sig") as f:
    pipe = json.load(f)

existing_cands = [c["candidate_id"] for c in pipe.get("candidates", [])]

if "P008" not in existing_cands:
    p008 = {
        "candidate_id": "P008",
        "status": "watching",
        "target_rule_file": "core/rules_tennis.json",
        "proposed_rule_id": "R015",
        "title": "PR(Protected Ranking)選手の実力補正",
        "description": (
            "Protected Ranking選手は「長期離脱後の復帰」を示すが、"
            "身体的回復済みの場合は実際のプレーレベルが現ランキング相当以上になる。"
            "PR選手と対戦する場合: (a) H2H確認が特に重要, "
            "(b) PR選手がサーブ型(Hurkacz等)なら回復後の威力は保持されやすい, "
            "(c) PR選手を「自動的に弱化」とみなしてはならない—むしろ意欲が高い可能性。"
            "推奨: PR選手対戦時はL2で「直近大会出場有無・セット数消化量」を確認し、"
            "フルフィット判断できる場合はcElo補正なしのフル評価を使う。"
        ),
        "trigger_threshold": 2,
        "current_count": 1,
        "evidence": [
            {
                "id": "U008",
                "match": "Marozsan vs Hurkacz (MC2026 R32)",
                "pattern": "HurkaczPR復帰初戦で6-2 6-3圧勝。PR=弱体化前提が崩壊。81% 1stSrvPts。",
                "tag": "atp_pr_player_recovery"
            }
        ],
        "tag_matches": ["atp_pr_player_recovery"],
        "note": "2件揃ったらR015として: PR選手対戦時のL2必須確認項目とcElo補正方針を明文化。"
    }
    pipe["candidates"].append(p008)
    with open(pipeline_path, "w", encoding="utf-8") as f:
        json.dump(pipe, f, ensure_ascii=False, indent=4)
    print("[OK] P008追加・rule_pipeline.json保存")
else:
    print("[SKIP] P008 既存済み")

print("\n=== 全処理完了 ===")
print("更新ファイル:")
print("  - records/tennis/2026-ATP.json (Fonseca/Rinderknech + Marozsan/Hurkacz)")
print("  - records/nrl/2026.json (Rabbitohs/Raiders 深掘り)")
print("  - stats/upset_patterns.json (U008/U009追加)")
print("  - core/rule_pipeline.json (P008追加)")
