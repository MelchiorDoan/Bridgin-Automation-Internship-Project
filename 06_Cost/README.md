# 06 Cost analysis and 50-unit sample portfolio

Converts energy into estimated cost at a flat electricity rate, checks the Power BI cost page against Python, and creates the tables and figures for the sample consulting report (a 50-unit portfolio).

**Notebook:** `06_Cost_analysis.ipynb`

**Run after:** `05_Dashboard` (it needs `fact_energyconsumption.csv`).

## Assumptions

- Rate: 0.33 $/kWh, rounded from 33.14 c/kWh. Source: Australian Energy Regulator, Default Market Offer 2026-27, Ausgrid area (NSW), single/flat rate, all-day usage charge, including GST. The price was read on 30 October 2026.
- The daily supply charge ($1.66 per day) is not included.
- Costs are per measurement, not per month or year: each home has about 200 measurements, with a median gap of about 30 hours (see `07_Time_checks`).
- The rate is indicative. To change it, edit `RATE` in the notebook **and** the `Electricity rate` parameter in Power BI, otherwise the two will not match.

## Output

| File | Where | What it holds |
| --- | --- | --- |
| `portfolio50_by_appliance.csv` | `data/processed/` | Average kWh, cost and share of cost by appliance, for the 50 homes and for all 500 homes |
| `portfolio50_by_home.csv` | `data/processed/` | One row per portfolio home: measurements, average kWh, average cost, difference from the 500-home average |
| `cost_assumptions.csv` | `data/processed/` | Rate, source, date and seed used |
| `fig1_cost_by_appliance.png`, `fig2_cost_share.png`, `fig3_units_vs_average.png` | `reports/figures/` | Figures used in the 50-unit report |

## Random seed

The 50 homes are drawn at random with seed 42 (`np.random.default_rng(42)`). The same homes are selected on every run as long as the data and the seed do not change. For a real client, replace the list of home IDs with the client's own list.

**Requires:** pandas, numpy, matplotlib.
