"""Session_57: dashboard_stats.json 再生成 (records 実態と同期)"""
import json
from pathlib import Path

ROOT = Path("C:/Users/ohwada/Desktop/claude_sport")

RECORDS = {
    "atp": "records/tennis/2026-ATP.json",
    "wta": "records/wta/2026.json",
    "nhl": "records/nhl/2025-26.json",
    "ufl": "records/ufl/2026.json",
    "nrl": "records/nrl/2026.json",
    "nba": "records/nba/2025-26.json",
    "superrugby": "records/superrugby/2026.json",
    "premiership": "records/premiership/2026.json",
    "top14": "records/top14/2026.json",
    "prod2": "records/prod2/2026.json",
    "superleague": "records/superleague/2026.json",
    "ahl": "records/ahl/2025-26.json",
    "soccer": "records/soccer/2025-26.json",
    "mlb": "records/mlb/2026.json",
}

TIER_MAP = {
    "atp": "advanced",
    "wta": "advanced",
    "nhl": "advanced",
    "nba": "advanced",
    "soccer": "advanced",
    "mlb": "advanced",
    "ufl": "basic",
    "nrl": "basic",
    "superrugby": "basic",
    "premiership": "basic",
    "top14": "basic",
    "prod2": "basic",
    "superleague": "basic",
    "ahl": "basic",
}

def iter_preds(d):
    if "games" in d:
        return d["games"]
    if "predictions" in d:
        return d["predictions"]
    if "tournaments" in d:
        out = []
        for t in d["tournaments"]:
            out.extend(t.get("predictions", []))
        return out
    return []

stats = {}
for sport, path in RECORDS.items():
    full = ROOT / path
    if not full.exists():
        stats[sport] = {"go_count": 0, "confirmed_count": 0, "hit_count": 0, "hit_rate": None, "pnl": 0.0, "pending_count": 0}
        continue
    with open(full, encoding="utf-8-sig") as f:
        d = json.load(f)
    go_total, confirmed, hits, pnl, pending = 0, 0, 0, 0.0, 0
    for p in iter_preds(d):
        if p.get("tier") in ("invalid", "duplicate_closed"):
            continue
        if p.get("void"):  # VOID schema: bet refunded, exclude from stats (Session_57 提案#3)
            continue
        if p.get("tier") != "go":
            continue
        go_total += 1
        h = p.get("hit")
        if h is None:
            pending += 1
        else:
            confirmed += 1
            if h is True:
                hits += 1
            ae = p.get("actual_ev", 0) or 0
            if isinstance(ae, (int, float)):
                pnl += ae
    hit_rate = round(hits / confirmed, 3) if confirmed else None
    stats[sport] = {
        "go_count": go_total,
        "confirmed_count": confirmed,
        "hit_count": hits,
        "hit_rate": hit_rate,
        "pnl": round(pnl, 3),
        "pending_count": pending,
    }

# Overview
tot_go = sum(s["go_count"] for s in stats.values())
tot_conf = sum(s["confirmed_count"] for s in stats.values())
tot_hits = sum(s["hit_count"] for s in stats.values())
tot_pnl = round(sum(s["pnl"] for s in stats.values()), 3)
tot_pending = sum(s["pending_count"] for s in stats.values())
tot_hit_rate = round(tot_hits / tot_conf, 3) if tot_conf else None

# By tier
by_tier = {"advanced": {"go_count": 0, "confirmed_count": 0, "hit_count": 0, "pnl": 0.0, "pending_count": 0, "sports": []},
           "basic": {"go_count": 0, "confirmed_count": 0, "hit_count": 0, "pnl": 0.0, "pending_count": 0, "sports": []}}
for sport, s in stats.items():
    tier = TIER_MAP.get(sport)
    if tier is None:
        continue
    by_tier[tier]["go_count"] += s["go_count"]
    by_tier[tier]["confirmed_count"] += s["confirmed_count"]
    by_tier[tier]["hit_count"] += s["hit_count"]
    by_tier[tier]["pnl"] += s["pnl"]
    by_tier[tier]["pending_count"] += s["pending_count"]
    if sport not in by_tier[tier]["sports"]:
        by_tier[tier]["sports"].append(sport)

for t in by_tier.values():
    t["pnl"] = round(t["pnl"], 3)
    t["hit_rate"] = round(t["hit_count"] / t["confirmed_count"], 3) if t["confirmed_count"] else None

# Load existing to preserve notes
ds_path = ROOT / "core/dashboard_stats.json"
with open(ds_path, encoding="utf-8-sig") as f:
    existing = json.load(f)

out = {
    "_comment": existing.get("_comment"),
    "last_updated": "2026-04-24",
    "session": "_57",
    "sports": stats,
    "overview": {
        "total_go": tot_go,
        "total_confirmed": tot_conf,
        "total_hits": tot_hits,
        "hit_rate": tot_hit_rate,
        "total_pnl": tot_pnl,
        "total_pending": tot_pending,
        "pending_breakdown": "auto-generated Session_57",
    },
    "by_tier": by_tier,
    "session_45_notes": existing.get("session_45_notes", []),
    "session_47_notes": existing.get("session_47_notes"),
    "session_48_notes": existing.get("session_48_notes"),
    "session_49_notes": existing.get("session_49_notes"),
    "session_50_notes": existing.get("session_50_notes"),
    "session_57_notes": {
        "result_reflection": "ATP Paul MISS -1.0u (Tirante UPSET), ATP Musetti CAUTION no-bet HIT, ATP Tsitsipas CAUTION no-bet HIT, WTA Keys VOID (illness withdrawal). NHL G3 5件反映 (BUF UPSET BOS / CAR HIT OTT / COL HIT LAK / DAL HIT MIN 2OT / PHI HIT PIT). WTA 7件追加反映 (Bondar UPSET / Cristian HIT / Wang HIT RET / Shnaider HIT / Kalinina HIT indirect / Li HIT / Jovic HIT). SL 2件 (York HIT / Leigh HIT).",
        "data_quality_issues": "CE019 (Mertens date 4/23→4/24) / CE020 (Bencic opponent Martincova→Marcinko) / CE021 (PHI G3 date 4/26→4/23) / CE022 (DAL G3 date 4/26→4/23) 4件訂正.",
        "pending_4_24_night": "Sinner/Shelton/de Minaur/Rublev/Fils/Fonseca/Rinderknech + TBL-MTL G3 / VGK-UTA G3 / EDM-ANA G3 / Mertens-Eala / Gauff / Rybakina 未完結 → 次セッション確認",
        "key_metrics": f"GO bet: {tot_hits}/{tot_conf} ({tot_hit_rate*100:.1f}%) {tot_pnl:+.3f}u / pending {tot_pending} / total GO {tot_go}",
    },
}

with open(ds_path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Dashboard stats regenerated.")
print(f"Overview: GO {tot_hits}/{tot_conf} ({(tot_hit_rate or 0)*100:.1f}%) PnL {tot_pnl:+.3f}u / pending {tot_pending} / total_go {tot_go}")
for sport, s in stats.items():
    print(f"  {sport:12s}: {s}")
