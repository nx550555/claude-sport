"""
Session健全性スキャン (STEP 0で毎セッション冒頭に実行必須)
異常検出時は赤字で警告。正常なら「✓ システム健全」出力。

チェック項目:
1. multi_bets.json の最新 session date が本日 or 前日か
2. 直近5セッションの Q3（出力A候補）件数分布（連続ゼロ警告）
3. Phase2移行後の Q2（UPSET_PICK）発動累計（7日以上ゼロ警告）
4. 各sport records の最新 screening_log 日付の健全性
5. 前セッションでの4象限 tagging 実施率
"""
import json
import sys
from pathlib import Path
from datetime import datetime, date, timedelta

BASE = Path(r"C:\Users\ohwada\Desktop\claude_sport")

RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BOLD = "\033[1m"
RESET = "\033[0m"

def load(p):
    return json.load(open(p, encoding="utf-8-sig"))

def parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(s.split("T")[0][:10], "%Y-%m-%d").date()
    except Exception:
        return None

def main():
    today = date.today()
    # 固定: プロジェクトの運用日時は2026-04-20
    # (システム日付 2026-04-20 基準。実行時は現行日付で補正)
    anomalies = []
    warnings = []
    goods = []

    print(f"{BOLD}=== [HC] Session健全性スキャン ==={RESET}")
    print(f"実行日: {today.isoformat()}\n")

    # ---- 1. multi_bets.json 最新 session date ----
    try:
        mb = load(BASE / "records" / "multi_bets.json")
        sessions = mb.get("sessions", [])
        if not sessions:
            anomalies.append("multi_bets.json に session エントリが存在しない")
        else:
            latest = sessions[-1]
            latest_date = parse_date(latest.get("date",""))
            session_id = latest.get("session_id","?")
            if latest_date is None:
                anomalies.append(f"最新 session ({session_id}) の date パース不可")
            else:
                days_old = (today - latest_date).days
                if days_old > 2:
                    warnings.append(f"multi_bets.json 最新 session ({session_id} / {latest_date.isoformat()}) が {days_old}日前。スクリーニング結果未追記の可能性")
                else:
                    goods.append(f"multi_bets 最新: {session_id} ({latest_date.isoformat()}, {days_old}日前)")
    except Exception as e:
        anomalies.append(f"multi_bets.json 読み込み失敗: {e}")

    # ---- 2. 直近5セッションの Q3 (output_a) 件数分布 ----
    try:
        mb = load(BASE / "records" / "multi_bets.json")
        sessions = mb.get("sessions", [])
        recent_5 = sessions[-5:] if len(sessions) >= 5 else sessions
        q3_counts = []
        for s in recent_5:
            # output_a_candidates / output_a_additions / output_a どれかにカウントがある
            cnt = len(s.get("output_a_candidates", [])) + len(s.get("output_a_additions", [])) + len(s.get("output_a", []))
            q3_counts.append((s.get("session_id","?"), cnt))
        zero_streak = 0
        for sid, cnt in reversed(q3_counts):
            if cnt == 0:
                zero_streak += 1
            else:
                break
        if zero_streak >= 3:
            anomalies.append(f"直近 {zero_streak} セッション連続で Q3（出力A候補）がゼロ。スクリーニング漏れ可能性大")
        elif zero_streak >= 2:
            warnings.append(f"直近 {zero_streak} セッション Q3 ゼロ。注意")
        else:
            goods.append(f"直近5セッション Q3件数: {[c for _, c in q3_counts]}")
    except Exception as e:
        warnings.append(f"Q3分布チェック失敗: {e}")

    # ---- 3. Phase2移行後の Q2 (UPSET_PICK) 発動累計 ----
    try:
        up = load(BASE / "stats" / "upset_patterns.json")
        cu = up.get("confirmed_upsets", [])
        phase2_start = date(2026, 4, 18)
        upset_picks_triggered = 0
        for u in cu:
            d = parse_date(u.get("date",""))
            # UPSET_PICK 発動の定義: upset_pick_feasibility に "condition met" or "FULLY MET" が含まれる
            fea = u.get("upset_pick_feasibility","").lower()
            if d and d >= phase2_start and ("condition met" in fea or "fully met" in fea):
                upset_picks_triggered += 1
        days_since_phase2 = (today - phase2_start).days
        if days_since_phase2 >= 7 and upset_picks_triggered == 0:
            warnings.append(f"Phase2移行後{days_since_phase2}日経過、UPSET_PICK 発動 0件。GEN005閾値 (UF≥3+div≥15pp) が厳しすぎる可能性。UPSET_PICK_Lite検討候補")
        else:
            goods.append(f"Phase2移行後{days_since_phase2}日、UPSET_PICK 条件充足事例 {upset_picks_triggered}件（発動しなかった過去も含む）")
    except Exception as e:
        warnings.append(f"UPSET_PICK累計チェック失敗: {e}")

    # ---- 4. 各sport records の最新 screening_log 日付 ----
    try:
        sport_files = {
            "nba": BASE / "records" / "nba" / "2025-26.json",
            "nhl": BASE / "records" / "nhl" / "2025-26.json",
            "nrl": BASE / "records" / "nrl" / "2026.json",
            "top14": BASE / "records" / "top14" / "2026.json",
            "superrugby": BASE / "records" / "superrugby" / "2026.json",
            "wta": BASE / "records" / "wta" / "2026.json",
            "tennis_atp": BASE / "records" / "tennis" / "2026-ATP.json",
            "ufl": BASE / "records" / "ufl" / "2026.json",
        }
        stale_sports = []
        for sport, fp in sport_files.items():
            if not fp.exists():
                continue
            d = load(fp)
            sl = d.get("screening_log", []) or d.get("log", [])
            if not sl:
                continue
            last = sl[-1]
            last_date = parse_date(last.get("date","") if isinstance(last, dict) else "")
            if last_date is None:
                continue
            gap = (today - last_date).days
            if gap > 7:
                stale_sports.append(f"{sport}({gap}d)")
        if stale_sports:
            warnings.append(f"7日以上 screening_log 更新がない sport: {', '.join(stale_sports)}")
        else:
            goods.append(f"全sportのscreening_log が直近7日以内に更新済")
    except Exception as e:
        warnings.append(f"screening_log チェック失敗: {e}")

    # ---- 5. 前セッションでの4象限 tagging 実施率 ----
    try:
        mb = load(BASE / "records" / "multi_bets.json")
        sessions = mb.get("sessions", [])
        if sessions:
            latest = sessions[-1]
            # quadrant tagging は session 内の screening_procedure_note / deep_dive / 実運用キー (output_a/go_recommendations) で識別
            # Session_48 以降は output_a / go_recommendations / closed_results が標準。output_a_candidates は旧世代互換。
            q_keys_checked = ["output_a_candidates","output_a_additions","upset_pick_checks","upset_pick_uf_deep_dive","output_a","go_recommendations","closed_results"]
            has_q_tag = any(latest.get(k) for k in q_keys_checked)
            if has_q_tag:
                matched = [k for k in q_keys_checked if latest.get(k)]
                goods.append(f"前セッション ({latest.get('session_id','?')}) で4象限分類記録あり [{','.join(matched)}]")
            else:
                warnings.append(f"前セッション ({latest.get('session_id','?')}) で4象限分類記録が見つからない。STEP⓪〜④の手順漏れの可能性")
    except Exception as e:
        warnings.append(f"4象限tagging チェック失敗: {e}")

    # ---- 6. pending_actions.md PA-PERM 常設タスク存在確認 ----
    try:
        pa_path = BASE / "monitoring" / "pending_actions.md"
        if pa_path.exists():
            text = pa_path.read_text(encoding="utf-8", errors="ignore")
            required_perm = ["PA-PERM01","PA-PERM02","PA-PERM03","PA-PERM04"]
            missing = [p for p in required_perm if p not in text]
            if missing:
                anomalies.append(f"pending_actions.md に常設タスク未登録: {', '.join(missing)}")
            else:
                goods.append(f"常設タスク PA-PERM01〜04 登録済")
    except Exception as e:
        warnings.append(f"pending_actions チェック失敗: {e}")

    # ---- 7. upset_patterns rule_linked 存在率 (Session_46 追加) ----
    try:
        up = load(BASE / "stats" / "upset_patterns.json")
        cu = up.get("confirmed_upsets", [])
        total = len(cu)
        linked = sum(1 for e in cu if e.get("rule_linked"))
        rate = (linked / total * 100) if total else 0
        if rate < 80:
            anomalies.append(f"upset_patterns rule_linked 存在率 {rate:.1f}% < 80% (linked={linked}/{total}). MISS分析→ルール反映の断絶")
        elif rate < 95:
            warnings.append(f"upset_patterns rule_linked 存在率 {rate:.1f}% (linked={linked}/{total})")
        else:
            goods.append(f"upset_patterns rule_linked 存在率 {rate:.1f}% (linked={linked}/{total})")
    except Exception as e:
        warnings.append(f"rule_linked チェック失敗: {e}")

    # ---- 8. rule_improvement_candidates 空/無status エントリ検出 (Session_46 追加) ----
    try:
        up = load(BASE / "stats" / "upset_patterns.json")
        ric = up.get("rule_improvement_candidates", [])
        empty_entries = [i for i, c in enumerate(ric) if not c.get("title") and not c.get("proposed") and not c.get("current_rule")]
        no_status = [i for i, c in enumerate(ric) if not c.get("status") and not c.get("type")]
        if empty_entries:
            warnings.append(f"rule_improvement_candidates 空エントリ index: {empty_entries}")
        if no_status:
            warnings.append(f"rule_improvement_candidates status 未設定 index: {no_status}")
        if not empty_entries and not no_status:
            goods.append(f"rule_improvement_candidates 全{len(ric)}件 status 設定済")
    except Exception as e:
        warnings.append(f"rule_improvement_candidates チェック失敗: {e}")

    # ---- 9. CE016 再発防止: confirmed_upsets 全件の winner vs market_favorite 整合性 (Session_46 追加) ----
    # UPSET の定義: 結果の勝者 != market_favorite。両者が一致している場合は UPSET ではない = 誤記録の疑い
    try:
        up = load(BASE / "stats" / "upset_patterns.json")
        cu = up.get("confirmed_upsets", [])
        suspect = []
        for e in cu:
            uid = e.get("upset_id") or e.get("id", "?")
            mf = e.get("market_favorite", "") or e.get("favorite_market", "") or e.get("favorite", "")
            result = e.get("result", "") or e.get("result_score", "") or e.get("actual_winner", "")
            if not mf or not result:
                continue
            # Extract the winner name from "X d. Y" or just the first token. Simple match: market_favorite substring appears in result before "d."
            result_lower = result.lower()
            mf_lower = str(mf).lower()
            # Take first token of mf (family name)
            mf_key = mf_lower.split()[0] if mf_lower else ""
            if not mf_key:
                continue
            # Find "d." position
            if " d. " in result_lower:
                winner_part = result_lower.split(" d. ")[0]
            elif " defeated " in result_lower:
                winner_part = result_lower.split(" defeated ")[0]
            else:
                continue
            # If market favorite family name appears in the winner part, it's NOT a real upset
            if mf_key in winner_part:
                suspect.append(f"{uid} (winner={winner_part.strip()[:30]}, fav={mf_key})")
        if suspect:
            anomalies.append(f"CE016系疑い: confirmed_upsets で winner==market_favorite のケース {len(suspect)}件: {', '.join(suspect[:5])}")
        else:
            goods.append(f"CE016整合性: confirmed_upsets {len(cu)}件全てで winner!=market_favorite (UPSET 成立確認)")
    except Exception as e:
        warnings.append(f"CE016整合性チェック失敗: {e}")

    # ---- 10. MISS miss_analysis 完全性 (Session_50 追加: feedback loop 監査) ----
    # 背景: 2026-04-23 ユーザー指摘で BOS G2 / SAS G2 の miss_analysis 空白が発覚。
    # Q3 output_a MISS が rule_pipeline に反映されない feedback loop 機能不全の再発防止。
    try:
        import glob
        record_files = sorted(glob.glob(str(BASE / "records" / "**" / "*.json"), recursive=True))
        incomplete = []
        for rf in record_files:
            if "multi_bets.json" in rf: continue
            try:
                d = load(Path(rf))
            except Exception:
                continue
            def walk(obj):
                if isinstance(obj, list):
                    for x in obj: yield from walk(x)
                elif isinstance(obj, dict):
                    yield obj
                    for v in obj.values(): yield from walk(v)
            for o in walk(d):
                result = o.get('result')
                pred = o.get('predicted_winner')
                if not result or not pred: continue
                if str(result).strip() == str(pred).strip(): continue
                ph = o.get('prediction_hit')
                if ph is True: continue
                # void/W-O は試合不成立で MISS ではないため除外 (Session_59 追加)
                if o.get('void') is True: continue
                if ph is None: continue
                has_ma = bool(o.get('miss_analysis'))
                has_layer = bool(o.get('miss_layer'))
                has_rl = bool(o.get('rule_linked') or o.get('rules_triggered'))
                if not (has_ma and has_layer and has_rl):
                    missing = []
                    if not has_ma: missing.append("miss_analysis")
                    if not has_layer: missing.append("miss_layer")
                    if not has_rl: missing.append("rule_linked")
                    match_name = str(o.get('match', '?'))[:40]
                    file_name = Path(rf).name
                    incomplete.append(f"{file_name}:{match_name}[{','.join(missing)}]")
        if incomplete:
            anomalies.append(f"MISS miss_analysis 欠損 {len(incomplete)}件: {'; '.join(incomplete[:3])}{'...' if len(incomplete)>3 else ''} → feedback loop 機能不全。rule_pipeline 反映前に補填必須。")
        else:
            goods.append(f"MISS feedback loop: 全 MISS 記録で miss_analysis + miss_layer + rule_linked 完全")
    except Exception as e:
        warnings.append(f"MISS miss_analysis 完全性チェック失敗: {e}")

    # ---- 11. CE017 再発防止: outcome_note 表記 vs prediction_hit / market_favorite 論理整合性 (Session_51 追加) ----
    # CE013/CE014/CE015/CE016/CE017 同根の「勝敗真逆記録」パターンを自動検知
    try:
        ce_inconsistencies = []
        for rf in record_files:
            if "multi_bets.json" in rf: continue
            try:
                d = load(Path(rf))
            except Exception:
                continue
            def walk2(obj):
                if isinstance(obj, list):
                    for x in obj: yield from walk2(x)
                elif isinstance(obj, dict):
                    yield obj
                    for v in obj.values(): yield from walk2(v)
            for o in walk2(d):
                note = str(o.get('outcome_note','')).lower()
                ph = o.get('prediction_hit')
                pred = o.get('predicted_winner')
                result = o.get('result')
                mfav = o.get('market_favorite')
                if not (pred and result):
                    continue
                fav_win_words = ('fav hit','fav win','favorite win','favorite hit')
                upset_words = ('upset',)
                file_name = Path(rf).name
                match_name = str(o.get('match', '?'))[:40]
                # パターン1: "UPSET" 表記なのに prediction_hit=True (本命予測HITしたなら UPSET ではない)
                if any(w in note for w in upset_words) and ph is True and 'ce017' not in note and 'ce_correction' not in (str(o.get('ce_correction','')).lower()):
                    ce_inconsistencies.append(f"{file_name}:{match_name}[UPSET表記+ph=True - CE017候補]")
                # パターン2: "favorite win" 表記なのに prediction_hit=False
                if any(w in note for w in fav_win_words) and ph is False:
                    ce_inconsistencies.append(f"{file_name}:{match_name}[fav_win表記+ph=False - CE017候補]")
                # パターン3: market_favorite 記載 + result 一致なのに prediction_hit=False
                if mfav and ph is False and str(mfav).strip().lower() == str(result).strip().lower():
                    ce_inconsistencies.append(f"{file_name}:{match_name}[mfav==result+ph=False - CE017候補]")
        if ce_inconsistencies:
            anomalies.append(f"CE017論理整合性違反 {len(ce_inconsistencies)}件: {'; '.join(ce_inconsistencies[:3])}{'...' if len(ce_inconsistencies)>3 else ''} → outcome_note と prediction_hit / market_favorite が矛盾。勝敗逆転記録の可能性。一次ソース再検証必須。")
        else:
            goods.append(f"CE017論理整合性: outcome_note と prediction_hit / market_favorite 全件整合 (CE013-017 同根パターン未検知)")
    except Exception as e:
        warnings.append(f"CE017論理整合性チェック失敗: {e}")

    # === v4 追加: 外部スタッツフィード (GEN006) ===
    try:
        import sys as _sys
        from pathlib import Path as _P
        _sys.path.insert(0, str(_P(__file__).resolve().parent.parent))
        from scripts.stats_feed_reader import feed_status, stale_feeds
        fs = feed_status()
        stale = stale_feeds()
        ok_count = sum(1 for v in fs.values() if v.get("available") and not v.get("stale"))
        total = len(fs)
        if not stale:
            goods.append(f"外部スタッツフィード (GEN006): {ok_count}/{total} OK・全フィード fresh")
        else:
            # unavailable vs stale を分けて報告
            unavail = [k for k in stale if not fs[k].get("available")]
            stale_only = [k for k in stale if fs[k].get("available") and fs[k].get("stale")]
            if unavail:
                warnings.append(f"GEN006: 未取得フィード {len(unavail)}件 - {', '.join(unavail[:5])}。scripts/fetch_*.py 実行 or ユーザー依頼。")
            if stale_only:
                warnings.append(f"GEN006: 古いフィード {len(stale_only)}件 - {', '.join(stale_only[:5])}。再取得推奨。")
    except Exception as e:
        warnings.append(f"GEN006 feed_status チェック失敗: {e}")

    # === v7 追加: parse=0 空フィード検知 (Session_55 2026-04-23 GEN007) ===
    # Fetcher が HTTP fetch に成功しても parser が 0件抽出で saved されている
    # ケースを検知。file 存在しても内容が空 = L1 データ欠損。
    try:
        from pathlib import Path as _P
        feeds_dir = BASE / "stats" / "external_feeds"
        today_iso = today.isoformat()
        empty = []
        # 本日日付の新規保存ファイルのみチェック (過去分まで遡ると誤検知増える)
        for f in sorted(feeds_dir.glob(f"*_{today_iso}.json")):
            try:
                j = json.load(open(f, encoding="utf-8-sig"))
            except Exception:
                continue
            # 各 fetcher が格納する件数 key を試行
            counts = []
            for key in ("teams", "team_count", "total_teams", "club_count"):
                v = j.get(key)
                if isinstance(v, int):
                    counts.append((key, v))
                elif isinstance(v, list):
                    counts.append((key, len(v)))
            # clubs (clubelo 形式)
            clubs = j.get("clubs")
            if isinstance(clubs, list):
                counts.append(("clubs", len(clubs)))
            # lineup 形式 (sport 別に dict)
            for sport_key in ("nba", "nfl", "mlb", "soccer", "rugby"):
                sv = j.get(sport_key)
                if isinstance(sv, dict):
                    counts.append((sport_key, len(sv)))
            # leagues (understat / clubelo 形式)
            lgs = j.get("leagues")
            if isinstance(lgs, dict):
                def _league_size(v):
                    if isinstance(v, dict):
                        return v.get("team_count", len(v.get("teams", [])))
                    if isinstance(v, list):
                        return len(v)
                    return 0
                tot = sum(_league_size(v) for v in lgs.values())
                counts.append(("leagues_teams_total", tot))
            # 判定: すべて 0 なら空フィード
            if counts and all(v == 0 for _, v in counts):
                empty.append(f.name)
        if empty:
            anomalies.append(
                f"parse=0 空フィード {len(empty)}件: {', '.join(empty)}。"
                "HTTP fetch 成功も parser が 0件抽出。該当 fetcher の parser を確認要。"
            )
        else:
            goods.append("本日分 fetcher 保存: parse=0 空フィード未検知")
    except Exception as e:
        warnings.append(f"空フィード検知チェック失敗: {e}")

    # ---- v8 追加: 日付妥当性自動検証 (Session_57 提案#1) ----
    # CE019-CE022 系の日付誤記再発防止: 未来30日以上先の pending 試合 / 過去30日以上前の pending 試合を警告
    try:
        from datetime import datetime, timedelta
        today = datetime.now()
        future_threshold = today + timedelta(days=30)
        past_threshold = today - timedelta(days=30)
        date_anomalies = []
        record_files = [
            "records/tennis/2026-ATP.json", "records/wta/2026.json",
            "records/nhl/2025-26.json", "records/nba/2025-26.json",
            "records/ufl/2026.json", "records/nrl/2026.json",
            "records/superrugby/2026.json", "records/premiership/2026.json",
            "records/top14/2026.json", "records/prod2/2026.json",
            "records/superleague/2026.json", "records/ahl/2025-26.json",
            "records/soccer/2025-26.json", "records/mlb/2026.json",
        ]
        for rel in record_files:
            p = BASE / rel
            if not p.exists():
                continue
            try:
                d = load(p)
            except Exception:
                continue
            items = []
            if "games" in d: items = d["games"]
            elif "predictions" in d: items = d["predictions"]
            elif "tournaments" in d:
                for t in d["tournaments"]:
                    items.extend(t.get("predictions", []))
            for item in items:
                if item.get("void") or item.get("tier") in ("invalid", "duplicate_closed"):
                    continue
                date_str = item.get("date", "")
                if not date_str or not isinstance(date_str, str):
                    continue
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    continue
                is_pending = (item.get("hit") is None and item.get("prediction_hit") is None)
                match_name = item.get("match", item.get("name", ""))[:40]
                # 未来30日以上先の pending → UCL SF 等を除外するため40日に緩和
                if dt > today + timedelta(days=40) and is_pending:
                    date_anomalies.append(f"{rel.split('/')[-1]}:{match_name}[date={date_str} 40日以上先+pending]")
                # 過去30日以上前の pending (結果確認忘れ)
                if dt < past_threshold and is_pending:
                    date_anomalies.append(f"{rel.split('/')[-1]}:{match_name}[date={date_str} 30日以上前+pending]")
        if date_anomalies:
            warnings.append(f"日付妥当性 {len(date_anomalies)}件の懸念: {'; '.join(date_anomalies[:5])}{'...' if len(date_anomalies)>5 else ''} → CE019-022 再発防止: 一次ソース確認推奨")
        else:
            goods.append("日付妥当性チェック: 未来40日以上先/過去30日以上前の pending なし (v8 2026-04-24追加)")
    except Exception as e:
        warnings.append(f"日付妥当性チェック失敗: {e}")

    # ---- 12. miss_analysis_tag_compliance (Session_62 フェーズ4 4-3 追加) ----
    # 5種タグ ([FETCH/FETCHER/SEARCH/MEMORY/INFER]) の付与状況を検査。
    # 遡及対象外: フェーズ4 ステージ3 承認日 (2026-04-27) 以降に追加された
    # miss_analysis のみ対象 (既存記録への遡及付与は実施しないため)。
    # (Session_62 フェーズ5 改修) record_class == "skip_record" フィルタ追加:
    # 区分3 試合は走査対象外。柱D 7. 既存柱との整合性 + 柱C との整合参照。
    # record_class が未設定のエントリは既存ロジック (APPROVAL_DATE 判定) に
    # よって自然に skip されるため遡及付与対象外として扱う。
    try:
        import re
        import glob as _glob
        TAG_PATTERN = re.compile(r"\[(FETCH|FETCHER|SEARCH|MEMORY|INFER|FETCH_FAILED)(:[^\]]*)?\]")
        APPROVAL_DATE = date(2026, 4, 27)  # フェーズ4 ステージ3 承認日
        record_files_v12 = sorted(_glob.glob(str(BASE / "records" / "**" / "*.json"), recursive=True))
        no_tag_entries = []
        partial_tag_entries = []
        checked_count = 0
        for rf in record_files_v12:
            if "multi_bets.json" in rf:
                continue
            try:
                d = load(Path(rf))
            except Exception:
                continue
            def walk_v12(obj):
                if isinstance(obj, list):
                    for x in obj:
                        yield from walk_v12(x)
                elif isinstance(obj, dict):
                    yield obj
                    for v in obj.values():
                        yield from walk_v12(v)
            for o in walk_v12(d):
                ma = o.get("miss_analysis")
                if not ma or not isinstance(ma, str):
                    continue
                # (Session_62 フェーズ5) 柱D 区分3 (skip_record) は走査対象外。
                # 区分3 はタグ義務対象外のため検査スキップ。
                # record_class 未設定エントリは既存ロジック (APPROVAL_DATE 判定)
                # で自然に skip されるため、明示フィルタは "skip_record" のみ。
                if o.get("record_class") == "skip_record":
                    continue
                # 承認日基準で対象判定: prediction_hit_date / last_updated_at / date のいずれか
                # を参照。日付不明 or 承認日より前なら遡及対象外として skip。
                entry_date = None
                for date_key in ("prediction_hit_updated_at", "last_updated_at", "date"):
                    dv = o.get(date_key)
                    parsed = parse_date(dv) if isinstance(dv, str) else None
                    if parsed:
                        entry_date = parsed
                        break
                if entry_date is None or entry_date < APPROVAL_DATE:
                    continue
                checked_count += 1
                tags_found = TAG_PATTERN.findall(ma)
                file_name = Path(rf).name
                match_name = str(o.get("match", "?"))[:40]
                if not tags_found:
                    # 完全タグなし → ALERT 候補
                    no_tag_entries.append(f"{file_name}:{match_name}")
                else:
                    # タグはあるが文末タグなし主張が混在しているかチェック:
                    # 文 (。 区切り) に分解し、各文がタグで終わっているか確認
                    sentences = [s.strip() for s in re.split(r"[。\n]+", ma) if s.strip()]
                    untagged_sentences = []
                    for sent in sentences:
                        if not TAG_PATTERN.search(sent):
                            # 短い接続句 (10文字未満) はカウント対象外 (例: 「なお、」)
                            if len(sent) >= 10:
                                untagged_sentences.append(sent[:30])
                    if untagged_sentences:
                        partial_tag_entries.append(
                            f"{file_name}:{match_name}[untagged_sentences={len(untagged_sentences)}]"
                        )
        if no_tag_entries:
            anomalies.append(
                f"miss_analysis_tag_compliance: 完全タグなし {len(no_tag_entries)}件: "
                f"{'; '.join(no_tag_entries[:3])}{'...' if len(no_tag_entries)>3 else ''} → "
                "5種タグ ([FETCH/FETCHER/SEARCH/MEMORY/INFER]) 必須。CLAUDE.md 柱C 4-3 参照。"
            )
        if partial_tag_entries:
            warnings.append(
                f"miss_analysis_tag_compliance: タグなし主張混在 {len(partial_tag_entries)}件: "
                f"{'; '.join(partial_tag_entries[:3])}{'...' if len(partial_tag_entries)>3 else ''} → "
                "主張ごとにタグ付与必須。"
            )
        if not no_tag_entries and not partial_tag_entries:
            if checked_count == 0:
                goods.append(
                    f"miss_analysis_tag_compliance: 承認日 {APPROVAL_DATE.isoformat()} 以降の"
                    "新規 miss_analysis 未検出 (遡及対象外のみ・正常)"
                )
            else:
                goods.append(
                    f"miss_analysis_tag_compliance: {checked_count}件全件で5種タグ付与済 "
                    f"(承認日 {APPROVAL_DATE.isoformat()} 以降の新規 miss_analysis のみ対象)"
                )
    except Exception as e:
        warnings.append(f"miss_analysis_tag_compliance チェック失敗: {e}")

    # === 結果出力 ===
    print(f"{BOLD}--- [OK] 正常項目 ---{RESET}")
    for g in goods:
        print(f"  {GREEN}✓{RESET} {g}")
    if warnings:
        print(f"\n{BOLD}--- [WARN] 警告 ---{RESET}")
        for w in warnings:
            print(f"  {YELLOW}⚠{RESET}  {w}")
    if anomalies:
        print(f"\n{BOLD}--- [ALERT] 異常（優先対処必須） ---{RESET}")
        for a in anomalies:
            print(f"  {RED}✗{RESET}  {a}")

    # 判定
    print()
    if anomalies:
        print(f"{RED}{BOLD}[ALERT] 異常 {len(anomalies)}件 検出。セッション作業開始前に対処してください。{RESET}")
        return 2
    elif warnings:
        print(f"{YELLOW}{BOLD}[WARN] 警告 {len(warnings)}件。STEP 1 以降の通常業務開始可能だが監視継続。{RESET}")
        return 1
    else:
        print(f"{GREEN}{BOLD}[OK] システム健全。STEP 1 以降の通常業務へ進んでください。{RESET}")
        return 0

if __name__ == "__main__":
    sys.exit(main())
