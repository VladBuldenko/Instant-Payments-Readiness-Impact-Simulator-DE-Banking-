# -----------------------------
# Streamlit app: Instant Payments Readiness Simulator
# -----------------------------

# Import system libs to adjust Python path (so we can import from ../src)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Streamlit for interactive UI
import streamlit as st

# Import plotting and data libs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import your simulation core functions from src/sim_core.py
from src.sim_core import (
    generate_synth,
    simulate_vop,
    scan_vop,
    simulate_fraud,
    scan_fraud
)

# -----------------------------
# Page / layout settings
# -----------------------------
# Set page title and layout to wide for more room
st.set_page_config(page_title="Instant Payments Readiness Simulator", layout="wide")

# Show a title for the app
st.title("💶 Instant Payments Readiness Simulator (DE Banking)")

# Add a short description so the reader knows what this is
st.write(
    "Interactively explore how **Verification of Payee (VoP)** and **Fraud Filter** thresholds "
    "influence key KPIs: Conversion, Latency p95, Manual Review Rate, and Risk Exposure."
)

# -----------------------------
# Sidebar — global controls
# -----------------------------
# Group controls in the sidebar
st.sidebar.header("🔧 Controls")

# Add a selector for number of synthetic transactions (larger -> smoother curves)
# Use a safe default for performance
n_rows = st.sidebar.select_slider("Synthetic transactions", options=[5_000, 20_000, 50_000, 100_000], value=20_000)

# Seed makes results reproducible; let the user change it if they want
seed = st.sidebar.number_input("Random seed", min_value=0, max_value=999999, value=42, step=1)

# -----------------------------
# Data creation with caching
# -----------------------------
# Use Streamlit cache to avoid regenerating data on every widget change unless inputs change
@st.cache_data(show_spinner=False)
def get_data(n: int, seed: int) -> pd.DataFrame:
    # Generate synthetic transactions using your core function
    df = generate_synth(n=n, seed=seed)
    # Ensure a boolean column for true fraud exists; if not, create a simple proxy
    # Here: mark very high fraud_probability as true fraud (e.g., > 0.9)
    if "is_true_fraud" not in df.columns:
        df["is_true_fraud"] = (df["fraud_probability"] > 0.90).astype(int)
    return df

# Build the dataset based on current sidebar selections
df = get_data(n_rows, seed)

# -----------------------------
# Sidebar — simulation sliders
# -----------------------------
# Slider for VoP strictness threshold (higher => stricter)
vop_thr = st.sidebar.slider("VoP threshold (strictness)", min_value=0.50, max_value=0.95, value=0.80, step=0.05)

# Slider for Fraud filter threshold (lower => more sensitive, more reviews)
fraud_thr = st.sidebar.slider("Fraud filter threshold", min_value=0.20, max_value=0.90, value=0.50, step=0.10)

# Option to scan curves around the chosen values
# This helps draw simple line charts without being too heavy
vop_scan_grid = np.arange(0.50, 0.95, 0.05)
fraud_scan_grid = np.arange(0.20, 0.90, 0.10)

# -----------------------------
# Compute KPIs for current thresholds
# -----------------------------
# Run the VoP simulation once at the selected threshold
vop_res = simulate_vop(df, threshold=vop_thr)

# Run the Fraud simulation once at the selected threshold
fraud_res = simulate_fraud(df, threshold=fraud_thr)

# Compute scan curves for small grids (for plots)
vop_curves = scan_vop(df, vop_scan_grid)
fraud_curves = scan_fraud(df, fraud_scan_grid)

# -----------------------------
# KPI summary row (metrics)
# -----------------------------
# Create three columns to show top KPIs
col1, col2, col3, col4 = st.columns(4)

# Show conversion rate metric
col1.metric(label="Conversion Rate (%)", value=f"{vop_res['conversion_rate']:.1f}")

# Show latency p95 metric
col2.metric(label="Latency p95 (s)", value=f"{vop_res['latency_p95']:.2f}")

# Show manual review rate metric
col3.metric(label="Manual Review Rate (%)", value=f"{fraud_res['manual_review_rate']:.1f}")

