# =============================================================================
# 2026 Ballon d'Or Candidates vs. 14 Years of History -- R version
# =============================================================================
# Mirrors descriptive_2026_overlay.py: a scatter plot of the full historical
# dataset with the 2026 candidates overlaid, and a box plot of PAST WINNERS
# ONLY with the 2026 candidates plotted on top to show whether each one's
# profile falls inside the normal range for a winner.
#
# HOW TO RUN:
#   1. Have R + RStudio installed (see earlier setup instructions)
#   2. Put historical_candidates_v6.csv in the same folder as this script
#   3. First time only: install.packages(c("tidyverse", "ggrepel", "ggthemes"))
#   4. Open in RStudio, click "Source"
#
# NOTE: I don't have R available in my own environment to test-run this --
# if anything errors, paste the message here and I'll fix it with you.
# =============================================================================

library(tidyverse)
library(ggthemes)  # for theme_clean()
library(ggrepel)   # for non-overlapping labels

# -----------------------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------------------
df <- read_csv("historical_candidates_v6.csv")

candidates_2026 <- tribble(
  ~player,             ~goal_contributions, ~trophy_prestige_score,
  "Lamine Yamal",       45,                  17.0,
  "Kylian Mbappe",      59,                   3.0,
  "Harry Kane",         75,                  15.0,
  "Michael Olise",      56,                  14.0,
  "Ousmane Dembele",    27,                  18.0,
  "Jude Bellingham",    20,                   4.0
)

# -----------------------------------------------------------------------------
# PLOT 1: Full scatter, 2026 candidates overlaid
# -----------------------------------------------------------------------------
# Note: ggplot2 doesn't have a built-in filled "star" shape without the extra
# ggstar package, so we use shape 23 (a filled diamond) instead -- same idea,
# one less dependency to install.
# This plot is DISPLAYED in R (Plots pane / console), not saved to a file --
# see the print() call at the bottom of this block.

scatter_plot <- ggplot() +
  geom_point(data = filter(df, won_balon_dor == 0),
             aes(x = goal_contributions, y = trophy_prestige_score),
             color = "#9CA3AF", alpha = 0.5, size = 2.6) +
  geom_point(data = filter(df, won_balon_dor == 1),
             aes(x = goal_contributions, y = trophy_prestige_score),
             fill = "#E11D48", shape = 21,
             size = 3.6, color = "white", stroke = 0.7) +
  geom_point(data = candidates_2026,
             aes(x = goal_contributions, y = trophy_prestige_score),
             shape = 23, size = 6.5, fill = "#FBBF24", color = "black", stroke = 0.9) +
  geom_text_repel(data = candidates_2026,
                   aes(x = goal_contributions, y = trophy_prestige_score, label = player),
                   fontface = "bold", size = 3.6, seed = 42,
                   box.padding = 0.6, point.padding = 0.3,
                   segment.color = "grey50", segment.size = 0.3) +
  labs(title = "2026 Ballon d'Or Candidates vs. 14 Years of History",
       subtitle = "Grey = didn't win \u00b7 Red = won Ballon d'Or \u00b7 Gold = 2026 candidate",
       x = "Goal Contributions (Goals + Assists)",
       y = "Trophy Prestige Score") +
  theme_clean(base_size = 13) +
  theme(
    legend.position = "none",
    plot.title = element_text(face = "bold", size = 15),
    plot.subtitle = element_text(color = "grey35", size = 10.5, margin = margin(b = 12)),
    axis.title = element_text(face = "bold", size = 11),
    plot.background = element_rect(color = NA)
  )

# Display in R (Plots pane in RStudio) instead of saving to a file
print(scatter_plot)

# -----------------------------------------------------------------------------
# PLOT 2: Box plot of PAST WINNERS ONLY, 2026 candidates overlaid
# -----------------------------------------------------------------------------
winners <- df %>% filter(won_balon_dor == 1)

# Reshape to long format so both metrics can share one faceted plot
winners_long <- winners %>%
  select(player, goal_contributions, trophy_prestige_score) %>%
  pivot_longer(cols = c(goal_contributions, trophy_prestige_score),
               names_to = "metric", values_to = "value") %>%
  mutate(metric = recode(metric,
                          goal_contributions = "Goal Contributions",
                          trophy_prestige_score = "Trophy Prestige Score"))

candidates_long <- candidates_2026 %>%
  pivot_longer(cols = c(goal_contributions, trophy_prestige_score),
               names_to = "metric", values_to = "value") %>%
  mutate(metric = recode(metric,
                          goal_contributions = "Goal Contributions",
                          trophy_prestige_score = "Trophy Prestige Score"))

set.seed(42)  # so the jitter is reproducible
box_plot <- ggplot(winners_long, aes(x = "Past winners (n=14)", y = value)) +
  geom_boxplot(fill = "#fecaca", width = 0.5, outlier.shape = 1) +
  geom_jitter(data = candidates_long, width = 0.15, height = 0,
              shape = 23, size = 5, fill = "#facc15", color = "black", stroke = 1) +
  geom_text_repel(data = candidates_long,
                   aes(x = "Past winners (n=14)", y = value,
                       label = word(player, -1)),
                   size = 3, seed = 42) +
  facet_wrap(~ metric, scales = "free_y") +
  labs(title = "Past Winners vs. 2026 Candidates", x = NULL, y = NULL) +
  theme_minimal(base_size = 12)

# Display in R (Plots pane in RStudio) instead of saving to a file
print(box_plot)
