from numbers import Number

import numpy as np
import pandas as pd
import talib as ta
from backtesting import Strategy
from backtesting.lib import crossover

from utils.helpers import Momentum


class RSIOscillatorCross(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def crossover_signals(self, buy_action, sell_action, is_live=False):
        if crossover(self.rsi, self.upper_bound):
            return sell_action()
        elif crossover(self.lower_bound, self.rsi):
            high = self.data.High[-2]
            low = self.data.Low[-2]
            prev_close = self.data.Close[-3]
            atr = max(high - low, abs(high - prev_close), abs(low - prev_close))
            return buy_action(sl=self.data.Close[-1] - 2 * atr)
        if not is_live:
            return

        series1, series2 = self.convert_to_series(self.lower_bound, self.rsi)
        if series1[-1] > series2[-1]:
            return buy_action()
        series1, series2 = self.convert_to_series(self.rsi, self.upper_bound)
        if series1[-1] > series2[-1]:
            return sell_action()

    def init(self):
        self.price = self.data.Close
        self.rsi = self.I(ta.RSI, self.price, self.rsi_window)

    def next(self):
        self.crossover_signals(self.buy, self.position.close)

    def next_live(self, prev_value=""):
        buy_print = lambda: Momentum.UPWARD
        sell_print = lambda: Momentum.DOWNWARD
        signal = self.crossover_signals(buy_print, sell_print, True)
        if not signal:
            signal = prev_value
        print(f"Signal now is: {signal}")
        return signal

    def __str__(self):
        return f"MyClass[name=RSI]"
