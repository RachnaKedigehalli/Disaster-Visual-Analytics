from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from geoplots import *
from frequency import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'textAlign': 'center'},
                      children=[
    html.H1('Disaster Data Dashboard'),
    dcc.Tabs(id="tabs", value='geoplots', children=[
        dcc.Tab(label='Geoplots', value='geoplots'),
        dcc.Tab(label='Frequency', value='frequency'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'geoplots':
        return geoplots
    elif tab == 'frequency':
        return frequency

if __name__ == '__main__':
    app.run_server(debug=True)