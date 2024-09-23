import pytest
import pandas as pd
from typer.testing import CliRunner
from stocksim.cli import app
import yfinance as yf

@pytest.fixture
def mock_yfinance(monkeypatch):
    stock_data = pd.DataFrame({'Close': [10, 10.5, 11, 10.8, 11.2, 11.5]})
    monkeypatch.setattr('yfinance.download', lambda *args, **kwargs: stock_data)


def test_app(mock_yfinance):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(app, ['--ticker', 'AAPL', '--target-price', '10.0', '--days', '5', '--runs', '10'])
        assert result.exit_code == 0
        assert result.output.startswith("Monte Carlo simulation results for AAPL")
        assert "Number of simulations: 10" in result.output
        assert "Probability of price above target: " in result.output
        assert "Probability of ever dipping below" not in result.output
