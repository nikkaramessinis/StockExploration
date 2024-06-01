import numpy as np
from helpers import retrieve_sp500_tickers
import pandas_ta
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
from backtesting_sma import SmaCross
from backtesting import Backtest
from helpers import fetch_latest_data, fill_with_ta, check_crossover



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
    symbols_list = ["ARM"]
    df = fetch_latest_data(symbols_list)
    df = fill_with_ta(df)
    #plot_sma(df)
    #plot_ema(df)

    sma_momentum(df)
    check_crossover(df)
    bt = Backtest(df, SmaCross, cash=1000, commission=.002,
              exclusive_orders=True)
    stats = bt.run()

    df_stats = pd.DataFrame(stats)

    # Save the DataFrame to a CSV file
    df_stats.to_csv('csvs/backtest_results.csv', index=False)
    print(stats)
    bt.plot()