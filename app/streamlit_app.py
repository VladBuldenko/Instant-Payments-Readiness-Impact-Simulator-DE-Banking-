
# -----------------------------
# Streamlit app: Instant Payments Readiness Simulator
# -----------------------------
# NOTE: All comments are placed ABOVE the lines, per your preference.
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

# Import your simulation core functions
from src.sim_core import (
    generate_synth,
    simulate_vop,
    scan_vop,
    simulate_fraud,
    scan_fraud
)

# -----------------------------
# Page & theme settings
# -----------------------------
# Set page title and wide layout for better charts
st.set_page_config(page_title="Instant Payments Readiness Simulator", layout="wide")

# Optional: consistent figure size and grid
plt.rcParams["figure.figsize"] = (7.0, 3.6)
plt.rcParams["axes.grid"] = True

# -----------------------------
# Header (Hero)
# -----------------------------
# Title with a crisp subtitle to explain value
st.title("💶 Instant Payments Readiness Simulator (DE Banking)")
st.markdown(
    """
**Purpose.** Explore how **Verification of Payee (VoP)** and **Fraud Filter** thresholds shape four core KPIs:
**Conversion Rate**, **Latency p95**, **Manual Review Rate**, and **Risk Exposure**.

Use the sliders on the left to tune operating parameters and see trade-offs in real time.
"""
)

# -----------------------------
# Sidebar — Global controls
# -----------------------------
st.sidebar.header("🔧 Controls")

# Select number of synthetic transactions (higher = smoother curves)
n_rows = st.sidebar.select_slider(
    "Synthetic transactions",
    options=[5_000, 20_000, 50_000, 100_000],
    value=20_000
)

# Seed for reproducible results
seed = st.sidebar.number_input("Random seed", min_value=0, max_value=999_999, value=42, step=1)

# Slider for VoP strictness threshold (higher => stricter checks)
vop_thr = st.sidebar.slider("VoP threshold (strictness)", min_value=0.50, max_value=0.95, value=0.80, step=0.05)

# Slider for Fraud filter threshold (lower => more sensitive, more manual reviews)
fraud_thr = st.sidebar.slider("Fraud filter threshold", min_value=0.20, max_value=0.90, value=0.50, step=0.10)

# Define scan grids for drawing KPI curves
vop_scan_grid = np.arange(0.50, 0.95, 0.05)
fraud_scan_grid = np.arange(0.20, 0.90, 0.10)

# -----------------------------
# Data creation (cached)
# -----------------------------
# Cache synthetic data to avoid regeneration on every UI interaction
@st.cache_data(show_spinner=False)
def get_data(n: int, seed: int) -> pd.DataFrame:
    # Generate synthetic transactions
    df = generate_synth(n=n, seed=seed)
    # Ensure "true fraud" exists for Risk Exposure narrative
    if "is_true_fraud" not in df.columns:
        df["is_true_fraud"] = (df["fraud_probability"] > 0.90).astype(int)
    return df

# Build the dataset once per parameter change
df = get_data(n_rows, seed)

# -----------------------------
# Current KPIs (one-shot calculations for chosen thresholds)
# -----------------------------
# Compute VoP KPIs for the selected VoP threshold
vop_res = simulate_vop(df, threshold=vop_thr)

# Compute Fraud KPIs for the selected Fraud threshold
fraud_res = simulate_fraud(df, threshold=fraud_thr)

# Also compute smooth KPI curves for charts
vop_curves = scan_vop(df, vop_scan_grid)
fraud_curves = scan_fraud(df, fraud_scan_grid)

# -----------------------------
# Section: Current KPI Snapshot
# -----------------------------
st.markdown("### 📈 Current KPI Snapshot")
st.caption("These KPIs summarize the system state under the current thresholds.")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Conversion Rate (%)", f"{vop_res['conversion_rate']:.1f}")
c2.metric("Latency p95 (s)", f"{vop_res['latency_p95']:.2f}")
c3.metric("Manual Review Rate (%)", f"{fraud_res['manual_review_rate']:.1f}")
c4.metric("Risk Exposure (€)", f"{fraud_res['risk_exposure_eur']:.0f}")

# Show a compact line with current settings for clarity
st.caption(
    f"**Current settings:** VoP threshold = {vop_thr:.2f} · Fraud threshold = {fraud_thr:.2f} "
    f"· N = {n_rows:,} synthetic transactions · Seed = {seed}"
)

