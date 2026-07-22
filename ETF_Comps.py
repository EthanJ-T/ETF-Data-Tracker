# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:55:29 2026

@author: Ethan Tsvayg
"""

import yfinance as yf
import pandas as pd
import numpy as np
#libraries needed

test = yf.download("SPY", period="10y")
print(test.head())

test = yf.download("QQQ", period="10y")
print(test.head())
#test if yf works

ETF_Tickers = ["VOO", "QQQ", "SCHD", "IWM", "BND"]
#etfs we are working with 
    
Expense_Ratio = {  
    "VOO":  0.03 / 100,
    "QQQ":  0.18 / 100,
    "SCHD": 0.06 / 100,
    "IWM":  0.19 / 100,
    "BND":  0.03 / 100,
}
#expense ratios as of 7/18/2026

Period = "10y"
Risk_Free = 0.0455
Bear_Market = {
    "COVID": ("2020-02-19", "2020-03-23"),
    "2022_Downturn": ("2022-01-03", "2022-10-12")
    }
#we are looking at data from 07-19-2016 onwards
#risk free is the rate of return someone is expecting if there is 0 default risk
#In here it is the 10 year US Treasury note, which is 0.4551 as of 7/18/2026
#Bear Market = Bad Growth for Market, in the past decade, early COVID in 2020 and 2022 (Russian
#Invasion of Ukraine/Inflation/Oil Crisis, were the 2 biggest bear markets )
    
raw_data = yf.download(ETF_Tickers, period=Period, auto_adjust=True)["Close"]
raw_data = raw_data.dropna(how="all")
daily_returns = raw_data.pct_change().dropna()
print(raw_data.head(10))
print(daily_returns.head(10))    
#check if we can get the data for each day

#functions needed for the project
def annual_return(prices):
    total_return = prices.iloc[-1]/prices.iloc[0]
    years = (prices.index[-1] - prices.index[0]).days / 365.25
    return total_return ** (1/years) - 1
#return of etfs annually

def volatility(returns):
    return returns.std() * np.sqrt(252)
#how volatile is our investment

def sharpe_ratio(annual_ret, annual_vol, risk_free=Risk_Free):
    sharpe = (annual_ret - risk_free) / annual_vol
    return sharpe
#return vs the risk, did you get the value comparison to the risk

def drawdowns(prices):
    max_cumulative = prices.cummax() #pause 
    drawdown = (prices - max_cumulative)/ max_cumulative
    return drawdown.min()
#max between high and low, how big is the diffrence in the year    

def period_return(prices, start, end):
    window = prices.loc[start:end]
    if window.empty:
        return np.nan
    return (window.iloc[-1] / window.iloc[0]) - 1
#Return of the etf through a period

#table for data
results_table = []
for ticker in ETF_Tickers:
    prices = raw_data[ticker].dropna()
    rets = prices.pct_change().dropna()
    
    annual_ret = annual_return(prices)
    annual_vol = volatility(rets)
    sharpe = sharpe_ratio(annual_ret, annual_vol)
    mdd = drawdowns(prices)
    fee = Expense_Ratio.get(ticker, np.nan)
    
    row = {
        "Ticker": ticker,
        "Annual Return (%)": round(annual_ret * 100, 2),
        "Annual Volatility (%)": round(annual_vol * 100, 2),
        "Sharpe Ratio": round(sharpe, 2),
        "Max Drawdown (%)": round(mdd * 100, 2),
        "Expense Ratio (%)": round(fee * 100, 3),
    }

    # add stress-period returns as extra columns
    for label, (start, end) in Bear_Market.items():
        row[label] = round(period_return(prices, start, end) * 100, 2)

    results_table.append(row)
    
ETF_Table = pd.DataFrame(results_table)


print(ETF_Table)
ETF_Table.to_csv("etf_data_table.csv", index=False)
