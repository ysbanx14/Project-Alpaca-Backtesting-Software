import os
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed  # 1. Added this import

def fetch_data(ticker="SPY", years=5):
    """
    Fetches daily OHLCV data for a given ticker.
    Attempts to use Alpaca API first; falls back to yfinance.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * years)
    
    alpaca_api_key = os.getenv("ALPACA_API_KEY")
    alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
    
    if alpaca_api_key and alpaca_secret_key:
        print(f"Fetching data for {ticker} using Alpaca API...")
        try:
            client = StockHistoricalDataClient(alpaca_api_key, alpaca_secret_key)
            request_params = StockBarsRequest(
                symbol_or_symbols=ticker,
                timeframe=TimeFrame.Day,
                start=start_date,
                end=end_date,
                feed=DataFeed.IEX  # 2. Added the IEX feed parameter
            )
            bars = client.get_stock_bars(request_params)
            df = bars.df
            # Alpaca multi-index has (symbol, timestamp). Let's drop symbol and keep timestamp.
            df = df.reset_index(level=0, drop=True)
            df.index = pd.to_datetime(df.index).tz_convert(None)
            return df
        except Exception as e:
            print(f"Alpaca API failed: {e}. Falling back to yfinance.")
            return _fetch_yfinance(ticker, start_date, end_date)
    else:
        print(f"Alpaca API keys not found. Fetching data for {ticker} using yfinance...")
        return _fetch_yfinance(ticker, start_date, end_date)

def _fetch_yfinance(ticker, start_date, end_date):
    ticker_obj = yf.Ticker(ticker)
    df = ticker_obj.history(start=start_date, end=end_date)
    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    })
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    return df
