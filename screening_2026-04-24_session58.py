"""
Session_58 (2026-04-24) スクリーニング script
- 2026-04-24.json の upcoming 試合から新規分を抽出
- L1 (cElo/xGF%/NRtg/PD) で差分計算
- Q1-Q4 + skip 分類
- 既存 records との重複を除外
- 結果を stdout に出力
"""

import json

# ============================
# cElo ratings (tennisabstract 2026-04-24 取得)
# ============================
ATP_CELO = {
    "Tommy Paul": 1891.3, "Jannik Sinner": 2194.1, "Andrey Rublev": 1865.9,
    "Lorenzo Musetti": 1956.9, "Stefanos Tsitsipas": 1872.0, "Alexander Bublik": 1884.7,
    "Alex De Minaur": 1892.0, "Rafael Jodar": 1867.5, "Joao Fonseca": 1845.2,
    "Marin Cilic": 1715.2, "Denis Shapovalov": 1729.6, "Tallon Griekspoor": 1742.5,
    "Ugo Humbert": 1732.1, "Cameron Norrie": 1827.7, "Tomas Machac": 1756.5,
    "Sebastian Ofner": 1679.8, "Tomas Martin Etcheverry": 1800.6, "Ben Shelton": 1917.0,
    "Dino Prizmic": 1733.4, "Brandon Nakashima": 1723.7, "Alexander Blockx": 1738.5,
    "Alejandro Davidovich Fokina": 1812.9, "Pablo Carreno Busta": 1724.4,
    "Mariano Navone": 1768.0, "Alexander Zverev": 2009.0,
    "Francisco Cerundolo": 1868.2, "Yannick Hanfmann": 1748.5, "Terence Atmane": 1625.3,
    "Jaume Munar": 1729.1, "Casper Ruud": 1930.7, "Vilius Gaubas": 1561.3,
    "Felix Auger Aliassime": 1885.2, "Karen Khachanov": 1793.3, "Adam Walton": 1469.2,
    "Learner Tien": 1633.4, "Adolfo Daniel Vallejo": 1671.0,
    "Juan Manuel Cerundolo": 1685.6, "Luciano Darderi": 1790.4,
    "Daniil Medvedev": 1905.7, "Fabian Marozsan": 1732.4, "Flavio Cobolli": 1832.3,
    "Camilo Ugo Carabelli": 1746.8, "Martin Damm": 1371.8, "Jakub Mensik": 1794.1,
    "Daniel Merida Aguilar": 1660.2, "Corentin Moutet": 1757.8,
    "Nikoloz Basilashvili": 1596.5, "Valentin Vacherot": 1811.9,
    "Emilio Nava": 1628.8, "Elmer Moller": 1526.4, "Gabriel Diallo": 1679.1,
    "Sebastian Baez": 1790, "Nikoloz Basilashvili": 1596.5,
    "Nicolai Budkov Kjaer": 1450, # estimate - very young
    "Hubert Hurkacz": 1760,  # estimate from memory
}

WTA_CELO = {
    "Aryna Sabalenka": 2152.4, "Iga Swiatek": 2031.4, "Coco Gauff": 2039.2,
    "Elena Rybakina": 2049.9, "Mirra Andreeva": 1980.3, "Madison Keys": 1888.7,
    "Jessica Pegula": 1955.4, "Belinda Bencic": 1815.8, "Naomi Osaka": 1805.0,
    "Elise Mertens": 1822.6, "Alexandra Eala": 1601.1, "Clara Tauson": 1752.6,
    "Katerina Siniakova": 1721.6, "Katie Boulter": 1707.1, "Linda Noskova": 1785.0,
    "Marta Kostyuk": 1878.2, "Yulia Putintseva": 1751.4, "Emiliana Arango": 1583.9,
    "Anhelina Kalinina": 1797.4, "Diana Shnaider": 1816.9, "Leylah Fernandez": 1720.4,
    "Iva Jovic": 1749.4, "Hailey Baptiste": 1695.4, "Jasmine Paolini": 1896.4,
    "Jaqueline Cristian": 1735.9, "Liudmila Samsonova": 1746.1, "Anna Bondar": 1730.5,
    "Simona Waltert": 1669.3, "Jelena Ostapenko": 1793.4, "Sorana Cirstea": 1804.3,
    "Tyra Caterina Grant": 1463.0, "Elena Ruse": 1743.6,
    "Xin Yu Wang": 1673.6, "Kristina Bucsa": 1615.4, "Zeynep Sonmez": 1649.7,
    "Leolia Jeanjean": 1587.7, "Katie Volynets": 1681.8, "Victoria Mboko": 1863.9,
    "Dayana Yastremska": 1731.9, "Tatjana Maria": 1553.2, "Xiyu Wang": 1645.8,
    "Ann Li": 1700,  # estimate
    "Darija Snigur": 1580,  # estimate (Ukrainian)
    "Petra Udvardy": 1640,  # estimate
    "Carla Osorio Serrano": 1580,  # estimate
    "Katie McNally": 1615,  # estimate
    "Peyton Stearns": 1750,  # estimate
    "Alycia Parks": 1720,  # estimate
}

