# -*- coding: utf-8 -*-
"""
stats/external_feeds/ の最新フィードを読み込むヘルパー。

Usage (Claude session 内):
  from scripts.stats_feed_reader import get_team_xgf, get_nrtg, feed_status
  x = get_team_xgf('COL')       # -> 56.67
  n = get_nrtg('BOS')            # -> 8.1 (nrtg_adj)
  st = feed_status()             # -> {"nhl": {"age_days": 1.2, "stale": False}, ...}

古い (>3日) / 欠落 なら GEN006 依頼を Claude 側で発動する合図を返す。
"""
from __future__ import annotations
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED_DIR = ROOT / "stats" / "external_feeds"
JST = timezone(timedelta(hours=9))

STALE_DAYS = 3

# チーム名→略称対応（MoneyPuck 側の表記揺れ吸収）
NHL_ALIAS = {
    "Colorado Avalanche": "COL", "Tampa Bay Lightning": "TBL",
    "Montreal Canadiens": "MTL", "Boston Bruins": "BOS",
    "Buffalo Sabres": "BUF", "Carolina Hurricanes": "CAR",
    "Ottawa Senators": "OTT", "Pittsburgh Penguins": "PIT",
    "Philadelphia Flyers": "PHI", "Los Angeles Kings": "LAK",
    "Dallas Stars": "DAL", "Minnesota Wild": "MIN",
    "Vegas Golden Knights": "VGK", "Utah Mammoth": "UTA",
    "Edmonton Oilers": "EDM", "Anaheim Ducks": "ANA",
    "New York Rangers": "NYR", "New York Islanders": "NYI",
    "Toronto Maple Leafs": "TOR", "Winnipeg Jets": "WPG",
    "St. Louis Blues": "STL", "Nashville Predators": "NSH",
    "Calgary Flames": "CGY", "Vancouver Canucks": "VAN",
    "Seattle Kraken": "SEA", "San Jose Sharks": "SJS",
    "Chicago Blackhawks": "CHI", "Detroit Red Wings": "DET",
    "Florida Panthers": "FLA", "Columbus Blue Jackets": "CBJ",
    "New Jersey Devils": "NJD", "Washington Capitals": "WSH",
}

NBA_ALIAS = {}  # bbref は team_name full で入るが略称照合用（必要時追加）


def _latest(pattern: str) -> Path | None:
    files = sorted(FEED_DIR.glob(pattern))
    return files[-1] if files else None


def _age_days(p: Path) -> float:
    m = datetime.fromtimestamp(p.stat().st_mtime, tz=JST)
    return (datetime.now(JST) - m).total_seconds() / 86400


FEED_CATALOG = {
    "nhl_team":           ("nhl_moneypuck_*.json",          3),
    "nhl_skaters":        ("nhl_skaters_*.json",            3),
    "nhl_goalies":        ("nhl_goalies_*.json",            3),
    "nhl_injuries":       ("nhl_injuries_*.json",           1),
    "nba_team":           ("nba_bbref_*.json",              3),
    "nba_per_game":       ("nba_players_per_game_*.json",   3),
    "nba_advanced":       ("nba_players_advanced_*.json",   3),
    "nba_injuries":       ("nba_injuries_*.json",           1),
    "tennis_atp_elo":     ("tennis_atp_elo_*.json",         3),
    "tennis_wta_elo":     ("tennis_wta_elo_*.json",         3),
    "tennis_atp_stats":   ("tennis_atp_player_stats_*.json",7),
    "tennis_wta_stats":   ("tennis_wta_player_stats_*.json",7),
    "tennis_withdrawals": ("tennis_withdrawals_*.json",     1),
    "nrl_standings":      ("nrl_standings_*.json",          3),
    "superrugby_standings":("superrugby_standings_*.json",  3),
    "premiership_standings":("premiership_standings_*.json",3),
    "top14_standings":    ("top14_standings_*.json",        3),
    "prod2_standings":    ("prod2_standings_*.json",        3),
    "superleague_standings":("superleague_standings_*.json",3),
    "ufl_standings":      ("ufl_standings_*.json",          3),
    "cfl_standings":      ("cfl_standings_*.json",          3),
}


