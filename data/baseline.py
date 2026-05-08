import pandas as pd

def build_baseline(data):
    # Filter to cards with >= 20 transactions for reliable Z-score baseline
    card_counts = data['card1'].value_counts()
    valid_cards = card_counts[card_counts >= 20].index
    filtered_data = data[data['card1'].isin(valid_cards)]
    
    # Per-card baseline
    card_baseline = filtered_data.groupby('card1')['TransactionAmt'].agg(['mean', 'std', 'count'])
    
    # Global baseline for low-count cards
    global_mean = filtered_data['TransactionAmt'].mean()
    global_std = filtered_data['TransactionAmt'].std()
    
    return card_baseline, global_mean, global_std
