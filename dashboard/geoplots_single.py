from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os

app = Dash(__name__)

def generate_geoplot():
    directory = './../data/json/'
    annotations = './../data/annotations/'
    # f = open('./../PE_Dataset/json/srilanka_floods_final_data.json')
    # data = json.load(f)
    # ax = plt.axes(projection=map_quest_aerial.crs)
    annotation_data = []
    for filename in os.listdir(annotations):
        f = open(os.path.join(annotations, filename))
        annot_data = pd.read_csv(f, sep='\t')
        annotation_data.append(annot_data)
    # ax.add_image(map_quest_aerial, 8)
    for filename in os.listdir(directory):
        f = open(os.path.join(directory, filename))
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
                    # for x in data:
                    tweets_with_loc.append(data)
                    # print([data['id'], data['timestamp_ms'], data['created_at'], data['place'], data['coordinates']])
                    # for i in range(4):
                    #     lat.append(data['place']['bounding_box']['coordinates'][0][i][0])
                    #     lon.append(data['place']['bounding_box']['coordinates'][0][i][1])
                    tweet = pd.DataFrame()
                    for i in range(len(annotation_data)):
                        # tweet = annotation_data[i].where(annotation_data[i]['tweet_id'] == data['id'])
                        if not annotation_data[i].loc[annotation_data[i]['tweet_id'] == data['id']].empty:
                            # print(type(annotation_data[i].loc[annotation_data[i]['tweet_id'] == data['id']]))
                            tweet = annotation_data[i].loc[annotation_data[i]['tweet_id'] == data['id']]
                            # print(tweet.columns)
                            break
                    # print("tweet after: ", tweet['text_info'].iloc[0])
                    if not tweet.empty and tweet['text_info'].iloc[0] == 'informative':
                        for i in range(4):
                            inf_lat.append(data['place']['bounding_box']['coordinates'][0][i][0])
                            inf_lon.append(data['place']['bounding_box']['coordinates'][0][i][1])
                    if not tweet.empty and tweet['text_info'].iloc[0] == 'not_informative':
                        for i in range(4):
                            lat.append(data['place']['bounding_box']['coordinates'][0][i][0])
                            lon.append(data['place']['bounding_box']['coordinates'][0][i][1])
                    #

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

        return fig


app.layout = html.Div(style={'textAlign': 'center', 'width': '80%', 'margin': 'auto'},
                       children=[
        html.H1(children='Disaster Data Dashboard'),

        html.H2('Tweet location data'),
        dcc.Graph(
            id='tweet-location',
            figure=generate_geoplot()
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)