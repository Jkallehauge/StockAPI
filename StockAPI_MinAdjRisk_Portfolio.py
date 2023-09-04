from yahoo_fin import stock_info as si
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Define the list of symbols for which you want to estimate the efficient frontier
#symbols = ["SPNO.CO", "ORSTED.CO","DSV.CO"]
symbols=["DSV.CO","NOVO-B.CO","SPNO.CO","FLS.CO"]

# Define the start and end dates for the historical data
start_date = '2023-05-01'
end_date = '2023-08-29'

# Define the training and test set periods
# Convert train_start_date and train_end_date to datetime objects
train_start_date = pd.to_datetime('2023-05-01')
train_end_date = pd.to_datetime('2023-08-20')

# Convert test_start_date and test_end_date to datetime objects
test_start_date = pd.to_datetime('2023-08-21')
test_end_date = pd.to_datetime('2023-08-29')

# Fetch data for each symbol and concatenate into the data DataFrame
data = pd.DataFrame()
for symbol in symbols:
    symbol_data = si.get_data(symbol, start_date=start_date, end_date=end_date)['adjclose']
    data = pd.concat([data, symbol_data], axis=1)

# Set column names to be the symbols
data.columns = symbols

# Create training set and test set
train_data = data.loc[train_start_date:train_end_date]
test_data = data.loc[test_start_date:test_end_date]


# Calculate the returns and covariances for training set
train_returns = train_data.pct_change().dropna()
train_cov_matrix = train_returns.cov()

# Perform portfolio optimization using training set
# Define optimization objective function (e.g. portfolio volatility)
def portfolio_volatility(weights, cov_matrix):
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    portfolio_volatility = np.sqrt(portfolio_variance)
    return portfolio_volatility

# Define constraints for optimization (e.g. sum of weights = 1)
cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

# Define bounds for weights (e.g. weights must be between 0 and 1)
bounds = [(0, 1)] * len(symbols)

# Define initial guess for weights (e.g. equal weights)
init_guess = np.array([1/len(symbols)] * len(symbols))

# Optimize portfolio weights using training set
result = minimize(portfolio_volatility, init_guess, args=(train_cov_matrix,),
                  constraints=cons, bounds=bounds, method='SLSQP')

# Extract optimized weights from result
optimal_weights = result.x

# Evaluate portfolio performance on test set
# Calculate returns of the test set
test_returns = test_data.pct_change().dropna()

# Calculate portfolio returns on the test set using optimized weights
portfolio_returns = np.dot(test_returns, optimal_weights)

# Calculate portfolio cumulative returns on the test set
portfolio_cumulative_returns = (portfolio_returns + 1).cumprod() - 1

print("Optimized Weights:")
print(optimal_weights)
# Plot portfolio cumulative returns on the test set
plt.plot(portfolio_cumulative_returns*100)

plt.xlabel('Date')
plt.ylabel('Cumulative Returns [%]')
plt.title('Portfolio Cumulative Returns (Test Set)')
plt.show()
print("Optimized Weights:")
print(optimal_weights)