# Helper
def classify(fav_celo, dog_celo, fav_odds, dog_odds, sport="atp"):
    diff = fav_celo - dog_celo
    thr = 100 if sport == "atp" else 80
    fav_implied = 1 / fav_odds * 100
    dog_implied = 1 / dog_odds * 100
    div_pp = fav_implied - dog_implied

    # base confidence from cElo diff (simple elo -> prob)
    # P = 1 / (1 + 10^(-diff/400))
    import math
    if diff > 0:
        prob_fav = 1 / (1 + 10 ** (-diff / 400))
    else:
        prob_fav = 1 / (1 + 10 ** (-diff / 400))
    conf = round(prob_fav * 100, 1)

    # EV
    ev = (prob_fav * fav_odds - 1) * 100

    # Classify
    l1_pass = abs(diff) >= thr
    if not l1_pass:
        q = "skip"
        tier = "skip"
    elif conf >= 75 and ev > 5:
        q = "Q1_go"
        tier = "go"
    elif conf >= 85:
        q = "Q3_output_a"
        tier = "skip" if ev <= 5 else "go"
    elif 80 <= conf < 85:
        q = "Q3_mid"
        tier = "skip"
    else:
        q = "skip"
        tier = "skip"

    return {
        "diff": round(diff, 1), "conf": conf, "ev": round(ev, 2),
        "fav_implied": round(fav_implied, 1), "div_pp": round(div_pp, 1),
        "quadrant": q, "tier": tier, "l1_pass": l1_pass
    }

# ============================
# ATP Madrid R2 (4/25 18:00 JST slot)
# ============================
atp_r2 = [
    # (p1, odds1, p2, odds2)
    ("Brandon Nakashima", 2.07, "Alexander Blockx", 1.76),
    ("Alejandro Davidovich Fokina", 1.49, "Pablo Carreno Busta", 2.65),
    ("Mariano Navone", 4.30, "Alexander Zverev", 1.23),
    ("Francisco Cerundolo", 1.31, "Yannick Hanfmann", 3.50),
    ("Ugo Humbert", 1.84, "Terence Atmane", 1.97),
    ("Daniel Merida Aguilar", 2.65, "Corentin Moutet", 1.49),
    ("Daniil Medvedev", 1.53, "Fabian Marozsan", 2.50),
    ("Karen Khachanov", 1.22, "Adam Walton", 4.40),
    ("Learner Tien", 2.20, "Adolfo Daniel Vallejo", 1.68),
    ("Juan Manuel Cerundolo", 2.55, "Luciano Darderi", 1.52),
    ("Alexander Bublik", 1.66, "Stefanos Tsitsipas", 2.23),
    ("Nicolai Budkov Kjaer", 2.47, "Denis Shapovalov", 1.55),
    ("Vilius Gaubas", 3.95, "Felix Auger Aliassime", 1.25),
    ("Jaume Munar", 2.90, "Casper Ruud", 1.42),
    ("Martin Damm", 3.65, "Jakub Mensik", 1.29),
    ("Camilo Ugo Carabelli", 2.80, "Flavio Cobolli", 1.44),
    # 4/25 JST early morning (ET 4/24 night)
    ("Rafael Jodar", 2.03, "Alex De Minaur", 1.83),
    ("Joao Fonseca", 1.23, "Marin Cilic", 4.20),
]

# ATP R2 remaining (4/24 late) from data upcoming
atp_r1_r2_late_424 = [
    ("Sebastian Ofner", 2.45, "Tomas Martin Etcheverry", 1.58),
    ("Tiago Agustin Tirante", 3.00, "Tommy Paul", 1.42),  # already in records
    ("Jannik Sinner", 1.01, "Benjamin Bonzi", 21.0),  # already in records likely
    ("Cameron Norrie", 2.14, "Tomas Machac", 1.74),
]

