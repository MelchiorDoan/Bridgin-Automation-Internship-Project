# Smart Home Analytics: Energy Profiling and Benchmarking

Intern project (Project A) for the Smart Home Analytics data science internship, September to November 2026.

The consulting team needs to profile 500 smart homes by appliance-level energy use, group them into usage segments, and show how any home compares with the other homes. This repository holds the data checks, the three segmentation models (K-means, Gaussian Mixture, Hierarchical), the Power BI dashboard, the cost analysis and the reports.

## Key findings

- **Appliance type is the only clear difference in the data.** Air Conditioning and Heater use about 3.5 kWh per measurement, seven appliances about 1.1 kWh, and the Fridge about 0.3 kWh.
- **Homes look alike.** Differences between homes are consistent with chance. Energy use does not change with season, outdoor temperature, time of day or household size.
- **None of the three models finds clear household groups.** Silhouette scores are 0.033 to 0.080 (a score below 0.25 means little structure), and none is clearly better than shuffled data once the number of tests is taken into account. The Gaussian Mixture BIC is lowest at k = 1, so one group fits best.
- **The Gaussian Mixture groups do not repeat.** When each home's readings are split into two random halves and the model is fitted on each, the two groupings agree no better than chance (mean ARI -0.002 over 10 repeats).
- **The models agree only very weakly with each other.** K-means and Gaussian Mixture groups match with ARI 0.09 (about 0.00 for shuffled labels). This is above shuffled labels but far from a match (1 would be identical groups).
- **On one common test, no model passes.** `08_Compare` gives all three models the same silhouette and split-half stability tests, each against the same 100 shuffled datasets. None scores better than shuffled data (silhouette 0.076, 0.058, 0.038; split-half ARI about 0 for all three).
- **Recommendation:** compare each home with all 500 homes, appliance by appliance, as the main view. Show segments only as a labelled, descriptive extra, not as distinct household types. The dashboard follows this: its home table carries the K-means segment, but no dashboard page shows it.
- **Cost:** at a flat 33 cents per kWh, an average measurement costs about $0.495. Air Conditioning and Heater make up about 47% of estimated cost.
- **The data appears simulated** (no seasonal, time-of-day or temperature pattern, and household size changes within every home), so these findings may not apply to real homes.

## Repository structure

```
├── README.md
├── requirements.txt                    Python libraries for the whole project
├── Data_Team_Smart Home Analytics_Risk Register.xlsx   project risk register
├── data/
│   ├── raw/                            the Kaggle CSV
│   └── processed/                      tables created by the notebooks (see Outputs)
├── 01_EDA/
│   ├── 01_Data_overview.ipynb          data checks and exploration
│   └── README.md
├── 02_KMeans/
│   ├── 02_Kmeans.ipynb                 K-means segmentation, tested against shuffled data
│   └── README.md
├── 03_GMM/
│   ├── 03_GMM.ipynb                    Gaussian Mixture segmentation, stability check, agreement with K-means
│   └── requirements.txt
├── 04_Hierarchical/
│   ├── 04_Hierarchical.ipynb           Ward hierarchical clustering
│   └── README.md
├── 05_Dashboard/
│   ├── 05_Dashboard.ipynb              creates the tables used by Power BI
│   ├── README.md
│   └── powerbi/
│       ├── Smart Home Energy_Dashboard.pbix    Power BI file
│       ├── Smart Home Energy_Dashboard.pdf     the five dashboard pages
│       └── measures.md                         parameter and DAX measures
├── 06_Cost/
│   ├── 06_Cost_analysis.ipynb          cost at a flat rate and the 50-home sample portfolio
│   └── README.md
├── 07_Time_checks/
│   ├── 07_Time_checks.ipynb            spacing of measurements, time of day, temperature
│   └── README.md
├── 08_Compare/
│   ├── 08_Compare.ipynb                the three models on the same tests and the same shuffled data
│   └── README.md
└── reports/
    ├── README.md                       key figures and how the reports are produced
    └── Smart Home Energy Sample Portfolio of 50 Units.pdf    sample client report
```

## Setup (once per computer)

