# trading_bot/backtester.py
"""
Module for running backtests on trading strategies.
"""

import backtrader as bt
import pyfolio as pf
from tradebot.trade_strategy import MyStrategy  # Import your strategy

def run_backtest(data):
    """
    Run a backtest on a given dataset using the provided strategy.

    Args:
        data (pd.DataFrame): Historical stock data for backtesting.

    Returns:
        float: Ending portfolio value after the backtest.
    """
    cerebro = bt.Cerebro()

    # Add data to backtest
    data = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data)

    # Add strategy to backtest
    cerebro.addstrategy(MyStrategy)

    # Set initial cash
    cerebro.broker.set_cash(100000)

    # Set commission
    cerebro.broker.setcommission(commission=0.001)

    # Run the backtest
    cerebro.run()

    # Analyze performance with pyfolio
    returns, positions, transactions, gross_lev = pf.utils.extract_rets_pos_txn_from_blotter(cerebro.blotter)
    pf.create_simple_tear_sheet(returns, positions=positions, transactions=transactions)

    # Return the ending portfolio value
    return cerebro.broker.getvalue()
