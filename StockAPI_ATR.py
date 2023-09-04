# Import the required libraries
import pandas as pd
from yahoo_fin import stock_info as si

# Define the stock symbol and timeframe
stock_symbol = "SPNO.CO"
# stock_symbols = ["SPNO.CO", "ROCK-B.CO","ORSTED.CO"]
start_date = "2020-01-01"
end_date = "2023-04-14"
period = 14 # The number of days used to calculate the ATR

# Retrieve the stock price data for the specified stock
stock_data = si.get_data(stock_symbol, start_date=start_date, end_date=end_date)

# Calculate the True Range (TR) for each day
high = stock_data["high"]
low = stock_data["low"]
close = stock_data["adjclose"]
tr = pd.DataFrame(index=stock_data.index, columns=["TR"])
tr.iloc[0]["TR"] = high.iloc[0] - low.iloc[0]
for i in range(1, len(stock_data)):
    tr.iloc[i]["TR"] = max(high.iloc[i] - low.iloc[i], abs(high.iloc[i] - close.iloc[i-1]), abs(low.iloc[i] - close.iloc[i-1]))

# Calculate the Average True Range (ATR) over the given period
atr = pd.DataFrame(index=stock_data.index, columns=["ATR"])
atr.iloc[period-1]["ATR"] = tr["TR"].rolling(window=period).mean().iloc[period-1]
for i in range(period, len(stock_data)):
    atr.iloc[i]["ATR"] = ((period-1)*atr.iloc[i-1]["ATR"] + tr.iloc[i]["TR"]) / period

print(atr.tail()) # Print the last 5 ATR values
