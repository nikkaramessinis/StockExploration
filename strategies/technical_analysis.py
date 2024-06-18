import mplfinance as mpf
import pandas as pd
from backtesting import Backtest
import mplfinance as mpf

from strategies.backtesting_sma import SmaCross
from strategies.backtesting_ema import EmaCross
from utils.helpers import check_crossover, fetch_latest_data, fill_with_ta
from config.feqos import merge_reference_with_test

def plot_with_line(df, column):
    # You can add a plot with another line usually a moving average.
    ap_ema = mpf.make_addplot(df[column], color="orange", width=1)
    mpf.plot(
        df,
        type="candle",
        style="charles",
        title="Candlestick Chart with {column} Line",
        ylabel="Price",
        ylabel_lower="Shares Traded",
        addplot=ap_ema,
    )


def sma_momentum(df):
    # Extract the closing price and SMA at the last moment
    last_row = df.iloc[-1]
    closing_price_last = last_row["Close"]
    sma_last = last_row["sma_20"]
    # Compare the values
    if closing_price_last > sma_last:
        print("Upward momentum")
    else:
        print("Downward momentum")


def ema_momentum(df):
    # Extract the closing price and SMA at the last moment
    last_row = df.iloc[-1]
    closing_price_last = last_row["Close"]
    ema_last = last_row["ema_20"]
    # Compare the values
    if closing_price_last > ema_last:
        print("Upward momentum")
    else:
        print("Downward momentum")


def analyze(symbols_list, show_graphs, show_feqos, save_as_reference):
    results_dataframe = pd.DataFrame()

    for symbol in symbols_list:
        print("Calling fetching data")
        df = fetch_latest_data(symbol)
        df = fill_with_ta(df)
        if show_graphs:
            plot_with_line(df, "sma_20")
            plot_with_line(df, "ema_20")

        sma_momentum(df)
        check_crossover(df)
        bt = Backtest(df, EmaCross, cash=1000, commission=0.002, exclusive_orders=True)
        stats = bt.run()
        #print(f"type(stats {type(stats)}")
        stats['Name'] = symbol
        results_dataframe = results_dataframe._append(stats, ignore_index=True)
        # print(stats)
        if show_graphs:
            bt.plot()

    # results_dataframe = pd.concat(list_of_dfs, ignore_index=True)
    results_dataframe.to_csv("csvs/stats.csv", index=False)
    if show_feqos:
        merge_reference_with_test(results_dataframe)

    if save_as_reference:
        results_dataframe.to_csv("csvs/reference.csv", index=False)

    #print(results_dataframe)
