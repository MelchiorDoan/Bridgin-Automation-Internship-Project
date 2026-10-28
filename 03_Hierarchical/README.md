# Hierarchical clustering

Hierarchical clustering (Ward linkage) of the 500 homes by appliance-level consumption, tested against shuffled data.

- **Notebook:** `03_hierarchical.ipynb`
- **Input:** the Kaggle data file, `home_features.csv` and `home_segments.csv` (created by `KMeans/02_segmentation.ipynb`). None is stored in this repository; run the K-means notebook first.
- **Requires:** pandas, numpy, matplotlib, scipy, scikit-learn (see `requirements.txt` in the repository root).

## Method
1. Use the same standardized table as K-means: mean kWh per reading for each appliance, 500 homes x 10 appliances.
2. Build the Ward merge tree and inspect the dendrogram. Ward merges the two clusters whose union increases within-cluster variance the least, which gives compact groups and keeps results comparable with K-means.
3. Compute silhouette for k = 2 to 8 and compare with 100 shuffled datasets (Home IDs shuffled, table rebuilt).
4. Test stability by clustering a random 80% of the homes and comparing with the clustering of all homes (adjusted Rand index), and repeat on 100 shuffled datasets. Hierarchical clustering has no random start, so stability is tested by removing homes instead of changing a seed.
5. Compare with the K-means grouping (k = 3) and with 100 shuffled datasets.

## Random seeds and shuffles
Hierarchical clustering has no randomness. Seeds are used only for shuffles and subsamples.

| Step | Seed | Repeats |
|---|---|---|
| Dendrogram baseline (top merge ratio) | 42 | 100 shuffles |
| Silhouette baseline, k = 2 to 5 | 42 | 100 shuffles |
| Stability on 80% subsamples, k = 3 and 5 | 0 for subsamples, 42 for shuffles | 15 subsamples per run, 100 shuffles |
| Agreement with K-means (k = 3) | 42 for shuffles; K-means `random_state = 0` | 100 shuffles |

## Main results
- The dendrogram shows no sharp break: the last merges are at about 22.4, 20.0, 19.4 and 18.4. The top merge ratio is not different from shuffled trees (p = 0.347).
- Silhouette is 0.033 to 0.053 for k = 2 to 8, below K-means and far below 0.25. It is not distinguishable from shuffled data for k = 2, 3 and 4 (p = 0.26 to 0.60); k = 5 is marginal (p = 0.05, about 0.20 after correcting for four values of k).
- Stability on 80% subsamples is not higher than on shuffled data (k = 3: p = 0.455; k = 5: p = 0.109), and absolute ARI is very low (0.10 to 0.17).
- Agreement with K-means (k = 3) is ARI 0.105 against a shuffled mean of 0.119 (p = 0.535).

## Limitation
The dataset appears simulated, so these results describe this dataset only. ARI values are only comparable with the shuffled baseline for the same test, not across methods.
