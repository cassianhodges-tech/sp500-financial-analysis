import sys
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as Tticker
import openpyxl

#show all columns and rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

data_frame_list = []
stocks_done = 0
stock_no_info = 0
stock_no_info_on_financials_set = set()
periods = [0, 1, 2, 3, 4, 5, 6]
Complete_rankings_of_stocks = {}
Complete_rankings_of_stocks_top_n = {}

stock_no_info_on_Gross_profit_or_revenue_set = set()
stock_no_info_on_Total_Revenue_and_Gross_profit = set()

stock_no_info_on_Total_Revenue_and_Operating_profit = set()
stock_no_info_on_operating_profit_or_revenue_set = set()

stock_no_info_on_Total_Revenue_and_Net_Income = set()
stock_no_info_on_net_profit_or_revenue_set = set()

stock_no_info_on_Assets_and_Net_Profit = set()
stock_no_info_on_net_profit_or_total_assets_set = set()

stock_no_info_on_equity_and_Net_Income = set()
stock_no_info_on_net_profit_or_stock_holders_equity_set = set()

stock_no_info_on_operating_cash_flow_and_net_issuance_payments_of_debt_and_capex_set = set()
stock_no_info_on_Operating_cash_flow_or_net_capital_expenditure_set= set()
stock_no_info_on_Net_issuance_payments_of_debt = set()

stock_no_info_on_equity_and_total_liabilities_set = set()
stock_no_info_on_Liabilities_or_stock_holders_equity_set = set()

stock_no_info_on_current_assets_and_current_liabilities_and_inventory_set = set()
stock_no_info_on_current_assets_or_current_liabilities_set = set()
stock_no_info_on_inventory_set = set()

stock_no_info_on_cash_and_current_liabilities = set()
stock_no_info_on_cash_or_current_liabilities = set()

stock_no_recommendations = set()


class Cashflow:


    def __init__(self, stocks: list):
        """
            Class to represent a list of Cash Flow dataframes for stocks passed

            Args:
                stocks (list): List of stocks
        """
        self.stocks = stocks
        self.all_cash_flow_data_frames = []

    def get_cash_flow(self, cash_flow_format: str) -> list:
        """
                Uses Yfinance to compute cash flow dataframes.

                Args:
                    cash_flow_format (str): 'cash_flow' or 'quarterly_cash_flow'

                Returns:
                    list: A list of the combined cash flow statements in data frame format of stocks provided
                """
        for stock in self.stocks:
            ticker = yf.Ticker(stock)
            if cash_flow_format == 'cash_flow':
                cash_flow = ticker.cash_flow  # for cash flow statement (years as columns, cash metrics as axis)
            elif cash_flow_format == 'quarterly_cash_flow':
                cash_flow = ticker.quarterly_cash_flow
            else:
                print('INACCURATE CASH_FLOW_FORMAT')
                sys.exit()
            cash_flow_index = cash_flow.index  # get cash metrics
            cash_level_label = f'{stock.upper()}'
            Cash = pd.Index(['Cash Flow' for u in range(len(cash_flow_index))])
            Cash_level = pd.Index([cash_level_label for i in range(len(cash_flow_index))])
            cash_components_level = pd.Index(cash_flow_index)  # already in index form, this line isnt needed
            # create multi-index of cash and cash titles
            arrays = [
                np.array(Cash),  # cash
                np.array(Cash_level),  # stock
                np.array(cash_components_level)  # cash metric
            ]
            mlt = pd.MultiIndex.from_arrays(arrays, names=['Topic', 'Company',
                                                           'Measurements'])  # creates row index of cash,stock,cash metric
            vals = [str(x) for x in cash_flow.columns.values]  # get dates as strings
            if vals == []:
                # print(f'No information on cash-flow for stock {stock}')
                stock_no_info_on_financials_set.add(stock)
            col_index_for_df = []
            for i in vals:
                col_index_for_df.append(i[:10])  # only get year,month, day
            col_index = pd.Index(col_index_for_df, name='Year')  # prepare col index
            Cash_data_frame = pd.DataFrame(cash_flow.values, columns=col_index,
                                           index=mlt)  # paste all values. Now columns are slighlt adjusted and additional...
            self.all_cash_flow_data_frames.append(Cash_data_frame)
        return self.all_cash_flow_data_frames

class Income_stmt:


    def __init__(self, stocks: list):
        """
                Args
                stocks (list): List of stocks
        """
        self.stocks = stocks
        self.all_income_stmt_data_frames = []

    def get_income_statement(self, income_stmt_format: str)-> list:
        """
                Uses Yfinance to compute income statement dataframes.

                Args:
                    income_stmt_format (str): 'incomestmt' or 'quarterly_incomestmt'

                Returns:
                    list: A list of the combined income statements in data frame format of stocks provided
                """
        for stock in self.stocks:
            ticker = yf.Ticker(stock)
            if income_stmt_format == 'incomestmt':
                income_statement = ticker.incomestmt
            elif income_stmt_format == 'quarterly_incomestmt':
                income_statement = ticker.quarterly_incomestmt
            else:
                print('INACCURATE INCOME STATEMENT FORMAT')
                sys.exit()
            Income_stmt_index = income_statement.index
            Income_stmt_label = f'{stock.upper()}'
            Income = pd.Index(['Income' for u in range(len(Income_stmt_index))])
            Income_level = pd.Index([Income_stmt_label for i in range(len(Income_stmt_index))])
            Income_components_level = pd.Index(Income_stmt_index)
            # create multi-index of income_stmt and income_stmt titles
            arrays = [
                np.array(Income),
                np.array(Income_level),
                np.array(Income_components_level)
            ]
            mlt = pd.MultiIndex.from_arrays(arrays, names=['Topic', 'Company', 'Measurements'])
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
            Income_stmt_data_frame = pd.DataFrame(income_statement.values, columns=col_index, index=mlt)
            self.all_income_stmt_data_frames.append(Income_stmt_data_frame)
        return self.all_income_stmt_data_frames

class Balance_Sheet:


    def __init__(self, stocks: list):
        """
            Class to represent a list of Balance Sheet dataframes for stocks passed

            Args
                stocks (list): List of stocks
        """
        self.stocks = stocks
        self.all_balance_sheet_data_frames = []

    def get_balance_sheet(self, balance_sheet_format: str)-> list:
        """
                Uses Yfinance to compute balance sheet dataframes.

                Args:
                    balance_sheet_format (str): 'balance_sheet' or 'quarterly_balance_sheet'

                Returns:
                    list: A list of the combined balance sheets in data frame format of stocks provided
                """
        for stock in self.stocks:
            ticker = yf.Ticker(stock)
            if balance_sheet_format == 'balance_sheet':
                Balance_sheet = ticker.balance_sheet
            elif balance_sheet_format == 'quarterly_balance_sheet':
                Balance_sheet = ticker.quarterly_balance_sheet
            else:
                print('INACCURATE INCOME STATEMENT FORMAT')
                sys.exit()
            Balance_sheet_index = Balance_sheet.index
            Balance_sheet_label = f'{stock.upper()}'
            Balance = pd.Index(['Balance' for u in range(len(Balance_sheet_index))])
            Balance_level = pd.Index([Balance_sheet_label for i in range(len(Balance_sheet_index))])
            Balance_components_level = pd.Index(Balance_sheet_index)
            # create multi-index of cash and cash titles
            arrays = [
                np.array(Balance),
                np.array(Balance_level),
                np.array(Balance_components_level)
            ]
            mlt = pd.MultiIndex.from_arrays(arrays, names=['Topic', 'Company', 'Measurements'])
            vals = [str(x) for x in Balance_sheet.columns.values]
            if vals == []:
                # print(f'No information on Balance sheet for stock {stock}')
                stock_no_info_on_financials_set.add(stock)
            col_index_for_df = []
            for i in vals:
                col_index_for_df.append(i[:10])
            col_index = pd.Index(col_index_for_df, name='Year')
            Balance_sheet_data_frame = pd.DataFrame(Balance_sheet.values, columns=col_index, index=mlt)
            self.all_balance_sheet_data_frames.append(Balance_sheet_data_frame)
        return self.all_balance_sheet_data_frames

