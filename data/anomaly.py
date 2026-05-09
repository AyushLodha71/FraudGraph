import pandas as pd
def calculate_suspicion(transaction, card_baseline, global_stats):
    suspicion_score = 0
    card = transaction['card1']
    entry = []
    cols = ['TransactionAmt','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14']
    if card in card_baseline.index:
        entry = card_baseline.loc[card]
    if (len(entry) == 0):
        for col in cols:
            if pd.isna(transaction[col]):
                continue
            elif (global_stats.loc['std', col] == 0):
                return float('inf')
            else:
                suspicion_score += abs((transaction[col] - global_stats.loc['mean',col]))/global_stats.loc['std', col]
    else:
        for col in cols:
            if pd.isna(transaction[col]):
                continue
            elif (entry[(col,'std')] == 0):
                return float('inf')
            else:
                suspicion_score += abs((transaction[col] - entry[(col,'mean')]))/entry[(col,'std')]
    return suspicion_score

def calculate_suspicion_vectorized(data, card_baseline, global_stats):
    cols = ['TransactionAmt','V95','V96','V97','V98','V99','V100']

    # fill missing baseline values with global stats for low-count cards
    for col in cols:
        data[f'{col}_mean'] = data[f'{col}_mean'].fillna(global_stats.loc['mean', col])
        data[f'{col}_std'] = data[f'{col}_std'].fillna(global_stats.loc['std', col])

    # compute Z-scores vectorized
    suspicion_score = pd.Series(0.0, index=data.index)
    for col in cols:
        std = data[f'{col}_std']
        mean = data[f'{col}_mean']
        value = data[col]
        z = (value - mean) / std.replace(0, float('nan'))
        suspicion_score += z.abs().fillna(0)
    data['suspicion_score'] = suspicion_score
    return suspicion_score
