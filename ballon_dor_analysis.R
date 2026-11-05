# =============================================================================
# Ballon d'Or Project -- R version
# =============================================================================
# Mirrors the Python analysis: logistic regression summary table, scatter
# plot, and box plots. Uses the SAME data (historical_candidates_v6.csv)
# so results should match the statsmodels output almost exactly.
#
# HOW TO RUN THIS:
#   1. Install R:        https://cran.r-project.org  (pick your OS, install)
#   2. Install RStudio:  https://posit.co/download/rstudio-desktop/ (free,
#      much friendlier than the plain R console -- has a Run button, no
#      terminal/PATH headaches like Python gave you)
#   3. Open this .R file in RStudio
#   4. Put historical_candidates_v6.csv in the SAME FOLDER as this script
#   5. Click "Source" (top-right of the script pane) or select-all + Ctrl/Cmd+Enter
#
# FIRST TIME ONLY -- install the packages this script needs:
#   install.packages(c("tidyverse", "readxl"))
# (tidyverse includes ggplot2 for plotting and dplyr for data wrangling)
# =============================================================================

library(tidyverse)   # ggplot2, dplyr, readr -- the standard R data toolkit

# -----------------------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------------------
# Option A: use the dataset already built (recommended -- matches the Python results)
df <- read_csv("historical_candidates_v6.csv")

# Option B: if you want to work from your ORIGINAL Excel file instead, uncomment:
# library(readxl)
# raw <- read_excel("Balon_de_Oro_2026_estadisticas.xlsx", sheet = "Resumen")

# Make position dummies into factors (R's version of one-hot, handled automatically
# by glm() when you pass a factor column -- cleaner than doing it by hand)
df <- df %>% mutate(position = as.factor(position))

# -----------------------------------------------------------------------------
# 1. LOGISTIC REGRESSION -- classic textbook summary table
# -----------------------------------------------------------------------------
model <- glm(
  won_balon_dor ~ goal_contributions + trophy_prestige_score + position,
  data = df,
  family = binomial(link = "logit")
)

cat("=====================================================\n")
cat("LOGISTIC REGRESSION SUMMARY (R glm)\n")
cat("=====================================================\n")
print(summary(model))

# McFadden's pseudo R-squared (R doesn't print this by default -- compute manually)
null_model <- glm(won_balon_dor ~ 1, data = df, family = binomial)
mcfadden_r2 <- 1 - (logLik(model) / logLik(null_model))
cat(sprintf("\nMcFadden's Pseudo R-squared: %.3f\n", mcfadden_r2))
cat("(0.2-0.4 is generally considered a strong fit for logistic regression)\n")

# Save the summary to a text file
sink("regression_summary_R.txt")
print(summary(model))
cat(sprintf("\nMcFadden's Pseudo R-squared: %.3f\n", mcfadden_r2))
sink()

# -----------------------------------------------------------------------------
# 2. SCATTER PLOT -- ggplot2 version
# -----------------------------------------------------------------------------
scatter_plot <- ggplot(df, aes(x = goal_contributions, y = trophy_prestige_score)) +
  geom_point(aes(color = factor(won_balon_dor), size = factor(won_balon_dor)),
             alpha = 0.7) +
  scale_color_manual(values = c("0" = "#94a3b8", "1" = "#dc2626"),
                      labels = c("Didn't win", "Won Ballon d'Or"),
                      name = NULL) +
  scale_size_manual(values = c("0" = 2, "1" = 4), guide = "none") +
  geom_text(data = filter(df, won_balon_dor == 1),
            aes(label = paste0(word(player, -1), " '", substr(year, 3, 4))),
            hjust = -0.15, vjust = -0.3, size = 3) +
  labs(title = "Ballon d'Or Candidates: Output vs. Team Success (2011-2025)",
       x = "Goal Contributions (Goals + Assists)",
       y = "Trophy Prestige Score") +
  theme_minimal() +
  theme(legend.position = "bottom")

ggsave("scatter_R.png", scatter_plot, width = 9, height = 6, dpi = 150)
cat("\nSaved scatter_R.png\n")

# -----------------------------------------------------------------------------
# 3. BOX PLOTS -- ggplot2 version
# -----------------------------------------------------------------------------
box_winloss <- ggplot(df, aes(x = factor(won_balon_dor), y = goal_contributions)) +
  geom_boxplot(fill = "#93c5fd") +
  labs(title = "Goal Contributions: Winners vs. Non-Winners",
       x = "Won Ballon d'Or (0 = No, 1 = Yes)", y = "Goal Contributions") +
  theme_minimal()

box_position <- ggplot(df, aes(x = position, y = goal_contributions)) +
  geom_boxplot(fill = "#86efac") +
  labs(title = "Goal Contributions by Position",
       x = "Position", y = "Goal Contributions") +
  theme_minimal()

ggsave("boxplot_winloss_R.png", box_winloss, width = 6, height = 5, dpi = 150)
ggsave("boxplot_position_R.png", box_position, width = 6, height = 5, dpi = 150)
cat("Saved boxplot_winloss_R.png and boxplot_position_R.png\n")

cat("\nAll done. Outputs: regression_summary_R.txt, scatter_R.png, boxplot_winloss_R.png, boxplot_position_R.png\n")
