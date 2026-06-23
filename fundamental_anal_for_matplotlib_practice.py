"""
S&P 500 Financial Analysis Project

This project analyses companies within the S&P 500 by sector using financial data from Yahoo Finance.

The script:

* Groups S&P 500 companies by sector
* Downloads quarterly income statement, balance sheet and cash flow data using yfinance
* Combines financial statement data into structured pandas DataFrames
* Calculates financial metrics including profit margins, ROA, ROE, FCFE, debt-to-equity and quick ratio
* Ranks companies within a selected sector using a cumulative scoring model
* Flags companies where financial data is missing or incomplete

This was built as a personal Python and financial analysis project to practise working with real company data, financial ratios and investment-style screening logic.

Note: This project is for educational purposes only and is not investment advice.
"""

import yfinance as yf
import pandas as pd
import numpy as np


#show all columns and rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

# all stocks in S&P 500
stock_list = ["A", "AAPL", "ABBV", "ABC", "ABMD", "ABT", "ACGL", "ACN", "ADBE", "ADI",
              "ADM", "ADP", "ADSK", "AEE", "AEP", "AES", "AFL", "AIG", "AIZ", "AJG",
              "AKAM", "ALB", "ALGN", "ALK", "ALL", "ALLE", "AMAT", "AMCR", "AMD", "AME",
              "AMGN", "AMP", "AMT", "AMZN", "ANET", "ANSS", "AON", "AOS", "APA", "APD",
              "APH", "APTV", "ARE", "ATO", "ATR", "ATVI", "AVB", "AVGO", "AVY", "AWK",
              "AXP", "AZO", "BA", "BAC", "BALL", "BAX", "BBWI", "BBY", "BDX", "BEN",
              "BF.B", "BIIB", "BIO", "BK", "BKNG", "BKR", "BLK", "BLL", "BMY", "BR",
              "BRK.B", "BRO", "BSX", "BWA", "BX", "C", "CAG", "CAH", "CARR", "CAT",
              "CB", "CBOE", "CBRE", "CCI", "CCL", "CDAY", "CDNS", "CDW", "CE", "CEG",
              "CF", "CFG", "CHD", "CHRW", "CHTR", "CI", "CINF", "CL", "CLX", "CMA",
              "CMCSA", "CME", "CMG", "CMS", "CNC", "CNP", "COF", "COO", "COP", "COST",
              "CPB", "CPRT", "CPT", "CRL", "CRM", "CSCO", "CSGP", "CSX", "CTAS", "CTLT",
              "CTRA", "CTSH", "CTVA", "CTXS", "CVS", "CVX", "CZR", "D", "DAL", "DD",
              "DE", "DFS", "DG", "DGX", "DHI", "DHR", "DIS", "DISCA", "DISCK", "DISH",
              "DLR", "DLTR", "DOV", "DOW", "DPZ", "DRE", "DRI", "DTE", "DUK", "DVA",
              "DVN", "DXCM", "EA", "EBAY", "ECL", "ED", "EFX", "EIX", "EL", "EMN",
              "EMR", "ENPH", "EOG", "EPAM", "EQIX", "EQR", "ES", "ESS", "ETN", "ETR",
              "ETSY", "EVRG", "EW", "EXC", "EXPD", "EXPE", "EXR", "F", "FANG", "FAST",
              "FBHS", "FCX", "FDS", "FDX", "FE", "FFIV", "FIS", "FISV", "FITB", "FLIR",
              "FLS", "FLT", "FMC", "FOX", "FOXA", "FRC", "FRT", "FTNT", "FTV", "GD",
              "GE", "GILD", "GIS", "GL", "GLW", "GM", "GNRC", "GOOG", "GOOGL", "GPC",
              "GPN", "GRMN", "GS", "GWW", "HAL", "HAS", "HBAN", "HBI", "HCA", "HES",
              "HFC", "HIG", "HII", "HLT", "HOLX", "HON", "HPE", "HPQ", "HRL", "HSIC",
              "HST", "HSY", "HUM", "HWM", "IBM", "ICE", "IDXX", "IEX", "IFF", "ILMN",
              "INCY", "INFO", "INTC", "INTU", "IP", "IPG", "IPGP", "IQV", "IR", "IRM",
              "ISRG", "IT", "ITW", "IVZ", "J", "JBHT", "JCI", "JKHY", "JNJ", "JNPR",
              "JPM", "K", "KEY", "KEYS", "KHC", "KIM", "KLAC", "KMB", "KMI", "KMX",
              "KO", "KR", "KSU", "L", "LDOS", "LEG", "LEN", "LH", "LHX", "LIN", "LKQ",
              "LLY", "LMT", "LNC", "LNT", "LOW", "LRCX", "LUMN", "LUV", "LVS", "LW",
              "LYB", "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", "MCK", "MCO",
              "MDLZ", "MDT", "MET", "MGM", "MHK", "MKC", "MKTX", "MLM", "MMC", "MMM",
              "MNST", "MO", "MOS", "MPC", "MPWR", "MRK", "MRO", "MS", "MSCI", "MSFT",
              "MSI", "MTB", "MTD", "MU", "NCLH", "NDAQ", "NDSN", "NEE", "NEM", "NFLX",
              "NI", "NKE", "NLOK", "NOC", "NOW", "NRG", "NSC", "NTAP", "NTRS", "NUE",
              "NVDA", "NVR", "NXPI", "O", "ODFL", "OGN", "OKE", "OMC", "ORCL", "ORLY",
              "OTIS", "OXY", "PARA", "PAYC", "PAYX", "PBCT", "PCAR", "PEAK", "PEG",
              "PENN", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PKI",
              "PLD", "PM", "PNC", "PNR", "PNW", "POOL", "PPG", "PPL", "PRGO", "PRU",
              "PSA", "PSX", "PTC", "PVH", "PWR", "PXD", "PYPL", "QCOM", "QRVO", "RCL",
              "RE", "REG", "REGN", "RF", "RHI", "RJF", "RL", "RMD", "ROK", "ROL", "ROP",
              "ROST", "RSG", "RTX", "SBAC", "SBUX", "SCHW", "SEE", "SHW", "SIVB", "SJM",
              "SLB", "SNA", "SNPS", "SO", "SPG", "SPGI", "SRE", "STE", "STT", "STX",
              "STZ", "SWK", "SWKS", "SYF", "SYK", "SYY", "T", "TAP", "TDG", "TDY",
              "TEL", "TER", "TFC", "TFX", "TGT", "TJX", "TMO", "TMUS", "TPR", "TRMB",
              "TROW", "TRV", "TSCO", "TSLA", "TSN", "TT", "TTWO", "TWTR", "TXN", "TXT",
              "TYL", "UA", "UAA", "UAL", "UDR", "UHS", "ULTA", "UNH", "UNM", "UNP",
              "UPS", "URI", "USB", "V", "VFC", "VIAC", "VLO", "VMC", "VNO", "VRSK",
              "VRSN", "VRTX", "VTR", "VZ", "WAB", "WAT", "WBA", "WDC", "WEC", "WELL",
              "WFC", "WHR", "WLTW", "WM", "WMB", "WMT", "WRB", "WRK", "WST", "WU",
              "WY", "WYNN", "XEL", "XLNX", "XOM", "XRAY", "XYL", "YUM", "ZBH", "ZBRA",
              "ZION", "ZTS"
              ]
