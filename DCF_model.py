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
'''from scipy.stats import norm'''

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
        yearly_discount_factor = 1/(1+wacc)
        freeCashFlow = self.stock.get_free_cashflow()
        dcf = 0
        prevCF =  0;
        cf5 = 0
        cf10 = 0
        year_in_period = 1
        dcf_for_given_year_from_today = []
        dcf_for_given_year_from_today.append(freeCashFlow)
        
        for year in range(1,21):
            if(year <= 5):
                dcf =  freeCashFlow *  (1 + self.short_term_growth_rate)**year_in_period * yearly_discount_factor**year
                year_in_period += 1
                dcf_for_given_year_from_today.append(dcf)
                if(year == 5):
                    cf5 = dcf
                    year_in_period = 1
            elif(year <= 10):
                dcf =  cf5 *  (1 + self.short_term_growth_rate)**year_in_period * yearly_discount_factor**year
                year_in_period +=1
                dcf_for_given_year_from_today.append(dcf)
                if(year == 10):
                    cf10 = dcf
                    year_in_period = 1
            elif(year <= 20):
                dcf =  cf10 *  (1 + self.short_term_growth_rate)**year_in_period * yearly_discount_factor**year
                year_in_period +=1
                dcf_for_given_year_from_today.append(dcf)
                if(year == 20):
                    prevCF = dcf
                    year_in_period = 1
         
                    
        cash_n_srt_trm_invstmnt = self.stock.get_cash_and_cash_equivalent()
        total_debt = self.stock.get_total_debt()
        num_shares = self.stock.get_num_shares_outstanding()
        intrinsic_value = (cash_n_srt_trm_invstmnt + sum(dcf_for_given_year_from_today) - total_debt)/num_shares
        result = intrinsic_value
        
        #TODO
        #end TODO
        
        result = intrinsic_value
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