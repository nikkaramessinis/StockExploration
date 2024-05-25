import requests, json
from config import *

ENDPOINT_URL = "https://paper-api.alpaca.markets/v2"
ACCOUNT_URL = "{}/account".format(ENDPOINT_URL)
HEADERS = {"APCA-API-KEY-ID": API_KEY, "APCA-API-SECRET-KEY": SECRET_KEY}
STOCKS_URL = "{}/stocks".format(ENDPOINT_URL)

def get_account():
  request = requests.get(ACCOUNT_URL, headers=HEADERS)
  return json.loads(request.content)

def get_trade_data(symbol):
  request = requests.get("{}/{}/trades".format(STOCKS_URL, symbol), headers=HEADERS)
  print(request)
  return json.loads(request.content)

print(get_trade_data("AAPL"))