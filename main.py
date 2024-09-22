import warnings

# Suppress specific FutureWarnings from backtesting module
warnings.filterwarnings("ignore", category=FutureWarning, module="backtesting")

import json

import yaml


def load_config(config_file="config/settings.yaml"):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config


def main():
    config = load_config()
    flow_list = config.get("strategy_flow", [])

    for flow in flow_list:

        class Args:
            stocks = config.get("stocks", [])

        if flow == "optimization" or flow == "live":
            from cli.commands import run_strategy

            class Args:
                flow_name = flow
                strategy = config.get("strategies")
                stocks_list = config.get("stocks", [])
                show_graphs = config.get("show_graphs", False)
                display_dashboard = config.get("display_dashboard", False)
                save_reference = config.get("save_reference", False)
                enable_optimizing = config.get("enable_optimizing", "RSI")
                enable_opt_portfolio = config.get("enable_opt_portfolio", False)

            run_strategy(Args)

        elif flow == "schedule_email":
            from cli.commands import email_alerts

            email_config = config.get("email_alerts", {})

            class Args:
                email = json.dumps(email_config)

            email_alerts(Args)
        else:
            print(f"Unknown flow: {flow}")


import os


def generate_secrets_file():
    secrets_file = os.path.join("config", "secrets.py")

    # Check if the file already exists
    if os.path.exists(secrets_file):
        print(f"The file {secrets_file} already exists. Skipping generation.")
        return True

    # Generate the secrets.py file
    try:
        with open(secrets_file, "w") as f:
            f.write("# This file contains sensitive information.\n\n")
            f.write("GMAIL_ADDRESS = ''\n")
            f.write("GMAIL_PASSWORD = ''\n")
        print(f"Successfully created {secrets_file}")
        print("Please edit this file and add your Gmail credentials.")
        return True
    except IOError as e:
        print(f"Error writing to {secrets_file}: {e}")
        return False


if __name__ == "__main__":
    # auto generate secrets.py if it doesn't exist
    generate_secrets_file()

    main()
