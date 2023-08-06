import json
from locale import D_FMT
from requests import get
import pandas as pd
import time

class FinanceLoader:
    prefix = "https://apipubaws.tcbs.com.vn/tcanalysis/v1/finance/"
    report_types = ["incomestatement", "cashflow", "balancesheet"]

    def __init__(self, symbol_list, yearly):
        '''
        Initializes a FinanceLoader object.

        Args:
            symbol_list: list of stock tickers
            yearly: 0 for quarterly, 1 for yearly
        '''
        self.symbol_list = symbol_list
        self.yearly = yearly

    def getFinancialReport(self, report_type):
        '''
        Gets the specified financial report for the specified stocks.

        Args:
            report_type: type of financial report to get

        Returns: a pandas DataFrame containing the financial report
        '''
        df = pd.DataFrame()
        for stock in self.symbol_list:
            url = f"{self.prefix}{stock}/{report_type}?yearly={self.yearly}&isAll=true"
            data = json.loads(get(url).text)
            temp = pd.DataFrame.from_dict(data)
            df = pd.concat([df,temp])
        return df

    def getIncomeStatement(self):
        '''
        Gets the income statement for the specified stocks.

        Returns: a pandas DataFrame containing the income statement
        '''
        return self.getFinancialReport(self.report_types[0])

    def getCashflow(self):
        '''
        Gets the cashflow statement for the specified stocks.

        Returns: a pandas DataFrame containing the cashflow statement
        '''
        return self.getFinancialReport(self.report_types[1])

    def getBalanceSheet(self):
        '''
        Gets the balance sheet for the specified stocks.

        Returns: a pandas DataFrame containing the balance sheet
        '''
        return self.getFinancialReport(self.report_types[2])

