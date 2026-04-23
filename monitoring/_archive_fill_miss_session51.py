"""Session_51 残 25件 miss_analysis 一括補填スクリプト"""
import json

# === ATP records 補填 ===
atp_path = 'records/tennis/2026-ATP.json'
with open(atp_path, encoding='utf-8-sig') as f:
    atp = json.load(f)
atp_g = atp.get('predictions') or []

# #10 de Minaur vs Vacherot MC2026 QF (4/10) - A004
g = atp_g[10]
g['miss_analysis'] = "Vacherot (WC, Monaco home) が R32 Hurkacz(PR) 撃破後 QF de Minaur(5) を撃破して 初の Monaco 人 MC SEMI-FINAL 進出 (Open Era)。home WC + 連続シード撃破モメンタム。crowd familiarity mental freedom of underdog with nothing to lose 全要因揃う。conf 算出時に R009 WC+2% のみで stop していた、連続ラウンド勝利モメンタムを織り込めなかった。"
g['miss_layer'] = "L4_External"
g['rule_linked'] = "R017 (P010 implemented 2026-04-20: WC home + 連続seed撃破モメンタム +5%)"
g['type_a_upset_id'] = "A004"

# #20 Khachanov(4) vs Ugo Carabelli (4/13 Barcelona R1) - A011
g = atp_g[20]
g['miss_analysis'] = "Carabelli (ARG, クレースペシャリスト) が Khachanov (ハードコート中心) をクレーで撃破。Carabelli 2026 クレー 10-4 Rosario Challenger 優勝。市場 cElo 差82pt は名声差に過ぎず surface-specific level では essentially equal。Carabelli 初 Top20 勝利。Khachanov MC R1 も敗退でフォーム不調。conf 算出時に surface-specific 補正が不足していた。"
g['miss_layer'] = "L1"
g['rule_linked'] = "P012 (R019 candidate: clay specialist vs hardcourt L1差縮小補正 - evidence 1/3)"
g['type_a_upset_id'] = "A011"

# #30 Martinez vs Sonego (4/14 Barcelona/Munich R1) - 詳細未調査
g = atp_g[30]
g['miss_analysis'] = "Sonego (ITA) が Martinez (ESP) をクレーで撃破。Martinez は Barcelona ホーム期待値高めだったが Sonego の clay baseline aggression が上回った。詳細スタッツ未取得 (次セッション WebSearch で要深掘り)。L2 直近フォーム + L4 home pressure 候補。"
g['miss_layer'] = "L2"
g['rule_linked'] = "PENDING (Session_52 詳細補填)"

# #36 Griekspoor(8) vs Shapovalov (4/14 Munich R1) - A005
g = atp_g[36]
g['miss_analysis'] = "Shapovalov (3連敗中だったが) returning to form。aggressive serve forehand combo on clay。市場が cElo 174pt 差で Griekspoor 過評価。Shapovalov の flat serve-centric style vs Griekspoor の clay baseline game で mismatch。cElo 差は noise band 範囲の effective 50/50。R1 upset winner だが直後 R2 で reversion (P014)。"
g['miss_layer'] = "L1"
g['rule_linked'] = "P014 (R021 candidate: R1 upset winner R2 reversion - evidence 1/3)"
g['type_a_upset_id'] = "A005"

# #40 Tsitsipas vs Marozsan (4/14 Munich R1) - A006
g = atp_g[40]
g['miss_analysis'] = "Tsitsipas MC R1 初敗退 (22-4 記録からの初大会 R1 敗退) 後 Barcelona→Munich 変更で直行。puntodebreak: Tsitsipas hits rock bottom。Marozsan は clay baseline specialist (Hungarian) style well-suited to Munich outdoor clay。cross-tournament travel の physical mental depletion + キャリア最悪exit メンタル崩壊。conf 算出時に R013 -5% フォーム調整では不足、-10% から -12% メンタル崩壊補正必要。"
g['miss_layer'] = "L4_External"
g['rule_linked'] = "P011 (R018 candidate: career worst exit 翌週 -10% メンタル崩壊補正 - evidence 1/3)"
g['type_a_upset_id'] = "A006"

