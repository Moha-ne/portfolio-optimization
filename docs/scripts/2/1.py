from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import scipy.stats as stats
import par84

images = Path(par84.img_path)
name = "markovar-"

symbols = ["PGR", "LLY", "JPM", "MU", "BRK-B", "RTX", "PLTR", "CVNA", "GE", "TMUS", "WMT", "CRWD", "GOOGL", "TSM", "IBKR", "AAPL", "GS", "PWR", "SPOT", "NVDA", "COST", "RCL", "GLD", "GDX", "NEM"]
symbols = sorted(symbols)
df = yf.Tickers(symbols).history(period='3y', auto_adjust=True)['Close']
df = df.tz_localize(None)

print(f"\n==== Basis 100 ====")
df100 = df / df.iloc[0] * 100
print(df100)

fig = go.Figure(layout=par84.layout)
for i in symbols:
    fig.add_scatter(x=df100.index, y=df100[i], name=i)
fig.write_html(images / f"{name}1.html", config=par84.config)

print(f"\n==== Daily returns ====")
daily_returns = np.log(df/ df.shift(1)).dropna()
print(daily_returns.map(lambda x: f"{x:.2%}"))

fig = go.Figure(layout=par84.layout)
for i in symbols:
    fig.add_scatter(x=daily_returns.index, y=daily_returns[i], name=i)
fig.write_html(images / f"{name}2.html", config=par84.config)

fig = go.Figure(layout=par84.layout)	
for i in symbols:
    fig.add_histogram(x=daily_returns[i], name=i)
fig.write_html(images / f"{name}3.html", config=par84.config)

print(f"\n==== Annual returns ====")
mean_returns = daily_returns.mean() * 252
print(mean_returns.map(lambda x: f"{x:.2%}"))

print(f"\n==== Covariance matrix ====")
cov_matrix = daily_returns.cov() * 252
print(cov_matrix.map(lambda x: f"{x:.2%}"))

print(f"\n==== Risk-free rate ====")
rf_series = yf.Ticker('^IRX').history(period='5d')['Close']
rf = rf_series.dropna().mean() / 100.0
print(f"{rf:.2%}")  

np.random.seed(42)
num_portfolios = 10_000
results = np.zeros((num_portfolios, 3))
weights_list = []
tickers_list=[]
for i in range(num_portfolios):
    weights = np.random.random(len(symbols))
    weights /= np.sum(weights)

    w = pd.Series(weights, index=symbols)
    port_return = float(w @ mean_returns)                 
    port_volatility = float(np.sqrt(w @ cov_matrix @ w)) 
    sharpe_ratio = (port_return - rf) / port_volatility

    results[i, 0] = port_return
    results[i, 1] = port_volatility
    results[i, 2] = sharpe_ratio
    
    weights_list.append(weights)
    tickers_list.append(symbols)

results = pd.DataFrame(results, columns=['Return', 'Volatility', 'Sharpe Ratio'])
print(f"==== {num_portfolios} results ====")
print(results)

print(f"\n==== Max. Sharpe ratio ====")
max_sharpe_idx = results['Sharpe Ratio'].idxmax()
max_sharpe_ratio = results.loc[max_sharpe_idx, 'Sharpe Ratio']
print(f"{max_sharpe_ratio:.2f}")

print(f"\n==== Best weights ====")
best_weights = weights_list[max_sharpe_idx]
best_weights_df = pd.DataFrame({
    'Asset': symbols,
    'Weight': best_weights
})
best_weights_df['Weight'] = best_weights_df['Weight'].map(lambda x: f"{x:.2%}")
print(best_weights_df)

fig = go.Figure(layout=par84.layout)
fig.add_pie(labels=symbols, values=best_weights, hole=.5, textposition='inside', textinfo='label+percent', marker=dict(colors=[par84.layout.colorway[symbols.index(s) % len(par84.layout.colorway)] for s in symbols]))
fig.update_layout(title_text='Optimal Portfolio Asset Allocation', showlegend=True)
fig.write_html(images / f"{name}4.html", config=par84.config)

