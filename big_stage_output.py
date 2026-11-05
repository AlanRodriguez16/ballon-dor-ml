"""
'Big stage' individual output -- goals+assists specifically on the World
Cup and Champions League stage, as a feature SEPARATE from season-total
goal_contributions.

WHY THIS IS A SEPARATE FEATURE, NOT A REPLACEMENT:
goal_contributions (used in v6) already includes these goals once, as
part of the full season total. This feature deliberately counts them
AGAIN, as a weighted "bonus" -- the idea being a World Cup semifinal
goal should carry extra weight beyond just being 1 of N goals in a
season tally. This is a legitimate design choice (a form of feature
weighting), not double-counting by accident -- just be aware it's
correlated with goal_contributions by construction.

DATA SOURCE & HONESTY NOTE:
For the 2026 candidates, I'm using the "Seleccion" (national team) and
"Champions League" rows directly from your ORIGINAL spreadsheet -- no
new guessing. This isn't a perfect isolation of "knockout rounds only"
(it includes qualifiers/group stage too), but for a World Cup year the
national team total is heavily dominated by the tournament itself, and
it's the most reliable number available without speculative reconstruction
of match-by-match logs.

LIMITATION: I do NOT have this breakdown for the 94 historical rows (it
would require researching national-team and UCL-specific splits for 94
players individually, which I haven't done). So this analysis is applied
to the 2026 candidates only, as an additional descriptive lens on top of
the v6 model -- not (yet) folded into the trained regression coefficients.
"""
import pandas as pd

# player: (seleccion_goals, seleccion_assists, ucl_goals, ucl_assists)
# -- pulled directly from the "Por competicion" sheet of your spreadsheet
big_stage = {
    "Lamine Yamal":     (1, 4, 6, 4),
    "Kylian Mbappe":    (10, 1, 15, 1),
    "Harry Kane":       (6, 1, 14, 2),
    "Michael Olise":    (0, 7, 4, 7),
    "Ousmane Dembele":  (0, 0, 2, 8),   # UCL figure is actually "Champions/Cup/Supercups" combined -- least precise of the six
    "Jude Bellingham":  (6, 1, 2, 1),
}

rows = []
for player, (wg, wa, ug, ua) in big_stage.items():
    wc_total = wg + wa
    ucl_total = ug + ua
    big_stage_total = wc_total + ucl_total
    rows.append((player, wc_total, ucl_total, big_stage_total))

df = pd.DataFrame(rows, columns=["player", "wc_goal_contributions", "ucl_goal_contributions", "big_stage_total"])
df = df.sort_values("big_stage_total", ascending=False)
print("'Big stage' output -- World Cup + Champions League goal contributions combined:")
print(df.to_string(index=False))

df.to_csv("big_stage_output.csv", index=False)
