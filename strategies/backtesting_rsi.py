from backtesting.lib import crossover
import talib as ta

class RSIOscillatorCross:
    def __init__(self, upper_bound=70, lower_bound=30, rsi_window=14):
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.rsi_window = rsi_window

    def generate_signal(self, df):
        price = df['Close']
        rsi = ta.RSI(price, self.rsi_window)
        
        if crossover(rsi, self.upper_bound):
            return "UPWARD"
        elif crossover(self.lower_bound, rsi):
            return "DOWNWARD"
        else:
            return None
