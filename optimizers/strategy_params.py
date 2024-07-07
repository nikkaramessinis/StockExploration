class StrategyParams(object):
    def __init__(self, param_ranges, param_defaults):
        self.param_ranges = param_ranges
        self.param_defaults = param_defaults


strategy_params = {
    "RSI": StrategyParams(
        param_ranges={
            "upper_bound": range(40, 85, 5),
            "lower_bound": range(10, 45, 5),
            "rsi_window": range(10, 30, 2),
        },
        param_defaults={
            "upper_bound": 70,
            "lower_bound": 30,
            "rsi_window": 15,
        },
    ),
    "Mix": StrategyParams(
        param_ranges={
            "upper_bound": range(40, 85, 5),
            "lower_bound": range(10, 45, 5),
            "rsi_window": range(10, 30, 2),
            "ema_period_1": range(5, 20, 3),
            "ema_period_2": range(20, 50, 5),
        },
        param_defaults={
            "upper_bound": 70,
            "lower_bound": 30,
            "rsi_window": 15,
            "ema_period_1": 9,
            "ema_period_2": 21,
        },
    ),
}


def get_params_ranges(strategy_name):
    if strategy_name not in strategy_params:
        assert (
            False
        ), f"Strategy_name {strategy_name} does not exist in strategy_params!"
    return (strategy_params[strategy_name]).param_ranges


def get_params_defaults(strategy_name):
    if strategy_name not in strategy_params:
        assert (
            False
        ), f"Strategy_name {strategy_name} does not exist in strategy_params!"
    return strategy_params[strategy_name].param_defaults
