# Import the required libraries
import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si
import matplotlib.pyplot as plt

# Define the stock symbol and timeframe
stock_symbol = "ORSTED.CO"
# stock_symbols = ["SPNO.CO", "ROCK-B.CO","ORSTED.CO"]
start_date = "2020-01-01"
end_date = "2023-04-14"

# Retrieve the stock price and volume data for the specified stock
stock_data = si.get_data(stock_symbol, start_date=start_date, end_date=end_date)

# Calculate the daily price change and daily volume change
daily_price_change = stock_data['adjclose'].pct_change()
daily_volume_change = stock_data['volume'].pct_change()

# Calculate the PVI and NVI
pvi = pd.Series(1000, index=stock_data.index)
nvi = pd.Series(1000, index=stock_data.index)
for i in range(1, len(stock_data)):
    if daily_volume_change.iloc[i] > 0:
        pvi.iloc[i] = pvi.iloc[i-1] + (daily_price_change.iloc[i] / daily_volume_change.iloc[i]) * pvi.iloc[i-1]
        nvi.iloc[i] = nvi.iloc[i-1]
    else:
        pvi.iloc[i] = pvi.iloc[i-1]
        nvi.iloc[i] = nvi.iloc[i-1] + (daily_price_change.iloc[i] / daily_volume_change.iloc[i]) * nvi.iloc[i-1]

# Plot the stock price along with the PVI and NVI
fig, ax = plt.subplots(figsize=(15,10))
ax.plot(stock_data.index, stock_data['adjclose'], label="Stock Price")
ax.plot(pvi.index, pvi, label="PVI")
ax.plot(nvi.index, nvi, label="NVI")
ax.legend(loc="upper left")
ax.set_title("Stock Price with PVI and NVI")
