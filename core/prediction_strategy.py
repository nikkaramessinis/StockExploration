from strategies.technical_analysis import analyze


def run_prediction(strategy_name, stocks_list, display_dashboard, save_reference):
    strategies = {
        "technical_analysis": analyze,
        # Add other strategies here
    }

    if strategy_name in strategies:
        strategy = strategies[strategy_name]
        return strategy(stocks_list, display_dashboard, save_reference)
    else:
        return f"Strategy {strategy_name} not found."
