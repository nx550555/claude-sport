"""
ダッシュボード自動生成スクリプト
使用方法: python generate_dashboard.py
全 records/*.json と core/rules_log.json を読み込み dashboard.html を生成する
"""
import json, os
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
RECORDS_DIR = BASE / "records"
CORE_DIR    = BASE / "core"
OUT_HTML    = BASE / "dashboard.html"

# ──────────────────────────────────────────
# データ読み込み
# ──────────────────────────────────────────

def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  [WARN] 読み込み失敗: {path} ({e})")
        return None

def all_picks_from_tennis(data):
    """テニスのトーナメント形式 → 統一フォーマット"""
    picks = []
    tournament = data.get("tournament", "")
    rule_ver   = data.get("rule_version", "")
    dates      = data.get("dates", "")
    start_date = dates.split(" ")[0] if dates else ""
    for rnd, rdata in data.get("rounds", {}).items():
        date = rdata.get("date", start_date)
        for p in rdata.get("predictions", []):
            picks.append({
                "sport": "Tennis",
                "date": date,
                "event": tournament,
                "round": rnd,
                "match": p.get("match", ""),
                "tier": p.get("tier", "skip"),
                "rec": p.get("rec", "—"),
                "rec_odds": p.get("rec_odds", p.get("rec_odds_est")),
                "ev": p.get("ev", p.get("ev_est")),
                "confidence": p.get("confidence"),
                "result": p.get("result"),
                "hit": p.get("hit"),
                "actual_ev": p.get("actual_ev"),
                "score": p.get("score"),
                "note": p.get("note", ""),
                "rule_version": rule_ver,
            })
    return picks

def all_picks_from_sport(data):
    """NHL/NRL/UFL 形式 → 統一フォーマット"""
    picks = []
    sport   = (data.get("sport") or "").upper()
    season  = data.get("season", "")
    rv      = data.get("rule_version", "")
    for g in data.get("games", []):
        picks.append({
            "sport": sport,
            "date": g.get("date", ""),
            "event": f"{sport} {season}",
            "round": f"Round {g.get('round', g.get('week', ''))}" if g.get("round") or g.get("week") else "",
            "match": g.get("match", ""),
            "tier": g.get("tier", "go"),
            "rec": g.get("rec", "—"),
            "rec_odds": g.get("rec_odds"),
            "ev": g.get("ev"),
            "confidence": g.get("confidence"),
            "result": g.get("result"),
            "hit": g.get("hit"),
            "actual_ev": g.get("actual_ev"),
            "score": g.get("score"),
            "note": g.get("note", ""),
            "rule_version": rv,
        })
    return picks

def load_all_picks():
    picks = []
    for path in sorted(RECORDS_DIR.rglob("*.json")):
        d = load(path)
        if not d:
            continue
        if "rounds" in d:
            picks += all_picks_from_tennis(d)
        elif "games" in d:
            picks += all_picks_from_sport(d)
    picks.sort(key=lambda x: x["date"] or "")
    return picks

def load_rules_log():
    d = load(CORE_DIR / "rules_log.json")
    return d.get("log", []) if d else []

# ──────────────────────────────────────────
# 統計計算
# ──────────────────────────────────────────

