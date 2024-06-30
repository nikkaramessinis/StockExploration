from backtesting import Strategy
from  pandas_ta.trend.chop import chop

# function that returns true if i%0==1
# Function to upload a file to an S3 bucket

# Function called my_chop that accepts a dataframe and a chop_len and an atr_len and return a pandas_ta.trend series.

def my_CHOP(df, chop_len, atr_len):
    #  Calculate Choppiness
    chop_series = chop(high=df['High'], low=df['Low'], close=df['Close'], length=chop_len, atr_length=atr_len)
    # what does chop_seried returns
    return chop_series

class GridCross(Strategy):
    chop_len = 14
    atr_len = 1
    num_grid_lines = 5 #  number of grid lines for buy/sell
    grid_interval = 10 / 10000 # 10 pips, 50 pips, or 100 pips or whatever
    take_profit_interval = 20 / 10000 #  pips
    stop_loss_interval = 10 / 10000 # pips
    buy_grid_prices = []
    sell_grid_prices = []
    executed_buy_grid_prices = []
    executed_sell_grid_prices = []
    last_purchase_price = 0
    long_hold = 0
    short_hold = 0
    buy_stop_loss_price = 0
    sell_stop_loss_price = 0
    grid_in_progress = False
    grid_start_index = 0 #  time index when grid starts
    grid_max_interval = 2000 #  max time steps to run the grid
    i = 0



    def init(self):
        super().init()
        #  Calculate indicators
        self.chop = self.I(my_CHOP, self.data, self.chop_len, self.atr_len)

    def reset_grid(self):
        self.grid_in_progress = False
        self.buy_grid_prices = []
        self.sell_grid_prices = []
        self.grid_start_index = 0
        self.buy_stop_loss_price = 0
        self.sell_stop_loss_price = 0
    
    def next(self):
        super().init()
        self.i += 1
        #  Check ranging or trending markets
        is_ranging = False
        if self.chop[-1] > 50 and self.chop[-2] <= 50:
            is_ranging = True
        #  Set up new grid for ranging -> against the trend
        current_price = self.data.Close[-1]
        if not self.grid_in_progress and is_ranging:
            self.reset_grid()
            self.grid_in_progress = True
            self.grid_start_index = self.i
            #  Stop loss
            buy_stop_loss = current_price - (self.num_grid_lines * self.grid_interval) - self.stop_loss_interval
            sell_stop_loss = current_price + (self.num_grid_lines * self.grid_interval) + self.stop_loss_interval
            #  Set buy/sell grid prices
            for i in range(1, self.num_grid_lines + 1):
                #  Calculate buy grid price
                grid_buy_price = current_price - (i * self.grid_interval)
                buy_take_profit = grid_buy_price + self.take_profit_interval
                self.buy_grid_prices.append(grid_buy_price)
                #  Create buy order
                self.buy(size=0.1, limit=grid_buy_price, sl=buy_stop_loss, tp=buy_take_profit)
                #  Calculate sell grid price
                grid_sell_price = current_price + (i * self.grid_interval)
                sell_take_profit = grid_sell_price - self.take_profit_interval
                self.sell_grid_prices.append(grid_sell_price)
                #  Create sell order
                self.sell(size=0.1, limit=grid_sell_price, sl=sell_stop_loss, tp=sell_take_profit)
            #  Optional - Plot the grid
            #plot_chart(self.i, symbol, df, current_price, self.buy_grid_prices, self.sell_grid_prices, buy_stop_loss, sell_stop_loss)