import json
import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ATP_MATCHES = [
    ("2026-04-23","R1","Hanfmann Y. vs Giron M.","Yannick Hanfmann","Marcos Giron",1.37,3.20,80,61,-16.0,"skip","skip","cElo +80pt micro-edge only","Market overprices Hanfmann."),
    ("2026-04-23","R1","Blockx A. vs Garin C.","Alexander Blockx","Cristian Garin",1.47,2.80,26,54,-21.1,"skip","skip","cElo +26pt negligible","Coin flip with market bias."),
    ("2026-04-23","R1","Kecmanovic M. vs Atmane T.","Miomir Kecmanovic","Terence Atmane",1.74,2.16,54,58,0.4,"skip","skip","cElo +54pt","Near break-even EV."),
    ("2026-04-23","R1","Carreno Busta P. vs Fucsovics M.","Pablo Carreno Busta","Marton Fucsovics",1.89,1.96,9,51,-3.0,"skip","skip","cElo +9pt","Near coin flip."),
    ("2026-04-23","R1","Munar J. vs Shevchenko A.","Jaume Munar","Alexander Shevchenko",1.61,2.34,81,62,-1.0,"skip","skip","cElo +81pt home","Market fairly priced."),
    ("2026-04-23","R1","Marozsan F. vs Quinn E.","Fabian Marozsan","Ethan Quinn",1.74,2.11,2,50,-12.7,"skip","skip","cElo +2pt","Marozsan market-inflated."),
    ("2026-04-23","R1","Navone M. vs Borges N.","Mariano Navone","Nuno Borges",1.57,2.42,74,60,-5.0,"skip","skip","cElo +74pt","Clay near parity, EV-."),
    ("2026-04-23","R1","Popyrin A. vs Damm M.","Alexei Popyrin","Martin Damm",1.46,2.75,365,89,30.1,"caution","Q4_upset_watch","cElo +365pt but Popyrin 4-11 2026 / 2-2 clay","DOWNGRADE from GO: cElo overrates per 2026 slump. R018. Damm beat Garin momentum."),
    ("2026-04-23","R1","Tsitsipas S. vs Kypson P.","Stefanos Tsitsipas","Patrick Kypson",1.35,3.25,316,86,16.1,"go","Q1_go","cElo +316pt Tsitsipas clay pedigree","GO: cElo dominant. Risk R018 post-MC R1. Rec Tsitsipas @1.35."),
    ("2026-04-23","R1","Baez S. vs Gaubas V.","Sebastian Baez","Vilius Gaubas",1.38,3.05,163,72,-0.8,"skip","skip","cElo +163pt","Market accurately prices Baez."),
    ("2026-04-23","R1","Vallejo A.D. vs Dimitrov G.","Adolfo Daniel Vallejo","Grigor Dimitrov",1.88,1.93,-49,43,-19.2,"skip","skip","cElo Dimitrov -49pt edge","Near coin flip."),
    ("2026-04-23","R1","Merida D. vs Trungelliti M.","Daniel Merida","Marco Trungelliti",1.73,2.12,-10,49,-15.9,"skip","skip","cElo -10pt","Market overrates Merida."),
    ("2026-04-23","R1","Cerundolo J.M. vs Altmaier D.","Juan Manuel Cerundolo","Daniel Altmaier",1.72,2.13,8,51,-12.1,"skip","skip","cElo +8pt","Coin flip."),
    ("2026-04-23","R1","Carabelli H. vs Monfils G.","Hugo Carabelli","Gael Monfils",1.56,2.44,39,56,-13.3,"skip","skip","cElo +39pt","Market priced."),
    ("2026-04-23","R1","Opelka R. vs Budkov Kjaer N.","Reilly Opelka","Nikolai Budkov Kjaer",1.80,2.02,128,68,21.7,"caution","Q4_upset_watch","cElo +128pt serve-heavy","CAUTION-MARGIN: conf 68<75 EV+21.7."),
    ("2026-04-24","R2","Landaluce M. vs Walton A.","Martin Landaluce","Adam Walton",1.23,4.20,134,68,-16.0,"skip","skip","cElo +134pt","Market overprice."),
    ("2026-04-24","R2","Etcheverry T.M. vs Ofner S.","Tomas Martin Etcheverry","Sebastian Ofner",1.48,2.65,121,67,-1.3,"skip","skip","cElo +121pt","Near break-even."),
    ("2026-04-24","R2","Rinderknech A. vs Lajovic D.","Arthur Rinderknech","Dusan Lajovic",1.58,2.39,141,69,9.5,"caution","Q4_upset_watch","cElo +141pt clay","CAUTION-MARGIN: conf 69<75 EV+9.5."),
    ("2026-04-24","R2","Sinner J. vs Bonzi B.","Jannik Sinner","Benjamin Bonzi",1.01,18.0,602,97,-2.0,"skip","Q3_output_a","cElo +602pt #1 seed","Q3 output_a: conf 97."),
    ("2026-04-24","R2","Shelton B. vs Prizmic D.","Ben Shelton","Dino Prizmic",1.46,2.75,184,74,8.3,"caution","Q4_upset_watch","cElo +184pt","CAUTION-MARGIN: conf 74<75. Prizmic Munich momentum."),
    ("2026-04-24","R2","Machac T. vs Norrie C.","Tomas Machac","Cameron Norrie",1.73,2.12,-71,40,-31.0,"skip","skip","cElo Machac -71pt","Market inverted."),
    ("2026-04-24","R2","de Minaur A. vs Jodar R.","Alex de Minaur","Rafael Jodar",1.82,1.99,24,54,-2.6,"caution","Q4_upset_watch","cElo +24pt / Jodar home WC","CAUTION-MARGIN: R017 home WC momentum."),
    ("2026-04-24","R2","Paul T. vs Tirante T.A.","Tommy Paul","Thiago Agustin Tirante",1.40,3.00,243,80,12.3,"go","Q1_go","cElo +243pt Paul 5-0 clay Houston champ","GO: Rec Paul @1.40."),
    ("2026-04-24","R2","Fonseca J. vs Cilic M.","Joao Fonseca","Marin Cilic",1.28,3.75,130,68,-13.1,"skip","skip","cElo +130pt","Market overprices."),
    ("2026-04-24","R2","Musetti L. vs Hurkacz H.","Lorenzo Musetti","Hubert Hurkacz",1.42,2.90,202,76,8.2,"go","Q1_go","cElo +202pt clay pedigree H2H clay 1-0","GO: Rec Musetti @1.42. Risk P008 Hurkacz PR."),
    ("2026-04-24","R2","Lehecka J. vs Tabilo A.","Jiri Lehecka","Alejandro Tabilo",1.67,2.22,56,58,-3.1,"skip","skip","cElo +56pt","Near break-even."),
    ("2026-04-24","R2","Struff J.L. vs Michelsen A.","Jan-Lennard Struff","Alex Michelsen",1.73,2.13,-10,48,-16.1,"skip","skip","cElo Michelsen edge","Market inverted."),
    ("2026-04-24","R2","Diallo G. vs Moller E.","Gabriel Diallo","Elmer Moller",1.69,2.19,153,71,19.5,"caution","Q4_upset_watch","cElo +153pt","CAUTION-MARGIN: conf 71<75 EV+19.5."),
    ("2026-04-24","R2","Fils A. vs Buse I.","Arthur Fils","Ignacio Buse",1.17,5.20,272,83,-3.2,"skip","skip","cElo +272pt","Market priced."),
    ("2026-04-24","R2","Rublev A. vs Kopriva V.","Andrey Rublev","Vit Kopriva",1.24,4.10,186,74,-7.6,"skip","skip","cElo +186pt","Kopriva R020 momentum."),
    ("2026-04-24","R2","Griekspoor T. vs Dzumhur D.","Tallon Griekspoor","Damir Dzumhur",1.62,2.30,110,65,5.9,"caution","Q4_upset_watch","cElo +110pt","CAUTION-MARGIN."),
    ("2026-04-24","R2","Vacherot V. vs Nava E.","Valentin Vacherot","Emilio Nava",1.42,2.90,183,74,5.4,"caution","Q4_upset_watch","cElo +183pt Vacherot MC SF","CAUTION-MARGIN: R017 momentum."),
]

