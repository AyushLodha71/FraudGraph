import pandas as pd
import numpy as np

# DESIGN DECISION: chose threshold = 20
# Minimum 20 transactions per card for reliable Z-score baseline
# Cards below threshold will use global baseline instead
# Impact: excludes 8.6% of transactions, 6.8% of fraud cases

data = pd.read_csv("train_transaction.csv")

print("=== DATASET OVERVIEW ===")
print(data.head())

print("\n=== TRANSACTION AMOUNT DISTRIBUTION ===")
print(data['TransactionAmt'].describe())

print("\n=== FRAUD DISTRIBUTION ===")
print(data['isFraud'].value_counts())

print("\n=== MISSING VALUES — card1 ===")
print(data['card1'].isnull().sum())

print("\n=== MISSING VALUES — V columns ===")
print(data['V1'].isnull().sum())
print(data['V10'].isnull().sum())
print(len(data.loc[pd.isnull(data['V1']) & pd.isnull(data['V10'])]))

print("\n=== CARD TRANSACTION COUNT DISTRIBUTION ===")
unique, counts = np.unique(data['card1'], return_counts=True)
unique_counts, count = np.unique(counts, return_counts=True)
print(unique_counts[:5])
print(count[:10])
count_sum = 0
for i in range(10):
    count_sum += count[i]
print(count_sum)
print(count[:20])
count_sum = 0
for i in range(20):
    count_sum += count[i]
print(count_sum)
count_sum = 0
for i in range(20):
    count_sum += (i + 1) * count[i]
print(count_sum)
print(count[:30])
count_sum = 0
for i in range(30):
    count_sum += count[i]
print(count_sum)

print("\n=== CARD COUNTS — max, min, low count cards ===")
card_counts = data['card1'].value_counts(ascending=True)
print(card_counts.head())
print(card_counts.max())
print(card_counts.min())
low_count_cards = card_counts[card_counts < 20].index
print(len(low_count_cards))
fraud_count = 0
transaction_count = 0
low_count_data = data[data['card1'].isin(low_count_cards)]
fraud_count = (low_count_data['isFraud'] == 1).sum()
print(len(low_count_data))
print(fraud_count)

print("\n=== MISSING VALUES — V100 ===")
print(data['V100'].isnull().sum())

print("\n=== FRAUD DISTRIBUTION — normalized ===")
print(data['isFraud'].value_counts(normalize=True))

print("\n=== TOP 20 COLUMNS BY MISSING VALUES ===")
print(data.isnull().sum().sort_values(ascending=False).head(20))

print("\n=== THRESHOLD COMPARISON — 10, 20, 30 ===")
card_counts_desc = data['card1'].value_counts()
for threshold in [10, 20, 30]:
    low = card_counts_desc[card_counts_desc < threshold].index
    low_data = data[data['card1'].isin(low)]
    fraud_in_low = (low_data['isFraud'] == 1).sum()
    print(f"\n--- Threshold: {threshold} ---")
    print(f"Cards below threshold: {len(low)} of {len(card_counts_desc)}")
    print(f"Transactions excluded: {len(low_data)} ({len(low_data)/len(data)*100:.1f}%)")
    print(f"Fraud excluded: {fraud_in_low} ({fraud_in_low/data['isFraud'].sum()*100:.1f}% of all fraud)")


print(data[['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14']].isnull().sum())
print(data[['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14']].describe())
