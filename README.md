# Smart Home Analytics: Energy Profiling and Benchmarking

Intern project (Project A) for the Smart Home Analytics data science internship, September 2026.

The consulting team needs to profile 500 smart homes by appliance-level energy use, group them into usage segments, and show how any home compares with its peers. This repository contains the data exploration and the segmentation analysis behind the dashboard.

## Key findings


## Repository structure

```
├── README.md              this file
├── requirements.txt       Python libraries for the whole project
├── .gitignore             keeps data files out of the repository
├── data/
│   ├── raw/               put the Kaggle CSV here (not committed)
│   └── processed/         outputs created by the notebooks (not committed)
├── docs/                  project brief (only if the repository is private)
├── 01_EDA/
│   └── 01_Data_overview.ipynb   data checks and exploration
├── 02_KMeans/
│   └── 02_K-means.ipynb   K-means segmentation, tested against shuffled data
├── 03_GMM/
│   └── 03_GMM.py          Gaussian Mixture Model segmentation
└── 04_Hierarchical/
    └── 04_Hierarchical.ipynb    hierarchical clustering
```

## Setup (once per computer)

1. Install Python 3.12 or later.
2. From the repository root, install the libraries:
   ```
   python -m pip install -r requirements.txt
   ```
   `requirements.txt` should list: `pandas`, `numpy`, `matplotlib`, `scikit-learn`.