class Financials:

    def __init__(self, stocks: list):
        """
            Class to represent a financial dataframe for stocks passed

            Args:
                stocks (list): List of stocks
               """
        self.cash_flow_dfs = Cashflow(stocks)
        self.income_stmt_dfs = Income_stmt(stocks)
        self.balance_sheet_dfs = Balance_Sheet(stocks)
        self.financials_list = []

    def get_financials_data_frame(self)-> pd.DataFrame:
        """
        Uses Yfinance to compute a finanial dataframe of all stocks in 'stocks'.

        Returns:
            dataframe: The combined finanicial statements in data frame format of stocks provided.
                       Data frame format is:
                       Topic, Company, Measurements on index
                       Years on columns
        """
        from dummy_stock import dummy_stock_df
        print('Computing cash flow dataframe')
        cash_flow = self.cash_flow_dfs.get_cash_flow('cash_flow')
        # cash_flow = self.cash_flow_dfs.get_cash_flow('quarterly_cash_flow')
        print('Computing income statement dataframe')
        income_stms = self.income_stmt_dfs.get_income_statement('incomestmt')
        # income_stms = self.income_stmt_dfs.get_income_statement('quarterly_incomestmt')
        print('Computing balance sheet dataframe')
        balance_sheets = self.balance_sheet_dfs.get_balance_sheet('balance_sheet')
        # balance_sheets = self.balance_sheet_dfs.get_balance_sheet('quarterly_balance_sheet')
        data_frame_combined = pd.concat([*cash_flow, *income_stms, *balance_sheets, dummy_stock_df])
        data_frame_combined = data_frame_combined.sort_index(level='Topic')  # Group by balance,income and cash
        # Sort column years
        data_frame_combined = data_frame_combined.sort_index(axis=1, ascending=False)
        return data_frame_combined

