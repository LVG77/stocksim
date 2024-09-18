from enum import Enum
import numpy as np
import pandas as pd


class ReturnsDistribution(str, Enum):
    bootstrap = "bootstrap"
    normal = "normal"

def run_simulation(
    data: pd.DataFrame,
    returns_dist: ReturnsDistribution,
    days: int,
    simulations: int
) -> np.ndarray:
        # Calculate daily returns
        returns = data['Close'].pct_change().dropna()

        # Simulate future stock prices
        last_price = data['Close'].iloc[-1]

        if returns_dist == ReturnsDistribution.bootstrap:
            random_returns = np.random.choice(returns, size=(days, simulations), replace=True)
        else:  # normal distribution
            mu = returns.mean()
            var = returns.var()
            random_returns = np.random.normal(mu, var**0.5, size=(days, simulations))

        # Calculate price paths
        price_paths = last_price * np.cumprod(1 + random_returns, axis=0)

        # Insert the initial price at the beginning of each path
        price_paths = np.insert(price_paths, 0, last_price, axis=0)
        return price_paths