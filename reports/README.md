# Reports

The data used in the project appear to be simulated (see the technical report), so the reports show how the method and the tool work. They are not findings about real buildings.

## Files

| File | Audience | What it is |
| --- | --- | --- |
| `Smart Home Energy Sample Portfolio of 50 Units` (.pdf) | Client, non-technical | Sample consulting report for a simulated property developer with a 50-unit portfolio. It compares the 50 units with the 500-home benchmark, shows estimated cost by appliance, explains how to use the dashboard, and gives three recommendations |
| `Smart Home Energy Benchmarking_Technical Report` (.pdf) | Team, mentor, CTO | Technical report: data checks, evidence that the dataset appears simulated, tests for household groups, position-based benchmarking, cost model, dashboard design, search for more realistic data, limitations and reproducibility |
| `Figures` | Used in the reports | `fig1_cost_by_appliance.png`, `fig2_cost_share.png` and `fig3_units_vs_average.png` |


## Which report to read

- **Client report:** start here for the findings and recommendations. It leaves out the grouping methods on purpose and only says that no natural groups of homes were found.
- **Technical report:** read this for every test, the p-values, the limitations and the steps to rerun the work.

## Key figures

The same numbers are used in both reports, the dashboard and the presentation. If one changes, update all of them.

| Figure | Value | Source notebook |
| --- | --- | --- |
| Homes, appliance types and measurements | 500 homes, 10 appliance types, about 100,000 measurements, 1 January 2023 to 1 January 2024 | 01 Data overview |
| Average energy per measurement | 1.50 kWh | 01 Data overview |
| Electricity rate | 33 cents per kWh (rounded from 33.14), AER Default Market Offer 2026-27, Ausgrid area (NSW), single/flat rate, including GST, usage charge only | 06 Cost |
| Average cost per measurement, 50-unit sample and all 500 homes | $0.495 | 06 Cost |
| Share of cost from Air Conditioning and Heater | 46.5% in the 50-unit sample, about 47% across all 500 homes | 06 Cost |
| 50-unit sample against the 500-home average | Within about 2% for every appliance; units between 6.7% below and 8.6% above | 06 Cost |
| Median gap between two measurements of one home | About 30 hours | 07 Time checks |

## How the figures are made

The three figures are drawn by the cost notebook (section 7, folder `06_Cost`). The notebook reads `portfolio50_by_appliance.csv` and `portfolio50_by_home.csv` from the processed data folder and saves the images here, in `figures/`. To regenerate them, run the cost notebook again.

- Dark green marks the 50-unit portfolio (and Air Conditioning and Heater in the cost share figure).
- Grey marks the 500-home benchmark and the other appliances.

## How the reports are produced

The reports are written documents. The tables and figures in them are copied from the notebook outputs.

If the notebooks are rerun with different data or a different electricity rate:

1. Check that the key figures above still match.
2. Replace the tables and figures in both reports.
3. Update the dashboard (refresh the data and set the same rate in the `Electricity rate` parameter) and the presentation.
4. Update the version number and the date.

## Wording used in the reports

- **Measurement:** one recorded energy value (kWh) for one appliance in one home. The data do not say how long each value covers.
- **Cost per measurement:** the cost of the energy in one measurement, at the electricity rate. It is used to compare homes and appliances. It is not a monthly or yearly bill.
- **Position (Uses more than, % of homes):** where a home stands among the 500 homes for one appliance. A position of 75 means 75 of every 100 homes use less energy than this home. It shows position only, not whether an appliance is efficient or wasteful.
- **Benchmark:** the average of all 500 homes.
