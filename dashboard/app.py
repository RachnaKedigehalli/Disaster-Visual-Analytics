from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

colors = {
    'background': '#ffffff',
    'text': '#7F1F1F'
}

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig.update_layout(
    plot_bgcolor = colors["background"],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

def generate_table(df, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))
        ])
    ])

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(children='Hello Dash',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }),

        html.Div(children='''
            Dash: A web application framework for your data.
        ''', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='example-graph',
            figure=fig
        ),
        
        html.H4(children='US Agriculture Exports (2011)'),

        generate_table(df)
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)