class Get_financial_metrics:
    def __init__(self, dataframe: pd.DataFrame):
        """
            Class to represent succinct dataframes for all major financial metrics and rank them accordingly

            Args:
                dataframe (pd.Dataframe): Dataframe containing the financials of every stock you want to analyse.
                Pass the data frame which is the result of:
                    Class --> Financials
                    Method --> get_financials_data_frame()
                       """
        self.dataframe = dataframe

    def get_gross_profit_margin(self) -> pd.DataFrame:
        """
            Computes gross profit margin for each stock in dataframe passed to Get_financial_metrics.

            Returns:
                Data frame: A data frame of stocks passed with gross profit margin computed
                        """
        # stock_no_info_on_Total_Revenue_and_Gross_profit = set()
        gathering_statistics = self.dataframe.loc[('Income', slice(None), ('Gross Profit', 'Total Revenue')),
                               :].copy()
        # print(gathering_statistics)
        print('*' * 50)
        # print(gathering_statistics)

        list_of_columns = list(gathering_statistics.columns)  # get the dates for the values
        Stocks_in_df = set(gathering_statistics.index.get_level_values(1))  # get the stocks involved for the values
        Stocks_in_df = list(Stocks_in_df)
        for stock in self.dataframe.index.get_level_values(1):
            if stock not in Stocks_in_df:
                stock_no_info_on_Total_Revenue_and_Gross_profit.add(stock)

        list_every_stock_result = []
        for stock in Stocks_in_df:
            # print('*' * 20, 'NEW STOCK','*' * 20 )
            stock_results = []
            for column in list_of_columns:
                # print(stock,column)
                try:
                    Gross_profit_figure = gathering_statistics.loc[
                        ('Income', stock, 'Gross Profit'), (column)]  # get profit for stock a
                    # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
                    Revenue_Figure = gathering_statistics.loc[
                        ('Income', stock, 'Total Revenue'), (column)]  # get revenue for stock a
                    # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
                    Gross_profit_margin = Gross_profit_figure / Revenue_Figure
                    # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
                    stock_results.append(Gross_profit_margin)
                    # print('*' * 100)
                except Exception:
                    # print(f'{stock} is missing Gross profit or revenue value')
                    stock_no_info_on_Gross_profit_or_revenue_set.add(stock)
                    continue

            mlt = pd.MultiIndex.from_arrays(
                [np.array([stock]), np.array(['Gross Profit margin'])]  # row index of stock then GPM value
            )
            if stock_results != []:  # check stock actually has readable contents by Yahoo
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
        return data_frame_combined_gross_profit_margin


    def get_operating_profit_margin(self) -> pd.DataFrame:
        """
            Computes operating profit margin for each stock in dataframe passed to Get_financial_metrics.

            Returns:
                Data frame: A data frame of stocks passed with operating profit margin computed
        """
        gathering_statistics = self.dataframe.loc[('Income', slice(None), ('Operating Income', 'Total Revenue')),
                               :].copy()
        print('*' * 50)

        list_of_columns = list(gathering_statistics.columns)  # get the dates
        Stocks_in_df = set(gathering_statistics.index.get_level_values(1))  # get the stocks involved
        Stocks_in_df = list(Stocks_in_df)
        for stock in self.dataframe.index.get_level_values(1):
            if stock not in Stocks_in_df:
                stock_no_info_on_Total_Revenue_and_Operating_profit.add(stock)

        list_every_stock_result = []
        for stock in Stocks_in_df:
            stock_results = []
            for column in list_of_columns:
                try:
                    Operating_Income_figure = gathering_statistics.loc[
                        ('Income', stock, 'Operating Income'), (column)]
                    # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
                    Revenue_Figure = gathering_statistics.loc[
                        ('Income', stock, 'Total Revenue'), (column)]
                    # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
                    Operating_Income_margin = Operating_Income_figure / Revenue_Figure
                    # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
                    stock_results.append(Operating_Income_margin)
                except Exception:
                    # print(f'{stock} is missing Operating profit or revenue value')
                    stock_no_info_on_operating_profit_or_revenue_set.add(stock)
                    continue

            mlt = pd.MultiIndex.from_arrays(
                [np.array([stock]), np.array(['Operating profit margin'])]  # row index of stock then GPM value
            )
            if stock_results != []:  # check stock actually has readable contents by Yahoo
                gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
                print()
                list_every_stock_result.append(gp_df)

        data_frame_combined_Operating_income_margin = pd.concat(list_every_stock_result)
        return data_frame_combined_Operating_income_margin

    def get_net_profit_margin(self) -> pd.DataFrame:
        """
           Computes net profit margin for each stock in dataframe passed to Get_financial_metrics.

           Returns:
               Data frame: A data frame of stocks passed with net profit margin computed
        """
    # stock_no_info_on_Total_Revenue_and_Net_Income = set()
        gathering_statistics = self.dataframe.loc[('Income', slice(None), ('Net Income', 'Total Revenue')), :].copy()
        print('*' * 50)

        list_of_columns = list(gathering_statistics.columns)  # get the dates
        Stocks_in_df = set(gathering_statistics.index.get_level_values(1))  # get the stocks involved
        Stocks_in_df = list(Stocks_in_df)
        for stock in self.dataframe.index.get_level_values(1):
            if stock not in Stocks_in_df:
                stock_no_info_on_Total_Revenue_and_Net_Income.add(stock)

        list_every_stock_result = []
        for stock in Stocks_in_df:
            # print('*' * 20, 'NEW STOCK','*' * 20 )
            stock_results = []
            for column in list_of_columns:
                # print(stock,column)
                try:
                    Net_profit_figure = gathering_statistics.loc[
                        ('Income', stock, 'Net Income'), (column)]  # get Net profit for stock a
                    # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
                    Revenue_Figure = gathering_statistics.loc[
                        ('Income', stock, 'Total Revenue'), (column)]  # get revenue for stock a
                    # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
                    Net_profit_margin = Net_profit_figure / Revenue_Figure
                    # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
                    stock_results.append(Net_profit_margin)
                    # print('*' * 100)
                except Exception:
                    # print(f'{stock} is missing Net income or revenue value')
                    stock_no_info_on_net_profit_or_revenue_set.add(stock)
                    continue

            mlt = pd.MultiIndex.from_arrays(
                [np.array([stock]), np.array(['Net profit margin'])]  # row index of stock then GPM value
            )
            if stock_results != []:  # check stock actually has readable contents by Yahoo
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
        return data_frame_combined_Net_profit_margin

    def get_ROA(self):
        """
           Computes ROA for each stock in dataframe passed to Get_financial_metrics.

           Returns:
               Data frame: A data frame of stocks passed with ROA computed
        """
        gathering_statistics = self.dataframe.loc[
                               (
                                   ('Balance', 'Income'),
                                   (slice(None)),
                                   ('Total Assets', 'Net Income')

                               ),
                               :].copy()
        print('*' * 50)

        list_of_columns = list(gathering_statistics.columns)  # get the dates
        Stocks_in_df = set(gathering_statistics.index.get_level_values(1))  # get the stocks involved
        Stocks_in_df = list(Stocks_in_df)
        for stock in self.dataframe.index.get_level_values(1):
            if stock not in Stocks_in_df:
                stock_no_info_on_Assets_and_Net_Profit.add(stock)

        list_every_stock_result = []
        for stock in Stocks_in_df:
            stock_results = []
            for column in list_of_columns:
                try:
                    Net_profit_figure = gathering_statistics.loc[
                        ('Income', stock, 'Net Income'), (column)]  # get Net profit for stock a
                    # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
                    Assets_Figure = gathering_statistics.loc[
                        ('Balance', stock, 'Total Assets'), (column)]  # get Total assets for stock a
                    # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
                    ROA = Net_profit_figure / Assets_Figure
                    # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
                    stock_results.append(ROA)
                    # print('*' * 100)
                except Exception:
                    # print(f'{stock} is missing Net income or Net assets figure')
                    stock_no_info_on_net_profit_or_total_assets_set.add(stock)
                    continue
            #
            mlt = pd.MultiIndex.from_arrays(
                [np.array([stock]), np.array(['ROA'])]  # row index of stock then GPM value
            )
            if stock_results != []:  # check stock actually has readable contents by Yahoo
                gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
                print()
                list_every_stock_result.append(gp_df)

        data_frame_combined_ROA = pd.concat(list_every_stock_result)
        return data_frame_combined_ROA

    def get_ROE(self):
        """
                  Computes ROE for each stock in dataframe passed to Get_financial_metrics.

                  Returns:
                      Data frame: A data frame of stocks passed with ROE computed
               """
        gathering_statistics = self.dataframe.loc[
                               (
                                   ('Balance', 'Income'),
                                   (slice(None)),
                                   ('Stockholders Equity', 'Net Income')

                               ),
                               :].copy()
        print('*' * 50)

        list_of_columns = list(gathering_statistics.columns)  # get the dates
        Stocks_in_df = set(gathering_statistics.index.get_level_values(1))  # get the stocks involved
        Stocks_in_df = list(Stocks_in_df)
        for stock in self.dataframe.index.get_level_values(1):
            if stock not in Stocks_in_df:
                stock_no_info_on_equity_and_Net_Income.add(stock)

        list_every_stock_result = []
        for stock in Stocks_in_df:
            stock_results = []
            for column in list_of_columns:
                try:
                    Net_profit = gathering_statistics.loc[
                        ('Income', stock, 'Net Income'), (column)]  # get Net profit for stock a
                    # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
                    Stock_holders_equity = gathering_statistics.loc[
                        ('Balance', stock, 'Stockholders Equity'), (column)]  # get Total assets for stock a
                    # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
                    ROE = Net_profit / Stock_holders_equity
                    # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
                    stock_results.append(ROE)
                    # print('*' * 100)
                except Exception:
                    # print(f'{stock} is missing Net income or Net assets figure')
                    stock_no_info_on_net_profit_or_stock_holders_equity_set.add(stock)
                    continue
            #
            mlt = pd.MultiIndex.from_arrays(
                [np.array([stock]), np.array(['ROE'])]  # row index of stock then GPM value
            )
            if stock_results != []:  # check stock actually has readable contents by Yahoo
                gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
                print()
                list_every_stock_result.append(gp_df)

        data_frame_combined_ROE = pd.concat(list_every_stock_result)
        return data_frame_combined_ROE

    def get_FCFE(self):
        """
         Computes FCFE for each stock in dataframe passed to Get_financial_metrics.

         Returns:
             Data frame: A data frame of stocks passed with FCFE computed
        """
        stock_no_info_on_operating_cash_flow_and_net_issuance_payments_of_debt_and_capex_set = set()
        gathering_statistics = self.dataframe.loc[
                               (
                                   ('Cash Flow'),
                                   (slice(None)),
                                   ('Operating Cash Flow', 'Net Issuance Payments Of Debt', 'Capital Expenditure')

                               ),
                               :].copy()
        print('*' * 50)

        list_of_columns = list(gathering_statistics.columns)  # get the dates
        Stocks_in_df = set(gathering_statistics.index.get_level_values(1))  # get the stocks involved
        Stocks_in_df = list(Stocks_in_df)
        for stock in self.dataframe.index.get_level_values(1):
            if stock not in Stocks_in_df:
                stock_no_info_on_operating_cash_flow_and_net_issuance_payments_of_debt_and_capex_set.add(stock)

        list_every_stock_result = []
        for stock in Stocks_in_df:
            # print('*' * 20, 'NEW STOCK','*' * 20 )
            stock_results = []
            for column in list_of_columns:
                # print(stock,column)
                try:
                    Operating_cash_flow = gathering_statistics.loc[
                        ('Cash Flow', stock, 'Operating Cash Flow'), column]  # get Net profit for stock a
                    # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
                    Net_Issuance_payment_Of_debt = gathering_statistics.loc[
                        ('Cash Flow', stock, 'Net Issuance Payments Of Debt'), column]  # get Total assets for stock a
                    # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
                    Capital_expenditure = gathering_statistics.loc[
                        ('Cash Flow', stock, 'Capital Expenditure'), column]
                    FCFE = (Operating_cash_flow + Net_Issuance_payment_Of_debt + Capital_expenditure)
                    # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
                    stock_results.append(FCFE)
                    # print('*' * 100)
                except Exception:
                    try:
                        Operating_cash_flow = gathering_statistics.loc[
                            ('Cash Flow', stock, 'Operating Cash Flow'), column]
                        Capital_expenditure = gathering_statistics.loc[
                            ('Cash Flow', stock, 'Capital Expenditure'), column]
                        FCFE = Operating_cash_flow + Capital_expenditure
                        stock_results.append(FCFE)
                        stock_no_info_on_Net_issuance_payments_of_debt.add(stock)
                    except Exception:
                        stock_no_info_on_Operating_cash_flow_or_net_capital_expenditure_set.add(stock)
                        continue

            mlt = pd.MultiIndex.from_arrays(
                [np.array([stock]), np.array(['FCFE'])]  # row index of stock then GPM value
            )
            if stock_results:  # check stock actually has readable contents by Yahoo
                gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
                print()
                list_every_stock_result.append(gp_df)

        data_frame_combined_FCFE = pd.concat(list_every_stock_result)
        return data_frame_combined_FCFE

    def get_debt_to_equity(self):
        """
         Computes debt-to-equity for each stock in dataframe passed to Get_financial_metrics.

         Returns:
             Data frame: A data frame of stocks passed with debt-to-equity computed
        """
        gathering_statistics = self.dataframe.loc[
                               (
                                   ('Balance'),
                                   (slice(None)),
                                   ('Stockholders Equity', 'Total Liabilities Net Minority Interest')

                               ),
                               :].copy()
        print('*' * 50)

        list_of_columns = list(gathering_statistics.columns)  # get the dates
        Stocks_in_df = set(gathering_statistics.index.get_level_values(1))  # get the stocks involved
        Stocks_in_df = list(Stocks_in_df)
        for stock in self.dataframe.index.get_level_values(1):
            if stock not in Stocks_in_df:
                stock_no_info_on_equity_and_total_liabilities_set.add(stock)

        list_every_stock_result = []
        for stock in Stocks_in_df:
            # print('*' * 20, 'NEW STOCK','*' * 20 )
            stock_results = []
            for column in list_of_columns:
                # print(stock,column)
                try:
                    Liabilities = gathering_statistics.loc[
                        ('Balance', stock, 'Total Liabilities Net Minority Interest'), (
                            column)]  # get Net profit for stock a
                    # print(f'Gross Profit for {stock} in year {column}: {Gross_profit_figure}')
                    Stock_holders_equity = gathering_statistics.loc[
                        ('Balance', stock, 'Stockholders Equity'), (column)]  # get Total assets for stock a
                    # print(f'Revenue for {stock} in year {column}: {Revenue_Figure}')
                    Debt_Equity = Liabilities / Stock_holders_equity
                    # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
                    stock_results.append(Debt_Equity)
                    # print('*' * 100)
                except Exception:
                    # print(f'{stock} is missing Net income or Net assets figure')
                    stock_no_info_on_Liabilities_or_stock_holders_equity_set.add(stock)
                    continue
            #
            mlt = pd.MultiIndex.from_arrays(
                [np.array([stock]), np.array(['Debt to equity'])]  # row index of stock then GPM value
            )
            if stock_results != []:  # check stock actually has readable contents by Yahoo
                gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
                print()
                list_every_stock_result.append(gp_df)

        data_frame_combined_D_E = pd.concat(list_every_stock_result)
        return data_frame_combined_D_E

    def get_quick_ratio(self):
        """
                Computes quick ratio for each stock in dataframe passed to Get_financial_metrics.

                Returns:
                    Data frame: A data frame of stocks passed with quick ratio computed
               """
        gathering_statistics = self.dataframe.loc[
                               (
                                   ('Balance'),
                                   (slice(None)),
                                   ('Current Assets', 'Inventory', 'Current Liabilities')

                               ),
                               :].copy()
        print('*' * 50)
        # print(self.dataframe)

        list_of_columns = list(gathering_statistics.columns)  # get the dates
        Stocks_in_df = set(gathering_statistics.index.get_level_values(1))  # get the stocks involved
        Stocks_in_df = list(Stocks_in_df)
        print(list_of_columns)
        for stock in self.dataframe.index.get_level_values(1):
            if stock not in Stocks_in_df:
                stock_no_info_on_current_assets_and_current_liabilities_and_inventory_set.add(stock)

        list_every_stock_result = []
        for stock in Stocks_in_df:
            stock_results = []
            for column in list_of_columns:
                try:
                    Current_assets = gathering_statistics.loc[('Balance', stock, 'Current Assets'), (column)]
                    Current_liabilities = gathering_statistics.loc[('Balance', stock, 'Current Liabilities'), (column)]
                    Inventory = gathering_statistics.loc[('Balance', stock, 'Inventory'), (column)]
                    Quick_ratio = (Current_assets - Inventory) / Current_liabilities
                    # print(f'Gross profit margin for {stock} in year {column} : {Gross_profit_margin}')
                    stock_results.append(Quick_ratio)
                    # print(f'{stock} has CA,CL & inventory {column}')
                    # print(Quick_ratio)

                    # print('*' * 100)
                except Exception:
                    try:
                        Current_assets = gathering_statistics.loc[('Balance', stock, 'Current Assets'), (column)]

                        # print(f'current assets for {stock} in year {column}')
                        # print(Current_assets)
                        Current_liabilities = gathering_statistics.loc[
                            ('Balance', stock, 'Current Liabilities'), (column)]
                        # print(f'Current liabilities for {stock} in year {column}')
                        # print(Current_liabilities)
                        Quick_ratio_no_inv = (Current_assets) / (Current_liabilities)
                        # print(f'{stock} is missing a number for inventory')
                        # print(f'{stock} has no inventory')
                        stock_results.append(Quick_ratio_no_inv)
                        stock_no_info_on_inventory_set.add(stock)

                    except Exception:
                        stock_no_info_on_current_assets_or_current_liabilities_set.add(stock)

                        continue

            mlt = pd.MultiIndex.from_arrays(
                [np.array([stock]), np.array(['Quick ratio'])]  # row index of stock then GPM value
            )
            if stock_results != []:  # check stock actually has readable contents by Yahoo
                gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
                print()
                list_every_stock_result.append(gp_df)

        data_frame_combined_Quick_ratio = pd.concat(list_every_stock_result)
        return data_frame_combined_Quick_ratio

    def get_cash_ratio(self):
        """
                       Computes cash ratio for each stock in dataframe passed to Get_financial_metrics.

                       Returns:
                           Data frame: A data frame of stocks passed with cash ratio computed
                      """
        gathering_statistics = self.dataframe.loc[
                               (
                                   ('Balance'),
                                   (slice(None)),
                                   ('Cash And Cash Equivalents', 'Current Liabilities')

                               ),
                               :].copy()
        print('*' * 50)
        # print(self.dataframe)

        list_of_columns = list(gathering_statistics.columns)  # get the dates
        Stocks_in_df = set(gathering_statistics.index.get_level_values(1))  # get the stocks involved
        Stocks_in_df = list(Stocks_in_df)
        print(list_of_columns)
        for stock in self.dataframe.index.get_level_values(1):
            if stock not in Stocks_in_df:
                stock_no_info_on_cash_and_current_liabilities.add(stock)

        list_every_stock_result = []
        for stock in Stocks_in_df:
            stock_results = []
            for column in list_of_columns:
                try:
                    Cash = gathering_statistics.loc[('Balance', stock, 'Cash And Cash Equivalents'), (column)]
                    Current_liabilities = gathering_statistics.loc[('Balance', stock, 'Current Liabilities'), (column)]
                    cash_ratio = Cash / Current_liabilities
                    stock_results.append(cash_ratio)
                except Exception:
                    stock_no_info_on_cash_or_current_liabilities.add(stock)
                    continue

            mlt = pd.MultiIndex.from_arrays(
                [np.array([stock]), np.array(['Cash ratio'])]  # row index of stock then GPM value
            )
            if stock_results != []:  # check stock actually has readable contents by Yahoo
                gp_df = pd.DataFrame([[x for x in stock_results]], index=mlt, columns=[gathering_statistics.columns])
                print()
                list_every_stock_result.append(gp_df)

        data_frame_combined_Quick_ratio = pd.concat(list_every_stock_result)
        return data_frame_combined_Quick_ratio

    def clean_up_data_frame(self, dataframe: pd.DataFrame, ratio: str) -> pd.DataFrame:
        """
            Cleans up dataframe. Operations include:
            (1) Removing empty row/columns
            (2) Computing a mean for each row.

            Args:
                dataframe (pd.Dataframe): Dataframe returned from a financial method operation such as get_operating_profit_margin()
                ratio (str): Ratio for mean row column label. ie 'Gross Profit margin'

            Returns:
                Dataframe: A complete, cleaned up data frame of stocks and relevant financial metric
        """
        data_frame_last_n_periods = dataframe.iloc[:,
                                                                 periods]
        Df_mean_calculation_last_n_periods = data_frame_last_n_periods.mean(
            axis=1)
        data_frame_last_n_periods.insert(0,
                                      f'Mean {ratio} periods shown',
                                      Df_mean_calculation_last_n_periods)
        data_frame_last_n_periods = data_frame_last_n_periods.sort_values(
            by=(f'Mean {ratio} periods shown',), axis=0, ascending=False)
        data_frame_last_n_periods = data_frame_last_n_periods.dropna(
            axis=1, how='all')
        # print(data_frame_last_n_periods)
        print()

        Df_mean_calculation_whole_period = dataframe.mean(axis=1)
        dataframe.insert(0, f'Mean {ratio}',
                                                       Df_mean_calculation_whole_period)
        data_frame = dataframe.sort_values(
            by=(f'Mean {ratio}',), axis=0, ascending=False)
        data_frame = data_frame.dropna(axis=1, how='all')
        data_frame = data_frame.dropna(axis=0, how='all')
        return data_frame


    def compute_results_discontinued(self, dataframe: pd.DataFrame, multiplier: float=1) -> dict:
        """
           Ranks the stocks by their position in the data-frame.
           0 points for stock at index position 0, increasing in increments of 1

           Args:
               dataframe (pd.Dataframe): Dataframe returned from clean_up_data_frame()
               multiplier: A way to give more weight to metric. Index position points multiplied by multiplier.

           Returns:
               Dict: A sorted dictionary of stock and CURRENT ranking points
        """
        Stocks_in_df_for_complete_ranking_of_stocks = list(
            dataframe.index.get_level_values(0))  # get the stocks involved
        points = 0
        for stock in Stocks_in_df_for_complete_ranking_of_stocks:
            try:
                a = Complete_rankings_of_stocks[stock]
                Complete_rankings_of_stocks[stock] += (points * multiplier)
                # print(f'{stock} gained {points} points')
            except Exception:
                Complete_rankings_of_stocks[stock] = (points * multiplier)
                # print(f'{stock} has {points} points')
            points += 1
         # sorted(Complete_rankings_of_stocks.items(), key=lambda x: x[1])
        return Complete_rankings_of_stocks

    def clean_up_data_frame_debt_to_equity(self, dataframe: pd.DataFrame, ratio: str) -> pd.DataFrame:
        """
                   Cleans up dataframe. Operations include:
                   (1) Removing empty row/columns
                   (2) Computing a mean for each row.

                   Args:
                       dataframe (pd.Dataframe): Dataframe returned from a financial method operation such as get_operating_profit_margin()
                       ratio (str): Ratio for mean row column label. ie 'Gross Profit margin'

                   Returns:
                       Dataframe: A complete, cleaned up data frame of stocks and relevant financial metric

                   Note:
                        Method slightly differs from clean_up_data_frame()
                        Debt to equity is different to many other valuation ratios:
                        Smaller positive number is better than a bigger positive number
                        But a negative number is bad. How bad are negative numbers relative to large positive?
                        Hard to say but for the purpose of this data-frame negative numbers are pushed to the bottom.

                   Thus:
                        Ascending=
        """
        data_frame_last_n_periods = dataframe.iloc[:,
                                    periods]
        Df_mean_calculation_last_n_periods = data_frame_last_n_periods.mean(
            axis=1)
        data_frame_last_n_periods.insert(0,
                                         f'Mean {ratio} periods shown',
                                         Df_mean_calculation_last_n_periods)
        data_frame_last_n_periods = data_frame_last_n_periods.sort_values(
            by=(f'Mean {ratio} periods shown',), axis=0, ascending=True,
            key = lambda Series: Series.where(Series > 0, Series * -100000))
        data_frame_last_n_periods = data_frame_last_n_periods.dropna(
            axis=1, how='all')
        # print(data_frame_last_n_periods)
        print()

        Df_mean_calculation_whole_period = dataframe.mean(axis=1)
        dataframe.insert(0, f'Mean {ratio}',
                         Df_mean_calculation_whole_period)
        data_frame = dataframe.sort_values(
            by=(f'Mean {ratio}',), axis=0, ascending=True,
            key = lambda Series: Series.where(Series > 0, Series * -100000))
        data_frame = data_frame.dropna(axis=0, how='all')
        data_frame = data_frame.dropna(axis=1, how='all')
        return data_frame

