# :chart_with_upwards_trend: Bond Pricer and Stock Evaluator :chart_with_downwards_trend:

### How to use the app:
1. Clone the github repo
2. populate the StockUniverse.csv file with stock ticker and estimated EPS for the next 5Y (in percent)
3. run the program using: `python run_analysis.py`
4. Wait for the program to indicate completion
5. StockUniverseOutput.csv is populated with the evaluator 

### For the Stock Evalutator:
-  The input is a CSV file with  stock ticker symbol and the EPS Next 5Y (in percent) from finviz 
- The output is a CSV file with DCF value, 	Current Price,	Sector, 	Market Cap, 	Beta, 	Total Assets, 	Total Debt, 	Free Cash Flow, 	P/E Ratio, 	P/S Ratio, and the last 5 prices in the  	RSI, 	10 day EMA, 	20 day SMA, 	50 day SMA, 	200 day SMA

[Sample input for Stock Evalution](https://github.com/tasnimul2/Bond_Pricer_and_Stock_Evaluator/blob/main/StockUniverse.csv)

[Sample output for Stock Evalution](https://github.com/tasnimul2/Bond_Pricer_and_Stock_Evaluator/blob/main/StockUniverseOutput.csv)

```
NOTE : Some outputs for the stock evlaution are not accurate due to the YahooFinancials API not having suffient data. (It is an old API that is no longer supported)
```

## [Bond Pricer](https://github.com/tasnimul2/Bond_Pricer_and_Stock_Evaluator/blob/main/CF_Fall21_finalProject.ipynb) 

[Python code used to implement the bond pricier](https://github.com/tasnimul2/Bond_Pricer_and_Stock_Evaluator/blob/main/bond_calculator.py)


# Stock Price Data and Technical Indicators Visulaization

[The python code used to implement the Technical Indicators can be found here](https://github.com/tasnimul2/Bond_Pricer_and_Stock_Evaluator/blob/main/TA.py) 

```
Note : The stock charts do not show up on the jupyter notebook (under the "Part 2: Technical Indicators" heading) in Github repository hence, here are some samples:   
```
### Stock Price Chart Example: 
![](https://i.imgur.com/fqnLMeG.png)

### Moving Averages Technical Indicators (SMA & EMA):

![](https://i.imgur.com/nQLGbay.png)

### RSI Technical indicator for VZ stock
![](https://i.imgur.com/5BnwEsI.png)


