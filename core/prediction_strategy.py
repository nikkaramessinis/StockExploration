from strategies.backtesting_ema import EmaCross
from strategies.backtesting_rsi import RSIOscilatorCross
from strategies.backtesting_sma import SmaCross
from strategies.backtesting_bollinger_bands import BBandsCross
from strategies.backtesting_grip import GridCross
from strategies.technical_analysis import analyze
from optimizers.rsi_optimizer import RSIOptimizer
from optimizers.grid_optimizer import GridOptimizer

strategies_to_optimizer = {
    "RSI": RSIOptimizer,
    "Grid": GridOptimizer
    # Add other strategies here
}


def run_prediction(
    strategy_name, stocks_list, display_dashboard, save_reference, enable_optimizing
):
    strategies = {
        "SMA": SmaCross,
        "EMA": EmaCross,
        "RSI": RSIOscilatorCross,
        "BBands": BBandsCross,
        "Grid": GridCross
        # Add other strategies here
    }

    if strategy_name in strategies:
        strategy = strategies[strategy_name]

        if enable_optimizing:
            args = strategies_to_optimizer[strategy_name](strategy, stocks_list).optimize()
        return analyze(
            strategy, stocks_list, display_dashboard, save_reference, args
        )
    else:
        return f"Strategy {strategy_name} not found."
