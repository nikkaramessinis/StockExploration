from strategies.backtesting_ema import EmaCross
from strategies.backtesting_rsi import RSIOscillatorCross
from strategies.backtesting_sma import SmaCross
from strategies.backtesting_bollinger_bands import BBandsCross
from strategies.technical_analysis import analyze
from strategies.optimization import optimize

def run_prediction(
    strategy_name, stocks_list, display_dashboard, save_reference, enable_optimizing
):
    strategies = {
        "SMA": SmaCross,
        "EMA": EmaCross,
        "RSI": RSIOscillatorCross,
        "BBands": BBandsCross,
        # Add other strategies here
    }

    if strategy_name in strategies:
        strategy = strategies[strategy_name]

        if enable_optimizing:
            args = optimize(strategy, stocks_list)
        return analyze(
            strategy, stocks_list, display_dashboard, save_reference, args
        )
    else:
        return f"Strategy {strategy_name} not found."