class get_insider_share_purchases:

    def __init__(self, stocks: list):
        """
            Class to represent a dataframe of 'insider share purchase' for stocks passed

            Args:
                stocks (list): List of stocks
        """
        self.stocks = stocks
        self.all_insider_purchases_df = []


    def get_insider_share_purchases(self, metric: str, column_label: str=None) -> pd.DataFrame:
        """
            Uses Yfinance to compute an insider share dataframe.

            Args:
                metric (str): 'Trans' or 'Shares'. Trans is no. of transactions by insiders, shares is amount
                column_label (str): Optional. 'Proportion bought numerically' (for Trans)  or 'proportion bought monetarily' (for Shares)

            Returns:
                data frame: A data frame for insider share purchases of stocks provided ranked by proportion of purchases

            Note:
                Proportion of purchases is purchases/ sales + purchases
        """

        for stock in self.stocks:
            ticker = yf.Ticker(stock)
            insider_purchases = ticker.insider_purchases
            insider_purchases = insider_purchases.loc[(0, 1, 2), ('Insider Purchases Last 6m', f'{metric}')]
            insider_purchases = pd.DataFrame(insider_purchases)
            insider_purchases = insider_purchases.set_index('Insider Purchases Last 6m')
            insider_purchases = insider_purchases.transpose()
            bought = insider_purchases.at[f'{metric}', 'Purchases']
            sold = insider_purchases.at[f'{metric}', 'Sales']
            try:
                calc = (bought / (bought + sold))
                calc=float(calc)
            # calc = float(calc)
                #all positive
                insider_purchases[f'{column_label}'] = calc
                order = [f'{column_label}', 'Purchases', 'Sales', 'Net Shares Purchased (Sold)']
                insider_purchases = insider_purchases[order]
                insider_purchases = insider_purchases.rename({f'{metric}': f'{stock}'})
                insider_purchases = insider_purchases.rename_axis(index='Stock', columns='Purchase Metrics')
                # print(insider_purchases)
            except (TypeError, RuntimeWarning) as e :   #Typeerror or runtimeWarning
                    try:
                        calc = -(sold / (sold))
                        calc = float(calc)
                        insider_purchases[f'{column_label}'] = calc
                        order = [f'{column_label}', 'Purchases', 'Sales', 'Net Shares Purchased (Sold)']
                        insider_purchases = insider_purchases[order]
                        insider_purchases = insider_purchases.rename({f'{metric}': f'{stock}'})
                        insider_purchases = insider_purchases.rename_axis(index='Stock', columns='Purchase Metrics')
                    except (TypeError, RuntimeWarning) as e:
                            print('error', '0/0')
                            insider_purchases[f'{column_label}'] = 0
                            order = [f'{column_label}', 'Purchases', 'Sales', 'Net Shares Purchased (Sold)']
                            insider_purchases = insider_purchases[order]
                            insider_purchases = insider_purchases.rename({f'{metric}': f'{stock}'})
                            insider_purchases = insider_purchases.rename_axis(index='Stock', columns='Purchase Metrics')
            self.all_insider_purchases_df.append(insider_purchases)

        data_frame_combined = pd.concat(self.all_insider_purchases_df)
        data_frame_combined = data_frame_combined.sort_values(
            by=f'{column_label}', axis=0, ascending=False)
        return data_frame_combined