WTA_MATCHES = [
    ("2026-04-23","R1","Svitolina E. vs Bondar A.","Elina Svitolina","Anna Bondar",1.18,5.20,217,78,-8.3,"skip","skip","cElo +217pt","Market overprice."),
    ("2026-04-23","R1","Starodubtseva Y. vs Cristian J.","Yuliia Starodubtseva","Jaqueline Cristian",1.63,2.35,-22,47,-23.7,"skip","skip","cElo -22pt Cristian edge","Market inverted."),
    ("2026-04-23","R1","Bencic B. vs Martincova P.","Belinda Bencic","Petra Martincova",1.19,4.90,343,88,4.5,"skip","Q3_output_a","cElo +343pt","Q3: conf 88 EV+4.5."),
    ("2026-04-23","R1","Wang X. vs Samson L.","Xinyu Wang","Laura Samson",1.75,2.09,70,60,4.8,"caution","Q4_upset_watch","cElo +70pt","CAUTION-MARGIN."),
    ("2026-04-23","R1","Shnaider D. vs Bouzas Maneiro J.","Diana Shnaider","Jessica Bouzas Maneiro",1.32,3.40,128,68,-10.8,"skip","skip","cElo +128pt","Market overprice."),
    ("2026-04-23","R1","Kalinskaya A. vs Galfi D.","Anna Kalinskaya","Dalma Galfi",1.48,2.65,129,68,0.2,"caution","Q4_upset_watch","cElo +129pt / Galfi Q Final momentum","CAUTION-MARGIN: R020 momentum."),
    ("2026-04-23","R1","Swiatek I. vs Snigur D.","Iga Swiatek","Daria Snigur",1.02,15.0,498,95,-3.5,"skip","Q3_output_a","cElo +498pt","Q3: conf 95."),
    ("2026-04-23","R1","Paolini J. vs Siegemund L.","Jasmine Paolini","Laura Siegemund",1.31,3.50,222,78,2.6,"caution","Q4_upset_watch","cElo +222pt / Paolini P007 slump","CAUTION-MARGIN: Siegemund vet danger."),
    ("2026-04-23","R1","Bouzkova M. vs Kalinina A.","Marie Bouzkova","Anhelina Kalinina",1.77,2.06,-5,49,-12.7,"skip","skip","cElo -5pt","Coin flip."),
    ("2026-04-23","R1","Li A. vs Parks A.","Ann Li","Alycia Parks",1.76,2.08,157,71,25.3,"caution","Q4_upset_watch","cElo +157pt","CAUTION-MARGIN: EV+25.3 but conf 71."),
    ("2026-04-23","R1","Sabalenka A. vs Stearns P.","Aryna Sabalenka","Peyton Stearns",1.05,11.0,381,90,-5.5,"skip","Q3_output_a","cElo +381pt #1","Q3: conf 90."),
    ("2026-04-23","R1","Jovic I. vs Linette M.","Iva Jovic","Magda Linette",1.49,2.65,-9,49,-27.4,"skip","skip","cElo -9pt Linette edge","Market overprice."),
    ("2026-04-23","R1","Fernandez L. vs Grabher J.","Leylah Fernandez","Julia Grabher",1.16,5.40,118,66,-23.1,"skip","skip","cElo +118pt impl 86","Big overprice."),
    ("2026-04-23","R1","Baptiste H. vs Quevedo C.","Hailey Baptiste","Caitlin Quevedo",1.46,2.75,86,62,-9.3,"skip","skip","cElo +86pt","Market overprice."),
    ("2026-04-23","R1","Osaka N. vs Osorio C.","Naomi Osaka","Camila Osorio",1.88,1.93,70,60,12.6,"caution","Q4_upset_watch","cElo Osaka +70pt / 1st clay month break","UPSET WATCH: Osaka clay weak, Osorio 6-0 6-3 R1 momentum. Dog @1.93 UF>=2."),
    ("2026-04-23","R1","Andreeva M. vs Udvardy P.","Mirra Andreeva","Panna Udvardy",1.04,11.0,377,90,-6.7,"skip","Q3_output_a","cElo +377pt","Q3: conf 90."),
    ("2026-04-24","R2","Frech M. vs Sierra S.","Magdalena Frech","Solana Sierra",1.65,2.25,69,60,-1.5,"skip","skip","cElo +69pt","Near break-even."),
    ("2026-04-24","R2","Gauff C. vs Jeanjean L.","Coco Gauff","Leolia Jeanjean",1.06,9.0,452,93,-1.3,"skip","Q3_output_a","cElo +452pt","Q3: conf 93."),
    ("2026-04-24","R2","Rybakina E. vs Ruse E.G.","Elena Rybakina","Elena Gabriela Ruse",1.05,11.0,306,85,-10.3,"skip","Q3_output_a","cElo +306pt","Q3: conf 85."),
    ("2026-04-24","R2","Sakkari M. vs Pliskova K.","Maria Sakkari","Karolina Pliskova",1.52,2.55,23,53,-19.0,"skip","skip","cElo +23pt tiny","Market overprice."),
    ("2026-04-24","R2","Zheng Q. vs Kenin S.","Qinwen Zheng","Sofia Kenin",1.38,3.05,145,70,-3.7,"skip","skip","cElo +145pt","Market priced."),
    ("2026-04-24","R2","Sonmez Z. vs Bucsa C.","Zeynep Sonmez","Cristina Bucsa",1.66,2.23,34,55,-8.9,"skip","skip","cElo +34pt tiny","Near coin flip."),
    ("2026-04-24","R2","Mboko V. vs McNally C.","Victoria Mboko","Caty McNally",1.28,3.75,177,74,-5.9,"skip","skip","cElo +177pt","Market priced."),
    ("2026-04-24","R2","Kostyuk M. vs Putintseva Y.","Marta Kostyuk","Yulia Putintseva",1.37,3.10,127,68,-7.5,"skip","skip","cElo +127pt","Market priced."),
    ("2026-04-24","R2","Noskova L. vs Arango E.","Linda Noskova","Emiliana Arango",1.15,5.60,201,76,-12.5,"skip","skip","cElo +201pt impl 87","Big overprice."),
    ("2026-04-24","R2","Cirstea S. vs Grant T.C.","Sorana Cirstea","Tyra Caterina Grant",1.25,4.00,341,88,9.6,"caution","Q4_upset_watch","cElo +341pt BUT Grant 19yo qualifier 3連勝momentum","DOWNGRADE GO to CAUTION-MARGIN: Grant R020/P010 momentum."),
    ("2026-04-24","R2","Pegula J. vs Boulter K.","Jessica Pegula","Katie Boulter",1.18,5.00,248,81,-4.8,"skip","skip","cElo +248pt","Market priced."),
    ("2026-04-24","R2","Keys M. vs Zhang Sh.","Madison Keys","Shuai Zhang",1.23,4.20,313,86,5.5,"go","Q1_go","cElo +313pt / Keys #16 seed / Zhang 6-match losing streak just broken","GO: Rec Keys @1.23."),
    ("2026-04-24","R2","Ostapenko J. vs Waltert S.","Jelena Ostapenko","Simona Waltert",1.45,2.80,124,67,-2.7,"skip","skip","cElo +124pt","Near break-even."),
    ("2026-04-24","R2","Samsonova L. vs Tjen J.","Liudmila Samsonova","Janice Tjen",1.56,2.45,144,70,8.6,"caution","Q4_upset_watch","cElo +144pt","CAUTION-MARGIN: EV+8.6."),
    ("2026-04-24","R2","Tauson C. vs Siniakova K.","Clara Tauson","Katerina Siniakova",1.81,2.00,31,54,-1.5,"skip","skip","cElo +31pt tiny","Near coin flip."),
    ("2026-04-24","R2","Mertens E. vs Eala A.","Elise Mertens","Alexandra Eala",1.37,3.15,222,78,7.1,"go","Q1_go","cElo +222pt / Eala past R2 in 7 tournaments / H2H Mertens 7-5 6-0","GO: Rec Mertens @1.37."),
]