def calc_stats(picks):
    """全pickから集計"""
    go_picks = [p for p in picks if p["tier"] in ("go",)]
    done     = [p for p in go_picks if p["hit"] is not None]
    hits     = [p for p in done if p["hit"]]
    ev_vals  = [p["actual_ev"] for p in done if p["actual_ev"] is not None]

    total   = len(go_picks)
    settled = len(done)
    hit_n   = len(hits)
    rate    = hit_n / settled if settled > 0 else None
    ev_sum  = sum(ev_vals) if ev_vals else None

    by_sport = {}
    sports = sorted(set(p["sport"] for p in go_picks))
    for sp in sports:
        sp_picks   = [p for p in go_picks if p["sport"] == sp]
        sp_done    = [p for p in sp_picks if p["hit"] is not None]
        sp_hits    = [p for p in sp_done if p["hit"]]
        sp_ev      = [p["actual_ev"] for p in sp_done if p["actual_ev"] is not None]
        sp_pending = [p for p in sp_picks if p["hit"] is None]
        by_sport[sp] = {
            "total": len(sp_picks),
            "settled": len(sp_done),
            "hits": len(sp_hits),
            "rate": len(sp_hits)/len(sp_done) if sp_done else None,
            "ev_sum": sum(sp_ev) if sp_ev else None,
            "pending": len(sp_pending),
            "rule_version": sp_picks[-1]["rule_version"] if sp_picks else "",
        }

    # 時系列ヒット率（GO確定順）
    timeline = []
    cum_hit = 0
    for i, p in enumerate([x for x in go_picks if x["hit"] is not None], 1):
        if p["hit"]:
            cum_hit += 1
        timeline.append({
            "n": i,
            "date": p["date"],
            "sport": p["sport"],
            "match": p["match"],
            "hit": p["hit"],
            "cum_rate": round(cum_hit / i * 100, 1),
            "actual_ev": p["actual_ev"],
        })

    return {
        "total": total, "settled": settled, "hits": hit_n,
        "rate": rate, "ev_sum": ev_sum,
        "by_sport": by_sport,
        "timeline": timeline,
    }

# ──────────────────────────────────────────
# HTML 生成
# ──────────────────────────────────────────

SPORT_COLOR = {
    "Tennis": "#79c0ff",
    "NHL":    "#a5f3fc",
    "NRL":    "#86efac",
    "UFL":    "#fca5a5",
}
SPORT_EMOJI = {
    "Tennis": "🎾",
    "NHL":    "🏒",
    "NRL":    "🏉",
    "UFL":    "🏈",
}

def pct(v):
    if v is None: return "-"
    return f"{v*100:.1f}%"

def ev_str(v):
    if v is None: return "-"
    return f"+{v:.3f}" if v >= 0 else f"{v:.3f}"

def ev_pct(v):
    if v is None: return "-"
    return f"+{v:.1f}%" if v >= 0 else f"{v:.1f}%"

def odds_str(v):
    if v is None: return "-"
    return f"{v:.2f}"

def hit_badge(hit):
    if hit is True:  return '<span class="badge badge-hit">✓ HIT</span>'
    if hit is False: return '<span class="badge badge-miss">✗ MISS</span>'
    return '<span class="badge badge-pending">⏳ 待機中</span>'

def tier_badge(tier):
    if tier == "go":         return '<span class="badge badge-go">GO</span>'
    if tier == "caution":    return '<span class="badge badge-warn">CAUTION</span>'
    if tier == "borderline": return '<span class="badge badge-warn">BORDER</span>'
    return '<span class="badge badge-skip">SKIP</span>'

def sport_tag(sp):
    color = SPORT_COLOR.get(sp, "#8b949e")
    emoji = SPORT_EMOJI.get(sp, "🏆")
    return f'<span class="sport-tag" style="color:{color};">{emoji} {sp}</span>'

