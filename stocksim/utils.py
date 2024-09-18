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
    """
    Run a Monte Carlo simulation for stock price prediction.

    Parameters
    ----------
    data : pd.DataFrame
        Historical stock price data.
    returns_dist : ReturnsDistribution
        Method for generating returns.
    days : int
        Number of days for simulation.
    simulations : int
        Number of Monte Carlo simulations.

    Returns
    -------
    np.ndarray
        Array of simulated stock price paths. The shape is (days + 1, simulations). The additional day is the last day of the data.
    """
    if returns_dist == ReturnsDistribution.bootstrap:
        # Bootstrap
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