import json
import os

import pandas as pd

from core.data_fetching import fetch_stock_data
from core.email_alert import schedule_email_alert
from core.prediction_strategy import run_prediction
from strategies.live_strategy_reminder import live_strategy

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
    flow_name = args.flow_name
    strategy_name = args.strategy
    stocks_list = args.stocks_list
    display_dashboard = args.display_dashboard
    save_reference = args.save_reference
    enable_optimizing = args.enable_optimizing

    if not strategy_name:
        print("Strategy name is required.")
        return

    print(f"Running strategy: {strategy_name} with flow {flow_name}")

    if flow_name == "optimization":
        run_prediction(
            strategy_name, stocks_list, display_dashboard, save_reference, enable_optimizing
        )
    elif flow_name == "live":
        live_strategy(strategy_name, stocks_list)
    else:
        print(f"Unknown strategy: {flow_name}")
        return


def email_alerts(args):
    try:
        email_config = json.loads(args.email) if args.email else {}
        schedule_email_alert(email_config)
    except json.JSONDecodeError:
        print("Invalid JSON format for email configuration.")