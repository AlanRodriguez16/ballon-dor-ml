"""
Adds GRADED tournament-depth scoring instead of binary "won it or didn't."

STAGE WEIGHTS (subjective but reasoned -- a final loss should count for a
lot, a group-stage exit for ~nothing):

World Cup / Euros / Copa America:
  Winner=10, Runner-up=6, 3rd place=4, 4th place=3,
  Quarterfinal=1.5, Round of 16=0.5, Group stage=0

Champions League (continental club cup):
  Winner=8, Runner-up=5, Semifinal=3, Quarterfinal=1.5,
  Round of 16=0.5, League/group phase exit=0

DATA CONFIDENCE NOTE -- being honest about what I actually know here:
For the 2026 candidates, the World Cup stages are EXPLICITLY stated in
your spreadsheet's notes (Spain champion/Yamal, England 3rd/Kane+Bellingham,
France 4th/Mbappe+Olise+Dembele). Reliable.
The Champions League stage for PSG (winner, Dembele) and Bayern (semifinal,
Kane+Olise) is also explicit in your sheet.
BUT your sheet does NOT state what stage Real Madrid (Mbappe, Bellingham)
or Barcelona (Yamal) reached in the 2025-26 Champions League beyond goal
tallies -- so I'm leaving those at 0 rather than guessing. If you know
those stages, they should be added; they could matter, especially for
Mbappe given he topped the UCL scoring charts.

For the older 42-row core of the historical dataset, I've only retrofitted
the two cases I'm confident about (2014 Messi/Argentina WC runner-up,
2018 Modric/Croatia WC runner-up) -- both real, well-documented near-misses
that are exactly the kind of case this feature should capture. Reconstructing
exact knockout-stage results for all 94 historical rows is future work,
not something to fake for the sake of looking complete.
"""
import pandas as pd

WC_STAGE = {"winner":10, "runner_up":6, "third":4, "fourth":3,
            "quarterfinal":1.5, "round16":0.5, "group":0, "none":0}
UCL_STAGE = {"winner":8, "runner_up":5, "semifinal":3, "quarterfinal":1.5,
             "round16":0.5, "group":0, "none":0}

df = pd.read_csv("historical_candidates_v5.csv")

# Start from the existing trophy_prestige_score (which already counts
# league/domestic cup/super cup trophies correctly -- we're only
# upgrading the WC and UCL components from binary to graded).
# Historical won_international_tournament / won_continental_cup columns
# aren't in v5 (we replaced them with the combined prestige score in v4),
# so we apply targeted corrections directly by player+year.

# Subtract-then-add pattern: remove old binary WC/UCL contribution where
# we're overriding it, then add the graded version.
corrections = {
    # (year, player): (wc_stage, ucl_stage)  -- only where I'm confident
    (2014, "Lionel Messi"): ("runner_up", None),     # Argentina lost 2014 final
    (2018, "Luka Modric"):  ("runner_up", None),     # Croatia lost 2018 final (UCL win already counted as winner)
}

for (yr, player), (wc, ucl) in corrections.items():
    mask = (df["year"] == yr) & (df["player"] == player)
    if wc:
        df.loc[mask, "trophy_prestige_score"] += WC_STAGE[wc]  # they had 0 WC credit before
    if ucl:
        df.loc[mask, "trophy_prestige_score"] += UCL_STAGE[ucl]

# ---------------------------------------------------------------------------
# 2026 candidates -- graded WC + UCL depth, explicit from your spreadsheet
# ---------------------------------------------------------------------------
candidates_2026 = {
    # player: (base_trophy_score_excl_WC_UCL, wc_stage, ucl_stage)
    "Lamine Yamal":     (7,  "winner", "none"),    # la_liga(6)+super_cup(1)=7, WC won, UCL stage unknown->none
    "Kylian Mbappe":    (0,  "fourth", "none"),    # no trophies, France 4th, Real's UCL stage unknown
    "Harry Kane":       (8,  "third",  "semifinal"),  # bundesliga+domestic_cup+super_cup=8, England 3rd, Bayern UCL semis
    "Michael Olise":    (8,  "fourth", "semifinal"),  # same club trophies, France 4th, Bayern UCL semis
    "Ousmane Dembele":  (7,  "fourth", "winner"),  # ligue1+domestic_cup+super_cup=7, France 4th, PSG won UCL
    "Jude Bellingham":  (0,  "third",  "none"),    # no trophies, England 3rd, Real's UCL stage unknown
}

print("2026 candidates -- graded prestige scores:")
rows = []
for player, (base, wc, ucl) in candidates_2026.items():
    total = base + WC_STAGE[wc] + UCL_STAGE[ucl]
    print(f"  {player:20s} base={base:2d} + WC({wc})={WC_STAGE[wc]:.1f} + UCL({ucl})={UCL_STAGE[ucl]:.1f}  = {total:.1f}")
    rows.append((player, total))

df.to_csv("historical_candidates_v6.csv", index=False)

import json
with open("candidates_2026_v6.json","w") as f:
    json.dump(rows, f)
print("\nSaved historical_candidates_v6.csv and candidates_2026_v6.json")
