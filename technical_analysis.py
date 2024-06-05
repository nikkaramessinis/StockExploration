import mplfinance as mpf
import pandas as pd
from backtesting import Backtest

from backtesting_sma import SmaCross
from helpers import check_crossover, fetch_latest_data, fill_with_ta


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


def analyze(symbols_list, strategy, hide_graphs=False):
    print(f"Running technical analysis on {symbols_list} using {strategy} strategy")
    df = fetch_latest_data(symbols_list)
    df = fill_with_ta(df)
    if not hide_graphs:
        plot_with_line(df, "sma_20")
        plot_with_line(df, "ema_20")

    sma_momentum(df)
    check_crossover(df)
    bt = Backtest(df, SmaCross, cash=1000, commission=0.002, exclusive_orders=True)
    stats = bt.run()
    print(f"type(stats {type(stats)}")

    df_stats = pd.DataFrame(stats)

    # Save the DataFrame to a CSV file
    df_stats.to_csv("csvs/backtest_results.csv", index=False)
    print(stats)
    if not hide_graphs:
        bt.plot()


if __name__ == "__main__":
    # Example usage for when this file is run directly
    symbols_list = ["ARM", "CDNS", "EVCM", "MSFT", "NKE", "NKLA", "NVDA"]
    symbols_list = ["ARM"]
    strategy = "default_strategy"
    analyze(symbols_list, strategy)
