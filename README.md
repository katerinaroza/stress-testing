# Portfolio Stress Testing App

This is a Streamlit-based tool to simulate the impact of various stress testing scenarios on an uploaded investment portfolio. The app allows users to apply different types of shocks to portfolio instruments and visualize the resulting P&L impact.

## Features

- Upload an Excel file with instrument-level portfolio data
- Apply different stress scenarios:
  - Specified shocks per instrument
  - Implied shocks based on volatility
  - Named historical or thematic scenarios
- Calculates shocked prices and resulting profit/loss
- Generates bar charts of P&L impact by instrument
- Option to download results as an Excel file

## Input Format

The uploaded Excel file must include the following columns:

- `Instrument`
- `Price`
- `Quantity`

For the "Implied Shocks Scenario", an additional `Volatility` column is required.

## Example Input

```
Instrument | Price | Quantity | Volatility
AAPL       | 190   | 50       | 0.25
MSFT       | 330   | 40       | 0.18
GOOG       | 2700  | 10       | 0.22
```

A sample file (`sample_portfolio.xlsx`) is included.

## Getting Started

### Install requirements

```bash
pip install streamlit pandas plotly numpy openpyxl
```

### Run the app

```bash
streamlit run app.py
```

## Files

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit app |
| `sample_portfolio.xlsx` | Sample portfolio for testing |
| `requirements.txt` | Dependency list |
| `README.md` | Project overview |

## Author

Katerina Roza  
[Email](mailto:katerinaroza@outlook.com)