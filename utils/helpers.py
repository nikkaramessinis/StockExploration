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


def fill_with_ta(df, write_to_csv=False):
    df["engulfing"] = ta.CDLENGULFING(
        df["Open"], df["High"], df["Low"], df["Close"]
    ).shift(1)
    df["rsi"] = ta.RSI(df["Close"], timeperiod=14).shift(1)
    df["sma_15"] = ta.SMA(df["Close"], 15).shift(1)
    df["sma_20"] = ta.SMA(df["Close"], 15).shift(1)

    df["ema_20"] = ta.EMA(df["Close"], 20).shift(1)
    # Create Simple moving average 30 days
    df["SMA 30"] = df["Close"].shift(1).rolling(30).mean().shift(1)
    # Create Simple moving average 60 days
    df["SMA 60"] = df["Close"].shift(1).rolling(60).mean().shift(1)

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
    # We say signal when we open or close a trade and poistion to talk about the whole time we are into a trade
    # df["position"] = df["signal"].fillna(method="ffill")

    # We define a fix cost we need to pay each time we interact with the market
    # cost_ind = 0.0001

    # We create a vector of cost
    # df["cost"] = (np.abs(df["signal"]) * cost_ind).fillna(
    #    value=0
    # )  # (-0.0001, 0, 0, 0, 0, 0 , 0, -0.0001, 0, 0) (-0.0001,-0.0001,-0.0001,-0.0001,-0.0001,)

    # Compute the percentage of variation of the asset
    # df["pct"] = df["Close"].pct_change(1)

    # Compute the return of the strategy
    # df["return"] = (df["pct"] * df["position"].shift(1) - df["cost"]) * 100
    df["ret"] = df["Close"].pct_change()
    lagit(df, 2)
    df["direction"] = np.where(df.ret > 0, 1, 0)
    if write_to_csv:
        df.to_csv("csvs/arm.csv", index=False)
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


def fetch_latest_data(
    ticker,
    is_live=False,
    start_date="2021-09-27",
):
    #
    # end_date = "2024-06-30"
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
