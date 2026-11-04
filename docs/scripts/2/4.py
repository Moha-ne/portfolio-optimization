from pathlib import Path
import yfinance as yf
import par84

images = Path(par84.img_path)
name = "news-"

tickers = ["WMT", "COST", "RTX"]
n = 3
html = ""

for ticker in tickers:
    news = yf.Search(ticker, news_count=n).news
    links = ""

    for x in news[:n]:
        link = x.get("link", "")
        title = x.get("title", "")
        links += f'<li><a href="{link}" target="_blank" style="color:white">{title}</a></li>'

    html += f"<h2>{ticker}</h2><ul>{links}</ul>"

(images / f"{name}1.html").write_text(
    f'<body style="background:rgb(40,40,40);color:white;font-family:sans-serif">{html}</body>',
    encoding="utf-8"
)
