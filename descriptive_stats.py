"""
Descriptive Statistics & Classic Regression -- Ballon d'Or Project
======================================================================
This complements the scikit-learn predictive model with the kind of
output taught in an intro Business Statistics course: a regression
summary table (coefficients, standard errors, z-values, p-values,
pseudo R-squared), a scatter plot, and box plots comparing groups.

Run this after predict_ballon_dor_v6.py / build_stage_depth.py have
already produced historical_candidates_v6.csv.
"""

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

df = pd.read_csv("historical_candidates_v6.csv")

FEATURES = [
    "goal_contributions", "trophy_prestige_score",
    "is_MF", "is_DF", "is_GK",
]
TARGET = "won_balon_dor"

# ---------------------------------------------------------------------------
# 1. CLASSIC LOGISTIC REGRESSION TABLE (statsmodels, not sklearn)
#    This is the textbook-style output: coefficients, std errors,
#    z-statistics, p-values, and pseudo R-squared.
# ---------------------------------------------------------------------------
X = sm.add_constant(df[FEATURES])  # adds the intercept term
y = df[TARGET]

logit_model = sm.Logit(y, X)
result = logit_model.fit(disp=0)  # disp=0 suppresses optimizer chatter

print("=" * 70)
print("LOGISTIC REGRESSION SUMMARY (statsmodels)")
print("=" * 70)
print(result.summary())
print()
print(f"Pseudo R-squared: {result.prsquared:.3f}")
print("(Pseudo R-squared works differently than OLS R-squared -- 0.2-0.4")
print(" is often considered a strong fit for logistic regression.)")

# Save the summary table to a text file too, for easy reference/quoting
with open("regression_summary.txt", "w") as f:
    f.write(str(result.summary()))
    f.write(f"\n\nPseudo R-squared: {result.prsquared:.3f}\n")

# ---------------------------------------------------------------------------
# 2. SCATTER PLOT -- the two strongest predictors, colored by outcome
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
winners = df[df[TARGET] == 1]
losers = df[df[TARGET] == 0]

ax.scatter(losers["goal_contributions"], losers["trophy_prestige_score"],
           alpha=0.5, s=50, color="#94a3b8", label="Didn't win")
ax.scatter(winners["goal_contributions"], winners["trophy_prestige_score"],
           alpha=0.9, s=90, color="#dc2626", label="Won Ballon d'Or", edgecolors="black")

# label the winners so it's readable
for _, row in winners.iterrows():
    ax.annotate(f"{row['player'].split()[-1]} '{str(row['year'])[2:]}",
                (row["goal_contributions"], row["trophy_prestige_score"]),
                fontsize=8, xytext=(4, 4), textcoords="offset points")

ax.set_xlabel("Goal Contributions (Goals + Assists)")
ax.set_ylabel("Trophy Prestige Score")
ax.set_title("Ballon d'Or Candidates: Output vs. Team Success (2011-2025)")
ax.legend()
plt.tight_layout()
plt.savefig("scatter_output_vs_trophies.png", dpi=150)
plt.close()
print("\nSaved scatter_output_vs_trophies.png")

# ---------------------------------------------------------------------------
# 3. BOX PLOTS -- distribution comparisons
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Box plot A: goal_contributions by win/loss
df.boxplot(column="goal_contributions", by=TARGET, ax=axes[0])
axes[0].set_xlabel("Won Ballon d'Or (0 = No, 1 = Yes)")
axes[0].set_ylabel("Goal Contributions")
axes[0].set_title("Goal Contributions: Winners vs. Non-Winners")

# Box plot B: goal_contributions by position
df.boxplot(column="goal_contributions", by="position", ax=axes[1])
axes[1].set_xlabel("Position")
axes[1].set_ylabel("Goal Contributions")
axes[1].set_title("Goal Contributions by Position")

plt.suptitle("")  # remove the default pandas suptitle
plt.tight_layout()
plt.savefig("boxplots_goal_contributions.png", dpi=150)
plt.close()
print("Saved boxplots_goal_contributions.png")

print("\nDone. Three outputs: regression_summary.txt, scatter_output_vs_trophies.png, boxplots_goal_contributions.png")