# #45 Molcan(Q) vs Bublik(3) (4/14 Munich R1, CAUTION) - A012/U006
g = atp_g[45]
g['miss_analysis'] = "Bublik Munich debut + MC QF (Alcaraz戦大敗) → Munich 4日後 B2B inter-tournament 疲弊。Molcan は Djokovic beater quality の dangerous clay opponent。MC QF base adjustment -3% は under-correct (実際は -6 から -10% 必要)。CAUTION 判断は正しかったが GO 化避けた点が evidence。Molcan 6-4 6-2 dominant。"
g['miss_layer'] = "L4_External"
g['rule_linked'] = "P006 (R014 candidate: B2B inter-tournament 疲弊強化補正 - evidence 1/3)"
g['type_a_upset_id'] = "A012"

# #53 Norrie vs Quinn (4/17 Barcelona R2) - CE012
g = atp_g[53]
g['miss_analysis'] = "CE012 関連: predicted=Quinn は明確な誤記 (Norrie #54 GS決勝経験者が本命だった)。実際は Norrie が 6-3 4-6 6-4 で勝利 → 予測 Quinn は誤予測 → False は記録上正しいが prediction_basis に L1 cElo 優位側 (Norrie) と一致しない理由が記入されていなかった。CE012 で identify 済み。"
g['miss_layer'] = "PREDICTION_LOGIC_ERROR"
g['rule_linked'] = "CE012 (predicted_winner self-check protocol 必須化済 / R1消耗仮説の不適切な過大評価)"

# #55 Altmaier vs Molcan (4/16 Munich R2) - U006_R2 (R020 implemented evidence)
g = atp_g[55]
g['miss_analysis'] = "Molcan(Q) Munich R1 d. Bublik(3seed) 6-4 6-2 → R2 d. Altmaier 84% 1stSrvPts 総得点73-63で圧勝。連続upsetでqualifier がseed を2連破。Altmaier はクレー得意ドイツ人(ホーム) でも押された。R1 upset winner の R2 momentum 継続 (P013→R020 implemented evidence の一つ)。conf 算出時に Q選手 R1 upset 後の momentum を織り込めていなかった。"
g['miss_layer'] = "L4_External"
g['rule_linked'] = "R020 (P013 implemented 2026-04-20: R1 upset winner R2 +5% モメンタム)"
g['type_a_upset_id'] = "U006_R2"

# #57 Shapovalov vs Marozsan (4/17 Munich R2) - A015
g = atp_g[57]
g['miss_analysis'] = "Shapovalov R1 d. Griekspoor 6-4 3-6 6-2 (3連敗脱出反発 win) → R2 d. Marozsan 7-6(7) 6-2。1stセット TB接戦勝利、2ndセット完勝。3連敗中→3セット勝利=ピーク前の調子回復途上。対照的に Marozsan R1 d. Tsitsipas は career-worst-exit opponent での大興奮 upset、R2 ではその興奮が引いて実力通り → R2 reversion パターン (P014 候補)。"
g['miss_layer'] = "L4_External"
g['rule_linked'] = "P014 (R021 candidate: R1 upset winner R2 reversion - evidence 1/3 同一試合 A015)"
g['type_a_upset_id'] = "A015"

# #59 Fonseca vs Shelton (4/17 Munich QF) - A017 INVALIDATED → P023 evidence
g = atp_g[59]
g['miss_analysis'] = "Shelton No.2 seed fav @1.44 で予測通り勝利 (6-3 3-6 6-3)。Fonseca 19歳 clay momentum (Rinderknech 撃破) でも Shelton serve dominance (76% 1st / 71% 2nd) + aggressive baseline で封殺。若手モメンタムが Top20 サーブ型に stalled。**predicted=Fonseca は誤予測** (CE012 系列の L1 cElo 優位側選択ミス相当)。Shelton 側を選ぶべきだった。"
g['miss_layer'] = "PREDICTION_LOGIC_ERROR + L1"
g['rule_linked'] = "P023 (R023 candidate: Top20サーブ型 vs 若手 clay momentum 停止 - evidence 2/3)"
g['type_a_upset_id'] = "A017_corrected (UPSET 不成立、fav HIT として再分類)"

