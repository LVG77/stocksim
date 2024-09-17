# stocksim

[![PyPI](https://img.shields.io/pypi/v/stocksim.svg)](https://pypi.org/project/stocksim/)
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

For help, run:
```bash
stocksim --help
```
You can also use:
```bash
python -m stocksim --help
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
