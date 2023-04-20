from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from geoplots import *

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
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs-dcc',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=True)