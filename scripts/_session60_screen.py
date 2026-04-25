"""Session_60 一括スクリーニング: MLB + NRL R9"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from stats_feed_reader import get_mlb_all_teams, get_league_standings

BASE = Path(__file__).parent.parent

MLB_JP2EN = {
    "ボルチモア・オリオールズ":"Baltimore Orioles","ボストン・レッドソックス":"Boston Red Sox",
    "セントルイス・カージナルス":"St. Louis Cardinals","シアトル・マリナーズ":"Seattle Mariners",
    "トロント・ブルージェイズ":"Toronto Blue Jays","クリーブランド ガーディアンズ":"Cleveland Guardians",
    "サンフランシスコ・ジャイアンツ":"San Francisco Giants","マイアミ・マーリンス":"Miami Marlins",
    "シカゴ・ホワイトソックス":"Chicago White Sox","ワシントンナショナルス":"Washington Nationals",
    "ニューヨーク・メッツ":"New York Mets","コロラドロッキーズ":"Colorado Rockies",
    "タンパベイ・レイズ":"Tampa Bay Rays","ミネソタ・ツインズ":"Minnesota Twins",
    "アリゾナダイアモンドバックス":"Arizona Diamondbacks","サンディエゴ・パドレス":"San Diego Padres",
    "テキサス・レンジャーズ":"Texas Rangers","アスレティックス":"Athletics",
    "ヒューストンアストロズ":"Houston Astros","ニューヨーク・ヤンキース":"New York Yankees",
    "カンザスシティ・ロイヤルズ":"Kansas City Royals","ロサンゼルス・エンゼルス":"Los Angeles Angels",
    "ミルウォーキー・ブリュワーズ":"Milwaukee Brewers","ピッツバーグ・パイレーツ":"Pittsburgh Pirates",
    "シンシナティ・レッズ":"Cincinnati Reds","デトロイトタイガース":"Detroit Tigers",
    "ロサンゼルス・ドジャース":"Los Angeles Dodgers","シカゴ・カブス":"Chicago Cubs",
    "アトランタ・ブレーブ":"Atlanta Braves","フィラデルフィア・フィリーズ":"Philadelphia Phillies",
}
MLB_TEAMS = {t["team"]: t for t in (get_mlb_all_teams() or [])}

def mlb_find(jp):
    en = MLB_JP2EN.get(jp)
    if en in MLB_TEAMS: return en, MLB_TEAMS[en]
    if en:
        for k in MLB_TEAMS:
            if en.split()[-1] in k or k.split()[-1] in en:
                return k, MLB_TEAMS[k]
    return en, None

NRL_JP2EN = {
    "ニューキャッスル・ナイツ":"Newcastle Knights","ペンリス・パンサーズ":"Penrith Panthers",
    "マンリー・シ―イーグルス":"Manly Sea Eagles","パラマッタ・イールズ":"Parramatta Eels",
    "カンタベリー・ブルドックス":"Canterbury Bulldogs","ノースクイーンズランド・カウボーイズ":"North Queensland Cowboys",
    "Dolphins (Nrl)":"Dolphins","メルボルン・ストーム":"Melbourne Storm",
    "ゴールドコースト・タイタンズ":"Gold Coast Titans","キャンベラ・ライダース":"Canberra Raiders",
    "ニュージランド・ウォリアーズ":"New Zealand Warriors","シドニー・ルースターズ":"Sydney Roosters",
    "ブリスベン・ブロンコス":"Brisbane Broncos","サウス・シドニー・ラビトス":"South Sydney Rabbitohs",
}

nrl_standings_data = get_league_standings("NRL")
print(f"NRL standings raw type: {type(nrl_standings_data)}")
if isinstance(nrl_standings_data, dict):
    nrl_standings = nrl_standings_data.get("teams", []) or []
elif isinstance(nrl_standings_data, list):
    nrl_standings = nrl_standings_data
else:
    nrl_standings = []
print(f"NRL standings: {len(nrl_standings)}")
if nrl_standings:
    print(f"  sample: {nrl_standings[0]}")

NRL_TEAMS = {}
for t in nrl_standings:
    nm = t.get("team_name") or t.get("team") or t.get("name") or ""
    if nm: NRL_TEAMS[nm] = t

# 短縮形 → 長い名前マッピング (NRL standings は "Panthers" のような短縮表記)
NRL_SHORT2FULL = {
    "Panthers":"Penrith Panthers","Knights":"Newcastle Knights","Sea Eagles":"Manly Sea Eagles",
    "Eels":"Parramatta Eels","Bulldogs":"Canterbury Bulldogs","Cowboys":"North Queensland Cowboys",
    "Dolphins":"Dolphins","Storm":"Melbourne Storm","Titans":"Gold Coast Titans","Raiders":"Canberra Raiders",
    "Warriors":"New Zealand Warriors","Roosters":"Sydney Roosters","Broncos":"Brisbane Broncos",
    "Rabbitohs":"South Sydney Rabbitohs","Sharks":"Cronulla Sharks","Tigers":"Wests Tigers","Dragons":"St George Dragons",
}

def nrl_find(jp):
    en = NRL_JP2EN.get(jp)
    if not en: return None, None
    # try NRL_TEAMS direct
    if en in NRL_TEAMS: return en, NRL_TEAMS[en]
    # try short form match
    for short, full in NRL_SHORT2FULL.items():
        if full == en and short in NRL_TEAMS:
            return en, NRL_TEAMS[short]
    # try fuzzy
    for k in NRL_TEAMS:
        if k in en or en.split()[-1] == k:
            return en, NRL_TEAMS[k]
    return en, None

data = json.load(open(BASE / "手動試合データ/2026-04-25.json", encoding="utf-8-sig"))

# === MLB ===
mlb_results = []
for tour in data["tournaments"]:
    if tour["tournament"] != "メジャーリーグベースボール": continue
    for status in ["upcoming", "live"]:
        for m in tour["matches"].get(status, []):
            t1_jp = m.get("team1"); t2_jp = m.get("team2")
            odds = m.get("odds", {})
            o1 = odds.get("team1"); o2 = odds.get("team2")
            if not (t1_jp and t2_jp and o1 and o2): continue
            t1_en, td1 = mlb_find(t1_jp)
            t2_en, td2 = mlb_find(t2_jp)
            tier = "skip"; conf = None; ev = None; pred = None; note = ""
            if td1 and td2:
                wrc1, wrc2 = td1["wRC_plus"], td2["wRC_plus"]
                fip1, fip2 = td1["FIP"], td2["FIP"]
                wrc_diff = round(wrc1 - wrc2, 1)
                fip_diff = round(fip1 - fip2, 2)
                ip1, ip2 = 1/o1, 1/o2
                tot = ip1 + ip2
                mp_h = ip1 / tot
                shift = (wrc_diff/10) * 0.03 + (-fip_diff/0.4) * 0.03 + 0.03
                est_h = max(0.05, min(0.95, mp_h + shift))
                est_a = 1 - est_h
                if est_h >= est_a:
                    pred = t1_en; conf = round(est_h*100, 1); ev = round(est_h*o1 - 1, 3)
                else:
                    pred = t2_en; conf = round(est_a*100, 1); ev = round(est_a*o2 - 1, 3)
                strong_l1 = abs(wrc_diff) >= 10 or abs(fip_diff) >= 0.4
                if conf >= 75 and ev >= 0.05:
                    tier = "caution_waiting_sp"
                elif conf >= 65 and ev >= 0.05:
                    tier = "caution_margin"
                else:
                    tier = "skip"
                note = f"wRC+ {wrc1:.1f} vs {wrc2:.1f} (diff {wrc_diff:+.1f}) | FIP {fip1:.2f} vs {fip2:.2f} (diff {fip_diff:+.2f}) | L1={'PASS' if strong_l1 else 'fail'} | proxy: wRC+/FIP both"
            else:
                note = f"team_data missing"
                tier = "skip_data_missing"
            mlb_results.append({
                "league":"MLB","match_jp":f"{t1_jp} vs {t2_jp}",
                "match_en":f"{t1_en or t1_jp} vs {t2_en or t2_jp}",
                "date": m.get("date","2026-04-25"),"start": m.get("start_time",""),
                "home_odds":o1,"away_odds":o2,
                "predicted_winner":pred,"conf":conf,"ev":ev,"tier":tier,"note":note
            })

print(f"\n=== MLB screening: {len(mlb_results)} games ===")
notable = [r for r in mlb_results if r["tier"] not in ("skip","skip_data_missing")]
print(f"Notable: {len(notable)}")
for r in notable:
    print(f"  [{r['tier']}] {r['match_en']} | conf={r['conf']}% EV={r['ev']:+.1%}")
    print(f"      {r['note']}")
print(f"--- Skip ({len([r for r in mlb_results if r['tier']=='skip'])}) ---")
for r in [r for r in mlb_results if r['tier']=='skip']:
    print(f"  {r['match_en']} | conf={r['conf']} EV={r['ev']:+.2f}")

json.dump(mlb_results, open(BASE / "stats/_screening_mlb_2026-04-25.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# === NRL R9 ===
nrl_results = []
for tour in data["tournaments"]:
    if tour["tournament"] != "NRL": continue
    for status in ["upcoming", "live"]:
        for m in tour["matches"].get(status, []):
            t1_jp = m.get("team1"); t2_jp = m.get("team2")
            odds = m.get("odds", {})
            o1 = odds.get("team1"); o2 = odds.get("team2")
            if not (t1_jp and t2_jp and o1 and o2): continue
            t1_en, td1 = nrl_find(t1_jp)
            t2_en, td2 = nrl_find(t2_jp)
            tier = "skip"; conf = None; ev = None; pred = None; note = ""
            if td1 and td2:
                pdg1 = float(td1.get("pd_per_game", 0) or 0)
                pdg2 = float(td2.get("pd_per_game", 0) or 0)
                if not pdg1 and not pdg2:
                    pf1 = float(td1.get("pf", td1.get("points_for", 0)) or 0)
                    pa1 = float(td1.get("pa", td1.get("points_against", 0)) or 0)
                    gp1 = float(td1.get("gp", td1.get("games_played", 1)) or 1)
                    pf2 = float(td2.get("pf", td2.get("points_for", 0)) or 0)
                    pa2 = float(td2.get("pa", td2.get("points_against", 0)) or 0)
                    gp2 = float(td2.get("gp", td2.get("games_played", 1)) or 1)
                    pdg1 = (pf1 - pa1)/gp1 if gp1 > 0 else 0
                    pdg2 = (pf2 - pa2)/gp2 if gp2 > 0 else 0
                pdg_diff = round(pdg1 - pdg2, 2)
                ip1, ip2 = 1/o1, 1/o2
                tot = ip1 + ip2
                mp_h = ip1/tot
                shift = max(-0.18, min(0.18, pdg_diff*0.012)) + 0.03
                est_h = max(0.05, min(0.95, mp_h + shift))
                est_a = 1 - est_h
                if est_h >= est_a:
                    pred = t1_en; conf = round(est_h*100,1); ev = round(est_h*o1 - 1, 3)
                else:
                    pred = t2_en; conf = round(est_a*100,1); ev = round(est_a*o2 - 1, 3)
                if conf >= 78 and ev >= 0.07:
                    tier = "provisional_go"
                elif conf >= 70 and ev >= 0.05:
                    tier = "caution_margin"
                else:
                    tier = "skip"
                note = f"PD/G {pdg1:+.2f} vs {pdg2:+.2f} (diff {pdg_diff:+.2f})"
            else:
                note = f"team_data missing: {t1_jp}/{t2_jp}"
                tier = "skip_data_missing"
            nrl_results.append({
                "league":"NRL","match_jp":f"{t1_jp} vs {t2_jp}",
                "match_en":f"{t1_en or t1_jp} vs {t2_en or t2_jp}",
                "date": m.get("date","2026-04-25"),"start": m.get("start_time",""),
                "home_odds":o1,"away_odds":o2,
                "predicted_winner":pred,"conf":conf,"ev":ev,"tier":tier,"note":note
            })

print(f"\n=== NRL R9 screening: {len(nrl_results)} games ===")
for r in nrl_results:
    print(f"  [{r['tier']}] {r['match_en']} ({r['date']}) | conf={r['conf']}% EV={r['ev']}")
    print(f"      {r['note']}")
json.dump(nrl_results, open(BASE / "stats/_screening_nrl_2026-04-25.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("\n=== SUMMARY ===")
print(f"  Soccer: 35 games (4 provisional_go + 3 caution_margin + 28 skip)")
print(f"  MLB:    {len(mlb_results)} games ({len(notable)} notable + {len([r for r in mlb_results if r['tier']=='skip'])} skip + {len([r for r in mlb_results if r['tier']=='skip_data_missing'])} missing)")
print(f"  NRL:    {len(nrl_results)} games ({len([r for r in nrl_results if r['tier'] not in ('skip','skip_data_missing')])} notable + {len([r for r in nrl_results if r['tier']=='skip'])} skip + {len([r for r in nrl_results if r['tier']=='skip_data_missing'])} missing)")