def render_overview(stats):
    r = stats["rate"]
    evs = stats["ev_sum"]
    rate_color = "#3fb950" if r and r >= 0.6 else ("#e3b341" if r and r >= 0.4 else "#f85149")
    ev_color   = "#3fb950" if evs and evs > 0 else "#f85149"

    cards = ""
    for sp, s in stats["by_sport"].items():
        r2 = s["rate"]
        rc = "#3fb950" if r2 and r2 >= 0.6 else ("#e3b341" if r2 and r2 >= 0.4 else ("#f85149" if r2 is not None else "#8b949e"))
        evv = s["ev_sum"]
        evc = "#3fb950" if evv and evv > 0 else ("#f85149" if evv is not None else "#8b949e")
        color = SPORT_COLOR.get(sp, "#8b949e")
        emoji = SPORT_EMOJI.get(sp, "🏆")
        cards += f"""
        <div class="sport-card">
          <div class="sport-card-header" style="color:{color};">{emoji} {sp} <span class="rule-ver">{s['rule_version']}</span></div>
          <div class="sport-metrics">
            <div class="sm"><div class="sm-label">GO回数</div><div class="sm-val">{s['total']}</div></div>
            <div class="sm"><div class="sm-label">結果済</div><div class="sm-val">{s['settled']}</div></div>
            <div class="sm"><div class="sm-label">的中</div><div class="sm-val">{s['hits']}</div></div>
            <div class="sm"><div class="sm-label">正答率</div><div class="sm-val" style="color:{rc};">{pct(s['rate']) if s['rate'] is not None else ('—' if not s['settled'] else '0.0%')}</div></div>
            <div class="sm"><div class="sm-label">累積EV</div><div class="sm-val" style="color:{evc};">{ev_str(evv)}</div></div>
            <div class="sm"><div class="sm-label">待機中</div><div class="sm-val" style="color:#e3b341;">{s['pending']}</div></div>
          </div>
        </div>"""

    return f"""
    <div class="section">
      <div class="overview-top">
        <div class="big-stat">
          <div class="bs-label">総GO回数</div>
          <div class="bs-val">{stats['total']}</div>
          <div class="bs-sub">結果確定: {stats['settled']}件</div>
        </div>
        <div class="big-stat">
          <div class="bs-label">通算正答率</div>
          <div class="bs-val" style="color:{rate_color};">{pct(r) if r is not None else ('—' if not stats['settled'] else '0.0%')}</div>
          <div class="bs-sub">{stats['hits']}HIT / {stats['settled']}試合</div>
        </div>
        <div class="big-stat">
          <div class="bs-label">累積EV合計</div>
          <div class="bs-val" style="color:{ev_color};">{ev_str(evs)}</div>
          <div class="bs-sub">単位: 賭け金1あたり</div>
        </div>
      </div>
      <div class="sport-cards">{cards}</div>
    </div>"""

def render_active(picks):
    active = [p for p in picks if p["tier"] == "go" and p["hit"] is None]
    if not active:
        return '<div class="section"><p style="color:#8b949e;">現在アクティブな推奨はありません</p></div>'
    rows = ""
    for p in active:
        color = SPORT_COLOR.get(p["sport"], "#8b949e")
        rows += f"""
        <div class="active-card" style="border-color:{color}30;background:linear-gradient(135deg,{color}08,transparent);">
          <div class="ac-sport">{SPORT_EMOJI.get(p['sport'],'🏆')} {p['sport']} {p.get('round','')}</div>
          <div class="ac-match">{p['match']}</div>
          <div class="ac-rec">推奨: <strong style="color:#e3b341;">{p['rec']}</strong></div>
          <div class="ac-metrics">
            <div class="acm"><div class="acm-l">オッズ</div><div class="acm-v odds">{odds_str(p['rec_odds'])}</div></div>
            <div class="acm"><div class="acm-l">予測EV</div><div class="acm-v ev">{ev_pct(p['ev'])}</div></div>
            <div class="acm"><div class="acm-l">確信度</div><div class="acm-v">{f"{p['confidence']:.1f}%" if p['confidence'] else '—'}</div></div>
            <div class="acm"><div class="acm-l">ルール</div><div class="acm-v rule">{p['rule_version']}</div></div>
          </div>
          <div class="ac-note">{p['note'][:120] + '…' if len(p.get('note','')) > 120 else p.get('note','')}</div>
          <div class="ac-date">📅 {p['date']}</div>
        </div>"""
    return f'<div class="section"><div class="active-grid">{rows}</div></div>'

def render_history(picks):
    go_picks = [p for p in picks if p["tier"] in ("go", "caution", "borderline")]
    rows = ""
    for p in reversed(go_picks):
        ev_c = "ev-pos" if p["ev"] and p["ev"] > 0 else "ev-neg"
        aev_c = "ev-pos" if p.get("actual_ev") and p["actual_ev"] > 0 else "ev-neg"
        rows += f"""
        <tr>
          <td>{p['date']}</td>
          <td>{sport_tag(p['sport'])}</td>
          <td style="font-size:12px;">{p['event']} {p['round']}</td>
          <td class="match-cell">{p['match']}</td>
          <td>{tier_badge(p['tier'])}</td>
          <td style="color:#e3b341;font-weight:600;">{p['rec']}</td>
          <td style="color:#e3b341;">{odds_str(p['rec_odds'])}</td>
          <td class="{ev_c}">{ev_pct(p['ev'])}</td>
          <td>{f"{p['confidence']:.0f}%" if p['confidence'] else '—'}</td>
          <td>{hit_badge(p['hit'])}</td>
          <td style="font-size:12px;color:#8b949e;">{p.get('score','—') or '—'}</td>
          <td class="{aev_c}">{ev_str(p.get('actual_ev'))}</td>
        </tr>"""
    return f"""
    <div class="section">
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>日付</th><th>スポーツ</th><th>大会/ラウンド</th><th>試合</th>
              <th>Tier</th><th>推奨</th><th>オッズ</th><th>予測EV</th>
              <th>確信度</th><th>結果</th><th>スコア</th><th>実績EV</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>"""

