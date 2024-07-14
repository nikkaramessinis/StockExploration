from optimizers.optimizer import Optimizer
from optimizers.strategy_params import get_params_defaults, get_params_ranges

from strategies.technical_analysis import analyze



def run_prediction(
    strategy, strategy_name, stocks_list, display_dashboard, save_reference, enable_optimizing
):
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
    return analyze(strategy_name, stocks_list, display_dashboard, save_reference, args)
