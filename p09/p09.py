import numpy as np
from scipy.integrate import odeint
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column, layout
from bokeh.models import Slider, Div, ColumnDataSource

beta = 0.3
gamma = 0.1

def SIR(y, _, beta, gamma):
    S, I, _ = y
    dSdt = -beta*S*I
    dIdt = beta*S*I - gamma*I
    dRdt = gamma*I
    return [dSdt, dIdt, dRdt]

fig = figure(width=1200, aspect_ratio=3)
fig.y_range.start = 0
fig.y_range.end = 1
fig.x_range.start = 0
fig.background_fill_color = 'white'

t = np.linspace(0, 30, 200)
y = odeint(SIR, [0.99, 0.01, 0], t, args=(beta, gamma))
source = ColumnDataSource(data=dict(x=t, y=y[:, 0]))

# Line with white background
line = fig.line('x', 'y', source=source, line_color='red', line_width=3)


slider_beta = Slider(title='beta', value=beta, start=0.0, end=1.0, step=0.01, width=200)
slider_gamma = Slider(title='gamma', value=gamma, start=0.0, end=1.0, step=0.01, width=200)
div = Div(text='<h1>SIR Model</h1>')

def update(attr, old, new):
    beta = slider_beta.value
    gamma = slider_gamma.value

    y = odeint(SIR, [0.99, 0.01, 0], t, args=(beta, gamma))
    source.data = dict(x=t, y=y[:, 0])

slider_beta.on_change('value', update)
slider_gamma.on_change('value', update)

layout = column(div, row(column(slider_beta, slider_gamma), fig))
curdoc().add_root(layout)
