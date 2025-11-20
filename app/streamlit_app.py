# =============================================================
# 💶 Instant Payments Readiness Simulator — Streamlit App
# =============================================================

# --- PATH FIX (so imports from src work correctly)
import sys, os
# --- PATH FIX (so imports from src work correctly)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

FIG_DIR = os.path.join(BASE_DIR, "reports", "figures")

# --- LIBRARIES
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.sim_core import (
    generate_synth,
    simulate_vop,
    scan_vop,
    simulate_fraud,
    scan_fraud
)

# --- STREAMLIT SETTINGS
st.set_page_config(page_title="Instant Payments Readiness Simulator", layout="wide")
plt.rcParams["figure.figsize"] = (7,3.2)
plt.rcParams["axes.grid"] = True

# =============================================================
# HEADER
# =============================================================
st.title("💶 Instant Payments Readiness & Impact Simulator")

st.markdown("""
This app helps explore how **Verification of Payee (VoP)** and **Fraud Filter** thresholds affect:
- Conversion Rate  
- Latency (p95)  
- Manual Review Rate  
- Risk Exposure  

It combines:  
🔵 **Real Bundesbank data** (H1 & H2) + 🔴 **Synthetic simulations** (H3 & H4)  
to show a complete picture of instant payment readiness.
""")

# =============================================================
# SIDEBAR CONTROLS — Simulator settings
# =============================================================
st.sidebar.header("⚙️ Simulation Settings")

n_rows = st.sidebar.select_slider(
    "Synthetic transactions",
    options=[5000, 20000, 50000, 100000],
    value=20000
)

seed = st.sidebar.number_input("Random seed", 0, 999999, value=42)

vop_thr = st.sidebar.slider("VoP threshold", 0.50, 0.95, value=0.80, step=0.05)
fraud_thr = st.sidebar.slider("Fraud threshold", 0.20, 0.90, value=0.50, step=0.10)

# Grids for curves
vop_grid = np.arange(0.50, 0.95, 0.05)
fraud_grid = np.arange(0.20, 0.90, 0.10)

# =============================================================
# DATA (cached)
# =============================================================
@st.cache_data(show_spinner=False)
def load_data(n, seed):
    df = generate_synth(n=n, seed=seed)
    df["is_true_fraud"] = (df["fraud_probability"] > 0.90).astype(int)
    return df

df = load_data(n_rows, seed)

# KPIs
vop_res = simulate_vop(df, threshold=vop_thr)
fraud_res = simulate_fraud(df, threshold=fraud_thr)

vop_curves = scan_vop(df, vop_grid)
fraud_curves = scan_fraud(df, fraud_grid)

# =============================================================
# KPI SNAPSHOT
# =============================================================
st.subheader("📈 Current KPI Snapshot")

col1,col2,col3,col4 = st.columns(4)
col1.metric("Conversion Rate (%)", f"{vop_res['conversion_rate']:.1f}")
col2.metric("Latency p95 (s)", f"{vop_res['latency_p95']:.2f}")
col3.metric("Manual Review Rate (%)", f"{fraud_res['manual_review_rate']:.1f}")
col4.metric("Risk Exposure (€)", f"{fraud_res['risk_exposure_eur']:,.0f}")

st.caption(f"Current settings → VoP = {vop_thr:.2f}, Fraud = {fraud_thr:.2f}, N = {n_rows:,}")

# =============================================================
# TABS (5 Hypothesis sections)
# =============================================================
tab_h1, tab_h2, tab_h3, tab_h4, tab_heatmap = st.tabs([
    "📊 H1 — Instant vs Paper",
    "📈 H2 — Infrastructure Load",
    "🎛 H3 — VoP Simulation",
    "🔐 H4 — Fraud Simulation",
    "🌈 Final Heatmap"
])

# -----------------------------------------------------------
# TAB H1 — Real Data: Instant vs Paper
# -----------------------------------------------------------
with tab_h1:
    st.subheader("📊 H1 — Instant vs Paper-Based Transfers (Real Data)")
    st.write("Instant payments grow sharply, paper-based transfers decline → confirms digital transformation.")

    st.image(
        os.path.join(FIG_DIR, "H1_stacked_sct_vs_paper.png"),
        caption="SCT Inst vs Paper-Based (Bundesbank 2022–2024)"
    )

# -----------------------------------------------------------
# TAB H2 — Real Data: Infrastructure Load
# -----------------------------------------------------------
with tab_h2:
    st.subheader("📈 H2 — Domestic Electronic Payments (System Load)")
    st.write("Domestic electronic payments (volume & value) grow → load on banking infrastructure increases.")

    st.image(
    os.path.join(FIG_DIR, "H2_total_domestic.png"),
    caption="Domestic Transaction Volume (2022–2024)"
    )
    st.image(
        os.path.join(FIG_DIR, "H2_total_domestic_values.png"),
        caption="Domestic Payment Values (2022–2024)"
    )

# -----------------------------------------------------------
# TAB H3 — VoP Simulation
# -----------------------------------------------------------
with tab_h3:
    st.subheader("🎛 H3 — VoP Simulation (Conversion & Latency)")
    st.write("Stricter VoP → fewer passes → **lower conversion** & **higher latency**.")

    fig1, ax1 = plt.subplots()
    ax1.plot(vop_curves["vop_threshold"], vop_curves["conversion_rate"], marker="o")
    ax1.set_title("VoP strictness → Conversion Rate")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.plot(vop_curves["vop_threshold"], vop_curves["latency_p95"], marker="o")
    ax2.set_title("VoP strictness → Latency p95")
    st.pyplot(fig2)

# -----------------------------------------------------------
# TAB H4 — Fraud Simulation
# -----------------------------------------------------------
with tab_h4:
    st.subheader("🔐 H4 — Fraud Simulation (Risk & Manual Review)")
    st.image(
        os.path.join(FIG_DIR, "H4_line_fraud_risk_exposure.png"),
        caption="Effect of Fraud Threshold on Manual Review Rate and Risk Exposure",
        use_container_width=True
    )

# -----------------------------------------------------------
# TAB — FINAL HEATMAP
# -----------------------------------------------------------
with tab_heatmap:
    st.subheader("🌈 Final Heatmap — Optimal VoP × Fraud Balance")

    st.image(
        os.path.join(FIG_DIR, "H5_heatmap_vop_fraud_optimal.png"),
        caption="Optimal VoP × Fraud Operating Region (Based on KPI Score)",
        use_container_width=True
    )

    st.info("""
**Interpretation:**  
- Higher VoP improves accuracy but reduces conversion  
- Lower Fraud reduces risk but increases manual load  
- **Optimal region: VoP ≈ 0.80 and Fraud ≈ 0.50**
""")

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


# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------
st.caption("© Instant Payments Readiness & Impact Simulator — Synthetic simulation + real Bundesbank data.")