3. Download the dataset from [Kaggle: Smart Home Energy Consumption](https://www.kaggle.com/datasets/mexwell/smart-home-energy-consumption) and save `smart_home_energy_consumption_large.csv` in `data/raw/`.

## How to run

Run the folders in order: `01_EDA` → `02_KMeans` → `03_GMM`. **Run each file from inside its own folder**, because the code uses paths such as `../data/raw/`.

- **K-means:** open `02_KMeans/02_K-means.ipynb` in Jupyter and choose Restart & Run All. The shuffle tests take a few minutes.
- **GMM:** from a terminal:
  ```
  cd 03_GMM
  python 03_GMM.py
  ```
  Each chart opens in a window and pauses the script; close it to continue.

## Data

- **Source:** [Smart Home Energy Consumption](https://www.kaggle.com/datasets/mexwell/smart-home-energy-consumption) (Kaggle).
- **Size:** 100,000 readings, 500 homes, about 200 readings per home (157 to 245).
- **Fields:** Home ID, Appliance Type, Energy Consumption (kWh), Date, Time, Outdoor Temperature (°C), Season, Household Size.
- **Quality:** no missing values and no duplicate rows. The data has **10** appliance types (the project brief says 9): Air Conditioning, Computer, Dishwasher, Fridge, Heater, Lights, Microwave, Oven, TV, Washing Machine.

## Method (shared by all models)

1. **One row per home.** Each home is described by its mean kWh per reading for each of the 10 appliances (500 × 10 table). Means are used rather than totals because homes have different numbers of readings.
2. **Standardise** each column (mean 0, standard deviation 1), so large appliances such as Air Conditioning (about 3.5 kWh) do not outweigh small ones such as Fridge (about 0.3 kWh).
3. **Fit the model** for a range of segment counts (k).
4. **Test whether the segments are meaningful.** A segment counts as meaningful only if it is:
   - clearer than segments found in shuffled data (Home IDs shuffled, table rebuilt),
   - stable when the analysis is repeated with different random seeds (adjusted Rand index, ARI),
   - describable in plain language.

## Results by model

| | K-means | Gaussian Mixture Model |
|---|---|---|
| Folder | `02_KMeans` | `03_GMM` |
| k tested | 2 to 8 | 1 to 8 |
| How k was judged | Silhouette, inertia | BIC (lower is better) |
| Best k according to the data | None (silhouette flat at 0.075 to 0.080, no elbow) | k = 1 (BIC rises steadily from 14,545 at k = 1 to 16,574 at k = 8) |
| Working choice | k = 3 (184 / 175 / 141 homes) | k = 2 (253 / 247 homes), the lowest BIC once k ≥ 2 |
| Silhouette | 0.076 at k = 3 | 0.058 at k = 2 |
| Better than shuffled data? | Silhouette: no for k = 2 to 4, marginal at k = 5 (p = 0.05, about 0.20 after correction). Stability: no after correction (p × 3 = 0.535, 0.059, 0.089 for k = 2, 3, 5) | Stability at k = 3: no (p = 0.921) |
| Output | `home_features.csv`, `home_segments.csv` | `segments_gmm.csv` |

### K-means

- Silhouette is 0.075 to 0.080 for every k from 2 to 8, far below 0.25.
- Stability across seeds is not clearly above shuffled data once the three values of k tested are taken into account.
- A sensitivity check using each appliance's share of the home's total energy gives slightly higher silhouette (0.084 to 0.102), but shuffled data score about the same (p = 0.25 and 0.35), so mean kWh per reading stays the main feature table.
- **k = 3 is used as the working segmentation** because the groups are balanced and describable, not because the data favour it. k = 2 would be equally defensible.

| Segment | Homes | Description (relative to the average home) |
|---|---|---|
| AC and laundry-leaning | 184 | Higher Air Conditioning, Washing Machine and TV |
| Lower appliance use | 175 | Lower Washing Machine, Oven, TV, Fridge and Lights |
| Fridge, lights and oven-leaning | 141 | Higher Fridge, Lights and Oven; lower Air Conditioning and Dishwasher |

Random seeds used:

| Step | Seed | Shuffles |
|---|---|---|
| Silhouette scan, k = 2 to 8 | `random_state = 42` | not applicable |
| Shuffled baseline for silhouette (k = 2 to 5) | 42 | 30; k = 5 repeated with 200 |
| Cluster labels, profiles, stability of real data | `random_state = 0`, stability seeds 1 to 10 | not applicable |
| Stability baseline | 7 (one shuffle) and 123 | 1, then 100 |
| Share-of-total sensitivity check (k = 2, 3) | 42 | 100 |

### Gaussian Mixture Model

- Settings: full covariance, 5 starting points per fit, `reg_covar = 1e-4`, `random_state = 42`.
- BIC is lowest at k = 1, meaning one group fits the data better than any split. The script still fits k = 2 so the segments can be compared with K-means; set `K_OVERRIDE` in the script to choose another k.
- At k = 2, average membership probability is 0.857, and 49 homes are borderline (probability below 0.6).
- Segment 1 (253 homes) is lower on Air Conditioning and higher on Dishwasher and Lights; Segment 2 (247 homes) is the reverse.
- The stability result (p = 0.921 at k = 3) comes from a separate run and is not produced by `03_GMM.py`.

## Outputs

All outputs are written to `data/processed/` and are not stored in the repository. Run the code to create them.

| File | Created by | Contents |
|---|---|---|
| `home_features.csv` | K-means notebook | 500 homes × 10 appliances (mean kWh per reading), plus `n_readings` and `avg_kwh` |
| `home_segments.csv` | K-means notebook | Features plus `cluster` (0 to 2) and `segment_name` (k = 3). Not used by the dashboard |
| `segments_gmm.csv` | GMM script | Features plus `segment`, `membership_prob` and one probability column per segment |

## Limitations

- The dataset appears synthetic (no seasonal pattern, household size changes within every home), so the findings may not apply to real households.
- Segments are a descriptive grouping, not distinct household types. Segment labels are arbitrary and depend on the random seed.
- ARI values can only be compared with the shuffled baseline for the same k, not across different k.

## Adapting to a new dataset

The analysis needs one row per reading with a home ID, an appliance type and an energy value. To use another dataset:

1. Save it in `data/raw/` and change the file name at the top of each notebook or script.
2. If its column names differ, rename them to match: `Home ID`, `Appliance Type`, `Energy Consumption (kWh)`.
3. Rerun the shuffle tests before trusting any segments. Real data may show clearer groups than this dataset.
