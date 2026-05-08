def calculate_suspicion(transaction, card_baseline, global_mean, global_std):
    suspicion_score = 0
    card = transaction['card1']
    entry = []
    if card in card_baseline.index:
        entry = card_baseline.loc[card]
    if (len(entry) == 0):
        if (global_std == 0):
            suspicion_score = float('inf')
        else:
            suspicion_score = (transaction['TransactionAmt'] - global_mean)/global_std
    else:
        if (entry['std'] == 0):
            suspicion_score = float('inf')
        else:
            suspicion_score = (transaction['TransactionAmt'] - entry['mean'])/entry['std']
    return abs(suspicion_score)
