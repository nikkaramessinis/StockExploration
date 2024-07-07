from optimizers.optimizer import Optimizer
from optimizers.strategy_params import get_params_defaults, get_params_ranges
from strategies.backtesting_bollinger_bands import BBandsCross
from strategies.backtesting_ema import EmaCross
from strategies.backtesting_grip import GridCross
from strategies.backtesting_mix import MixCross
from strategies.backtesting_rsi import RSIOscillatorCross
from strategies.backtesting_sma import SmaCross
from strategies.technical_analysis import analyze


def run_prediction(
    strategy_name, stocks_list, display_dashboard, save_reference, enable_optimizing
):
    strategies = {
        "SMA": SmaCross,
        "EMA": EmaCross,
        "RSI": RSIOscillatorCross,
        "BBands": BBandsCross,
        "Grid": GridCross,
        "Mix": MixCross,
        # Add other strategies here
    }

    if strategy_name in strategies:
        strategy = strategies[strategy_name]

        args = get_params_defaults(strategy_name)
        current_optimizer = Optimizer(strategy, stocks_list, args)
        if enable_optimizing:
            optimized_args = current_optimizer.optimize(
                get_params_ranges(strategy_name)
            )
            args = {
                key: (range(value, value + 1, 5))
                for key, value in optimized_args.items()
            }
        return analyze(strategy, stocks_list, display_dashboard, save_reference, args)
    else:
        return f"Strategy {strategy_name} not found."
