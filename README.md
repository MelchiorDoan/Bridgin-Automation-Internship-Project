# Smart Home Analytics: Energy Profiling and Benchmarking

Intern project (Project A) for the Smart Home Analytics data science internship, September 2026.

The consulting team needs to profile 500 smart homes by appliance-level energy use, group them into usage segments, and show how any home compares with the other homes. This repository holds the data exploration and the three segmentation models (K-means, Gaussian Mixture, Hierarchical) behind the dashboard.

## Key findings

- **Appliance type is the only clear difference in the data.** Air Conditioning and Heater use about 3.5 kWh per reading, seven appliances about 1.1 kWh, and the Fridge about 0.3 kWh.
- **Homes look alike.** Differences between homes are consistent with chance. Energy use does not change with season, outdoor temperature, time of day or household size.
- **None of the three models finds clear household groups.** Silhouette scores are 0.033 to 0.080 (a score below 0.25 means little structure), and none is clearly better than shuffled data once the number of tests is taken into account. The Gaussian Mixture BIC is lowest at k = 1, so one group fits best.
- **The Gaussian Mixture groups do not repeat.** When each home's readings are split into two random halves and the model is fitted on each, the two groupings agree no better than chance (mean ARI -0.002 over 10 repeats).
- **Recommendation:** compare each home with all 500 homes, appliance by appliance, as the main view. Show segments only as a labelled, descriptive extra, not as distinct household types. The dashboard follows this and does not use the segments.
- **The data appears simulated** (no seasonal pattern, household size changes within every home), so these findings may not apply to real homes.

## Repository structure

```
├── README.md
├── requirements.txt          Python libraries for the whole project
├── Data_Team_Smart Home Analytics_Risk Register.xlsx   project risk register
├── data/
│   ├── raw/                  the Kaggle CSV
│   └── processed/            outputs created by the notebooks and script
├── 01_EDA/
│   ├── 01_Data_overview.ipynb      data checks and exploration
│   └── README.md
├── 02_KMeans/
│   ├── 02_K-means.ipynb            K-means segmentation, tested against shuffled data
│   └── README.md
├── 03_GMM/
│   ├── 03_GMM.py                   Gaussian Mixture segmentation and stability check
│   └── requirements.txt
└── 04_Hierarchical/
    ├── 04_Hierarchical.ipynb       Ward hierarchical clustering
    └── README.md
```

The Power BI dashboard is built separately and is not stored in this repository.

## Setup (once per computer)

