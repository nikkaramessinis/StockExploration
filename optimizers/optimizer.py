from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional, Callable, Dict, Any, Union, Tuple
from backtesting import Backtest
from utils.helpers import fetch_latest_data, fill_with_ta


class Optimizer:
    def __init__(self, strategy, stocks_list, default_values: Dict):
        self.strategy = strategy
        self.stocks_list = stocks_list
        self.default_values = default_values

    @staticmethod
    def optimize_strategy(bt,
        param_ranges: Dict[str, Union[range, list]],
        constraint_func: Optional[Callable[[Any], bool]],
        maximize_metric: str = "Equity Final [$]"
    ) -> Tuple[Any, Any]:

        stats, optiheatmap = bt.optimize(
            **param_ranges,
            maximize=maximize_metric,
            constraint=constraint_func,
            return_heatmap=True
        )
        return stats, optiheatmap

    def optimize(self, param_ranges, constraint_func: Optional[Callable[[Any], bool]]=None) -> Dict[str, Any]:
        param_sums = defaultdict(int)
        for symbol in self.stocks_list:
            print(f"Calling fetching data for symbol {symbol}")
            df = fetch_latest_data(symbol)
            df = fill_with_ta(df)
            bt = Backtest(df, self.strategy, cash=1000, commission=0.002, exclusive_orders=True)
            stats, optiheatmap = Optimizer.optimize_strategy(bt, param_ranges, constraint_func)
            best_params = optiheatmap.idxmax(skipna=True)
            if isinstance(best_params, tuple):
                for param, value in zip(param_ranges.keys(), best_params):
                    param_sums[param] += value
            else:
                for param, default_value in self.default_values.items():
                    param_sums[param] += default_value
                pass

            stats['Name'] = symbol
        
        # Calculate averages for each parameter
        averaged_params = {param: value // len(self.stocks_list) for param, value in param_sums.items()}
        
        print(f"Averaged parameters: {averaged_params}")
        return averaged_params
