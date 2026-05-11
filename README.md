# FraudGraph

A financial fraud detection system built on 590,540 real credit card transactions from the IEEE-CIS dataset. Combines statistical anomaly detection, machine learning classification, and cryptographic audit trails to identify fraudulent transactions and generate tamper-evident investigation reports.

## Project Structure

```
FraudGraph/
├── crypto/          — SHA-256 tamper detection + ECDSA signing
├── data/            — data pipeline, baselines, anomaly detection
├── graph/           — planned: NetworkX fraud ring detection
├── optimization/    — planned: knapsack + Dijkstra investigation routing
├── notebooks/       — Jupyter exploration and ML prototyping
├── models/          — saved trained models (not pushed to GitHub)
├── data/explore.py  — dataset exploration and analysis
├── validate.py      — F1 scoring and model evaluation
├── train.py         — trains and saves both ML models
├── FINDINGS.md      — data exploration findings and design decisions
└── main.py          — runs the full pipeline
```

## Components

### 1. Cryptographic Audit Trail
SHA-256 hashing for tamper detection and ECDSA signing for report authentication using the P-256 curve. Every investigation report is signed and verifiable — mirroring FINTRAC requirements for tamper-evident suspicious transaction reports in Canada.

### 2. Data Pipeline
590,540 transactions, 394 features. Built per-card behavioral baselines using pandas groupby. Designed minimum 20-transaction threshold for statistically reliable Z-score baselines — excludes 8.6% of transactions and 6.8% of fraud cases. Full analysis documented in FINDINGS.md.

### 3. Statistical Anomaly Detection
Multi-dimensional Z-score scoring across 15 features (TransactionAmt + C1-C14). Vectorized pandas implementation — 0.12 second merge vs 30-60 minute row-by-row apply(). Global fallback baseline for low-history cards. Empirically tested V columns — adding V95-V100 hurt F1 from 5.68% to 4.13%, confirming C columns as the stronger signal.

### 4. Machine Learning Classification
Two models trained and compared on 252 features (181 numeric + encoded categoricals). Features engineered from raw data — hour of day and day of week extracted from timestamp, categorical columns encoded with get_dummies. Class imbalance (96.5% legitimate / 3.5% fraud) handled via class_weight="balanced" in Random Forest and scale_pos_weight in XGBoost. Models saved with joblib for reuse without retraining.

## Model Comparison

| Approach | F1 | Precision | Recall | Notes |
|---|---|---|---|---|
| Naive baseline | 6.76% | 3.5% | 100% | Flags everything |
| Z-score anomaly detection | 5.68% | 9.9% | 2.6% | Individual transaction scoring |
| Random Forest | 59.0% | 93% | 43% | Conservative — high precision |
| XGBoost | 40.0% | 26% | 82% | Aggressive — high recall |

**Selected model: Random Forest** — higher F1 and more practically useful. 93% precision means fewer false positives and less customer friction. XGBoost's aggressive flagging (26% precision) would flag too many legitimate transactions in a production environment.

## Planned Extensions
- **Graph-based fraud ring detection** — bipartite transaction graph using NetworkX, centrality analysis to identify compromised merchants, community detection to surface coordinated fraud rings invisible to per-transaction scoring
- **Investigation optimization** — knapsack optimization to maximize fraud recovery under compliance team resource constraints, Dijkstra's algorithm to trace investigation paths through suspect networks

## Setup

```bash
pip install cryptography pandas numpy scikit-learn xgboost networkx matplotlib joblib
```

For XGBoost on Mac:
```bash
brew install libomp
```

## Data

Download IEEE-CIS Fraud Detection dataset from Kaggle:
https://www.kaggle.com/c/ieee-fraud-detection/data

Place files in data/:
```
data/
├── train_transaction.csv
└── train_identity.csv
```

## Usage

Train and save both models:
```bash
python train.py
```

Evaluate Z-score anomaly detection:
```bash
python validate.py
```

## Key Design Decisions
- **Threshold = 20 transactions** — balances statistical reliability against coverage loss (8.6% transactions, 6.8% fraud excluded)
- **C1-C14 over V columns** — empirically tested: V columns hurt F1 from 5.68% to 4.13% due to high missing rate and unknown semantics
- **Vectorized scoring** — replaced row-by-row apply() with pandas merge + vectorized operations, reducing runtime from ~60 min to under 1 second
- **Random Forest over XGBoost** — higher F1 (59% vs 40%) and 93% precision reduces customer friction in production
- **class_weight="balanced"** — handles 96.5%/3.5% class imbalance without resampling

## What I Learned

Building FraudGraph gave me hands-on experience with cryptographic fundamentals — implementing SHA-256 and ECDSA from scratch gave me a much deeper understanding than reading about them ever could. I genuinely understood precision, recall, and F1 score for the first time by seeing how changing a detection threshold directly moved false positives and false negatives in real fraud data. The project also reinforced my data science fundamentals — handling class imbalance, cleaning missing values, and encoding categorical features for ML models. Feature importance analysis revealed that transaction amount, card identity, and time of day were the strongest fraud signals, pointing toward richer feature engineering as a future direction.

## Tech Stack
Python, pandas, NumPy, scikit-learn, XGBoost, NetworkX, matplotlib, cryptography, joblib
