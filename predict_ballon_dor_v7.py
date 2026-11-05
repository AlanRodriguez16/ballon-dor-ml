"""
Ballon d'Or 2026 Predictor v7 — 'big stage' sensitivity test
=================================================================
IMPORTANT: this is a SENSITIVITY TEST, not a retrained model. The v6
model's coefficients are trained on the 94-row historical dataset, which
does NOT have World Cup/Champions-League-specific goal splits (only your
6 2026 candidates do, from your spreadsheet). So we cannot honestly fit
a NEW coefficient that says "big-stage goals matter X amount more."

What we CAN honestly do: take the model's already-learned sensitivity to
goal_contributions (how much each additional goal contribution shifts win
probability) and apply it to an INFLATED goal_contributions number for the
2026 candidates only -- where World Cup + Champions League goal
contributions count a second time, as a bonus. This tells us how much the
ranking WOULD move if big-stage output matters at least as much as a
regular goal -- a lower bound on the effect, since big-stage goals
plausibly deserve MORE than a 1x bonus, not just an equal one.

If this test barely moves the needle, that's informative too -- it would
mean this feature isn't worth the (substantial) effort of going back and
researching WC/UCL splits for the full historical dataset.
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

df = pd.read_csv("historical_candidates_v6.csv")

FEATURES = [
    "goal_contributions", "trophy_prestige_score",
    "is_MF", "is_DF", "is_GK",
    "journalists_only_voting", "season_based_period",
]
TARGET = "won_balon_dor"
X, y = df[FEATURES], df[TARGET]

model = LogisticRegression(max_iter=2000, class_weight="balanced", C=0.5)
model.fit(X, y)
goal_contrib_coef = model.coef_[0][FEATURES.index("goal_contributions")]
print(f"Model's learned sensitivity to goal_contributions: {goal_contrib_coef:+.4f} per goal contribution")
print("(this is the SAME v6 model, unchanged -- we're not refitting it)\n")

# 2026 candidates: base stats (same as v6) + big-stage bonus
candidates_2026 = pd.DataFrame([
    # player, position, goal_contributions, trophy_prestige_score, big_stage_bonus
    ["Lamine Yamal",     "FW", 45, 17.0, 15],
    ["Kylian Mbappe",    "FW", 59,  3.0, 27],
    ["Harry Kane",       "FW", 75, 15.0, 23],
    ["Michael Olise",    "FW", 56, 14.0, 18],
    ["Ousmane Dembele",  "FW", 27, 18.0, 10],
    ["Jude Bellingham",  "MF", 20,  4.0, 10],
], columns=["player", "position", "goal_contributions", "trophy_prestige_score", "big_stage_bonus"])

for pos in ["MF","DF","GK"]:
    candidates_2026[f"is_{pos}"] = (candidates_2026["position"] == pos).astype(int)
candidates_2026["journalists_only_voting"] = 1
candidates_2026["season_based_period"] = 1

# v6 prediction (original, unweighted)
candidates_2026["prob_v6_original"] = model.predict_proba(candidates_2026[FEATURES])[:, 1]

# v7 prediction: goal_contributions gets the big-stage bonus added on top
candidates_2026_v7 = candidates_2026.copy()
candidates_2026_v7["goal_contributions"] = candidates_2026_v7["goal_contributions"] + candidates_2026_v7["big_stage_bonus"]
candidates_2026["prob_v7_bigstage_weighted"] = model.predict_proba(candidates_2026_v7[FEATURES])[:, 1]

candidates_2026["shift_pp"] = (candidates_2026["prob_v7_bigstage_weighted"] - candidates_2026["prob_v6_original"]) * 100

candidates_2026 = candidates_2026.sort_values("prob_v7_bigstage_weighted", ascending=False)

print("=" * 85)
print("COMPARISON: v6 (original) vs v7 (big-stage-weighted goal_contributions)")
print("=" * 85)
print(f"{'Player':20s} {'v6 %':>8s} {'v7 %':>8s} {'Shift (pp)':>12s}")
for _, row in candidates_2026.iterrows():
    print(f"{row['player']:20s} {row['prob_v6_original']*100:7.1f}% {row['prob_v7_bigstage_weighted']*100:7.1f}% "
          f"{row['shift_pp']:+11.1f}")

candidates_2026.to_csv("predictions_2026_v7.csv", index=False)
print("\nSaved to predictions_2026_v7.csv")
