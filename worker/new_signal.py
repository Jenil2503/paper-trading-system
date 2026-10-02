import pandas as pd
import numpy as np


def compute_atr(df : pd.DataFrame, period : int = 20):
    high = df['High']
    low = df['Low']
    close = df['Close']
    # df = df.copy()
    prev_close = close.shift(1)
    
    first = high-low
    second = (high-prev_close).abs()
    third = (low-prev_close).abs()
    

    tr = pd.concat([first,second,third],axis = 1).max(axis = 1)
    
    atr = tr.ewm(alpha = 1/period, adjust = False).mean()
    
    return atr

def compute_ema(df : pd.DataFrame, fast_period = 21, slow_period = 9):
    
    fast_ema = df["Close"].ewm(span=fast_period,adjust=False).mean()
    slow_ema = df["Close"].ewm(span=slow_period,adjust=False).mean()
    
    return pd.DataFrame({"ema_fast" : fast_ema, "ema_slow" : slow_ema})


def compute_vwap(df : pd.DataFrame):

    typical_price = (df["High"] + df["Close"] + df["Low"]) / 3
    price_vol = typical_price * df["Volume"]
    
    cum_pv = price_vol.groupby(df.index.date).cumsum()
    cum_vol = df["Volume"].groupby(df.index.date).cumsum()
    
    vwap = cum_pv / cum_vol
    
    return vwap

def compute_volume_sma(df : pd.DataFrame, period : int = 20):
    volume_sma = df["Volume"].rolling(period).mean()
    
    return volume_sma


def generate_signals(df : pd.DataFrame):
    
    df = df.copy()
    
    ema = compute_ema(df)
    df["fast_ema"] = ema["fast_ema"]
    df["slow_ema"] = ema["slow_ema"]
    
    df["vwap"] = compute_vwap(df)
    
    df["volume_sma"] = compute_volume_sma(df)
    
    df["atr"] = compute_atr(df)
    
    # Entry Conditons
    
    trend_bullish = (df["ema_fast"] > df["ema_slow"])
    price_above_vwap = (df["Close"] > df["vwap"])
    breakout = (df["Close"] > df["High"].shift(1))
    vol_confirmation = (df["Volume"] > 1.5*df["volume_sma"])
    
    entry = (trend_bullish & price_above_vwap & breakout & vol_confirmation)
    
    df["entry_signal"] = entry.astype(int)
    
    # Exit Conditons
    
    trend_bearish = (df["ema_fast"] < df["ema_slow"])
    price_below_vwap = (df["Close"] < df["vwap"])
    
    entry = (trend_bearish | price_below_vwap)
    
    df["exit_signal"] = entry.astype(int)
    
    df["unit_size"] = 0.01 / df["atr"]
    
    return df
