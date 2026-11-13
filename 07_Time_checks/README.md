# 07 Time checks

Checks how the measurements are spaced in time, and whether energy use changes with time of day or outdoor temperature.

**Notebook:** `07_Time_checks.ipynb`

**Run after:** `05_Dashboard` (it needs `data/processed/fact_energyconsumption.csv`).

## Output

No files are saved. The results are printed in the notebook.

## Main results

- The measurements are not at 15-minute intervals: only 6.6% of time stamps fall on a 15-minute mark, which is what random times give.
- The median gap between two measurements of the same home is about 30 hours (mean 43.7 hours, longest 573 hours). The measurements are separate samples, not a continuous record, so costs are reported per measurement and not as monthly or yearly bills.
- Energy use does not change with time of day (p = 0.56 against shuffled data).
- Energy use does not change with outdoor temperature (p = 0.38 with all bands). Air Conditioning and Heater show no response to temperature (correlations 0.002 and -0.006, inside a noise range of about +/-0.020).
- The hottest band (40 to 45 °C) has only 93 measurements, so its average varies a lot by chance. Without it, the temperature result is p = 0.71.

Together with the missing seasonal pattern (see `01_EDA`), this supports the view that the dataset is simulated.

## Random seeds and shuffles

Shuffled baselines use seed 42 and 200 shuffles (`np.random.default_rng(42)`).

**Requires:** pandas, numpy.
