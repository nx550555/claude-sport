# -*- coding: utf-8 -*-
"""Session _47 結果反映スクリプト
NHL PO R1 G1 残6試合 + NBA Play-in 2件 + NBA PO R1 G1 6件 の結果記入
一次ソース確認済: NHL.com / ESPN / CBS / NBA.com / Yahoo
"""
import json, sys
from pathlib import Path

ROOT = Path(r'C:\Users\ohwada\Desktop\claude_sport')

def load(p):
    with open(ROOT/p, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def save(p, d):
    with open(ROOT/p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# =========== NHL RECORDS UPDATE ===========
nhl = load('records/nhl/2025-26.json')

# series -> (result, score, prediction_hit, actual_date_jst, sources, notes)
NHL_G1 = {
    'PO_R1_E1': {  # BUF-BOS: predicted BUF -> BUF 4-3 BOS = HIT
        'result': 'Buffalo Sabres',
        'score': '4-3',
        'prediction_hit': True,
        'actual_date': '2026-04-20',
        'sources': [
            'NHL.com 2026 playoffs first round schedule results',
            'ESPN Stanley Cup Playoffs 2026 bracket'
        ],
        'outcome_note': 'BUF 4-3 BOS G1. 予測HIT (SKIP no-bet). L1 diff 2.66pp で skip 判断だが home +7% が効いた。BOS PDO 102 / Goals%>xGF% over-index (luck-driven) の PO regression 想定通り。'
    },
    'PO_R1_E3': {  # CAR-OTT: predicted CAR -> CAR 2-0 OTT = HIT
        'result': 'Carolina Hurricanes',
        'score': '2-0',
        'prediction_hit': True,
        'actual_date': '2026-04-21',
        'sources': [
            'NHL.com 2026 playoffs first round results',
            'ESPN bracket'
        ],
        'outcome_note': 'CAR 2-0 OTT G1 shutout. 予測HIT (SKIP no-bet). 両チーム elite xGF% だが home +7% と完封試合で CAR が優位を確実化。'
    },
    'PO_R1_E4': {  # PIT-PHI: predicted PIT -> PHI 3-2 PIT = MISS (A027)
        'result': 'Philadelphia Flyers',
        'score': '3-2',
        'prediction_hit': False,
        'actual_date': '2026-04-19',
        'type_a_upset_id': 'A027',
        'miss_layer': 'L4_External',
        'miss_analysis': 'PHI 3-2 PIT UPSET (Drysdale/Sanheim/Martone 各1G, Rust 2G PIT)。Konecny 1A, Crosby 0pt held off stat sheet。 L1 xGF% 0.40pp coin flip で SKIP 判断自体は妥当。home PIT +7% が外れた要因: (1) Crosby/Malkin veteran core が PHI young energy (Drysdale/Martone) に追いつかず、(2) RS 最終20G で PIT xGF% 低下傾向・PHI rivalry モチベーション、(3) Vladar (PHI G) の save work。P019 候補 evidence として適合。',
        'sources': [
            'ESPN gameId 401869717 Flyers 3-2 Penguins Apr 18 2026',
            'PensBurgh Penguins/Flyers Game 1 Recap sloppy-pens-bottled-up-lose-3-2',
            'Broad Street Hockey takeaways-flyers-snatch-game-1-in-gutsy-3-2-win'
        ],
        'outcome_note': 'PHI young energy outpaced PIT veteran core. Sloppy Pens bottled up.'
    },
    'PO_R1_W2': {  # DAL-MIN: predicted DAL -> MIN 6-1 DAL = MISS (A028)
        'result': 'Minnesota Wild',
        'score': '6-1',
        'prediction_hit': False,
        'actual_date': '2026-04-19',
        'type_a_upset_id': 'A028',
        'miss_layer': 'L1_xGF',
        'miss_analysis': 'MIN 6-1 DAL BLOWOUT UPSET (seed upset: C3 > C2 home). L1 xGF% では MIN 51.50% が DAL 50.79% より 0.71pp 高く、lower seed だが process で上回っていた (type_a_watch に記録済み)。home DAL +7% を MIN の圧倒的攻勢が覆した: Kaprizov 1G2A, Boldy 1G1A, Eriksson Ek 2G (PP), Zuccarello 3A, Hartman 1G + PA to Kaprizov。前半6分半で 4-0 lead, Oettinger 23 saves. Wallstedt (MIN) 27 saves Playoff debut。→ "seed順位よりxGF%順位を優先すべし" 教訓。L1ラベル「SKIP」自体は妥当だが predicted_winner を DAL にしたのが誤り（L1 higher xGF% team = MIN を予測すべき）。',
        'sources': [
            'ESPN gameId 401869716 Wild 6-1 Stars Apr 18 2026',
            'NHL.com wild news minnesota-wild-dallas-stars-game-1-recap',
            'The Hockey Writers 3-takeaways-from-stars-stunning-6-1-loss'
        ],
        'outcome_note': 'MIN 6-1 blowout. Kaprizov+Boldy 40G teammates explosion. Wallstedt PO debut 27sv. type_a_watch が事前に示唆していた seed vs xGF% の矛盾が顕在化。'
    },
    'PO_R1_W3': {  # VGK-UTA: predicted VGK -> VGK 4-2 UTA = HIT
        'result': 'Vegas Golden Knights',
        'score': '4-2',
        'prediction_hit': True,
        'actual_date': '2026-04-21',
        'sources': [
            'NHL.com 2026 playoffs first round results',
            'ESPN bracket'
        ],
        'outcome_note': 'VGK 4-2 UTA G1. 予測HIT (SKIP no-bet, conf 56%)。home +7% が効いた。UTA P1 seed 挑戦成らず。'
    },
    'PO_R1_W4': {  # EDM-ANA: predicted EDM -> EDM 4-3 ANA = HIT
        'result': 'Edmonton Oilers',
        'score': '4-3',
        'prediction_hit': True,
        'actual_date': '2026-04-21',
        'sources': [
            'ESPN gameId 401869722 Oilers 4-3 Ducks Apr 20 2026',
            'NHL.com anaheim-ducks-edmonton-oilers-game-1-recap-april-20-2026',
            'FOX Sports nhl playoffs round 1 game 1 boxscore'
        ],
        'outcome_note': 'EDM 4-3 ANA G1 (Kapanen 2G incl. late winner 1:54 remaining 3rd, Dickinson 2G)。予測HIT (SKIP no-bet, conf 51%)。type_a_watch が ANA xGF% marginally higher を警戒していたが home +7% + McDavid/Draisaitl impact で EDM 逃げ切り。late rally で決着: 3rd period まで僅差 → Kapanen 2nd goal が decisive。'
    }
}

count_nhl = 0
for i, g in enumerate(nhl.get('games', nhl) if isinstance(nhl, dict) else nhl):
    if not isinstance(g, dict): continue
    s = g.get('series')
    if s in NHL_G1 and g.get('result') in (None, ''):
        upd = NHL_G1[s]
        for k, v in upd.items():
            g[k] = v
        # hit field: rec がない SKIP/CAUTION なら null のまま
        # rec があるシリーズは CAUTION の TBL だけ(既に処理済)
        count_nhl += 1
        print(f'NHL updated: {s} -> {upd["result"]} {upd["score"]}')

save('records/nhl/2025-26.json', nhl)
print(f'[OK] NHL records updated: {count_nhl} games\n')

# =========== NBA RECORDS UPDATE ===========
nba = load('records/nba/2025-26.json')

# Match-based lookup (since NBA records has multiple structures)
NBA_UPDATES = {
    # Play-in (4/17 ET = 4/18 JST)
    'NBA-004': {  # CHA vs ORL predicted CHA -> ORL 121-90 CHA = MISS
        'result': 'Orlando Magic',
        'score': 'ORL 121-90 CHA',
        'prediction_hit': False,
        'actual_date': '2026-04-18',
        'miss_layer': 'L1_NRtg_small_edge',
        'miss_analysis': 'Play-in East Final: ORL 121-90 CHA blowout。予測CHA(L1 NRtg diff 4.2pt) が外れ: (1) ORL が Banchero/Wagner breakout で圧倒、(2) Play-in は RS平均よりプレーオフモチベ・チーム集中度が効く試合構造。L1 NRtg差が4-5pt 以下の場合、Play-inゲームで home-court意識より個人ブレイクアウト依存度が高い可能性。',
        'round_correction': 'Play-in Final (East 9v10). records 上は "4/18" だが ET 4/17 Fri 開催。',
        'sources': [
            'NBA.com recap 2026 sofi play-in magic suns earn eight seeds',
            'Yahoo Sports hornets magic warriors suns wrap-up play-in'
        ],
        'outcome_note': 'ORL earned 8 seed to face DET R1 (later UPSET G1 A026)。'
    },
    'NBA-005': {  # PHX vs GSW predicted PHX -> PHX 111-96 GSW = HIT
        'result': 'Phoenix Suns',
        'score': 'PHX 111-96 GSW',
        'prediction_hit': True,
        'actual_date': '2026-04-18',
        'round_correction': 'Play-in Final (West 9v10). records 上は "4/18" だが ET 4/17 Fri 開催。',
        'sources': [
            'NBA.com suns-warriors-play-in-recap Jalen Green 36pts',
            'Yahoo nba play-in 2026 suns emphatically end warriors'
        ],
        'outcome_note': 'PHX 111-96 GSW. Jalen Green 36pts led all scorers. PHX earned 8 seed to face OKC R1 (後に G1 119-84 OKC blowout HIT)。'
    },
    # NBA PO R1 G1 (by date + match text match)
    'NBA-007': {  # DEN vs MIN (4/19) predicted DEN -> DEN 116-105 MIN = HIT
        'result': 'Denver Nuggets',
        'score': 'DEN 116-105 MIN',
        'prediction_hit': True,
        'actual_date': '2026-04-19',
        'sources': [
            'NBA.com live-updates-2026-nba-playoffs-r1 hawks-timberwolves',
            'ESPN nba playoffs 2026 western conference first-round takeaways'
        ],
        'outcome_note': 'DEN 116-105 MIN G1. 予測HIT (SKIP: conf 52% / EV -4.5%)。NRtg 差小さく coin flip でも home DEN 逃げ切り。'
    },
    'NBA-008': {  # NYK vs ATL (4/19) predicted NYK -> NYK 112-102 ATL = HIT
        'result': 'New York Knicks',
        'score': 'NYK 112-102 ATL',
        'prediction_hit': True,
        'actual_date': '2026-04-19',
        'sources': [
            'NBA.com live-updates-2026-nba-playoffs-r1 cavaliers knicks',
            'ESPN NBA 2026 playoffs bracket'
        ],
        'outcome_note': 'NYK 112-102 ATL G1. 予測HIT (SKIP: conf 57% / EV -4.4%)。10pt差は NYK NRtg優位と home +2-3% のみで達成。'
    },
    'NBA-009': {  # LAL vs HOU (4/18) predicted HOU -> LAL 107-98 HOU = MISS (A029)
        'result': 'Los Angeles Lakers',
        'score': 'LAL 107-98 HOU',
        'prediction_hit': False,
        'actual_date': '2026-04-18',
        'date_correction': 'ET 4/18 Sat (records 記載 4/19 を修正)。Crypto.com Arena LA。',
        'type_a_upset_id': 'A029',
        'miss_layer': 'L4_External',
        'miss_analysis': '**LAL 107-98 HOU UPSET (A029新規登録候補)**。L4要因が絶対的: Kevin Durant (HOU) G1 欠場 (right knee contusion/patellar tendon deep bruise, 火曜日の練習で負傷, ESPN/CBS/Yahoo複数確認)。Durant RS 26.0ppg の絶対主力欠場で HOU は "shell of itself" (CBS)。LAL は short-handed でも Luke Kennard playoff career-high 27pts 爆発。L1 NRtg 3.5pt 差は HOU の Durant 前提値、Durant 欠場で NRtg 実質 -3〜-4pt 下方修正すべきだった。pre-game warmup で ruled out 確認情報は game-day dailyfaceoff 相当の NBA injury report で取得可能だった。',
        'sources': [
            'ESPN gameId 401869190 Lakers 107-98 Rockets Apr 18 2026',
            'ESPN rockets kevin-durant-g1-vs-lakers-knee-contusion',
            'NBA.com rockets-lakers-2026-playoffs-game-1-takeaways Kennard monster',
            'CBS Sports kevin-durant-injury-rockets-lakers-nba-playoffs'
        ],
        'outcome_note': 'KD G1 absence決定的。Udoka "nothing major", G2 game-time decision。ルール化候補: NBA PO G1 star scorer (>25ppg RS) 欠場時の -8〜-10% 補正。'
    },
    'NBA-010': {  # BOS vs PHI (4/20) predicted BOS -> BOS 123-91 PHI = HIT
        'result': 'Boston Celtics',
        'score': 'BOS 123-91 PHI',
        'prediction_hit': True,
        'actual_date': '2026-04-20',
        'sources': [
            'NBA.com 76ers-celtics-2026-playoffs-game-1-takeaways',
            'CBS Sports 2026 nba playoff bracket'
        ],
        'outcome_note': 'BOS 123-91 PHI G1 (+32 margin, franchise PO opener record)。Tatum 25/11/7, Brown 26pts。予測HIT but SKIP (EV -1.7%@1.13)。L1 NRtg 8.5pt diff + Embiid OUT が予測通りblowout。'
    }
}

# Apply by id
count_nba = 0
nba_games = nba.get('games', nba if isinstance(nba, list) else [])
for g in nba_games:
    if not isinstance(g, dict): continue
    gid = g.get('id')
    if gid in NBA_UPDATES and g.get('result') in (None, ''):
        upd = NBA_UPDATES[gid]
        for k, v in upd.items():
            g[k] = v
        count_nba += 1
        print(f'NBA updated: {gid} -> {upd["result"]} {upd["score"]}')

# Also update the pending G1 entries by match text (line 518+)
G1_MATCH_UPDATES = {
    'Cleveland Cavaliers vs Toronto Raptors (G1 R1)': {
        'result': 'Cleveland Cavaliers',
        'score': 'CLE 126-113 TOR',
        'prediction_hit': True,
        'actual_date': '2026-04-18',
        'outcome_note': 'CLE 126-113 TOR G1 HIT (Session_45 既確認)。',
        'status': 'completed'
    },
    'New York Knicks vs Atlanta Hawks (G1 R1)': {
        'result': 'New York Knicks',
        'score': 'NYK 112-102 ATL',
        'prediction_hit': True,
        'actual_date': '2026-04-19',
        'outcome_note': 'NYK 112-102 ATL G1 HIT。',
        'status': 'completed'
    },
    'Denver Nuggets vs Minnesota Timberwolves (G1 R1)': {
        'result': 'Denver Nuggets',
        'score': 'DEN 116-105 MIN',
        'prediction_hit': True,
        'actual_date': '2026-04-19',
        'outcome_note': 'DEN 116-105 MIN G1 HIT。',
        'status': 'completed'
    },
    'Los Angeles Lakers @ Houston Rockets (G1 R1)': {
        'result': 'Los Angeles Lakers',
        'score': 'LAL 107-98 HOU',
        'prediction_hit': False,
        'actual_date': '2026-04-18',
        'type_a_upset_id': 'A029',
        'miss_layer': 'L4_External',
        'outcome_note': 'HOU UPSET MISS。KD G1 欠場 (patellar tendon contusion)。A029登録。',
        'status': 'completed'
    },
    'Boston Celtics vs Philadelphia 76ers (G1 R1)': {
        'result': 'Boston Celtics',
        'score': 'BOS 123-91 PHI',
        'prediction_hit': True,
        'actual_date': '2026-04-20',
        'outcome_note': 'BOS 123-91 PHI G1 HIT (+32 blowout)。',
        'status': 'completed'
    },
    'Oklahoma City Thunder vs Phoenix Suns (G1 R1)': {
        'result': 'Oklahoma City Thunder',
        'score': 'OKC 119-84 PHX',
        'prediction_hit': True,
        'actual_date': '2026-04-19',
        'outcome_note': 'OKC 119-84 PHX G1 HIT (+35 blowout, #1 seed dominance)。',
        'status': 'completed'
    },
    'Detroit Pistons vs Orlando Magic (RS live)': {
        'result': 'Orlando Magic',
        'score': 'ORL 112-101 DET',
        'prediction_hit': False,
        'actual_date': '2026-04-19',
        'type_a_upset_id': 'A026',
        'miss_layer': 'L4_External',
        'outcome_note': 'ORL UPSET (A026既登録)。',
        'status': 'completed'
    }
}

for g in nba_games:
    if not isinstance(g, dict): continue
    m = g.get('match','')
    if m in G1_MATCH_UPDATES and g.get('result') in (None, ''):
        upd = G1_MATCH_UPDATES[m]
        for k, v in upd.items():
            g[k] = v
        count_nba += 1
        print(f'NBA G1-entry updated: {m[:50]} -> {upd["result"]}')

save('records/nba/2025-26.json', nba)
print(f'[OK] NBA records updated: {count_nba} games\n')

print('=== Session _47 result reflection complete ===')
