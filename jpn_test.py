import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px

from datetime import date
from dateutil.relativedelta import relativedelta


pricing_date = date(2021, 1, 1)
issue_date = date(2021, 1, 1)

from bond_calculator import *
#from bond_calculator_AP import *
# commented out the bond_calculator_AP import because it it not part of our files.

## Create an Bond Calculator for a pricing date
engine = BondCalculator(pricing_date)

'''We will be using bonds defined Example 2, 3 and 4 of the BondMath notebook. 
We will refer them as bond2, bond3 and bond4 for the rest of the notebook'''

## Fill in the missing code below

# bond2 is a 10Y annual payment bond with 5% coupon & 30/360 daycount
# bond3 is a 2Y semi-annual payment bond with 8% coupon & Actual/360 daycount
# bond4 is a 5Y semi-annual payment bond with 5% coupon & Actual/Actual daycount

bond2 = Bond(issue_date, term=10, day_count = DayCount.DAYCOUNT_30360,
            payment_freq = PaymentFrequency.ANNUAL,
            coupon = 0.05)

#bond3 = Bond(issue_date, ....)
bond3 = Bond(issue_date, term=2, day_count= DayCount.DAYCOUNT_ACTUAL_360, 
             payment_freq= PaymentFrequency.SEMIANNUAL, coupon=0.08)

#bond4 = Bond(...)
bond4 = Bond(issue_date, term=5, day_count= DayCount.DAYCOUNT_ACTUAL_ACTUAL, 
             payment_freq= PaymentFrequency.SEMIANNUAL, coupon=0.08)

''' Question 1: (a) Price bond2 and bond3 at 6% yield. (b) Calculate the yield of bond4 if it is priced at 103.72 '''

yld = 0.06
px_bond2 = engine.calc_clean_price(bond2, yld)
px_bond3 = engine.calc_clean_price(bond3,yld)
print("The clean price of bond 2 is: ", format(px_bond2, '.4f'))
print("The clean price of bond 3 is: ", format(px_bond3, '.4f'))

price = 103.72
yld = engine.calc_yield(bond4, price)
print("The yield of bond 4 is: ", yld)

'''Question 2: Calculate their macaculay and modified duration and convexity at 6% yield'''
# need to come back to this
yld = .06
mDuration2 = engine.calc_macaulay_duration(bond2, yld)
mDuration3 = engine.calc_macaulay_duration(bond3, yld)
mDuration4 = engine.calc_macaulay_duration(bond4, yld)
print("The Macaulay Duration of bond 2 is: ", format(mDuration2, '.4f'))
print("The Macaulay Duration of bond 3 is: ", format(mDuration3, '.4f'))
print("The Macaulay Duration of bond 4 is: ", format(mDuration4, '.4f'))


modDur2 = engine.calc_modified_duration(bond2,yld)
modDur3 = engine.calc_modified_duration(bond3,yld)
modDur4 = engine.calc_modified_duration(bond4,yld)
print("The Modified Duration of bond 2 is: ", format(modDur2, '.4f'))
print("The Modified Duration of bond 3 is: ", format(modDur3, '.4f'))
print("The Modified Duration of bond 4 is: ", format(modDur4, '.4f'))

'''Question 3: Calculate their new price after the yield is moved up by 1 bps'''
yld = 0.0601
px_bond2new = engine.calc_clean_price(bond2, yld)
px_bond3new = engine.calc_clean_price(bond3,yld)
px_bond4new = engine.calc_clean_price(bond4,yld)
print("The new clean price of bond 2 is: ", format(px_bond2new, '.4f'))
print("The new clean price of bond 3 is: ", format(px_bond3new, '.4f'))
print("The new clean price of bond 4 is: ", format(px_bond4new, '.4f'))

'''Question 4: Use their modified duration to estimate what the new price would be if yield is moved up by 1 bps. 
Compare with your answers with those in Question 3'''

# bond price change = - modified duration * change in yield 
bpc2 = -modDur2 * (.0001)
bond2NewPrice = px_bond2 + bpc2

bpc3 = -modDur3 * (.0001)
bond3NewPrice = px_bond3 + bpc3

px_bond4 = engine.calc_clean_price(bond4,.06)
bpc4 = -modDur4 * (.0001)
bond4NewPrice = px_bond4 + bpc4

print("The new price of bond 2 is :",format(bond2NewPrice, '.4f'))
print("The new price of bond 3 is :",format(bond3NewPrice, '.4f'))
print("The new price of bond 4 is :",format(bond4NewPrice, '.4f'))

'''**Question 5: Calculate the accrual interest for each of them if the settle date is March 10, 2021**'''
settle_date = date(2021, 3, 10)
accInterestBond2 = engine.calc_accrual_interest(bond2,settle_date)
accInterestBond3 = engine.calc_accrual_interest(bond3,settle_date)
accInterestBond4 = engine.calc_accrual_interest(bond4,settle_date)
print("The accrual interest of bond 2 is :",format(accInterestBond2, '.4f'))
print("The accrual interest of bond 3 is :",format(accInterestBond3, '.4f'))
print("The accrual interest of bond 4 is :",format(accInterestBond4, '.4f'))

from TA import *
symbol = 'AAPL'
as_of_date = date(2021, 11, 1)
mystock = Stock(symbol)
end_date = as_of_date
start_date = end_date + relativedelta(years = -2)
mystock.get_daily_hist_price(start_date, end_date)
ohlcv_df = mystock.ohlcv_df
prices_df = pd.DataFrame(ohlcv_df.loc['prices'].values[0])
prices_df.head()

'''**First let's plot the stock Candle stick using Plotly**'''

import plotly.graph_objects as go

    
                
candlestick = go.Candlestick(
                            x=prices_df['formatted_date'],
                            open=prices_df['open'], 
                            high=prices_df['high'],
                            low=prices_df['low'],
                            close=prices_df['close'],
                            name = symbol
                            )

traces = []
traces.append(candlestick)

layout = {"title": "{} Price".format(symbol)}
fig = go.Figure(data=traces, layout=layout)

fig.show()

# we will create a SMA object and call its run method
periods = [9, 20, 50, 100, 200]
smas = SimpleMovingAverages(ohlcv_df, periods)
smas.run()

smas.get_series(9)

'''Question 6: Plot 20, 50, 200 Simple Moving Averages and 10 EMA along with the candlesticks'''
emaPeriods = [10]
ema = ExponentialMovingAverages(ohlcv_df,emaPeriods)
ema.run()
fig = go.Figure()

sma20 = go.Scatter(x=prices_df['formatted_date'], 
                            y=smas.get_series(20),name='20')

sma50 = go.Scatter(x=prices_df['formatted_date'], 
                            y=smas.get_series(50),name='sma50')

sma200 = go.Scatter(x=prices_df['formatted_date'], 
                            y=smas.get_series(200),name='sma200')

ema10 = go.Scatter(x=prices_df['formatted_date'], 
                            y=ema.get_series(10),name='ema')

candlestick = go.Candlestick(
                            x=prices_df['formatted_date'],
                            open=prices_df['open'], 
                            high=prices_df['high'],
                            low=prices_df['low'],
                            close=prices_df['close'],
                            name = symbol
                            )

fig.add_trace(sma20)
fig.add_trace(sma50)
fig.add_trace(sma200)
fig.add_trace(ema10)
fig.add_trace(candlestick)

fig.show()
fig = go.Figure()