class get_analyst_recommendations:
    def __init__(self, stocks: list):
        """
            Class to represent a dataframe of analyst recommendations for stocks passed

            Args:
                stocks (list): List of stocks
        """
        self.stocks = stocks
        self.all_analyst_recommendations_df = []

    def get_analyst_recommendations(self) -> pd.DataFrame:
        """
            Uses Yfinance to compute an analyst recommendations dataframe.

            Args:
                metric (str): 'Trans' or 'Shares'. Trans is no. of transactions by insiders, shares is amount
                column_label (str): Optional. 'Proportion bought numerically' (for Trans)  or 'proportion bought monetarily' (for Shares)

            Returns:
                data frame: A data frame for analyst recommendations of stocks provided ranked by proportion of positive reviews

            Note:
                Proportion of purchases is purchases/ sales + purchases
        """

        for stock in self.stocks:
            ticker = yf.Ticker(stock)
            recommendations = ticker.recommendations
            if recommendations.empty:
                stock_no_recommendations.add(stock)
            else:
                recommendations['Total recommendations'] = recommendations.sum(axis=1, numeric_only=True)
                recommendations['Total strongBuy/buy'] = recommendations.loc[:,('strongBuy','buy')].sum(axis=1)
                recommendations = recommendations.transpose()
                recommendations[f'{stock}'] = recommendations.loc[('strongBuy','buy','hold','sell','strongSell','Total recommendations','Total strongBuy/buy'),:].sum(axis=1)
                recommendations = recommendations.transpose()
                no_of_months = len(recommendations.index.get_level_values(0))-1
                recommendations = recommendations.rename_axis(columns=f'Analyst reviews past {no_of_months} months', index='Stock')
                recommendations = pd.DataFrame(recommendations)
                recommendations = recommendations.loc[(f'{stock}',), ('strongBuy','buy','hold','sell','strongSell','Total recommendations','Total strongBuy/buy')]
                recommendations['Proportion of positive analyst reviews'] = recommendations.loc[:,'Total strongBuy/buy'] / recommendations.loc[:,'Total recommendations']
                order = ['Proportion of positive analyst reviews','strongBuy', 'buy','hold','sell','strongSell','Total recommendations','Total strongBuy/buy']
                recommendations = recommendations[order]
                self.all_analyst_recommendations_df.append(recommendations)

        data_frame_combined = pd.concat(self.all_analyst_recommendations_df)
        data_frame_combined = data_frame_combined.sort_values(
        by=f'Proportion of positive analyst reviews', axis=0, ascending=False)
        return data_frame_combined

