# Instant-Payments-Readiness-Impact-Simulator-DE-Banking-
SCT Inst readiness &amp; impact simulator: models how VoP and fraud thresholds affect payment success rate, p95 latency, and manual reviews using synthetic transactions; outputs KPIs and recommended settings.

link of the data - https://www.bundesbank.de/en/statistics/banks-and-other-financial-corporations/payments-statistics/statistics-on-payments-and-securites-trading-clearing-and-settlement-in-germany-810330

dataset - I. Payments statistics (24.07.2025)

🚀 Quick Start
Prerequisites

Python 3.9–3.11

pip (or pipx)

macOS/Linux/Windows are all fine

1) Clone & enter the project
git clone <your_repo_url>.git
cd Instant-Payments-Readiness-Impact-Simulator-DE-Banking-

2) Create venv & activate
python -m venv venv
# macOS / Linux:
source venv/bin/activate
# Windows (PowerShell):
# .\venv\Scripts\Activate.ps1

3) Install requirements
pip install -r requirements.txt
# If Streamlit is not listed, also run:
# pip install streamlit

4) Run the simulator app
# IMPORTANT: run from the project root (not from /app)
streamlit run app/streamlit_app.py


Open the printed URL (e.g., http://localhost:8501) in your browser.

5) Run tests (optional but recommended)
pytest -q


1. What I am Analyzing (Contextual Analysis)

The project analyzes the half-yearly payment statistics published by the Deutsche Bundesbank (2022–2024) to understand the German payment market's shift toward instant transactions.

Data Source

Focus

Analytical Goal

Bundesbank Statistics

SCT Inst growth, traditional credit transfers, card and ATM usage.

To validate the urgency of Instant Payments adoption and establish a realistic base-load and risk context for the subsequent simulation phase.

2. Key Hypotheses for Testing (Simulator Focus)

My main objective is to build a Readiness Simulator that allows a bank to test different operational parameters against key performance indicators (KPIs). The following hypotheses drive the simulator's logic:

H1: SCT Inst Growth and Cannibalization (Trend Validation)

Assertion: The growth in electronic credit transfers (including SCT Inst) correlates with a corresponding decrease in paper-based transfers, indicating a rapid, successful digital transformation.

Purpose: Use data analysis to confirm market behavior and justify the Simulator's necessity.

H2: Verification of Payee (VoP) vs. Conversion and Latency (Simulator KPI)

Assertion: Implementing stricter Verification of Payee (VoP) filters significantly reduces fraud/error, but this comes at a cost of operational efficiency.

Simulator Test: Strict VoP settings will result in a measurable drop in the Conversion Rate of successful transactions and an increase in p95 Latency for transactions requiring enhanced validation or manual routing.

H3: Fraud Filter Stringency vs. Operational Load (Simulator KPI)

Assertion: Increasing the sensitivity of fraud detection rules (lowering the threshold) is a direct trade-off between risk exposure and operational overhead.

Simulator Test: Higher filter stringency reduces the total Risk Exposure (EUR) for the bank, but simultaneously increases the Manual Review Rate (%), stressing the fraud operations team.

H4: Volume Correlation with Infrastructure Load (Contextual KPI)

Assertion: The observed year-over-year increase in overall electronic transaction volumes (e.g., card payments, credit transfers) signals a growing stress on the bank's core payment processing infrastructure.

Simulator Test: The historical transaction growth rate is used as the input load parameter to simulate and monitor critical performance metrics like p95 Latency under growing pressure.

🎯 Executive Summary and Project Goal

The project is focused on analyzing the dynamics of the German payment market and developing a Readiness Simulator for a financial institution. The goal is to help the bank optimize operational parameters (VoP, Fraud Filters, Operating Modes) to achieve the ideal balance between Security, Speed, and Operational Load in the era of instant payments.

1. 📊 Subject and Contextual Analysis

We analyze the semi-annual payment statistics from the Deutsche Bundesbank for 2022–2024 to identify key market trends.

Data Source

Focus Analysis

Analytical Task

Bundesbank Statistics

SCT Inst growth, traditional transfers, card and ATM/POS usage.

Confirm the relevance of SCT Inst implementation and establish a realistic context of load and risk for the Simulator.

2. 🧪 Key Hypotheses for Simulation

A total of four hypotheses are formulated. The first is validated through data analysis, and the remaining three are tested by running the Simulator with various input parameters.

H1: SCT Inst Growth and Cannibalization (Trend Validation)

Assertion: The increase in the share of electronic transfers (including SCT Inst) correlates with a decrease in the number of paper-based transfers, signaling a rapid digital transformation of the market.

Project Link: Justification for the necessity of the Simulator.

H2: Verification of Payee (VoP) vs. Conversion and Latency (KPI: Speed)

Assertion: Implementing a strict VoP filter reduces errors but can negatively impact efficiency.

Simulator Test: Strict VoP settings will lead to a drop in the Conversion Rate of successful transactions and an increase in p95 Latency for transfers requiring manual review.

H3: Fraud Filter Stringency vs. Operational Load (KPI: Risk vs. Operations)

Assertion: Increasing the stringency of fraud filters represents a direct compromise between risk and operational load.

Simulator Test: Higher filter stringency reduces the overall Monetary Fraud Risk (Risk Exposure, EUR), but simultaneously increases the Manual Review Rate (%).

H4: Volume Correlation with Infrastructure Load (KPI: Scalability)

Assertion: The general growth of electronic transactions (credit transfers, cards) in the country signals an increasing load on the bank's payment infrastructure.

Simulator Test: Historical volume growth is used as the input load parameter to monitor the critical p95 Latency under growing pressure.

📁 Project Structure
project/
├── data/
│   ├── raw/              # original Bundesbank Excel data
│   ├── interim/          # intermediate cleaned tables
│   └── processed/        # final tidy-format datasets for analysis
├── notebooks/
│   ├── 01_data_extraction_cleaning.ipynb   # extracts tables from Excel
│   ├── 02_data_transform_tidy.ipynb        # cleaning and transformation
│   └── 03_data_exploration.ipynb           # data exploration and visualization (next step)
└── README.md

⚙️ Workflow Overview
🧩 Step 1 — Data Extraction & Cleaning

Open 01_data_extraction_cleaning.ipynb

Load the Bundesbank Excel file (I.Payments_statistics_810262.xlsx)

Read sheets table_3 (transactions) and table_4 (values)

Save clean CSV files to data/interim/

🧩 Step 2 — Data Transformation (Tidy Format)

Open 02_data_transform_tidy.ipynb

Remove helper rows ("of which", "Total")

Standardize column names (2022 S1, 2022 S2 → 2022H1, 2022H2)

Transform wide-format tables into tidy format using melt()

Save tidy datasets to data/processed/

🧩 Step 3 — Data Exploration & Visualization

Open 03_data_exploration.ipynb

Analyze SCT Inst growth and the decline of paper-based transfers

Compare electronic vs. traditional credit transfers

Produce first visualizations (line charts and trends)
(next stage to be implemented)

🧩 Version Control Workflow (Git)

Below is the basic command sequence used in this project to track changes and keep the repository up to date:

# 1️⃣ Check project status (see modified and untracked files)
git status

# 2️⃣ Add all new and modified files to the staging area
git add .

# 3️⃣ Commit your changes with a clear, descriptive message
git commit -m "Stage 1: Data extraction and cleaning completed (Bundesbank payments)"

# 4️⃣ Push commits to the remote GitHub repository
git push