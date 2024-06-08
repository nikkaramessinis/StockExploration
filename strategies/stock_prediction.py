import requests
import csv
#import pandas as pd
#import yfinance as yf

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)


# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
CSV_URL = 'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey=demo'

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        print(row)




# Define the weights for each metric (customize as needed)
weight_pe = 0.4
weight_pb = 0.3
weight_fcf = 0.3

# Example stock symbol (you can replace with any stock you're interested in)
stock_symbol = 'AAPL'

# Get fundamental data using yfinance
stock_info = yf.Ticker(stock_symbol).info

# Extract relevant metrics
pe_ratio = stock_info.get('trailingPE', None)
pb_ratio = stock_info.get('priceToBook', None)
free_cash_flow = stock_info.get('freeCashflow', None)

# Normalize the metrics (scale to a common range)
normalized_pe = pe_ratio / max(pe_ratio, pb_ratio, free_cash_flow)
normalized_pb = pb_ratio / max(pe_ratio, pb_ratio, free_cash_flow)
normalized_fcf = free_cash_flow / max(pe_ratio, pb_ratio, free_cash_flow)

# Calculate the composite score
composite_score = (weight_pe * normalized_pe) + (weight_pb * normalized_pb) + (weight_fcf * normalized_fcf)
print(f"composite_score {composite_score}")

print(f"Composite Score for {stock_symbol}: {composite_score:.2f}")