OEI_MATCHES = [
    ("2026-04-23","R1","Osuigwe W. vs Akli A.","Whitney Osuigwe","Ayana Akli",1.20,4.10,149,70,-15.8,"skip","skip","125K out-of-scope","SKIP"),
    ("2026-04-23","R1","Klimovicova L. vs Barthel M.","Linda Klimovicova","Mona Barthel",1.83,1.87,-76,39,-28.1,"skip","skip","125K out-of-scope","SKIP"),
    ("2026-04-23","R1","Ferro F. vs Havlickova L.","Fiona Ferro","Lucie Havlickova",1.72,2.00,38,55,-4.7,"skip","skip","125K out-of-scope","SKIP"),
    ("2026-04-24","R2","Semenistaja D. vs Monnet C.","Darja Semenistaja","Carole Monnet",1.30,3.20,147,70,-9.1,"skip","skip","125K out-of-scope","SKIP"),
    ("2026-04-24","R2","Kudermetova P. vs Bronzetti L.","Polina Kudermetova","Lucia Bronzetti",1.37,2.85,157,71,-2.6,"skip","skip","125K out-of-scope","SKIP"),
]


def build_entry(r, sport="atp"):
    d,rnd,match,fav,dog,fo,do,cd,wp,ev,tier,quad,basis,note = r
    entry = {
        "tournament": "Mutua Madrid Open 2026",
        "round": rnd, "date": d, "match": match,
        "tier": tier, "quadrant": quad,
        "l1_metric": "clay_cElo" + ("_wta" if sport=="wta" else ""),
        "l1_data": {"ce_diff": cd, "fav": fav, "dog": dog},
        "predicted_winner": fav,
        "prediction_confidence": wp,
        "prediction_basis": basis,
        "odds": {"fav": fo, "dog": do},
        "note": note,
        "screened_session": "_50",
        "source": "2026-04-23.json",
    }
    if sport == "atp":
        entry["category"] = "ATP 1000"
        entry["surface"] = "clay"
    if tier == "go":
        entry["rec"] = fav; entry["rec_odds"] = fo; entry["ev"] = round(ev/100,4)
    elif tier == "caution":
        entry["caution_type"] = "margin" if wp < 75 else "track"
        entry["rec"] = None; entry["rec_odds"] = None; entry["ev"] = round(ev/100,4)
    else:
        entry["rec"] = None; entry["rec_odds"] = None; entry["ev"] = None
    entry["result"] = None; entry["score"] = None; entry["prediction_hit"] = None
    entry["hit"] = None; entry["actual_ev"] = None
    return entry


