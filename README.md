# 🚕 RideOpt AI — NYC Demand Forecasting & Fleet Allocation

RideOpt AI is a machine-learning and simulation project that forecasts hourly ride-hailing pickup demand across New York City taxi zones and evaluates a distance-constrained strategy for repositioning a hypothetical taxi fleet.

The dashboard lets users explore held-out demand forecasts and compare aggregate fleet-allocation simulation outcomes. **It is a historical-data dashboard, not a live dispatch system.**

## Highlights

- Processed **20.4M+ January 2025 NYC high-volume for-hire vehicle trip records** and aggregated demand by taxi zone and hour.
- Prepared hourly time-series features, including calendar features, lags, and rolling averages.
- Trained and evaluated an **XGBoost** demand-forecasting model using chronological splits.
- Simulated fleet repositioning using a **greedy, shortest-distance-first** algorithm, with zone-centroid distances and a configurable limit.
- Compared XGBoost demand forecasts with a **same-hour-last-week (168-hour lag)** baseline.
- Built a **Streamlit dashboard** showing historical predictions, evaluation metrics, and saved allocation results.

## Reported results

### Held-out demand forecasting

| Metric | Value |
|---|---:|
| Test MAE | **11.66 pickups** |
| Test R² | **0.967** |
| Test WAPE | **10.98%** |
| Test MAE improvement vs weekly baseline | **19.4%** |

The test period is **January 28–31, 2025**, with predictions evaluated against recorded pickup counts. This is a historical holdout evaluation, not live forecasting.

### Distance-constrained fleet simulation

Across **72 hypothetical scenarios** (24 hours on January 28 × 3 randomly generated starting fleets per hour), using an approximate **3.33 km** maximum repositioning distance:

| Metric | XGBoost vs weekly baseline |
|---|---:|
| Scenarios with higher simulated pickup coverage | **61 of 72** |
| Average simulated coverage improvement | **0.99%** |
| Average repositioning vehicle-km change | **−1.31%** |

The 3.33 km threshold was calculated from **an assumed 20 km/h speed and 10-minute limit**. Simulations use straight-line distances between zone centroids, not actual road travel. These results do **not** demonstrate verified real-world improvements.

## Dashboard

- **Overview:** Held-out model performance and simulated pickup coverage visualization.
- **Demand Prediction:** Select a taxi zone, date, and hour within the held-out period to compare recorded pickups with precomputed predictions.
- **Fleet Allocation:** Compare average coverage and repositioning vehicle-km from the saved distance-constrained scenarios.

> **Note:** The dashboard loads **precomputed predictions and simulation outputs**. It does not retrain XGBoost or generate new future forecasts on demand.

## Repository structure

```text
RideOpt-AI/
├── app/
│   └── app.py
├── requirements.txt
├── test_predictions.parquet
├── taxi_zone_lookup.csv
├── distance_constrained_results.csv
├── fleet_coverage_comparison.png
└── README.md
```

The supporting notebook may be added separately after checking for private paths, outputs, and oversized embedded data. The original 20.4M+ trip dataset is **not** required for dashboard execution.

## Run locally

**Prerequisite:** Python 3.10+ recommended.

1. Download or clone the repository.
2. Open a terminal in the root `RideOpt-AI` folder.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start Streamlit:

   ```bash
   streamlit run app/app.py
   ```

5. Open the localhost URL printed by Streamlit (typically `http://localhost:8501`).

All four supporting files named in the repository structure must be present at the repository root, alongside `requirements.txt`, because `app.py` reads them relative to its parent directory.

## Technical stack

- **Forecasting and analysis:** Python, DuckDB, Pandas, NumPy, Scikit-learn, XGBoost
- **Geospatial simulation:** GeoPandas, SciPy (distance calculations)
- **Dashboard:** Streamlit, Pandas, PyArrow

The lightweight `requirements.txt` installs **dashboard dependencies only**. Reproducing the training notebook requires additional packages and the source datasets.

## Methodology and limitations

1. Demand is represented by **recorded pickups**, not the full number of passengers requesting rides.
2. Simulated vehicle availability is **hypothetically generated**, not observed NYC taxi fleet availability.
3. For each scenario, the allocation function identifies zones with surplus and shortage against forecast demand, then moves vehicles along eligible **shortest straight-line routes first**.
4. The simulation estimates coverage using `min(actual_pickups, available_taxis)` for each zone. It assumes simplified instantaneous repositioning and approximately one covered pickup per available taxi per evaluation hour.
5. The 72 scenarios are **24 hourly cases with three independent random starting fleets each**; they are not 72 independent days or field experiments.
6. Straight-line centroid distances and the assumed speed do not represent actual travel times, congestion, route availability, or operating costs.
7. The displayed demand predictions are for a **historical held-out test window** and are not production forecasts.

## Data attribution

The project uses January 2025 NYC high-volume for-hire vehicle trip data and the NYC taxi-zone lookup / geospatial boundary data published by the **New York City Taxi & Limousine Commission (NYC TLC)**.

Official data portal: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

## Author

**Sufiyan Tejani** — M.Sc. Mathematics, IIT Kharagpur  
[LinkedIn](https://www.linkedin.com/in/sufiyan-tejani/) · [GitHub](https://github.com/sufiyan-tejani)

---

*RideOpt AI is a portfolio / research demonstration built on historical data and a simplified fleet simulation.*
