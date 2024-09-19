# stocksim

<!-- [![PyPI](https://img.shields.io/pypi/v/stocksim.svg)](https://pypi.org/project/stocksim/) -->
[![Changelog](https://img.shields.io/github/v/release/LVG77/stocksim?include_prereleases&label=changelog)](https://github.com/LVG77/stocksim/releases)
[![Tests](https://github.com/LVG77/stocksim/actions/workflows/test.yml/badge.svg)](https://github.com/LVG77/stocksim/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/LVG77/stocksim/blob/master/LICENSE)

Simulate stock price over a future period

## Installation

Install this tool using `pip`:
```bash
pip install stocksim
```
## Usage

The `stocksim` tool provides a command-line interface to run Monte Carlo simulations for stock price prediction. To use the tool, you can run the following command:

```
stocksim [OPTIONS]
```

The available options are:

- `--ticker TEXT`: Stock ticker symbol.
- `--target-price FLOAT`: Target price for probability calculation.
- `--days INTEGER`: Number of days for simulation.
- `--runs INTEGER`: Number of Monte Carlo simulation runs.
- `--returns-dist [bootstrap|normal]`: Method for generating returns.
- `--ever-above FLOAT`: Target price to calculate probability of ever reaching above (defaults to `--target-price` if not specified).
- `--ever-below FLOAT`: Target price to calculate probability of ever dipping below.

Here's an example usage:

```
stocksim --ticker AAPL --target-price 150 --days 30 --runs 1000 --returns-dist bootstrap --ever-above 160
```

This will run a Monte Carlo simulation for the Apple (AAPL) stock with the following parameters:
- Target price: $150
- Number of days: 30
- Number of simulations: 1000
- Returns distribution method: Bootstrap
- Probability of ever reaching above $160

The tool will output the simulation results, including the probability of the stock price exceeding the target price, the probability of the stock price ever reaching above the specified price, and the simulated price range.

For help, run:
```bash
stocksim --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd stocksim
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
