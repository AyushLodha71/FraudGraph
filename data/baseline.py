import pandas as pd

def build_baseline(data):
    # Filter to cards with >= 20 transactions for reliable Z-score baseline
    card_counts = data['card1'].value_counts()
    valid_cards = card_counts[card_counts >= 20].index
    filtered_data = data[data['card1'].isin(valid_cards)]
    
    # Per-card baseline
    cols = ['TransactionAmt','V95','V96','V97','V98','V99','V100']
    card_baseline = filtered_data.groupby('card1')[cols].agg(['mean', 'std',])
    card_counts_filtered = filtered_data.groupby('card1')['TransactionAmt'].agg(['count'])
    
    # Global baseline for low-count cards
    global_stats = filtered_data[cols].agg(['mean', 'std'])
    card_baseline.columns = ['_'.join(col) for col in card_baseline.columns]
    return card_baseline, card_counts_filtered, global_stats
