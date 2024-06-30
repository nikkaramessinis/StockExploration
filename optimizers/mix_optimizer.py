def optimize_strategy(params: Dict, maximize_metric="Equity Final [$]"):
    """
    Optimize strategy parameters using bt.optimize.
    
    Parameters:
    - upper_bound_range: Range or list of values for the upper_bound parameter (optional).
    - lower_bound_range: Range or list of values for the lower_bound parameter (optional).
    - rsi_window_range: Range or list of values for the rsi_window parameter (optional).
    - maximize_metric: The metric to maximize during optimization.
    
    Returns:
    - stats: The optimization statistics.
    - optiheatmap: The heatmap of the optimization results.
    """
    # Dictionary to hold the parameters
    params = {}
    
    # Add parameters to the dictionary if they are provided
    if upper_bound_range is not None:
        params['upper_bound'] = upper_bound_range
    if lower_bound_range is not None:
        params['lower_bound'] = lower_bound_range
    if rsi_window_range is not None:
        params['rsi_window'] = rsi_window_range
    
    stats, optiheatmap = bt.optimize(
        **params,
        maximize=maximize_metric,
        constraint=lambda param: param.upper_bound > param.lower_bound if 'upper_bound' in param and 'lower_bound' in param else True,
        return_heatmap=True
    )
    
    return stats, optiheatmap


class RSIOptimizer(Optimizer):
    def optimize(self):
        upper_bounds, lower_bounds, rsi_windows = 0, 0, 0
        for symbol in self.stocks_list:
            print(f"Calling fetching data for symbol {symbol}")
            df = fetch_latest_data(symbol)
            df = fill_with_ta(df)

            bt = Backtest(df, self.strategy, cash=1000, commission=0.002, exclusive_orders=True)
            stats, optiheatmap = optimize_strategy(upper_bound_range=range(40, 85, 5), lower_bound_range=range(10, 45, 5), rsi_window_range=range(10, 30, 2), maximize_metric="Equity Final [$]")

            best_params = optiheatmap.idxmax(skipna=True)
            upper_bound, lower_bound, rsi_window,  = 70, 30, 15
            if isinstance(best_params, tuple):
                upper_bound = best_params[0]
                lower_bound = best_params[1]
                rsi_window = best_params[2]
            upper_bounds += upper_bound
            lower_bounds += lower_bound
            rsi_windows += rsi_window
            stats['Name'] = symbol
        upper_bound = upper_bounds//len(self.stocks_list)
        lower_bound = lower_bounds//len(self.stocks_list)
        rsi_windows = rsi_windows//len(self.stocks_list)
        print(f"upper_bound:{upper_bound}, lower_bound:{lower_bound}, rsi_window:{rsi_window}")
        return {"upper_bound":upper_bound, "lower_bound":lower_bound, "rsi_window":rsi_window}