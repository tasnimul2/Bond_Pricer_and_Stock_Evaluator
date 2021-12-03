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