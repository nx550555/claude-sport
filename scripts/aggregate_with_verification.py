#!/usr/bin/env python3
"""
GEN009 v2 verification 準拠状況を含む3軸集計。

aggregate_stats.py とは別ファイル。既存運用に影響を与えない。

集計軸:
  (A) all      : 全データ (legacy + verified)
  (B) verified : verification フィールドありのみ (新ルール準拠)
  (C) legacy   : verification フィールドなしのみ (旧データ)

使い方:
  python scripts/aggregate_with_verification.py            # 全スポーツ
  python scripts/aggregate_with_verification.py --sport atp  # ATP のみ
  出力: _verification_aggregate.json (リポジトリルート)
"""

import json
import os
import glob
import argparse
from collections import defaultdict


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RECORDS_ROOT = os.path.join(REPO_ROOT, "records")

EXCLUDED_STATUSES = {"walkover", "cancelled", "duplicate_removed", "invalid", "void", "retired"}


def label_record(rec):
    """各レコードを 'verified' / 'legacy' / 'excluded' に分類"""
    if not isinstance(rec, dict):
        return None

    # 試合レコードの判定 (tier or prediction_hit or predicted_winner を持つ)
    if not (("tier" in rec) or ("prediction_hit" in rec) or ("predicted_winner" in rec)):
        return None

    match_status = (rec.get("match_status") or "").lower()
    status = (rec.get("status") or "").lower()
    if match_status in EXCLUDED_STATUSES:
        return "excluded"
    if status in EXCLUDED_STATUSES:
        return "excluded"
    if rec.get("void") is True:
        return "excluded"

    ph = rec.get("prediction_hit")
    if ph is None:
        return None  # 未確定 (集計対象外)

    if "verification" in rec and rec["verification"]:
        return "verified"
    return "legacy"


def walk(o, on_record):
    if isinstance(o, dict):
        on_record(o)
        for v in o.values():
            walk(v, on_record)
    elif isinstance(o, list):
        for v in o:
            walk(v, on_record)


def normalize_hit(ph):
    if ph in (True, "true", "True", "HIT", "hit"):
        return "hit"
    if ph in (False, "false", "False", "MISS", "miss"):
        return "miss"
    return None


def get_quadrant(rec):
    return (rec.get("quadrant") or rec.get("tier") or "unknown").lower()


