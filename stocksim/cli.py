import typer
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing_extensions import Annotated
from rich import print
from rich.progress import Progress, SpinnerColumn

from .utils import run_simulation, ReturnsDistribution

app = typer.Typer(help="Simulate stock price over a future period")

@app.command()
def simulate(
    ticker: Annotated[str, typer.Option(..., help="Stock ticker symbol")],
    target_price: Annotated[float, typer.Option(help="Target price for probability calculation")],
    days: Annotated[int, typer.Option(help="Number of days for simulation")] = 30,
    simulations: Annotated[int, typer.Option('--sims', help="Number of Monte Carlo simulations")] = 1000,
    returns_dist: Annotated[ReturnsDistribution, typer.Option(help="Method for generating returns")] = ReturnsDistribution.bootstrap
):
    """
    Run a Monte Carlo simulation for stock price prediction.
    """
    with Progress(SpinnerColumn(), "[progress.description]{task.description}") as progress:
        progress.add_task(description="Processing...", total=None)
        # Download historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5*365)  # 5 years ago
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        # simulate future stock prices
        last_price = data['Close'].iloc[-1]
        price_paths = run_simulation(data, returns_dist, days, simulations)
        
        # Convert to DataFrame
        simulation_df = pd.DataFrame(price_paths, columns=[f'Sim_{i}' for i in range(simulations)])
        
        # Calculate probability of exceeding target price
        final_prices = simulation_df.iloc[-1]
        prob_above_target = (final_prices > target_price).mean()
        
        progress.remove_task(progress.task_ids[0])
        # Output results
        print(f"Monte Carlo simulation results for [bold yellow on black]{ticker}[/]:")
        print(f"Number of simulations: {simulations:,}")
        print(f"Number of days: {days}")
        print(f"Returns distribution method: [green]{returns_dist.value}")
        print(f"Target price: ${target_price:.2f}")
        print(f"Probability of price above target: {prob_above_target:.2%}")
        print(f"Current price: ${last_price:.2f}")
        print(f"Simulated price range: ${final_prices.min():.2f} - ${final_prices.max():.2f}")