1. Install Python 3.12 or later.
2. From the repository root, install the libraries:
   ```
   python -m pip install -r requirements.txt
   ```
   This installs `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `scipy` and `ipykernel`. To open the notebooks in a browser, also install `jupyter`; VS Code works with `ipykernel`.
3. The dataset is already in `data/raw/`. If it is missing, download `smart_home_energy_consumption_large.csv` from [Kaggle: Smart Home Energy Consumption](https://www.kaggle.com/datasets/mexwell/smart-home-energy-consumption) and save it there.

## How to run

**Run each file from inside its own folder**, because the code uses paths such as `../data/raw/`. The folder name `data` must be lowercase.

| Step | Folder | How to run | Notes |
|---|---|---|---|
| 1 | `01_EDA` | Open `01_Data_overview.ipynb`, Restart & Run All | Includes permutation tests |
| 2 | `02_KMeans` | Open `02_K-means.ipynb`, Restart & Run All | The shuffle tests take a few minutes. Creates `home_features.csv` and `home_segments.csv` |
| 3 | `03_GMM` | `cd 03_GMM`, then `python 03_GMM.py` | Each chart opens in a window and pauses the script; close it to continue. Step 8 (stability) takes a little longer than the other steps |
| 4 | `04_Hierarchical` | Open `04_Hierarchical.ipynb`, Restart & Run All | Needs the two CSV files created in step 2 |

## Data

- **Source:** [Smart Home Energy Consumption](https://www.kaggle.com/datasets/mexwell/smart-home-energy-consumption) (Kaggle).
- **Size:** 100,000 readings, 500 homes, about 200 readings per home (157 to 245). Readings run from 1 January 2023 to 1 January 2024.
- **Fields:** Home ID, Appliance Type, Energy Consumption (kWh), Date, Time, Outdoor Temperature (°C), Season, Household Size.
- **Quality:** no missing values and no duplicate rows. The data has **10** appliance types (the project brief says 9): Air Conditioning, Computer, Dishwasher, Fridge, Heater, Lights, Microwave, Oven, TV, Washing Machine.

## Method (shared by all models)

1. **One row per home.** Each home is described by its mean kWh per reading for each of the 10 appliances (500 × 10 table). Means are used instead of totals because homes have different numbers of readings.
2. **Standardise** each column (mean 0, standard deviation 1), so large appliances such as Air Conditioning (about 3.5 kWh) do not outweigh small ones such as Fridge (about 0.3 kWh).
3. **Fit the model** for a range of segment counts (k).
4. **Test whether the segments are meaningful.** A segment counts as meaningful only if it is:
   - clearer than segments found in shuffled data,
   - stable when the analysis is repeated,
   - describable in plain language.

Each model uses a different stability test (see below), so stability scores should not be compared across models. ARI (adjusted Rand index) is 1 when two groupings are identical and about 0 when they agree no better than chance.

## Results by model

| | K-means | Gaussian Mixture | Hierarchical (Ward) |
|---|---|---|---|
| Folder | `02_KMeans` | `03_GMM` | `04_Hierarchical` |
| k tested | 2 to 8 | 1 to 8 | 2 to 8 |
| How k was judged | Silhouette, inertia | BIC (lower is better) | Dendrogram, silhouette |
| Best k according to the data | None (silhouette flat, no elbow) | k = 1 (BIC rises from 14,545 at k = 1 to 16,574 at k = 8) | None (no sharp break in the dendrogram) |
| Working choice | k = 3 (184 / 175 / 141 homes) | k = 2 (253 / 247 homes), the lowest BIC once k ≥ 2 | None (k = 3 used only to compare with K-means) |
| Silhouette | 0.075 to 0.080 | 0.058 at k = 2 | 0.033 to 0.053 |
| Compared with shuffled data | Silhouette: no for k = 2 to 4; marginal at k = 5 (p = 0.05, about 0.20 after correction) | Not tested in this script | Silhouette: no for k = 2 to 4 (p = 0.26 to 0.60); marginal at k = 5 (p = 0.05, about 0.20 after correction) |
| Stability test | Repeat with 10 different random seeds (ARI), compared with 100 shuffled datasets | Split each home's readings into two halves, fit on each, compare (ARI), 10 repeats | Cluster a random 80% of homes and compare with all homes (ARI), compared with 100 shuffled datasets |
| Stability result | Not above shuffled data after correction (p × 3 = 0.535, 0.059, 0.089 for k = 2, 3, 5) | Mean ARI -0.002 (no better than chance) | Not above shuffled data (k = 3: p = 0.455; k = 5: p = 0.109); ARI 0.10 to 0.17 |
| Output | `home_features.csv`, `home_segments.csv` | `segments_gmm.csv` | None |

### K-means

- Silhouette is 0.075 to 0.080 for every k from 2 to 8, far below 0.25.
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

### Gaussian Mixture Model

- Settings: full covariance, 5 starting points per fit, `reg_covar = 1e-4`, `random_state = 42`.
- BIC is lowest at k = 1, meaning one group fits better than any split. The script still fits k ≥ 2 so the groups can be compared with K-means; set `K_OVERRIDE` in the script to choose another k.
- At k = 2, average membership probability is 0.857 and 49 homes are borderline (probability below 0.6).
- Segment 1 (253 homes) is lower on Air Conditioning and higher on Dishwasher and Lights; Segment 2 (247 homes) is the reverse.
- Step 8 builds a feature table from each half of every home's readings, fits the same model on each, and compares the two groupings with ARI. A score near 0 means the groups change with the readings.

### Hierarchical clustering

- Ward linkage on the same standardised table. It has no random start, so stability is tested by removing homes instead of changing a seed.
- The dendrogram shows no sharp break (top merge not different from shuffled trees, p = 0.347).
- Agreement with the K-means groups (k = 3) is ARI 0.105 against a shuffled mean of 0.119 (p = 0.535).

## Outputs

All outputs are written to `data/processed/`.

| File | Created by | Contents |
|---|---|---|
| `home_features.csv` | K-means notebook | 500 homes × 10 appliances (mean kWh per reading), plus `n_readings` and `avg_kwh` |
| `home_segments.csv` | K-means notebook | Features plus `cluster` (0 to 2) and `segment_name` (k = 3). Not used by the dashboard |
| `segments_gmm.csv` | GMM script | Features plus `segment`, `membership_prob` and one probability column per segment |

`data/processed/` also holds `dim_home.csv`, `dim_appliance.csv`, `fact_energyconsumption.csv` and `fact_homeappliance.csv`, the tables used by the dashboard.

## Limitations

- The dataset appears synthetic, so the findings may not apply to real households.
- Segments are a descriptive grouping, not distinct household types. Segment labels are arbitrary and depend on the random seed.
- The three models use different stability tests, and the GMM script has no shuffled-data baseline yet, so the models are not compared on exactly the same footing.
- ARI values can only be compared with a shuffled baseline for the same k and the same test.

## Adapting to a new dataset

The analysis needs one row per reading with a home ID, an appliance type and an energy value. To use another dataset:

1. Save it in `data/raw/` and change the file name at the top of each notebook or script.
2. If its column names differ, rename them to match: `Home ID`, `Appliance Type`, `Energy Consumption (kWh)`.
3. Rerun the shuffle and stability tests before trusting any segments. Real data may show clearer groups than this dataset.
