# S&P 500 Financial Analysis Project

This Python project analyses companies within the S&P 500 by sector using financial data from Yahoo Finance. The aim of the project is to compare firms within the same sector using a range of financial metrics and produce a ranked output based on their relative performance.

## Overview

The project groups S&P 500 companies into sectors, allows a sector to be selected, then downloads quarterly financial data for each company in that sector. It uses income statement, balance sheet and cash flow data to calculate several financial ratios and measures.

The project then ranks companies across the selected metrics using a cumulative scoring model. Lower cumulative scores indicate stronger relative performance across the measures used.

## Metrics Included

The project calculates and compares companies using:

* Gross profit margin
* Operating profit margin
* Net profit margin
* Return on assets
* Return on equity
* Free cash flow to equity
* Debt-to-equity ratio
* Quick ratio

## Tools Used

* Python
* yfinance
* pandas
* numpy
* PyCharm

## Why I Built This

I built this project to apply Python to financial analysis and develop a more practical understanding of how company data can be used to compare businesses. I wanted to move beyond theory and work directly with financial statement data, ratios and ranking logic.

The project also helped me develop my ability to work with larger datasets, handle missing financial information, and structure outputs in a way that supports investment-style analysis.

## How It Works

1. A sector is selected from the S&P 500 sector dictionary.
2. The script downloads quarterly financial data for each company in that sector.
3. Income statement, balance sheet and cash flow data are combined into a structured DataFrame.
4. Financial ratios are calculated for each company where data is available.
5. Companies are ranked for each metric.
6. A cumulative scoring model is used to identify the strongest companies within the selected sector.

## Notes

This project is intended as a personal learning project and portfolio piece. It is not investment advice. The ranking model is simplified and designed to demonstrate data analysis, financial ratio calculation and Python programming skills.

## Future Improvements

Potential improvements include:

* Refactoring repeated ratio calculations into reusable functions
* Adding charts and visualisations
* Exporting final rankings to Excel or CSV
* Creating a cleaner user input system for sector selection
* Improving error handling where Yahoo Finance data is missing
* Expanding the scoring model to include valuation metrics
