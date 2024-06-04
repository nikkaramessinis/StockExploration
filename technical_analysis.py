import pandas as pd
from backtesting_sma import SmaCross
from backtesting import Backtest
from helpers import fetch_latest_data, fill_with_ta, check_crossover
import mplfinance as mpf




def plot_with_line(df, column):
    # You can add a plot with another line usually a moving average.
    ap_ema = mpf.make_addplot(df[column], color='orange', width=1)
    mpf.plot(df, type='candle', style='charles',
             title='Candlestick Chart with {column} Line',
             ylabel='Price', ylabel_lower='Shares Traded',
             addplot=ap_ema)


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
    symbols_list = ["ARM", "CDNS", "EVCM",  "MSFT", "NKE", "NKLA", "NVDA"]
    list_of_dfs = []
    results_dataframe = pd.DataFrame()

    for symbol in symbols_list:
        df = fetch_latest_data(symbol)
        df = fill_with_ta(df)
        #plot_with_line(df, 'sma_20')
        #plot_with_line(df, 'ema_20')

        sma_momentum(df)
        check_crossover(df)
        bt = Backtest(df, SmaCross, cash=1000, commission=.002,
                  exclusive_orders=True)
        stats = bt.run()
        print(f"type(stats {type(stats)}")
        results_dataframe = results_dataframe._append(stats, ignore_index=True)
        print(stats)
        #bt.plot()

    #results_dataframe = pd.concat(list_of_dfs, ignore_index=True)
    results_dataframe.to_csv('csvs/stats.csv', index=False)

    print(results_dataframe)

    # Save the DataFrame to a CSV file
