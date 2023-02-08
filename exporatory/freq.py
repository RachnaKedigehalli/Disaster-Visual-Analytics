import os
import json
import csv
import matplotlib.dates as md
import datetime as dt
from datetime import datetime
import matplotlib.pyplot as plt

directory = './data/json/'
# f = open('./../PE_Dataset/json/srilanka_floods_final_data.json')
# data = json.load(f)

for filename in os.listdir(directory):
    print(filename)
    f = open(os.path.join(directory, filename))
    tweet_list = []
    tweet_time = []

    for jsonObj in f:
        try:
            data = json.loads(jsonObj)
            # tweet_list.append(data)
            
            # for x in data:
            #     print( x + " ->> " + str(data[x]))
            # print(data['timestamp_ms'])
            # print(data['created_at'])
            # tweets_with_loc.append(data)
            # print(md.epoch2num(data['timestamp_ms']))
            # print(dt.datetime.fromtimestamp(int(data['timestamp_ms'])/1000))
            # print(data['created_at'])
            dt_obj = dt.datetime.fromtimestamp(int(data['timestamp_ms'])/1000)
            # print(md.date2num(dt.datetime.fromtimestamp(data['timestamp_ms']/1000)))
            # print([data['id'], data['timestamp_ms'], data['created_at'], dates.date2num(dates.datetime.utcfromtimestamp(data['timestamp_ms']))])
            # print(datetime.fromisoformat(data['created_at']))
            tweet_time.append(md.date2num(dt_obj))
            # break
        except Exception as e:
            print(e)
            # break
                # print(jsonObj)
                # print("exception")
            # print(("PLACE",data['place']))
            # print(("COORDINATES", data['coordinates']))
            # print()
        # break
    # print(filename + " Tweets with location data: " + str(len(tweets_with_loc)) + "/" + str(len(tweet_list)))
    fig, ax = plt.subplots(1,1)
    ax.hist(tweet_time, bins=15, color='lightblue')
    locator = md.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(md.ConciseDateFormatter(locator))
    fig.autofmt_xdate()
    plt.locator_params(axis='x', nbins=10)
    plt.title(filename)
    plt.show()
    # break