from .trade import get_account, get_orders


def print_order_details():
    orders = get_orders()
    for order in orders:
        symbol, qty, average_fill_price, status = (
            order["symbol"],
            order["qty"],
            order["filled_avg_price"],
            order["status"],
        )

        print(
            f"symbol={symbol}, qty={qty}, status={status}, average_fill_price={average_fill_price}"
        )


def print_account_details():
    account = get_account()
    cash = account["cash"]
    buying_power = account["buying_power"]
    portfolio_value = account["portfolio_value"]

    print(
        f"cash={cash}, buying_power={buying_power}, portfolio_value={portfolio_value}"
    )


def main():
    print_account_details()
    print_order_details()


if __name__ == "__main__":
    main()
