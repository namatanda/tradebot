import os
import configparser
import logging
from datetime import datetime, timedelta
from typing import Union, List, Optional

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import pandas as pd

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_connection(api_config_path: str = ".\.env") -> bool:
    """
    Check the connection and set up environment variables for Alpaca API keys.

    Parameters:
    - api_config_path (str): Path to the configuration file containing Alpaca API keys.

    Returns:
    - bool: True if the connection is successful, False otherwise.
    """
    config = configparser.ConfigParser()
    loaded = config.read(api_config_path)

    if loaded:
        logger.info(f'Configuration file successfully read.')
        
        os.environ["KEY_ID"] = config["alpaca"]["KEY_ID"]
        os.environ["SECRET_KEY"] = config["alpaca"]["SECRET_KEY"]

        trading_client = TradingClient(os.environ["KEY_ID"], os.environ["SECRET_KEY"])
        account = trading_client.get_account()

        if account.trading_blocked:
            logger.info(f'Account is currently restricted from trading.')
            return False

        return True

    else:
        logger.info(f'Failed to read the configuration file')
        return False

def download_tickers(security: Union[List[str], str], start_date: str, api_config_path: str = ".\.env") -> pd.DataFrame:
    """
    Downloads historical stock data for the given security or list of securities using the alpaca api.

    Parameters:
    - security (Union[List[str], str]): A single security ticker or a list of tickers.
    - start_date (str): The start date for the historical data in the format 'YYYY-MM-DD'.
    - api_config_path (str): Path to the configuration file containing Alpaca API keys.

    Returns:
    pd.DataFrame: DataFrame containing historical stock data for the given security or securities
                 from the start date until the present.

    Example:
    >>> download_tickers('AAPL', '2022-01-01')
    >>> download_tickers(['AAPL', 'MSFT'], '2022-01-01')
    """
    if not check_connection(api_config_path):
        # Handle connection failure, raise an exception, or return an appropriate value.
        logger.error("Failed to establish a connection.")
        return pd.DataFrame()  # Or handle the error in your specific way

    # Initialize the StockHistoricalDataClient with your API keys
    client = StockHistoricalDataClient(os.environ["KEY_ID"], os.environ["SECRET_KEY"])

    # Prepare the request parameters
    request_params = StockBarsRequest(symbol_or_symbols=security, 
                                      timeframe=TimeFrame.Day,
                                      start=datetime.strptime(start_date, '%Y-%m-%d')
                                      )

    # Fetch historical data and reset the index
    bars = client.get_stock_bars(request_params).df.reset_index(level=[0, 1])
    return bars

