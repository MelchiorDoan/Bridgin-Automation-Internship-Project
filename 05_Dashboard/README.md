# 05_Dashboard: data tables and Power BI files

Creates the tables used by the Power BI dashboard from the raw readings and the K-means outputs.

**Notebook:** `05_Dashboard.ipynb`

**Run after:** `02_KMeans` (it needs `home_features.csv` and `home_segments.csv`).

## Input (in `data/`)

| File | Created by |
| --- | --- |
| `raw/smart_home_energy_consumption_large.csv` | Kaggle (see the main README) |
| `processed/home_features.csv`, `processed/home_segments.csv` | `02_KMeans` |

## Output (in `data/processed/`)

| File | Rows | What it holds |
| --- | --- | --- |
| `fact_energyconsumption.csv` | 100,000 | One row per measurement, with short column names (`home_id`, `appliance`, `kwh`, `time`, `date`, `temp`, `season`, `household_size`). No values are changed |
| `fact_homeappliance.csv` | 5,000 | One row per home and appliance: average kWh per measurement (`avg_kwh`) and the home's position among the 500 homes for that appliance (`percentile`, 0 to 100) |
| `dim_home.csv` | 500 | One row per home: K-means segment (descriptive only), number of measurements and average kWh |
| `dim_appliance.csv` | 10 | The 10 appliance types |

`fact_energyconsumption.csv` is also the input of `06_Cost` and `07_Time_checks`.

## Notes

- Averages per measurement are used instead of totals, because homes have between 157 and 245 measurements.
- `household_size` changes within every home, so it is kept on each measurement and is not a home attribute.
- `percentile` is the rank of the home among all 500 homes for that appliance (higher means more energy). Differences between homes are consistent with random variation in this dataset, so read it as position only.
- The segments are weakly separated and are descriptive only.
- The Power BI file is built separately and is not stored in this repository.

**Requires:** pandas. 
**Random seeds:** none (no random steps).

## Power BI files

The Power BI dashboard is built separately. Its finished files are in `powerbi/`:

| File | What it holds |
| --- | --- |
| `smart_home_energy_dashboard.pdf` | The five dashboard pages: Overview, Household Profile, Appliance Summary, Cost, and How to read this dashboard |
| `measures.md` | The parameter, calculated column and DAX measures used by the dashboard |

To rebuild the dashboard: run the notebook in this folder, open the `.pbix`, and choose Home, then Refresh.
