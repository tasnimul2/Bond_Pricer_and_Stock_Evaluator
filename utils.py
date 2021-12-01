'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021

@Student Name  : first last

https://github.com/JECSand/yahoofinancials

'''

from yahoofinancials import YahooFinancials 
import yfinance as yf

class MyYahooFinancials(YahooFinancials):
    '''
    Extended class based on YahooFinancial libary

    '''
    
    def __init__(self, symbol, freq = 'annual'):
        YahooFinancials.__init__(self, symbol)
        self.freq = freq
        self.symbol = symbol

    def get_operating_cashflow(self):
        return self._financial_statement_data('cash', 'cashflowStatementHistory', 'totalCashFromOperatingActivities', self.freq)

    def get_capital_expenditures(self):
        return self._financial_statement_data('cash', 'cashflowStatementHistory', 'capitalExpenditures', self.freq)

    def get_long_term_debt(self):
        return self._financial_statement_data('balance', 'balanceSheetHistory', 'longTermDebt', self.freq)

    def get_account_payable(self):
        return self._financial_statement_data('balance', 'balanceSheetHistory', 'accountsPayable', self.freq)

    def get_total_current_liabilities(self):
        return self._financial_statement_data('balance', 'balanceSheetHistory', 'totalCurrentLiabilities', self.freq)

    def get_other_current_liabilities(self):
        return self._financial_statement_data('balance', 'balanceSheetHistory', 'otherCurrentLiab', self.freq)

    def get_cash(self):
        return self._financial_statement_data('balance', 'balanceSheetHistory', 'cash', self.freq)

    def get_short_term_investments(self):
        return self._financial_statement_data('balance', 'balanceSheetHistory', 'shortTermInvestments', self.freq)
    
    '''def get_marketcap(self):#ERASE AND PUT IN STOCK.PY
        return self.get_market_cap()

    def get_revenue(self):
        return self.get_total_revenue()

    def get_PE_ratio(self):
        return self.get_pe_ratio()

    def get_PS_ratio(self):
        return (self.get_marketcap() / self.get_revenue())

    def get_sector(self):
        stock = yf.Ticker(self.symbol)
        return stock.info['sector']'''


def _test():
    symbol = 'KO'
    
    yfinance = MyYahooFinancials(symbol)

    
    print("Getting Financial Data for {}".format(symbol))
    print("Long Term Debt: ", yfinance.get_long_term_debt())


if __name__ == "__main__":
    _test()
