from numbers import Number

import numpy as np
import pandas as pd
import talib as ta
from backtesting import Strategy
from backtesting.lib import crossover
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split

from utils.helpers import Momentum


class LogisticRegressionCross(Strategy):
    def crossover_signals(self, buy_action, sell_action):

        if crossover(self.rsi, self.upper_bound):
            # print("KARAM is sell signal")
            series1, series2 = self.convert_to_series(self.rsi, self.upper_bound)
            # if series1[-1] > series2[-1]:
            #    #print(f"{series1[-1]} > {series2[-1]}")
            return sell_action()
        elif crossover(self.lower_bound, self.rsi):
            # print("KARAM is buy signal")
            # print(f"type {type(self.rsi)} self.upper{type(self.upper_bound)}")
            series1, series2 = self.convert_to_series(self.rsi, self.upper_bound)
            # print(f"{series1[-1]} > {series2[-1]}")
            return buy_action()
        # if series1[-1] > series2[-1]:
        #    print("DOWARD MOMENTUM")
        #    return "DOWNWARD MOMENTUM"

        series1, series2 = self.convert_to_series(self.lower_bound, self.rsi)
        # print(f"{series1[-1]} > {series2[-1]}")
        if series1[-1] > series2[-1]:
            # print("upWARD MOMENTUM")
            return "UPWARD MOMENTUM"

    def init(self):
        self.price = self.data.Close

        print(len(self.data.df))
        subset = self.data.df[
            [
                "rsi",
                "sma_15",
                "ema_20",
                "SMA 30",
                "SMA 60",
                "Lag_1",
                "Lag_2",
                "direction",
            ]
        ]
        subset.dropna(inplace=True)

        X = subset[
            [
                "sma_15",
                "ema_20",
                "SMA 30",
                "SMA 60",
                "Lag_1",
                "Lag_2",
            ]
        ]
        print(X.columns)
        print(len(X))
        y = subset["direction"]
        print(y)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        model = LogisticRegression()
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        # Evaluate the model
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy:.2f}")

        # Confusion Matrix and Classification Report
        print(confusion_matrix(y_test, predictions))
        print(classification_report(y_test, predictions))
        print(f"type(X) {type(X)} {X.df.columns}")
        self.rsi = self.I(ta.RSI, self.price, self.rsi_window)

    def next(self):
        self.crossover_signals(self.buy, self.position.close)

    def next_live(self, prev_value=""):
        buy_print = lambda: Momentum.UPWARD
        sell_print = lambda: Momentum.DOWNWARD
        signal = self.crossover_signals(buy_print, sell_print)
        if not signal:
            signal = prev_value
        print(f"Karam {signal}")
        return signal

    def __str__(self):
        return f"MyClass[name=RSI]"
