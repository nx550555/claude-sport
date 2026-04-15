#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. アクティブタブ: HIT/SKIP カードを削除（PENDING GO のみ残す）
2. アクティブタブ: セクションタイトルの文字化けを修正
3. 高確率予想タブ: 選手名・チーム名を日本語化
4. マルチベットタブ: 選手名・チーム名を日本語化
"""

html_path = r"C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
with open(html_path, encoding='utf-8') as f:
    html = f.read()

fixes = []

# ===== 1. セクションタイトル修正（文字化け） =====
# 現状: "繧｢繧ｯ繝・ぅ繝・GO 謗ｨ螂ｨ 窶・邨先棡蠕・■・域律莉倥・繝ｪ繝ｼ繧ｰ鬆・ｼ・"
old_title_garbled = '  <div class="section-title">\xe7\xb9\xa7\xe3\x82\xa2\xe7\xb9\xa7\xe3\x83\xaf\xe7\xb9\x9d\xe3\x83\xbb\xe3\x81\x85\xe3\x83\x9d\xe3\x83\xbb\xe3\x82\x9a GO \xe8\xac\x97\xe3\xa8\x98\xe8\xac\xa1\xe3\xa8\x8a \xe7\xaa\x9f\xe3\x83\xbb\xe9\x82\xa8\xe5\x85\x88\xe6\xa3\x9f\xe8\xb9\x83\xe3\x83\xbb\xe2\x96\xa0\xe3\x83\xbb\xe5\x9f\x9f\xe5\xbe\x8b\xe8\x8e\x89\xe5\x80\xa5\xe3\x83\xbb\xe7\xb9\x9d\xe3\x83\xaa\xe3\x83\xbc\xe3\x82\xb0\xe9\xac\x86\xe3\x83\xbb\xe3\x82\xbc\xe3\x83\xbb</div>'

# 実際の文字列で検索
import re

# section-titleを正確に置換（アクティブ推奨タブの最初のsection-title）
pattern = r'(<div class="tab-content" id="content-active">)\s*<div class="section-title">[^<]+</div>'
replacement_title = r'\1\n  <div class="section-title">アクティブ GO 推奨 — PENDING のみ（結果確定後は全履歴タブへ移動）</div>'

new_html, count = re.subn(pattern, replacement_title, html, count=1)
if count:
    html = new_html
    fixes.append("セクションタイトル: 文字化け修正")
else:
    # 別パターンで試す
    idx = html.find('<div class="tab-content" id="content-active">')
    if idx != -1:
        end = html.find('</div>', idx) + 6
        snippet = html[idx:end]
        print(f"DEBUG title area: {repr(snippet[:200])}")


# ===== 2. アクティブタブ: HIT/SKIP カード削除 =====
# 削除対象ブロック（各コメント開始〜</div>\n\nまで）

blocks_to_remove = [
    # ATP Barcelona R1 HIT (Musetti)
    (
        '\n    <!-- ATP Barcelona R1 HIT -->\n'
        '    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">\n'
        '      <div class="ac-sport">&#x1F3BE; ATP &mdash; Barcelona R1 2026 <span class="badge badge-hit">HIT &#x2713;</span></div>\n'
        '      <div class="ac-match">2026-04-14 JST / Barcelona Clay R1</div>\n'
        '      <div class="ac-rec" style="color:#3fb950;">&#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3; 7-5 6-2</div>\n'
        '      <div class="ac-metrics">\n'
        '        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.27</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+9.7%</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.27u</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">86.4%</div></div>\n'
        '      </div>\n'
        '      <div class="ac-note">cElo &#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3; ~2017 / &#x30E9;&#x30F3;&#x30C0;&#x30EB;&#x30FC;&#x30B5; ~1648. conf 86.4% / EV+9.7%</div>\n'
        '      <div class="ac-date">&#x1F4C5; 2026-04-14 JST &#x2713;&#x78BA;&#x5B9A;</div>\n'
        '    </div>\n'
    ),
    # ATP Munich R1 Cobolli HIT
    (
        '\n    <!-- ATP Munich R1 Cobolli HIT -->\n'
        '    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">\n'
        '      <div class="ac-sport">&#x1F3BE; ATP &mdash; Munich R1 2026 <span class="badge badge-hit">HIT &#x2713;</span></div>\n'
        '      <div class="ac-match">2026-04-14 JST / Munich Clay R1</div>\n'
        '      <div class="ac-rec" style="color:#3fb950;">&#x30B3;&#x30DC;&#x30C3;&#x30EA; 6-4 7-5</div>\n'
        '      <div class="ac-metrics">\n'
        '        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.21</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+8.7%</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.21u</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">89.8%</div></div>\n'
        '      </div>\n'
        '      <div class="ac-note">cElo &#x30B3;&#x30DC;&#x30C3;&#x30EA; 1929 / &#x30C7;&#x30C9;&#x30A5;&#x30E9;=&#x30D1;&#x30EB;&#x30E1;&#x30ED; 1551. conf 89.8% / EV+8.7%</div>\n'
        '      <div class="ac-date">&#x1F4C5; 2026-04-14 JST &#x2713;&#x78BA;&#x5B9A;</div>\n'
        '    </div>\n'
    ),
    # ATP Munich R1 Kopriva HIT
    (
        '\n    <!-- ATP Munich R1 Kopriva HIT -->\n'
        '    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">\n'
        '      <div class="ac-sport">&#x1F3BE; ATP &mdash; Munich R1 2026 <span class="badge badge-hit">HIT &#x2713;</span></div>\n'
        '      <div class="ac-match">2026-04-14 JST / Munich Clay R1</div>\n'
        '      <div class="ac-rec" style="color:#3fb950;">&#x30B3;&#x30D7;&#x30B8;&#x30D0; 6-3 5-7 6-2</div>\n'
        '      <div class="ac-metrics">\n'
        '        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.36</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+9.8%</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.36u</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">80.7%</div></div>\n'
        '      </div>\n'
        '      <div class="ac-note">cElo &#x30B3;&#x30D7;&#x30B8;&#x30D0; 1699 / &#x30A8;&#x30F3;&#x30B2;&#x30EB; 1388. conf 80.7% / EV+9.8%</div>\n'
        '      <div class="ac-date">&#x1F4C5; 2026-04-14 JST &#x2713;&#x78BA;&#x5B9A;</div>\n'
        '    </div>\n'
    ),
    # ATP MC Final SKIP
    (
        '<!-- ATP MC Final SKIP -->\n'
        '    <div class="active-card" style="border-color:#30363d;background:linear-gradient(135deg,#30363d10,transparent);opacity:.7;">\n'
        '      <div class="ac-sport">&#x1F3BE; ATP &mdash; MC2026 &#x6C7A;&#x52DD; <span class="badge badge-skip">SKIP&#xFF08;&#x89B3;&#x6226;&#xFF09;</span></div>\n'
        '      <div class="ac-match">&#x30A2;&#x30EB;&#x30AB;&#x30E9;&#x30B9; C.(1) vs &#x30B7;&#x30CA;&#x30FC; J.(2)</div>\n'
        '      <div class="ac-rec" style="color:#3fb950;">&#x7D50;&#x679C;: &#x30B7;&#x30CA;&#x30FC; 7-6(5) 6-3 &mdash; &#x4E88;&#x6E2C;&#x306A;&#x3057;&#xFF08;SKIP&#xFF09;</div>\n'
        '      <div class="ac-metrics">\n'
        '        <div class="acm"><div class="acm-l">cElo&#x5DEE;</div><div class="acm-v rule">~20pt</div></div>\n'
        '        <div class="acm"><div class="acm-l">L1&#x5224;&#x5B9A;</div><div class="acm-v" style="color:#f85149;">&#x4E0D;&#x901A;&#x904E;</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;</div><div class="acm-v" style="color:#8b949e;">50/50</div></div>\n'
        '        <div class="acm"><div class="acm-l">bet</div><div class="acm-v rule">&#x306A;&#x3057;</div></div>\n'
        '      </div>\n'
        '      <div class="ac-note">SKIP&#x6B63;&#x89E3;&#xFF08;&#x5DEE;&#x306A;&#x3057;&#x3067;&#x5F53;&#x3066;&#x3066;&#x3082;&#x904B;&#xFF09;&#x3002;&#x30B7;&#x30CA;&#x30FC;&#x304C;7-6(5) 6-3&#x3067;&#x512A;&#x52DD;&#x3002;</div>\n'
        '      <div class="ac-date">&#x1F4C5; 2026-04-13 JST &#x2713;&#x5B8C;&#x4E86;</div>\n'
        '    </div>\n'
    ),
    # UFL Week 3 HIT
    (
        '\n    <!-- UFL Week 3 Dallas HIT -->\n'
        '    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">\n'
        '      <div class="ac-sport">&#x1F3C8; UFL Week 3 &mdash; &#x30B3;&#x30ED;&#x30F3;&#x30D0;&#x30B9; @ &#x30C0;&#x30E9;&#x30B9; <span class="badge badge-hit">HIT &#x2713;</span></div>\n'
        '      <div class="ac-match">2026-04-12 JST / Cotton Bowl, Dallas</div>\n'
        '      <div class="ac-rec" style="color:#3fb950;">&#x30C0;&#x30E9;&#x30B9;&#x30FB;&#x30EC;&#x30CD;&#x30B2;&#x30FC;&#x30BA; 28 &mdash; 23 &#x30B3;&#x30ED;&#x30F3;&#x30D0;&#x30B9;&#x30FB;&#x30A2;&#x30D3;&#x30A8;&#x30A4;&#x30BF;&#x30FC;&#x30BA;</div>\n'
        '      <div class="ac-metrics">\n'
        '        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.32</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+8.2%</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.32u</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">82%</div></div>\n'
        '      </div>\n'
        '      <div class="ac-note">PD&#x5DEE;30pt&#xFF08;&#x30C0;&#x30E9;&#x30B9; +17.5/&#x8A66;&#x5408; vs &#x30B3;&#x30ED;&#x30F3;&#x30D0;&#x30B9; -12.5/&#x8A66;&#x5408;&#xFF09;&#x304C;&#x5730;&#x529B;&#x5DEE;&#x901A;&#x308A;&#x3002;</div>\n'
        '      <div class="ac-date">&#x1F4C5; 2026-04-12 JST &#x2713;&#x78BA;&#x5B9A;</div>\n'
        '    </div>\n'
    ),
    # NBA Rockets HIT
    (
        '\n    <!-- NBA Rockets HIT -->\n'
        '    <div class="active-card" style="border-color:#23863640;background:linear-gradient(135deg,#23863610,transparent);opacity:.8;">\n'
        '      <div class="ac-sport">&#x1F3C0; NBA &mdash; &#x30B0;&#x30EA;&#x30BA;&#x30EA;&#x30FC;&#x30BA; @ &#x30ED;&#x30B1;&#x30C3;&#x30C8; <span class="badge badge-hit">HIT &#x2713;</span></div>\n'
        '      <div class="ac-match">2026-04-12 JST / Toyota Center, Houston</div>\n'
        '      <div class="ac-rec" style="color:#3fb950;">&#x30D2;&#x30E5;&#x30FC;&#x30B9;&#x30C8;&#x30F3;&#x30FB;&#x30ED;&#x30B1;&#x30C3;&#x30C4;&#x30B9; 124 &mdash; 109 &#x30E1;&#x30F3;&#x30D5;&#x30A3;&#x30B9;&#x30FB;&#x30B0;&#x30EA;&#x30BA;&#x30EA;&#x30FC;&#x30BA;</div>\n'
        '      <div class="ac-metrics">\n'
        '        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v odds">1.20</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x4E88;&#x6E2C;EV</div><div class="acm-v ev">+5.6%</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x5B9F;&#x7E3E;EV</div><div class="acm-v ev">+0.20u</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x78BA;&#x4FE1;&#x5EA6;</div><div class="acm-v">88%</div></div>\n'
        '      </div>\n'
        '      <div class="ac-date">&#x1F4C5; 2026-04-12 JST &#x2713;&#x78BA;&#x5B9A;&#x6E08;</div>\n'
        '    </div>\n'
    ),
    # NBA Wizards SKIP
    (
        '\n    <!-- NBA Wizards SKIP -->\n'
        '    <div class="active-card" style="border-color:#30363d;background:linear-gradient(135deg,#30363d08,transparent);opacity:.7;">\n'
        '      <div class="ac-sport">&#x1F3C0; NBA &mdash; &#x30A6;&#x30A3;&#x30B6;&#x30FC;&#x30BA; @ &#x30AD;&#x30E3;&#x30D0;&#x30EA;&#x30A2;&#x30FC;&#x30BA; <span class="badge badge-skip">SKIP</span></div>\n'
        '      <div class="ac-match">2026-04-12 JST / Cavs 130-126&#xFF08;&#x53C2;&#x8003;&#x8A18;&#x9332;&#xFF09;</div>\n'
        '      <div class="ac-rec" style="color:#8b949e;">&#x30AA;&#x30C3;&#x30BA;&#x672A;&#x78BA;&#x8A8D;&#x306E;&#x305F;&#x3081;&#x30D9;&#x30C3;&#x30C8;&#x672A;&#x5B9F;&#x884C;</div>\n'
        '      <div class="ac-metrics">\n'
        '        <div class="acm"><div class="acm-l">&#x7D50;&#x679C;</div><div class="acm-v" style="color:#3fb950;">Cavs&#x52DD;</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x30DF;&#x30C3;&#x30C1;&#x30A7;&#x30EB;</div><div class="acm-v ev">48pts</div></div>\n'
        '        <div class="acm"><div class="acm-l">&#x30AA;&#x30C3;&#x30BA;</div><div class="acm-v warn">&#x672A;&#x53D6;&#x5F97;</div></div>\n'
        '        <div class="acm"><div class="acm-l">EV</div><div class="acm-v rule">&#x30AB;&#x30A6;&#x30F3;&#x30C8;&#x5916;</div></div>\n'
        '      </div>\n'
        '      <div class="ac-date">&#x1F4C5; 2026-04-12 JST &mdash; &#x7D71;&#x8A08;&#x30CE;&#x30FC;&#x30AB;&#x30A6;&#x30F3;&#x30C8;</div>\n'
        '    </div>\n'
    ),
]

removed = 0
for block in blocks_to_remove:
    if block in html:
        html = html.replace(block, '')
        removed += 1
    else:
        print(f"WARN: block not found (first 80 chars): {repr(block[:80])}")

fixes.append(f"HIT/SKIP カード削除: {removed}/{len(blocks_to_remove)} 件")

# ===== 3. 高確率予想タブ: 選手名・チーム名を日本語化（highprob-rows 内のみ） =====
# セクションを特定してから置換
hp_start = html.find('<tbody id="highprob-rows">')
hp_end = html.find('</tbody>', hp_start) + 8
hp_section = html[hp_start:hp_end]

jp_replacements_hp = [
    # 試合名セル（選手名）
    ('Swiatek I. vs<br><strong>Siegemund L.</strong>',
     'シフィアテク I. vs<br><strong>ジーゲムント L.</strong>'),
    ('Alcaraz C. vs<br><strong>Machac T.</strong>',
     'アルカラス C. vs<br><strong>マハッチ T.</strong>'),
    ('Columbus Aviators @<br><strong>Arlington Renegades</strong>',
     'コロンバス・アビエイターズ @<br><strong>アーリントン・レネゲーズ</strong>'),
    ('Houston Gamblers vs<br><strong>Louisville Kings</strong>',
     'ヒューストン・ギャンブラーズ vs<br><strong>ルイビル・キングス</strong>'),
    ('Samsonova L. vs<br><strong>Gauff C.</strong>',
     'サムソノワ L. vs<br><strong>ゴーフ C.</strong>'),
    ('Moutet C. vs<br><strong>Musetti L.</strong>',
     'ムテ C. vs<br><strong>ムセッティ L.</strong>'),
    ('Sonmez Z. vs<br><strong>Paolini J.(4)</strong>',
     'ソンメズ Z. vs<br><strong>パオリーニ J.(4)</strong>'),
    # 推奨バッジ
    ('>Swiatek<', '>シフィアテク<'),
    ('>Alcaraz<', '>アルカラス<'),
    ('>Renegades<', '>レネゲーズ<'),
    ('>Louisville<', '>ルイビル<'),
    ('>Gauff<', '>ゴーフ<'),
    ('>Musetti<', '>ムセッティ<'),
    ('>Paolini<', '>パオリーニ<'),
    # 理由列の英語
    ('Renegades 3-0 vs Aviators 0-3。DIFF/G差。Austin Reed QB確認済。ホーム優位+4%。EV+15.6%。',
     'レネゲーズ 3-0 vs アビエイターズ 0-3。DIFF/G差。Austin Reed QB確認済。ホーム優位+4%。EV+15.6%。'),
    ('Louisville 3-0 vs Gamblers 0-3。DIFF/G差8点超。OLine格差。EV+35.3%。',
     'ルイビル 3-0 vs ギャンブラーズ 0-3。DIFF/G差8点超。OLine格差。EV+35.3%。'),
    ('WTA #3 vs 世界10位前後。Gauff Clay成績良好。推定勝率81%。EV-6.7%のため予測のみ。',
     'WTA #3 vs 世界10位前後。ゴーフ クレー成績良好。推定勝率81%。EV-6.7%のため予測のみ。'),
    ('cElo差300pt（Paolini 1916 vs Sonmez 1616）。推定勝率78%。EV+5.4%。',
     'cElo差300pt（パオリーニ 1916 vs ソンメズ 1616）。推定勝率78%。EV+5.4%。'),
    ('ATP #3 Clay specialist vs 世界66位。cElo差300pt超。Barcelona地元。',
     'ATP #3 クレー専門家 vs 世界66位。cElo差300pt超。バルセロナ地元。'),
]

hp_new = hp_section
for old, new in jp_replacements_hp:
    if old in hp_new:
        hp_new = hp_new.replace(old, new)
    else:
        print(f"WARN highprob: not found: {repr(old[:50])}")

html = html[:hp_start] + hp_new + html[hp_end:]
fixes.append("高確率予想タブ: 選手名・チーム名を日本語化")

# ===== 4. マルチベットタブ: 選手名・チーム名を日本語化（multi-rows 内のみ） =====
m_start = html.find('<div id="multi-rows"')
m_end = html.find('</div>\n\n<!-- ===== ', m_start) + 6  # closing div of multi-rows
# 代替検索
if m_end < m_start:
    m_end = html.find('</div>\n</div>\n</div>\n\n<div class="footer">', m_start)

m_section = html[m_start:m_end]

jp_replacements_multi = [
    # タイトル行
    ('Louisville &times; Renegades &times; Musetti（3試合）',
     'ルイビル &times; レネゲーズ &times; ムセッティ（3試合）'),
    ('Louisville &times; Renegades &times; Musetti &times; Alcaraz（4試合）',
     'ルイビル &times; レネゲーズ &times; ムセッティ &times; アルカラス（4試合）'),
    ('Louisville &times; Renegades &times; Musetti &times; Paolini（4試合）',
     'ルイビル &times; レネゲーズ &times; ムセッティ &times; パオリーニ（4試合）'),
    ('Louisville &times; Renegades &times; Musetti &times; Alcaraz &times; Paolini（5試合）',
     'ルイビル &times; レネゲーズ &times; ムセッティ &times; アルカラス &times; パオリーニ（5試合）'),
    ('Louisville &times; Renegades &times; Musetti &times; Swiatek（4試合）',
     'ルイビル &times; レネゲーズ &times; ムセッティ &times; シフィアテク（4試合）'),
    # 詳細行
    ('Houston vs <strong>Louisville Kings</strong> (UFL W4) &times; Aviators @ <strong>Renegades</strong> (UFL W4) &times; Moutet vs <strong>Musetti</strong> (Barcelona R2)',
     'ヒューストン vs <strong>ルイビル・キングス</strong> (UFL W4) &times; アビエイターズ @ <strong>レネゲーズ</strong> (UFL W4) &times; ムテ vs <strong>ムセッティ</strong> (バルセロナ R2)'),
    ('+<strong>Alcaraz</strong> (Barcelona R2) 追加',
     '+<strong>アルカラス</strong> (バルセロナ R2) 追加'),
    ('+<strong>Paolini</strong> (WTA Stuttgart R2) 追加',
     '+<strong>パオリーニ</strong> (WTA シュトゥットガルト R2) 追加'),
    ('+<strong>Alcaraz</strong> &amp; <strong>Paolini</strong> 追加（5連複）',
     '+<strong>アルカラス</strong> &amp; <strong>パオリーニ</strong> 追加（5連複）'),
    ('+<strong>Swiatek</strong> (WTA Stuttgart R2) 追加',
     '+<strong>シフィアテク</strong> (WTA シュトゥットガルト R2) 追加'),
]

m_new = m_section
for old, new in jp_replacements_multi:
    if old in m_new:
        m_new = m_new.replace(old, new)
    else:
        print(f"WARN multi: not found: {repr(old[:60])}")

html = html[:m_start] + m_new + html[m_end:]
fixes.append("マルチベットタブ: 選手名・チーム名を日本語化")

# ===== 保存 =====
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("\n===== 修正完了 =====")
for i, fix in enumerate(fixes, 1):
    print(f"  {i}. {fix}")
print("\ndashboard.html: saved")
