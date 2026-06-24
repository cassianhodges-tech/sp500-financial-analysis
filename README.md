# S&P 500 Financial Analysis Project

This project analyses companies within the S&P 500 by sector using financial data from Yahoo Finance.

It downloads financial statement data, calculates company-level financial ratios, ranks stocks within a chosen sector and exports the results to Excel. The project also includes further analysis using insider purchase data and analyst recommendations.

## What the project does

The programme allows a user to select a sector, such as Real Estate, Technology or Financial Services. It then analyses the stocks in that sector and calculates a range of financial metrics.

The main financial metrics include:

* Gross profit margin
* Operating profit margin
* Net profit margin
* Return on assets
* Return on equity
* Free cash flow to equity
* Debt-to-equity
* Quick ratio
* Cash ratio

The project then ranks stocks using a cumulative scoring model. Stronger-performing stocks receive lower ranking points, allowing the programme to produce a final ranked list for the chosen sector.

## Additional analysis

After the initial financial ranking, the project performs further analysis on the top-ranked stocks using:

* Insider purchase activity
* Analyst recommendation data

This provides an additional view beyond the core financial statement ratios.

## Excel export and visualisation

The project exports the cleaned financial metric tables into an Excel workbook, with separate sheets for each metric. The Excel file is generated when the script is run and is not included in this repository.

The project also includes early-stage matplotlib functionality to visualise selected financial metrics. This is still being developed, but it shows how the analysis can be extended beyond tables into charts.

## Tools used

* Python
* pandas
* numpy
* yfinance
* matplotlib
* openpyxl

## Project structure

The repository contains the following main files:

* `sp500_financial_analysis.py`
  This is the main analysis script. It downloads financial data from Yahoo Finance, organises income statement, balance sheet and cash flow data into pandas DataFrames, calculates financial ratios, ranks companies within a selected S&P 500, consdiers analyst recommendations and inside share selling, with optional excel and matplotlib visualisation

* `sample_stock_data.py`
  This file creates a sample financial statement DataFrame using the same structure as the main yfinance financial data. It acts as a template to help keep the DataFrame format consistent when combining financial statements across companies.

* `requirements.txt`
  Lists the Python packages required to run the project.

* `.gitignore`
  Excludes local files such as virtual environments, test files, cached Python files and generated Excel outputs from the repository.

* `README.md`
  Provides an overview of the project, how it works and the tools used.

## Why I built this

I built this project to apply Python to financial analysis in a practical way. It allowed me to work with real company financial data, practise pandas DataFrame manipulation, calculate financial ratios and develop a simple investment-style ranking model.

The project also helped me practise handling incomplete financial data, exporting results to Excel, building early visualisations and structuring a larger Python script using classes.

## Data source note

This project uses Yahoo Finance data through the `yfinance` package. Data availability can vary by ticker, and repeated requests may occasionally trigger rate limits. If this happens, wait before rerunning the script or test with a smaller number of tickers.

## Disclaimer

This project is for educational purposes only and should not be treated as investment advice.

