import time
 # For Windows; use pygame for cross-platform support
from utils.helpers import fetch_latest_data, fill_with_ta, check_crossover
from utils.helpers import Momentum
import yagmail
from config.secrets import GMAIL_PASSWORD, GMAIL_ADDRESS
from sys import platform

def send_email(body=""):
    if GMAIL_ADDRESS == "" or GMAIL_PASSWORD == "":
        return

    yag = yagmail.SMTP(GMAIL_ADDRESS, GMAIL_PASSWORD)
    subject = 'Hello from Yagmail!'
    yag.send(GMAIL_ADDRESS, subject, body)


def live_strategy(strategy_name, stocks_list):
    if platform == "win32":
        import winsound

    previous = Momentum.DOWNWARD
    while True:
        for stock in stocks_list:
            df = fetch_latest_data(stock)
            sma_value = fill_with_ta(df)  # Adjust with your data
            crossover_status = check_crossover(df)

            if crossover_status != previous:
                # Trigger the beep sound (implement this part)

                body = (f"Momentum has swifted! We now have an {crossover_status} momentum for {stock}")
                print(body)
                send_email(body)
                previous = crossover_status
                if platform == "win32":
                    winsound.Beep(1000, 500)  # Example beep sound

        time.sleep(60)  # Sleep for 1 minute
