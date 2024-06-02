import requests
import pandas as pd
import bs4 as bs
import requests
import yfinance as yf
import datetime

# Visit the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
response = requests.get(url)
soup = bs.BeautifulSoup(response.content, "html.parser")

# Find the table containing S&P 500 stocks data
table = soup.find("table", {"class": "wikitable sortable"})

# Extract tickers from the table
tickers = []
for row in table.find_all("tr")[1:]:
    ticker = row.find_all("td")[0].text.strip()
    tickers.append(ticker)

# Remove newline characters
sp500_symbols = [s.replace("\n", "") for s in tickers]

print(tickers)  # Display the list of tickers



# Replace with your own Alpha Vantage API key
API_KEY = "YAI0JP3LDYL1MYND"


# Initialize an empty DataFrame to store the data
sp500_data = pd.DataFrame()
weight_pe = 0.4
weight_pb = 0.3
weight_fcf = 0.3

# for stock_symbol in sp500_symbols:
#
#     stock_info = yf.Ticker(stock_symbol).info
#     # Extract relevant metrics
#     pe_ratio = stock_info.get('trailingPE', None)
#     pb_ratio = stock_info.get('priceToBook', None)
#     free_cash_flow = stock_info.get('freeCashflow', None)
#
#     # Normalize the metrics (scale to a common range)
#     normalized_pe = pe_ratio / max(pe_ratio, pb_ratio, free_cash_flow)
#     normalized_pb = pb_ratio / max(pe_ratio, pb_ratio, free_cash_flow)
#     normalized_fcf = free_cash_flow / max(pe_ratio, pb_ratio, free_cash_flow)
#
#     # Calculate the composite score
#     composite_score = (weight_pe * normalized_pe) + (weight_pb * normalized_pb) + (weight_fcf * normalized_fcf)
#     print(f"composite_score {composite_score}")
#
#     print(f"Composite Score for {stock_symbol}: {composite_score:.2f}")


iexcloud = "sk_62b7e81c291b45129155244cf92601bd"
sp500_symbols = ["MMM"]
sp500_data_list = []

# Loop through each stock symbol
for symbol in sp500_symbols:
    try:
        # Make API request for PE ratio, PB ratio, and free cash flow
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        print(data)
        # Extract relevant metrics
        pe_ratio = data.get("PERatio")
        pb_ratio = data.get("PriceToBookRatio")
        print(pe_ratio)
        print(pb_ratio)
        url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={API_KEY}'
        r = requests.get(url)
        data = r.json()
        free_cash_flow = data.get("FreeCashFlow")
        print(pb_ratio)
        print(data)

        # Append data to DataFrame
        sp500_data_list.append({
            "Symbol": symbol,
            "PE Ratio": pe_ratio,
            "PB Ratio": pb_ratio,
            "Free Cash Flow": free_cash_flow
        })
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

sp500_data = pd.DataFrame(sp500_data_list)
# Save data to a CSV file
sp500_data.to_csv("sp500_metrics.csv", index=False)
print("Data saved to sp500_metrics.csv")
