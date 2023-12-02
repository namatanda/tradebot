# trading_bot/trading_bot.py
import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from tradebot.data_client import YahooFinanceClient
from tradebot.data_processor import process_data
from tradebot.backtester import run_backtest
from tradebot.trade_strategy import MyStrategy
# Load environment variables from a .env file
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)

# Create a logger
logger = logging.getLogger(__name__)

def execute_trades(data, symbol, ending_portfolio_value):
    processed_data = process_data(data)
    # Use the processed_data as needed
    strategy_instance = MyStrategy(data=processed_data)
    strategy_instance.run()
    
def main():
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
