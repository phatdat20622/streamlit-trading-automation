# Trading Data Automation — Streamlit Demo

Small demo project for fetching, cleaning, analyzing, and exporting market data using Yahoo Finance (via `yfinance`) and Streamlit.

## Features
- Fetch historical market data for a given ticker (e.g., AAPL, BTC-USD, ^VNINDEX).
- Clean and preprocess data (compute returns, rolling mean, rolling volatility).
- Display interactive charts and summary statistics.
- Export cleaned and raw CSV files.

## Prerequisites
- Python 3.9+
- `pip` available

## Installation
```bash
git clone <your-repo-url>
cd trading_data_dashboard
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
