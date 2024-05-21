import requests #The requests library for HTTP requests in Python
import bs4 as bs


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