class Rank_data_frame:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def compute_results_linear(self, multiplier: float=1, stocks_chosen: str='all') -> dict:
        """
           Ranks the stocks by their position in the data-frame.
           0 points for stock at index position 0, increasing in increments of 1

           Args:
               multiplier: A way to give more weight to metric. Index position points multiplied by multiplier.
               stocks_chosen: 'all' refers to Complete_ranking_of_stocks_dict
                              'some' refers to Complete_ranking_of_stocks_dict_top_n

           Returns:
               Dict: A sorted dictionary of stock and CURRENT ranking points
        """
        if stocks_chosen == 'all':
            Stocks_in_df_for_complete_ranking_of_stocks = list(
                self.dataframe.index.get_level_values(0))  # get the stocks involved
            points = 0
            for stock in Stocks_in_df_for_complete_ranking_of_stocks:
                try:
                    a = Complete_rankings_of_stocks[stock]
                    Complete_rankings_of_stocks[stock] += (points * multiplier)
                    # print(f'{stock} gained {points} points')
                except Exception:
                    Complete_rankings_of_stocks[stock] = (points * multiplier)
                    # print(f'{stock} has {points} points')
                points += 1
             # sorted(Complete_rankings_of_stocks.items(), key=lambda x: x[1])
            return Complete_rankings_of_stocks

        elif stocks_chosen == 'some':
            Stocks_in_df_for_complete_ranking_of_stocks = list(
                self.dataframe.index.get_level_values(0))  # get the stocks involved
            points = 0
            for stock in Stocks_in_df_for_complete_ranking_of_stocks:
                try:
                    a = Complete_rankings_of_stocks_top_n[stock]
                    Complete_rankings_of_stocks_top_n[stock] += (points * multiplier)
                    # print(f'{stock} gained {points} points')
                except Exception:
                    Complete_rankings_of_stocks_top_n[stock] = (points * multiplier)
                    # print(f'{stock} has {points} points')
                points += 1
            return Complete_rankings_of_stocks_top_n
            # sorted(Complete_rankings_of_stocks.items(), key=lambda x: x[1])
        else:
            raise SystemError('You need to choose some or all')

class Excel():
    list_excel_writer = []
    sheet_name_list = []

    @staticmethod
    def prepare_to_send_to_excel(df: pd.DataFrame,sheet_name: str,sheet_name_list=sheet_name_list,list_excel_writer=list_excel_writer):
        """
           Appends the Data-frame provided to a list (list is not part of any instantiation, thus does not reset)

           Args:
               df: Panda's data frame
               list_excel_writer: **don't change** - passes the object list_excel_writer to the method
        """
        list_excel_writer.append(df)
        sheet_name_list.append(sheet_name)

    @staticmethod
    def send_to_excel(path: str='Write_a_df_to_me_2.0.xlsx',list_excel_writer=list_excel_writer, sheet_name_list=sheet_name_list):
        """
           Sends each data frame in list_excel_writer to an Excel file with each name in the same index position in sheet_name_list
        """
        with pd.ExcelWriter(path=path) as writer:
            for i in range(len(list_excel_writer)):
                list_excel_writer[i].to_excel(writer, sheet_name=sheet_name_list[i],na_rep='N/A', header=True, index=True,
                startrow=0, startcol=0, merge_cells=False)

