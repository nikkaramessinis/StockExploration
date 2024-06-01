import numpy as np
import yfinance as yf
from helpers import retrieve_sp500_tickers
from datetime import date
import pandas_ta
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
from backtesting_sma import SmaCross
from backtesting import Backtest

def fill_df(start_date='2023-09-27', write_to_csv = True):
    end_date = date.today()
    print(end_date)
    symbols_list = ["ARM"]
    df = yf.download(tickers=symbols_list, start=start_date, end=str(end_date), auto_adjust=True)
    df['engulfing'] = ta.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
    df['rsi'] = ta.RSI(df['Close'], timeperiod=14)
    df['sma_20'] = ta.SMA(df['Close'], 20)
    df['ema_20'] = ta.EMA(df['Close'], 15)
    if write_to_csv:
        df.to_csv("csvs/arm.csv", index=False)
    return df

def plot_sma(df):
    plt.plot(df['Close'])
    plt.plot(df['sma_20'])
    plt.show()


def plot_ema(df):
    plt.plot(df['Close'])
    plt.plot(df['ema_20'])
    plt.show()


def sma_momentum(df):
    # Extract the closing price and SMA at the last moment
    last_row = df.iloc[-1]
    closing_price_last = last_row['Close']
    sma_last = last_row['sma_20']
    # Compare the values
    if closing_price_last > sma_last:
        print("Upward momentum")
    else:
        print("Downward momentum")


def ema_momentum(df):
    # Extract the closing price and SMA at the last moment
    last_row = df.iloc[-1]
    closing_price_last = last_row['Close']
    ema_last = last_row['ema_20']
    # Compare the values
    if closing_price_last > ema_last:
        print("Upward momentum")
    else:
        print("Downward momentum")



if __name__=="__main__":
    #main()
    df = fill_df()
    plot_sma(df)
    plot_ema(df)

    sma_momentum(df)
    ema_momentum(df)
    bt = Backtest(df, SmaCross, cash=1000, commission=.002,
              exclusive_orders=True)
    stats = bt.run()

    df_stats = pd.DataFrame(stats)

    # Save the DataFrame to a CSV file
    df_stats.to_csv('csvs/backtest_results.csv', index=False)
    print(stats)
    bt.plot()