from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import json
import dash_bootstrap_components as dbc

data_folder = "./../data/"

app = Dash(__name__)

def generate_geoplot(filename):
    annotation_data = pd.read_csv(data_folder+ "annotations/" + filename + ".tsv", sep='\t')
    f = open(data_folder + "json/" + filename + ".json")
    tweet_list = []
    tweets_with_loc = []
    lat = []
    lon = []
    inf_lat = []
    inf_lon = []
    for jsonObj in f:
        try:
            data = json.loads(jsonObj)
            tweet_list.append(data)
            
            if data['place'] != None: #or data['coordinates'] != None:
                tweets_with_loc.append(data)
                tweet = pd.DataFrame()
                if not annotation_data.loc[annotation_data['tweet_id'] == data['id']].empty:
                    tweet = annotation_data.loc[annotation_data['tweet_id'] == data['id']]
                    # print(tweet)

                if not tweet.empty and tweet['text_info'].iloc[0] == 'informative':
                    for i in range(4):
                        inf_lat.append(data['place']['bounding_box']['coordinates'][0][i][0])
                        inf_lon.append(data['place']['bounding_box']['coordinates'][0][i][1])
                if not tweet.empty and tweet['text_info'].iloc[0] == 'not_informative':
                    for i in range(4):
                        lat.append(data['place']['bounding_box']['coordinates'][0][i][0])
                        lon.append(data['place']['bounding_box']['coordinates'][0][i][1])

        except Exception as e:
            print(e)
    
    print(filename + " Tweets with location data: " + str(len(tweets_with_loc)) + "/" + str(len(tweet_list)))
    print("inf length: ", len(inf_lat))
    print("non inf length: ", len(lat))

    locations_lat = lat[:]
    locations_lat.extend(inf_lat)

    locations_lon = lon[:]
    locations_lon.extend(inf_lon)
    informative = ["non-inf" for i in range(len(lat))]
    informative.extend(["info" for i in range(len(inf_lat))])

    locations = pd.DataFrame({
        "lat": locations_lat,
        "lon": locations_lon,
        "informative": informative
    })

    fig = px.scatter_mapbox(
        locations,
        lat="lon",
        lon="lat",
        color="informative",
        zoom=1,
        height=600,
        title=filename
    )
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(showlegend=True)
    fig.update_layout(mapbox_bounds={"west": -180, "east": 180, "south": -90, "north": 90})

    print(filename + "done")
    return fig


file_names = ["california_wildfires_final_data", "hurricane_harvey_final_data", "hurricane_irma_final_data",
              "hurricane_maria_final_data", "mexico_earthquake_final_data",
              "srilanka_floods_final_data"]

geoplots = html.Div(style={'textAlign': 'center', 'width': '90%', 'margin': 'auto'},
                       children=[
        # html.H1(children='Disaster Data Dashboard'),

        html.H2('Tweet location data'),
        html.Div(
            [
                dbc.Row([
                    dbc.Col([
                        html.Div(
                            style={'width': '60%'},
                            children=[
                                html.H3(file_names[3*i+j]),
                                dcc.Graph(
                                    id='tweet-location'+file_names[3*i+j],
                                    figure=generate_geoplot(file_names[3*i+j])
                                )
                            ]
                        )],
                        width=4
                    )
                    for j in range(3)
                ], align='center') 
                for i in range(2)
            ]
        )
    ]
)

app.layout = geoplots
if __name__ == '__main__':
    app.run_server(debug=True)