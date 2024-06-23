from strategies.backtesting_ema import EmaCross
from strategies.backtesting_rsi import RSIOscilatorCross
from strategies.backtesting_sma import SmaCross
from strategies.technical_analysis import analyze


def run_prediction(
    strategy_name, stocks_list, display_dashboard, save_reference, enable_optimizing
):
    strategies = {
        "SMA": SmaCross,
        "EMA": EmaCross,
        "RSI": RSIOscilatorCross,
        # Add other strategies here
    }

    if strategy_name in strategies:
        strategy = strategies[strategy_name]
        return analyze(
            strategy, stocks_list, display_dashboard, save_reference, enable_optimizing
        )
    else:
        return f"Strategy {strategy_name} not found."