# #65 Darderi vs Kopriva (4/16 Munich R2) - A014
g = atp_g[65]
g['miss_analysis'] = "Kopriva (#77) Munich R1 d. Engel(WC) 3セット (GO HIT) → R2 d. Darderi (クレー2026 13-4)。1stセット2-6敗、2ndセット0-2ビハインドから逆転勝利。南米クレー Rio SF 実績の rally 能力が decisive。Darderi はクレー本命@1.37 だったが Kopriva の clay rally experience に敗北。R1 upset winner の R2 momentum 継続 (P013→R020 implemented evidence の一つ)。"
g['miss_layer'] = "L4_External"
g['rule_linked'] = "R020 (P013 implemented 2026-04-20: R1 upset winner R2 +5% モメンタム)"
g['type_a_upset_id'] = "A014"

# #67 Shapovalov vs Molcan (4/17 Munich QF) - A018
g = atp_g[67]
g['miss_analysis'] = "Molcan(Q) 3連続本命撃破完遂: R1 Bublik(3seed) 6-4 6-2 → R2 Altmaier(独ホーム) 84% 1stSrvPts → QF Shapovalov(4-match winstreak) ストレート。Slovak qualifier 初 ATP500 SF 到達。R020 decisive evidence。Shapovalov の Griekspoor R1 3セット消耗 (反発型) よりも Molcan の純粋なモメンタムが上回った。"
g['miss_layer'] = "L4_External"
g['rule_linked'] = "R020 (P013 implemented 2026-04-20: R1 upset winner R2/QF +5% モメンタム - decisive evidence)"
g['type_a_upset_id'] = "A018"

# #70 Fils(9) vs Musetti(2) (4/17 Barcelona QF)
g = atp_g[70]
g['miss_analysis'] = "Fils が Musetti を撃破 → Barcelona SF 進出 (後の F で Rublev 撃破して優勝)。Musetti クレー上位だったが Fils フォーム圧倒的。詳細スタッツ未取得 (Fils Barcelona Champion run の詳細は次セッション WebSearch で深掘り要)。L2 フォームピーク + L4 surface adaptation。"
g['miss_layer'] = "L2"
g['rule_linked'] = "PENDING (Fils Barcelona Champion run momentum pattern - 新規候補検討)"

# #81 Trungelliti vs Gojo Madrid Q (4/20)
g = atp_g[81]
g['miss_analysis'] = "Trungelliti が Gojo を撃破。Madrid Q R1 pickem (オッズ 1.86)。詳細スタッツ未取得 (次セッション WebSearch で深掘り要)。L1 effective coin-flip 試合での予測ミス。Q特有 borderline ケース。"
g['miss_layer'] = "L2"
g['rule_linked'] = "PENDING (Madrid Q R1 詳細補填 - Session_52)"

# #84 Darwin vs Bonzi Madrid Q (4/20) - A025
g = atp_g[84]
g['miss_analysis'] = "Bonzi (Top100 vet) が fav @1.61 で Darwin (低ランク無名) に敗北。market divergence 12pp。Top100 vet の Masters Q R1 motivational dip パターン (本戦出場権のみの副次大会ステージで motivational 低下)。conf 算出時にこの構造的 dip を織り込めていなかった (-5 から -7% 補正候補)。"
g['miss_layer'] = "L4_External"
g['rule_linked'] = "P017 (R022 candidate: Top100 vet Masters Q R1 motivation dip -5% - evidence 1/3)"
g['type_a_upset_id'] = "A025"

# #90 Hijikata vs Rodesch Madrid Q (4/20)
g = atp_g[90]
g['miss_analysis'] = "Hijikata が Rodesch を撃破。Madrid Q R1 pickem (オッズ 1.87 effective coin-flip)。詳細スタッツ未取得 (次セッション WebSearch で深掘り要)。Q特有 borderline ケース。"
g['miss_layer'] = "L2"
g['rule_linked'] = "PENDING (Madrid Q R1 詳細補填 - Session_52)"

