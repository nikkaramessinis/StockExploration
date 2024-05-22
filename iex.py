import numpy as np
import pandas as pd #The Pandas data science library
import xlsxwriter #The XlsxWriter libarary for
import math #The Python math module
from scipy import stats #The SciPy stats module
from mysecrets import  IEX_CLOUD_API_TOKEN
import certifi
from helpers import retrieve_sp500_tickers


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
    'RV Score',
    'net_income',
    'equity',
    'revenue',
    'eps'
]

def get_fundamentals(symbol_string):
    url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote,advanced-stats,cash-flow,fundamentals&token={IEX_CLOUD_API_TOKEN}'
    print(url)

    response = requests.get(url, verify=certifi.where())
    data = response.json()
    return data


def get_initial_dataframe(sp500_symbols):
    rv_dataframe = pd.DataFrame()
    new_rows = []
    for symbol_string in sp500_symbols:
        data = get_fundamentals(symbol_string)
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
                    'N/A',
                    data[symbol].get('cash-flow', {}).get('cashflow', [{}])[0].get('netIncome', float('nan')),
                    data[symbol].get('fundamentals', {}).get('fundamentals', [{}])[0].get('equityShareholder', float('nan')),
                    data[symbol].get('fundamentals', {}).get('fundamentals', [{}])[0].get('revenue', float('nan')),
                    data[symbol].get('fundamentals', {}).get('fundamentals', [{}])[0].get('incomeNetPerWabsoSplitAdjusted', float('nan'))
            ]
            new_rows.append(new_row)

    # Convert the list of lists to a DataFrame
    new_rows_df = pd.DataFrame(new_rows, columns=rv_columns)

    # Concatenate the new rows to the existing DataFrame
    rv_dataframe = pd.concat([rv_dataframe, new_rows_df], ignore_index=True)


    # Save the result to a CSV file
    #rv_dataframe.to_csv("nikola.csv", index=False)
    return rv_dataframe


def assign_composite_score(df):
    pe_ratio = df["Price-to-Earnings Ratio"].astype(float)
    pb_ratio = df["Price-to-Book Ratio"].astype(float)
    print(pb_ratio)
    #free_cash_flow = df["Free Cash Flow"]
    normalized_pe = pe_ratio / max(pe_ratio.max(), pb_ratio.max())
    normalized_pb = pb_ratio / max(pe_ratio.max(), pb_ratio.max())
    #normalized_fcf = free_cash_flow / max(pe_ratio, pb_ratio, free_cash_flow)

    weight_pe = 0.6
    weight_pb = 0.4
    weight_fcf = 0

    # Calculate the composite score
    composite_score = (weight_pe * normalized_pe) + (weight_pb * normalized_pb)# + (weight_fcf * normalized_fcf)
    df = df.assign(composite_score=composite_score)
    return df


def min_max_normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

def assign_financial_composite_metric(df):
    net_income = df.get('net_income').astype(float)
    equity = df.get('equity').astype(float)
    revenue = df.get('revenue').astype(float)
    eps = df.get('eps').astype(float)
    stock_price = df.get('Price').astype(float)  # Replace with actual stock price

    roe = net_income / equity
    profit_margin = net_income / revenue
    earnings_yield = eps / stock_price

    # Normalize the ratios (optional)
    # Min-Max normalize each ratio
    roe_normalized = min_max_normalize(roe, min(roe), max(roe))
    profit_margin_normalized = min_max_normalize(profit_margin, min(profit_margin), max(profit_margin))
    earnings_yield_normalized = min_max_normalize(earnings_yield, min(earnings_yield), max(earnings_yield))

    # Calculate the composite metric (e.g., average)
    composite_financial_metric = (roe_normalized + profit_margin_normalized + earnings_yield_normalized) / 3
    df = df.assign(composite_financial_score=composite_financial_metric)
    return df


if __name__ == "__main__":
    sp500_symbols = retrieve_sp500_tickers()
    #sp500_symbols = ["MMM", "AAPL"]
    #sp500_symbols = ["NKLA"]
    # either query the dataframe online or read from the existing csv
    #rv_dataframe = get_initial_dataframe(sp500_symbols)
    rv_dataframe = pd.read_csv("sp500.csv")

    rv_dataframe = assign_composite_score(rv_dataframe)
    rv_dataframe = assign_financial_composite_metric(rv_dataframe)
    rv_dataframe = rv_dataframe.sort_values(by='composite_score', ascending=False)
    rv_dataframe.to_csv("sthsth_new.csv", index=False)