def render_timeline(stats):
    tl = stats["timeline"]
    if not tl:
        return '<p style="color:#8b949e;padding:16px;">まだ確定した試合がありません</p>'
    rows = ""
    for t in tl:
        rc = "#3fb950" if t["cum_rate"] >= 60 else ("#e3b341" if t["cum_rate"] >= 40 else "#f85149")
        hc = "#3fb950" if t["hit"] else "#f85149"
        ev_c = "ev-pos" if t.get("actual_ev") and t["actual_ev"] > 0 else "ev-neg"
        rows += f"""
        <tr>
          <td>#{t['n']}</td>
          <td>{t['date']}</td>
          <td>{sport_tag(t['sport'])}</td>
          <td style="font-size:12px;">{t['match']}</td>
          <td style="color:{hc};font-weight:700;">{'✓ HIT' if t['hit'] else '✗ MISS'}</td>
          <td class="{ev_c}">{ev_str(t.get('actual_ev'))}</td>
          <td style="color:{rc};font-weight:700;">{t['cum_rate']}%</td>
        </tr>"""
    return f"""
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr><th>#</th><th>日付</th><th>スポーツ</th><th>試合</th><th>結果</th><th>実績EV</th><th>累積正答率</th></tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>"""

def render_rules_log(log):
    rows = ""
    for entry in reversed(log):
        sp = entry.get("sport", "")
        color = SPORT_COLOR.get(sp.capitalize(), "#8b949e")
        emoji = SPORT_EMOJI.get(sp.capitalize(), "📋")
        changes_html = "".join(f"<li>{c}</li>" for c in entry.get("changes", []))
        before = entry.get("result_before", "—")
        after  = entry.get("result_after", "—")
        trigger = entry.get("trigger", "")
        note   = entry.get("note", "")
        rows += f"""
        <div class="rule-entry">
          <div class="rule-header">
            <span style="color:{color};">{emoji} {sp.upper()}</span>
            <span class="rule-ver-badge">{entry.get('version_from','—')} → <strong>{entry.get('version_to','')}</strong></span>
            <span class="rule-date">{entry.get('date','')}</span>
          </div>
          <div class="rule-trigger">📌 トリガー: {trigger}</div>
          <ul class="rule-changes">{changes_html}</ul>
          <div class="rule-result">
            変更前: <span style="color:#f85149;">{before}</span> &nbsp;→&nbsp;
            変更後: <span style="color:#3fb950;">{after}</span>
          </div>
          {f'<div class="rule-note">💡 {note}</div>' if note else ''}
        </div>"""
    return f'<div class="section"><div class="rules-list">{rows}</div></div>'

# ──────────────────────────────────────────
# CSS / HTML テンプレート
# ──────────────────────────────────────────

