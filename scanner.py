
import yfinance as yf
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def get_nse_universe():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    df = pd.read_csv(url)
    return [s + ".NS" for s in df['SYMBOL'].tolist()]

def fetch_data(symbol):
    return yf.download(symbol, period="6mo", interval="1d", progress=False, threads=False)

def add_indicators(df):
    df['EMA50'] = df['Close'].ewm(span=50).mean()
    df['EMA200'] = df['Close'].ewm(span=200).mean()
    df['Vol_SMA10'] = df['Volume'].rolling(10).mean()
    df['ATR14'] = (df['High'] - df['Low']).rolling(14).mean()
    return df

def ai_score(df):
    last = df.iloc[-2]
    score = 0
    if last['Close'] > last['EMA50'] > last['EMA200']:
        score += 2
    if last['Volume'] < last['Vol_SMA10']:
        score += 2
    if last['Close'] > last['Open']:
        score += 1
    return score

def process_symbol(symbol):
    try:
        df = fetch_data(symbol)
        df = add_indicators(df)
        score = ai_score(df)
        if score >= 3:
            return {"symbol": symbol, "score": score}
    except:
        return None

def run_full_scan():
    symbols = get_nse_universe()
    results = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        data = list(executor.map(process_symbol, symbols))
    for r in data:
        if r:
            results.append(r)
    return pd.DataFrame(results).sort_values(by="score", ascending=False).head(10)
