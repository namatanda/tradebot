
from tradebot.trade_strategy import MyStrategy 
import backtrader as bt

def test_strategy_initialization():
    strategy = MyStrategy()
    assert isinstance(strategy, bt.Strategy)
