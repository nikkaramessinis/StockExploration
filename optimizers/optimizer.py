import multiprocessing
import warnings
from collections import defaultdict
from typing import Any, Callable, Dict, Optional, Tuple, Union

from backtesting import Backtest

from strategies.backtesting_rsi import RSIOscillatorCross
from utils.helpers import fetch_latest_data, fill_with_ta

# Suppress the warning about searching for best configurations
warnings.filterwarnings("ignore", message="Searching for best of*")

# Set multiprocessing start method to 'fork' on Unix-based systems
if hasattr(multiprocessing, "set_start_method"):
    try:
        multiprocessing.set_start_method("fork")
    except RuntimeError:
        pass  # method already set


class Optimizer:
    def __init__(self, strategy, stocks_list, default_values: Dict):
        self.strategy = strategy
        self.stocks_list = stocks_list
        self.default_values = default_values

    @staticmethod
    def optimize_strategy(
        bt,
        param_ranges: Dict[str, Union[range, list]],
        constraint_func: Optional[Callable[[Any], bool]],
        maximize_metric: str = "Equity Final [$]",
    ) -> Tuple[Any, Any]:

        stats, optiheatmap = bt.optimize(
            **param_ranges,
            maximize=maximize_metric,
            constraint=constraint_func,
            return_heatmap=True,
        )
        return stats, optiheatmap

    def optimize(
        self, param_ranges, constraint_func: Optional[Callable[[Any], bool]] = None
    ) -> Dict[str, Any]:
        param_sums = defaultdict(int)
        for symbol in self.stocks_list:
            print(f"Calling fetching data for symbol {symbol}")
            df = fetch_latest_data(symbol)
            df = fill_with_ta(df)

            bt = Backtest(
                df, self.strategy, cash=1000, commission=0.002, exclusive_orders=True
            )

            # Set initial parameter values
            bt._strategy.upper_bound = param_ranges["upper_bound"].start
            bt._strategy.lower_bound = param_ranges["lower_bound"].start
            bt._strategy.rsi_window = param_ranges["rsi_window"].start

            stats, optiheatmap = self.optimize_strategy(
                bt, param_ranges, constraint_func
            )
            best_params = optiheatmap.idxmax(skipna=True)
            if isinstance(best_params, tuple):
                for param, value in zip(param_ranges.keys(), best_params):
                    param_sums[param] += value
            else:
                for param, default_value in self.default_values.items():
                    param_sums[param] += default_value

            stats["Name"] = symbol

        # Calculate averages for each parameter
        averaged_params = {
            param: value // len(self.stocks_list) for param, value in param_sums.items()
        }

        print(f"Averaged parameters: {averaged_params}")
        return averaged_params


# Example usage:
if __name__ == "__main__":
    stocks_list = ["AAPL", "MSFT", "GOOGL"]  # Example stock list
    default_values = {"upper_bound": 70, "lower_bound": 30, "rsi_window": 14}
    param_ranges = {
        "upper_bound": range(60, 81, 5),
        "lower_bound": range(20, 41, 5),
        "rsi_window": range(10, 21, 2),
    }

    optimizer = Optimizer(RSIOscillatorCross, stocks_list, default_values)
    optimized_params = optimizer.optimize(param_ranges)
    print("Optimized parameters:", optimized_params)
