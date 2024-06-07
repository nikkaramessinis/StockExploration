import yfinance as yf


def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1mo")
    return data.to_dict()
