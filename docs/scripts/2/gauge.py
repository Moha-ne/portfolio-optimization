from pathlib import Path
import par84
import plotly.graph_objects as go

images = Path(par84.img_path)
name = "gauge-"

value = 16.88
minvalue = 0
maxvalue = 30
reference = 14.87

fig = go.Figure(layout=par84.layout)

fig.add_indicator(
    mode="gauge+number+delta",
    value=value,
    domain={'x': [0, 1], 'y': [0, 1]},
    delta={
        'reference': reference,
        'increasing': {'color': '#f92672'}
    },
    gauge={
        'axis': {
            'range': [None, maxvalue],
            'tickwidth': 1,
            'tickcolor': '#aaaaaa'
        },
        'bar': {'color': '#7b2cff'},
        'bgcolor': 'rgba(10, 10, 20, 1)',
        'borderwidth': 3,
        'bordercolor': 'rgba(123, 44, 255, 0.8)',
        'steps': [
            {'range': [minvalue, maxvalue * 0.6], 'color': 'rgba(123, 44, 255, 0.10)'},
            {'range': [maxvalue * 0.6, maxvalue * 0.85], 'color': 'rgba(123, 44, 255, 0.25)'},
            {'range': [maxvalue * 0.85, maxvalue], 'color': 'rgba(249, 38, 114, 0.5)'}
        ],
        'threshold': {
            'line': {'color': '#ff2cff', 'width': 6},
            'thickness': 0.8,
            'value': 490
        }
    }
)

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font={'color': 'rgb(40,40,40)', 'family': 'Helvetica'}
)

fig.write_html(images / f"{name}1.html", config=par84.config)

