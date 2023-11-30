# strategy.py
def swing_momentum_strategy(data):
    data['signal'] = 0

    # Buy signal: Positive momentum and price closing above the previous day's high
    data.loc[(data['momentum'] > 0) & (data['close'] > data['high'].shift(1)), 'signal'] = 1

    # Sell signal: Negative momentum or price closing below the previous day's low
    data.loc[(data['momentum'] < 0) | (data['close'] < data['low'].shift(1)), 'signal'] = -1

    return data

