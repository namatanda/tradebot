# Trading Bot 

## Overview

This project is a simple trading bot written in Python that leverages the Alpaca API for fetching stock data, implements trading strategies, and conducts backtesting using Backtrader. The bot is designed for educational purposes and provides a basic framework that can be extended for more sophisticated trading strategies.

## Project Structure

The project is organized into the following main components:

- **data_client.py**: Handles the communication with the Alpaca API for fetching stock data.

- **data_processor.py**: Contains functions for processing and cleaning the historical stock data.

- **backtester.py**: Implements the backtesting functionality using the Backtrader library.

- **rade_strategy.py**: Defines trading strategies using the Backtrader framework.

- **tradebot.py**: The main script that orchestrates the entire trading process, from data retrieval to backtesting and execution of trades.

- **tests/**: Contains unit tests for the individual components of the project.

- **scripts/**: Placeholder for any deployment or utility scripts.

## Setup and Dependencies

### Prerequisites

- Python 3.8 or later

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/namatanda/tradebot.git
