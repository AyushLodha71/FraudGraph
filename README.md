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
├── explore.py       — dataset exploration and analysis
├── validate.py      — F1 scoring and model evaluation
├── train.py         — model training and saving
├── FINDINGS.md      — data exploration findings and design decisions
└── main.py          — runs the full pipeline
```

## Components

### 1. Cryptographic Audit Trail
SHA-256 hashing for tamper detection and ECDSA signing for report authentication. Every investigation report is signed and verifiable — mirroring FINTRAC requirements for tamper-evident suspicious transaction reports in Canada.

### 2. Data Pipeline
590,540 transactions, 394 features. Built per-card behavioral baselines using pandas groupby. Designed minimum 20-transaction threshold for statistically reliable Z-score baselines — excludes 8.6% of transactions and 6.8% of fraud cases, documented in FINDINGS.md.

### 3. Statistical Anomaly Detection
Multi-dimensional Z-score scoring across 15 features (TransactionAmt + C1-C14). Vectorized pandas implementation for performance — 0.12 second merge vs 30-60 minute row-by-row apply(). Global fallback baseline for low-history cards.

Results:
- Naive baseline F1: 6.76%
- Z-score F1 (threshold=5): 5.68%
- Limitation: Z-score cannot detect coordinated fraud invisible at the individual transaction level — addressed by graph layer (planned)

### 4. Machine Learning Classification (In Progress)
Random Forest classifier with class_weight="balanced" to handle 3.5% fraud rate. Features selected based on missing value analysis (<20% null threshold). Model saved with joblib for reuse without retraining.

## Planned Extensions
- **Graph-based fraud ring detection** — bipartite transaction graph using NetworkX, centrality analysis to identify compromised merchants, community detection to surface coordinated fraud rings
- **Investigation optimization** — knapsack optimization to maximize fraud recovery under compliance team resource constraints, Dijkstra's algorithm to trace investigation paths

## Setup

```bash
pip install cryptography pandas numpy scikit-learn networkx matplotlib joblib
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

## Key Design Decisions
- **Threshold = 20 transactions** — balances statistical reliability against coverage loss (8.6% transactions, 6.8% fraud excluded)
- **C1-C14 over V columns** — empirically tested: V columns hurt F1 from 5.68% to 4.13% due to high missing rate and unknown semantics
- **Vectorized scoring** — replaced row-by-row apply() with pandas merge + vectorized operations, reducing runtime from ~60 min to <1 sec
- **class_weight="balanced"** — handles 96.5%/3.5% class imbalance without resampling

## Results

| Approach | F1 Score |
|---|---|
| Naive baseline (flag everything) | 6.76% |
| Z-score anomaly detection | 5.68% |
| Random Forest (in progress) | TBD |


## Tech Stack
Python, pandas, NumPy, scikit-learn, NetworkX, matplotlib, cryptography, joblib
