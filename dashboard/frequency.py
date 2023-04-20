from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import json
import dash_bootstrap_components as dbc
import matplotlib.dates as md
import datetime as dt

data_folder = "./../data/"

app = Dash(__name__)

def generate_frequency_plot(filename):
    f = open(data_folder + "json/" + filename + ".json")
    tweet_list = []
    tweet_time = []

    for jsonObj in f:
        try:
            data = json.loads(jsonObj)
            dt_obj = dt.datetime.fromtimestamp(int(data['timestamp_ms'])/1000)
            # tweet_time.append(md.date2num(dt_obj))
            tweet_time.append(dt_obj)
        except Exception as e:
            print(e)
    
    tweet_times = pd.DataFrame({
        "time": tweet_time
    })
    fig = px.histogram(tweet_times, nbins=15)
    # locator = md.AutoDateLocator()
    return fig

file_names = ["california_wildfires_final_data", "hurricane_harvey_final_data", "hurricane_irma_final_data",
              "hurricane_maria_final_data", "mexico_earthquake_final_data",
              "srilanka_floods_final_data"]

frequency = html.Div(style={'textAlign': 'center', 'width': '90%', 'margin': 'auto'},
                       children=[
        # html.H1(children='Disaster Data Dashboard'),

        html.H2('Tweet frequency'),
        html.Div(
            [
                dbc.Row([
                    dbc.Col([
                        html.Div(
                            style={'width': '60%'},
                            children=[
                                html.H3(file_names[3*i+j]),
                                # dcc.Graph(
                                #     id='tweet-location'+file_names[3*i+j],
                                #     figure=generate_geoplot(file_names[3*i+j])
                                # )
                                dcc.Graph(
                                    figure=generate_frequency_plot(file_names[3*i+j])
                                )
                            ]
                        )],
                        width=4
                    )
                    for j in range(3)
                ]) 
                for i in range(2)
            ],
            style={'textAlign': 'center'}
            
        )
    ]
)


app.layout = frequency
if __name__ == '__main__':
    app.run_server(debug=True)