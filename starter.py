import yfinance as yf
import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
import matplotlib.pyplot as plt
# from secrets import FMP_API_TOKEN




## Strategy 1 20/50-Day Moving Average Crossover
# Rules:
# Buy when the 20-day SMA crosses above the 50-day SMA (trend turning bullish).
# Sell when the 20-day SMA crosses below the 50-day SMA (trend turning bearish).
# Stay in cash when not in a trade.

# Define the ticker symbol
ticker_symbol = "AAPL"

# Create a Ticker object
ticker = yf.Ticker(ticker_symbol)

# Fetch historical market data
historical_data = ticker.history(period="2y")  # data for the last year

closedata = historical_data["Close"]
sma20 = historical_data["Close"].rolling(20).mean()
sma50 = historical_data["Close"].rolling(50).mean()




money = 1000
old_diff = np.nan
stocks_owned = 0
valuation = money
buy_dates = []
sell_dates = []
for i in range(len(sma50)-1):
    print(type(historical_data["Open"][i]))
    if pd.notna(sma50[i]):
        diff = (sma20[i] - sma50[i]) > 0
        if pd.isna(old_diff):
            old_diff = diff
        elif old_diff != diff:
            if diff: 
                stocks_owned = money / historical_data["Open"][i+1]
                money = 0
                valuation = stocks_owned * historical_data["Open"][i+1]
                buy_dates.append(historical_data.index[i])
            else:
                money = stocks_owned * historical_data["Open"][i+1]
                valuation = money
                sell_dates.append(historical_data.index[i])
        
            old_diff = diff
                
                
print(money)
print(stocks_owned)
print(valuation)
print(buy_dates)

plt.figure()
plt.plot(historical_data.index, historical_data['Close'], label='Close Price', linewidth=1.5)

# Plot the SMAs
plt.plot(historical_data.index, sma20, label='20-Day SMA', linewidth=1)
plt.plot(historical_data.index, sma50, label='50-Day SMA', linewidth=1)
for date in sell_dates:
    plt.axvline(date, color = 'red')
for date in buy_dates:
    plt.axvline(date, color = 'blue')
plt.show()

