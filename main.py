import warnings

# Suppress specific FutureWarnings from backtesting module
warnings.filterwarnings("ignore", category=FutureWarning, module="backtesting")

import json

from config.config import load_config


def main():
    config = load_config()
    commands = config.get("run_commands", [])

    for command in commands:
        if command == "fetch_stocks":
            from cli.commands import fetch_stocks

            class Args:
                stocks = config.get("stocks", [])

            fetch_stocks(Args)
        elif command == "run_strategy":
            from cli.commands import run_strategy

            class Args:
                strategy = config.get("strategies")
                stocks_list = config.get("stocks", [])
                show_graphs = config.get("show_graphs", False)
                display_dashboard = config.get("display_dashboard", False)
                save_reference = config.get("save_reference", False)
                enable_optimizing = config.get("enable_optimizing", "RSI")

            run_strategy(Args)
        elif command == "schedule_email":
            from cli.commands import email_alerts

            email_config = config.get("email_alerts", {})

            class Args:
                email = json.dumps(email_config)

            email_alerts(Args)
        else:
            print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
