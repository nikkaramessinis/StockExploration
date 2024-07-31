from numbers import Number

import numpy as np
import pandas as pd
import talib as ta
import tensorflow as tf
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
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential

from utils.helpers import Momentum

columns_to_keep = [
    "sma_15",
    "ema_20",
    "SMA 30",
    "SMA 60",
    "MACD",
    "MACD_Signal",
    "MACD_Hist",
    "ATR",
    "OBV",
    "MFI",
    "ADX",
    "Stochastic_D",
    "Stochastic_K",
    "BB_Upper",
    "BB_Middle",
    "BB_Lower",
    "Lag_1",
    "Lag_2",
    "Lag_3",
    "direction",
]


class LogisticRegressionCross(Strategy):
    def crossover_signals(self, buy_action, sell_action):
        subset = self.data.df[columns_to_keep]
        X = subset.drop(columns=["direction"])

        X_last_row = X.iloc[-2].values.reshape(1, -1)

        # Make the prediction
        prediction = self.model.predict(X_last_row)[0]
        if prediction > 0.6:
            buy_action()
        elif prediction < 0.5:
            sell_action()

    def init(self):
        self.price = self.data.Close

        print(len(self.data.df))

        subset = self.data.df[columns_to_keep]
        subset.dropna(inplace=True)
        X = subset.drop(columns=["direction"])
        print(f"X.columns {X.columns} len{len(X)}")
        y = subset["direction"]
        print(y)

        # Normalize the data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Split to train test
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )

        # Define the model
        self.model = Sequential(
            [
                Dense(256, input_dim=X_train.shape[1], activation="relu"),
                Dropout(0.3),
                Dense(128, activation="relu"),
                Dropout(0.5),
                Dense(64, activation="relu"),
                Dropout(0.3),
                Dense(1, activation="sigmoid"),
            ]
        )

        self.model.compile(
            optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]
        )
        history = self.model.fit(
            X_train,
            y_train,
            epochs=100,
            batch_size=32,
            validation_data=(X_test, y_test),
        )

        predictions = self.model.predict(X_test)
        # Evaluate the model

        loss, accuracy = self.model.evaluate(X_test, y_test)
        print(f"Test Accuracy: {accuracy:.2f}")

    def next(self):
        self.crossover_signals(self.buy, self.position.close)

    def next_live(self, prev_value=""):
        pass

    def __str__(self):
        return f"MyClass[name=RSI]"