def aggregate_file(fp):
    """1ファイルから verified / legacy / excluded を仕分けて集計"""
    sport_rel = os.path.relpath(fp, RECORDS_ROOT).replace("\\", "/")
    sport_key = sport_rel.split("/", 1)[0]

    counts = {
        "sport": sport_key,
        "file": sport_rel,
        "verified": {"total": 0, "hit": 0, "miss": 0, "by_quadrant": defaultdict(lambda: {"hit": 0, "miss": 0})},
        "legacy":   {"total": 0, "hit": 0, "miss": 0, "by_quadrant": defaultdict(lambda: {"hit": 0, "miss": 0})},
        "excluded": 0,
        "pending":  0,
    }

    try:
        with open(fp, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        counts["error"] = str(e)
        return counts

    def on_rec(rec):
        if not isinstance(rec, dict):
            return
        # 試合レコード判定
        if not (("tier" in rec) or ("prediction_hit" in rec) or ("predicted_winner" in rec)):
            return
        label = label_record(rec)
        if label is None:
            counts["pending"] += 1
            return
        if label == "excluded":
            counts["excluded"] += 1
            return

        ph = normalize_hit(rec.get("prediction_hit"))
        if ph is None:
            counts["pending"] += 1
            return

        bucket = counts[label]
        bucket["total"] += 1
        bucket[ph] += 1
        q = get_quadrant(rec)
        bucket["by_quadrant"][q][ph] += 1

    walk(data, on_rec)
    # defaultdict -> dict
    for label in ("verified", "legacy"):
        counts[label]["by_quadrant"] = {k: dict(v) for k, v in counts[label]["by_quadrant"].items()}
    return counts


def merge_buckets(a, b):
    """同一スポーツ内の複数ファイルをマージ"""
    out = {"total": a["total"] + b["total"],
           "hit":   a["hit"] + b["hit"],
           "miss":  a["miss"] + b["miss"],
           "by_quadrant": {}}
    keys = set(a["by_quadrant"]) | set(b["by_quadrant"])
    for k in keys:
        av = a["by_quadrant"].get(k, {"hit": 0, "miss": 0})
        bv = b["by_quadrant"].get(k, {"hit": 0, "miss": 0})
        out["by_quadrant"][k] = {"hit": av.get("hit", 0) + bv.get("hit", 0),
                                 "miss": av.get("miss", 0) + bv.get("miss", 0)}
    return out


def empty_bucket():
    return {"total": 0, "hit": 0, "miss": 0, "by_quadrant": {}}


def hit_rate(b):
    return (b["hit"] / b["total"]) if b["total"] > 0 else None


def aggregate(sport_filter=None):
    """全 records/*.json を走査して 3軸集計を返す"""
    files = sorted(glob.glob(os.path.join(RECORDS_ROOT, "**", "*.json"), recursive=True))
    files = [f for f in files if "multi_bets" not in os.path.basename(f)]

    by_sport = {}  # sport -> {"verified": bucket, "legacy": bucket, "excluded": int, "pending": int}
    file_details = []

    for fp in files:
        c = aggregate_file(fp)
        if "error" in c:
            file_details.append(c)
            continue
        sport = c["sport"]
        if sport_filter and sport != sport_filter:
            continue
        if sport not in by_sport:
            by_sport[sport] = {
                "verified": empty_bucket(),
                "legacy":   empty_bucket(),
                "excluded": 0,
                "pending":  0,
                "files":    [],
            }
        by_sport[sport]["verified"] = merge_buckets(by_sport[sport]["verified"], c["verified"])
        by_sport[sport]["legacy"]   = merge_buckets(by_sport[sport]["legacy"],   c["legacy"])
        by_sport[sport]["excluded"] += c["excluded"]
        by_sport[sport]["pending"]  += c["pending"]
        by_sport[sport]["files"].append(c["file"])
        file_details.append(c)

    # オールスポーツ合算 (3軸)
    total = {"verified": empty_bucket(), "legacy": empty_bucket(), "excluded": 0, "pending": 0}
    for sport, b in by_sport.items():
        total["verified"] = merge_buckets(total["verified"], b["verified"])
        total["legacy"]   = merge_buckets(total["legacy"],   b["legacy"])
        total["excluded"] += b["excluded"]
        total["pending"]  += b["pending"]

    # all = legacy + verified
    total["all"] = merge_buckets(total["verified"], total["legacy"])

    # スポーツ別準拠率
    sport_compliance = []
    for sport, b in sorted(by_sport.items()):
        confirmed = b["verified"]["total"] + b["legacy"]["total"]
        verified_n = b["verified"]["total"]
        compliance = (verified_n / confirmed * 100) if confirmed > 0 else None
        sport_compliance.append({
            "sport": sport,
            "confirmed_total": confirmed,
            "verified_count": verified_n,
            "legacy_count": b["legacy"]["total"],
            "verified_pct": compliance,
            "excluded": b["excluded"],
            "pending": b["pending"],
        })

    # サマリ表
    summary = {
        "axis_A_all": {
            "total": total["all"]["total"],
            "hit": total["all"]["hit"],
            "miss": total["all"]["miss"],
            "hit_rate": hit_rate(total["all"]),
        },
        "axis_B_verified_only": {
            "total": total["verified"]["total"],
            "hit": total["verified"]["hit"],
            "miss": total["verified"]["miss"],
            "hit_rate": hit_rate(total["verified"]),
        },
        "axis_C_legacy_only": {
            "total": total["legacy"]["total"],
            "hit": total["legacy"]["hit"],
            "miss": total["legacy"]["miss"],
            "hit_rate": hit_rate(total["legacy"]),
        },
        "excluded_total": total["excluded"],
        "pending_total": total["pending"],
    }

    return {
        "summary_3axis": summary,
        "by_sport": {sport: {
            "verified": b["verified"],
            "legacy":   b["legacy"],
            "all":      merge_buckets(b["verified"], b["legacy"]),
            "excluded": b["excluded"],
            "pending":  b["pending"],
        } for sport, b in by_sport.items()},
        "sport_compliance": sport_compliance,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sport", default=None, help="特定スポーツのみ集計 (例: tennis, nhl)")
    parser.add_argument("--out", default=os.path.join(REPO_ROOT, "_verification_aggregate.json"))
    args = parser.parse_args()

    result = aggregate(sport_filter=args.sport)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)

    print(f"Output: {args.out}")
    s = result["summary_3axis"]
    def fmt(b):
        hr = b["hit_rate"]
        hrs = f"{hr*100:.1f}%" if hr is not None else "n/a"
        return f"  total={b['total']:4d}  hit={b['hit']:4d}  miss={b['miss']:4d}  hit_rate={hrs}"
    print("\n=== 3軸集計 ===")
    print("(A) all          :"); print(fmt(s["axis_A_all"]))
    print("(B) verified only:"); print(fmt(s["axis_B_verified_only"]))
    print("(C) legacy only  :"); print(fmt(s["axis_C_legacy_only"]))
    print(f"excluded={s['excluded_total']}  pending={s['pending_total']}")

    print("\n=== スポーツ別準拠率 ===")
    print(f"{'sport':<14}{'confirmed':>10}{'verified':>10}{'legacy':>8}{'verified%':>12}{'pending':>9}{'excluded':>10}")
    for sc in result["sport_compliance"]:
        pct = f"{sc['verified_pct']:.1f}%" if sc["verified_pct"] is not None else "n/a"
        print(f"{sc['sport']:<14}{sc['confirmed_total']:>10}{sc['verified_count']:>10}{sc['legacy_count']:>8}{pct:>12}{sc['pending']:>9}{sc['excluded']:>10}")


if __name__ == "__main__":
    main()
