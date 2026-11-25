
import streamlit as st
import pandas as pd
from pathlib import Path

# Project folder
project_path = Path(__file__).resolve().parent

# Page settings
st.set_page_config(
    page_title="RideOpt AI",
    page_icon="🚕",
    layout="wide"
)


# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Demand Prediction", "Fleet Allocation"]
)

# Dashboard title
st.title("🚕 RideOpt AI")
st.write("NYC Ride-Hailing Demand Prediction & Fleet Allocation")

st.divider()

if page == "Overview":

    # Machine Learning results
    st.header("Machine Learning Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("Test MAE", "11.66")
    col2.metric("Test R²", "0.967")
    col3.metric("Test WAPE", "10.98%")

    # Fleet allocation results
    st.header("Fleet Allocation Simulation")

    st.image(
        str(project_path / "fleet_coverage_comparison.png"),
        caption="Average simulated pickup coverage across 72 scenarios"
    )

    st.info(
        "Fleet allocation results are simulated using hypothetical "
        "vehicle availability and straight-line distances."
    )


# Interactive demand prediction
if page == "Demand Prediction":

    st.header("Predict NYC Taxi Demand")

    predictions = pd.read_parquet(
        project_path / "test_predictions.parquet"
    )

    zones = pd.read_csv(
        project_path / "taxi_zone_lookup.csv"
    )

    zone_names = dict(zip(zones["LocationID"], zones["Zone"]))

    selected_zone = st.selectbox(
        "Select NYC Taxi Zone",
        sorted(predictions["zone_id"].unique()),
        format_func=lambda z: zone_names.get(z, str(z))
    )

    zone_data = predictions[
        predictions["zone_id"] == selected_zone
    ].copy()

    # Select a date
    selected_date = st.selectbox(
        "Select Date",
        sorted(zone_data["pickup_hour"].dt.date.unique())
    )

    # Show only the selected date
    zone_data = zone_data[
        zone_data["pickup_hour"].dt.date == selected_date
    ]

    st.line_chart(
        zone_data.set_index("pickup_hour")[
            ["pickup_count", "predicted_count"]
        ]
    )


    # Select an hour to inspect
    selected_hour = st.selectbox(
        "Select Hour",
        range(24),
        format_func=lambda h: f"{h:02d}:00"
    )

    # Find the selected hour's prediction
    selected_row = zone_data[
        zone_data["pickup_hour"].dt.hour == selected_hour
    ].iloc[0]

    predicted = selected_row["predicted_count"]
    actual = selected_row["pickup_count"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Predicted Pickups", f"{predicted:.0f}")
    col2.metric("Actual Pickups", f"{actual:.0f}")
    col3.metric("Absolute Error", f"{abs(actual - predicted):.1f}")

    st.caption(
        "Actual vs predicted hourly pickups on held-out "
        "January 28–31, 2025 data."
    )


# Fleet Allocation page
if page == "Fleet Allocation":

    st.header("Fleet Allocation Simulation")

    st.write(
        "Compare simulated taxi allocation strategies "
        "using a 3.33 km repositioning limit."
    )

    # Load saved simulation results
    fleet_results = pd.read_csv(
        project_path / "distance_constrained_results.csv"
    )

    # Calculate average performance
    summary = pd.DataFrame({
        "Strategy": ["Weekly Baseline", "XGBoost"],
        "Average Pickups Covered": [
            fleet_results["weekly_covered"].mean(),
            fleet_results["ml_covered"].mean()
        ],
        "Average Vehicle-km": [
            fleet_results["weekly_distance"].mean(),
            fleet_results["ml_distance"].mean()
        ]
    })


    # Calculate improvements
    coverage_gain = (
        summary.loc[1, "Average Pickups Covered"]
        / summary.loc[0, "Average Pickups Covered"] - 1
    ) * 100

    distance_reduction = (
        1 - summary.loc[1, "Average Vehicle-km"]
        / summary.loc[0, "Average Vehicle-km"]
    ) * 100

    col1, col2 = st.columns(2)

    col1.metric(
        "Simulated Pickup Coverage Gain",
        f"+{coverage_gain:.2f}%"
    )

    col2.metric(
        "Repositioning Distance Reduction",
        f"{distance_reduction:.2f}%"
    )

    st.dataframe(summary.round(2), hide_index=True)

    # Compare pickup coverage visually
    st.subheader("Pickup Coverage Comparison")

    chart_data = summary.set_index("Strategy")[
        "Average Pickups Covered"
    ]

    st.bar_chart(chart_data)




    # Compare repositioning distance
    st.subheader("Repositioning Distance Comparison")

    distance_data = summary.set_index("Strategy")[
        "Average Vehicle-km"
    ]

    st.bar_chart(distance_data)

    st.caption(
        "Lower vehicle-km means less simulated "
        "empty repositioning travel."
    )

    st.caption(
        "Results are based on 72 independent hypothetical "
        "hourly fleet scenarios, not real NYC vehicle movements."
    )
