from yahoo_fin import stock_info as si
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Define the list of symbols for which you want to estimate the efficient frontier
# symbols = ["SPNO.CO", "ORSTED.CO","DSV.CO"]
#symbols=["DANSKE.CO","DSV.CO","GMAB.CO","AMBU-B.CO","BAVA.CO","FLS.CO","GN.CO","DEMANT.CO","COLO-B.CO","NZYM-B.CO","CHR.CO","TRYG.CO","TOP.CO","JYSK.CO","VWS.CO","ORSTED.CO"]
#symbols=["DSV.CO","NOVO-B.CO","NZYM-B.CO"]
symbols=["DSV.CO","NOVO-B.CO","FLS.CO","SPNO.CO"]
#symbols=["DSV.CO","SPNO.CO"]
# Define the start and end dates for the historical data
start_date = '2023-06-01'
end_date = '2023-08-29'

# Get historical adjusted closing prices for each symbol
# Initialize an empty DataFrame to store the adjusted closing prices
data = pd.DataFrame()
# Fetch data for each symbol and concatenate into the data DataFrame
for symbol in symbols:
    symbol_data = si.get_data(symbol, start_date=start_date, end_date=end_date)['adjclose']
    data = pd.concat([data, symbol_data], axis=1)

# Set column names to be the symbols
data.columns = symbols

# Calculate the returns and covariances
returns = data.pct_change().dropna()
cov_matrix = returns.cov()

# Define the objective function for portfolio optimization
def portfolio_variance(weights, cov_matrix):
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return portfolio_volatility

# Define the constraints for portfolio optimization
cons = ({'type':'eq', 'fun': lambda x: np.sum(x) - 1})

# Define the bounds for portfolio optimization
bounds = [(0, 1)] * len(symbols)

# Initialize the weights for portfolio optimization
weights_init = np.ones(len(symbols)) / len(symbols)

# Optimize for the minimum variance portfolio
result = minimize(portfolio_variance, weights_init, args=(cov_matrix,), constraints=cons, bounds=bounds, method='SLSQP')

# Extract the optimized weights
weights_opt = result.x

# Calculate the optimal portfolio return and volatility
portfolio_return = np.dot(returns.mean(), weights_opt) * 252
portfolio_volatility = np.sqrt(np.dot(weights_opt.T, np.dot(cov_matrix, weights_opt))) * np.sqrt(252)

# Print the optimized weights and portfolio performance
print("Optimized Weights:")
print(symbols)
print(weights_opt)
print("Portfolio Return: {:.2%}".format(portfolio_return))
print("Portfolio Volatility: {:.2%}".format(portfolio_volatility))

# Generate random portfolios for the efficient frontier
num_portfolios = 10000
portfolio_weights = np.zeros((num_portfolios, len(symbols)))
portfolio_returns = np.zeros(num_portfolios)
portfolio_volatilities = np.zeros(num_portfolios)

for i in range(num_portfolios):
    weights = np.random.random(len(symbols))
    weights /= np.sum(weights)
    portfolio_weights[i] = weights
    portfolio_returns[i] = np.dot(returns.mean(), weights) * 252
    portfolio_volatilities[i] = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)

# Plot the efficient frontier
plt.figure(figsize=(12, 6))
plt.scatter(portfolio_volatilities, portfolio_returns, c=portfolio_returns / portfolio_volatilities, marker='o', cmap='coolwarm')
plt.colorbar(label='Sharpe Ratio')
plt.scatter(portfolio_volatility, portfolio_return, c='red', marker='x', s=100, label='Optimized Portfolio')
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.title('Efficient Frontier')
plt.legend()
plt.show()
print("!")
