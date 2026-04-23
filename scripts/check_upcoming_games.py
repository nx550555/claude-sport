# -*- coding: utf-8 -*-
"""
直近キックオフ試合の抽出スクリプト (GitHub Actions lineup_watch 用)

records/{sport}/*.json を走査し、以下の条件に該当する試合があるか判定:
  - サッカー / ラグビー全種: キックオフまで 60-90 分以内 (75分前 fetch のため)
  - NBA / NFL: キックオフまで 75-105 分以内 (90分前 fetch のため)
  - MLB: JST 10:00 ± 30 分 = このスクリプトは時刻固定トリガなので毎回 true

出力 (stdout JSON):
  {"should_fetch": ["soccer", "nba"], "matches": [...]}

終了コード:
  0: 対象なし (lineup_watch は早期 return)
  10: 対象あり (workflow が fetch_lineups 実行)
  1: エラー
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JST = timezone(timedelta(hours=9))

# 各スポーツのスタメン取得リードタイム (分)
LEAD_MINUTES = {
    "soccer": 75,
    "mlb": 0,      # 時刻固定 (JST 10:00) なのでここでは無視
    "nba": 90,
    "nfl": 90,
    "nrl": 75,
    "superrugby": 75,
    "premiership": 75,
    "top14": 75,
    "prod2": 75,
    "super_league": 75,
}

# fetch_lineups 側のスポーツ名へマッピング
FETCH_SPORT_MAP = {
    "soccer": "soccer",
    "mlb": "mlb",
    "nba": "nba",
    "nfl": "nfl",
    "nrl": "rugby",
    "superrugby": "rugby",
    "premiership": "rugby",
    "top14": "rugby",
    "prod2": "rugby",
    "super_league": "rugby",
}


def parse_kickoff(p: dict) -> datetime | None:
    for field in ("kickoff", "start_time", "tipoff", "first_pitch", "date_jst"):
        v = p.get(field)
        if not v:
            continue
        try:
            # ISO 8601 想定
            if v.endswith("Z"):
                v = v.replace("Z", "+00:00")
            dt = datetime.fromisoformat(v)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=JST)
            return dt.astimezone(JST)
        except ValueError:
            continue
    return None


def scan(window_minutes: int = 15) -> dict:
    """現在から window_minutes 以内に各スポーツのリードタイム±window を満たす試合を抽出"""
    now = datetime.now(JST)
    result = {"now": now.isoformat(), "should_fetch": set(), "matches": []}
    records_dir = ROOT / "records"

    for records_file in records_dir.rglob("*.json"):
        try:
            data = json.loads(records_file.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        sport_in_file = data.get("sport") or records_file.parent.name
        lead = LEAD_MINUTES.get(sport_in_file)
        if lead is None:
            continue
        preds = data.get("predictions", [])
        if not isinstance(preds, list):
            continue
        for p in preds:
            if not isinstance(p, dict):
                continue
            if p.get("tier") not in ("provisional_go", "caution_waiting", "go"):
                continue
            if p.get("notified"):
                continue
            kickoff = parse_kickoff(p)
            if not kickoff:
                continue
            delta_min = (kickoff - now).total_seconds() / 60
            # 対象: lead - window 〜 lead + window (例: サッカー 60-90分前)
            if lead - window_minutes <= delta_min <= lead + window_minutes:
                fetch_sport = FETCH_SPORT_MAP[sport_in_file]
                result["should_fetch"].add(fetch_sport)
                result["matches"].append({
                    "sport": sport_in_file,
                    "fetch_sport": fetch_sport,
                    "match": p.get("match") or f"{p.get('home','?')} vs {p.get('away','?')}",
                    "kickoff": kickoff.isoformat(),
                    "minutes_until_kickoff": round(delta_min, 1),
                })
    result["should_fetch"] = sorted(result["should_fetch"])
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window-minutes", type=int, default=15,
                    help="現在時刻を中心に ±N 分の幅で対象判定")
    ap.add_argument("--pretty", action="store_true")
    args = ap.parse_args()

    result = scan(args.window_minutes)

    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))

    if result["should_fetch"]:
        sys.exit(10)
    sys.exit(0)


if __name__ == "__main__":
    main()
