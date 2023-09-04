# import required libraries
from yahoo_fin import stock_info as si
import pandas as pd
import matplotlib.pyplot as plt

# set the stock symbols and timeframe
stock_symbols=["DSV.CO","NOVO-B.CO","FLS.CO","SPNO.CO"]
start_date = "2023-01-01"
end_date = "2023-07-10"

# retrieve the stock price data for the specified stocks
stock_data = pd.DataFrame()
for symbol in stock_symbols:
    data = si.get_data(symbol, start_date=start_date, end_date=end_date)
    stock_data[symbol] = data['close']

# calculate the difference in price between each day
delta = stock_data.diff()

# get the positive and negative gains (up-closes and down-closes)
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

# set the time period (x) for RSI calculation
x = 14

# calculate the average gain and loss over the specified time period
average_gain = gain.rolling(x).mean()
average_loss = loss.rolling(x).mean()

# calculate the relative strength (RS)
relative_strength = average_gain / average_loss

# calculate the RSI using the relative strength
RSI = 100 - (100 / (1 + relative_strength))

# calculate the 50-day and 200-day moving averages for each stock
moving_averages = stock_data.rolling(window=50).mean()

# plot the stock prices and RSI for each stock
fig, axs = plt.subplots(3, sharex=True, figsize=(10,8))
axs[0].plot(stock_data.index, stock_data[stock_symbols[0]], label=stock_symbols[0])
axs[0].plot(stock_data.index, stock_data[stock_symbols[1]], label=stock_symbols[1])
axs[0].plot(stock_data.index, stock_data[stock_symbols[2]], label=stock_symbols[2])
axs[0].plot(stock_data.index, stock_data[stock_symbols[3]], label=stock_symbols[3])

axs[0].legend()
axs[0].set_title('Stock Prices')
axs[1].plot(RSI.index, RSI[stock_symbols[0]], label=stock_symbols[0])
axs[1].plot(RSI.index, RSI[stock_symbols[1]], label=stock_symbols[1])
axs[1].plot(RSI.index, RSI[stock_symbols[2]], label=stock_symbols[2])
axs[1].plot(RSI.index, RSI[stock_symbols[3]], label=stock_symbols[3])
axs[1].legend()
axs[1].set_title('RSI Momentum indicator')
axs[2].plot(moving_averages.index, moving_averages[stock_symbols[0]], label=stock_symbols[0])
axs[2].plot(moving_averages.index, moving_averages[stock_symbols[1]], label=stock_symbols[1])
axs[2].plot(moving_averages.index, moving_averages[stock_symbols[2]], label=stock_symbols[2])
axs[2].plot(moving_averages.index, moving_averages[stock_symbols[3]], label=stock_symbols[3])
axs[2].legend()
axs[2].set_title('Moving Averages')
plt.tight_layout()
plt.show()
print("hej")
