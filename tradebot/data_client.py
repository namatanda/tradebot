# client.py
import os
import yfinance as yf
import pandas as pd

class YahooFinanceClient:
    def get_symbols(self):
        # Get the list of S&P 500 symbols
        snp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        return snp500['Symbol'].tolist()

    def get_historical_data(self, symbol, start, end):
        # Get historical stock data using yfinance
        data = yf.download(symbol, start=start, end=end)
        return data

