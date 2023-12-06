import os
import sys
import backtrader as bt
import datetime

class DonchianChannel(bt.Indicator):
    lines = ('upper', 'lower')

    params = (('period', 20),)

    def __init__(self):
        self.addminperiod(self.params.period + 1)  # Ensure enough historical data

    def next(self):
        if len(self) >= self.params.period:
            highest_high = max(self.data.high.get(size=self.params.period))
            lowest_low = min(self.data.low.get(size=self.params.period))
            self.lines.upper[0] = highest_high
            self.lines.lower[0] = lowest_low

class EMAStrategy(bt.Strategy):
    params = (('fast_ema', 12), ('slow_ema', 26), ('signal_ema', 9), ('donchian_period', 20),)

    def __init__(self):
        self.fast_ema = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.params.fast_ema)
        self.slow_ema = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.params.slow_ema)
        self.signal_ema = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.params.signal_ema)
        self.donchian = DonchianChannel(self.data)

    def next(self):
        if self.fast_ema > self.slow_ema and self.data.close > self.donchian.lines.upper:
            self.buy()
        elif self.fast_ema < self.slow_ema and self.data.close < self.donchian.lines.lower:
            self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    datapath = os.path.join(modpath, '../data/TSLA.csv')
    
    data = bt.feeds.YahooFinanceCSVData(dataname=datapath, fromdate=datetime.datetime(2022, 10, 31), todate=datetime.datetime(2023, 4, 30),) 
   
    cerebro.adddata(data)
    cerebro.addstrategy(EMAStrategy)

    cerebro.run()

    cerebro.plot(style='candlestick')  # You can visualize the results with a candlestick chart