class Matplotlib():

    def Show_yfinance_data_frame(self, df: pd.DataFrame, ratio: str, percent_value: str='yes', y_axis_label: str= 'value'):
        """
          Computes a matplotlib bar chart for data frame passed
          Lists values for each year-end (or nearest estimate) and overall average

          Args:
              df: Yfinance Pandas data frame recruited from class Get_financial_metrics
              ratio: The financial metric which is the focus of data frame passed. Will be used for graph title
              percent_value: 'yes' or 'no'.
              'yes' means values range from 0 to 1 in a percentage esque format ie.Net profit margin
              'no' means values are not scaled from 0 to 1 in such a way ie.FCFE
              y_axis_label: label for y axis
        """
        title = f'{ratio}'
        plt.close()
        y_label_graph = [y_axis_label]
        Name_of_average_column = f'Mean {ratio}' # CHANGE
        loop = 0
        y_line_across_grid = 0
        # DROP N/A rows & columns
        df = df.dropna(axis=1, how='all')
        df = df.dropna(axis=0, how='all')
        # Move index level 0 to columns (ie. the stocks)
        df = df.unstack(level=[0])
        # Move the dates and the average to the index
        df = df.stack(level=0, future_stack=True)
        # Drop Index level 1 as gives the metric, not needed
        df = df.droplevel(level=0, axis=0)
        # Get the average row
        df_average_row = df.loc[Name_of_average_column, :]
        # Drop the average row
        df = df.drop(index=Name_of_average_column)
        # Forward fill columns so NAN previous values are filled with the closest future value
        df = df.ffill(axis=0)
        ##Forward fill columns so NAN previous values are filled with the closest Past value
        df = df.bfill(axis=0)
        # Create a df with average row (stocks on index, FCFE (the average) on columns, values are average FCFE)
        # average row is currently a series
        df_average_row = pd.DataFrame(df_average_row)
        # Switch index and columns so matches df
        df_average_row = df_average_row.transpose()
        # Append average to main data-frame
        df = pd.concat([df, df_average_row]) # df = df._append(df_average_row)
        # Get only year end and average values
        df = df.loc[
             (Name_of_average_column, '2020-12-31', '2021-12-31', '2022-12-31', '2023-12-31'), :
             ]
        # name average column
        df = df.rename(index={Name_of_average_column: 'Average'})
        print(df)

        # create figure
        fig = plt.figure(figsize=(8, 15), facecolor='lightgrey', edgecolor='red', frameon=True,  # set figure
                         layout='constrained')
        rect = mpatches.Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                                  edgecolor='red', facecolor='none', linewidth=5)  # set border
        fig.patches.append(rect)
        ax = fig.subplots(
            subplot_kw={'position': [0.10, 0.15, 0.8, 0.7]})  # set axis (no values yet) & position of axis

        # create axis
        basic_css_colors = [
            'Red',
            'Green',
            'Blue',
            'Yellow',
            'Cyan',
            'Magenta',
            'Black',
            'Gray',
            'Maroon',
            'Orange',
            'Olive',
            'Purple',
            'Teal',
            'Navy',
            'Silver',
            'Lime',
            'Aqua',
            'Fuchsia',
            'Brown'
        ]
        df.plot(figsize=(8, 15), kind='bar', ax=ax, color=basic_css_colors)

        # add stuff

        # text
        # ax.text(0.8, 0.8, 'Please do not take from office', transform=ax.transAxes,
        #         ha="center", va="center", fontsize=10, color="darkgrey", fontweight='extra bold')

        # major ticker, split y axis into 5 parts. Minor ticker, 20 parts
        if percent_value == 'yes':
            ax.yaxis.set_major_formatter(Tticker.PercentFormatter(xmax=1))    #percent formatter for percent values
        else:
            ax.set_yticklabels(
            [format(x, '.2e') for x in ax.get_yticks()])  # scientific notation for non percent values
        ax.yaxis.set_major_locator(Tticker.LinearLocator(5))
        ax.yaxis.set_minor_locator(Tticker.LinearLocator(20))

        # legend and other labels
        legend_values = df.columns.get_level_values(level=0)
        ax.legend(legend_values, loc='upper right', bbox_to_anchor=(0.95, 1.1, 0.1, 0.1), fontsize='small',
                  labelcolor='grey', ncol=3)
        ax.set_title(f'{title}', loc='center', fontstyle='oblique', fontsize='medium')
        ax.set_ylabel(y_label_graph[0])

        # background colour of axis
        ax.set_facecolor('whitesmoke')

        # line at some data point
        # y_tick_position = y_line_across_grid
        # ax.axhline(y=y_tick_position, color='red', linestyle='--', linewidth=1)        #line across from tick on y axis
        plt.show()


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
                 'Communication Services': ['CHTR', 'CMCSA', 'DIS', 'EA', 'FOX', 'GOOGL', 'IPG', 'LUMN', 'LYV', 'NFLX', 'OMC', 'PARA', 'T', 'TMUS', 'TTWO', 'VZ']}
no_sector_stocks = {'No Sector': ['ABC', 'ABMD', 'ATVI', 'BF.B', 'BLL', 'BRK.B', 'CDAY', 'CTXS', 'DISCA', 'DISCK', 'DISH', 'DRE', 'FBHS', 'FISV', 'FLIR', 'FLT', 'FRC', 'HFC', 'INFO', 'KSU', 'NLOK', 'PBCT', 'PEAK', 'PKI', 'PXD', 'RE', 'SIVB', 'TWTR', 'VIAC', 'WLTW', 'XLNX']}

#removed
# 'FOXA', 'GOOG'

#metrics done
#Gross/operating/net profit margin  #income
#ROA                                #income + balance
#FCFE                               #cash
#quick ratio                        #balance
#ROE                                #income + balance
#debt-to-equity                     #balance

input_sector = 'Real Estate'
stock_sector_options = ['Healthcare', 'Technology', 'Financial Services', 'Consumer Defensive', 'Industrials',
                        'Utilities', 'Basic Materials', 'Consumer Cyclical', 'Real Estate', 'Energy', 'Communication Services']
stocks_in_sector_chosen = sector_stocks[input_sector]
print(stocks_in_sector_chosen)
print('Sector chosen is', input_sector)

financials_obj = Financials(stocks_in_sector_chosen)   #or stocks_excell
financial_df = financials_obj.get_financials_data_frame()

Financial_metrics_obj = Get_financial_metrics(financial_df)

##################################
#gross profit
Gross_profit_df = Financial_metrics_obj.get_gross_profit_margin()
cleaned_up_gross_profit_df = Financial_metrics_obj.clean_up_data_frame(Gross_profit_df, 'Gross Profit Margin')
print(cleaned_up_gross_profit_df)
compute_results_obj = Rank_data_frame(cleaned_up_gross_profit_df)
stocks_ranked = compute_results_obj.compute_results_linear(0.5)
print(stocks_ranked)

excel_class = Excel()
excel_class.prepare_to_send_to_excel(cleaned_up_gross_profit_df, 'gross profit')


mat_plot_lib_class = Matplotlib()
# mat_plot_lib_class.Show_yfinance_data_frame(cleaned_up_gross_profit_df, 'Gross Profit Margin')




# operating profit
Operating_profit_df = Financial_metrics_obj.get_operating_profit_margin()
cleaned_up_operating_profit_margin = Financial_metrics_obj.clean_up_data_frame(Operating_profit_df, 'Operating Profit Margin')
print(cleaned_up_operating_profit_margin)
compute_results_obj = Rank_data_frame(cleaned_up_operating_profit_margin)
stocks_ranked = compute_results_obj.compute_results_linear(0.5)
print(stocks_ranked)

excel_class.prepare_to_send_to_excel(cleaned_up_operating_profit_margin, 'operating profit')
# mat_plot_lib_class.Show_yfinance_data_frame(cleaned_up_operating_profit_margin, 'Operating Profit Margin')



#net profit
net_profit_df = Financial_metrics_obj.get_net_profit_margin()
cleaned_up_net_profit_margin = Financial_metrics_obj.clean_up_data_frame(net_profit_df, 'Net Profit Margin')
print(cleaned_up_net_profit_margin)
compute_results_obj = Rank_data_frame(cleaned_up_net_profit_margin)
stocks_ranked = compute_results_obj.compute_results_linear(0.5)
print(stocks_ranked)

