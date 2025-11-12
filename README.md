💶 Instant Payments Readiness & Impact Simulator (DE Banking)

SCT Inst readiness simulator: explore how Verification of Payee (VoP) and Fraud Filter thresholds affect Conversion Rate, Latency p95, Manual Review Rate, and Risk Exposure.
Combines Bundesbank payment trends (2022–2024) with a synthetic “what-if” model to recommend operating settings.

🔗 Data Source

Deutsche Bundesbank — Statistics on payments and securities trading, clearing and settlement in Germany.
Section I. Payments statistics (24.07.2025).
Source hub: https://www.bundesbank.de/en/statistics/banks-and-other-financial-corporations/payments-statistics/statistics-on-payments-and-securites-trading-clearing-and-settlement-in-germany-810330

Note: Bundesbank data validates market trends (SCT Inst growth, credit transfers, cards, etc.).
It does not contain VoP/Fraud fields — the simulator uses synthetic transactions for scenario testing.

🚀 Quick Start
Prerequisites

Python 3.9–3.11

pip (or pipx)

macOS / Linux / Windows

1) Clone & enter the project
git clone <your_repo_url>.git
cd Instant-Payments-Readiness-Impact-Simulator-DE-Banking-

2) Create & activate a virtual environment
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
# .\venv\Scripts\Activate.ps1

3) Install dependencies
pip install -r requirements.txt
# (If needed) pip install streamlit

4) Run the simulator app
# IMPORTANT: run from the project root (not from /app)
streamlit run app/streamlit_app.py


Open the printed URL (e.g., http://localhost:8501) in your browser.

5) Run unit tests (optional, recommended)
pytest -q

🎯 What this project answers

Goal: help a bank balance speed, security, and operational load when adopting SCT Inst.

Hypotheses:

H1 — SCT Inst growth vs paper-based transfers (trend validation).
Electronic credit transfers (incl. SCT Inst) rise as paper-based decline → market is digitizing.

H2 — VoP strictness → Conversion & Latency.
Stricter payee-name checks reduce mistakes but lower conversion and increase p95 latency.

H3 — Fraud filter threshold → Risk vs Manual load.
Tighter filters reduce risk exposure but increase manual reviews (ops workload).

H4 — Volumes → Infrastructure load.
Growing electronic volumes imply higher p95 latency pressure → need for smart tuning.

How it works:

Descriptive analysis of Bundesbank trends (2022–2024).

Synthetic simulator for instant payments to test VoP & Fraud thresholds.

Interactive Streamlit app to explore trade-offs and pick recommended settings.

🧭 Project Structure
project-root/
├── app/
│   └── streamlit_app.py                # Interactive Streamlit dashboard
├── src/
│   └── sim_core.py                     # Simulation logic (VoP/Fraud & scans)
├── data/
│   ├── raw/                            # Original Bundesbank Excel/PDF
│   ├── interim/                        # Cleaned but not yet tidy
│   └── processed/                      # Tidy CSVs for analysis
├── notebooks/
│   ├── 01_data_extraction_cleaning.ipynb
│   ├── 02_data_transform_tidy.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   ├── 04_hypothesis_validation.ipynb
│   └── 05_simulation_experiments.ipynb
├── tests/
│   └── test_sim_core.py                # Unit tests for simulator core
├── requirements.txt
└── README.md

🔬 Workflow Overview
🧩 Step 1 — Data extraction & cleaning

Load Bundesbank Excel (I.Payments_statistics_810262.xlsx).

Extract Table 3a/3b (transactions / values).

Save cleaned CSVs to data/interim/.

🧩 Step 2 — Tidy transformation

Remove helper rows (e.g., “of which”).

Standardize columns (2022 S1→2022H1, etc.).

Convert to long (tidy) format with melt().

Save tidy CSVs to data/processed/.

🧩 Step 3 — Exploratory analysis

Descriptive stats (mean, median, quartiles).

Visualize SCT Inst vs paper-based, domestic totals, volume trends.

Context for simulator inputs.

🧩 Step 4 — Hypothesis validation & simulation

Generate synthetic instant payments (amount, fraud probability, VoP score).

Functions in src/sim_core.py:

simulate_vop / scan_vop → Conversion & Latency p95 vs VoP threshold.

simulate_fraud / scan_fraud → Manual Review Rate & Risk Exposure vs fraud threshold.

Consolidate findings (balanced operating zone).

🧩 Step 5 — Interactive app

app/streamlit_app.py shows KPIs, curves, explanations, and CSV exports.

Live tuning of thresholds to see trade-offs.

📸 App Highlights (what to look for)

📈 KPI Snapshot: Conversion, Latency p95, Manual Review Rate, Risk Exposure — for current settings.

🔍 Sensitivity Curves:

VoP strictness → Conversion & Latency.

Fraud threshold → Manual load & Risk exposure (dual-axis chart).

🧩 Interpretation panel: short “so-what” explaining trade-offs and a rule-of-thumb balance.

Rule-of-thumb zone: VoP ≈ 0.75–0.85, Fraud ≈ 0.40–0.55
keeps Conversion healthy, Latency under control, and Risk acceptable without overwhelming analysts.

✅ Testing

tests/test_sim_core.py covers:

Synthetic generator shape/columns/ranges.

Output schema & ranges for simulate_vop / simulate_fraud.

Shapes/columns for scan_vop / scan_fraud.

Run:

pytest -q

🩹 Troubleshooting

ModuleNotFoundError: No module named 'src'

Run Streamlit from project root:
streamlit run app/streamlit_app.py

We also add the root to sys.path at the top of streamlit_app.py:

import sys, os
sys.path.append(os.path.abspath(".."))


Cache issues

streamlit cache clear

🧠 Why this project is relevant for a Data Analyst role

Business framing: shows a real trade-off (speed vs security vs ops load).

Data craft: tidy transformations, descriptive stats, trend validation.

Modeling: scenario simulation with clear, decision-ready KPIs.

Communication: interactive dashboard + concise narrative + tests.

🗺️ Roadmap (nice-to-have)

Add Plotly interactivity & tooltips.

Connect historical volumes as load inputs to scale latency scenarios.

Sensitivity heatmap (VoP × Fraud) to visualize global optima.

Export current KPIs as a one-click CSV/PNG.

📝 License & Attribution

Data © Deutsche Bundesbank — used for analytical/educational purposes.

Simulator code © You (MIT suggested).

🤝 Contact

Author: Your Name — Data Analyst

LinkedIn / Email: add your links here

Version Control (example)
git status
git add .
git commit -m "Stage 1: Data extraction & cleaning (Bundesbank payments)"
git push