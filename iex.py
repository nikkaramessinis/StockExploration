import numpy as np #The Numpy numerical computing library
import pandas as pd #The Pandas data science library
import requests #The requests library for HTTP requests in Python
import xlsxwriter #The XlsxWriter libarary for
import math #The Python math module
from scipy import stats #The SciPy stats module
import bs4 as bs
from secrets import  IEX_CLOUD_API_TOKEN

def retrieve_sp500_tickers() -> list[str]:
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
    return sp500_symbols

rv_columns = [
    'Ticker',
    'Price',
    'Number of Shares to Buy',
    'Price-to-Earnings Ratio',
    'PE Percentile',
    'Price-to-Book Ratio',
    'PB Percentile',
    'Price-to-Sales Ratio',
    'PS Percentile',
    'EV/EBITDA',
    'EV/EBITDA Percentile',
    'EV/GP',
    'EV/GP Percentile',
    'RV Score'
]



def get_initial_dataframe(sp500_symbols):
    rv_dataframe = pd.DataFrame()
    new_rows = []
    for symbol_string in sp500_symbols:
        batch_api_call_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote,advanced-stats&token={IEX_CLOUD_API_TOKEN}'
        print(batch_api_call_url)
        data = requests.get(batch_api_call_url).json()
        for symbol in symbol_string.split(','):
            enterprise_value = data[symbol]['advanced-stats']['enterpriseValue']
            ebitda = data[symbol]['advanced-stats']['EBITDA']
            gross_profit = data[symbol]['advanced-stats']['grossProfit']

            try:
                ev_to_ebitda = enterprise_value / ebitda
            except TypeError:
                ev_to_ebitda = np.NaN

            try:
                ev_to_gross_profit = enterprise_value / gross_profit
            except TypeError:
                ev_to_gross_profit = np.NaN

            new_row = [
                    symbol,
                    data[symbol]['quote']['latestPrice'],
                    'N/A',
                    data[symbol]['quote']['peRatio'],
                    'N/A',
                    data[symbol]['advanced-stats']['priceToBook'],
                    'N/A',
                    data[symbol]['advanced-stats']['priceToSales'],
                    'N/A',
                    ev_to_ebitda,
                    'N/A',
                    ev_to_gross_profit,
                    'N/A',
                    'N/A'
                ]
            new_rows.append(new_row)

    # Convert the list of lists to a DataFrame
    new_rows_df = pd.DataFrame(new_rows, columns=rv_columns)

    # Concatenate the new rows to the existing DataFrame
    rv_dataframe = pd.concat([rv_dataframe, new_rows_df], ignore_index=True)

    # Save the result to a CSV file
    rv_dataframe.to_csv("rv_dataframe.csv", index=False)
    return rv_dataframe


if __name__ == "__main__":
    sp500_symbols = retrieve_sp500_tickers()
    rv_dataframe = get_initial_dataframe(sp500_symbols)