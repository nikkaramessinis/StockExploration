import numpy as np
import pandas as pd
import talib as ta
from backtesting import Strategy
from backtesting.lib import crossover


class RSIOscillatorCross(Strategy):

    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def crossover_signals(self, buy_action, sell_action):
        if crossover(self.rsi, self.upper_bound):
            sell_action()
        elif crossover(self.lower_bound, self.rsi):
            buy_action()

    def init(self):
        self.price = self.data.Close
        self.rsi = self.I(ta.RSI, self.price, self.rsi_window)

    def next(self):
        self.crossover_signals(self.buy, self.position.close)

    def next_live(self):
        buy_print = lambda: print("change in momentum - buy")
        sell_print = lambda: print("change in momentum - sell")
        self.crossover_signals(buy_print, sell_print)