CSS = """
:root {
  --bg:#0d1117; --surface:#161b22; --surface2:#21262d; --border:#30363d;
  --text:#e6edf3; --text2:#8b949e;
  --go:#238636; --go-l:#2ea043; --go-bg:#0f2c1a;
  --warn:#d29922; --warn-bg:#2d2100;
  --miss:#f85149;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:14px;}
a{color:inherit;text-decoration:none;}

/* ヘッダー */
.hdr{background:var(--surface);border-bottom:1px solid var(--border);padding:14px 24px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:100;}
.hdr h1{font-size:17px;font-weight:700;}
.hdr-right{display:flex;gap:10px;align-items:center;font-size:12px;color:var(--text2);}

/* タブ */
.tabs{display:flex;gap:0;border-bottom:1px solid var(--border);background:var(--surface);padding:0 24px;}
.tab{padding:10px 18px;font-size:13px;font-weight:500;cursor:pointer;border-bottom:2px solid transparent;color:var(--text2);transition:.15s;}
.tab.active{color:var(--text);border-bottom-color:#58a6ff;}
.tab:hover{color:var(--text);}
.tab-content{display:none;padding:20px 24px;max-width:1280px;margin:0 auto;}
.tab-content.active{display:block;}

/* セクション */
.section{margin-bottom:28px;}
.section-title{font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:var(--text2);margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid var(--border);}

/* 概要 */
.overview-top{display:flex;gap:16px;margin-bottom:20px;flex-wrap:wrap;}
.big-stat{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px 20px;flex:1;min-width:160px;text-align:center;}
.bs-label{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--text2);margin-bottom:6px;}
.bs-val{font-size:32px;font-weight:700;line-height:1;}
.bs-sub{font-size:11px;color:var(--text2);margin-top:4px;}

.sport-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;}
.sport-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px 16px;}
.sport-card-header{font-size:13px;font-weight:700;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;}
.rule-ver{font-size:10px;font-weight:400;color:var(--text2);background:var(--surface2);padding:1px 6px;border-radius:4px;}
.sport-metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;}
.sm{text-align:center;}
.sm-label{font-size:10px;color:var(--text2);text-transform:uppercase;}
.sm-val{font-size:18px;font-weight:700;}

/* アクティブ */
.active-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;}
.active-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px;}
.ac-sport{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--text2);margin-bottom:6px;}
.ac-match{font-size:13px;color:var(--text2);margin-bottom:4px;}
.ac-rec{font-size:15px;font-weight:600;margin-bottom:10px;}
.ac-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:10px;}
.acm{text-align:center;background:var(--surface2);border-radius:6px;padding:6px 4px;}
.acm-l{font-size:9px;color:var(--text2);text-transform:uppercase;}
.acm-v{font-size:14px;font-weight:600;}
.acm-v.odds{color:#e3b341;} .acm-v.ev{color:#3fb950;} .acm-v.rule{font-size:11px;color:#8b949e;}
.ac-note{font-size:11px;color:var(--text2);line-height:1.5;margin-bottom:8px;}
.ac-date{font-size:11px;color:var(--text2);}

/* バッジ */
.badge{display:inline-block;font-size:10px;font-weight:700;padding:2px 7px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;}
.badge-hit{background:#0f2c1a;color:#3fb950;border:1px solid var(--go);}
.badge-miss{background:#2d1014;color:#f85149;border:1px solid var(--miss);}
.badge-pending{background:var(--warn-bg);color:var(--warn);border:1px solid var(--warn);}
.badge-go{background:var(--go-bg);color:var(--go-l);border:1px solid var(--go);}
.badge-warn{background:var(--warn-bg);color:var(--warn);border:1px solid var(--warn);}
.badge-skip{background:var(--surface2);color:var(--text2);border:1px solid var(--border);}
.sport-tag{font-size:12px;font-weight:600;}

/* テーブル */
.table-wrap{overflow-x:auto;}
.data-table{width:100%;border-collapse:collapse;font-size:12px;}
.data-table th{text-align:left;font-size:10px;text-transform:uppercase;letter-spacing:.04em;color:var(--text2);padding:7px 10px;border-bottom:1px solid var(--border);font-weight:500;white-space:nowrap;}
.data-table td{padding:9px 10px;border-bottom:1px solid rgba(48,54,61,.5);vertical-align:middle;}
.data-table tr:hover td{background:rgba(255,255,255,.02);}
.data-table tr:last-child td{border-bottom:none;}
.match-cell{max-width:220px;font-size:12px;}
.ev-pos{color:#3fb950;font-weight:600;}
.ev-neg{color:#f85149;font-weight:600;}

/* ルールログ */
.rules-list{display:flex;flex-direction:column;gap:14px;}
.rule-entry{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;}
.rule-header{display:flex;align-items:center;gap:12px;margin-bottom:8px;font-weight:600;}
.rule-ver-badge{font-size:12px;background:var(--surface2);border:1px solid var(--border);padding:2px 8px;border-radius:4px;}
.rule-date{font-size:11px;color:var(--text2);margin-left:auto;}
.rule-trigger{font-size:12px;color:var(--warn);margin-bottom:8px;}
.rule-changes{padding-left:20px;font-size:12px;line-height:1.8;color:var(--text2);}
.rule-changes li{margin-bottom:2px;}
.rule-result{font-size:12px;margin-top:8px;padding-top:8px;border-top:1px solid var(--border);}
.rule-note{font-size:11px;color:var(--text2);margin-top:6px;font-style:italic;}

/* フッター */
.footer{text-align:center;padding:16px;color:var(--text2);font-size:11px;border-top:1px solid var(--border);margin-top:24px;}

@media(max-width:600px){
  .overview-top{flex-direction:column;}
  .sport-metrics{grid-template-columns:repeat(2,1fr);}
  .ac-metrics{grid-template-columns:repeat(2,1fr);}
  .tabs{overflow-x:auto;padding:0 12px;}
}
"""

