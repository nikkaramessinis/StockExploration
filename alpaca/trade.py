import requests, json
from config import *

ENDPOINT_URL = "https://paper-api.alpaca.markets/v2"
ACCOUNT_URL = "{}/account".format(ENDPOINT_URL)
HEADERS = {"APCA-API-KEY-ID": API_KEY, "APCA-API-SECRET-KEY": SECRET_KEY}


def get_account():
  request = requests.get(ACCOUNT_URL, headers=HEADERS)
  return json.loads(request.content)

account = get_account()

print(account)