# -----------------------------
# Section: KPI Curves (tabs for clean navigation)
# -----------------------------
st.markdown("### 🔍 Threshold Sensitivity (KPI Curves)")
# Use tabs to separate VoP and Fraud stories
tab_vop, tab_fraud = st.tabs(["VoP → Conversion & Latency", "Fraud → Manual Load & Risk"])

# --- Tab 1: VoP
with tab_vop:
    st.write(
        "Stricter VoP thresholds reduce mistaken payouts but **lower Conversion** and **increase Latency** "
        "due to extra validation steps."
    )
    # Plot conversion vs VoP threshold
    fig1, ax1 = plt.subplots()
    ax1.plot(vop_curves["vop_threshold"], vop_curves["conversion_rate"], marker="o", linewidth=2)
    ax1.set_title("VoP strictness → Conversion Rate")
    ax1.set_xlabel("VoP Threshold")
    ax1.set_ylabel("Conversion Rate (%)")
    st.pyplot(fig1, clear_figure=True)

    # Plot latency vs VoP threshold
    fig2, ax2 = plt.subplots()
    ax2.plot(vop_curves["vop_threshold"], vop_curves["latency_p95"], marker="o", linewidth=2)
    ax2.set_title("VoP strictness → Latency p95")
    ax2.set_xlabel("VoP Threshold")
    ax2.set_ylabel("Latency p95 (s)")
    st.pyplot(fig2, clear_figure=True)

# --- Tab 2: Fraud
with tab_fraud:
    st.write(
        "Lower Fraud thresholds flag more items, **raising Manual Review load** but **reducing Risk Exposure**."
    )
    # Dual-axis plot to show trade-offs clearly
    fig3, ax_left = plt.subplots()
    ax_left.plot(
        fraud_curves["fraud_threshold"], fraud_curves["manual_review_rate"],
        marker="o", linewidth=2
    )
    ax_left.set_xlabel("Fraud Threshold")
    ax_left.set_ylabel("Manual Review Rate (%)")

    # Second axis for risk exposure
    ax_right = ax_left.twinx()
    ax_right.plot(
        fraud_curves["fraud_threshold"], fraud_curves["risk_exposure_eur"],
        marker="s", linewidth=2
    )
    ax_right.set_ylabel("Risk Exposure (€)")
    fig3.suptitle("Fraud filter strictness → Risk vs Manual Load")
    fig3.tight_layout()
    st.pyplot(fig3, clear_figure=True)

# -----------------------------
# Section: Interpretation (human narrative)
# -----------------------------
st.markdown("### 🧩 Interpretation")
st.info(
    "- **VoP:** Increasing strictness improves name-match assurance but typically lowers conversion and adds latency.\n"
    "- **Fraud:** Lowering the threshold catches more suspicious items, lowering risk but driving manual workload.\n"
    "- **Balance:** As a rule-of-thumb, VoP ≈ 0.75–0.85 and Fraud ≈ 0.40–0.55 keeps Conversion healthy, "
    "Latency under control, and Risk acceptable without overwhelming analysts."
)

# -----------------------------
# Section: Data Context & Notes
# -----------------------------
with st.expander("ℹ️ Data context & assumptions (open)"):
    st.markdown(
        """
- **Source context:** Bundesbank payment statistics (2022–2024) validate market trends (growth in instant & electronic payments).
- **Important:** VoP and Fraud signals are **not** present in the source; this simulator uses **synthetic transactions** to explore *what-if* readiness settings.
- **Intended use:** Internal workshops and decision support to pre-tune operational parameters before full deployment.
"""
    )

# -----------------------------
# Optional: Download helpers (for demo completeness)
# -----------------------------
# Provide compact CSV exports of curves for easy sharing
dl_c1, dl_c2 = st.columns(2)
with dl_c1:
    st.download_button(
        label="⬇️ Download VoP curves (CSV)",
        data=vop_curves.to_csv(index=False),
        file_name="vop_curves.csv",
        mime="text/csv"
    )
with dl_c2:
    st.download_button(
        label="⬇️ Download Fraud curves (CSV)",
        data=fraud_curves.to_csv(index=False),
        file_name="fraud_curves.csv",
        mime="text/csv"
    )

# -----------------------------
# Footer
# -----------------------------
st.caption(
    "© Instant Payments Readiness & Impact Simulator — educational demo. "
    "Graphs and KPIs are computed from synthetic data to illustrate operational trade-offs."
)
