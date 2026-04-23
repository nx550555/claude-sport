# -*- coding: utf-8 -*-
"""
日次ダイジェストメール通知 (B 系)

JST 23:00 に 1 日分の GO 昇格・スタメン変動・結果確定をまとめて 1 通。
GitHub Actions cron で定期実行する。

使い方:
  python scripts/notify_digest.py                  # 当日ダイジェスト送信
  python scripts/notify_digest.py --date 2026-04-23 # 指定日
  python scripts/notify_digest.py --dry-run

環境変数 (GitHub Secrets 経由):
  SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS
  NOTIFY_TO / NOTIFY_FROM
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# notify_go_candidate から send_email を再利用
sys.path.insert(0, str(Path(__file__).resolve().parent))
from notify_go_candidate import send_email  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
JST = timezone(timedelta(hours=9))


def collect_today(target_date: str) -> dict:
    """records 全件を走査し、指定日の go/caution/result をまとめる"""
    records_dir = ROOT / "records"
    summary = {
        "date": target_date,
        "new_go": [],
        "caution_waiting": [],
        "results_hit": [],
        "results_miss": [],
        "provisional_go_not_upgraded": [],
    }
    for records_file in records_dir.rglob("*.json"):
        try:
            data = json.loads(records_file.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        preds = data.get("predictions", [])
        if not isinstance(preds, list):
            continue
        sport = data.get("sport", records_file.parent.name)
        for p in preds:
            if not isinstance(p, dict):
                continue
            # その日に発生したイベントのみ集計
            notified_at = p.get("notified_at", "")
            date_f = p.get("date", "") or p.get("kickoff", "")
            if target_date not in (notified_at + " " + date_f):
                continue

            match = p.get("match") or f"{p.get('home','?')} vs {p.get('away','?')}"
            tier = p.get("tier")
            hit = p.get("hit")

            entry = {
                "sport": sport,
                "match": match,
                "tier": tier,
                "conf": p.get("prediction_confidence") or p.get("confidence"),
                "ev": p.get("ev"),
                "rec": p.get("rec") or p.get("predicted_winner"),
                "odds": p.get("rec_odds") or p.get("odds"),
                "result": p.get("result"),
                "score": p.get("score"),
                "actual_ev": p.get("actual_ev"),
            }

            if tier == "go" and p.get("notified"):
                summary["new_go"].append(entry)
            elif tier == "caution_waiting":
                summary["caution_waiting"].append(entry)
            elif tier == "provisional_go":
                summary["provisional_go_not_upgraded"].append(entry)

            if hit is True:
                summary["results_hit"].append(entry)
            elif hit is False:
                summary["results_miss"].append(entry)
    return summary


def build_digest_body(summary: dict) -> str:
    lines = []
    lines.append(f"▼ 日次ダイジェスト ({summary['date']})")
    lines.append("")

    lines.append(f"─── 新規 GO 昇格: {len(summary['new_go'])} 件 ───")
    for g in summary["new_go"]:
        lines.append(f"  [{g['sport'].upper()}] {g['match']} | {g['rec']} @ {g['odds']} conf={g['conf']}% EV=+{g['ev']}%")
    lines.append("")

    lines.append(f"─── CAUTION WAITING (スタメン未発表でキックオフ): {len(summary['caution_waiting'])} 件 ───")
    for g in summary["caution_waiting"]:
        lines.append(f"  [{g['sport'].upper()}] {g['match']}")
    lines.append("")

    lines.append(f"─── 仮GO→正式GO昇格せず (EV閾値未達): {len(summary['provisional_go_not_upgraded'])} 件 ───")
    for g in summary["provisional_go_not_upgraded"]:
        lines.append(f"  [{g['sport'].upper()}] {g['match']} (再計算後 conf={g['conf']}% EV={g['ev']}%)")
    lines.append("")

    lines.append(f"─── 結果 HIT: {len(summary['results_hit'])} 件 ───")
    for g in summary["results_hit"]:
        lines.append(f"  [{g['sport'].upper()}] {g['match']} | {g['result']} ({g['score']}) +{g['actual_ev']}u")
    lines.append("")

    lines.append(f"─── 結果 MISS: {len(summary['results_miss'])} 件 ───")
    for g in summary["results_miss"]:
        lines.append(f"  [{g['sport'].upper()}] {g['match']} | {g['result']} ({g['score']}) {g['actual_ev']}u")
    lines.append("")

    lines.append("─" * 40)
    lines.append("このメールは claude-sport システムからの日次ダイジェスト (B 系) です。")
    lines.append(f"送信時刻: {datetime.now(JST).isoformat()}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (default: 今日)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    target_date = args.date or datetime.now(JST).strftime("%Y-%m-%d")
    summary = collect_today(target_date)
    body = build_digest_body(summary)
    subject = f"[claude-sport] 日次ダイジェスト {target_date}"

    # イベント全件 0 なら送らない (ノイズ削減)
    total_events = (
        len(summary["new_go"]) + len(summary["caution_waiting"])
        + len(summary["provisional_go_not_upgraded"])
        + len(summary["results_hit"]) + len(summary["results_miss"])
    )
    if total_events == 0 and not args.dry_run:
        print("[SKIP] no events to digest")
        sys.exit(0)

    ok = send_email(subject, body, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
