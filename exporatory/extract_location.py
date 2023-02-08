import csv
import json
import os

import cartopy.crs as ccrs
# import cartopy.io.img_tiles as cimgt
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from shapely.geometry.polygon import LinearRing

directory = './data/json/'
# f = open('./../PE_Dataset/json/srilanka_floods_final_data.json')
# data = json.load(f)
# ax = plt.axes(projection=map_quest_aerial.crs)

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
            
            if data['place'] != None or data['coordinates'] != None:
                # for x in data:
                #     print( x + " ->> " + str(data[x]))
                tweets_with_loc.append(data)
                # print([data['id'], data['timestamp_ms'], data['created_at'], data['place'], data['coordinates']])
                # print(data['place']['bounding_box']['coordinates'][0][0])
                for i in range(4):
                    lat.append(data['place']['bounding_box']['coordinates'][0][i][0])
                    lon.append(data['place']['bounding_box']['coordinates'][0][i][1])
                # print(data['coordinates'])
        except:
                print(jsonObj)
            # print(("PLACE",data['place']))
            # print(("COORDINATES", data['coordinates']))
            # print()
        # break
    # print(lat)
    # print(lon)
    # print((len(lat), len(lon)))
    print(filename + " Tweets with location data: " + str(len(tweets_with_loc)) + "/" + str(len(tweet_list)))
    print("Lon", lon)
    print("Lat", lat)
    # ring = LinearRing(list(zip(lon, lat)))
    # ax.add_geometries([ring], ccrs.PlateCarree(), facecolor='green', edgecolor='red')

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(linewidths=0.5)
    ax.add_feature(cfeature.LAND, facecolor='white')
    ax.set_extent([-180, 180, -90, 90])
    ax.scatter(lat,lon,
        color="red",
        s=1,
        alpha=1,
        transform=ccrs.PlateCarree())

    # ax.set_extent([lat[0], lat[1], lon[0], lon[1]], ccrs.PlateCarree())
    plt.title(filename)
    plt.show()
