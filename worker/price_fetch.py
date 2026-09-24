import yfinance as yf
import pandas as pd

def fetch_ohlc(ticker : str, period = '15d', interval : str = '5m'):
    df = yf.download(ticker, period = period, interval = interval, progress = False)
    
    if df.empty:
        raise ValueError(f"No price data returned for the {ticker}")
    
    return df