sector_stocks = {'Healthcare': ['A', 'ABBV', 'ABT', 'ALGN', 'AMGN', 'ATR', 'BAX', 'BDX', 'BIIB', 'BIO', 'BMY', 'BSX', 'CAH', 'CI', 'CNC', 'COO', 'CRL', 'CTLT', 'CVS', 'DGX', 'DHR', 'DVA', 'DXCM', 'EW', 'GILD', 'HCA', 'HOLX', 'HSIC', 'HUM', 'IDXX', 'ILMN', 'INCY', 'IQV', 'ISRG', 'JNJ', 'LH', 'LLY', 'MCK', 'MDT', 'MRK', 'MTD', 'OGN', 'PFE', 'PRGO', 'REGN', 'RMD', 'STE', 'SYK', 'TFX', 'TMO', 'UHS', 'UNH', 'VRTX', 'WAT', 'WBA', 'WST', 'XRAY', 'ZBH', 'ZTS'],
                 'Technology': ['AAPL', 'ACN', 'ADBE', 'ADI', 'ADSK', 'AKAM', 'AMAT', 'AMD', 'ANET', 'ANSS', 'APH', 'AVGO', 'BR', 'CDNS', 'CDW', 'CRM', 'CSCO', 'CTSH', 'ENPH', 'EPAM', 'FFIV', 'FIS', 'FTNT', 'FTV', 'GLW', 'GRMN', 'HPE', 'HPQ', 'IBM', 'INTC', 'INTU', 'IPGP', 'IT', 'JKHY', 'JNPR', 'KEYS', 'KLAC', 'LDOS', 'LRCX', 'MCHP', 'MPWR', 'MSFT', 'MSI', 'MU', 'NOW', 'NTAP', 'NVDA', 'NXPI', 'ORCL', 'PAYC', 'PTC', 'QCOM', 'QRVO', 'ROP', 'SNPS', 'STX', 'SWKS', 'TDY', 'TEL', 'TER', 'TRMB', 'TXN', 'TYL', 'VRSN', 'WDC', 'ZBRA'],
                 'Financial Services': ['ACGL', 'AFL', 'AIG', 'AIZ', 'AJG', 'ALL', 'AMP', 'AON', 'AXP', 'BAC', 'BEN', 'BK', 'BLK', 'BRO', 'BX', 'C', 'CB', 'CBOE', 'CFG', 'CINF', 'CMA', 'CME', 'COF', 'DFS', 'FDS', 'FITB', 'GL', 'GS', 'HBAN', 'HIG', 'ICE', 'IVZ', 'JPM', 'KEY', 'L', 'LNC', 'MA', 'MCO', 'MET', 'MKTX', 'MMC', 'MS', 'MSCI', 'MTB', 'NDAQ', 'NTRS', 'PFG', 'PGR', 'PNC', 'PRU', 'PYPL', 'RF', 'RJF', 'SCHW', 'SPGI', 'STT', 'SYF', 'TFC', 'TROW', 'TRV', 'UNM', 'USB', 'V', 'WFC', 'WRB', 'WU', 'ZION'],
                 'Consumer Defensive': ['ADM', 'CAG', 'CHD', 'CL', 'CLX', 'COST', 'CPB', 'DG', 'DLTR', 'EL', 'GIS', 'HRL', 'HSY', 'K', 'KHC', 'KMB', 'KO', 'KR', 'LW', 'MDLZ', 'MKC', 'MNST', 'MO', 'PEP', 'PG', 'PM', 'SJM', 'STZ', 'SYY', 'TAP', 'TGT', 'TSN', 'WMT'],
                 'Industrials': ['ADP', 'ALK', 'ALLE', 'AME', 'AOS', 'BA', 'CARR', 'CAT', 'CHRW', 'CPRT', 'CSX', 'CTAS', 'DAL', 'DE', 'DOV', 'EFX', 'EMR', 'ETN', 'EXPD', 'FAST', 'FDX', 'FLS', 'GD', 'GE', 'GNRC', 'GPN', 'GWW', 'HII', 'HON', 'HWM', 'IEX', 'IR', 'ITW', 'J', 'JBHT', 'JCI', 'LHX', 'LMT', 'LUV', 'MAS', 'MMM', 'NDSN', 'NOC', 'NSC', 'ODFL', 'OTIS', 'PAYX', 'PCAR', 'PH', 'PNR', 'POOL', 'PWR', 'RHI', 'ROK', 'RSG', 'RTX', 'SNA', 'SWK', 'TDG', 'TT', 'TXT', 'UAL', 'UNP', 'UPS', 'URI', 'VRSK', 'WAB', 'WM', 'XYL'],
                 'Utilities': ['AEE', 'AEP', 'AES', 'ATO', 'AWK', 'CEG', 'CMS', 'CNP', 'D', 'DTE', 'DUK', 'ED', 'EIX', 'ES', 'ETR', 'EVRG', 'EXC', 'FE', 'LNT', 'NEE', 'NI', 'NRG', 'PEG', 'PNW', 'PPL', 'SO', 'SRE', 'WEC', 'XEL'],
                 'Basic Materials': ['ALB', 'APD', 'CE', 'CF', 'CTVA', 'DD', 'DOW', 'ECL', 'EMN', 'FCX', 'FMC', 'IFF', 'LIN', 'LYB', 'MLM', 'MOS', 'NEM', 'NUE', 'PPG', 'SHW', 'VMC'],
                 'Consumer Cyclical': ['AMCR', 'AMZN', 'APTV', 'AVY', 'AZO', 'BALL', 'BBWI', 'BBY', 'BKNG', 'BWA', 'CCL', 'CMG', 'CZR', 'DHI', 'DPZ', 'DRI', 'EBAY', 'ETSY', 'EXPE', 'F', 'GM', 'GPC', 'HAS', 'HBI', 'HLT', 'IP', 'KMX', 'LEG', 'LEN', 'LKQ', 'LOW', 'LVS', 'MAR', 'MCD', 'MGM', 'MHK', 'NCLH', 'NKE', 'NVR', 'ORLY', 'PENN', 'PHM', 'PKG', 'PVH', 'RCL', 'RL', 'ROL', 'ROST', 'SBUX', 'SEE', 'TJX', 'TPR', 'TSCO', 'TSLA', 'UA', 'UAA', 'ULTA', 'VFC', 'WHR', 'WRK', 'WYNN', 'YUM'],
                 'Real Estate': ['AMT', 'ARE', 'AVB', 'CBRE', 'CCI', 'CPT', 'CSGP', 'DLR', 'EQIX', 'EQR', 'ESS', 'EXR', 'FRT', 'HST', 'IRM', 'KIM', 'MAA', 'O', 'PLD', 'PSA', 'REG', 'SBAC', 'SPG', 'UDR', 'VNO', 'VTR', 'WELL', 'WY'],
                 'Energy': ['APA', 'BKR', 'COP', 'CTRA', 'CVX', 'DVN', 'EOG', 'FANG', 'HAL', 'HES', 'KMI', 'MPC', 'MRO', 'OKE', 'OXY', 'PSX', 'SLB', 'VLO', 'WMB', 'XOM'],
                 'Communication Services': ['CHTR', 'CMCSA', 'DIS', 'EA', 'FOX', 'FOXA', 'GOOG', 'GOOGL', 'IPG', 'LUMN', 'LYV', 'NFLX', 'OMC', 'PARA', 'T', 'TMUS', 'TTWO', 'VZ']}
no_sector_stocks = {'No Sector': ['ABC', 'ABMD', 'ATVI', 'BF.B', 'BLL', 'BRK.B', 'CDAY', 'CTXS', 'DISCA', 'DISCK', 'DISH', 'DRE', 'FBHS', 'FISV', 'FLIR', 'FLT', 'FRC', 'HFC', 'INFO', 'KSU', 'NLOK', 'PBCT', 'PEAK', 'PKI', 'PXD', 'RE', 'SIVB', 'TWTR', 'VIAC', 'WLTW', 'XLNX']}


#metrics done
#Gross/operating/net profit margin  #income
#ROA                                #income + balance
#FCFE                               #cash
#quick ratio                        #balance
#ROE                                #income + balance
#debt-to-equity                     #balance


#Makes sure there is a dummy stock which all the ratios work on
# from dummy_stock import dummy_stock_df


input_sector = 'Real Estate'
stock_sector_options = ['Healthcare', 'Technology', 'Financial Services', 'Consumer Defensive', 'Industrials',
                        'Utilities', 'Basic Materials', 'Consumer Cyclical', 'Real Estate', 'Energy', 'Communication Services']
stocks_in_sector_chosen = sector_stocks[input_sector]
print('Sector chosen is', input_sector)

