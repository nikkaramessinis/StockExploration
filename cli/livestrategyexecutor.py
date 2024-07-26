from backtesting import Backtest, Strategy
from backtesting._util import _Data
from backtesting.backtesting import _Broker


class LiveStrategyExecutor(Backtest):
    def __init__(self, *args, **kwargs):
        # Call the __init__ of the parent Backtest class
        super().__init__(*args, **kwargs)

    def live_strategy(self, **kwargs):
        # Implement the logic for your live strategy here
        data = _Data(self._data.copy(deep=False))
        broker: _Broker = self._broker(data=data)
        strategy: Strategy = self._strategy(broker, data, kwargs)
        strategy.init()
        last_row = self._data.iloc[-1]
        print(f"Running live strategy... {last_row['Close']}")
        return strategy.next_live()


# Example usage:
# Assuming you have defined your strategy and data
# strategy = YourStrategy()
# data = pd.DataFrame(...)  # Your data here

# Initialize the extended backtest
# extended_bt = ExtendedBacktest(data, strategy)
# extended_bt.run()  # This would run the backtest
# extended_bt.live_strategy()  # This would run the live strategy
