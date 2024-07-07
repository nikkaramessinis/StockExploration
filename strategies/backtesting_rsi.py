import numpy as np
import pandas as pd
import talib as ta
from backtesting import Strategy
from backtesting.lib import crossover


class RSIOscillatorCross(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
            self.sell()
        elif crossover(self.lower_bound, self.rsi):
            self.position.close()
            self.buy()

    @classmethod
    def generate_signal(cls, data, upper_bound=70, lower_bound=30, rsi_window=14):
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)

        price = data["Close"]
        rsi = ta.RSI(price, rsi_window)

        if len(rsi) > 1:
            crossover_upper = (rsi.shift(1) <= upper_bound) & (rsi > upper_bound)
            crossover_lower = (rsi.shift(1) >= lower_bound) & (rsi < lower_bound)
            signal = np.where(
                crossover_upper, "SELL", np.where(crossover_lower, "BUY", None)
            )
            return signal[-1]
        else:
            # For a single data point, we can't determine a crossover
            if rsi.iloc[-1] > upper_bound:
                return "SELL"
            elif rsi.iloc[-1] < lower_bound:
                return "BUY"
            else:
                return None
