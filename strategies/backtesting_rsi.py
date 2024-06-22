from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta

class RSIOscilatorCross(Strategy):

    upper_bound = 70
    lower_bound = 30
    rsi_window = 14
    def init(self):
        self.price = self.data.Close
        self.rsi = self.I(ta.RSI, self.price, self.rsi_window)


    def next(self):
        # Compare the values
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            self.buy()
