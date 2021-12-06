'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Group : Rocket
@Student Name  : Mohammed Chowdhury, Kyle Coleman, Tamzid Chowdhury

@Date          : June 2021

Discounted Cash Flow Model with Financial Data from Yahoo Financial

https://github.com/JECSand/yahoofinancials


'''
import enum
import calendar
import math
import pandas as pd
import numpy as np

import datetime 
from scipy.stats import norm

from math import log, exp, sqrt

from stock import Stock

'''Mohammed'''
class DiscountedCashFlowModel(object):
    '''
    DCF Model:

    FCC is assumed to go have growth rate by 3 periods, each of which has different growth rate
           short_term_growth_rate for the next 5Y
           medium_term_growth_rate from 6Y to 10Y
           long_term_growth_rate from 11Y to 20thY
    '''

    def __init__(self, stock, as_of_date):
        self.stock = stock
        self.as_of_date = as_of_date

        self.short_term_growth_rate = None
        self.medium_term_growth_rate = None
        self.long_term_growth_rate = None


    def set_FCC_growth_rate(self, short_term_rate, medium_term_rate, long_term_rate):
        self.short_term_growth_rate = short_term_rate
        self.medium_term_growth_rate = medium_term_rate
        self.long_term_growth_rate = long_term_rate


    def calc_fair_value(self):
        '''
        calculate the fair_value using DCF model as follows

        1. calculate a yearly discount factor using the WACC
        2. Get the Free Cash flow
        3. Sum the discounted value of the FCC for the 20 years using similar approach as presented in class
        4. Compute the PV as cash + short term investments - total debt + the above sum of discounted free cash flow
        5. Return the stock fair value of the stock
        '''  
        
        beta = self.stock.get_beta()
        wacc = self.stock.lookup_wacc_by_beta(beta)
        debt = self.stock.get_total_debt()
        cash = self.stock.get_cash_and_cash_equivalent()
        fcc = self.stock.get_free_cashflow()
        shares = self.stock.get_num_shares_outstanding()
        dcf = 0
        start_date = datetime.date(2020, 1, 1)
        end_date = datetime.date.today()
        self.stock.get_daily_hist_price(start_date, end_date)
        listOfPriceDicts = self.stock.ohlcv_df.loc['prices'].values[0]
        #get_cash_and_cash_equivalent()
        #dcf = fcc
        for i in range(1, 20 + 1):
            exp = i
            if (i<6):
                dcf += ((fcc)*(1+self.short_term_growth_rate)**exp)*(1/((1+wacc)**i))
            elif (i>=6 and i<11):
                if(i==6): fcc *= (1+self.short_term_growth_rate)**5
                exp -= 5
                dcf += ((fcc)*(1+self.medium_term_growth_rate)**exp)*(1/((1+wacc)**i))
            elif (i>=11 and i<21):
                if(i==11): fcc *= (1+self.medium_term_growth_rate)**5
                exp -= 10
                dcf += ((fcc)*(1+self.long_term_growth_rate)**exp)*(1/((1+wacc)**i))
        PV = cash + dcf - debt
        result = PV/shares
        return(result)


def _test():
    symbol = 'AAPL'
    as_of_date = datetime.date(2021, 11, 1)

    stock = Stock(symbol)
    model = DiscountedCashFlowModel(stock, as_of_date)
    
    print("Shares ", stock.get_num_shares_outstanding())
    print("FCC ", stock.get_free_cashflow())
    beta = stock.get_beta()
    wacc = stock.lookup_wacc_by_beta(beta)
    print("Beta ", beta)
    print("WACC ", wacc)
    print("Total debt ", stock.get_total_debt())
    print("cash ", stock.get_cash_and_cash_equivalent())
    
    # look up EPS next 5Y from Finviz
    eps5y = 0.1543
    model.set_FCC_growth_rate(eps5y, eps5y/2, 0.04)

    model_price = model.calc_fair_value()
    print(f"DCF price for {symbol} as of {as_of_date} is {model_price}")
    

if __name__ == "__main__":
    _test()