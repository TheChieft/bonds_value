#importing required libraries
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
import scipy.stats as stats
from sklearn.preprocessing import MinMaxScaler

#getting historic stock data from yfinance
stocks_list = ['AMZN', 'NVDA','TSLA','^GSPC']

data = yf.download(stocks_list, period='5y',interval='1mo')['Adj Close']

# Calculating Daily % change in stock prices
daily_returns = data.pct_change()
daily_returns.iloc[0,:] = 0

# Boxplot of daily returns (in %)
#daily_returns.boxplot(figsize=(6, 5), grid=False)

# Initializing empty dictionaries to save results

beta,alpha = dict(), dict()

# Make a subplot

fig, axes = plt.subplots(1,3, dpi=150, figsize=(15,8))

axes = axes.flatten()

for idx, stock in enumerate(daily_returns.columns.values[:-1]):

    # scatter plot between stocks and the NSE

    daily_returns.plot(kind = "scatter", x = "^GSPC", y = stock, ax=axes[idx])

    # Fit a line (regression using polyfit of degree 1)

    b_, a_ = np.polyfit(daily_returns["^GSPC"], daily_returns[stock], 1)

    regression_line = b_ * daily_returns["^GSPC"] + a_

    axes[idx].plot(daily_returns["^GSPC"], regression_line, "-", color = "r")

    # save the regression coeeficient for the current stock

    beta[stock] = b_
    alpha[stock] = a_
    
plt.show()

keys = list(beta.keys()) # list of stock names

beta_3 = dict()

for k in keys:
    beta_3[k] = [daily_returns[[k,'^GSPC']].cov()/daily_returns['^GSPC'].var()][0].iloc[0,1]
    print(f"el beta de {k}: {beta[k]}")

ER = dict()

rf = 0.0733

trading_days = 250

# Estimate the expected return of the market using the daily returns

rm = daily_returns["^GSPC"].mean() * trading_days

for k in keys:

    # Calculate return for every security using CAPM

    ER[k] = rf + beta[k] * (rm-rf)

for k in keys:

    print("Expected return based on CAPM model for {} is {}%".format(k, round(ER[k], 2)))

# Calculating historic returns

for k in keys:

    print('Return based on historkeysical data for {} is {}%'.format(k, round(daily_returns[k].mean() * trading_days, 2)))