import pandas as pd
from backtesting import Backtest

from config.feqos import merge_reference_with_test
from strategies.backtesting_ema import EmaCross
from utils.helpers import check_crossover, fetch_latest_data, fill_with_ta


def analyze(
    strategy, symbols_list, display_dashboard, save_as_reference, enable_optimizing
):
    results_dataframe = pd.DataFrame()
    symbol_data = {}

    for symbol in symbols_list:
        print(f"Fetching data for {symbol}")
        df = fetch_latest_data(symbol)
        df = fill_with_ta(df)

        check_crossover(df)
        bt = Backtest(df, strategy, cash=1000, commission=0.002, exclusive_orders=True)
        if enable_optimizing:
            stats = bt.optimize(
                upper_bound=range(50, 85, 5),
                lower_bound=range(10, 45, 5),
                rsi_window=range(10, 30, 2),
                maximize="Equity Final [$]",
            )
        else:
            stats = bt.run()
        # print(f"type(stats {type(stats)}")
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
