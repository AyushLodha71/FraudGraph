import pandas as pd
data = pd.read_csv("train_transaction.csv")
print(data.head())
card_counts = data['card1'].value_counts()
valid_cards = card_counts[card_counts >= 20].index
data = data[data['card1'].isin(valid_cards)]
dgb = data.groupby(by='card1')
print(dgb.head())
stats = dgb['TransactionAmt'].agg(['mean', 'std', 'count'])
globalstats = data['TransactionAmt'].agg(['mean', 'std', 'count'])
print(stats)
print(data['TransactionAmt'].agg(['mean', 'std', 'count']))
null_std = stats[stats['std'] == 0]
print(len(null_std))

