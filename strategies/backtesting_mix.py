from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import talib as ta

class MixCross(Strategy):
    ema_period_1 = 9
    ema_period_2 = 21
    rsi_period = 14
    rsi_low = 30
    rsi_high = 70
    take_profit_percent = 3
    stop_loss_percent = 1
    last_purchase_price = 0
    long_hold = 0

    def init(self):
        self.price = self.data.Close
        self.rsi = self.I(ta.RSI, self.price, self.rsi_period)
        self.ema1 = self.I(ta.EMA, self.price, ema_period_1)
        self.ema2 = self.I(ta.EMA, self.price, ema_period_2)


    def next(self):
        super().next()

        # EMA crossover check
        ema_crossover = crossover(self.ema_1, self.ema_2)
        
        # RSI crossing above the low threshold check
        rsi_crossover = crossover(self.rsi, self.rsi_low)

        # Determine the current price
        price = self.data.Close[-1]

        # Take profit and stop loss conditions
        is_take_profit = self.long_hold == 1 and price > self.last_purchase_price * (1 + (self.take_profit_percent / 100))
        is_stop_loss = self.long_hold == 1 and price < self.last_purchase_price * (1 - (self.stop_loss_percent / 100))

        # Long entry signal if both EMA and RSI conditions are met
        if self.long_hold == 0 and ema_crossover and rsi_crossover:
            self.buy()
            self.last_purchase_price = price
            self.long_hold = 1

        # Long exit signal if take profit or stop loss conditions are met
        elif self.long_hold == 1 and (is_take_profit or is_stop_loss):
            self.position.close()
            self.long_hold = 0
            self.last_purchase_price = 0