print(f"\n==== Optimal return ====")
optimal_return = results.loc[max_sharpe_idx, 'Return']
print(f"{optimal_return:.2%}")

print(f"\n==== Optimal volatility====")
optimal_volatility = results.loc[max_sharpe_idx, 'Volatility']
print(f"{optimal_volatility:.2%}")

cml_x = np.linspace(0, max(results['Volatility']), 100)
cml_y = rf + (optimal_return - rf) / optimal_volatility * cml_x

optimal_weights_text = [f'{symbols[i]}: {best_weights[i]:.2f}' for i in range(len(symbols))]
optimal_weights_string = ', '.join(optimal_weights_text)  

fig = go.Figure(layout=par84.layout)
fig.add_scatter(
    x=results['Volatility'], y=results['Return'],
    marker=dict(color=(results['Return'] - rf)/(results['Volatility']), showscale=True, line=dict(width=1), colorscale="viridis", colorbar=dict(title="Sharpe<br>Ratio")), mode='markers',
    text=[str(np.array(tickers_list[i])) + "<br>" + str(np.array(weights_list[i]).round(2)) for i in range(len(tickers_list))]
)
fig.add_scatter(x=[optimal_volatility], y=[optimal_return], mode='markers', marker=dict(color='greenyellow'), text=optimal_weights_string)
fig.update_layout(title='Efficient Frontier', xaxis_title='Volatility', yaxis_title='Return', showlegend=False)
fig.write_html(images / f"{name}5a.html", config=par84.config)
fig.add_scatter(x=cml_x, y=cml_y)
fig.write_html(images / f"{name}5b.html", config=par84.config)

w_best = pd.Series(best_weights, index=symbols)
marginal_contribution = cov_matrix @ w_best
risk_contribution = w_best * marginal_contribution
percent_contribution = risk_contribution / (optimal_volatility**2)

fig = go.Figure(layout=par84.layout)
fig.add_bar(x=symbols, y=percent_contribution.values, name='Risk Contribution')
fig.update_layout(title='Contribution to Portfolio Risk', xaxis_title='Assets', yaxis_title='Percentage of Total Risk')
fig.write_html(images / f"{name}6.html", config=par84.config)

risk_contrib_table = pd.DataFrame({
    'Asset': symbols,
    'Weight': w_best.values,
    'Risk Contribution': percent_contribution.values
})
print(f"\n==== Contribution to risk ====")
risk_contrib_table['Weight'] = risk_contrib_table['Weight'].map(lambda x: f"{x:.2%}")
risk_contrib_table['Risk Contribution'] = risk_contrib_table['Risk Contribution'].map(lambda x: f"{x:.2%}")
print(risk_contrib_table)

print("\n==== Value at Risk ====")
investment = 2_000_000_000
conf_level = 0.99

optimal_return_d = optimal_return / 252
optimal_volatility_d = optimal_volatility / np.sqrt(252)

mean_val_1d = investment * (1 + optimal_return_d)
std_val_1d  = investment * optimal_volatility_d
cutoff = stats.norm.ppf(1 - conf_level, mean_val_1d, std_val_1d)
var_1d = investment - cutoff
print("Value at Risk of the portfolio after 1 day : " + str(var_1d))

var_array = []
horizon = 10
for t in range(1, horizon+1):
    mean_val_t = investment * (1 + optimal_return_d * t)
    std_val_t  = investment * (optimal_volatility_d * np.sqrt(t))
    cutoff_t = stats.norm.ppf(1 - conf_level, mean_val_t, std_val_t)
    var_array.append(np.round(investment - cutoff_t, 2))
    print(str(t) + " day(s) : " + str(np.round(investment - cutoff_t, 2)))

fig = go.Figure(layout=par84.layout)
fig.add_scatter(y = var_array)
fig.update_layout(
    title="Maximal loss after 10 days",
    xaxis_title="Days",
    yaxis_title="$")
fig.write_html(images / f"{name}7.html", config=par84.config)
