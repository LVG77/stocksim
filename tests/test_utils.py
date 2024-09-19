import pytest
import numpy as np
import pandas as pd
from stocksim.utils import run_simulation, ReturnsDistribution

@pytest.fixture
def sample_data():
    return pd.DataFrame({'Close': [10, 10.5, 11, 10.8, 11.2, 11.5]})

def test_run_simulation_bootstrap(sample_data):
    price_paths = run_simulation(sample_data, ReturnsDistribution.bootstrap, 10, 100)
    assert price_paths.shape == (11, 100)
    assert np.all(price_paths[0, :] == sample_data['Close'].iloc[-1])

def test_run_simulation_normal(sample_data):
    price_paths = run_simulation(sample_data, ReturnsDistribution.normal, 10, 100)
    assert price_paths.shape == (11, 100)
    assert np.all(price_paths[0, :] == sample_data['Close'].iloc[-1])

def test_run_simulation_invalid_returns_dist(sample_data):
    with pytest.raises(AttributeError):
        run_simulation(sample_data, ReturnsDistribution.invalid, 10, 100)