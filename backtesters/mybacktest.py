import numpy as np
import pandas as pd
from backtesting import Backtest
from backtesting._stats import compute_stats
from backtesting._util import _as_str, _Data, _Indicator, try_


class _OutOfMoneyError(Exception):
    pass


class MyBackTest(Backtest):
    def __init__(self,
            data: pd.DataFrame,
            strategy: Type[Strategy],
            *,
            cash: float = 10_000,
            commission: float = .0,
            margin: float = 1.,
            trade_on_close=False,
            hedging=False,
            exclusive_orders=False
            ):
        super().__init__(
            data,
            strategy,
            *,
            cash,
            commission,
            margin,
            trade_on_close,
            hedging,
            exclusive_orders)
        data = _Data(self._data.copy(deep=False))
        broker: _Broker = self._broker(data=data)

    def run(self, **kwargs) -> pd.Series:
        strategy: Strategy = self._strategy(self.broker, self.data, kwargs)

        strategy.init()
        data._update()  # Strategy.init might have changed/added to data.df

        # Indicators used in Strategy.next()
        indicator_attrs = {
            attr: indicator
            for attr, indicator in strategy.__dict__.items()
            if isinstance(indicator, _Indicator)
        }.items()

        # Skip first few candles where indicators are still "warming up"
        # +1 to have at least two entries available
        start = 1 + max(
            (
                np.isnan(indicator.astype(float)).argmin(axis=-1).max()
                for _, indicator in indicator_attrs
            ),
            default=0,
        )

        # Disable "invalid value encountered in ..." warnings. Comparison
        # np.nan >= 3 is not invalid; it's False.
        with np.errstate(invalid="ignore"):

            for i in range(start, len(self._data)):
                # Prepare data and indicators for `next` call
                data._set_length(i + 1)
                for attr, indicator in indicator_attrs:
                    # Slice indicator on the last dimension (case of 2d indicator)
                    setattr(strategy, attr, indicator[..., : i + 1])

                # Handle orders processing and broker stuff
                try:
                    broker.next()
                except _OutOfMoneyError:
                    break

                # Next tick, a moment before bar close
                strategy.next()
            else:
                # Close any remaining open trades so they produce some stats
                for trade in broker.trades:
                    trade.close()

                # Re-run broker one last time to handle orders placed in the last strategy
                # iteration. Use the same OHLC values as in the last broker iteration.
                if start < len(self._data):
                    try_(broker.next, exception=_OutOfMoneyError)

            # Set data back to full length
            # for future `indicator._opts['data'].index` calls to work
            data._set_length(len(self._data))

            equity = pd.Series(broker._equity).bfill().fillna(broker._cash).values
            self._results = compute_stats(
                trades=broker.closed_trades,
                equity=equity,
                ohlc_data=self._data,
                risk_free_rate=0.0,
                strategy_instance=strategy,
            )
        return self._results
