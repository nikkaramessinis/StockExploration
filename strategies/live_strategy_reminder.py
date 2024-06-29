import yagmail
from config.secrets import GMAIL_PASSWORD, GMAIL_ADDRESS
from sys import platform
from utils.helpers import fetch_latest_data, fill_with_ta, check_crossover, Momentum, save_to_json
from backtesting import Backtest
from strategies.backtesting_rsi import RSIOscillatorCross
import time

def send_alert(body=""):
    if platform == "win32":
        import winsound
        winsound.Beep(1000, 500)
    
    if GMAIL_ADDRESS == "" or GMAIL_PASSWORD == "":
        return
    
    yag = yagmail.SMTP(GMAIL_ADDRESS, GMAIL_PASSWORD)
    subject = 'Trading Alert'
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
    
    while True:
        for stock in stocks_list:
            df = fetch_latest_data(stock)
            strategy_class = strategies[strategy_name]()
            signal = strategy_class.generate_signal(df)
            
            print(f"Checking signal for {stock}... Signal: {signal}")
            if signal and signal != previous[stock]:
                body = f"Momentum has shifted! We now have a {signal} signal for {stock}"
                print(body)
                send_alert(body)
                previous[stock] = signal

                # Store data into JSON file
                data_to_store = {
                    "stock": stock,
                    "signal": signal,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                filename = f"{stock}_momentum.json"
                save_to_json(data_to_store, filename)

        time.sleep(60)  # Sleep for 1 minute