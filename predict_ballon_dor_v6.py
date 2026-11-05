"""
Ballon d'Or 2026 Predictor v6 — graded tournament depth (WC + UCL)
=====================================================================
Same model structure as v5, but trophy_prestige_score now credits HOW FAR
a team went in the World Cup and Champions League, not just whether they
won it outright. See build_stage_depth.py for the exact stage weights and
which rows/candidates this was confidently applied to.
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
scores = cross_val_score(model, X, y, cv=5, scoring="roc_auc")
model.fit(X, y)

print(f"Dataset size: {len(df)} rows")
print(f"Cross-val ROC-AUC: {scores.mean():.2f}\n")
print("Coefficients:")
for feat, coef in zip(FEATURES, model.coef_[0]):
    print(f"  {feat:30s} {coef:+.4f}")
print()

# 2026 candidates with graded prestige scores from build_stage_depth.py
candidates_2026 = pd.DataFrame([
    # player, position, goal_contributions, trophy_prestige_score (graded)
    ["Lamine Yamal",     "FW", 45, 17.0],
    ["Kylian Mbappe",    "FW", 59,  3.0],
    ["Harry Kane",       "FW", 75, 15.0],
    ["Michael Olise",    "FW", 56, 14.0],
    ["Ousmane Dembele",  "FW", 27, 18.0],
    ["Jude Bellingham",  "MF", 20,  4.0],
], columns=["player", "position", "goal_contributions", "trophy_prestige_score"])

for pos in ["MF","DF","GK"]:
    candidates_2026[f"is_{pos}"] = (candidates_2026["position"] == pos).astype(int)
candidates_2026["journalists_only_voting"] = 1
candidates_2026["season_based_period"] = 1

candidates_2026["predicted_win_probability"] = model.predict_proba(candidates_2026[FEATURES])[:, 1]
candidates_2026 = candidates_2026.sort_values("predicted_win_probability", ascending=False)

print("=" * 70)
print("2026 PREDICTIONS v6 -- graded World Cup + Champions League depth")
print("=" * 70)
for _, row in candidates_2026.iterrows():
    print(f"  {row['player']:20s} ({row['position']})  {row['predicted_win_probability']*100:5.1f}%   "
          f"goal_contrib={row['goal_contributions']:.0f}, prestige={row['trophy_prestige_score']:.1f}")

candidates_2026.to_csv("predictions_2026_v6.csv", index=False)
print("\nSaved to predictions_2026_v6.csv")
