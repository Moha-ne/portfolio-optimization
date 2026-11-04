import yfinance as yf
import numpy as np

tickers = ["SHY", "GLD", "KO", "CBOE", "MO", "DBA", "DBMF", "TIP", "VCSH", "PM", "TRV", "MUB", "MNA", "LLY", "ABBV", "IBM", "WMT", "IEF", "JNJ", "V", "AEP", "ALL", "AAPL", "NDAQ", "MSFT"]
benchmark = '^GSPC'

rf_annual = yf.Ticker('^IRX').history(period='5d')['Close'].dropna().iloc[-1] / 100
rf_daily = (1 + rf_annual)**(1/252) - 1

df = yf.Tickers(tickers + [benchmark]).history(period='3y', auto_adjust=True)['Close']

daily_returns = df.pct_change().dropna()
portfolio_returns = daily_returns[tickers].mean(axis=1)   # equal-weight portfolio
market_returns = daily_returns[benchmark]

beta = portfolio_returns.cov(market_returns) / market_returns.var()
alpha_daily = (portfolio_returns.mean() - rf_daily) - beta * (market_returns.mean() - rf_daily)
alpha_annual = (1 + alpha_daily)**252 - 1

print(f"Portfolio Beta: {beta:.4f}")
print(f"Daily Alpha: {alpha_daily:.6%}")
print(f"Annualized Alpha: {alpha_annual:.2%}")




