# stocks_Excel = [('PSA', 5), ('SPG', 14), ('EXR', 18), ('AMT', 32), ('AVB', 35),('WY', 43)]
    # [('EBAY', 37), ('NKE', 41), ('NVR', 54), ('TPR', 62), ('DHI', 67), ('LEN', 70),  ('PHM', 83),  ('BKNG', 91)]
    # [('CE', 8), ('NUE', 12), ('CF', 23)]
    # [('UNP', 41), ('LMT', 54), ('ITW', 55), ('EMR', 66), ('CSX', 73), ('DE', 77), ('ADP', 78), ('HON', 79),  ('PAYX', 81), ('CTAS', 103), ('NSC', 111)]
    # [('PG', 21), ('KO', 23), ('CL', 30), ('PM', 36), ('PEP', 39), ('HSY', 42), ('MO', 47)]
    # [('V', 12), ('MA', 14), ('SPGI', 59), ('BX', 67), ('DFS', 81), ('MCO', 83), ('BLK', 83), ('SCHW', 88), ('PYPL', 94), ('AXP', 97), ('COF', 106), ('PGR', 107),('MMC', 112)]
    # [('JNJ', 31), ('AMGN', 38), ('REGN', 48), ('VRTX', 60), ('PFE', 63), ('LLY', 67), ('MRK', 71), ('ZTS', 80), ('HOLX', 91), ('GILD', 98)]
    #Tech [('AAPL', 18), ('MSFT', 26), ('NVDA', 28), ('TXN', 35), ('QCOM', 43), ('KLAC', 46), ('AVGO', 46), ('ADBE', 52), ('AMAT', 53), ('LRCX', 57), ('CSCO', 69), ('ORCL', 69), ('INTU', 109), ('SWKS', 119)]


# stocks_excell = []
# for (stock,v)  in stocks_Excel:
#     stocks_excell.append(stock)
# print(stocks_excell)
data_frame_list = []
stocks_done = 0
stock_no_info = 0
stock_no_info_on_financials_set = set()
periods = [0,1,2,3,4,5,6]     #for shorter table for all metrics
#Getting all financials (balance, income and cash flow)
for stock in stocks_in_sector_chosen:
    ticker = yf.Ticker(stock)

    #get cash flow
    cash_flow = ticker.quarterly_cash_flow#for cash flow statement (years as columns, cash metrics as axis)
    cash_flow_index = cash_flow.index   #get cash metrics
    cash_level_label = f'{stock.upper()}'
    Cash = pd.Index(['Cash Flow' for u in range(len(cash_flow_index))])
    Cash_level = pd.Index([cash_level_label for i in range(len(cash_flow_index))])
    cash_components_level = pd.Index(cash_flow_index)   #already in index form, this line isnt needed
    #create multi-index of cash and cash titles
    arrays = [
        np.array(Cash),  #cash
        np.array(Cash_level),   #stock
        np.array(cash_components_level)  #cash metric
    ]
    mlt = pd.MultiIndex.from_arrays(arrays, names=['Topic','Company','Measurements'])   #creates row index of cash,stock,cash metric
    vals = [str(x) for x in cash_flow.columns.values]                                   #get dates as strings
    if vals == []:
        # print(f'No information on cash-flow for stock {stock}')
        stock_no_info_on_financials_set.add(stock)
    col_index_for_df = []
    for i in vals:
        col_index_for_df.append(i[:10])                                                  #only get year,month, day
    col_index = pd.Index(col_index_for_df, name='Year')                                  #prepare col index
    Cash_data_frame = pd.DataFrame(cash_flow.values,columns=col_index,index=mlt)         #paste all values. Now columns are slighlt adjusted and additional...
    data_frame_list.append(Cash_data_frame)                                              #info before each metric (cash,stock)

    #get income stmnt
    income_statement = ticker.quarterly_incomestmt
    Income_stmt_index = income_statement.index
    Income_stmt_label = f'{stock.upper()}'
    Income = pd.Index(['Income' for u in range(len(Income_stmt_index))])
    Income_level = pd.Index([Income_stmt_label for i in range(len(Income_stmt_index))])
    Income_components_level = pd.Index(Income_stmt_index)
    #create multi-index of income_stmt and income_stmt titles
    arrays = [
        np.array(Income),
        np.array(Income_level),
        np.array(Income_components_level)
    ]
    mlt = pd.MultiIndex.from_arrays(arrays, names=['Topic','Company','Measurements'])
    vals = [str(x) for x in income_statement.columns.values]
    if vals == []:
        # print(f'No information on income statement for stock {stock}')
        stock_no_info_on_financials_set.add(stock)
        # stock_no_info += 1
        # print(f'No info on {stock_no_info} stocks')
    col_index_for_df = []
    for i in vals:
        col_index_for_df.append(i[:10])
    col_index = pd.Index(col_index_for_df, name='Year')
    Income_stmt_data_frame = pd.DataFrame(income_statement.values,columns=col_index,index=mlt)
    data_frame_list.append(Income_stmt_data_frame)


    #get balance sheet
    Balance_sheet = ticker.quarterly_balance_sheet
    Balance_sheet_index = Balance_sheet.index
    Balance_sheet_label = f'{stock.upper()}'
    Balance = pd.Index(['Balance' for u in range(len(Balance_sheet_index))])
    Balance_level = pd.Index([Balance_sheet_label for i in range(len(Balance_sheet_index))])
    Balance_components_level = pd.Index(Balance_sheet_index)
    #create multi-index of cash and cash titles
    arrays = [
        np.array(Balance),
        np.array(Balance_level),
        np.array(Balance_components_level)
    ]
    mlt = pd.MultiIndex.from_arrays(arrays, names=['Topic','Company','Measurements'])
    vals = [str(x) for x in Balance_sheet.columns.values]
    if vals == []:
        # print(f'No information on Balance sheet for stock {stock}')
        stock_no_info_on_financials_set.add(stock)
    col_index_for_df = []
    for i in vals:
        col_index_for_df.append(i[:10])
    col_index = pd.Index(col_index_for_df, name='Year')
    Balance_sheet_data_frame = pd.DataFrame(Balance_sheet.values,columns=col_index,index=mlt)
    data_frame_list.append(Balance_sheet_data_frame)


    #count-down of stocks done
    stocks_done +=1
    print(stocks_done, stock)

#Create a combined data frame of cash,income and balance
# data_frame_list.append(dummy_stock_df)
data_frame_combined = pd.concat(data_frame_list)
data_frame_combined = data_frame_combined.sort_index(level='Topic')  #Group by balance,income and cash

#Sort column years
data_frame_combined = data_frame_combined.sort_index(axis=1, ascending=False)
# print(data_frame_combined)
# Output to txt file so when working with large data it is all shown
# (issue with all data showing on intellegi run pane when large)
with open("outputt_fund.txt", 'w') as data_frame_output:
    print(data_frame_combined,file=data_frame_output)


# Calculating Gross profit margin
stock_no_info_on_Total_Revenue_and_Gross_profit = set()
gathering_statistics = data_frame_combined.loc[('Income',slice(None), ('Gross Profit', 'Total Revenue')),:].copy()
# print(gathering_statistics)
print('*' * 50)
# print(gathering_statistics)

list_of_columns = list(gathering_statistics.columns)  #get the dates for the values
Stocks_in_df = set(gathering_statistics.index.get_level_values(1)) #get the stocks involved for the values
Stocks_in_df = list(Stocks_in_df)
for stock in data_frame_combined.index.get_level_values(1):
    if stock not in Stocks_in_df:
        stock_no_info_on_Total_Revenue_and_Gross_profit.add(stock)

stock_results = []
list_every_stock_result = []
stock_no_info_on_Gross_profit_or_revenue_set = set()
for stock in Stocks_in_df:
    # print('*' * 20, 'NEW STOCK','*' * 20 )
    stock_results = []
    for column in list_of_columns:
        # print(stock,column)
        try:
            Gross_profit_figure = gathering_statistics.loc[('Income', stock, 'Gross Profit'), (column)] #get profit for stock a
            # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
            Revenue_Figure = gathering_statistics.loc[('Income', stock, 'Total Revenue'), (column)] #get revenue for stock a
            # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
            Gross_profit_margin = Gross_profit_figure/Revenue_Figure
            # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
            stock_results.append(Gross_profit_margin)
            # print('*' * 100)
        except Exception:
            # print(f'{stock} is missing Gross profit or revenue value')
            stock_no_info_on_Gross_profit_or_revenue_set.add(stock)
            continue

    mlt = pd.MultiIndex.from_arrays(
        [np.array([stock]), np.array(['Gross Profit margin'])] #row index of stock then GPM value
    )
    if stock_results != []:  #check stock actually has readable contents by Yahoo
        # print(mlt)
        # print(stock_results)
        i = [[x for x in stock_results]]
        # print(i)
        gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
        # gp_df = pd.DataFrame(stock_results, index=mlt, columns=gathering_statistics.columns[:2])
        # print(gp_df)
        print()
        list_every_stock_result.append(gp_df)

