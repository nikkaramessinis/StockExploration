import pandas as pd
from backtesting import Backtest

from config.feqos import merge_reference_with_test
from strategies.backtesting_ema import EmaCross
from utils.helpers import check_crossover, fetch_latest_data, fill_with_ta


def analyze(symbols_list, display_dashboard, save_as_reference):
    results_dataframe = pd.DataFrame()
    symbol_data = {}

    for symbol in symbols_list:
        print(f"Fetching data for {symbol}")
        df = fetch_latest_data(symbol)
        df = fill_with_ta(df)

        check_crossover(df)
        bt = Backtest(df, EmaCross, cash=1000, commission=0.002, exclusive_orders=True)
        stats = bt.run()
        stats["Name"] = symbol
        results_dataframe = results_dataframe._append(stats, ignore_index=True)

        # Store the DataFrame for each symbol
        symbol_data[symbol] = df

    results_dataframe.to_csv("csvs/stats.csv", index=False)

    if display_dashboard:
        merge_reference_with_test(results_dataframe, symbol_data)

    if save_as_reference:
        results_dataframe.to_csv("csvs/reference.csv", index=False)

    return results_dataframe, symbol_data
