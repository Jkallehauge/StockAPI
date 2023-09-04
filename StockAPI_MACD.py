    # Import the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from yahoo_fin import stock_info as si

# Define the stock symbol and timeframe
stock_symbol = "SPNO.CO"
# stock_symbols = ["SPNO.CO", "ROCK-B.CO","ORSTED.CO"]
start_date = "2023-01-01"
end_date = "2023-04-18"

# Retrieve the stock price data for the specified stock
stock_data = si.get_data(stock_symbol, start_date=start_date, end_date=end_date)

# Calculate the 26-day and 12-day exponential moving averages (EMAs)
ema_26 = stock_data['close'].ewm(span=26).mean()
ema_12 = stock_data['close'].ewm(span=12).mean()

# Calculate the MACD line
macd_line = ema_12 - ema_26

# Calculate the 9-day EMA of the MACD line
signal_line = macd_line.ewm(span=9).mean()

# Calculate the MACD histogram
macd_histogram = macd_line - signal_line

# Plot the MACD line, signal line, and histogram
fig, axs = plt.subplots(2, sharex=True, figsize=(10,8))
axs[0].plot(stock_data.index, stock_data['close'], label='Stock Price')
axs[0].legend()
axs[0].set_title('Stock Prices')
axs[1].plot(macd_line.index, macd_line, label='MACD Line')
axs[1].plot(signal_line.index, signal_line, label='Signal Line')
axs[1].bar(macd_histogram.index, macd_histogram, width=0.4, label='MACD Histogram')
axs[1].legend()
axs[1].set_title('MACD')
plt.show()
print("if MACD line>Signal line (Buy the stock)")
print("if MACD line<Signal line (Sell the stock)")