def feed_status() -> dict:
    """各フィードの最新状況を返す (catalog 全件)"""
    out = {}
    for key, (pat, thresh) in FEED_CATALOG.items():
        latest = _latest(pat)
        if not latest:
            out[key] = {"available": False, "stale": True, "message": "GEN006 必要: フィード未取得"}
            continue
        age = _age_days(latest)
        stale = age > thresh
        out[key] = {
            "available": True,
            "file": latest.name,
            "age_days": round(age, 2),
            "threshold_days": thresh,
            "stale": stale,
            "message": f"GEN006 発動可 (age={age:.1f} > thresh={thresh})" if stale else "OK"
        }
    return out


def stale_feeds() -> list[str]:
    """閾値超過 or 未取得のフィード名一覧（GEN006 依頼時の対象）"""
    return [k for k, v in feed_status().items() if not v.get("available") or v.get("stale")]


def _load(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _match_team(name: str, alias_map: dict, team_field: str = "team") -> callable:
    """チーム名 → 略称 or そのまま で検索する内部クロージャ"""
    # フルネーム → 略称変換
    abbr = alias_map.get(name, name)
    def matcher(entry: dict) -> bool:
        t = (entry.get(team_field) or "").strip()
        return t == name or t == abbr or alias_map.get(t) == abbr
    return matcher


def _iter_teams(container):
    """teams が dict (abbr->entry) でも list でも扱えるようにする"""
    if isinstance(container, dict):
        return list(container.values())
    if isinstance(container, list):
        return container
    return []


def get_team_xgf(team: str, score_adj: bool = False, situation: str = "all") -> float | None:
    """MoneyPuck xGF% 取得。situation='all' or '5on5'. score_adj=True で score-adjusted 値"""
    p = _latest("nhl_moneypuck_*.json")
    if not p:
        return None
    data = _load(p)
    teams_container = data.get("teams") if situation == "all" else data.get("teams_5on5") or data.get("teams")
    matcher = _match_team(team, NHL_ALIAS)
    for entry in _iter_teams(teams_container):
        if isinstance(entry, dict) and matcher(entry):
            return entry.get("xGF_pct_score_adj" if score_adj else "xGF_pct")
    return None


def get_team_gf_pct(team: str, situation: str = "all") -> float | None:
    p = _latest("nhl_moneypuck_*.json")
    if not p:
        return None
    data = _load(p)
    teams_container = data.get("teams") if situation == "all" else data.get("teams_5on5") or data.get("teams")
    matcher = _match_team(team, NHL_ALIAS)
    for entry in _iter_teams(teams_container):
        if isinstance(entry, dict) and matcher(entry):
            return entry.get("GF_pct")
    return None


def get_team_pdo(team: str) -> float | None:
    # PDO は直接カラムに無いため GF% / xGF% の差分で proxy 計算
    xgf = get_team_xgf(team, situation="5on5")
    gf = get_team_gf_pct(team, situation="5on5")
    if xgf is None or gf is None:
        return None
    # PDO proxy: over/under-performance vs xGF% (5v5)
    return round((gf - xgf) + 100, 2)


def get_nrtg(team: str, adj: bool = True) -> float | None:
    """Basketball Reference NRtg 取得。adj=True (default) は SOS調整後."""
    p = _latest("nba_bbref_*.json")
    if not p:
        return None
    data = _load(p)
    for entry in data.get("teams", []):
        t = (entry.get("team") or "").strip()
        if t == team or team in t:
            return entry.get("nrtg_adj" if adj else "nrtg")
    return None


def get_nhl_all_teams() -> dict | list | None:
    """全 NHL チームのフィード内容を返す（スクリーニング一括処理用）。"""
    p = _latest("nhl_moneypuck_*.json")
    return _load(p).get("teams") if p else None


def get_nba_all_teams() -> list | None:
    p = _latest("nba_bbref_*.json")
    return _load(p).get("teams") if p else None


# ===== NHL 選手関連 =====

def get_nhl_skater(name: str, situation: str = "all") -> dict | None:
    """選手名 or player_id で NHL skater の統計行を取得 (situation filter)"""
    p = _latest("nhl_skaters_*.json")
    if not p:
        return None
    data = _load(p)
    by_pid = data.get("by_player_id", {})
    for pid, rows in by_pid.items():
        if not rows:
            continue
        # name matching: partial
        if any(name.lower() in (r.get("name") or "").lower() for r in rows):
            for r in rows:
                if r.get("situation") == situation:
                    return r
            return rows[0]
    return None


def get_nhl_goalie(name: str, situation: str = "all") -> dict | None:
    p = _latest("nhl_goalies_*.json")
    if not p:
        return None
    data = _load(p)
    for pid, rows in data.get("by_player_id", {}).items():
        if not rows:
            continue
        if any(name.lower() in (r.get("name") or "").lower() for r in rows):
            for r in rows:
                if r.get("situation") == situation:
                    return r
            return rows[0]
    return None


def get_nhl_injuries_for_team(team: str) -> list[dict]:
    """team 略称/フル名で NHL 怪我情報をフィルタ"""
    p = _latest("nhl_injuries_*.json")
    if not p:
        return []
    data = _load(p)
    abbr = NHL_ALIAS.get(team, team)
    out = []
    for inj in data.get("injuries", []):
        t = inj.get("team") or ""
        if t == team or t == abbr or abbr in t or team in t:
            out.append(inj)
    return out


def get_nhl_starting_goalies() -> list[dict]:
    p = _latest("nhl_injuries_*.json")
    return _load(p).get("starting_goalies", []) if p else []


# ===== NBA 選手関連 =====

def get_nba_player_stats(name: str, kind: str = "advanced") -> dict | None:
    """kind: 'per_game' or 'advanced'"""
    p = _latest(f"nba_players_{kind}_*.json")
    if not p:
        return None
    for r in _load(p).get("players", []):
        if name.lower() in (r.get("player") or "").lower():
            return r
    return None


def get_nba_injuries_for_team(team: str) -> list[dict]:
    p = _latest("nba_injuries_*.json")
    if not p:
        return []
    out = []
    for inj in _load(p).get("injuries", []):
        t = inj.get("team") or ""
        if t == team or team in t:
            out.append(inj)
    return out


# ===== Tennis 選手関連 =====

def get_tennis_elo(player: str, tour: str = "atp") -> dict | None:
    p = _latest(f"tennis_{tour}_elo_*.json")
    if not p:
        return None
    for r in _load(p).get("players", []):
        if player.lower() in (r.get("player") or "").lower():
            return r
    return None


def get_tennis_serve_stats(player: str, tour: str = "atp") -> dict | None:
    p = _latest(f"tennis_{tour}_player_stats_*.json")
    if not p:
        return None
    for r in _load(p).get("serve", {}).get("rows", []):
        if player.lower() in (r.get("player") or "").lower():
            return r
    return None


def get_tennis_return_stats(player: str, tour: str = "atp") -> dict | None:
    p = _latest(f"tennis_{tour}_player_stats_*.json")
    if not p:
        return None
    for r in _load(p).get("return", {}).get("rows", []):
        if player.lower() in (r.get("player") or "").lower():
            return r
    return None


# ===== Rugby / Football standings =====

def get_league_standings(league: str) -> list[dict] | None:
    """league: nrl, superrugby, premiership, top14, prod2, superleague, ufl, cfl"""
    p = _latest(f"{league}_standings_*.json")
    return _load(p).get("teams") if p else None


def get_league_team(league: str, team: str) -> dict | None:
    teams = get_league_standings(league) or []
    for t in teams:
        tn = t.get("team") or ""
        if tn == team or team in tn or tn in team:
            return t
    return None


if __name__ == "__main__":
    import json as _j
    print(_j.dumps(feed_status(), indent=2, ensure_ascii=False))
