from optimizers.optimizer import Optimizer
from backtesting import Backtest
from utils.helpers import fetch_latest_data, fill_with_ta
from pandas_ta.trend.chop import chop

class GridOptimizer(Optimizer):
    def optimize(self):
        chop_lens = 0
        atr_lens = 0
        for symbol in self.stocks_list:
            print(f"Calling fetching data for symbol {symbol}")
            df = fetch_latest_data(symbol)
            df = fill_with_ta(df)

            bt = Backtest(df, self.strategy, cash=1000, commission=0.002, exclusive_orders=True)
            stats, optiheatmap = bt.optimize(chop_len=range(5, 20, 2),
                                atr_len=range(1, 10, 2),
                                maximize="Equity Final [$]",
                                return_heatmap = True
                                )
            best_params = optiheatmap.idxmax(skipna=True)
            chop_len, atr_len = 14, 1
            if isinstance(best_params, tuple):
                chop_len = best_params[0]
                atr_len = best_params[1]
            chop_lens += chop_len
            atr_lens += atr_len
            stats['Name'] = symbol
        chop_len = chop_lens//len(self.stocks_list)
        atr_len = atr_lens//len(self.stocks_list)
        print(f"atr_len:{atr_len} chop_len:{chop_len}")
        return {"atr_len":atr_len, "chop_len":chop_len}