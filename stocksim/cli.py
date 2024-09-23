import typer
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing_extensions import Annotated
from rich.console import Console
from rich.progress import Progress, SpinnerColumn

from .utils import run_simulation, ReturnsDistribution

app = typer.Typer(help="Simulate stock price over a future period")
console = Console()

@app.command()
def simulate(
    ticker: Annotated[str, typer.Option(..., help="Stock ticker symbol")],
    target_price: Annotated[float, typer.Option(help="Target price for probability calculation")],
    days: Annotated[int, typer.Option(help="Number of days for simulation")] = 30,
    simulations: Annotated[int, typer.Option('--runs', help="Number of Monte Carlo simulation runs")] = 1000,
    returns_dist: Annotated[ReturnsDistribution, typer.Option(help="Method for generating returns")] = ReturnsDistribution.bootstrap,
    ever_above: Annotated[float, typer.Option(help="Target price to calculate probability of ever reaching above  (defaults to target_price if not specified)")] = None,
    ever_below: Annotated[float, typer.Option(help="Target price to calculate probability of ever dipping below")] = None,
    history_length: Annotated[float, typer.Option('--history', help="Number of years of historical data to use. For half year use 0.5.")] = 5.0
):
    """
    Run a Monte Carlo simulation for stock price prediction.
    """
    with Progress(SpinnerColumn(), "[progress.description]{task.description}") as progress:
        progress.add_task(description="Processing...", total=None)
        # Download historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=history_length*365)  # 5 years ago
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        # simulate future stock prices
        last_price = data['Close'].iloc[-1]
        price_paths = run_simulation(data, returns_dist, days, simulations)
        
        # Convert to DataFrame
        simulation_df = pd.DataFrame(price_paths, columns=[f'Sim_{i}' for i in range(simulations)])
        
        # Calculate probability of exceeding target price
        final_prices = simulation_df.iloc[-1]
        prob_above_target = (final_prices > target_price).mean()
        quantile_25 = final_prices.quantile(0.25)
        quantile_75 = final_prices.quantile(0.75)
        
        ever_above = ever_above if ever_above is not None else target_price
        prob_ever_above = (simulation_df.max() > ever_above).mean()
    
        prob_ever_below = None
        if ever_below is not None:
            prob_ever_below = (simulation_df.min() < ever_below).mean()
        
        progress.remove_task(progress.task_ids[0])
        # Output results
        console.print(f"Monte Carlo simulation results for [bold yellow on black]{ticker}[/]:")
        console.print(f"Number of simulations: {simulations:,}")
        console.print(f"Number of days: {days}")
        console.print(f"Historical data from {start_date:%Y-%m-%d} to {end_date:%Y-%m-%d}")
        console.print(f"Returns distribution method: [cyan]{returns_dist.value}")
        console.print(f"Current price: ${last_price:.2f}")
        console.print(f"Target price: ${target_price:.2f}")
        console.print("[bold white]Results: " + "="*40)
        console.print(f"Probability of price above target: {prob_above_target:.2%}")
        console.print(f"Probability of ever reaching above ${ever_above:.2f}: {prob_ever_above:.2%}")
        if prob_ever_below is not None:
            console.print(f"Probability of ever dipping below ${ever_below:.2f}: {prob_ever_below:.2%}")
        console.print(f"Simulated price range: ${final_prices.min():.2f} - ${final_prices.max():.2f}")
        console.print(f"25th-75th percentile range: ${quantile_25:.2f} - ${quantile_75:.2f}")
