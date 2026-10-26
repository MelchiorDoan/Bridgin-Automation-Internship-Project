# K-means segmentation

K-means clustering of the 500 homes by appliance-level consumption, tested against shuffled data.

- **Notebook:** `02_K-means.ipynb`
- **Input:** the Kaggle data file.
- **Output:** `home_features.csv` (500 homes x 10 appliances, mean kWh per reading, plus `n_readings` and `avg_kwh`) and `home_segments.csv` (k = 3 labels), both written to `data/processed/`. These files are not stored in this repository; run the notebook to create them.
- **Requires:** pandas, numpy, matplotlib, scikit-learn (see `requirements.txt` in the repository root).

## Method
1. Build one row per home: mean kWh per reading for each appliance, standardized before clustering.
2. Fit k-means for k = 2 to 8 and compare silhouette scores.
3. Compare silhouette scores with 100 or more shuffled datasets (Home ID shuffled, table rebuilt).
4. Measure stability across random seeds (ARI) and compare with shuffled data.
5. Profile the clusters for k = 2, 3 and 5.
6. Sensitivity check: share of total energy per appliance instead of mean kWh per reading.

## Random seeds and shuffles
| Step | Seed | Shuffles |
|---|---|---|
| Silhouette scan, k = 2 to 8 | `random_state = 42` | not applicable |
| Shuffled baseline for silhouette (k = 2 to 5) | 42 | 30; k = 5 repeated with 200 |
| Cluster labels, profiles, stability of real data | `random_state = 0`, stability seeds 1 to 10 | not applicable |
| Stability baseline | 7 (one shuffle) and 123 | 1, then 100 |
| Share-of-total sensitivity check (k = 2, 3) | 42 | 100 |

## Main results
- Silhouette is 0.075 to 0.080 for every k from 2 to 8 and no elbow appears, far below 0.25.
- The real silhouette is not above shuffled data for k = 2 to 4. For k = 5 it is marginal (p = 0.05; about 0.20 after correcting for four values of k).
- Stability across seeds is not clearly above shuffled data after correcting for three values of k (p x 3 = 0.535, 0.059 and 0.089 for k = 2, 3 and 5).
- Differences between clusters are small (at most about 0.2 kWh per reading on any appliance).
- Share-of-total features give higher silhouette (0.084 to 0.102), but shuffled data score about the same (p = 0.25 and 0.35), so mean kWh per reading remains the primary feature table.
- **Working choice:** k = 3 (184 / 175 / 141 homes) for balanced, describable groups, not because the data favour it. k = 2 would be an equally defensible choice.

## Limitation
The dataset appears synthetic, so the segments are a descriptive grouping and not distinct household types. ARI values are only comparable with the shuffled baseline for the same k.
