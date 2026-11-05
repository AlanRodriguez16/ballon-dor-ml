"""
Descriptive visuals -- 2026 candidates overlaid on 14 years of history
==========================================================================
Two plots:
  1. Scatter: full historical dataset (gray=lost, red=won) with the 2026
     candidates plotted on top as gold stars -- shows at a glance whether
     each candidate's profile lands inside the historical "winner zone."
  2. Box plot of PAST WINNERS ONLY (goal_contributions and trophy_prestige_score),
     with each 2026 candidate's value overlaid as a point -- a more rigorous
     "does this profile fall within the normal range of past winners" check.

Uses REAL stats (v6 graded trophy_prestige_score, actual season goal_contributions)
-- not the v7 big-stage sensitivity-test numbers, to keep this an honest
descriptive picture rather than mixing in the hypothetical weighting.
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("historical_candidates_v6.csv")

candidates_2026 = pd.DataFrame([
    ["Lamine Yamal",     45, 17.0],
    ["Kylian Mbappe",    59,  3.0],
    ["Harry Kane",       75, 15.0],
    ["Michael Olise",    56, 14.0],
    ["Ousmane Dembele",  27, 18.0],
    ["Jude Bellingham",  20,  4.0],
], columns=["player", "goal_contributions", "trophy_prestige_score"])

# ---------------------------------------------------------------------------
# PLOT 1: Full scatter, 2026 candidates overlaid
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 7))

losers = df[df["won_balon_dor"] == 0]
winners = df[df["won_balon_dor"] == 1]

ax.scatter(losers["goal_contributions"], losers["trophy_prestige_score"],
           alpha=0.35, s=45, color="#94a3b8", label="Historical: didn't win", zorder=1)
ax.scatter(winners["goal_contributions"], winners["trophy_prestige_score"],
           alpha=0.85, s=80, color="#dc2626", edgecolors="black",
           label="Historical: won Ballon d'Or", zorder=2)

# 2026 candidates as gold stars, larger and on top
ax.scatter(candidates_2026["goal_contributions"], candidates_2026["trophy_prestige_score"],
           marker="*", s=350, color="#facc15", edgecolors="black", linewidths=1.0,
           label="2026 candidate", zorder=3)

for _, row in candidates_2026.iterrows():
    ax.annotate(row["player"], (row["goal_contributions"], row["trophy_prestige_score"]),
                fontsize=10, fontweight="bold", xytext=(8, 6), textcoords="offset points")

ax.set_xlabel("Goal Contributions (Goals + Assists)")
ax.set_ylabel("Trophy Prestige Score")
ax.set_title("2026 Ballon d'Or Candidates vs. 14 Years of History")
ax.legend(loc="upper left")
plt.tight_layout()
plt.savefig("scatter_2026_overlay.png", dpi=150)
plt.close()
print("Saved scatter_2026_overlay.png")

# ---------------------------------------------------------------------------
# PLOT 2: Box plot of PAST WINNERS ONLY, 2026 candidates overlaid as points
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

for ax, col, title in zip(
    axes,
    ["goal_contributions", "trophy_prestige_score"],
    ["Goal Contributions", "Trophy Prestige Score"],
):
    ax.boxplot(winners[col], positions=[0], widths=0.5, patch_artist=True,
               boxprops=dict(facecolor="#fecaca"), medianprops=dict(color="black"))
    # jitter the 2026 candidates slightly on the x-axis so labels don't overlap
    import numpy as np
    rng = np.random.default_rng(42)
    jitter = rng.uniform(-0.15, 0.15, size=len(candidates_2026))
    ax.scatter(jitter, candidates_2026[col], marker="*", s=350,
               color="#facc15", edgecolors="black", linewidths=1, zorder=3)
    for x, (_, row) in zip(jitter, candidates_2026.iterrows()):
        ax.annotate(row["player"].split()[-1], (x, row[col]), fontsize=8,
                    xytext=(6, 0), textcoords="offset points")
    ax.set_xticks([0])
    ax.set_xticklabels([f"Past winners\n(n={len(winners)})"])
    ax.set_title(f"{title}: Past Winners vs. 2026 Candidates")
    ax.set_ylabel(title)

plt.tight_layout()
plt.savefig("boxplot_winners_vs_2026.png", dpi=150)
plt.close()
print("Saved boxplot_winners_vs_2026.png")
