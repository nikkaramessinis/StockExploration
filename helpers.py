import requests #The requests library for HTTP requests in Python
import bs4 as bs
from datetime import date
import yfinance as yf
import talib as ta
from enum import Enum


class Momentum(Enum):
    UPWARD = "upward"
    DOWNWARD = "downward"

def fill_with_ta(df, write_to_csv = False):
    df['engulfing'] = ta.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
    df['rsi'] = ta.RSI(df['Close'], timeperiod=14)
    df['sma_20'] = ta.SMA(df['Close'], 15)
    df['ema_20'] = ta.EMA(df['Close'], 20)
    if write_to_csv:
        df.to_csv("csvs/arm.csv", index=False)
    return df



def check_crossover(df):
    # Extract the closing price and SMA at the last moment
    last_row = df.iloc[-1]
    closing_price_last = last_row['Close']
    ema_last = last_row['ema_20']
    # Compare the values
    if closing_price_last > ema_last:
        return Momentum.UPWARD
    else:
        return Momentum.UPWARD

def fetch_latest_data(symbols_list, start_date='2023-09-27'):
    end_date = date.today()
    end_date = '2024-05-31'
    #df = yf.download(tickers=symbols_list, start=start_date, end=str(end_date), auto_adjust=True)
    ticker_yahoo = yf.Ticker(symbols_list)
    df = ticker_yahoo.history(start=start_date, end=str(end_date), auto_adjust=True)
    return df


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