data_frame_combined_gross_profit_margin = pd.concat(list_every_stock_result)


data_frame_combined_gross_profit_margin_last_3_periods = data_frame_combined_gross_profit_margin.iloc[:,periods]
Df_Gross_profit_table_mean_calculation_last_3_periods = data_frame_combined_gross_profit_margin_last_3_periods.mean(axis=1)
data_frame_combined_gross_profit_margin_last_3_periods.insert(0,f'Mean Gross Profit margin last {len(periods)} periods',Df_Gross_profit_table_mean_calculation_last_3_periods)
data_frame_combined_gross_profit_margin_last_3_periods = data_frame_combined_gross_profit_margin_last_3_periods.sort_values(by=(f'Mean Gross Profit margin last {len(periods)} periods',), axis=0, ascending=False)
print(data_frame_combined_gross_profit_margin_last_3_periods)

Df_Gross_profit_table_mean_calculation_whole_period = data_frame_combined_gross_profit_margin.mean(axis=1)
data_frame_combined_gross_profit_margin.insert(0, 'Mean Gross Profit margin', Df_Gross_profit_table_mean_calculation_whole_period)
data_frame_combined_gross_profit_margin = data_frame_combined_gross_profit_margin.sort_values(by=('Mean Gross Profit margin',), axis=0, ascending=False)
print(data_frame_combined_gross_profit_margin)
print(len(data_frame_combined_gross_profit_margin))

Complete_rankings_of_stocks = {}
Stocks_in_df_for_complete_ranking_of_stocks = list(data_frame_combined_gross_profit_margin.index.get_level_values(0))  #get the stocks involved
points = 0
for stock in Stocks_in_df_for_complete_ranking_of_stocks:
    try:
        a = Complete_rankings_of_stocks[stock]
        Complete_rankings_of_stocks[stock] += points
        # print(f'{stock} gained {points} points')
    except Exception:
        Complete_rankings_of_stocks[stock] = points
        # print(f'{stock} has {points} points')
    points += 1


# a = data_frame_combined_gross_profit_margin_last_3_periods.index.get_level_values(0)
b = data_frame_combined_gross_profit_margin.index.get_level_values(0)
# print('*****last n periods******')
# for i in a:
#     print(i)
# print('*****last n periods******')
# print()
print('*****overall******')
for i in b:
    print(i)
print('*****overall******')








# Calculating operating profit margin
stock_no_info_on_Total_Revenue_and_Operating_profit = set()
gathering_statistics = data_frame_combined.loc[('Income',slice(None), ('Operating Income', 'Total Revenue')),:].copy()
print('*' * 50)

list_of_columns = list(gathering_statistics.columns)  #get the dates
Stocks_in_df = set(gathering_statistics.index.get_level_values(1)) #get the stocks involved
Stocks_in_df = list(Stocks_in_df)
for stock in data_frame_combined.index.get_level_values(1):
    if stock not in Stocks_in_df:
        stock_no_info_on_Total_Revenue_and_Operating_profit.add(stock)


stock_results = []
list_every_stock_result = []
stock_no_info_on_operating_profit_or_revenue_set = set()
for stock in Stocks_in_df:
    # print('*' * 20, 'NEW STOCK','*' * 20 )
    stock_results = []
    for column in list_of_columns:
        # print(stock,column)
        try:
            Operating_Income_figure = gathering_statistics.loc[('Income', stock, 'Operating Income'), (column)] #get operating income for stock a
            # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
            Revenue_Figure = gathering_statistics.loc[('Income', stock, 'Total Revenue'), (column)] #get revenue for stock a
            # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
            Operating_Income_margin = Operating_Income_figure/Revenue_Figure
            # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
            stock_results.append(Operating_Income_margin)
            # print('*' * 100)
        except Exception:
            # print(f'{stock} is missing Operating profit or revenue value')
            stock_no_info_on_operating_profit_or_revenue_set.add(stock)
            continue

    mlt = pd.MultiIndex.from_arrays(
        [np.array([stock]), np.array(['Operating profit margin'])] #row index of stock then GPM value
    )
    if stock_results != []:  #check stock actually has readable contents by Yahoo
        # print(mlt)
        # print(stock_results)
        i = [[x for x in stock_results]]
        # print(i)
        gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
        # gp_df = pd.DataFrame(stock_results, index=mlt, columns=gathering_statistics.columns[:2])
        # print(gp_df)
        print()
        list_every_stock_result.append(gp_df)

data_frame_combined_Operating_income_margin = pd.concat(list_every_stock_result)


data_frame_combined_operating_income_margin_last_3_periods = data_frame_combined_Operating_income_margin.iloc[:,periods]
Df_Operating_income_table_mean_calculation_last_3_periods = data_frame_combined_operating_income_margin_last_3_periods.mean(axis=1)
data_frame_combined_operating_income_margin_last_3_periods.insert(0,f'Operating Profit margin last {len(periods)} periods', Df_Operating_income_table_mean_calculation_last_3_periods)
data_frame_combined_Operating_income_margin_last_3_periods = data_frame_combined_operating_income_margin_last_3_periods.sort_values(by=(f'Operating Profit margin last {len(periods)} periods',), axis=0, ascending=False)
print(data_frame_combined_Operating_income_margin_last_3_periods)

Df_Operating_Income_table_mean_calculation_whole_period = data_frame_combined_Operating_income_margin.mean(axis=1)
data_frame_combined_Operating_income_margin.insert(0, 'Operating Profit margin', Df_Operating_Income_table_mean_calculation_whole_period)
data_frame_combined_Operating_income_margin = data_frame_combined_Operating_income_margin.sort_values(by=('Operating Profit margin',), axis=0, ascending=False)
print(data_frame_combined_Operating_income_margin)
print(len(data_frame_combined_Operating_income_margin))

Stocks_in_df_for_complete_ranking_of_stocks = list(data_frame_combined_Operating_income_margin.index.get_level_values(0))  #get the stocks involved
points = 0
for stock in Stocks_in_df_for_complete_ranking_of_stocks:
    try:
        a = Complete_rankings_of_stocks[stock]
        Complete_rankings_of_stocks[stock] += points
        # print(f'{stock} gained {points} points')
    except Exception:
        Complete_rankings_of_stocks[stock] = points
        # print(f'stock has {points} points')
    points += 1
a = data_frame_combined_operating_income_margin_last_3_periods.index.get_level_values(0)
b = data_frame_combined_Operating_income_margin.index.get_level_values(0)
# print('*****last n periods******')
# for i in a:
#     print(i)
# print('*****last n periods******')
# print()
print('*****overall******')
for i in b:
    print(i)
print('*****overall******')







#Calculating net profit margin
stock_no_info_on_Total_Revenue_and_Net_Income = set()
gathering_statistics = data_frame_combined.loc[('Income',slice(None), ('Net Income', 'Total Revenue')),:].copy()
print('*' * 50)

list_of_columns = list(gathering_statistics.columns)  #get the dates
Stocks_in_df = set(gathering_statistics.index.get_level_values(1)) #get the stocks involved
Stocks_in_df = list(Stocks_in_df)
for stock in data_frame_combined.index.get_level_values(1):
    if stock not in Stocks_in_df:
        stock_no_info_on_Total_Revenue_and_Net_Income.add(stock)

stock_results = []
list_every_stock_result = []
stock_no_info_on_net_profit_or_revenue_set = set()
for stock in Stocks_in_df:
    # print('*' * 20, 'NEW STOCK','*' * 20 )
    stock_results = []
    for column in list_of_columns:
        # print(stock,column)
        try:
            Net_profit_figure = gathering_statistics.loc[('Income', stock, 'Net Income'), (column)] #get Net profit for stock a
            # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
            Revenue_Figure = gathering_statistics.loc[('Income', stock, 'Total Revenue'), (column)] #get revenue for stock a
            # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
            Net_profit_margin = Net_profit_figure/Revenue_Figure
            # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
            stock_results.append(Net_profit_margin)
            # print('*' * 100)
        except Exception:
            # print(f'{stock} is missing Net income or revenue value')
            stock_no_info_on_net_profit_or_revenue_set.add(stock)
            continue

    mlt = pd.MultiIndex.from_arrays(
        [np.array([stock]), np.array(['Net profit margin'])] #row index of stock then GPM value
    )
    if stock_results != []:  #check stock actually has readable contents by Yahoo
        # print(mlt)
        # print(stock_results)
        i = [[x for x in stock_results]]
        # print(i)
        gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
        # gp_df = pd.DataFrame(stock_results, index=mlt, columns=gathering_statistics.columns[:2])
        # print(gp_df)
        print()
        list_every_stock_result.append(gp_df)

