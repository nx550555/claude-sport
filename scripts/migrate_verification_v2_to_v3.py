#!/usr/bin/env python3
"""
GEN009 v2 verification 構造を v3 (facts/analysis/rules_implication 分離) にマイグレーション。

対象: records/tennis/2026-ATP.json + records/wta/2026.json
変更内容:
  1. 既存 note の内容を facts に移行
  2. analysis を {decisive_factor: null, market_blind_spot: null, confidence_level: null} で初期化
  3. rules_implication を {candidate_pattern: null, rule_candidate_id: null, replicability: null} で初期化
  4. source_tier は既存値を保持、なければ "primary" を設定
  5. 元の note フィールドは削除

使い方:
  python scripts/migrate_verification_v2_to_v3.py --dry-run   # 件数表示のみ
  python scripts/migrate_verification_v2_to_v3.py             # 本実行 (書き込み)
"""

import json
import os
import argparse


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TARGET_FILES = [
    os.path.join(REPO_ROOT, "records", "tennis", "2026-ATP.json"),
    os.path.join(REPO_ROOT, "records", "wta", "2026.json"),
]


def has_v2_schema(v):
    """v2 schema (note フィールドあり, facts フィールドなし) かを判定"""
    if not isinstance(v, dict):
        return False
    return "note" in v and "facts" not in v


def has_v3_schema(v):
    """既に v3 にマイグ済みか"""
    if not isinstance(v, dict):
        return False
    return "facts" in v


def migrate_one(v):
    """1 つの verification dict を v3 に書き換える (in-place)"""
    if not isinstance(v, dict):
        return False

    if has_v3_schema(v):
        return False  # 既に v3

    if not has_v2_schema(v):
        return False  # note なし → 何もしない (skip)

    # 1. note → facts
    note_content = (v.get("note") or "").strip()
    v["facts"] = note_content

    # 2. analysis を null 初期化
    v["analysis"] = {
        "decisive_factor": None,
        "market_blind_spot": None,
        "confidence_level": None,
    }

    # 3. rules_implication を null 初期化
    v["rules_implication"] = {
        "candidate_pattern": None,
        "rule_candidate_id": None,
        "replicability": None,
    }

    # 4. source_tier 既存値保持 / なければ primary
    if "source_tier" not in v:
        v["source_tier"] = "primary"

    # 5. note 削除
    del v["note"]

    return True


def walk_and_migrate(o, stats):
    """JSON を再帰探索して verification をマイグレーション"""
    if isinstance(o, dict):
        # 親が verification を持っている場合の処理
        if isinstance(o.get("verification"), dict):
            v = o["verification"]
            if has_v3_schema(v):
                stats["already_v3"] += 1
            elif has_v2_schema(v):
                # depth を確認
                depth = v.get("depth", "?")
                if depth == "light":
                    stats["v2_light"] += 1
                elif depth == "deep":
                    stats["v2_deep"] += 1
                else:
                    stats["v2_unknown_depth"] += 1
                # マイグ実行
                ok = migrate_one(v)
                if ok:
                    stats["migrated"] += 1
            else:
                stats["other"] += 1

        for val in o.values():
            walk_and_migrate(val, stats)
    elif isinstance(o, list):
        for v in o:
            walk_and_migrate(v, stats)


def process_file(fp, dry_run):
    rel = os.path.relpath(fp, REPO_ROOT)
    print(f"\n=== {rel} ===")
    if not os.path.exists(fp):
        print("  (file not found, skip)")
        return None

    with open(fp, encoding="utf-8") as f:
        data = json.load(f)

    stats = {
        "v2_light": 0,
        "v2_deep": 0,
        "v2_unknown_depth": 0,
        "already_v3": 0,
        "migrated": 0,
        "other": 0,
    }

    walk_and_migrate(data, stats)

    print(f"  v2 light       : {stats['v2_light']}")
    print(f"  v2 deep        : {stats['v2_deep']}")
    print(f"  v2 unknown     : {stats['v2_unknown_depth']}")
    print(f"  already v3     : {stats['already_v3']}")
    print(f"  migrated       : {stats['migrated']}")
    print(f"  other          : {stats['other']}")

    if dry_run:
        print(f"  [dry-run] 書き込みスキップ")
    else:
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  [written] {rel}")

    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="件数表示のみ、書き込みしない")
    args = parser.parse_args()

    print(f"GEN009 v2 verification schema v2 -> v3 migration")
    print(f"  dry-run: {args.dry_run}")

    total = {
        "v2_light": 0, "v2_deep": 0, "v2_unknown_depth": 0,
        "already_v3": 0, "migrated": 0, "other": 0,
    }
    for fp in TARGET_FILES:
        s = process_file(fp, args.dry_run)
        if s:
            for k, n in s.items():
                total[k] += n

    print(f"\n=== TOTAL ===")
    for k, n in total.items():
        print(f"  {k:18}: {n}")


if __name__ == "__main__":
    main()
