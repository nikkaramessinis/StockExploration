from strategies.technical_analysis import analyze


def run_prediction(strategy_name, params):
    strategies = {
        "moving_average": moving_average_strategy,
        "linear_regression": linear_regression_strategy,
        "technical_analysis": analyze,
        # Add other strategies here
    }

    if strategy_name in strategies:
        strategy = strategies[strategy_name]
        return strategy(params)
    else:
        return f"Strategy {strategy_name} not found."


def moving_average_strategy(params):
    window_size = params.get("window_size", 50)
    # Placeholder for actual strategy implementation
    return f"Running moving average with window size {window_size}"


def linear_regression_strategy(params):
    lookback_period = params.get("lookback_period", 30)
    # Placeholder for actual strategy implementation
    return f"Running linear regression with lookback period {lookback_period}"