data_frame_combined_Net_profit_margin = pd.concat(list_every_stock_result)


data_frame_combined_Net_profit_margin_last_n_periods = data_frame_combined_Net_profit_margin.iloc[:,periods]
Df_Net_Profit__margin_table_mean_calculation_last_n_periods = data_frame_combined_Net_profit_margin_last_n_periods.mean(axis=1)
data_frame_combined_Net_profit_margin_last_n_periods.insert(0,f'Net Profit margin last {len(periods)} periods', Df_Net_Profit__margin_table_mean_calculation_last_n_periods)
data_frame_combined_Net_profit_margin_last_n_periods = data_frame_combined_Net_profit_margin_last_n_periods.sort_values(by=(f'Net Profit margin last {len(periods)} periods',), axis=0, ascending=False)
print(data_frame_combined_Net_profit_margin_last_n_periods)

Df_Net_Profit_margin_table_mean_calculation_whole_period = data_frame_combined_Net_profit_margin.mean(axis=1)
data_frame_combined_Net_profit_margin.insert(0, 'Net Profit margin Average', Df_Net_Profit_margin_table_mean_calculation_whole_period)
data_frame_combined_Net_profit_margin = data_frame_combined_Net_profit_margin.sort_values(by=('Net Profit margin Average',), axis=0, ascending=False)
print(data_frame_combined_Net_profit_margin)
print(len(data_frame_combined_Net_profit_margin))

Stocks_in_df_for_complete_ranking_of_stocks = list(data_frame_combined_Net_profit_margin.index.get_level_values(0))  #get the stocks involved
points = 0
for stock in Stocks_in_df_for_complete_ranking_of_stocks:
    try:
        a = Complete_rankings_of_stocks[stock]
        Complete_rankings_of_stocks[stock] += points
        # print(f'{stock} gained {points} points')
    except Exception:
        Complete_rankings_of_stocks[stock] = points
        # print(f'stock has {points} points')
    points += 1


# a = data_frame_combined_Net_profit_margin_last_n_periods.index.get_level_values(0)
b = data_frame_combined_Net_profit_margin.index.get_level_values(0)
# print('*****last n periods******')
# for i in a:
#     print(i)
# print('*****last n periods******')
# print()
# print('*****overall******')
for i in b:
    print(i)
print('*****overall******')



#Calculating ROA
stock_no_info_on_Assets_and_Net_Profit = set()
gathering_statistics = data_frame_combined.loc[
                       (
                           ('Balance','Income'),
                           (slice(None)),
                           ('Total Assets', 'Net Income')

                       ),
                       :].copy()
print('*' * 50)

list_of_columns = list(gathering_statistics.columns)  #get the dates
Stocks_in_df = set(gathering_statistics.index.get_level_values(1)) #get the stocks involved
Stocks_in_df = list(Stocks_in_df)
for stock in data_frame_combined.index.get_level_values(1):
    if stock not in Stocks_in_df:
        stock_no_info_on_Assets_and_Net_Profit.add(stock)


stock_results = []
list_every_stock_result = []
stock_no_info_on_net_profit_or_total_assets_set = set()
for stock in Stocks_in_df:
    #print('*' * 20, 'NEW STOCK','*' * 20 )
    stock_results = []
    for column in list_of_columns:
        # print(stock,column)
        try:
            Net_profit_figure = gathering_statistics.loc[('Income', stock, 'Net Income'), (column)] #get Net profit for stock a
            # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
            Assets_Figure = gathering_statistics.loc[('Balance', stock, 'Total Assets'), (column)] #get Total assets for stock a
            # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
            ROA = Net_profit_figure/Assets_Figure
            # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
            stock_results.append(ROA)
            # print('*' * 100)
        except Exception:
            # print(f'{stock} is missing Net income or Net assets figure')
            stock_no_info_on_net_profit_or_total_assets_set.add(stock)
            continue
    #
    mlt = pd.MultiIndex.from_arrays(
        [np.array([stock]), np.array(['ROA'])] #row index of stock then GPM value
    )
    if stock_results != []:  #check stock actually has readable contents by Yahoo
        # print(mlt)
        # print(stock_results)
        i = [[x for x in stock_results]]
        # print(i)
        gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
        # gp_df = pd.DataFrame(stock_results, index=mlt, columns=gathering_statistics.columns[:2])
        # print(gp_df)
        print()
        list_every_stock_result.append(gp_df)

data_frame_combined_ROA = pd.concat(list_every_stock_result)


data_frame_combined_ROA_last_n_periods = data_frame_combined_ROA.iloc[:,periods]
Df_ROA_table_mean_calculation_last_n_periods = data_frame_combined_ROA_last_n_periods.mean(axis=1)
data_frame_combined_ROA_last_n_periods.insert(0,f'ROA last {len(periods)} periods', Df_ROA_table_mean_calculation_last_n_periods)
data_frame_combined_ROA_last_n_periods = data_frame_combined_ROA_last_n_periods.sort_values(by=(f'ROA last {len(periods)} periods',), axis=0, ascending=False)
print(data_frame_combined_ROA_last_n_periods)

Df_ROA_table_mean_calculation_whole_period = data_frame_combined_ROA.mean(axis=1)
data_frame_combined_ROA.insert(0, 'ROA Average', Df_ROA_table_mean_calculation_whole_period)
data_frame_combined_ROA = data_frame_combined_ROA.sort_values(by=('ROA Average',), axis=0, ascending=False)
print(data_frame_combined_ROA)
print(len(data_frame_combined_ROA))
#
Stocks_in_df_for_complete_ranking_of_stocks = list(data_frame_combined_ROA.index.get_level_values(0))  #get the stocks involved
points = 0
for stock in Stocks_in_df_for_complete_ranking_of_stocks:
    try:
        a = Complete_rankings_of_stocks[stock]
        Complete_rankings_of_stocks[stock] += points
        # print(f'{stock} gained {points} points')
    except Exception:
        Complete_rankings_of_stocks[stock] = points
        # print(f'stock has {points} points')
    points += 1


# a = data_frame_combined_ROA_last_n_periods.index.get_level_values(0)
b = data_frame_combined_ROA.index.get_level_values(0)
# print('*****last n periods******')
# for i in a:
#     print(i)
# print('*****last n periods******')
# print()
print('*****overall******')
for i in b:
    print(i)
print('*****overall******')





#Calculating ROE
stock_no_info_on_equity_and_Net_Income = set()
gathering_statistics = data_frame_combined.loc[
                       (
                           ('Balance','Income'),
                           (slice(None)),
                           ('Stockholders Equity', 'Net Income')

                       ),
                       :].copy()
print('*' * 50)

list_of_columns = list(gathering_statistics.columns)  #get the dates
Stocks_in_df = set(gathering_statistics.index.get_level_values(1)) #get the stocks involved
Stocks_in_df = list(Stocks_in_df)
for stock in data_frame_combined.index.get_level_values(1):
    if stock not in Stocks_in_df:
        stock_no_info_on_equity_and_Net_Income.add(stock)


stock_results = []
list_every_stock_result = []
stock_no_info_on_net_profit_or_stock_holders_equity_set = set()
for stock in Stocks_in_df:
    #print('*' * 20, 'NEW STOCK','*' * 20 )
    stock_results = []
    for column in list_of_columns:
        # print(stock,column)
        try:
            Net_profit = gathering_statistics.loc[('Income', stock, 'Net Income'), (column)] #get Net profit for stock a
            # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
            Stock_holders_equity = gathering_statistics.loc[('Balance', stock, 'Stockholders Equity'), (column)] #get Total assets for stock a
            # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
            ROE = Net_profit/Stock_holders_equity
            # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
            stock_results.append(ROE)
            # print('*' * 100)
        except Exception:
            # print(f'{stock} is missing Net income or Net assets figure')
            stock_no_info_on_net_profit_or_stock_holders_equity_set.add(stock)
            continue
    #
    mlt = pd.MultiIndex.from_arrays(
        [np.array([stock]), np.array(['ROE'])] #row index of stock then GPM value
    )
    if stock_results != []:  #check stock actually has readable contents by Yahoo
        # print(mlt)
        # print(stock_results)
        i = [[x for x in stock_results]]
        # print(i)
        gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
        # gp_df = pd.DataFrame(stock_results, index=mlt, columns=gathering_statistics.columns[:2])
        # print(gp_df)
        print()
        list_every_stock_result.append(gp_df)

