import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import platform

import yagmail
from backtesting import Backtest

from cli.livestrategyexecutor import LiveStrategyExecutor
from config.secrets import GMAIL_ADDRESS, GMAIL_PASSWORD
from strategies.backtesting_rsi import RSIOscillatorCross
from utils.helpers import fetch_latest_data, fill_with_ta


def send_mail(body=""):
    # Email configuration
    password = GMAIL_PASSWORD
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email content
    subject = "Test Email with Attachment"

    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = GMAIL_ADDRESS
    message["To"] = GMAIL_ADDRESS
    message["Subject"] = subject

    # Attach the body to the message
    message.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        # Connect to the server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(GMAIL_ADDRESS, password)  # Log in to the server

        # Send the email
        server.sendmail(GMAIL_ADDRESS, GMAIL_ADDRESS, message.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()  # Close the connection


def send_alert(body=""):
    if platform == "win32":
        import winsound

        winsound.Beep(1000, 500)

    if GMAIL_ADDRESS == "" or GMAIL_PASSWORD == "":
        return
    try:
        print(GMAIL_ADDRESS)
        print(GMAIL_PASSWORD)
        yag = yagmail.SMTP(GMAIL_ADDRESS, GMAIL_PASSWORD)

        #    host="smtp.gmail.com",
        #    port=587,
        #    smtp_starttls=True,  # Enable TLS/STARTTLS
        #    smtp_ssl=False,
        # )
        subject = "Trading Alert"
        yag.send("nikaramessinis@gmail.com", subject, body)
    except Exception as e:
        print(f"Error: {e}")


def live_strategy(strategy, stocks_list):

    previous = {stock: None for stock in stocks_list}

    while True:
        for stock in stocks_list:
            df = fetch_latest_data(stock, True)
            df = fill_with_ta(df)  # Make sure to add technical indicators

            # Use the class method to generate the signal
            # We're passing the last two rows to allow for crossover calculation
            lse = LiveStrategyExecutor(
                df, strategy, cash=1000, commission=0.002, exclusive_orders=True
            )
            signal = lse.live_strategy()

            print(f"Checking signal for {stock}... Signal: {signal}")

            if signal and signal != previous[stock]:
                body = f"New signal for {stock}: {signal}"
                print(body)
                send_mail("body")
                time.sleep(60)  # Sleep for 1 minute

                previous[stock] = signal

        time.sleep(60)  # Sleep for 1 minute
