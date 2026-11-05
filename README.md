# Predicting the 2026 Ballon d'Or Winner

An iterative machine learning project: a logistic regression model trained on 94 historical Ballon d'Or candidates (2011-2025) to estimate each 2026 contender's probability of winning. Built in Python (pandas, scikit-learn, statsmodels) with a matching descriptive analysis in R (tidyverse, ggplot2).

## Result: how the model did

The model was run in September 2026, before the October 26 ceremony. (This repo was published afterward, so the commit history can't prove the timing.) The actual outcome:

| Player | Model probability (v6) | Model rank (of 6) | Actual finish |
|---|---|---|---|
| Harry Kane | 95.6% | 1 | **1st (winner)** |
| Lamine Yamal | 84.9% | 2 | 3rd |
| Michael Olise | 82.9% | 3 | 9th |
| Ousmane Dembele | 70.5% | 4 | 7th |
| Kylian Mbappe | 20.5% | 5 | 2nd |
| Jude Bellingham | 4.5% | 6 | 11th |

Actual results: [Yahoo Sports top-10 rankings](https://sports.yahoo.com/articles/top-10-ballon-dor-rankings-235628080.html), [ESPN](https://www.espn.com/soccer/story/_/id/50236983/harry-kane-2026-ballon-dor-kylian-mbappe-lamine-yamal).

**What went right:** the model picked the winner and put Bellingham last of the six.

**What went wrong:** it badly underrated Mbappe (finished 2nd, model gave 20.5%) and overrated Olise (finished 9th). The model leans heavily on team trophies, and Mbappe had none this cycle despite a record-setting World Cup and Champions League scoring run. The `predict_ballon_dor_v7.py` sensitivity test, which gives extra credit for World Cup and Champions League output, moved Mbappe the most (+38 points), which points in the right direction. That is a hypothesis about one year, not a validated finding.

**Read this as one data point.** A correct winner in a single year, from a model trained on 94 rows, does not show the model is reliable. The model also only scored the six players in my source spreadsheet, so players who finished 4th-6th (Rodri, Messi, Kvaratskhelia) were never in the field.

## Approach

- **Model:** logistic regression (supervised, binary classification), L2-regularized (`C=0.5`), 5-fold cross-validated.
- **Features:** goal contributions (goals + assists), a trophy prestige score, player position, and two flags for changes to the award's rules.
- **Trophy prestige score:** a weighted sum where competitions count by importance (World Cup 10, Champions League 8, Premier League/La Liga 6, Bundesliga/Serie A 5, Ligue 1 4, and so on), with graded credit for how far a team went in the World Cup and Champions League (a runner-up finish counts for something; a group-stage exit doesn't).
- **Rule changes handled explicitly:** the voting panel changed to journalists only in 2016, and the assessment window moved from calendar year to full season in 2022. Both are model features instead of being ignored.

## How it evolved

| Step | Problem found | Fix |
|---|---|---|
| v1 | Baseline on 42 rows | -- |
| v2 | Ignored voting-rule changes | Added era flags |
| v3 | Overfit: two examples made assists look twice as important as goals | Combined feature and stronger regularization |
| v4 | A Bundesliga title counted the same as a World Cup | Prestige-weighted trophies |
| v5 | Only top-3 finalists per year | Expanded to 94 rows using real top-30 shortlists (2024, 2025), added positions |
| v6 | Binary "won it / didn't" credit | Graded tournament-depth scoring |
| v7 | -- | Sensitivity test for World Cup / Champions League output (not retrained) |

Cross-validated ROC-AUC rose from about 0.73 (v1-v4) to 0.90 (v6). **These scores are not strictly comparable across versions**, because the dataset grew from 42 to 94 rows along the way, so part of the gain comes from more data rather than better modeling.

## Repository contents

```
predict_ballon_dor_v6.py       Final trained model; prints 2026 predictions
predict_ballon_dor_v7.py       Sensitivity test on top of v6 (does not retrain)
big_stage_output.py            World Cup + Champions League output for 2026 candidates
build_full_dataset.py          Builds the 94-row historical dataset (positions, prestige)
build_stage_depth.py           Adds graded World Cup / Champions League depth -> v6 CSV
descriptive_stats.py           statsmodels logistic regression table, scatter, box plots
descriptive_2026_overlay.py    2026 candidates overlaid on historical winners (Python)
descriptive_2026_overlay.R     Same plots in R / ggplot2
ballon_dor_analysis.R          Logistic regression summary + plots in R
historical_candidates_v6.csv   Final dataset used by the model
figures/                       Output plots
docs/                          One-page project report (Word)
```

## Running it

```bash
pip install -r requirements.txt
python predict_ballon_dor_v6.py      # train model and print predictions
python predict_ballon_dor_v7.py      # sensitivity test
```

To rebuild the dataset from scratch first: `python build_full_dataset.py`, then `python build_stage_depth.py`.

For R: `install.packages(c("tidyverse", "ggrepel", "ggthemes"))`, then open `descriptive_2026_overlay.R` in RStudio and click Source. Keep `historical_candidates_v6.csv` in the same folder.

## Limitations

- **Small sample (94 rows).** Results are directional, not precise probabilities. Extreme outputs (like 95.6%) reflect how logistic regression behaves on small data, not real certainty.
- **Historical data is compiled by hand** from news coverage and general football knowledge. The 2024 and 2025 shortlists were checked against published rankings; stats for earlier years are approximate and not independently verified line by line.
- **Prestige weights are subjective** (for example World Cup = 10, Bundesliga = 5). They are reasoned judgment calls, not an objective standard.
- **Missing context:** the Champions League stage reached by Real Madrid and Barcelona in 2025-26 was not in the source data, so those candidates get no Champions League depth credit. Mbappe's score is probably understated because of this.
- **`descriptive_stats.py`** shows complete separation on the defender and goalkeeper dummies (no defender or goalkeeper has ever won in this dataset), which is why the scikit-learn model uses regularization.
- **v7 is not a trained model.** It reuses v6's coefficients and adds a hypothetical bonus; it was not validated against historical data.


