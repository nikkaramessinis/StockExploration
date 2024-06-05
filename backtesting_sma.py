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
        if crossover(self.price, self.ma1):
            self.buy()
        elif crossover(self.ma1, self.price):
            #self.position.close()
            self.sell()