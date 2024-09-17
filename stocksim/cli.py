import click
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

@click.group()
@click.version_option()
def cli():
    "Simulate stock price over a future period"

@click.command()
@click.option('--ticker', required=True, help='Stock ticker symbol')
@click.option('--days', default=30, help='Number of days for simulation')
@click.option('--target-price', required=True, type=float, help='Target price for probability calculation')
@click.option('--simulations', default=1000, help='Number of Monte Carlo simulations')
def cli(ticker, days, target_price, simulations):
    # Download historical data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)  # 5 years ago
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # Calculate daily returns
    returns = data['Close'].pct_change().dropna()
    
    # Calculate mean and variance of daily returns
    mu = returns.mean()
    var = returns.var()
    
    # Simulate future stock prices
    last_price = data['Close'].iloc[-1]
    
    # Create a matrix of random returns
    random_returns = np.random.normal(mu, var**0.5, size=(days, simulations))
    
    # Calculate price paths
    price_paths = last_price * np.exp(np.cumsum(random_returns, axis=0))
    
    # Insert the initial price at the beginning of each path
    price_paths = np.insert(price_paths, 0, last_price, axis=0)
    
    # Convert to DataFrame
    simulation_df = pd.DataFrame(price_paths, columns=[f'Sim_{i}' for i in range(simulations)])
    
    # Calculate probability of exceeding target price
    final_prices = simulation_df.iloc[-1]
    prob_above_target = (final_prices > target_price).mean()
    
    # Output results
    click.echo(f"Monte Carlo simulation results for {ticker}:")
    click.echo(f"Number of simulations: {simulations}")
    click.echo(f"Number of days: {days}")
    click.echo(f"Target price: ${target_price:.2f}")
    click.echo(f"Probability of price above target: {prob_above_target:.2%}")
    click.echo(f"Current price: ${last_price:.2f}")
    click.echo(f"Simulated price range: ${final_prices.min():.2f} - ${final_prices.max():.2f}")

if __name__ == '__main__':
    cli()
