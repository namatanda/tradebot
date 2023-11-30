# trading_bot/trading_bot.py
"""
Main script for the trading bot.
"""

import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from alpaca_client import YahooFinanceClient
from data_processor import process_data
from backtester import run_backtest
from trade_strategy import MyStrategy  # Import your strategy

# Load environment variables from a .env file
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)

# Create a logger
logger = logging.getLogger(__name__)

def execute_trades(data, symbol, ending_portfolio_value):
    """
    Execute trades based on generated signals.

    Args:
        data (pd.DataFrame): Data with trading signals.
        symbol (str): Stock symbol.
        ending_portfolio_value (float): Portfolio value at the end of the backtest.
    """
    # Implement your trade execution logic here based on signals
    # You can use the ending_portfolio_value or other information from the backtest
    data_with_signals = MyStrategy.generate_signals(data)  # Example, use your strategy functions

    for index, row in data_with_signals.iterrows():
        if row['signal'] == 1:
            # Buy signal
            logger.info(f"Executing BUY order for {symbol} at {row['close']}")
            # Implement your buy order execution logic here

        elif row['signal'] == -1:
            # Sell signal
            logger.info(f"Executing SELL order for {symbol} at {row['close']}")
            # Implement your sell order execution logic here

def main():
    """
    Main function to run the trading bot.
    """
    # Use environment variables for configuration
    api = YahooFinanceClient()
    symbols = api.get_symbols()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 2)  # 2 years historical data

    for symbol in symbols:
        logger.info(f"Processing data for {symbol}")
        historical_data = api.get_historical_data(symbol, start_date, end_date)
        
        # Run backtest and get results
        ending_portfolio_value = run_backtest(historical_data)

        # Process data
        processed_data = process_data(historical_data)

        # Implement your strategy here based on processed_data
        execute_trades(processed_data, symbol, ending_portfolio_value)

if __name__ == "__main__":
    main()
