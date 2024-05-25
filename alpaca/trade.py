import json

import requests
from config import *

ENDPOINT_URL = "https://paper-api.alpaca.markets/v2"
ACCOUNT_URL = "{}/account".format(ENDPOINT_URL)
HEADERS = {"APCA-API-KEY-ID": API_KEY, "APCA-API-SECRET-KEY": SECRET_KEY}
STOCKS_URL = "{}/stocks".format(ENDPOINT_URL)
ORDERS_URL = "{}/orders".format(ENDPOINT_URL)


def get_account():
    request = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(request.content)


def get_trade_data(symbol):
    request = requests.get("{}/{}/trades".format(STOCKS_URL, symbol), headers=HEADERS)
    return json.loads(request.content)


def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force,
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    return json.loads(r.content)


def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)
    return json.loads(r.content)


response = create_order("AAPL", 1, "buy", "market", "gtc")
response = create_order("MSFT", 1, "buy", "market", "gtc")

orders = get_orders()

print(orders)
