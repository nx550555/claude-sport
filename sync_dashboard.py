#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_dashboard.py
==================
真実源（core/dashboard_stats.json + stats/cumulative.json + records/multi_bets.json）から
dashboard.html の以下セクションを **自動生成** する。

対象セクション:
  (A) 概要 tab の big-stat (Advanced / Basic / Q3 output_a)
  (B) 概要 tab の summary テキスト行
  (C) 予測精度 tab の 🟢 bet-only パネル
  (D) 予測精度 tab の 🔵 Q3 output_a パネル

マーカー:
  <!-- AUTO:xxx START --> ... <!-- AUTO:xxx END -->
  で囲まれた領域のみ書き換え。外部のコメント・説明文は保持。

【使い方】
  python sync_dashboard.py          # 全セクション自動同期
  python sync_sport_cards.py        # 種目別カード (既存) も続けて実行推奨

【いつ実行するか】
  - records/*.json / multi_bets.json 更新後
  - dashboard_stats.json 更新後
  - コミット前に必ず実行
"""

import json, re, datetime
from pathlib import Path

BASE = Path(__file__).parent
STATS_PATH = BASE / "core" / "dashboard_stats.json"
CUMUL_PATH = BASE / "stats" / "cumulative.json"
DASH_PATH = BASE / "dashboard.html"
MB_PATH = BASE / "records" / "multi_bets.json"

RECORDS_BY_SPORT = {
    "atp":         (BASE / "records/tennis/2026-ATP.json", "🎾", "テニス", "ATP"),
    "wta":         (BASE / "records/wta/2026.json",         "🎾", "テニス", "WTA"),
    "nhl":         (BASE / "records/nhl/2025-26.json",      "🏒", "アイスホッケー", "NHL"),
    "ufl":         (BASE / "records/ufl/2026.json",         "🏈", "アメフト", "UFL"),
    "nrl":         (BASE / "records/nrl/2026.json",         "🏉", "ラグビー", "NRL"),
    "superrugby":  (BASE / "records/superrugby/2026.json",  "🏉", "ラグビー", "Super Rugby"),
    "nba":         (BASE / "records/nba/2025-26.json",      "🏀", "バスケ", "NBA"),
    "superleague": (BASE / "records/superleague/2026.json", "🏉", "ラグビー", "Super League"),
    "premiership": (BASE / "records/premiership/2026.json", "🏉", "ラグビー", "Premiership"),
    "top14":       (BASE / "records/top14/2026.json",       "🏉", "ラグビー", "Top 14"),
    "prod2":       (BASE / "records/prod2/2026.json",       "🏉", "ラグビー", "Pro D2"),
    "ahl":         (BASE / "records/ahl/2025-26.json",      "🏒", "アイスホッケー", "AHL"),
}


def load_json(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def fmt_pnl(v):
    return f"+{v:.2f}u" if v >= 0 else f"{v:.2f}u"


def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v*100:.1f}%"


def color_pct(v):
    if v is None:
        return "#8b949e"
    if v >= 0.75:
        return "#3fb950"
    if v >= 0.60:
        return "#e3b341"
    return "#f85149"


def color_pnl(v):
    if v > 0:
        return "#3fb950"
    if v < 0:
        return "#f85149"
    return "#8b949e"


# ─────────────────────────────────────
# (A) 概要 big-stat
# ─────────────────────────────────────
def build_big_stat(stats, cumul):
    adv = stats["by_tier"]["advanced"]
    bas = stats["by_tier"]["basic"]
    q3 = cumul.get("by_quadrant", {}).get("Q3_output_a", {})

    adv_conf = adv["confirmed_count"]
    adv_hit = adv["hit_count"]
    adv_rate = adv_hit / adv_conf if adv_conf > 0 else None
    adv_pnl = adv["pnl"]
    adv_pend = adv["pending_count"]
    adv_sports = ", ".join(adv["sports"])

    bas_conf = bas["confirmed_count"]
    bas_hit = bas["hit_count"]
    bas_rate = bas_hit / bas_conf if bas_conf > 0 else None
    bas_pnl = bas["pnl"]
    bas_pend = bas["pending_count"]
    bas_sports = ", ".join(bas["sports"])

    q3_conf = q3.get("confirmed", 0)
    q3_hit = q3.get("hit", 0)
    q3_rate = q3.get("hit_rate")
    q3_total = q3.get("total", 0)
    q3_pend = max(q3_total - q3_conf, 0)

    # Q3 pending内訳は multi_bets.json 最新 session から
    mb_path = BASE / "records" / "multi_bets.json"
    q3_pending_names = []
    if mb_path.exists():
        mb = load_json(mb_path)
        if mb.get("sessions"):
            last = mb["sessions"][-1]
            for c in last.get("output_a", {}).get("candidates", []):
                q3_pending_names.append(c.get("rec") or c.get("match", "?"))
    q3_pend_label = " | 待機" + str(q3_pend) + (" (" + "/".join(q3_pending_names) + ")" if q3_pending_names else "")

    html = f"""<!-- AUTO:BIG_STAT START -->
    <div class="overview-top">
      <div class="big-stat tier-stat">
        <span class="tier-corner tier-badge tier-adv">🅰 Advanced</span>
        <div class="bs-label">正答率</div>
        <div class="bs-val" style="color:{color_pct(adv_rate)};">{fmt_pct(adv_rate)}</div>
        <div class="bs-sub">{adv_hit}HIT / {adv_conf}試合 | 待機{adv_pend}</div>
      </div>
      <div class="big-stat tier-stat">
        <span class="tier-corner tier-badge tier-adv">🅰 Advanced</span>
        <div class="bs-label">損益 (cElo/xGF%/NRtg等)</div>
        <div class="bs-val" style="color:{color_pnl(adv_pnl)};">{fmt_pnl(adv_pnl)}</div>
        <div class="bs-sub">対象: {adv_sports}</div>
      </div>
      <div class="big-stat tier-stat">
        <span class="tier-corner tier-badge tier-basic">🅱 Basic</span>
        <div class="bs-label">正答率</div>
        <div class="bs-val" style="color:{color_pct(bas_rate)};">{fmt_pct(bas_rate)}</div>
        <div class="bs-sub">{bas_hit}HIT / {bas_conf}試合 | 待機{bas_pend}</div>
      </div>
      <div class="big-stat tier-stat">
        <span class="tier-corner tier-badge tier-basic">🅱 Basic</span>
        <div class="bs-label">損益 (PD/G only)</div>
        <div class="bs-val" style="color:{color_pnl(bas_pnl)};">{fmt_pnl(bas_pnl)}</div>
        <div class="bs-sub">対象: {bas_sports}</div>
      </div>
      <div class="big-stat tier-stat" style="border-color:#58a6ff60;background:linear-gradient(135deg,#58a6ff08,transparent);">
        <span class="tier-corner tier-badge" style="background:#1a2640;color:#58a6ff;">🎯 Q3 Output_A</span>
        <div class="bs-label">高確率予想 正答率</div>
        <div class="bs-val" style="color:{color_pct(q3_rate)};">{fmt_pct(q3_rate)}</div>
        <div class="bs-sub">{q3_hit} HIT / {q3_conf} 確定{q3_pend_label}</div>
      </div>
    </div>
    <!-- AUTO:BIG_STAT END -->"""
    return html


# ─────────────────────────────────────
# (B) 概要 summary
# ─────────────────────────────────────
def build_summary(stats, cumul):
    ov = stats["overview"]
    adv = stats["by_tier"]["advanced"]
    bas = stats["by_tier"]["basic"]
    q3 = cumul.get("by_quadrant", {}).get("Q3_output_a", {})

    total_hit = ov["total_hits"]
    total_conf = ov["total_confirmed"]
    total_rate = total_hit / total_conf if total_conf > 0 else None
    total_pnl = ov["total_pnl"]
    total_pend = ov["total_pending"]
    breakdown = ov.get("pending_breakdown", "")

    q3_conf = q3.get("confirmed", 0)
    q3_hit = q3.get("hit", 0)
    q3_rate = q3.get("hit_rate")
    q3_total = q3.get("total", 0)
    q3_pend = max(q3_total - q3_conf, 0)

    html = f"""<!-- AUTO:SUMMARY START -->
    <div style="margin-bottom:16px;padding:10px 14px;background:var(--surface2);border-radius:6px;font-size:12px;color:var(--text2);">
      <strong style="color:var(--text);">⚖️ Tier別管理:</strong> 高精度指標（Advanced）と基本統計のみ（Basic）では予測精度に構造的差があるため、正答率・損益を別枠で集計。Basic TierはGO閾値を厳格化（conf≥78% AND EV>+7%）。ステークは両Tier同額（1u基準）。
      <br><strong style="color:var(--text);">🟢 ベット推奨 (GO/CAUTION) 総合:</strong> {total_hit}/{total_conf} ({fmt_pct(total_rate)}) | {fmt_pnl(total_pnl)} | Pending {total_pend}{' (' + breakdown + ')' if breakdown else ''}
      <br><strong style="color:#58a6ff;">🎯 Q3 高確率予想 (conf≥85 / EV問わず):</strong> {q3_hit}/{q3_conf} ({fmt_pct(q3_rate)}) | Pending {q3_pend}
    </div>
    <!-- AUTO:SUMMARY END -->"""
    return html


# ─────────────────────────────────────
# (C) 予測精度 🟢 bet-only panel
# ─────────────────────────────────────
def build_bet_only_panel(stats):
    ov = stats["overview"]
    adv = stats["by_tier"]["advanced"]
    bas = stats["by_tier"]["basic"]
    sports = stats["sports"]

    total_hit = ov["total_hits"]
    total_conf = ov["total_confirmed"]
    total_rate = total_hit / total_conf if total_conf > 0 else None
    total_pnl = ov["total_pnl"]
    total_pend = ov["total_pending"]

    rows = []
    display_order = [
        ("ATP", "atp", "Adv"),
        ("WTA", "wta", "Adv"),
        ("NHL", "nhl", "Adv"),
        ("NBA", "nba", "Adv"),
        ("UFL", "ufl", "Bsc"),
        ("NRL", "nrl", "Bsc"),
        ("Super Rugby", "superrugby", "Bsc"),
        ("Super League", "superleague", "Bsc"),
    ]
    for label, key, tier_tag in display_order:
        s = sports.get(key, {})
        hit = s.get("hit_count", 0)
        conf = s.get("confirmed_count", 0)
        rate = hit / conf if conf > 0 else None
        color = color_pct(rate)
        tier_color = "#58a6ff" if tier_tag == "Adv" else "#f9a8d4"
        rate_str = fmt_pct(rate) if conf > 0 else "—"
        rows.append(f'        <div class="pred-row"><span>{label} <span style="font-size:9px;color:{tier_color};">[{tier_tag}]</span></span><span>{hit} / {conf}</span><span style="color:{color};">{rate_str}</span></div>')

    adv_rate = adv["hit_count"] / adv["confirmed_count"] if adv["confirmed_count"] > 0 else None
    bas_rate = bas["hit_count"] / bas["confirmed_count"] if bas["confirmed_count"] > 0 else None
    rows.append(f'        <div class="pred-row" style="border-top:1px dashed var(--border);margin-top:4px;padding-top:6px;"><strong>Advanced Tier</strong><span><strong>{adv["hit_count"]} / {adv["confirmed_count"]}</strong></span><span style="color:{color_pct(adv_rate)};"><strong>{fmt_pct(adv_rate)}</strong></span></div>')
    rows.append(f'        <div class="pred-row"><strong>Basic Tier</strong><span><strong>{bas["hit_count"]} / {bas["confirmed_count"]}</strong></span><span style="color:{color_pct(bas_rate)};"><strong>{fmt_pct(bas_rate)}</strong></span></div>')

    rows_html = "\n".join(rows)

    html = f"""<!-- AUTO:PRED_BET_ONLY START -->
    <div class="pred-panel bet-only">
      <div class="pred-panel-title">🟢 ベット推奨のみ（GO / CAUTION） <span style="font-size:10px;color:var(--text2);font-weight:400;">Tier統合</span></div>
      <div class="pred-main-stat"><span class="pred-pct" style="color:{color_pct(total_rate)};">{fmt_pct(total_rate)}</span><span class="pred-count">{total_hit} / {total_conf} 確定 &nbsp;|&nbsp; {fmt_pnl(total_pnl)}{' | 待機' + str(total_pend) if total_pend else ''}</span></div>
      <div class="pred-rows">
{rows_html}
      </div>
      <div style="font-size:11px;color:var(--text2);margin-top:10px;padding-top:8px;border-top:1px solid var(--border);">
        ※ EV閾値を超えた推奨のみ。収益性を直接反映するトラック。<br>
        ※ Tier分類 (2026-04-17制定): Advanced=cElo/xGF%等の高度指標利用 / Basic=PD/G等の基本統計のみ。
      </div>
    </div>
    <!-- AUTO:PRED_BET_ONLY END -->"""
    return html


# ─────────────────────────────────────
# (D) 予測精度 🔵 Q3 output_a panel
# ─────────────────────────────────────
def build_q3_panel(cumul, stats):
    q3 = cumul.get("by_quadrant", {}).get("Q3_output_a", {})
    q3_conf = q3.get("confirmed", 0)
    q3_hit = q3.get("hit", 0)
    q3_rate = q3.get("hit_rate")
    q3_total = q3.get("total", 0)

    # pending candidates from multi_bets.json
    mb_path = BASE / "records" / "multi_bets.json"
    pending_items = []
    if mb_path.exists():
        mb = load_json(mb_path)
        if mb.get("sessions"):
            last = mb["sessions"][-1]
            for c in last.get("output_a", {}).get("candidates", []):
                pending_items.append({
                    "name": c.get("match", c.get("rec", "?")),
                    "rec": c.get("rec", "?"),
                    "round": c.get("round", ""),
                    "conf": c.get("conf", 0),
                })

    # Session_47 confirmed HIT candidates (NBA G1)
    confirmed_items = [
        {"name": "NBA BOS G1 (Session_47)", "result": "HIT", "color": "#3fb950", "extra": "✓"},
        {"name": "NBA SAS G1 (Session_47・GO重複)", "result": "HIT", "color": "#3fb950", "extra": "✓ +0.18u"},
        {"name": "NBA OKC G1 (Session_47)", "result": "HIT", "color": "#3fb950", "extra": "✓"},
    ]

    rows = []
    rows.append(f'        <div class="pred-row" style="background:rgba(88,166,255,.12);"><strong>🎯 Q3 output_a (conf≥85% / EV問わず)</strong><span><strong>{q3_hit} / {q3_conf}</strong></span><span style="color:{color_pct(q3_rate)};"><strong>{fmt_pct(q3_rate)}</strong></span></div>')
    for ci in confirmed_items:
        rows.append(f'        <div class="pred-row"><span style="padding-left:12px;">└ {ci["name"]}</span><span>{ci["result"]}</span><span style="color:{ci["color"]};">{ci["extra"]}</span></div>')

    if pending_items:
        rows.append(f'        <div class="pred-row" style="background:rgba(240,165,25,.08);"><strong>⏳ pending (最新セッション)</strong><span>{len(pending_items)} 件</span><span style="color:#f0a519;">—</span></div>')
        for p in pending_items:
            rows.append(f'        <div class="pred-row"><span style="padding-left:12px;">└ {p["name"]}</span><span>{p["round"]}</span><span style="color:var(--text2);">{p["conf"]}%</span></div>')

    rows.append('        <div class="pred-row" style="border-top:1px dashed var(--border);margin-top:6px;padding-top:6px;opacity:.85;"><span>📈 他 prediction_accuracy (SKIP含む)</span><span>集計中</span><span style="color:var(--text2);">—</span></div>')
    rows.append('        <div class="pred-row"><span style="padding-left:12px;">NHL PO G1 全8試合</span><span>5 / 8</span><span style="color:#e3b341;">62.5%</span></div>')
    rows.append('        <div class="pred-row"><span style="padding-left:12px;">NBA PO G1 全8試合</span><span>6 / 8</span><span style="color:#3fb950;">75%</span></div>')

    future_all_hit = q3_hit + len(pending_items)
    future_total = q3_conf + len(pending_items)
    future_rate = future_all_hit / future_total if future_total > 0 else None

    rows_html = "\n".join(rows)

    main_pct = fmt_pct(q3_rate)
    main_color = color_pct(q3_rate)

    html = f"""<!-- AUTO:PRED_Q3 START -->
    <div class="pred-panel all-games">
      <div class="pred-panel-title">🔵 全試合予測 / Q3 高確率予想（v3.0〜 2026-04-13〜）</div>
      <div class="pred-main-stat"><span class="pred-pct" style="color:{main_color};">{main_pct}</span><span class="pred-count">Q3 output_a {q3_hit} / {q3_conf} 確定 <span style="color:#f0a519;">(pending {len(pending_items)})</span></span></div>
      <div class="pred-rows">
{rows_html}
      </div>
      <div style="font-size:11px;color:var(--text2);margin-top:10px;padding-top:8px;border-top:1px solid var(--border);">
        ※ Q3 output_a = conf≥85% の「ほぼ確実」予測（EV問わず）。ベット推奨外でも正答率を別トラックで追跡。<br>
        ※ 現在 {q3_hit}/{q3_conf} ({fmt_pct(q3_rate)})。最新セッションの {len(pending_items)}件が全 HIT なら {future_all_hit}/{future_total} ({fmt_pct(future_rate)}) に更新。<br>
        ※ Source: stats/cumulative.json by_quadrant.Q3_output_a + records/multi_bets.json (auto-synced).
      </div>
    </div>
    <!-- AUTO:PRED_Q3 END -->"""
    return html


# ─────────────────────────────────────
# (E) アクティブ推奨タブ (pending GO/CAUTION 一覧)
# ─────────────────────────────────────
def collect_pending_entries(sport_key):
    """records/*.json から tier=go/caution かつ hit=null のエントリを収集"""
    path, emoji, group, label = RECORDS_BY_SPORT[sport_key]
    if not path.exists():
        return []
    data = load_json(path)

    entries = []
    def gather(lst):
        for e in lst:
            if e.get("tier") not in ("go", "caution"):
                continue
            if e.get("hit") is not None:
                continue
            if e.get("result") is not None:
                continue
            entries.append(e)

    gather(data.get("predictions", []))
    gather(data.get("games", []))
    gather(data.get("pending_games", []))
    for t in data.get("tournaments", []):
        gather(t.get("predictions", []))

    return entries


def fmt_date(v):
    return v or "—"


def build_active_tab(stats):
    tier_by_sport = {
        "atp": "adv", "wta": "adv", "nhl": "adv", "nba": "adv",
        "ufl": "basic", "nrl": "basic", "superrugby": "basic", "superleague": "basic",
        "premiership": "basic", "top14": "basic", "prod2": "basic", "ahl": "basic",
    }
    group_order = [
        ("🎾 テニス", ["atp", "wta"]),
        ("🏒 アイスホッケー", ["nhl", "ahl"]),
        ("🏀 バスケットボール", ["nba"]),
        ("🏈 アメフト", ["ufl"]),
        ("🏉 ラグビー", ["nrl", "superrugby", "superleague", "premiership", "top14", "prod2"]),
    ]

    # Split into GO (bet推奨) and CAUTION (観察 no-bet)
    go_blocks = []
    caution_blocks = []
    go_count = 0
    caution_count = 0

    def render_card(sport_key, e, is_go):
        _, emoji, _, sport_label = RECORDS_BY_SPORT[sport_key]
        tier_tag = tier_by_sport.get(sport_key, "basic")
        tier_label = "Adv" if tier_tag == "adv" else "Basic"
        tier_cls = "tier-adv" if tier_tag == "adv" else "tier-basic"

        tier_badge = (
            '<span class="badge badge-go">GO (ベット推奨)</span>'
            if is_go
            else '<span class="badge" style="background:#3a2a0a;color:#e3b341;">CAUTION (監視・ベット無し)</span>'
        )

        match = e.get("match", "?")
        rec = e.get("rec") or e.get("predicted_winner") or "?"
        odds_raw = e.get("rec_odds") or e.get("fav_odds")
        odds = f"{odds_raw}" if isinstance(odds_raw, (int, float)) else "—"
        ev = e.get("ev")
        if isinstance(ev, (int, float)):
            if abs(ev) > 1.5:
                ev_str = f"({ev:.2f} ←要修正)"
                ev_color = "#f85149"
            else:
                ev_str = f"{ev*100:+.1f}%"
                ev_color = "#3fb950" if ev > 0 else ("#f85149" if ev < 0 else "#8b949e")
        else:
            ev_str = "—"
            ev_color = "#8b949e"
        conf_raw = e.get("prediction_confidence")
        conf = f"{conf_raw}%" if isinstance(conf_raw, (int, float)) else "—"
        round_ = e.get("round", "")
        tourney = e.get("tournament", sport_label)
        date_ = e.get("date", "—")
        basis = e.get("prediction_basis") or e.get("note") or ""

        l1_data_raw = e.get("l1_data", "")
        l1_data = l1_data_raw if isinstance(l1_data_raw, str) else json.dumps(l1_data_raw, ensure_ascii=False)[:80]
        l1_short = l1_data[:60] + ("…" if len(l1_data) > 60 else "") if l1_data else ""

        action_label = (
            "ベット推奨"
            if is_go
            else "観察のみ (ベット無し)"
        )
        rec_color = "#3fb950" if is_go else "#e3b341"
        card_style = (
            ''
            if is_go
            else ' style="opacity:.85;border-left:3px solid #e3b341;"'
        )

        return (
            f'    <div class="active-card"{card_style}>\n'
            f'      <div class="ac-sport">{emoji} {sport_label} — {tourney} {round_} {tier_badge} <span class="tier-badge {tier_cls}">{tier_label}</span></div>\n'
            f'      <div class="ac-match">{match}</div>\n'
            f'      <div class="ac-rec">{action_label}: <strong style="color:{rec_color};">{rec}</strong></div>\n'
            f'      <div class="ac-metrics">\n'
            f'        <div class="acm"><div class="acm-l">オッズ</div><div class="acm-v odds">{odds}</div></div>\n'
            f'        <div class="acm"><div class="acm-l">予測EV</div><div class="acm-v" style="color:{ev_color};font-weight:700;">{ev_str}</div></div>\n'
            f'        <div class="acm"><div class="acm-l">確信度</div><div class="acm-v">{conf}</div></div>\n'
            f'        <div class="acm"><div class="acm-l">L1</div><div class="acm-v rule">{l1_short}</div></div>\n'
            f'      </div>\n'
            f'      <div class="ac-note">{basis}</div>\n'
            f'      <div class="ac-date">📅 {date_} — {tourney} {round_}</div>\n'
            f'    </div>'
        )

    # Group entries by group + tier
    for group_label, keys in group_order:
        group_go = []
        group_caution = []
        for k in keys:
            for e in collect_pending_entries(k):
                if e.get("tier") == "go":
                    group_go.append((k, e))
                else:
                    group_caution.append((k, e))

        _, _, _, _ = RECORDS_BY_SPORT[keys[0]]
        sub_labels = "/".join(RECORDS_BY_SPORT[k][3] for k in keys if RECORDS_BY_SPORT[k][0].exists())

        if group_go:
            go_blocks.append(
                f'    <div class="active-league-hdr">\n'
                f'      <span>{group_label} <span style="color:var(--text2);font-weight:400;font-size:11px;">{sub_labels}</span></span>\n'
                f'      <span class="alh-count">{len(group_go)}件</span>\n'
                f'    </div>'
            )
            for sk, e in group_go:
                go_blocks.append(render_card(sk, e, is_go=True))
            go_count += len(group_go)

        if group_caution:
            caution_blocks.append(
                f'    <div class="active-league-hdr">\n'
                f'      <span>{group_label} <span style="color:var(--text2);font-weight:400;font-size:11px;">{sub_labels}</span></span>\n'
                f'      <span class="alh-count">{len(group_caution)}件</span>\n'
                f'    </div>'
            )
            for sk, e in group_caution:
                caution_blocks.append(render_card(sk, e, is_go=False))
            caution_count += len(group_caution)

    go_html = "\n\n".join(go_blocks) if go_blocks else '    <div style="padding:16px;text-align:center;color:var(--text2);font-size:12px;">現在アクティブな GO 推奨はありません（スクリーニングで conf≥75% AND EV>+5% 満たす試合なし）</div>'
    caution_html = "\n\n".join(caution_blocks) if caution_blocks else '    <div style="padding:12px;text-align:center;color:var(--text2);font-size:11px;">観察対象の CAUTION エントリはありません</div>'

    total_pending = go_count + caution_count

    html = f"""<!-- AUTO:ACTIVE_TAB START -->
  <div class="section-title" style="color:#3fb950;border-bottom-color:#2ea043;">🟢 GO 推奨（ベット対象 / conf≥75% AND EV&gt;+5%）</div>
  <div style="background:var(--surface);border:1px solid #3fb95040;border-radius:10px;padding:12px 16px;margin-bottom:14px;font-size:12px;color:var(--text2);line-height:1.7;">
    条件を満たした試合のみ <strong style="color:#3fb950;">ベット推奨</strong>。stake 1u。結果確定後は全履歴タブへ移動。<br>
    現在 <strong style="color:var(--text);">{go_count}件</strong>
  </div>
  <div class="section"><div class="active-grid">

{go_html}

  </div></div>

  <div class="section-title" style="margin-top:20px;color:#e3b341;border-bottom-color:#d29922;">🟡 CAUTION 監視（予測のみ・ベット無し）</div>
  <div style="background:var(--surface);border:1px solid #d2992240;border-radius:10px;padding:12px 16px;margin-bottom:14px;font-size:12px;color:var(--text2);line-height:1.7;">
    <strong style="color:#e3b341;">CAUTION = 予測精度 tracking のみの監視対象</strong>。GO閾値未達（conf&lt;75% / EV&lt;+5%）または goalie/injury 要確認で <strong>ベットは行いません</strong>。<br>
    EV がマイナス表示でも推奨ではなく「予測が当たったかを追跡するだけ」の意味です。<br>
    現在 <strong style="color:var(--text);">{caution_count}件</strong>
  </div>
  <div class="section"><div class="active-grid">

{caution_html}

  </div></div>

  <div style="margin-top:14px;padding:10px 14px;background:var(--surface2);border-radius:6px;font-size:12px;color:var(--text2);line-height:1.7;">
    <strong style="color:var(--text);">🔄 自動同期:</strong> records/*.json から tier=go/caution かつ hit=null のエントリを動的抽出。最終 sync: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} | Pending 総数: {total_pending}件 (GO {go_count} + CAUTION {caution_count})
  </div>
</div>
<!-- AUTO:ACTIVE_TAB END -->"""
    return html


# ─────────────────────────────────────
# (F) 高確率予想タブ アクティブ候補 (output A)
# ─────────────────────────────────────
def build_highprob_active(cumul):
    """multi_bets.sessions[-1].output_a を根拠にテーブル生成"""
    if not MB_PATH.exists():
        return None
    mb = load_json(MB_PATH)
    if not mb.get("sessions"):
        return None
    last = mb["sessions"][-1]
    session_id = last.get("session", "?").lstrip("_")
    session_date = last.get("date", "?")
    candidates = last.get("output_a", {}).get("candidates", [])

    # Also pull Galfi GO if it's in go_list
    go_items = last.get("go_list", {}).get("recommendations", [])

    rows = []

    # GO 推奨（GO重複）先頭
    for g in go_items:
        odds = g.get("odds", "—")
        ev = g.get("ev")
        ev_str = f"{ev*100:+.1f}%" if isinstance(ev, (int, float)) else "—"
        ev_color = "#3fb950" if isinstance(ev, (int, float)) and ev > 0 else "#f85149"
        rows.append(
            f'            <tr style="background:rgba(46,160,67,.12);">\n'
            f'              <td style="font-weight:600;">{g.get("match", "?")}</td>\n'
            f'              <td>{g.get("sport","?")} {g.get("round","")}<br><span style="font-size:10px;color:var(--text2);">Session_{session_id} {session_date}</span></td>\n'
            f'              <td><span class="badge badge-go">{g.get("rec","?")}</span></td>\n'
            f'              <td style="text-align:center;font-weight:700;color:#4ade80;">{g.get("conf","?")}%</td>\n'
            f'              <td style="text-align:center;color:#e3b341;">@{odds}</td>\n'
            f'              <td style="text-align:center;color:{ev_color};">{ev_str}</td>\n'
            f'              <td style="text-align:center;"><span class="tier-badge tier-adv">Adv</span></td>\n'
            f'              <td><span class="badge badge-pending">pending</span><br><span style="font-size:10px;color:var(--text2);">GO (EV+{ev_str} 重複掲載)</span></td>\n'
            f'            </tr>'
        )

    # Output A candidates
    for c in candidates:
        rows.append(
            f'            <tr style="background:rgba(88,166,255,.06);">\n'
            f'              <td style="font-weight:600;">{c.get("match","?")}</td>\n'
            f'              <td>{c.get("sport","?")} {c.get("round","")}<br><span style="font-size:10px;color:var(--text2);">Session_{session_id} {session_date}</span></td>\n'
            f'              <td><span class="badge" style="background:#1a2640;color:#58a6ff;">{c.get("rec","?")}</span></td>\n'
            f'              <td style="text-align:center;font-weight:700;color:#4ade80;">{c.get("conf","?")}%</td>\n'
            f'              <td style="text-align:center;color:#e3b341;">@{c.get("odds","—")}</td>\n'
            f'              <td style="text-align:center;color:#f85149;">EV-</td>\n'
            f'              <td style="text-align:center;"><span class="tier-badge tier-adv">Adv</span></td>\n'
            f'              <td><span class="badge badge-pending">pending</span><br><span style="font-size:10px;color:var(--text2);">出力A (高確率・EV-)</span></td>\n'
            f'            </tr>'
        )

    rows_html = "\n".join(rows) if rows else "            <tr><td colspan='8' style='text-align:center;color:var(--text2);padding:20px;'>現在アクティブな候補なし</td></tr>"

    html = f"""<!-- AUTO:HIGHPROB_ACTIVE START -->
  <div class="section">
    <div class="section-title" style="color:#3fb950;border-bottom-color:#2ea043;">🎯 アクティブ候補（これから試合・ベット対象）</div>
    <p style="color:var(--text2);font-size:12px;margin-bottom:14px;line-height:1.7;">
      最新セッション (Session_{session_id} {session_date}) の出力A候補を <strong>multi_bets.json から自動抽出</strong>。結果確定後は下の累計履歴へ移動。
    </p>
    <div style="background:var(--surface);border:1px solid #3fb95040;border-radius:10px;padding:14px 18px;margin-bottom:14px;">
      <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:10px;">
        <div style="font-size:11px;color:#3fb950;font-weight:700;text-transform:uppercase;letter-spacing:.05em;">現在アクティブ:</div>
        <div style="font-size:11px;color:var(--text2);">GO {len(go_items)}件 + 出力A {len(candidates)}件 (Session_{session_id})</div>
        <div style="font-size:11px;color:var(--text2);margin-left:auto;">最終同期: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>試合</th><th>種目/ラウンド</th><th>推奨</th><th>勝率</th><th>オッズ</th><th>EV</th><th>Tier</th><th>状態</th>
            </tr>
          </thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <!-- AUTO:HIGHPROB_ACTIVE END -->"""
    return html


# ─────────────────────────────────────
# (G) マルチベットタブ アクティブマルチ
# ─────────────────────────────────────
def build_multi_active(cumul):
    if not MB_PATH.exists():
        return None
    mb = load_json(MB_PATH)
    if not mb.get("sessions"):
        return None
    last = mb["sessions"][-1]
    session_id = last.get("session", "?").lstrip("_")
    session_date = last.get("date", "?")

    output_a_candidates = last.get("output_a", {}).get("candidates", [])
    output_b = last.get("output_b", {})
    combos_all = output_b.get("combos_all", {}) if isinstance(output_b, dict) else {}

    if len(output_a_candidates) < 2:
        content = f"""
    <div style="background:var(--surface);border:1px solid #f0a51940;border-radius:10px;padding:14px 18px;margin-bottom:14px;">
      <div style="color:#f0a519;font-size:13px;">⚠️ アクティブ出力A候補が2件未満のためマルチ構成不可 (現在 {len(output_a_candidates)}件)</div>
    </div>"""
    else:
        # Build tables from combos_all
        two_leg = combos_all.get("2-leg_max_prob", [])
        def fmt_row(i, combo):
            legs = " × ".join(combo.get("legs", []))
            prob = combo.get("total_prob", 0)
            odds = combo.get("total_odds", 0)
            ev = combo.get("ev", 0)
            ev_color = "#3fb950" if ev > 0 else "#f85149"
            return (f'            <tr><td>{i}</td><td>{legs}</td>'
                    f'<td style="text-align:center;color:#4ade80;font-weight:700;">{prob*100:.1f}%</td>'
                    f'<td style="text-align:center;color:#e3b341;">@{odds:.3f}</td>'
                    f'<td style="text-align:center;color:{ev_color};">{ev*100:+.1f}%</td></tr>')

        # Sort by prob desc
        two_leg_by_prob = sorted(two_leg, key=lambda x: -x.get("total_prob", 0))[:5]
        # Sort by ev desc
        all_combos = list(two_leg) + list(combos_all.get("3-leg", [])) + list(combos_all.get("4-leg_full", []))
        all_combos_by_ev = sorted(all_combos, key=lambda x: -x.get("ev", 0))[:5]

        prob_rows = "\n".join(fmt_row(i+1, c) for i, c in enumerate(two_leg_by_prob))
        ev_rows = "\n".join(fmt_row(i+1, c) for i, c in enumerate(all_combos_by_ev))

        ev_plus = sum(1 for c in all_combos if c.get("ev", 0) > 0)
        note = output_b.get("note", "")

        content = f"""
    <div style="background:var(--surface);border:1px solid #58a6ff40;border-radius:10px;padding:14px 18px;margin-bottom:14px;">
      <div style="display:flex;gap:10px;align-items:center;margin-bottom:10px;flex-wrap:wrap;">
        <div style="font-size:13px;font-weight:700;color:#3fb950;">Session_{session_id} マルチ構成計算結果 ({session_date})</div>
        <div style="font-size:11px;color:var(--text2);">出力A {len(output_a_candidates)}件 × 組合せ {len(all_combos)}通り</div>
      </div>
      <div style="background:{"#0f2c1a" if ev_plus else "#2d1014"};border:1px solid {"#23863640" if ev_plus else "#f8514940"};border-radius:6px;padding:10px 14px;margin-bottom:12px;font-size:12px;color:var(--text);line-height:1.7;">
        {"🟢" if ev_plus else "🔴"} <strong style="color:{"#3fb950" if ev_plus else "#f85149"};">EV+組み合わせ: {ev_plus}件</strong> — {note}
      </div>
      <div style="font-size:12px;font-weight:700;color:#4ade80;margin-bottom:6px;">📊 総合勝率 TOP 5（2-leg / 参考）</div>
      <div class="table-wrap" style="margin-bottom:12px;">
        <table class="data-table" style="font-size:11px;">
          <thead><tr><th>#</th><th>組み合わせ</th><th>勝率</th><th>マルチodds</th><th>EV</th></tr></thead>
          <tbody>
{prob_rows}
          </tbody>
        </table>
      </div>
      <div style="font-size:12px;font-weight:700;color:#e3b341;margin-bottom:6px;">💰 EV最大 TOP 5（損失幅最小・参考）</div>
      <div class="table-wrap" style="margin-bottom:12px;">
        <table class="data-table" style="font-size:11px;">
          <thead><tr><th>#</th><th>組み合わせ</th><th>勝率</th><th>マルチodds</th><th>EV</th></tr></thead>
          <tbody>
{ev_rows}
          </tbody>
        </table>
      </div>
    </div>"""

    html = f"""<!-- AUTO:MULTI_ACTIVE START -->
  <div class="section">
    <div class="section-title" style="color:#3fb950;border-bottom-color:#2ea043;">🎯 アクティブマルチ候補（自動算出）</div>
    <p style="color:var(--text2);font-size:12px;margin-bottom:14px;line-height:1.7;">
      最新セッション (Session_{session_id} {session_date}) の output_b を <strong>multi_bets.json から自動抽出</strong>。出力A 2件以上でマルチ構成可。
    </p>
{content}
  </div>
  <!-- AUTO:MULTI_ACTIVE END -->"""
    return html


# ─────────────────────────────────────
# マーカー差し替え
# ─────────────────────────────────────
def replace_marker(content, marker_name, new_html):
    pattern = re.compile(
        rf"<!-- AUTO:{marker_name} START -->.*?<!-- AUTO:{marker_name} END -->",
        re.DOTALL,
    )
    if pattern.search(content):
        return pattern.sub(lambda m: new_html, content), True
    return content, False


def ensure_markers(content):
    """既存の手書きセクションに AUTO マーカーを初回挿入"""
    changes = []

    # BIG_STAT: <div class="overview-top"> 周辺
    if "<!-- AUTO:BIG_STAT START -->" not in content:
        m = re.search(r'<div class="overview-top">.*?</div>\s*</div>\s*<div style="margin-bottom:16px;padding:10px 14px;background:var\(--surface2\)', content, re.DOTALL)
        if m:
            s, e = m.start(), content.find("</div>", m.start()) + len("</div>")
            # Find the real end of overview-top block - it's the outer </div> of big-stat children
            # Easier: find from <div class="overview-top"> to the matching </div> that closes overview-top
            start = content.find('<div class="overview-top">')
            # overview-top closes before <div style="margin-bottom:16px
            summary_start = content.find('<div style="margin-bottom:16px;padding:10px 14px;background:var(--surface2)', start)
            # the close </div> is right before summary_start
            # Find last </div> before summary_start
            close = content.rfind('</div>', start, summary_start)
            if close > start:
                content = content[:start] + "<!-- AUTO:BIG_STAT START -->\n    PLACEHOLDER_BIG_STAT\n    <!-- AUTO:BIG_STAT END -->" + content[close + len("</div>"):]
                changes.append("BIG_STAT marker inserted")

    # SUMMARY: the big summary block after big-stat
    if "<!-- AUTO:SUMMARY START -->" not in content:
        m = re.search(r'<div style="margin-bottom:16px;padding:10px 14px;background:var\(--surface2\);border-radius:6px;font-size:12px;color:var\(--text2\);">\s*<strong[^>]*>⚖️', content)
        if m:
            start = m.start()
            # find closing </div>
            close = content.find("</div>", start)
            if close > 0:
                content = content[:start] + "<!-- AUTO:SUMMARY START -->\nPLACEHOLDER_SUMMARY\n<!-- AUTO:SUMMARY END -->" + content[close + len("</div>"):]
                changes.append("SUMMARY marker inserted")

    # PRED_BET_ONLY: bet-only panel
    if "<!-- AUTO:PRED_BET_ONLY START -->" not in content:
        m = re.search(r'<div class="pred-panel bet-only">', content)
        if m:
            start = m.start()
            # find closing - next `<div class="pred-panel all-games">`
            next_panel = content.find('<div class="pred-panel all-games">', start)
            # go back to find the </div> that closes the bet-only panel
            if next_panel > 0:
                close = content.rfind("</div>", start, next_panel)
                if close > start:
                    content = content[:start] + "<!-- AUTO:PRED_BET_ONLY START -->\nPLACEHOLDER_BET_ONLY\n<!-- AUTO:PRED_BET_ONLY END -->\n    " + content[close + len("</div>"):]
                    changes.append("PRED_BET_ONLY marker inserted")

    # PRED_Q3: all-games panel
    if "<!-- AUTO:PRED_Q3 START -->" not in content:
        m = re.search(r'<div class="pred-panel all-games">', content)
        if m:
            start = m.start()
            # panel closes before </div> that closes .section pred-compare
            # Easier heuristic: find next `</div>\s*</div>\s*\n\s*<!-- 学習ループ`
            end_m = re.search(r'</div>\s*</div>\s*<!-- 学習ループ可視化', content[start:])
            if end_m:
                abs_end = start + end_m.start() + len("</div>")
                content = content[:start] + "<!-- AUTO:PRED_Q3 START -->\nPLACEHOLDER_Q3\n<!-- AUTO:PRED_Q3 END -->" + content[abs_end:]
                changes.append("PRED_Q3 marker inserted")

    # ACTIVE_TAB: replace entire content-active body
    if "<!-- AUTO:ACTIVE_TAB START -->" not in content:
        m = re.search(r'<div class="tab-content" id="content-active">', content)
        if m:
            start = m.end()
            # content-active closes with `</div>\n<!-- ===== 全履歴 ===== -->` pattern
            end_m = re.search(r'</div>\s*<!-- ===== (?:\S+ )?全履歴 ===== -->', content[start:])
            if end_m:
                abs_end = start + end_m.start() + len("</div>")
                content = content[:start] + "\n<!-- AUTO:ACTIVE_TAB START -->\nPLACEHOLDER_ACTIVE\n<!-- AUTO:ACTIVE_TAB END -->\n" + content[abs_end:]
                changes.append("ACTIVE_TAB marker inserted")

    # HIGHPROB_ACTIVE: replaces the wrapper <div class="section"> containing 🎯 アクティブ候補セクション
    if "<!-- AUTO:HIGHPROB_ACTIVE START -->" not in content:
        m = re.search(r'<!-- 🎯 アクティブ候補セクション.*?-->', content, re.DOTALL)
        if m:
            # find the <div class="section"> wrapper start (BEFORE or AFTER the comment)
            # scan back to find <div class="section"> just before this comment
            wrap_start = content.rfind('<div class="section">', 0, m.start() + 200)
            # then find the matching closing </div> for that section wrapper
            # use depth counter starting from wrap_start + 1
            if wrap_start > 0:
                depth = 0
                pos = wrap_start
                close_pos = None
                while pos < len(content):
                    open_m = content.find('<div', pos)
                    close_m = content.find('</div>', pos)
                    if close_m == -1:
                        break
                    if open_m != -1 and open_m < close_m:
                        depth += 1
                        pos = open_m + 4
                    else:
                        depth -= 1
                        if depth == 0:
                            close_pos = close_m + len('</div>')
                            break
                        pos = close_m + len('</div>')
                if close_pos:
                    content = content[:wrap_start] + "<!-- AUTO:HIGHPROB_ACTIVE START -->\nPLACEHOLDER_HIGHPROB\n<!-- AUTO:HIGHPROB_ACTIVE END -->" + content[close_pos:]
                    changes.append("HIGHPROB_ACTIVE marker inserted")

    # MULTI_ACTIVE: replaces the wrapper <div class="section"> containing 🎯 アクティブマルチ候補
    if "<!-- AUTO:MULTI_ACTIVE START -->" not in content:
        m = re.search(r'<!-- 🎯 アクティブマルチ候補', content)
        if m:
            wrap_start = content.rfind('<div class="section">', 0, m.start() + 200)
            if wrap_start > 0:
                depth = 0
                pos = wrap_start
                close_pos = None
                while pos < len(content):
                    open_m = content.find('<div', pos)
                    close_m = content.find('</div>', pos)
                    if close_m == -1:
                        break
                    if open_m != -1 and open_m < close_m:
                        depth += 1
                        pos = open_m + 4
                    else:
                        depth -= 1
                        if depth == 0:
                            close_pos = close_m + len('</div>')
                            break
                        pos = close_m + len('</div>')
                if close_pos:
                    content = content[:wrap_start] + "<!-- AUTO:MULTI_ACTIVE START -->\nPLACEHOLDER_MULTI\n<!-- AUTO:MULTI_ACTIVE END -->" + content[close_pos:]
                    changes.append("MULTI_ACTIVE marker inserted")

    return content, changes


def main():
    print("=== sync_dashboard.py ===")
    stats = load_json(STATS_PATH)
    cumul = load_json(CUMUL_PATH)

    content = DASH_PATH.read_text(encoding="utf-8")

    # Step 0: ensure markers present
    content, inserted = ensure_markers(content)
    for c in inserted:
        print(f"  [INIT] {c}")

    # Step 1: build each section
    big_stat_html = build_big_stat(stats, cumul)
    summary_html = build_summary(stats, cumul)
    bet_only_html = build_bet_only_panel(stats)
    q3_html = build_q3_panel(cumul, stats)
    active_html = build_active_tab(stats)
    highprob_html = build_highprob_active(cumul)
    multi_html = build_multi_active(cumul)

    # Step 2: replace
    sections = [
        ("BIG_STAT", big_stat_html),
        ("SUMMARY", summary_html),
        ("PRED_BET_ONLY", bet_only_html),
        ("PRED_Q3", q3_html),
        ("ACTIVE_TAB", active_html),
        ("HIGHPROB_ACTIVE", highprob_html),
        ("MULTI_ACTIVE", multi_html),
    ]
    for name, html in sections:
        if html is None:
            print(f"  [SKIP] {name} (no data)")
            continue
        content, ok = replace_marker(content, name, html)
        print(f"  [{'OK' if ok else 'MISS'}] {name}")

    # Step 3: div balance
    masked = re.sub(r'<style[\s\S]*?</style>',
                    lambda m: m.group().replace('<div', '<XXX').replace('</div>', '</XXX'), content)
    masked = re.sub(r'<script[\s\S]*?</script>',
                    lambda m: m.group().replace('<div', '<XXX').replace('</div>', '</XXX'), masked)
    o = masked.count('<div')
    cl = masked.count('</div>')
    diff = o - cl
    print(f"Div balance: <div={o}, </div={cl}, diff={diff} -> {'OK' if diff == 0 else 'PROBLEM'}")

    # Step 4: save
    DASH_PATH.write_text(content, encoding="utf-8")
    print(f"dashboard.html saved. updated_at={datetime.datetime.now().isoformat()}")
    print()
    print("次ステップ:")
    print("  python sync_sport_cards.py  # 種目別カードも再同期")
    print("  git add dashboard.html core/dashboard_stats.json records/ stats/ && git commit -m 'Sync dashboard'")


if __name__ == "__main__":
    main()
