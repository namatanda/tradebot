# data_processor.py
import pandas as pd
import talib

def calculate_technical_indicators(data):
    # Calculate technical indicators using talib
    data['rsi'] = talib.RSI(data['close'], timeperiod=14)
    data['macd'], _, _ = talib.MACD(data['close'])
    data['sma'] = talib.SMA(data['close'], timeperiod=20)
    return data

def backtest_strategy(data, signal_column='signal'):
    # Simple backtesting framework
    initial_balance = 100000  # Initial portfolio balance
    balance = initial_balance
    position = 0  # 0 means no position, 1 means long, -1 means short
    shares_held = 0
    pnl = []

    for index, row in data.iterrows():
        if row[signal_column] == 1 and position == 0:
            # Buy signal
            position = 1
            shares_held = balance // row['close']
            balance -= shares_held * row['close']
        elif row[signal_column] == -1 and position == 1:
            # Sell signal
            position = 0
            balance += shares_held * row['close']
            shares_held = 0

        pnl.append(balance + shares_held * row['close'])

    data['pnl'] = pnl
    return data

def calculate_momentum(data, lookback_period=14):
    data['close_delta'] = data['close'].diff()
    data['momentum'] = data['close_delta'].rolling(window=lookback_period).sum()
    return data

def process_data(data):
    data = calculate_momentum(data)
    data = calculate_technical_indicators(data)
    return data