1. Install Python 3.12 or later.
2. From the repository root, install the libraries:
   ```
   python -m pip install -r requirements.txt
   ```
   This installs `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `scipy` and `ipykernel`. To open the notebooks in a browser, also install `jupyter`; VS Code works with `ipykernel`.
3. The dataset is already in `data/raw/`. If it is missing, download `smart_home_energy_consumption_large.csv` from [Kaggle: Smart Home Energy Consumption](https://www.kaggle.com/datasets/mexwell/smart-home-energy-consumption) and save it there.
4. To open the dashboard, install Power BI Desktop (Windows) and open `05_Dashboard/powerbi/Smart Home Energy_Dashboard.pbix`.

## How to run

Open each notebook and choose **Restart & Run All**. The notebooks use paths such as `../data/raw/`, so keep the folder structure as it is and keep the folder name `data` in lowercase. Run the notebooks in the order below, because later ones read files created by earlier ones.

| Step | Folder | Notebook | Needs | Notes |
|---|---|---|---|---|
| 1 | `01_EDA` | `01_Data_overview.ipynb` | raw data | Includes permutation tests |
| 2 | `02_KMeans` | `02_Kmeans.ipynb` | raw data | The shuffle tests take a few minutes. Creates `home_features.csv` and `home_segments.csv` |
| 3 | `03_GMM` | `03_GMM.ipynb` | raw data; Step 9 also needs `home_segments.csv` from step 2 | Step 8 (stability) takes a little longer. Creates `segments_gmm.csv` |
| 4 | `04_Hierarchical` | `04_Hierarchical.ipynb` | `home_features.csv`, `home_segments.csv` from step 2 | Creates no files |
| 5 | `05_Dashboard` | `05_Dashboard.ipynb` | raw data, files from step 2 | Creates the four tables used by Power BI |
| 6 | `06_Cost` | `06_Cost_analysis.ipynb` | `fact_energyconsumption.csv` from step 5 | Creates the cost tables and the three report figures |
| 7 | `07_Time_checks` | `07_Time_checks.ipynb` | `fact_energyconsumption.csv` from step 5 | Prints results only |
| 8 | `08_Compare` | `08_Compare.ipynb` | raw data; `home_features.csv`, `home_segments.csv` (step 2); `segments_gmm.csv` (step 3) | Takes one to two minutes. Creates `model_comparison.csv` and `model_agreement.csv` |

The notebooks 01 to 05 can be run in order; 06, 07 and 08 can then be run in any order (08 only needs steps 2 and 3). The files they create are already included in `data/processed/`, so any single notebook can also be run on its own as long as the files it needs are there.

## Data

- **Source:** [Smart Home Energy Consumption](https://www.kaggle.com/datasets/mexwell/smart-home-energy-consumption) (Kaggle).
- **Size:** 100,000 readings, 500 homes, 157 to 245 readings per home (about 200). Readings run from 1 January 2023 to 1 January 2024.
- **Fields:** Home ID, Appliance Type, Energy Consumption (kWh), Date, Time, Outdoor Temperature (°C), Season, Household Size.
- **Quality:** no missing values and no duplicate rows. The data has **10** appliance types (the project brief says 9): Air Conditioning, Computer, Dishwasher, Fridge, Heater, Lights, Microwave, Oven, TV, Washing Machine.
- **Timing:** readings are single samples at irregular times, not a continuous record. The median gap between two readings of the same home is about 30 hours. The data does not say how long each reading covers, so results are given per measurement, not as monthly or yearly bills. In this project, a *reading* and a *measurement* are the same thing.

## Method (shared by all models)

1. **One row per home.** Each home is described by its mean kWh per reading for each of the 10 appliances (500 × 10 table). Means are used instead of totals because homes have different numbers of readings.
2. **Standardise** each column (mean 0, standard deviation 1), so large appliances such as Air Conditioning (about 3.5 kWh) do not outweigh small ones such as Fridge (about 0.3 kWh).
3. **Fit the model** for a range of segment counts (k).
4. **Test whether the segments are meaningful.** A segment counts as meaningful only if it is:
   - clearer than segments found in shuffled data,
   - stable when the analysis is repeated,
   - describable in plain language.

The shuffle test mixes up the Home IDs, rebuilds the table and repeats the analysis. If the real result is not clearly better than the shuffled results, the "groups" could be chance.

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
| Compared with shuffled data | Silhouette: no for k = 2 to 4; marginal at k = 5 (p = 0.05, about 0.20 after correction) | Not in `03_GMM`. In `08_Compare`: no (p = 0.653). Agreement with K-means is tested in Step 9 | Silhouette: no for k = 2 to 4 (p = 0.26 to 0.60); marginal at k = 5 (p = 0.05, about 0.20 after correction) |
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

Differences between segments are small (at most about 0.2 kWh per reading on any appliance). The seeds and the number of shuffles for each step are listed in `02_KMeans/README.md`.

### Gaussian Mixture Model

- Settings: full covariance, 5 starting points per fit, `reg_covar = 1e-4`, `random_state = 42`.
- BIC is lowest at k = 1, meaning one group fits better than any split. The notebook still fits k ≥ 2 so the groups can be compared with K-means; set `K_OVERRIDE` in Step 6 of the notebook to choose another k.
- At k = 2, average membership probability is 0.857 and 49 homes are borderline (probability below 0.6).
- Segment 1 (253 homes) is lower on Air Conditioning and higher on Dishwasher and Lights; Segment 2 (247 homes) is the reverse.
- **Step 8 (stability):** builds a feature table from each half of every home's readings, fits the same model on each, and compares the two groupings with ARI. A score near 0 means the groups change with the readings. Result: mean -0.002 (range -0.006 to 0.004).
- **Step 9 (agreement with K-means):** compares the GMM groups with the K-means groups (k = 3) using ARI and 100 shuffles of the K-means labels. Result: ARI 0.09, shuffled mean 0.00 (maximum 0.01), p = 0.01. The two methods agree slightly more than random labels would, but not closely. This baseline is lenient, because shuffling labels does not change group sizes or the shape of the data.

### Hierarchical clustering

- Ward linkage on the same standardised table. It has no random start, so stability is tested by removing homes instead of changing a seed.
- The dendrogram shows no sharp break (top merge not different from shuffled trees, p = 0.347).
- Agreement with the K-means groups (k = 3) is ARI 0.105 against a shuffled mean of 0.119 (p = 0.535).

### Agreement between the models

| Pair | ARI |
|---|---|
| K-means and Gaussian Mixture | 0.090 |
| K-means and Hierarchical | 0.105 |
| Gaussian Mixture and Hierarchical | 0.208 |

All three are low. The models do not find the same groups, which fits the finding that there are no clear groups to find.

### Same-footing comparison (`08_Compare`)

The three model notebooks use different stability tests, so their scores cannot be compared. `08_Compare` gives every model the same two tests, each compared with the same 100 shuffled datasets. A model passes a test only if its p-value times 3 (three models) is below 0.05.

| | K-means (k = 3) | Gaussian Mixture (k = 2) | Hierarchical (k = 3) |
|---|---|---|---|
| Silhouette, real data | 0.076 | 0.058 | 0.038 |
| Silhouette, shuffled data (mean) | 0.073 | 0.060 | 0.039 |
| Silhouette p (p × 3) | 0.178 (0.535) | 0.653 (1.000) | 0.495 (1.000) |
| Split-half stability (ARI), real data | 0.001 | -0.000 | -0.002 |
| Split-half stability, shuffled data (mean) | 0.000 | -0.000 | 0.000 |
| Stability p (p × 3) | 0.188 (0.564) | 0.485 (1.000) | 0.792 (1.000) |
| Reliable groups? | No | No | No |

In the split-half test each home's readings are split at random into two halves, the model is fitted on each half, and the two sets of groups are compared with ARI. The seed test used in `02_KMeans` is easier to pass, because only the random start changes, so it is not used here. The p-values differ from those in the model notebooks because the tests differ. Hierarchical at k = 3 splits the homes 205 / 194 / 101.

## Dashboard (`05_Dashboard`)

Five pages: Overview, Household Profile, Appliance Summary, Cost, and How to read this dashboard.

- **Household Profile:** how one home compares with all 500 homes, appliance by appliance (difference from the average home, and the home's position among the 500 homes).
- **Appliance Summary:** the same position as a table with a level for each appliance: Low (under 25), Medium (25 to 75), High (75 or above).
- **Cost:** energy converted to dollars with a rate that can be changed (parameter `Electricity rate`, default 0.33).
- **Position (percentile)** is `fact_homeappliance[percentile]`: the rank of the home among all 500 homes for that appliance, 0 to 100. Because homes are very alike in this dataset, small differences between homes are random variation, so read it as position only.
- The segment columns are in `dim_home.csv`, but no dashboard page shows them.
- Formulas for the parameter and measures are in `05_Dashboard/powerbi/measures.md` (check them against the model in Power BI before relying on them).

To rebuild the dashboard data: run `05_Dashboard.ipynb`, open the `.pbix`, then choose Home, then Refresh.

## Cost analysis (`06_Cost`)

- Cost = kWh × rate. Rate: 0.33 $/kWh, rounded from 33.14 c/kWh (Australian Energy Regulator, Default Market Offer 2026-27, Ausgrid area, NSW, single/flat rate, all-day usage charge, including GST; read on 30 October 2026). The daily supply charge is not included.
- To change the rate, edit `RATE` in the notebook **and** the `Electricity rate` parameter in Power BI, otherwise the two will not match.
- A sample portfolio of 50 homes is drawn at random (seed 42) as a stand-in for a client's units. For a real client, replace the list of home IDs with the client's own list.
- Results: average cost per measurement $0.495 for both the 50-home sample and all 500 homes. Air Conditioning (23.8%) and Heater (22.7%) make up 46.5% of the sample's cost. The sample is within about 2% of the 500-home average for every appliance, and the 50 units are between 6.7% below and 8.6% above the average.

## Time checks (`07_Time_checks`)

- Only 6.6% of time stamps fall on a 15-minute mark, which is what random times give, so the readings are not at 15-minute intervals.
- Energy use does not change with time of day (p = 0.56 against shuffled data) or outdoor temperature (p = 0.38). Air Conditioning and Heater show no response to temperature (correlations 0.002 and -0.006, inside a noise range of about ±0.020).
- Together with the missing seasonal pattern (see `01_EDA`), this supports the view that the dataset is simulated.

## Outputs

All tables are written to `data/processed/`.

| File | Created by | Contents |
|---|---|---|
| `home_features.csv` | `02_KMeans` | 500 homes × 10 appliances (mean kWh per reading), plus `n_readings` and `avg_kwh` |
| `home_segments.csv` | `02_KMeans` | Features plus `cluster` (0 to 2) and `segment_name` (k = 3) |
| `segments_gmm.csv` | `03_GMM` | Features plus `segment`, `membership_prob` and one probability column per segment |
| `fact_energyconsumption.csv` | `05_Dashboard` | 100,000 rows, one per measurement, with short column names |
| `fact_homeappliance.csv` | `05_Dashboard` | 5,000 rows, one per home and appliance: `avg_kwh` and `percentile` |
| `dim_home.csv` | `05_Dashboard` | 500 rows: K-means segment columns, `n_readings`, `avg_kwh` |
| `dim_appliance.csv` | `05_Dashboard` | The 10 appliance types |
| `portfolio50_by_appliance.csv` | `06_Cost` | Average kWh, cost and share of cost by appliance, for the 50 homes and for all 500 |
| `portfolio50_by_home.csv` | `06_Cost` | One row per portfolio home: measurements, average kWh, average cost, difference from the 500-home average |
| `cost_assumptions.csv` | `06_Cost` | Rate, source, date, number of portfolio homes and seed |
| `model_comparison.csv` | `08_Compare` | Silhouette, split-half stability, p-values and verdict for each model |
| `model_agreement.csv` | `08_Compare` | ARI between each pair of models |

`06_Cost` also saves three figures to `reports/figures/`.

## Reports (`reports/`)

- **Sample client report** (`Smart Home Energy Sample Portfolio of 50 Units.pdf`): a consulting report for a simulated property developer with a 50-unit portfolio. It leaves out the grouping methods and says only that no natural groups of homes were found.
- **Key figures** are listed in `reports/README.md`. The same numbers are used in the reports, the dashboard and the presentation, so if one changes, update all of them.
- The technical report named in `reports/README.md` is not stored in this repository yet. Add it to `reports/` or remove it from that list.

## Limitations

- The dataset appears synthetic, so the findings may not apply to real households.
- Segments are a descriptive grouping, not distinct household types. Segment labels are arbitrary and depend on the random seed.
- The three model notebooks use different stability tests, and `03_GMM` has no shuffled-data baseline for silhouette or stability. Only `08_Compare` puts the models on the same footing.
- ARI values can only be compared with a shuffled baseline for the same k and the same test.
- Readings are irregular single samples, so costs are per measurement and cannot be turned into monthly or yearly bills.
- The electricity rate is indicative: one region, usage charge only, flat rate (time-of-use pricing is not modelled).

## Adapting to a new dataset

The analysis needs one row per reading with a home ID, an appliance type and an energy value. To use another dataset:

1. Save it in `data/raw/` and change the file name at the top of each notebook.
2. If its column names differ, rename them to match: `Home ID`, `Appliance Type`, `Energy Consumption (kWh)`.
3. Rerun the shuffle and stability tests before trusting any segments, and run `08_Compare` to see whether any model passes the same tests. Real data may show clearer groups than this dataset.
4. Rerun notebooks 05 and 06 and refresh the Power BI file. Set the same electricity rate in `06_Cost_analysis.ipynb` and in the `Electricity rate` parameter.
