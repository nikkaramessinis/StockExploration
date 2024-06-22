from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta

class MACDCross(Strategy):

    def init(self):
        self.price = self.data.Close
        self.macd = self.I(lambda x: ta.MACD(x)[0], self.price)
        self.macd_signal = self.I(lambda x: ta.MACD(x)[1], self.price)


    def next(self):
        # Compare the values
        if crossover(self.macd, self.macd_signal):
            self.buy()
        elif crossover(self.macd_signal, self.macd):
            self.sell()