data_frame_combined_ROE = pd.concat(list_every_stock_result)


data_frame_combined_ROE_last_n_periods = data_frame_combined_ROE.iloc[:,periods]
Df_ROE_table_mean_calculation_last_n_periods = data_frame_combined_ROE_last_n_periods.mean(axis=1)
data_frame_combined_ROE_last_n_periods.insert(0,f'ROE last {len(periods)} periods', Df_ROE_table_mean_calculation_last_n_periods)
data_frame_combined_ROE_last_n_periods = data_frame_combined_ROE_last_n_periods.sort_values(by=(f'ROE last {len(periods)} periods',), axis=0, ascending=False)
print(data_frame_combined_ROE_last_n_periods)

Df_ROE_table_mean_calculation_whole_period = data_frame_combined_ROE.mean(axis=1)
data_frame_combined_ROE.insert(0, 'ROE', Df_ROE_table_mean_calculation_whole_period)
data_frame_combined_ROE = data_frame_combined_ROE.sort_values(by=('ROE',), axis=0, ascending=False)
print(data_frame_combined_ROE)
print(len(data_frame_combined_ROE))
#
Stocks_in_df_for_complete_ranking_of_stocks = list(data_frame_combined_ROE.index.get_level_values(0))  #get the stocks involved
points = 0
for stock in Stocks_in_df_for_complete_ranking_of_stocks:
    try:
        a = Complete_rankings_of_stocks[stock]
        Complete_rankings_of_stocks[stock] += points
        # print(f'{stock} gained {points} points')
    except Exception:
        Complete_rankings_of_stocks[stock] = points
        # print(f'stock has {points} points')
    points += 1


# a = data_frame_combined_ROE_last_n_periods.index.get_level_values(0)
b = data_frame_combined_ROE.index.get_level_values(0)
# print('*****last n periods******')
# for i in a:
#     print(i)
# print('*****last n periods******')
# print()
print('*****overall******')
for i in b:
    print(i)
print('*****overall******')







#Calculating FCFE
stock_no_info_on_operating_cash_flow_and_net_issuance_payments_of_debt_and_capex_set = set()
gathering_statistics = data_frame_combined.loc[
                       (
                           ('Cash Flow'),
                           (slice(None)),
                           ('Operating Cash Flow','Net Issuance Payments Of Debt', 'Capital Expenditure')

                       ),
                       :].copy()



# print(gathering_statistics)
print('*' * 50)

list_of_columns = list(gathering_statistics.columns)  #get the dates
Stocks_in_df = set(gathering_statistics.index.get_level_values(1)) #get the stocks involved
Stocks_in_df = list(Stocks_in_df)
for stock in data_frame_combined.index.get_level_values(1):
    if stock not in Stocks_in_df:
        stock_no_info_on_operating_cash_flow_and_net_issuance_payments_of_debt_and_capex_set.add(stock)


stock_results = []
list_every_stock_result = []
stock_no_info_on_Operating_cash_flow_or_net_capital_expenditure_set= set()
stock_no_info_on_Net_issuance_payments_of_debt = set()
for stock in Stocks_in_df:
    #print('*' * 20, 'NEW STOCK','*' * 20 )
    stock_results = []
    for column in list_of_columns:
        # print(stock,column)
        try:
            Operating_cash_flow = gathering_statistics.loc[('Cash Flow', stock, 'Operating Cash Flow'), (column)] #get Net profit for stock a
            # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
            Net_Issuance_payment_Of_debt = gathering_statistics.loc[('Cash Flow', stock, 'Net Issuance Payments Of Debt'), (column)] #get Total assets for stock a
            # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
            Capital_expenditure = gathering_statistics.loc[('Cash Flow', stock, 'Capital Expenditure'), (column)]
            FCFE = (Operating_cash_flow + Net_Issuance_payment_Of_debt + Capital_expenditure)
            # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
            stock_results.append(FCFE)
            # print('*' * 100)
        except Exception:
            try:
                Operating_cash_flow = gathering_statistics.loc[('Cash Flow', stock, 'Operating Cash Flow'), (column)]
                Capital_expenditure = gathering_statistics.loc[('Cash Flow', stock, 'Capital Expenditure'), (column)]
                FCFE = Operating_cash_flow + Capital_expenditure
                stock_results.append(FCFE)
                stock_no_info_on_Net_issuance_payments_of_debt.add(stock)
            except Exception:
                stock_no_info_on_Operating_cash_flow_or_net_capital_expenditure_set.add(stock)
                continue

    mlt = pd.MultiIndex.from_arrays(
        [np.array([stock]), np.array(['FCFE'])] #row index of stock then GPM value
    )
    if stock_results != []:  #check stock actually has readable contents by Yahoo
        # print(mlt)
        # print(stock_results)
        i = [[x for x in stock_results]]
        # print(i)
        gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
        # gp_df = pd.DataFrame(stock_results, index=mlt, columns=gathering_statistics.columns[:2])
        # print(gp_df)
        print()
        list_every_stock_result.append(gp_df)

data_frame_combined_FCFE = pd.concat(list_every_stock_result)



data_frame_combined_FCFE_last_n_periods = data_frame_combined_FCFE.iloc[:,periods]
Df_FCFE_table_mean_calculation_last_n_periods = data_frame_combined_FCFE_last_n_periods.mean(axis=1)
data_frame_combined_FCFE_last_n_periods.insert(0,f'FCFE last {len(periods)} periods', Df_FCFE_table_mean_calculation_last_n_periods)
data_frame_combined_FCFE_last_n_periods = data_frame_combined_FCFE_last_n_periods.sort_values(by=(f'FCFE last {len(periods)} periods',), axis=0, ascending=False)
print(data_frame_combined_FCFE_last_n_periods)

Df_FCFE_table_mean_calculation_whole_period = data_frame_combined_FCFE.mean(axis=1)
data_frame_combined_FCFE.insert(0, 'FCFE', Df_FCFE_table_mean_calculation_whole_period)
data_frame_combined_FCFE = data_frame_combined_FCFE.sort_values(by=('FCFE',), axis=0, ascending=False)
print(data_frame_combined_FCFE)
print(len(data_frame_combined_FCFE))

Stocks_in_df_for_complete_ranking_of_stocks = list(data_frame_combined_FCFE.index.get_level_values(0))  #get the stocks involved
points = 0
for stock in Stocks_in_df_for_complete_ranking_of_stocks:
    try:
        a = Complete_rankings_of_stocks[stock]
        Complete_rankings_of_stocks[stock] += (points * 3)
        # print(f'{stock} gained {points} points')
    except Exception:
        Complete_rankings_of_stocks[stock] = (points * 3)
        # print(f'stock has {points} points')
    points += 1


# a = data_frame_combined_gross_profit_margin_last_3_periods.index.get_level_values(0)
b = data_frame_combined_FCFE.index.get_level_values(0)
# print('*****last n periods******')
# for i in a:
#     print(i)
# print('*****last n periods******')
# print()
print('*****overall******')
for i in b:
    print(i)
print('*****overall******')









#Calculating debt-to-equity
stock_no_info_on_equity_and_total_liabilities_set = set()
gathering_statistics = data_frame_combined.loc[
                       (
                           ('Balance'),
                           (slice(None)),
                           ('Stockholders Equity', 'Total Liabilities Net Minority Interest')

                       ),
                       :].copy()
print('*' * 50)

list_of_columns = list(gathering_statistics.columns)  #get the dates
Stocks_in_df = set(gathering_statistics.index.get_level_values(1)) #get the stocks involved
Stocks_in_df = list(Stocks_in_df)
for stock in data_frame_combined.index.get_level_values(1):
    if stock not in Stocks_in_df:
        stock_no_info_on_equity_and_total_liabilities_set.add(stock)

