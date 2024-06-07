import sys

from cli.parser import create_parser
from config.config import load_config


def main():
    config = load_config()

    parser = create_parser()
    args = parser.parse_args()

    # Use config or CLI args
    if args.command:
        command = args.command
    else:
        command = config.get("default_command")

    # Handle commands
    if command == "fetch_stocks":
        from cli.commands import fetch_stocks

        fetch_stocks(args)
    elif command == "run_strategy":
        from cli.commands import run_strategy

        if args.strategy:
            run_strategy(args)
        else:
            strategies = config.get("strategies", [])
            for strategy in strategies:
                run_strategy(strategy)
    elif command == "schedule_email":
        from cli.commands import schedule_email

        if args.email:
            schedule_email(args)
        else:
            email_config = config.get("email_alerts", {})
            schedule_email(email_config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
