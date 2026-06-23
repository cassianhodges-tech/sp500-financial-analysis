import yfinance as yf
import pandas as pd
import numpy as np
#to do
# df_with_all_values_dummy



data_frame_list = []
stock_no_info_on_financials_set = set()
dummy_stock_ticker = yf.Ticker('NVDA')
stock = 'Dummy stock'

#get cash flow
cash_flow = dummy_stock_ticker.cashflow   #for yearly cash flow
cash_flow_index = cash_flow.index
cash_level_label = f'{stock.upper()}'
Cash = pd.Index(['Cash Flow' for u in range(len(cash_flow_index))])
Cash_level = pd.Index([cash_level_label for i in range(len(cash_flow_index))])
cash_components_level = pd.Index(cash_flow_index)
#create multi-index of cash and cash titles
arrays = [
    np.array(Cash),
    np.array(Cash_level),
    np.array(cash_components_level)
]

mlt = pd.MultiIndex.from_arrays(arrays, names=['Topic','Company','Measurements'])
vals = [str(x) for x in cash_flow.columns.values]
if vals == []:
    print(f'No information on cash-flow for stock {stock}')
    stock_no_info_on_financials_set.add(stock)
col_index_for_df = []
for i in vals:
    col_index_for_df.append(i[:10])
col_index = pd.Index(col_index_for_df, name='Year')
Cash_data_frame = pd.DataFrame(cash_flow.values,columns=col_index,index=mlt)
data_frame_list.append(Cash_data_frame)


#get income stmnt
income_statement = dummy_stock_ticker.income_stmt
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
Balance_sheet = dummy_stock_ticker.balance_sheet
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



#Create a combined data frame of cash,income and balance
dummy_stock_df = pd.concat(data_frame_list)
dummy_stock_df= dummy_stock_df.sort_index(level='Topic')  #Group by balance,income and cash

#Sort column years
dummy_stock_df = dummy_stock_df.sort_index(axis=1, ascending=False)
dummy_stock_df[:] = np.nan
