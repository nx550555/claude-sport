#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. sport card 待機中カウント修正 (ATP: 0->1, NRL: 2->1)
2. 言語トグル (JP/EN) 追加
"""

path = r"C:\Users\ohwada\Desktop\claude_sport\dashboard.html"
with open(path, encoding='utf-8') as f:
    content = f.read()

# ── 1. ATP 待機中 0 → 1 ──────────────────────────────────
# ATP sport card: GO回数=13, 結果済=12, 的中..., 待機中=0
# Anchor: the cell right after ATP累積EV row (unique: ATP cumulative EV is +1.370)
old_atp_wait = (
    '          <div class="sm"><div class="sm-label">\u5f85\u6a5f\u4e2d<'
    '/div><div class="sm-val" style="color:#8b949e;">0</div></div>\n'
    '        </div>\n'
    '      </div>\n'
    '      <div class="sport-card">\n'
    '        <div class="sport-card-header" style="color:#f9a8d4;">'
)
new_atp_wait = (
    '          <div class="sm"><div class="sm-label">\u5f85\u6a5f\u4e2d<'
    '/div><div class="sm-val" style="color:#d29922;">1</div></div>\n'
    '        </div>\n'
    '      </div>\n'
    '      <div class="sport-card">\n'
    '        <div class="sport-card-header" style="color:#f9a8d4;">'
)
if old_atp_wait in content:
    content = content.replace(old_atp_wait, new_atp_wait, 1)
    print("OK: ATP 待機中 0->1")
else:
    print("MISS: ATP anchor not found")

# ── 2. NRL 待機中 2 → 1 ──────────────────────────────────
# NRL card anchor: color:#86efac (NRL header), then 待機中 with value 2 and e3b341
old_nrl_wait = (
    '          <div class="sm"><div class="sm-label">\u5f85\u6a5f\u4e2d'
    '</div><div class="sm-val" style="color:#e3b341;">2</div></div>\n'
    '        </div>\n'
    '      </div>\n'
    '      <div class="sport-card">\n'
    '        <div class="sport-card-header" style="color:#c4b5fd;">'
)
new_nrl_wait = (
    '          <div class="sm"><div class="sm-label">\u5f85\u6a5f\u4e2d'
    '</div><div class="sm-val" style="color:#d29922;">1</div></div>\n'
    '        </div>\n'
    '      </div>\n'
    '      <div class="sport-card">\n'
    '        <div class="sport-card-header" style="color:#c4b5fd;">'
)
if old_nrl_wait in content:
    content = content.replace(old_nrl_wait, new_nrl_wait, 1)
    print("OK: NRL 待機中 2->1")
else:
    print("MISS: NRL anchor not found")

# ── 3. CSS 追加 (言語トグル用) ──────────────────────────────────
css_lang = """
/* ── lang toggle ── */
.name-en { display: none; }
body.lang-en .name-ja { display: none; }
body.lang-en .name-en { display: inline; }
#lang-toggle {
  position: fixed; top: 10px; right: 14px; z-index: 1000;
  background: var(--surface2); border: 1px solid var(--border);
  color: var(--text2); border-radius: 6px; padding: 3px 10px;
  font-size: 11px; font-weight: 700; cursor: pointer; letter-spacing: .04em;
}
#lang-toggle:hover { color: var(--text); border-color: var(--text2); }
"""
content = content.replace('</style>', css_lang + '</style>', 1)
print("OK: CSS lang toggle added")

# ── 4. トグルボタン + JS 追加 ──────────────────────────────────
toggle_btn = '<button id="lang-toggle" onclick="toggleLang()" title="Switch player/team name language">EN</button>\n'
content = content.replace('<body>', '<body>\n' + toggle_btn, 1)
print("OK: toggle button added")

toggle_js = """
function toggleLang() {
  const en = document.body.classList.toggle('lang-en');
  document.getElementById('lang-toggle').textContent = en ? 'JA' : 'EN';
}
"""
content = content.replace('</script>', toggle_js + '\n</script>')
print("OK: toggleLang() JS added")

# ── 5. 名前要素を二言語化 ──────────────────────────────────

def dual(ja, en):
    return f'<span class="name-ja">{ja}</span><span class="name-en">{en}</span>'

# === ACTIVE カード ac-match ===
ac_match_pairs = [
    # Musetti
    ('class="ac-match">&#x30E0;&#x30C6; C. vs &#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3; L.(2)<',
     f'class="ac-match">{dual("&#x30E0;&#x30C6; C. vs &#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3; L.(2)", "Moutet C. vs Musetti L.(2)")}<'),
    # Bondar
    ('class="ac-match">&#x30BF;&#x30F3; H. vs &#x30DC;&#x30F3;&#x30C0;&#x30EB; A.<',
     f'class="ac-match">{dual("&#x30BF;&#x30F3; H. vs &#x30DC;&#x30F3;&#x30C0;&#x30EB; A.", "Tan H. vs Bondar A.")}<'),
    # Paolini
    ('class="ac-match">&#x30BD;&#x30F3;&#x30E1;&#x30BA; Z. vs &#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB; J.(4)<',
     f'class="ac-match">{dual("&#x30BD;&#x30F3;&#x30E1;&#x30BA; Z. vs &#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB; J.(4)", "Sonmez Z. vs Paolini J.(4)")}<'),
    # Louisville
    ('class="ac-match">&#x30D2;&#x30E5;&#x30FC;&#x30B9;&#x30C8;&#x30F3;&#x30FB;&#x30AE;&#x30E3;&#x30F3;&#x30D6;&#x30E9;&#x30FC;&#x30BA; vs &#x30EB;&#x30A4;&#x30D3;&#x30EB;&#x30FB;&#x30AD;&#x30F3;&#x30B0;&#x30B9;<',
     f'class="ac-match">{dual("&#x30D2;&#x30E5;&#x30FC;&#x30B9;&#x30C8;&#x30F3;&#x30FB;&#x30AE;&#x30E3;&#x30F3;&#x30D6;&#x30E9;&#x30FC;&#x30BA; vs &#x30EB;&#x30A4;&#x30D3;&#x30EB;&#x30FB;&#x30AD;&#x30F3;&#x30B0;&#x30B9;", "Houston Gamblers vs Louisville Kings")}<'),
    # Renegades
    ('class="ac-match">&#x30B3;&#x30ED;&#x30F3;&#x30D0;&#x30B9;&#x30FB;&#x30A2;&#x30D3;&#x30A8;&#x30A4;&#x30BF;&#x30FC;&#x30BA; @ &#x30A2;&#x30FC;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30EC;&#x30CD;&#x30B2;&#x30FC;&#x30BA;<',
     f'class="ac-match">{dual("&#x30B3;&#x30ED;&#x30F3;&#x30D0;&#x30B9;&#x30FB;&#x30A2;&#x30D3;&#x30A8;&#x30A4;&#x30BF;&#x30FC;&#x30BA; @ &#x30A2;&#x30FC;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30EC;&#x30CD;&#x30B2;&#x30FC;&#x30BA;", "Columbus Aviators @ Arlington Renegades")}<'),
    # NZ Warriors (with GO badge - need to handle specially)
    ('class="ac-match">NZ&#x30A6;&#x30A9;&#x30EA;&#x30A2;&#x30FC;&#x30BA; vs &#x30B4;&#x30FC;&#x30EB;&#x30C9;&#x30B3;&#x30FC;&#x30B9;&#x30C8;&#x30FB;&#x30BF;&#x30A4;&#x30BF;&#x30F3;&#x30BA; <span class="badge badge-go">GO</span><',
     f'class="ac-match">{dual("NZ&#x30A6;&#x30A9;&#x30EA;&#x30A2;&#x30FC;&#x30BA; vs &#x30B4;&#x30FC;&#x30EB;&#x30C9;&#x30B3;&#x30FC;&#x30B9;&#x30C8;&#x30FB;&#x30BF;&#x30A4;&#x30BF;&#x30F3;&#x30BA;", "NZ Warriors vs Gold Coast Titans")} <span class="badge badge-go">GO</span><'),
    # Leeds (with GO badge)
    ('class="ac-match">&#x30CF;&#x30C0;&#x30FC;&#x30BA;&#x30D5;&#x30A3;&#x30FC;&#x30EB;&#x30C9;&#x30FB;&#x30B8;&#x30E3;&#x30A4;&#x30A2;&#x30F3;&#x30C4; vs &#x30EA;&#x30FC;&#x30BA;&#x30FB;&#x30E9;&#x30A4;&#x30CE;&#x30BA; <span class="badge badge-go">GO</span><',
     f'class="ac-match">{dual("&#x30CF;&#x30C0;&#x30FC;&#x30BA;&#x30D5;&#x30A3;&#x30FC;&#x30EB;&#x30C9;&#x30FB;&#x30B8;&#x30E3;&#x30A4;&#x30A2;&#x30F3;&#x30C4; vs &#x30EA;&#x30FC;&#x30BA;&#x30FB;&#x30E9;&#x30A4;&#x30CE;&#x30BA;", "Huddersfield Giants vs Leeds Rhinos")} <span class="badge badge-go">GO</span><'),
    # Warrington (with GO badge)
    ('class="ac-match">&#x30AB;&#x30BF;&#x30EB;&#x30FC;&#x30CB;&#x30E3;&#x30FB;&#x30C9;&#x30E9;&#x30B4;&#x30F3;&#x30BA; vs &#x30A6;&#x30A9;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30A6;&#x30EB;&#x30D6;&#x30BA; <span class="badge badge-go">GO</span><',
     f'class="ac-match">{dual("&#x30AB;&#x30BF;&#x30EB;&#x30FC;&#x30CB;&#x30E3;&#x30FB;&#x30C9;&#x30E9;&#x30B4;&#x30F3;&#x30BA; vs &#x30A6;&#x30A9;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30A6;&#x30EB;&#x30D6;&#x30BA;", "Catalans Dragons vs Warrington Wolves")} <span class="badge badge-go">GO</span><'),
]

# === ACTIVE カード ac-rec (推奨名 strong内) ===
ac_rec_pairs = [
    ('>&#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3;&#x30FB;&#x30ED;&#x30EC;&#x30F3;&#x30C4;&#x30A9;</strong>',
     f'>{dual("&#x30E0;&#x30BB;&#x30C3;&#x30C6;&#x30A3;&#x30FB;&#x30ED;&#x30EC;&#x30F3;&#x30C4;&#x30A9;", "Musetti Lorenzo")}</strong>'),
    ('>&#x30DC;&#x30F3;&#x30C0;&#x30EB;&#x30FB;&#x30A2;&#x30F3;&#x30CA;</strong>',
     f'>{dual("&#x30DC;&#x30F3;&#x30C0;&#x30EB;&#x30FB;&#x30A2;&#x30F3;&#x30CA;", "Bondar Anna")}</strong>'),
    ('>&#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB;&#x30FB;&#x30B8;&#x30E3;&#x30B9;&#x30DF;&#x30F3;</strong>',
     f'>{dual("&#x30D1;&#x30AA;&#x30EA;&#x30FC;&#x30CB;&#x30FB;&#x30B8;&#x30E3;&#x30B9;&#x30DF;&#x30F3;", "Paolini Jasmine")}</strong>'),
    ('>&#x30EB;&#x30A4;&#x30D3;&#x30EB;&#x30FB;&#x30AD;&#x30F3;&#x30B0;&#x30B9;</strong>',
     f'>{dual("&#x30EB;&#x30A4;&#x30D3;&#x30EB;&#x30FB;&#x30AD;&#x30F3;&#x30B0;&#x30B9;", "Louisville Kings")}</strong>'),
    ('>&#x30A2;&#x30FC;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30EC;&#x30CD;&#x30B2;&#x30FC;&#x30BA;</strong>',
     f'>{dual("&#x30A2;&#x30FC;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30EC;&#x30CD;&#x30B2;&#x30FC;&#x30BA;", "Arlington Renegades")}</strong>'),
    ('>NZ&#x30A6;&#x30A9;&#x30EA;&#x30A2;&#x30FC;&#x30BA;</strong>',
     f'>{dual("NZ&#x30A6;&#x30A9;&#x30EA;&#x30A2;&#x30FC;&#x30BA;", "NZ Warriors")}</strong>'),
    ('>&#x30EA;&#x30FC;&#x30BA;&#x30FB;&#x30E9;&#x30A4;&#x30CE;&#x30BA;</strong>',
     f'>{dual("&#x30EA;&#x30FC;&#x30BA;&#x30FB;&#x30E9;&#x30A4;&#x30CE;&#x30BA;", "Leeds Rhinos")}</strong>'),
    ('>&#x30A6;&#x30A9;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30A6;&#x30EB;&#x30D6;&#x30BA;</strong>',
     f'>{dual("&#x30A6;&#x30A9;&#x30EA;&#x30F3;&#x30C8;&#x30F3;&#x30FB;&#x30A6;&#x30EB;&#x30D6;&#x30BA;", "Warrington Wolves")}</strong>'),
]

# === 高確率予想テーブル (UTF-8 日本語) ===
hp_match_pairs = [
    # Row 1: Swiatek
    ('シフィアテク I. vs<br><strong>ジーゲムント L.</strong>',
     f'{dual("シフィアテク I.", "Swiatek I.")} vs<br><strong>{dual("ジーゲムント L.", "Siegemund L.")}</strong>'),
    # Row 2: Alcaraz
    ('アルカラス C. vs<br><strong>マハッチ T.</strong>',
     f'{dual("アルカラス C.", "Alcaraz C.")} vs<br><strong>{dual("マハッチ T.", "Machac T.")}</strong>'),
    # Row 3: Renegades
    ('コロンバス・アビエイターズ @<br><strong>アーリントン・レネゲーズ</strong>',
     f'{dual("コロンバス・アビエイターズ", "Columbus Aviators")} @<br><strong>{dual("アーリントン・レネゲーズ", "Arlington Renegades")}</strong>'),
    # Row 4: Louisville
    ('ヒューストン・ギャンブラーズ vs<br><strong>ルイビル・キングス</strong>',
     f'{dual("ヒューストン・ギャンブラーズ", "Houston Gamblers")} vs<br><strong>{dual("ルイビル・キングス", "Louisville Kings")}</strong>'),
    # Row 5: Gauff
    ('サムソノワ L. vs<br><strong>ゴーフ C.</strong>',
     f'{dual("サムソノワ L.", "Samsonova L.")} vs<br><strong>{dual("ゴーフ C.", "Gauff C.")}</strong>'),
    # Row 6: Musetti (short names in HP table)
    ('ムテ C. vs<br><strong>ムセッティ L.</strong>',
     f'{dual("ムテ C.", "Moutet C.")} vs<br><strong>{dual("ムセッティ L.", "Musetti L.")}</strong>'),
    # Row 7: Paolini
    ('ソンメズ Z. vs<br><strong>パオリーニ J.(4)</strong>',
     f'{dual("ソンメズ Z.", "Sonmez Z.")} vs<br><strong>{dual("パオリーニ J.(4)", "Paolini J.(4)")}</strong>'),
    # Badges
    ('<span class="badge badge-go">シフィアテク</span>',
     f'<span class="badge badge-go">{dual("シフィアテク", "Swiatek")}</span>'),
    ('<span class="badge badge-go">アルカラス</span>',
     f'<span class="badge badge-go">{dual("アルカラス", "Alcaraz")}</span>'),
    ('<span class="badge badge-go">レネゲーズ</span>',
     f'<span class="badge badge-go">{dual("レネゲーズ", "Renegades")}</span>'),
    ('<span class="badge badge-go">ルイビル</span>',
     f'<span class="badge badge-go">{dual("ルイビル", "Louisville")}</span>'),
    ('<span class="badge badge-go">ゴーフ</span>',
     f'<span class="badge badge-go">{dual("ゴーフ", "Gauff")}</span>'),
    ('<span class="badge badge-go">ムセッティ</span>',
     f'<span class="badge badge-go">{dual("ムセッティ", "Musetti")}</span>'),
    ('<span class="badge badge-go">パオリーニ</span>',
     f'<span class="badge badge-go">{dual("パオリーニ", "Paolini")}</span>'),
]

# === マルチベット (UTF-8) ===
multi_pairs = [
    # タイトルスパン内
    ('ルイビル &times; レネゲーズ &times; ムセッティ（3試合）',
     f'{dual("ルイビル × レネゲーズ × ムセッティ", "Louisville × Renegades × Musetti")}（3試合）'),
    ('ルイビル &times; レネゲーズ &times; ムセッティ &times; アルカラス（4試合）',
     f'{dual("ルイビル × レネゲーズ × ムセッティ × アルカラス", "Louisville × Renegades × Musetti × Alcaraz")}（4試合）'),
    ('ルイビル &times; レネゲーズ &times; ムセッティ &times; パオリーニ（4試合）',
     f'{dual("ルイビル × レネゲーズ × ムセッティ × パオリーニ", "Louisville × Renegades × Musetti × Paolini")}（4試合）'),
    ('ルイビル &times; レネゲーズ &times; ムセッティ &times; アルカラス &times; パオリーニ（5試合）',
     f'{dual("ルイビル × レネゲーズ × ムセッティ × アルカラス × パオリーニ", "Louisville × Renegades × Musetti × Alcaraz × Paolini")}（5試合）'),
    ('ルイビル &times; レネゲーズ &times; ムセッティ &times; シフィアテク（4試合）',
     f'{dual("ルイビル × レネゲーズ × ムセッティ × シフィアテク", "Louisville × Renegades × Musetti × Swiatek")}（4試合）'),
    # 詳細行 (1位)
    ('ヒューストン vs <strong>ルイビル・キングス</strong> (UFL W4) &times; アビエイターズ @ <strong>レネゲーズ</strong> (UFL W4) &times; ムテ vs <strong>ムセッティ</strong> (バルセロナ R2)',
     f'{dual("ヒューストン", "Houston Gamblers")} vs <strong>{dual("ルイビル・キングス", "Louisville Kings")}</strong> (UFL W4) &times; {dual("アビエイターズ @", "Aviators @")} <strong>{dual("レネゲーズ", "Renegades")}</strong> (UFL W4) &times; {dual("ムテ", "Moutet")} vs <strong>{dual("ムセッティ", "Musetti")}</strong> (バルセロナ R2)'),
    # 2位 追加行
    ('+<strong>アルカラス</strong> (バルセロナ R2) 追加',
     f'+<strong>{dual("アルカラス", "Alcaraz")}</strong> (バルセロナ R2) 追加'),
    # 3位 追加行
    ('+<strong>パオリーニ</strong> (WTA シュトゥットガルト R2) 追加',
     f'+<strong>{dual("パオリーニ", "Paolini")}</strong> (WTA シュトゥットガルト R2) 追加'),
    # 4位 追加行
    ('+<strong>アルカラス</strong> &amp; <strong>パオリーニ</strong> 追加（5連複）',
     f'+<strong>{dual("アルカラス", "Alcaraz")}</strong> &amp; <strong>{dual("パオリーニ", "Paolini")}</strong> 追加（5連複）'),
    # 5位 追加行
    ('+<strong>シフィアテク</strong> (WTA シュトゥットガルト R2) 追加',
     f'+<strong>{dual("シフィアテク", "Swiatek")}</strong> (WTA シュトゥットガルト R2) 追加'),
]

all_pairs = ac_match_pairs + ac_rec_pairs + hp_match_pairs + multi_pairs
ok = 0
miss = 0
for old, new in all_pairs:
    if old in content:
        content = content.replace(old, new, 1)
        ok += 1
    else:
        print(f"MISS: {old[:70]}")
        miss += 1

print(f"名前置換: OK={ok}, MISS={miss}")

# ── 6. 保存 ──────────────────────────────────
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("dashboard.html saved.")
