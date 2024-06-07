import json
import os

import pandas as pd

from core.data_fetching import fetch_stock_data

# from core.email_alert import schedule_email_alert
from core.prediction_strategy import run_prediction


def fetch_stocks(args):
    symbols = args.symbols
    if not symbols:
        print("At least one stock symbol is required.")
        return

    # Ensure the 'csvs' directory exists
    if not os.path.exists("csvs"):
        os.makedirs("csvs")

    for symbol in symbols:
        data = fetch_stock_data(symbol)
        df = pd.DataFrame(data)
        csv_filename = f"csvs/{symbol}.csv"
        df.to_csv(csv_filename)
        print(f"Fetched data for {symbol} and saved to {csv_filename}")


def run_strategy(args):
    strategy_name = args.strategy
    try:
        params = json.loads(args.params) if args.params else {}
    except json.JSONDecodeError:
        print("Invalid JSON format for parameters.")
        return

    if not strategy_name:
        print("Strategy name is required.")
        return

    result = run_prediction(strategy_name, params)
    print(f"Strategy {strategy_name} result: {result}")


# def schedule_email(args):
#     try:
#         email_config = json.loads(args.email) if args.email else {}
#     except json.JSONDecodeError:
#         print("Invalid JSON format for email configuration.")
#         return

#     if not email_config:
#         print("Email configuration is required.")
#         return

#     schedule_email_alert(email_config)
#     print("Email alert scheduled.")
