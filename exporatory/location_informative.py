import json
import os

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd

directory = './data/json/'
annotations = './data/annotations/'
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
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(linewidths=0.5)
    ax.add_feature(cfeature.LAND, facecolor='white')
    ax.set_extent([-180, 180, -90, 90])
    ax.scatter(lat,lon,
        color="red",
        s=1,
        alpha=1,
        transform=ccrs.PlateCarree())
    ax.scatter(inf_lat, inf_lon,
        color="blue",
        s=1,
        alpha=1,
        transform=ccrs.PlateCarree())
    plt.title(filename)
    plt.show()
    # break
