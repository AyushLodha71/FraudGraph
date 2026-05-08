import pandas as pd
from data.baseline import build_baseline
from data.anomaly import calculate_suspicion

data = pd.read_csv("data/train_transaction.csv")
data = data.copy()
card_baseline, global_mean, global_std = build_baseline(data)
data['suspicion_score'] = data.apply(
    lambda row: calculate_suspicion(row, card_baseline, global_mean, global_std), 
    axis=1
)

THRESHOLD = 4
data['flagged'] = (data['suspicion_score'] > THRESHOLD).astype(int)

true_positives = len(data.loc[(data['isFraud'] == 1) & (data['flagged'] == 1)])
false_positives = len(data.loc[(data['isFraud'] == 0) & (data['flagged'] == 1)])
false_negatives = len(data.loc[(data['isFraud'] == 1) & (data['flagged'] == 0)])

precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)
f1 = 2 * precision * recall / (precision + recall)
print("true_positives: " + str(true_positives))
print("false_positives: " + str(false_positives))
print("false_negatives: " + str(false_negatives))
print("precision: " + str(precision))
print("recall: " + str(recall))
print("f1 score: " + str(f1))
