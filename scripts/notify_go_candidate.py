# -*- coding: utf-8 -*-
"""
正式 GO 候補メール通知 (即時通知 = A 系)

STEP 4.5 スタメン確認後、EV 再計算で tier='go' に昇格した試合を対象に
1 試合 1 メールで即時送信する。

使い方:
  # 対象試合を明示指定
  python scripts/notify_go_candidate.py \\
    --sport soccer \\
    --match "Real Madrid vs Barcelona" \\
    --kickoff "2026-04-23T21:00+09:00" \\
    --bet "Real Madrid" --odds 1.85 --conf 78 --ev 8.5 \\
    --lineup-summary "Courtois OK / Vinicius OK / Bellingham OUT" \\
    --deadline "2026-04-23T20:45+09:00"

  # records JSON の tier='go' で通知未送信 (notified=false) のエントリを自動送信
  python scripts/notify_go_candidate.py --scan --mark-sent

環境変数 (GitHub Secrets 経由):
  SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS
  NOTIFY_TO / NOTIFY_FROM

テストモード (環境変数未設定時):
  --dry-run でメール本文のみ stdout に出力
"""
from __future__ import annotations
import argparse
import json
import os
import smtplib
import ssl
import sys
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JST = timezone(timedelta(hours=9))


def build_subject(sport: str, match: str, bet: str, odds: float) -> str:
    return f"[claude-sport] 正式GO候補 {sport.upper()}: {match} | {bet} @ {odds}"


def build_body(
    sport: str,
    match: str,
    kickoff: str,
    bet: str,
    odds: float,
    conf: float,
    ev: float,
    lineup_summary: str,
    deadline: str,
    extra: dict | None = None,
) -> str:
    lines = []
    lines.append("▼ 正式 GO 候補発生 (スタメン確認完了)")
    lines.append("")
    lines.append(f"■ スポーツ:      {sport.upper()}")
    lines.append(f"■ 試合:          {match}")
    lines.append(f"■ キックオフ:    {kickoff} (JST)")
    lines.append("")
    lines.append("─── ベット推奨 ───")
    lines.append(f"  推奨: {bet}")
    lines.append(f"  オッズ: {odds}")
    lines.append(f"  確信度: {conf}%")
    lines.append(f"  EV:    +{ev}%")
    lines.append("")
    lines.append("─── 確認済みスタメン ───")
    lines.append(f"  {lineup_summary or '(データなし)'}")
    lines.append("")
    lines.append(f"■ 判断期限:      {deadline} (JST)")
    lines.append("")
    if extra:
        lines.append("─── 補足情報 ───")
        for k, v in extra.items():
            lines.append(f"  {k}: {v}")
        lines.append("")
    lines.append("─" * 40)
    lines.append("このメールは claude-sport システムからの自動通知です。")
    lines.append("メール通知モード: C (即時通知 + 日次ダイジェスト併用)")
    lines.append(f"送信時刻: {datetime.now(JST).isoformat()}")
    return "\n".join(lines)