JS = """
function showTab(id) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  document.getElementById('content-' + id).classList.add('active');
}
"""

def build_html(stats, active_html, history_html, timeline_html, rules_html, updated):
    overview_html = render_overview(stats)
    pending = stats["total"] - stats["settled"]
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sports Betting Dashboard</title>
<style>{CSS}</style>
</head>
<body>

<div class="hdr">
  <h1>⚡ Sports Betting Dashboard</h1>
  <div class="hdr-right">
    <span>GO {stats['total']}件 / 確定 {stats['settled']}件 / 待機 {pending}件</span>
    <span style="background:#21262d;border:1px solid #30363d;border-radius:6px;padding:3px 8px;">
      更新: {updated}
    </span>
  </div>
</div>

<div class="tabs">
  <div class="tab active" id="tab-overview" onclick="showTab('overview')">📊 概要</div>
  <div class="tab" id="tab-active"   onclick="showTab('active')">✅ アクティブ推奨</div>
  <div class="tab" id="tab-history"  onclick="showTab('history')">📋 全履歴</div>
  <div class="tab" id="tab-timeline" onclick="showTab('timeline')">📈 正答率推移</div>
  <div class="tab" id="tab-rules"    onclick="showTab('rules')">⚙️ ルール変更履歴</div>
</div>

<div class="tab-content active" id="content-overview">
  <div class="section-title">総合パフォーマンス</div>
  {overview_html}
</div>

<div class="tab-content" id="content-active">
  <div class="section-title">アクティブ GO 推奨 — 結果待ち</div>
  {active_html}
</div>

<div class="tab-content" id="content-history">
  <div class="section-title">全GO/CAUTION/BORDER 推奨履歴</div>
  {history_html}
</div>

<div class="tab-content" id="content-timeline">
  <div class="section-title">正答率・EV 推移 (GO確定試合)</div>
  {timeline_html}
</div>

<div class="tab-content" id="content-rules">
  <div class="section-title">ルール変更履歴 — 予測→結果→修正のサイクル</div>
  {rules_html}
</div>

<div class="footer">
  Sports Betting Dashboard &nbsp;|&nbsp;
  Tennis v2.0 / NHL v1.2 / NRL v1.0 / UFL v1.0 &nbsp;|&nbsp;
  Data: tennisabstract · MoneyPuck · DailyFaceoff · OddsPortal · Rotowire
</div>

<script>{JS}</script>
</body>
</html>"""

# ──────────────────────────────────────────
# メイン
# ──────────────────────────────────────────

def main():
    print("ダッシュボード生成中...")

    picks    = load_all_picks()
    rules_log = load_rules_log()
    stats    = calc_stats(picks)
    updated  = datetime.now().strftime("%Y-%m-%d %H:%M")

    active_html   = render_active(picks)
    history_html  = render_history(picks)
    timeline_html = render_timeline(stats)
    rules_html    = render_rules_log(rules_log)

    html = build_html(stats, active_html, history_html, timeline_html, rules_html, updated)

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] 生成完了: {OUT_HTML}")
    print(f"   総GO: {stats['total']}件 / 確定: {stats['settled']}件 / 正答率: {pct(stats['rate'])}")
    for sp, s in stats['by_sport'].items():
        print(f"   {sp}: {s['hits']}/{s['settled']} = {pct(s['rate'])} (待機: {s['pending']}件)")

if __name__ == "__main__":
    main()
