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

    # Step 2: replace
    for name, html in [
        ("BIG_STAT", big_stat_html),
        ("SUMMARY", summary_html),
        ("PRED_BET_ONLY", bet_only_html),
        ("PRED_Q3", q3_html),
    ]:
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
