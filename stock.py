'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Student Name  : 
@Date          : Nov 2021
'''
import enum
import calendar
import math
import pandas as pd
import numpy as np

import datetime 
from scipy.stats import norm

from math import log, exp, sqrt

from utils import MyYahooFinancials 

class Stock(object):
    '''
    Stock class for getting financial statements as well as pricing data
    '''
    def __init__(self, symbol, spot_price = None, sigma = None, dividend_yield = 0, freq = 'annual'):
        self.symbol = symbol
        self.spot_price = spot_price
        self.sigma = sigma
        self.dividend_yield = dividend_yield
        self.yfinancial = MyYahooFinancials(symbol, freq)
        self.ohlcv_df = None

    '''Mohammed'''
    def get_daily_hist_price(self, start_date, end_date):
        '''
        Get daily historical OHLCV pricing dataframe
        '''
        # TODO
        # data = self.yfinancial.get_historical...
        # create a OHLCV data frame
        # self.ohlcv_df =
        #end TODO
        
        # get_historical_price_data() takes in only strings as paramemters. Hence, had to convert start and end date to string
        start_date_as_str = datetime.date.isoformat(start_date);
        end_date_as_str = datetime.date.isoformat(end_date);
        data = self.yfinancial.get_historical_price_data(start_date_as_str, end_date_as_str, "daily")
        self.ohlcv_df = pd.DataFrame(data)
        return self.ohlcv_df;
        

    def calc_returns(self):
        '''
        '''
        self.ohlcv_df['prev_close'] = self.ohlcv_df['close'].shift(1)
        self.ohlcv_df['returns'] = (self.ohlcv_df['close'] - self.ohlcv_df['prev_close'])/ \
                                        self.ohlcv_df['prev_close']


    # financial statements related methods
    '''Mohammed'''
    def get_total_debt(self):
        '''
        return Total debt of the company
        '''
        # total debt = long term liabilities (debt) + current liabilities
        liabilities = self.yfinancial.get_total_current_liabilities()
        debt = self.yfinancial.get_long_term_debt()
        result =  debt + liabilities;
        return(result)

    '''Kyle'''
    def get_free_cashflow(self):
        '''
        return Free Cashflow of the company
        '''

        '''Free Cash Flow = Operating Cash Flow – Capital Expenditure'''
        ocf = self.yfinancial.get_operating_cashflow()
        ce = self.yfinancial.get_capital_expenditures()    
        result = ocf + ce
        # TODO
        # end TODO
        
        return(result)

    '''Kyle'''
    def get_cash_and_cash_equivalent(self):
        '''
        Return cash and cash equivalent of the company
        '''
        result = self.yfinancial.get_cash() + self.yfinancial.get_short_term_investments()


        # TODO
        # end TODO
        return(result)

    '''Tamzid'''
    def get_num_shares_outstanding(self):
        '''
        get current number of shares outstanding from Yahoo financial library
        '''
        result = None
        # TODO
        # end TODO
        return(result)

    '''Tamzid'''
    def get_beta(self):
        '''
        get beta from Yahoo financial
        '''
        result = None
        # TODO
        #result = self.yfinancial.get_beta()
        # end TODO
        return(result)

    '''whoever has time , please do this :) '''
    def lookup_wacc_by_beta(self, beta):
        '''
        lookup wacc by using the table in the DiscountedCashFlowModel lecture powerpoint
        '''
        result = None
        # TODO:
        #end TODO
        return(result)




def _test():
    # a few basic unit tests
    symbol = 'AAPL'
    stock = Stock(symbol)
    print(f"Free Cash Flow for {symbol} is {stock.get_free_cashflow()}")

    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2021, 11, 1)
    stock.get_daily_hist_price(start_date, end_date)
    print(type(stock.ohlcv_df))
    print(stock.ohlcv_df.head())
    #for testing
    print(f"Cash and Cash Equivalent for {symbol} is {stock.get_cash_and_cash_equivalent()}")



if __name__ == "__main__":
    _test()