atp = json.load(open('records/tennis/2026-ATP.json','r',encoding='utf-8-sig'))
wta = json.load(open('records/wta/2026.json','r',encoding='utf-8-sig'))

for r in ATP_MATCHES:
    atp['predictions'].append(build_entry(r, "atp"))

madrid = None
for t in wta['tournaments']:
    if t.get('short') == 'Madrid':
        madrid = t; break
if madrid is None:
    madrid = {
        "name": "Mutua Madrid Open 2026", "short": "Madrid",
        "tier": "WTA 1000", "surface": "clay",
        "dates": "2026-04-21 ~ 2026-05-04", "status": "r1_r2_in_progress",
        "predictions": []
    }
    wta['tournaments'].append(madrid)

for r in WTA_MATCHES + OEI_MATCHES:
    madrid['predictions'].append(build_entry(r, "wta"))

wta['screening_log'].append({
    "date": "2026-04-23", "session": "_50",
    "tournament": "ATP Madrid + WTA Madrid + WTA 125K Oeiras",
    "note": "Session_50: 69試合スクリーニング (ATP 32 / WTA 32 / Oeiras 5). GO 5件 (Tsitsipas/Paul/Musetti/Keys/Mertens). Popyrin+Cirstea DOWNGRADE from GO to caution (cElo overrate + Grant momentum). Osaka-Osorio Q4_upset_watch.",
    "total_games": 69,
    "go_recommendations": 5,
    "caution_margin": 13,
    "skip": 43,
    "q3_output_a_count": 8,
    "q4_upset_watch": 13
})

if 'screening_log' not in atp:
    atp['screening_log'] = []
atp['screening_log'].append({
    "date": "2026-04-23", "session": "_50",
    "tournament": "ATP Mutua Madrid Open 2026",
    "note": "R1 15試合 + R2 17試合. GO: Tsitsipas @1.35 / Paul @1.40 / Musetti @1.42. Popyrin DOWNGRADED.",
    "total_games": 32, "go": 3, "caution": 8, "skip": 21,
    "q3_output_a": 1
})

json.dump(atp, open('records/tennis/2026-ATP.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(wta, open('records/wta/2026.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"ATP predictions: {len(atp['predictions'])}")
print(f"WTA Madrid predictions: {len(madrid['predictions'])}")
print("Saved.")