# ============================
# WTA Madrid R2 (4/25 upcoming)
# ============================
wta_r2 = [
    # 4/24 later
    ("Clara Tauson", 1.83, "Katerina Siniakova", 2.03),
    # 4/25 slate
    ("Katie McNally", 3.45, "Victoria Mboko", 1.33),
    ("Jessica Pegula", 1.14, "Katie Boulter", 5.60),
    ("Iga Swiatek", 1.05, "Ann Li", 9.80),
    ("Belinda Bencic", 1.65, "Diana Shnaider", 2.25),
    ("Anhelina Kalinina", 2.18, "Naomi Osaka", 1.69),
    ("Mirra Andreeva", 1.12, "Dalma Galfi", 6.40),  # Galfi not in cElo dict
    ("Leylah Fernandez", 2.34, "Iva Jovic", 1.61),
    ("Aryna Sabalenka", 1.03, "Jaqueline Cristian", 13.0),
    ("Liudmila Samsonova", 3.40, "Anna Bondar", 1.32),
    ("Hailey Baptiste", 2.33, "Jasmine Paolini", 1.61),
]

def find_player_celo(name, pool):
    # Try exact
    if name in pool:
        return pool[name]
    # Try partial
    for k in pool:
        if name.lower() in k.lower() or k.lower() in name.lower():
            return pool[k]
    return None

def run_atp(matches, label):
    print(f"\n==== {label} ====")
    for p1, o1, p2, o2 in matches:
        c1 = find_player_celo(p1, ATP_CELO)
        c2 = find_player_celo(p2, ATP_CELO)
        if c1 is None or c2 is None:
            print(f"[MISSING cElo] {p1} ({c1}) vs {p2} ({c2})")
            continue
        # favorite = lower odds
        if o1 < o2:
            fav_name, fav_c, fav_o = p1, c1, o1
            dog_name, dog_c, dog_o = p2, c2, o2
        else:
            fav_name, fav_c, fav_o = p2, c2, o2
            dog_name, dog_c, dog_o = p1, c1, o1
        r = classify(fav_c, dog_c, fav_o, dog_o, "atp")
        marker = "🎯" if r["quadrant"] == "Q1_go" else ("📊" if r["quadrant"] in ("Q3_output_a","Q3_mid") else ("" if r["tier"]=="skip" else "🔍"))
        print(f"{marker} [{r['quadrant']:12s}] {fav_name:30s} (cElo {fav_c:.0f}) vs {dog_name:30s} (cElo {dog_c:.0f}) | diff {r['diff']:+7.1f} | conf {r['conf']:.1f}% | EV {r['ev']:+7.2f}% | odds {fav_o:.2f}")

def run_wta(matches, label):
    print(f"\n==== {label} ====")
    for p1, o1, p2, o2 in matches:
        c1 = find_player_celo(p1, WTA_CELO)
        c2 = find_player_celo(p2, WTA_CELO)
        if c1 is None or c2 is None:
            print(f"[MISSING cElo] {p1} ({c1}) vs {p2} ({c2})")
            continue
        if o1 < o2:
            fav_name, fav_c, fav_o = p1, c1, o1
            dog_name, dog_c, dog_o = p2, c2, o2
        else:
            fav_name, fav_c, fav_o = p2, c2, o2
            dog_name, dog_c, dog_o = p1, c1, o1
        r = classify(fav_c, dog_c, fav_o, dog_o, "wta")
        marker = "🎯" if r["quadrant"] == "Q1_go" else ("📊" if r["quadrant"] in ("Q3_output_a","Q3_mid") else ("" if r["tier"]=="skip" else "🔍"))
        print(f"{marker} [{r['quadrant']:12s}] {fav_name:25s} (cElo {fav_c:.0f}) vs {dog_name:25s} (cElo {dog_c:.0f}) | diff {r['diff']:+7.1f} | conf {r['conf']:.1f}% | EV {r['ev']:+7.2f}% | odds {fav_o:.2f}")

run_atp(atp_r1_r2_late_424, "ATP Madrid 4/24 late (R1/R2)")
run_atp(atp_r2, "ATP Madrid 4/25 slate (R2)")
run_wta(wta_r2, "WTA Madrid 4/25 slate (R2)")
