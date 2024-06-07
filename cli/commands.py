import json
import os

import pandas as pd

from core.data_fetching import fetch_stock_data
from core.email_alert import schedule_email_alert
from core.prediction_strategy import run_prediction


def fetch_stocks(args):
    stocks = args.stocks
    if not stocks:
        print("At least one stock symbol is required.")
        return

    # Ensure the 'csvs' directory exists
    if not os.path.exists("csvs"):
        os.makedirs("csvs")

    for stock in stocks:
        data = fetch_stock_data(stock)
        df = pd.DataFrame(data)
        csv_filename = f"csvs/{stock}.csv"
        df.to_csv(csv_filename)
        print(f"Fetched data for {stock} and saved to {csv_filename}")


def run_strategy(args):
    strategy_name = args.strategy
    stocks_list = args.stocks_list
    hide_graphs = args.hide_graphs

    if not strategy_name:
        print("Strategy name is required.")
        return

    print(f"Running strategy: {strategy_name}")
    run_prediction(strategy_name, stocks_list, hide_graphs)


def schedule_email(args):
    try:
        email_config = json.loads(args.email) if args.email else {}
        result = schedule_email_alert(email_config)
        print(f"Email scheduled: {result}")
    except json.JSONDecodeError:
        print("Invalid JSON format for email configuration.")
