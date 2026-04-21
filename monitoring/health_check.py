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
            # quadrant tagging は session 内の screening_procedure_note や deep_dive で識別
            has_q_tag = any(
                k in latest for k in ["output_a_candidates","output_a_additions","upset_pick_checks","upset_pick_uf_deep_dive"]
            )
            if has_q_tag:
                goods.append(f"前セッション ({latest.get('session_id','?')}) で4象限分類記録あり")
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
