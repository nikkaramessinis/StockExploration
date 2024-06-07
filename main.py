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

            strategies = config.get("strategies", [])
            for strategy_config in strategies:

                class Args:
                    strategy = strategy_config["name"]
                    params = json.dumps(strategy_config["parameters"])

                run_strategy(Args)
        elif command == "schedule_email":
            from cli.commands import schedule_email

            email_config = config.get("email_alerts", {})

            class Args:
                email = json.dumps(email_config)

            schedule_email(Args)
        else:
            print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