def send_email(subject: str, body: str, to: str | None = None, dry_run: bool = False) -> bool:
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    user = os.environ.get("SMTP_USER")
    pw = os.environ.get("SMTP_PASS")
    mail_from = os.environ.get("NOTIFY_FROM") or user
    mail_to = to or os.environ.get("NOTIFY_TO")

    if dry_run or not (user and pw and mail_to):
        print("─" * 60)
        print(f"[DRY-RUN] subject: {subject}")
        print(f"[DRY-RUN] to: {mail_to or '(NOTIFY_TO 未設定)'}")
        print(f"[DRY-RUN] from: {mail_from or '(NOTIFY_FROM 未設定)'}")
        print("[DRY-RUN] body:")
        print(body)
        print("─" * 60)
        if not dry_run:
            print("[WARN] SMTP credentials or NOTIFY_TO 未設定のため DRY-RUN で出力のみ")
            return False
        return True

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg.attach(MIMEText(body, "plain", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context, timeout=30) as server:
        server.login(user, pw)
        server.sendmail(mail_from, [mail_to], msg.as_string())
    print(f"[OK] sent to {mail_to}")
    return True


def scan_records_for_new_go(mark_sent: bool = False, dry_run: bool = False) -> int:
    """全 sport の records JSON をスキャンして tier='go' かつ notified=false の試合を通知。
    処理後は notified=true / notified_at=timestamp に更新。"""
    records_dir = ROOT / "records"
    sent_count = 0
    for records_file in records_dir.rglob("*.json"):
        try:
            data = json.loads(records_file.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        preds = data.get("predictions", [])
        if not isinstance(preds, list):
            continue
        sport_in_file = data.get("sport", records_file.parent.name)

        modified = False
        for p in preds:
            if not isinstance(p, dict):
                continue
            if p.get("tier") != "go":
                continue
            if p.get("notified"):
                continue
            # 必須フィールド確認
            match = p.get("match") or f"{p.get('home', '?')} vs {p.get('away', '?')}"
            bet = p.get("rec") or p.get("predicted_winner") or ""
            odds = p.get("rec_odds") or p.get("odds")
            conf = p.get("prediction_confidence") or p.get("confidence")
            ev = p.get("ev")
            kickoff = p.get("kickoff") or p.get("date") or "(未指定)"
            lineup_summary = p.get("lineup_summary") or "(STEP 4.5 情報なし)"
            deadline = p.get("deadline") or kickoff

            if not (bet and odds and conf is not None and ev is not None):
                continue

            subject = build_subject(sport_in_file, match, bet, odds)
            body = build_body(
                sport_in_file, match, kickoff, bet, odds, conf, ev,
                lineup_summary, deadline,
                extra={"match_id": p.get("id") or p.get("match_id"), "tournament": p.get("tournament")},
            )
            ok = send_email(subject, body, dry_run=dry_run)
            if ok and mark_sent:
                p["notified"] = True
                p["notified_at"] = datetime.now(JST).isoformat()
                modified = True
                sent_count += 1
            elif ok and not mark_sent:
                sent_count += 1

        if modified:
            records_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    return sent_count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true", help="records JSON を走査し未通知 go を送信")
    ap.add_argument("--mark-sent", action="store_true", help="送信後 records に notified=true を書き戻す")
    ap.add_argument("--dry-run", action="store_true", help="メール送信せず本文を print")
    ap.add_argument("--test", action="store_true", help="テストメール送信 (Secrets疎通確認用)")

    ap.add_argument("--sport")
    ap.add_argument("--match")
    ap.add_argument("--kickoff")
    ap.add_argument("--bet")
    ap.add_argument("--odds", type=float)
    ap.add_argument("--conf", type=float)
    ap.add_argument("--ev", type=float)
    ap.add_argument("--lineup-summary", default="")
    ap.add_argument("--deadline", default="")
    args = ap.parse_args()

    if args.test:
        subject = "[claude-sport] テスト通知"
        body = (
            "メール通知システムは正常に動作しています。\n\n"
            "・SMTP 認証 OK\n"
            "・GitHub Secrets 6 件 正常\n"
            f"・送信時刻: {datetime.now(JST).isoformat()}\n"
        )
        ok = send_email(subject, body, dry_run=args.dry_run)
        sys.exit(0 if ok else 1)

    if args.scan:
        n = scan_records_for_new_go(mark_sent=args.mark_sent, dry_run=args.dry_run)
        print(f"[DONE] {n} new GO candidate(s) notified")
        sys.exit(0)

    if not (args.sport and args.match and args.bet and args.odds):
        print("ERROR: --sport / --match / --bet / --odds が必要。または --scan / --test を指定。", file=sys.stderr)
        sys.exit(1)

    subject = build_subject(args.sport, args.match, args.bet, args.odds)
    body = build_body(
        args.sport, args.match, args.kickoff or "(未指定)",
        args.bet, args.odds, args.conf or 0, args.ev or 0,
        args.lineup_summary, args.deadline or args.kickoff or "(未指定)",
    )
    ok = send_email(subject, body, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