excel_class.prepare_to_send_to_excel(cleaned_up_net_profit_margin, 'net profit')
# mat_plot_lib_class.Show_yfinance_data_frame(cleaned_up_net_profit_margin, 'Net Profit Margin')

#ROA
ROA_df = Financial_metrics_obj.get_ROA()
cleaned_up_ROA = Financial_metrics_obj.clean_up_data_frame(ROA_df, 'ROA')
print(cleaned_up_ROA)
compute_results_obj = Rank_data_frame(cleaned_up_ROA)
stocks_ranked = compute_results_obj.compute_results_linear(2)
print(stocks_ranked)

excel_class.prepare_to_send_to_excel(cleaned_up_ROA, 'ROA')

#ROE
ROE_df = Financial_metrics_obj.get_ROE()
cleaned_up_ROE = Financial_metrics_obj.clean_up_data_frame(ROE_df, 'ROE')
print(cleaned_up_ROE)
compute_results_obj = Rank_data_frame(cleaned_up_ROE)
stocks_ranked = compute_results_obj.compute_results_linear(2)
print(stocks_ranked)

excel_class.prepare_to_send_to_excel(cleaned_up_ROE, 'ROE')

#FCFE
FCFE_df = Financial_metrics_obj.get_FCFE()
cleaned_up_FCFE = Financial_metrics_obj.clean_up_data_frame(FCFE_df, 'FCFE')
print(cleaned_up_FCFE)
compute_results_obj = Rank_data_frame(cleaned_up_FCFE)
stocks_ranked = compute_results_obj.compute_results_linear()
print(stocks_ranked)

excel_class.prepare_to_send_to_excel(cleaned_up_FCFE, 'FCFE')
# mat_plot_lib_class.Show_yfinance_data_frame(cleaned_up_FCFE, 'FCFE', percent_value='no')

#debt-to-equity
D_E_df = Financial_metrics_obj.get_debt_to_equity()
cleaned_up_D_E = Financial_metrics_obj.clean_up_data_frame_debt_to_equity(D_E_df, 'DE')
print(cleaned_up_D_E)
compute_results_obj = Rank_data_frame(cleaned_up_D_E)
stocks_ranked = compute_results_obj.compute_results_linear(2)
print(stocks_ranked)

excel_class.prepare_to_send_to_excel(cleaned_up_D_E, 'debt-to-equity')

#quick ratio
quick_ratio_df = Financial_metrics_obj.get_quick_ratio()
cleaned_up_quick_ratio = Financial_metrics_obj.clean_up_data_frame(quick_ratio_df, 'quick ratio')
print(cleaned_up_quick_ratio)
compute_results_obj = Rank_data_frame(cleaned_up_quick_ratio)
stocks_ranked = compute_results_obj.compute_results_linear(0.5)
print(stocks_ranked)

excel_class.prepare_to_send_to_excel(cleaned_up_quick_ratio, 'quick ratio')

# cash ratio
cash_ratio_df = Financial_metrics_obj.get_cash_ratio()
cleaned_up_cash_ratio = Financial_metrics_obj.clean_up_data_frame(cash_ratio_df, 'cash ratio')
print(cleaned_up_cash_ratio)
compute_results_obj = Rank_data_frame(cleaned_up_cash_ratio)
stocks_ranked = compute_results_obj.compute_results_linear(0.5)
print(stocks_ranked)

excel_class.prepare_to_send_to_excel(cleaned_up_cash_ratio, 'cash ratio')


#send to excel
excel_class.send_to_excel()


#Conclusions which should always be at bottom of page
def Conclusions_financial_statements(Complete_rankings_of_stocks,n):
    """

    :param Complete_rankings_of_stocks (dict): Tuples of stocks and associated ranking points
    :param n: top 'n' stocks to analyse explicitly
    :return:
    """
    print()
    print('For all stocks:')
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
    print('NO INFO ON CASH AND CURRENT LIABILITIES', stock_no_info_on_cash_and_current_liabilities)
    print('NO INFO ON CASH OR CURRENT LIABILITIES', stock_no_info_on_cash_or_current_liabilities)
    Complete_rankings_of_stocks = sorted(Complete_rankings_of_stocks.items(), key=lambda x: x[1])
    print()
    print(f'Based on ROA, FCFE, Quick ratio, ROE, debt-to-equity, the best stocks in {input_sector} are: ')
    print(Complete_rankings_of_stocks)
    print()
    print('total stocks', len(sector_stocks[input_sector])+1)  #think +1 is dummy stock now removed for df's
    print()

    #change n to analyse 2/3 stocks
    n = n
    print(f'For top {n} stocks: ')
    for (stock,points) in Complete_rankings_of_stocks[:n]:
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
        if stock in stock_no_info_on_cash_and_current_liabilities:
            print(f'{stock} no info on cash and current liabilities')
        if stock in stock_no_info_on_cash_or_current_liabilities:
            print(f'{stock} no info on cash or current liabilities')
    return Complete_rankings_of_stocks #change to fcfe/no fcfe

no_of_stocks_to_analyse_explicitly = 15
Complete_rankings_of_stocks = Conclusions_financial_statements(Complete_rankings_of_stocks,n=no_of_stocks_to_analyse_explicitly)




#further analysis with other metrics
top_15_stocks = Complete_rankings_of_stocks[:no_of_stocks_to_analyse_explicitly]
top_15_stocks_list = []
for (stock,points) in top_15_stocks:
    top_15_stocks_list.append(stock)


#insider purchases numeracy
input(f'For further analysis on the top {no_of_stocks_to_analyse_explicitly} stocks in {input_sector}, press enter: ')
insider_share_purchases_obj = get_insider_share_purchases(top_15_stocks_list)  #change list
insider_share_purchases = insider_share_purchases_obj.get_insider_share_purchases(metric='Trans', column_label='Proportion bought numerically')
print(insider_share_purchases)
compute_results_obj = Rank_data_frame(insider_share_purchases)
stocks_ranked = compute_results_obj.compute_results_linear(stocks_chosen='some')
print(stocks_ranked)

#insider purchases monetary
insider_share_purchases_obj_2 = get_insider_share_purchases(top_15_stocks_list)   #change list
insider_share_purchases = insider_share_purchases_obj_2.get_insider_share_purchases(metric='Shares', column_label='Proportion bought monetarily')
print(insider_share_purchases)
compute_results_obj = Rank_data_frame(insider_share_purchases)
stocks_ranked = compute_results_obj.compute_results_linear(stocks_chosen='some')
print(stocks_ranked)

#analyst recommendations
analyst_recommendations_obj = get_analyst_recommendations(top_15_stocks_list)
analyst_recommendations_obj = analyst_recommendations_obj.get_analyst_recommendations()
print(analyst_recommendations_obj)
compute_results_obj = Rank_data_frame(analyst_recommendations_obj)
stocks_ranked = compute_results_obj.compute_results_linear(stocks_chosen='some')
print(stocks_ranked)


def Conclusions_other_metrics(Complete_rankings_of_stocks_top_n):
    print('*' * 50)
    print('CONCLUSIONS')
    Complete_rankings_of_stocks_top_n = sorted(Complete_rankings_of_stocks_top_n.items(), key=lambda x: x[1])
    print('Other metrics table',Complete_rankings_of_stocks_top_n, sep='\n')
    print('Financials table',Complete_rankings_of_stocks, sep='\n')
    print('NO INFO ON RECOMMENDATIONS', stock_no_recommendations,sep='\n')

x = Conclusions_other_metrics(Complete_rankings_of_stocks_top_n)