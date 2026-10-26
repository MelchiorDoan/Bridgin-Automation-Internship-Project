# EDA notebook

Data quality checks and exploratory analysis of the Smart Home Energy Consumption dataset.

- **Notebook:** `01_Data_overview.ipynb`
- **Input:** `smart_home_energy_consumption_large.csv` (Kaggle, "Smart Home Energy Consumption", mexwell): 100,000 readings, 500 homes, 10 appliance types. 
- **Requires:** pandas, numpy, matplotlib (see `requirements.txt`).
- **Random seed:** 42 (permutation tests with 200 shuffles each).

## Main results
- No missing values or duplicate rows; 10 appliance types (the project brief mentions 9).
- Season labels are calendar quarters (December is labelled Fall). Outdoor temperature is about 15 °C in every month and appliance use does not change by season.
- Household size varies within every home (500 of 500 homes report all five sizes) and does not affect consumption.
- Appliances fall into three groups: Air Conditioning and Heater (about 3.5 kWh per reading), seven appliances (about 1.1 kWh) and Fridge (about 0.3 kWh).
- Differences between homes, in total and per appliance, are consistent with sampling noise (permutation tests).

## Limitation
The dataset appears synthetic, so these findings may not apply to real household data.
