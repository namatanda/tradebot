# trading_bot/strategy.py
"""
Module for defining trading strategies.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime
import os
import sys
import pandas as pd
import backtrader as bt
import logging
from data_processor import process_data

logger = logging.getLogger(__name__)

class MACrossover(bt.Strategy):

    params = (('pfast', 20), ('pslow', 50), ('myparam', 27),('exitbars', 3),)

    def log(self, text, dt= None):
        # get the date from the date column
        date_time = dt or self.datas[0].datetime.date(0)
        #log date and close
        logger.info(f"{date_time.isoformat()} {text}")


    def __init__(self):
        # data[0] refers to 1st data feed[ticker], data[1] would refer to the feed of the second ticker
        #data[n].close gets the close column, to get another column in ohlv data, use the appropriate column
        self.dataclose = self.datas[0].close
        self.bar_executed = 0
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.slow_sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.pslow)
        self.fast_sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.pfast)

        self.crossover = bt.indicators.CrossOver(self.slow_sma, self.fast_sma)
        self.signal_add(bt.SIGNAL_LONG, self.crossover)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY ORDER CREATED AT, Price: {order.executed.price:.2f} Cost:{order.executed.value:.2f} Comm:{order.executed.comm:.2f}')
            elif order.issell():
                self.log(f'SELL ORDER CREATED AT, Price: {order.executed.price:.2f} Cost:{order.executed.value:.2f} Comm:{order.executed.comm:.2f}')
            self.bar_executed = len(self)

        elif order.status in [order.Cancelled, order.Margin, order.Rejected]:
            self.log(f'Order Calcelled/Mrgin/Rejected')

        self.order = None


    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'OPERATION PROFIT, GROSS {trade.pnl:.2f}, NET {trade.pnlcomm:.2f}')

    def next(self):
        self.log(f'Close: {self.dataclose[0]}')
        
        if self.order:
            return
        # Check if we are in the market
        if not self.position:
            if self.dataclose[0] > self.slow_sma[0]:
            #if self.dataclose[0] < self.dataclose[-1]:
             #   if self.dataclose[-1] < self.dataclose[-2]:
                self.log(f'BUY ORDER CREATED AT {self.dataclose[0]:2f}')
                self.order = self.buy()
            elif self.dataclose[0] < self.slow_sma[0]:
                # We are already in the market, look for a signal to CLOSE trades
                #if len(self) >= (self.bar_executed + self.params.exitbars):
                self.log(f'CLOSE ORDER CREATED AT {self.dataclose[0]:2f}')
                self.order = self.close()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    cerebro = bt.Cerebro()
    
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    datapath = os.path.join(modpath, '../data/TSLA.csv')
    
    data = bt.feeds.YahooFinanceCSVData(dataname=datapath, fromdate=datetime.datetime(2022, 10, 31), todate=datetime.datetime(2023, 4, 30),) 
    
    cerebro.adddata(data)

    cerebro.addstrategy(MACrossover)

    cerebro.addsizer(bt.sizers.SizerFix, stake=1)

    start_portfolio_value = cerebro.broker.getvalue()

    cerebro.broker.setcommission(commission=0.001)

    cerebro.run()

    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    print(f'Starting Portfolio Value: {start_portfolio_value:.2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:.2f}')
    print(f'PnL: {pnl:.2f}')