import time
from sys import platform

import yagmail
from backtesting import Backtest

from config.secrets import GMAIL_ADDRESS, GMAIL_PASSWORD
from strategies.backtesting_rsi import RSIOscillatorCross
from utils.helpers import fetch_latest_data, fill_with_ta


def send_alert(body=""):
    if platform == "win32":
        import winsound

        winsound.Beep(1000, 500)

    if GMAIL_ADDRESS == "" or GMAIL_PASSWORD == "":
        return

    yag = yagmail.SMTP(GMAIL_ADDRESS, GMAIL_PASSWORD)
    subject = "Trading Alert"
    yag.send(GMAIL_ADDRESS, subject, body)


def live_strategy(strategy_name, stocks_list):
    strategies = {
        "RSI": RSIOscillatorCross,
        # Add other strategies here
    }

    if strategy_name not in strategies:
        print(f"Strategy {strategy_name} not found.")
        return

    previous = {stock: None for stock in stocks_list}
    strategy_class = strategies[strategy_name]

    while True:
        for stock in stocks_list:
            df = fetch_latest_data(stock)
            df = fill_with_ta(df)  # Make sure to add technical indicators

            # Use the class method to generate the signal
            # We're passing the last two rows to allow for crossover calculation
            signal = strategy_class.generate_signal(df.iloc[-2:])

            print(f"Checking signal for {stock}... Signal: {signal}")
            if signal and signal != previous[stock]:
                body = f"New signal for {stock}: {signal}"
                print(body)
                send_alert(body)
                previous[stock] = signal

        time.sleep(60)  # Sleep for 1 minute