# Show risk exposure metric
col4.metric(label="Risk Exposure (€)", value=f"{fraud_res['risk_exposure_eur']:.0f}")

# -----------------------------
# Charts section
# -----------------------------
# Add a subheader for charts
st.subheader("📈 KPI Curves")

# Create two columns for charts
c1, c2 = st.columns(2)

# --- Chart 1: VoP curves (Conversion & Latency on separate simple lines) ---
with c1:
    # Build a simple line plot for Conversion Rate vs VoP threshold
    fig1, ax1 = plt.subplots()
    # Plot conversion line
    ax1.plot(vop_curves["vop_threshold"], vop_curves["conversion_rate"], marker="o", linewidth=2)
    # Label axes and title
    ax1.set_title("VoP strictness → Conversion Rate")
    ax1.set_xlabel("VoP Threshold")
    ax1.set_ylabel("Conversion Rate (%)")
    # Render the figure in Streamlit
    st.pyplot(fig1, clear_figure=True)

    # Build a simple line plot for Latency p95 vs VoP threshold
    fig2, ax2 = plt.subplots()
    # Plot latency line
    ax2.plot(vop_curves["vop_threshold"], vop_curves["latency_p95"], marker="o", linewidth=2)
    # Label axes and title
    ax2.set_title("VoP strictness → Latency p95")
    ax2.set_xlabel("VoP Threshold")
    ax2.set_ylabel("Latency p95 (s)")
    # Render the figure
    st.pyplot(fig2, clear_figure=True)

# --- Chart 2: Fraud trade-off (dual-axis: Manual Review vs Risk) ---
with c2:
    # Create a dual-axis plot to show trade-offs clearly
    fig3, ax_left = plt.subplots()
    # Plot manual review rate on the left y-axis
    ax_left.plot(fraud_curves["fraud_threshold"], fraud_curves["manual_review_rate"],
                 color="tab:orange", marker="o", linewidth=2)
    # Label left axis
    ax_left.set_xlabel("Fraud Threshold")
    ax_left.set_ylabel("Manual Review Rate (%)", color="tab:orange")
    # Color the tick labels to match the line
    ax_left.tick_params(axis="y", labelcolor="tab:orange")

    # Create a twin axis sharing the same x-axis
    ax_right = ax_left.twinx()
    # Plot risk exposure on the right y-axis
    ax_right.plot(fraud_curves["fraud_threshold"], fraud_curves["risk_exposure_eur"],
                  color="tab:blue", marker="s", linewidth=2)
    # Label right axis
    ax_right.set_ylabel("Risk Exposure (€)", color="tab:blue")
    # Color the tick labels to match the line
    ax_right.tick_params(axis="y", labelcolor="tab:blue")

    # Add a title and tighten layout
    fig3.suptitle("Fraud filter strictness → Risk vs Manual Load")
    fig3.tight_layout()
    # Render the figure
    st.pyplot(fig3, clear_figure=True)

# -----------------------------
# Recommended operating zone (friendly text)
# -----------------------------
# Provide a small helper note that explains the trade-offs and suggests a zone
st.subheader("🧭 Recommended Operating Zone (Rule-of-Thumb)")

# Compose a short narrative based on current thresholds
st.markdown(
    f"""
- **VoP threshold = {vop_thr:.2f}** → Stricter checks **reduce mistakes** but **increase latency**.
- **Fraud threshold = {fraud_thr:.2f}** → Lower thresholds **reduce risk** but **increase manual reviews**.

**Heuristic balance:** VoP ≈ **0.75–0.85**, Fraud ≈ **0.40–0.55** often keeps
**Conversion** healthy, **Latency** under control, and **Risk** acceptable without overwhelming analysts.
"""
)

# -----------------------------
# Footer / context
# -----------------------------
# Add a small footer note (data generation and purpose)
st.caption(
    "Note: The dataset is synthetic and generated locally for scenario testing. "
    "Bundesbank statistics inform volume trends but do not contain VoP/Fraud fields; "
    "this app evaluates **what-if** operational settings."
)