stock_results = []
list_every_stock_result = []
stock_no_info_on_Liabilities_or_stock_holders_equity_set = set()
for stock in Stocks_in_df:
    #print('*' * 20, 'NEW STOCK','*' * 20 )
    stock_results = []
    for column in list_of_columns:
        # print(stock,column)
        try:
            Liabilities = gathering_statistics.loc[('Balance', stock, 'Total Liabilities Net Minority Interest'), (column)] #get Net profit for stock a
            # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
            Stock_holders_equity = gathering_statistics.loc[('Balance', stock, 'Stockholders Equity'), (column)] #get Total assets for stock a
            # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
            Debt_Equity = Liabilities/Stock_holders_equity
            # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
            stock_results.append(Debt_Equity)
            # print('*' * 100)
        except Exception:
            # print(f'{stock} is missing Net income or Net assets figure')
            stock_no_info_on_Liabilities_or_stock_holders_equity_set.add(stock)
            continue
    #
    mlt = pd.MultiIndex.from_arrays(
        [np.array([stock]), np.array(['Debt to equity'])] #row index of stock then GPM value
    )
    if stock_results != []:  #check stock actually has readable contents by Yahoo
        # print(mlt)
        # print(stock_results)
        i = [[x for x in stock_results]]
        # print(i)
        gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
        # gp_df = pd.DataFrame(stock_results, index=mlt, columns=gathering_statistics.columns[:2])
        # print(gp_df)
        print()
        list_every_stock_result.append(gp_df)

data_frame_combined_D_E = pd.concat(list_every_stock_result)


data_frame_combined_D_E_last_n_periods = data_frame_combined_D_E.iloc[:,periods]
Df_D_E_table_mean_calculation_last_n_periods = data_frame_combined_D_E_last_n_periods.mean(axis=1)
data_frame_combined_D_E_last_n_periods.insert(0,f'Debt-to-equity last {len(periods)} periods', Df_D_E_table_mean_calculation_last_n_periods)
data_frame_combined_D_E_last_n_periods = data_frame_combined_D_E_last_n_periods.sort_values(by=(f'Debt-to-equity last {len(periods)} periods',), axis=0, ascending=True,
                                                                                            key = lambda Series: Series.where(Series > 0, Series * -100000))
print(data_frame_combined_D_E_last_n_periods)

Df_D_E_table_mean_calculation_whole_period = data_frame_combined_D_E.mean(axis=1)
data_frame_combined_D_E.insert(0, 'Debt-to-equity', Df_D_E_table_mean_calculation_whole_period)
data_frame_combined_D_E = data_frame_combined_D_E.sort_values(by=('Debt-to-equity',), axis=0, ascending=True,
                                                              key = lambda Series: Series.where(Series > 0, Series * -100000))
# key = lambda Series: Series.apply(lambda value : value if value > 0 else value * -100000))
print(data_frame_combined_D_E)
print(len(data_frame_combined_D_E))
#
Stocks_in_df_for_complete_ranking_of_stocks = list(data_frame_combined_D_E.index.get_level_values(0))  #get the stocks involved
points = 0
for stock in Stocks_in_df_for_complete_ranking_of_stocks:
    try:
        a = Complete_rankings_of_stocks[stock]
        Complete_rankings_of_stocks[stock] += points
        # print(f'{stock} gained {points} points')
    except Exception:
        Complete_rankings_of_stocks[stock] = points
        # print(f'stock has {points} points')
    points += 1


# a = data_frame_combined_gross_profit_margin_last_3_periods.index.get_level_values(0)
b = data_frame_combined_D_E.index.get_level_values(0)
# print('*****last n periods******')
# for i in a:
#     print(i)
# print('*****last n periods******')
# print()
# print('*****overall******')
for i in b:
    print(i)
print('*****overall******')











# Calculating quick ratio
stock_no_info_on_current_assets_and_current_liabilities_and_inventory_set = set()
gathering_statistics = data_frame_combined.loc[
                       (
                           ('Balance'),
                           (slice(None)),
                           ('Current Assets','Inventory','Current Liabilities')

                       ),
                       :].copy()
print('*' * 50)



list_of_columns = list(gathering_statistics.columns)  #get the dates
Stocks_in_df = set(gathering_statistics.index.get_level_values(1)) #get the stocks involved
Stocks_in_df = list(Stocks_in_df)
for stock in data_frame_combined.index.get_level_values(1):
    if stock not in Stocks_in_df:
        stock_no_info_on_current_assets_and_current_liabilities_and_inventory_set.add(stock)



stock_results = []
list_every_stock_result = []
stock_no_info_on_current_assets_or_current_liabilities_set = set()
stock_no_info_on_inventory_set = set()
for stock in Stocks_in_df:
    #print('*' * 20, 'NEW STOCK','*' * 20 )
    stock_results = []
    for column in list_of_columns:
        # print(stock,column)
        try:
            Current_assets = gathering_statistics.loc[('Balance', stock, 'Current Assets'), (column)]
            Current_liabilities = gathering_statistics.loc[('Balance', stock, 'Current Liabilities'), (column)]
            Inventory = gathering_statistics.loc[('Balance', stock, 'Inventory'), (column)]
            Quick_ratio = (Current_assets - Inventory)/Current_liabilities
            # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
            stock_results.append(Quick_ratio)
            # print('*' * 100)
        except Exception:
            try:
                Current_assets = gathering_statistics.loc[('Balance', stock, 'Current Assets'), (column)]
                # print(f'current assets for {stock} in year {column}: {Current_assets}')
                Current_liabilities = gathering_statistics.loc[('Balance', stock, 'Current Liabilities'), (column)]
                # print(f'Current liabilities for {stock} in year {column}: {Current_liabilities}')
                Quick_ratio_no_inv = (Current_assets)/(Current_liabilities)
                # print(f'{stock} is missing a number for inventory')
                stock_results.append(Quick_ratio_no_inv)
                stock_no_info_on_inventory_set.add(stock)
            except Exception:
                # print('did we get here')
                # print(f'{stock} is missing a Current assets or Current liabilities')
                stock_no_info_on_current_assets_or_current_liabilities_set.add(stock)
                continue

    mlt = pd.MultiIndex.from_arrays(
        [np.array([stock]), np.array(['Quick ratio'])] #row index of stock then GPM value
    )
    if stock_results != []:  #check stock actually has readable contents by Yahoo
        # print(mlt)
        # print(stock_results)
        i = [[x for x in stock_results]]
        # print(i)
        gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
        # gp_df = pd.DataFrame(stock_results, index=mlt, columns=gathering_statistics.columns[:2])
        # print(gp_df)
        print()
        list_every_stock_result.append(gp_df)

data_frame_combined_Quick_ratio = pd.concat(list_every_stock_result)


data_frame_combined_Quick_ratio_last_n_periods = data_frame_combined_Quick_ratio.iloc[:,periods]
Df_Quick_Ratio_table_mean_calculation_last_n_periods = data_frame_combined_Quick_ratio_last_n_periods.mean(axis=1)
data_frame_combined_Quick_ratio_last_n_periods.insert(0,f'Quick ratio last {len(periods)} periods', Df_Quick_Ratio_table_mean_calculation_last_n_periods)
data_frame_combined_Quick_ratio_last_n_periods = data_frame_combined_Quick_ratio_last_n_periods.sort_values(by=(f'Quick ratio last {len(periods)} periods',), axis=0, ascending=False)
print(data_frame_combined_Quick_ratio_last_n_periods)

Df_Quick_ratio_table_mean_calculation_whole_period = data_frame_combined_Quick_ratio.mean(axis=1)
data_frame_combined_Quick_ratio.insert(0, 'Quick ratio', Df_Quick_ratio_table_mean_calculation_whole_period)
data_frame_combined_Quick_ratio = data_frame_combined_Quick_ratio.sort_values(by=('Quick ratio',), axis=0, ascending=False)
print(data_frame_combined_Quick_ratio)
print(len(data_frame_combined_Quick_ratio))

