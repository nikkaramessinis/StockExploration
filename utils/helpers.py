from datetime import date
from enum import Enum

import bs4 as bs
import numpy as np
import pandas as pd
import requests  # The requests library for HTTP requests in Python
import talib as ta
import yfinance as yf


class Momentum(Enum):
    UPWARD = "upward"
    DOWNWARD = "downward"
    NO_MOMENTUM = "No clear momentum"


def lagit(df: pd.DataFrame, lags: int) -> list:
    lag_columns = []
    for i in range(1, lags + 1):
        lag_column_name = f"Lag_{i}"
        df[lag_column_name] = df["ret"].shift(i)
        lag_columns.append(lag_column_name)
    return lag_columns


def fill_with_ta(df, shift_periods=1):
    def shift_by_periods(series):
        return series.shift(shift_periods)

    df["engulfing"] = shift_by_periods(
        ta.CDLENGULFING(df["Open"], df["High"], df["Low"], df["Close"])
    )
    df["rsi"] = shift_by_periods(ta.RSI(df["Close"], timeperiod=14))
    df["sma_15"] = shift_by_periods(ta.SMA(df["Close"], 15))
    df["sma_20"] = shift_by_periods(ta.SMA(df["Close"], 15))

    df["ema_20"] = shift_by_periods(ta.EMA(df["Close"], 20))

    # df["AOI"] = momentum.AwesomeOscillatorIndicator(df["High"], df["Low"])
    # Create Simple moving average 30 days
    df["SMA 30"] = shift_by_periods(df["Close"].shift(1).rolling(30).mean())
    # Create Simple moving average 60 days
    df["SMA 60"] = shift_by_periods(df["Close"].shift(1).rolling(60).mean())
    macd, macd_signal, macd_hist = ta.MACD(
        df["Close"], fastperiod=12, slowperiod=26, signalperiod=9
    )
    stochastic_k, stochastic_d = ta.STOCH(
        df["High"],
        df["Low"],
        df["Close"],
        fastk_period=14,
        slowk_period=3,
        slowk_matype=0,
        slowd_period=3,
        slowd_matype=0,
    )
    df["Stochastic_K"], df["Stochastic_D"] = shift_by_periods(
        stochastic_k
    ), shift_by_periods(stochastic_d)
    df["MACD"] = shift_by_periods(macd)
    df["MACD_Signal"] = shift_by_periods(macd_signal)
    df["MACD_Hist"] = shift_by_periods(macd_hist)
    df["ATR"] = shift_by_periods(
        ta.ATR(df["High"], df["Low"], df["Close"], timeperiod=14)
    )
    df["OBV"] = shift_by_periods(ta.OBV(df["Close"], df["Volume"]))
    df["MFI"] = shift_by_periods(
        ta.MFI(df["High"], df["Low"], df["Close"], df["Volume"], timeperiod=14)
    )
    df["ADX"] = shift_by_periods(
        ta.ADX(df["High"], df["Low"], df["Close"], timeperiod=14)
    )
    upper, middle, lower = ta.BBANDS(
        df["Close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
    )
    df["BB_Upper"] = shift_by_periods(upper)
    df["BB_Middle"] = shift_by_periods(middle)
    df["BB_Lower"] = shift_by_periods(lower)
    # Create an empty columns to put the signals
    df["signal"] = np.nan

    # Create the condition
    condition_buy = (df["SMA 30"] > df["SMA 60"]) & (
        df["SMA 30"].shift(1) < df["SMA 60"].shift(1)
    )
    condition_sell = (df["SMA 30"] < df["SMA 60"]) & (
        df["SMA 30"].shift(1) > df["SMA 60"].shift(1)
    )

    df.loc[condition_buy, "signal"] = 1
    df.loc[condition_sell, "signal"] = -1

    df["ret"] = df["Close"].pct_change()
    lagit(df, 4)
    df["direction"] = np.where(df.ret > 0, 1, 0)
    return df


def check_crossover(df):
    # Extract the closing price and SMA at the last moment
    last_row = df.iloc[-1]
    closing_price_last = last_row["Close"]
    ema_last = last_row["ema_20"]
    # Compare the values
    if closing_price_last > ema_last:
        return Momentum.UPWARD
    else:
        return Momentum.UPWARD


def fetch_latest_data(ticker, end_date, is_live=False, start_date="2021-09-27"):
    #
    # end_date = "2024-06-30"
    # end_date = date.today()
    end_date = "2024-07-19"
    end_date = date.today()
    if is_live:
        end_date = date.today()
    # df = yf.download(tickers=symbols_list, start=start_date, end=str(end_date), auto_adjust=True)
    ticker_yahoo = yf.Ticker(ticker)
    df = ticker_yahoo.history(start=start_date, end=str(end_date), auto_adjust=True)
    return df


def retrieve_sp500_tickers() -> list[str]:
    # Visit the Wikipedia page
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.content, "html.parser")

    # Find the table containing S&P 500 stocks data
    table = soup.find("table", {"class": "wikitable sortable"})

    # Extract tickers from the table
    tickers = []
    for row in table.find_all("tr")[1:]:
        ticker = row.find_all("td")[0].text.strip()
        tickers.append(ticker)

    # Remove newline characters
    sp500_symbols = [s.replace("\n", "") for s in tickers]
    return sp500_symbols
