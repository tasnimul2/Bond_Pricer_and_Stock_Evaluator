'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Mohammed Chowdhury , Kyle Coleman, Tamzid Chowdhury

@Date          : Nov 2021

Technical Indicators

'''
import enum
import calendar
import math
import pandas as pd
import numpy as np

from datetime import date
'''from scipy.stats import norm'''

from math import log, exp, sqrt

from stock import *

'''Mohammed'''
class SimpleMovingAverages(object):
    '''
    On given a OHLCV data frame, calculate corresponding simple moving averages
    '''
    def __init__(self, ohlcv_df, periods):
        #
        self.ohlcv_df = ohlcv_df
        self.periods = periods
        self._sma = {}

    def _calc(self, period, price_source):
        '''
        for a given period, calc the SMA as a pandas series from the price_source
        which can be  open, high, low or close
        '''
        
        #TODO
        #end TODO
        #period is a list of numbers 
        # price_source is the time during the day that the price comes from (ie. closing / opening price  etc)
        # there is only one column for the data frame, [the stock ticker] ie . self.ohlcv_df['AAPL']
        #doing self.ohlcv_df.iloc[4] is prices (ie. it is the 4th row i nthe daya frame ). [iloc prints rows]
        
        '''the following code means that in the row 'prices' of the dataframe, get the data from the 0th colmn 
         and set it to listOfPriceDicts . Note that this dataframe has a single column named AAPL, which can be accessed 
         by printing 'self.ohlcv_df['AAPL']' or print(self.ohlcv_df). 
         Hence df.loc['prices].values[0] means get 'prices' (row) from 'AAPL' or 0th (col) :
        '''
        listOfPriceDicts = self.ohlcv_df.loc['prices'].values[0];
        source = price_source
        givenPeriod = period
        pricesList = []
        for priceDict in listOfPriceDicts:
             pricesList.append(priceDict.get(source))
        
        ''' Now that we have a list with all the prices, we now need to perform a linear convolution to get the SMA.
        to do linear convolution, we will need 2 lists. The first list, we will call weights , the second list is the PriceList
        with all the prices of the given price_source. This youtube tutorial teaches linear convolution :
        https://www.youtube.com/watch?v=TrgfP7QD3Nk 
        when doing np.convolve, it is simply doing linear convolution under the hood, given 2 lists'''
        
        weights = np.repeat(1.0/givenPeriod,givenPeriod) # this will return a np array of size givenPeriod, with value 1.0/givenPeriod
        sma = np.convolve(pricesList,weights,'valid') # this will perfrom a linear convolution to get the SMA, and return it as numpy array
        result = pd.Series(sma)
        return(result)
        
    def run(self, price_source = 'close'):
        '''
        Calculate all the simple moving averages as a dict
        '''
        for period in self.periods:
            self._sma[period] = self._calc(period, price_source)
    
    def get_series(self, period):
        return(self._sma[period])

'''Mohammed'''
class ExponentialMovingAverages(object):
    '''
    On given a OHLCV data frame, calculate corresponding simple moving averages
    '''
    def __init__(self, ohlcv_df, periods):
        #
        self.ohlcv_df = ohlcv_df
        self.periods = periods
        self._ema = {}

    def _calc(self, period):
        '''
        for a given period, calc the EMA as a pandas series
        '''
        #TODO: implement details here
        #end TODO
        ''' extract the closing price data and put it into a list'''
        listOfPriceDicts = self.ohlcv_df.loc['prices'].values[0];
        source = 'close'
        givenPeriod = period
        pricesList = []
        for priceDict in listOfPriceDicts:
             pricesList.append(priceDict.get(source))
        
        '''
        #np.linspace creates an numpy array of numbers ranging between -1 and 0 ie. array of size 3 consisiting [-1.0,-0.5,0]
        #np.exp takes each element in that array and takes it to the power of e. [e^-1.0,e^-0.5,e^0] = [0.36,0.60,1.0]
        this list is set to a variable called 'weights' , as it is the weight put on priceList to get moving average.
        #then take all of the values in weights , and divide each element in weights by the sum of all values in weights.
        with the adjusted values in weights, calcuate the moving average (using linear convultion) and set it to variable 'ema'
        '''
        weights = np.exp(np.linspace(-1.0,0.0,givenPeriod))
        weights /= weights.sum()
        ema = np.convolve(pricesList,weights,'valid') #calculate moving average, using linear convolution
        ema[:givenPeriod] = ema[givenPeriod] # this will repeat the first 'givenPeriod' elements in the list
        result = pd.Series(ema)
        return(result)
        
    def run(self):
        '''
        Calculate all the Exponential moving averages as a dict
        '''
        for period in self.periods:
            self._ema[period] = self._calc(period)

    def get_series(self, period):
        return(self._ema[period])

'''Tamzid'''
class RSI(object):

    def __init__(self, ohlcv_df, period = 14):
        self.ohlcv_df = ohlcv_df
        self.period = period
        self.rsi = None

    def get_series(self):
        return(self.rsi)

    def run(self):
        '''
        calculate RSI
        '''
        #TODO: implement details here
        gain = []
        loss = []
        list_of_dict = self.ohlcv_df.loc['prices'].values[0]

        for i in range(len(list_of_dict)-14, len(list_of_dict)):
            if (list_of_dict[i]['close']-list_of_dict[i-1]['close'] < 0):
                loss.append(list_of_dict[i]['close']-list_of_dict[i-1]['close'])
            else:
                gain.append(list_of_dict[i]['close']-list_of_dict[i-1]['close'])

        sumLoss = 0
        sumGain = 0

        for j in range(0, len(loss)):
            sumLoss += loss[j]

        for j in range(0, len(gain)):
            sumGain += gain[j]

        avgGain = sumGain/14
        avgLoss = sumLoss/14

        rs = avgGain + avgLoss

        self.rsi = 100 - (100/(1+rs))
        #end TODO
        
'''Kyle'''
class VWAP(object):
    def __init__(self, ohlcv_df):
        self.ohlcv_df = ohlcv_df
        self.vwap = None

    def get_series(self):
        return(self.vwap)

    def run(self):
        '''
        calculate VWAP
        '''
      
        endday = len(self.ohlcv_df.loc['prices'].values[0]) - 1 #length of dictionary to find the last day
        startday = endday - 9
        totalVolume = 0
        totalPriceVolume = 0
        listOfPriceDicts = self.ohlcv_df.loc['prices'].values[0]
        for v in range(startday+1, endday+1):
            totalVolume += listOfPriceDicts[v]['volume']
        for pv in range(startday+1, endday+1):
            totalPriceVolume += listOfPriceDicts[pv]['close'] * listOfPriceDicts[pv]['volume']
        self.vwap = totalPriceVolume / totalVolume
        



def _test():
    # simple test cases
    symbol = 'AAPL'
    stock = Stock(symbol)
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date.today()

    stock.get_daily_hist_price(start_date, end_date)

    periods = [9, 20, 50, 100, 200]
    smas = SimpleMovingAverages(stock.ohlcv_df, periods)
    smas.run()
    s1 = smas.get_series(9)
    print(s1.index)
    print("SMA", s1)

    rsi_indicator = RSI(stock.ohlcv_df)
    rsi_indicator.run()

    print(f"RSI for {symbol} is {rsi_indicator.rsi}")
    
    # mo tests:
    ema = ExponentialMovingAverages(stock.ohlcv_df,periods)
    ema.run()
    s2 = ema.get_series(9)
    #print(s2.index)
    print(s2)
    print("PRINT",s2.tail(5)[474])
    
    # kyle tets
    vwap_indicator = VWAP(stock.ohlcv_df)
    vwap_indicator.run()
    print(f"VWAP for {symbol} in the last {periods[0]} days is {vwap_indicator.vwap}")
    
    
if __name__ == "__main__":
    _test()

