import pandas as pd
from backtesting import Backtest

from config.feqos import merge_reference_with_test
from utils.helpers import check_crossover, fetch_latest_data, fill_with_ta


def analyze(strategy, symbols_list, display_dashboard, save_as_reference, param_ranges):

    results_dataframe = pd.DataFrame()
    symbol_data = {}

    for symbol in symbols_list:
        print(f"Fetching data for {symbol}")
        df = fetch_latest_data(symbol)
        df = fill_with_ta(df)

        check_crossover(df)
        bt = Backtest(df, strategy, cash=1000, commission=0.002, exclusive_orders=True)

        if param_ranges:
            stats = bt.optimize(
                **param_ranges,
                maximize="Equity Final [$]",
                constraint=lambda param: param.upper_bound > param.lower_bound,
            )
        else:
            stats = bt.run()

        bt.plot(filename=f"csvs/{symbol}")
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
