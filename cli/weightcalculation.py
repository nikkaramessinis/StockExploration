import pandas as pd
import riskfolio as rp
import yfinance as yf


def calculate_weights(tickers):
    # Calculate returns
    data = yf.download(tickers, start="2020-01-01", end="2023-01-01")["Adj Close"]

    returns = data.pct_change().dropna()

    # Step 4: Create a portfolio object
    port = rp.Portfolio(returns=returns)

    # Step 4: Set the portfolio objective
    port.assets_stats(
        method_mu="hist", method_cov="hist"
    )  # Use historical data for stats
    model = "Classic"  # Could be Classic, BL (Black-Litterman), FM (Factor Model)
    rm = "MV"  # Risk measure ('MV' = Mean-Variance, 'MAD' = Mean Absolute Deviation, etc.)
    obj = "Sharpe"  # Objective function (maximize Sharpe ratio)
    hist = True  # Use historical returns to compute the frontier

    # Step 5: Optimization
    weights = port.optimization(model=model, rm=rm, obj=obj, hist=hist)
    # Step 7: Display optimized weights
    # Display optimized weights
    print(f"Optimized Weights:{weights} type {type(weights)}")
    return weights
