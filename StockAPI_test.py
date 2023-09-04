from yahoo_fin import stock_info as si
import matplotlib.pyplot as plt

# set the stock symbol and timeframe
stock_symbols = ["SPNO.CO", "ROCK-B.CO","ORSTED.CO"]
start_date = "2020-01-01"
end_date = "2023-04-14"

# retrieve the stock price data
stock_data_1 = si.get_data(stock_symbols[0], start_date=start_date, end_date=end_date)
stock_data_2 = si.get_data(stock_symbols[1], start_date=start_date, end_date=end_date)
stock_data_3 = si.get_data(stock_symbols[2], start_date=start_date, end_date=end_date)
# calculate the 50-day moving average for each stock
stock_data_1["MA50"] = stock_data_1["close"].rolling(window=50).mean()
stock_data_2["MA50"] = stock_data_2["close"].rolling(window=50).mean()
stock_data_3["MA50"] = stock_data_3["close"].rolling(window=50).mean()

# plot the stock price data
plt.plot(stock_data_1["close"])
plt.plot(stock_data_1["MA50"])
plt.plot(stock_data_2["close"])
plt.plot(stock_data_2["MA50"])
plt.plot(stock_data_3["close"])
plt.plot(stock_data_3["MA50"])
plt.xlabel("Date")
plt.ylabel("Stock Price ($)")
plt.title("Stock Prices")
plt.legend(stock_symbols + [f"{symbol} MA50" for symbol in stock_symbols])
plt.show()