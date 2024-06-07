import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="Stock Performance Prediction App")

    subparsers = parser.add_subparsers(dest="command")

    # Fetch stocks command
    fetch_parser = subparsers.add_parser("fetch_stocks", help="Fetch stocks data")
    fetch_parser.add_argument(
        "--symbols", nargs="+", type=str, help="Stock symbols to fetch"
    )

    # Run strategy command
    strategy_parser = subparsers.add_parser(
        "run_strategy", help="Run prediction strategy"
    )
    strategy_parser.add_argument(
        "--strategy", type=str, help="Name of the strategy to run"
    )
    strategy_parser.add_argument(
        "--params", type=str, help="Parameters for the strategy in JSON format"
    )

    # Schedule email command
    email_parser = subparsers.add_parser("schedule_email", help="Schedule email alerts")
    email_parser.add_argument(
        "--email", type=str, help="Email configuration in JSON format"
    )

    return parser
