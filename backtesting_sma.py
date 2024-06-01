from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import talib as ta

class SmaCross(Strategy):

    def init(self):
        self.price = self.data.Close
        self.ma1 = self.I(ta.SMA, self.price, 15)


    def next(self):
        # Compare the values
        if crossover(self.price,self.ma1):
            self.buy()
        elif crossover(self.ma1, self.price):
            #self.position.close()
            self.sell()



import pandas as pd
from backtesting.lib import SignalStrategy, TrailingStrategy


class SmaCross1(SignalStrategy,
               TrailingStrategy):
    n1 = 10
    n2 = 25

    def init(self):
        # In init() and in next() it is important to call the
        # super method to properly initialize the parent classes
        super().init()

        # Precompute the two moving averages
        sma1 = self.I(MACD, self.data.Close, self.n1)
        sma2 = self.I(MACD, self.data.Close, self.n2)

        # Where sma1 crosses sma2 upwards. Diff gives us [-1,0, *1*]
        signal = (pd.Series(sma1) > sma2).astype(int).diff().fillna(0)
        signal = signal.replace(-1, 0)  # Upwards/long only

        # Use 95% of available liquidity (at the time) on each order.
        # (Leaving a value of 1. would instead buy a single share.)
        entry_size = signal * .95

        # Set order entry sizes using the method provided by
        # `SignalStrategy`. See the docs.
        self.set_signal(entry_size=entry_size)

        # Set trailing stop-loss to 2x ATR using
        # the method provided by `TrailingStrategy`
        self.set_trailing_sl(2)


#bt = Backtest(GOOG, SmaCross1, commission=.002,
#exclusive_orders=True)
#stats = bt.run()
#print(stats)
#bt.plot()