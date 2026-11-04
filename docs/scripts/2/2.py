import numpy as np
import pandas as pd
import yfinance as yf

tickers = ["PGR", "LLY", "JPM", "MU", "BRK-B", "RTX", "PLTR", "CVNA", "GE", "TMUS", "WMT", "CRWD", "GOOGL", "TSM", "IBKR", "AAPL", "GS", "PWR", "SPOT", "NVDA", "COST", "RCL", "GLD", "GDX", "NEM"]

benchmark = "SPY"

data = yf.Tickers(tickers + [benchmark]).history(period="3y", auto_adjust=True)['Close']

missing = [t for t in tickers + [benchmark] if t not in data.columns]
if missing:
    raise ValueError(f"Missing data for: {missing}")

prices = data[tickers]
market = data[benchmark]

returns = prices.pct_change().dropna()
market_returns = market.pct_change().dropna()

df = pd.DataFrame(index=tickers)

df["momentum"] = prices.shift(21).iloc[-1] / prices.shift(273).iloc[-1] - 1
df["volatility"] = returns.tail(252).std() * np.sqrt(252)

betas = []

for ticker in tickers:
    concat_returns = pd.concat([returns[ticker], market_returns], axis=1).dropna().tail(252)
    stock_ret = concat_returns.iloc[ : , 0]
    bench_ret = concat_returns.iloc[ : , 1]

    cov = np.cov(stock_ret, bench_ret, ddof=1)[0, 1]
    var_bench = np.var(bench_ret, ddof=1)
    beta = cov / var_bench

    betas.append(beta)

df["beta"] = betas
df = df.fillna(df.median(numeric_only=True))

def zscore(series):
    return (series - series.mean()) / series.std(ddof=0)

df["z_momentum"] = zscore(df["momentum"])
df["z_volatility"] = zscore(df["volatility"])
df["z_beta"] = zscore(df["beta"])

df["z_score"] = (
    0.6 * df["z_momentum"]
    - 0.2 * df["z_volatility"]
    - 0.2 * df["z_beta"]
)

df = df.sort_values("z_score", ascending=False)

print(df[["momentum", "volatility", "beta", "z_momentum", "z_volatility", "z_beta", "z_score"]])