Stocks_in_df_for_complete_ranking_of_stocks = list(data_frame_combined_Quick_ratio.index.get_level_values(0))  #get the stocks involved
points = 0
for stock in Stocks_in_df_for_complete_ranking_of_stocks:
    try:
        a = Complete_rankings_of_stocks[stock]
        Complete_rankings_of_stocks[stock] += points
        # print(f'{stock} gained {points} points')
    except Exception:
        Complete_rankings_of_stocks[stock] = points
        # print(f'stock has {points} points')
    points += 1

# a = data_frame_combined_gross_profit_margin_last_3_periods.index.get_level_values(0)
b = data_frame_combined_Quick_ratio.index.get_level_values(0)
# print('*****last n periods******')
# for i in a:
#     print(i)
# print('*****last n periods******')
# print()
list_1 = []
print('*****overall******')
for i in b:
    print(i)
    list_1.append(i)
print('*****overall******')




#Conclusions which should always be at bottom of page
print('NO INFO ON FINANCIALS', stock_no_info_on_financials_set)
print('NO INFO ON REVENUE OR GROSS PROFIT',stock_no_info_on_Gross_profit_or_revenue_set)
print('NO INFO ON REVENUE AND GROSS PROFIT', stock_no_info_on_Total_Revenue_and_Gross_profit)
print('NO INFO ON REVENUE OR OPERATING PROFIT',stock_no_info_on_operating_profit_or_revenue_set)
print('NO INFO ON REVENUE AND OPERATING PROFIT',stock_no_info_on_Total_Revenue_and_Operating_profit)
print('NO INFO ON REVENUE OR NET PROFIT',stock_no_info_on_net_profit_or_revenue_set)
print('NO INFO ON REVENUE AND NET PROFIT', stock_no_info_on_Total_Revenue_and_Net_Income)
print('NO INFO ON TOTAL ASSETS OR NET PROFIT',stock_no_info_on_net_profit_or_total_assets_set)
print('NO INFO ON ASSETS AND NET PROFIT', stock_no_info_on_Assets_and_Net_Profit)
print('NO INFO ON CURRENT ASSETS OR LIABILITIES', stock_no_info_on_current_assets_or_current_liabilities_set)
print('NO INFO ON CURRENT ASSETS AND CURRENT LIABILITIES AND INVENTORY', stock_no_info_on_current_assets_and_current_liabilities_and_inventory_set)
print('NO INFO ON INVENTORY', stock_no_info_on_inventory_set)
print('NO INFO ON OPERATING CASH FLOW OR NET CAPITAL EXPENDITURE',stock_no_info_on_Operating_cash_flow_or_net_capital_expenditure_set)
print('NO INFO ON NET ISSUANCE PAYEMENTS OF DEBT',stock_no_info_on_Net_issuance_payments_of_debt)
print('NO INFO ON OPERATING CASH FLOW, CAPEX AND NET ISSUANCE PAYEMENTS OF DEBT', stock_no_info_on_operating_cash_flow_and_net_issuance_payments_of_debt_and_capex_set)
print('NO INFO ON NET PROFIT OR EQUITY',stock_no_info_on_net_profit_or_stock_holders_equity_set)
print('NO INFO ON NET PROFIT AND EQUITY', stock_no_info_on_equity_and_Net_Income)
print('NO INFO ON LIABILITIES OR EQUITY', stock_no_info_on_Liabilities_or_stock_holders_equity_set)
print('NO INFO ON LIABILITIES AND EQUITY', stock_no_info_on_equity_and_total_liabilities_set)
Complete_rankings_of_stocks = sorted(Complete_rankings_of_stocks.items(), key=lambda x: x[1])
print()
print(f'Based on ROA, FCFE, Quick ratio, ROE, debt-to-equity, the best stocks in {input_sector} are')
print(f'COMPLETE RANKING OF STOCK FOR {input_sector}')

# all_sectors_ranked_dict = {}
# all_sectors_ranked_dict[]
stock_has_all_contents = []
print(Complete_rankings_of_stocks)



# #delete stocks with no FCFE value
# Complete_rankings_of_stocks_no_FCFE = Complete_rankings_of_stocks.copy()
# listt = ['REG', 'O', 'KIM', 'PLD', 'ARE', 'DLR']
# for index in reversed(range(len(Complete_rankings_of_stocks_no_FCFE))):
#     ticker = Complete_rankings_of_stocks_no_FCFE[index][0]
#     if ticker in listt:
#         del Complete_rankings_of_stocks_no_FCFE[index]
# print(Complete_rankings_of_stocks_no_FCFE)
# print(len(Complete_rankings_of_stocks_no_FCFE))


print('total stocks', len(sector_stocks[input_sector])+1)
print(len(Complete_rankings_of_stocks))
# print(len(stock_no_info_on_operating_profit_or_revenue_set))

#for stock in top 5                                       #was top 15
for (stock,points) in Complete_rankings_of_stocks[:5]:
    if stock in stock_no_info_on_financials_set:
        print(f'{stock}, no info on financials')
    if stock in stock_no_info_on_Gross_profit_or_revenue_set:
        print(f'{stock}, no info on Gross profit or revenue')
    if stock in stock_no_info_on_Total_Revenue_and_Gross_profit:
        print(f'{stock}, no info on Gross profit and revenue')
    if stock in stock_no_info_on_operating_profit_or_revenue_set:
        print(f'{stock}, no info on Operating profit or revenue')
    if stock in stock_no_info_on_Total_Revenue_and_Operating_profit:
        print(f'{stock}, no info on Operating profit and revenue')
    if stock in stock_no_info_on_net_profit_or_revenue_set:
        print(f'{stock}, no info on net profit or revenue')
    if stock in stock_no_info_on_Total_Revenue_and_Net_Income:
        print(f'{stock}, no info on net profit and revenue')
    if stock in stock_no_info_on_net_profit_or_total_assets_set:
        print(f'{stock}, no info on net profit or total assets')
    if stock in stock_no_info_on_Assets_and_Net_Profit:
        print(f'{stock}, no info on net profit and total assets')
    if stock in stock_no_info_on_current_assets_or_current_liabilities_set:
        print(f'{stock}, no info on current assets or current liabilities')
    if stock in stock_no_info_on_current_assets_and_current_liabilities_and_inventory_set:
        print(f'{stock}, no info on current assets and current liabilities and inventory')
    if stock in stock_no_info_on_inventory_set:
        print(f'{stock}, no info on inventory')
    if stock in stock_no_info_on_Operating_cash_flow_or_net_capital_expenditure_set:
        print(f'{stock}, no info Operating cash flow or net capex')
    if stock in stock_no_info_on_operating_cash_flow_and_net_issuance_payments_of_debt_and_capex_set:
        print(f'{stock}, no info Operating cash flow and net capex and payments of debt')
    if stock in stock_no_info_on_Net_issuance_payments_of_debt:
        print(f'{stock}, no info on net issuance payements of debt')
    if stock in stock_no_info_on_net_profit_or_stock_holders_equity_set:
        print(f'{stock}, no info on net profit or equity')
    if stock in stock_no_info_on_equity_and_Net_Income:
        print(f'{stock}, no info on net profit and equity')
    if stock in stock_no_info_on_Liabilities_or_stock_holders_equity_set:
        print(f'{stock}, no info on liabilities or equity')
    if stock in stock_no_info_on_equity_and_total_liabilities_set:
        print(f'{stock}, no info on liabilities and equity')

    # elif stock not in (stock_no_info_on_Liabilities_or_stock_holders_equity_set):
    #                 # stock_no_info_on_net_profit_or_stock_holders_equity_set,
    #                 # stock_no_info_on_Net_issuance_payments_of_debt,
    #                 #  stock_no_info_on_Operating_cash_flow_or_net_capital_expenditure_set,
    #                 #  stock_no_info_on_inventory_set,
    #                 #  stock_no_info_on_current_assets_or_current_liabilities_set,
    #                 #  stock_no_info_on_net_profit_or_total_assets_set,
    #                 #  stock_no_info_on_net_profit_or_revenue_set,
    #                 #  stock_no_info_on_operating_profit_or_revenue_set,
    #                 #  stock_no_info_on_Gross_profit_or_revenue_set,
    #                 #  stock_no_info_on_financials_set):
#     else:
#         stock_has_all_contents.append(stock)
# print('STOCK WITH ALL CONTENTS',stock_has_all_contents)

# for stock in sector_stocks[input_sector]:
#     if stock not in Stocks_in_df_for_complete_ranking_of_stocks:
#         print(stock)
