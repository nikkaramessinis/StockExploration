from strategies.technical_analysis import analyze
from strategies.backtesting_sma import SmaCross
from strategies.backtesting_ema import EmaCross
from strategies.backtesting_rsi import RSIOscilatorCross

def run_prediction(strategy_name, stocks_list, show_graphs, show_feqos, save_reference, enable_optimizing):
    strategies = {
        "SMA": SmaCross,
        "EMA": EmaCross,
        "RSI": RSIOscilatorCross,
        # Add other strategies here
    }

    if strategy_name in strategies:
        strategy = strategies[strategy_name]
        return analyze(strategy, stocks_list, show_graphs, show_feqos, save_reference, enable_optimizing)
    else:
        return f"Strategy {strategy_name} not found."
