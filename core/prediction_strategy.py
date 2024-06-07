from strategies.technical_analysis import analyze


def run_prediction(strategy_name, stocks_list, hide_graphs):
    strategies = {
        "technical_analysis": analyze,
        "linear_regression": linear_regression_strategy,
        # Add other strategies here
    }

    if strategy_name in strategies:
        strategy = strategies[strategy_name]
        return strategy(stocks_list, hide_graphs)
    else:
        return f"Strategy {strategy_name} not found."


def linear_regression_strategy(params):
    lookback_period = params.get("lookback_period", 30)
    # Placeholder for actual strategy implementation
    return f"Running linear regression with lookback period {lookback_period}"