with open(atp_path, 'w', encoding='utf-8') as f:
    json.dump(atp, f, ensure_ascii=False, indent=2)
print('[OK] ATP records 14件補填完了')

# === NHL records 補填 ===
nhl_path = 'records/nhl/2025-26.json'
with open(nhl_path, encoding='utf-8-sig') as f:
    nhl = json.load(f)
nhl_g = nhl.get('predictions') or nhl.get('games') or []

# #3 PHI@CAR (4/13) - A002
g = nhl_g[3]
g['rule_linked'] = "N016 (seeding_secured_rest_implemented: CAR が PO 用に主力 6名意図的 rest) - key evidence for rule"

# #7 MIN@STL (4/13) - A003
g = nhl_g[7]
g['rule_linked'] = "N016 (seeding_secured_rest_implemented: MIN PO 確保で intensity 低下 + STL 5連続失点逆転) + UFH04 fatigue motivation"

# #17 MTL@TBL (4/18 RS最終, CAUTION)
g = nhl_g[17]
g['rule_linked'] = "PENDING (RS 4/18 試合・PO直前 line-up rest pattern 候補 - Session_52 深掘り)"

# #19 PHI@PIT (4/18) - A027 関連 RS prelude
g = nhl_g[19]
g['rule_linked'] = "A027 関連 RS 4/18 (G1 直前): PHI young energy (Drysdale/Martone/Vladar) vs PIT veteran fade pattern と同一構造の prelude RS。P018+P019 candidate。"

# #21 MIN@DAL (4/18) - A028 関連 RS prelude
g = nhl_g[21]
g['rule_linked'] = "A028 関連 RS 4/18 (G1 直前): MIN xGF% 上位 (51.50 vs 50.79) - lower seed process advantage の prelude。N001 + P025 candidate。"

# #31 MTL@TBL G1 (4/20) - A021
g = nhl_g[31]
g['rule_linked'] = "P018 (NHL PO G1 underdog 若手コア活性化 - evidence 1/3): MTL Slafkovsky(21歳) hat trick + OT 1:22 PP GWG。Suzuki(25歳) 101pts career high。TBL @1.53 home A2 seed + Vasilevskiy confirmed でも若手コア爆発。CAUTION no-bet で P&L影響なし。"
g['type_a_upset_id'] = "A021"

with open(nhl_path, 'w', encoding='utf-8') as f:
    json.dump(nhl, f, ensure_ascii=False, indent=2)
print('[OK] NHL records 6件補填完了 (#3/#7/#17/#19/#21/#31)')

# === NBA records 補填 ===
nba_path = 'records/nba/2025-26.json'
with open(nba_path, encoding='utf-8-sig') as f:
    nba = json.load(f)
nba_g = nba.get('predictions') or nba.get('games') or []

# #3 CHA vs ORL (4/18 RS)
g = nba_g[3]
g['rule_linked'] = "PENDING (NBA RS 4/18 - ORL season-end momentum / CHA tank pattern 候補 - Session_52 深掘り)"

# #8 LAL vs HOU (4/19 RS)
g = nba_g[8]
g['rule_linked'] = "PENDING (NBA RS 4/19 LAL-HOU - PO seeding 直前 motivation 確認要 - Session_52 詳細補填)"

# #16 DET vs ORL (4/20 RS live)
g = nba_g[16]
g['miss_analysis'] = "RS 4/20 試合。A026 (DET vs ORL G1) と同シリーズ前史。DET young core inexperience + ORL playoff experience の構造的 gap が RS 段階でも発現。詳細スタッツ未取得。L4_External (PO 直前 motivation curve)。"
g['miss_layer'] = "L4_External"
g['rule_linked'] = "P022 関連 (NBA PO G1 experience gap pattern の prelude - 同シリーズ A026 と関連)"

with open(nba_path, 'w', encoding='utf-8') as f:
    json.dump(nba, f, ensure_ascii=False, indent=2)
print('[OK] NBA records 3件補填完了 (#3/#8/#16)')

print()
print('=== 補填合計: ATP 15件 + NHL 6件 + NBA 3件 = 24件 ===')
