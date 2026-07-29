# ETF-Data-Tracker
Using Yfinance to find data on ETF performance over the last 10 years

I wanted to see how a prospective investor would use data and their goals and benchmarks. In this case, we are looking at ETFs, short for Exchange traded funds. These are fund that encompass stocks or bonds based on their sector (for example only tech stocks) or cap size (like the top 500 companies). These are preferred to stocks for more "risk-adverse" investors, due to  Some investor look for long term stability mainly and want an ETF that only returns a small consistent positve return every year. Others want some risk but with some better returns, and others don't care for risk and want to strike it rich. To accomplish this task I used 5 specific ETFs performed over the last 10 year on certain key metrics. The ETFs used were VOO, QQQ, SCHD, IWM and BND. These etfs were picked because they represented different risk levels due to their sector and cap (sizes. VOO tracks the S&P 500 (large cap, no specific sector), QQQ tracks the Nasdaq 100 (large cap tech stocks), SCHD tracks stock that give out dividends (usually large cap, no specific sector), IWM tracks the Russell 2000 index (smaller cap, no specific sector), and BND tracks Bonds (which are much less volatile). These represents the different types of investors, depending on what they want. For example, IWM is better suited for investors that want to "hit it big as soon as possible", who are willing throwing risk away, while BND is more suited for cautious investors that want consistent positive returns over a long period of time.

The metrics used are average return per year, average volatility per year, the sharpe ratio (returns vs volatility), drawdown (the difference between the max and minimum value per year), bear market (COVID) returns and expense ratios. This are the average annual return and volatility, expense ratios and how the ETFs performed during bad financial times, called Bear Markets (such as during 2022). This is important in telling how the ETFs performed over the past decade (from July 2016 to July 2026), and the risk versus reward for these ETFs. The code was done using yfinance, which is a tool that scrapes Yahoo Finance data using their API. I also used Numpy and pandas to help out with financial calculations and work with databases. 

"import yfinance as yf
import pandas as pd
import numpy as np
#libraries needed

test = yf.download("SPY", period="10y")
print(test.head())"

We needed to set some criteria, the time that we are measuring (10 years), the period. The risk free rate is 4.55%, which measured to the US treasury 10 year note, which is considered the safest investment possible. It will be used for calculating the Sharpe Ratio.

Period = "10y"
Risk_Free = 0.0455

To measure each of the different factors I created functions to find the factors, annual volatility and returns are based of the period length and that a year averages out to about 365.25 days. We can look at the annual return of each year, but in this case the average annual return over 10 years.  You look at volatility and ask what's with 252? Tha'ts an odd number. There are about 252 trading days per year on the new York Stock Exchange, so this measured the volatility compared to the returns on a trading day by day scale. Sharpe Ratio takes the 2 values before, and compares it to the risk free ratio, the 10 year US treausry note as stated before. Drawdowns are measured the prices comparing to the maximum value, this is to measured the price comparing the peak per year. Lastly, the period returns are measuring the bear markets (Covid and 2022 downturn due to inflation), to see how these ETFs handle negative markets.
 
def annual_return(prices):
    total_return = prices.iloc[-1]/prices.iloc[0]
    years = (prices.index[-1] - prices.index[0]).days / 365.25
    return total_return ** (1/years) - 1


def volatility(returns):
    return returns.std() * np.sqrt(252)


def sharpe_ratio(annual_ret, annual_vol, risk_free=Risk_Free):
    sharpe = (annual_ret - risk_free) / annual_vol
    return sharpe

def drawdowns(prices):
    max_cumulative = prices.cummax()  
    drawdown = (prices - max_cumulative)/ max_cumulative
    return drawdown.min()

def period_return(prices, start, end):
    window = prices.loc[start:end]
    if window.empty:
        return np.nan
    return (window.iloc[-1] / window.iloc[0]) - 1

Then the code for the functions was used to build the table. The table would fill out by row for each ETF, with the period, risk free rate all set to what was 
The code was transferred to an Excel Spreadsheet and I created a dashboard (using assistance from Google Stitch) to show the data, risk value and for scenairos prospective investors to "match" with their etf of choice.
Python Libraries Used: Yfinance, Numpy, Pandas
