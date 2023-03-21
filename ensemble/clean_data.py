import json
import pandas as pd

json_data = open('./../data/json/california_wildfires_final_data.json')

annotation_data = open('./../data/annotations/california_wildfires_final_data.tsv')
annot_data = pd.read_csv(annotation_data, sep='\t')

tweet_id = []
tweet_text = []
for jsonObj in json_data:
    data = json.loads(jsonObj)
    # print(data['id'])
    tweet_id.append(data['id'])
    # print(data['text'])
    tweet_text.append(data['text'])
    # break


tweet_df = pd.DataFrame({'tweet_id': tweet_id, 'tweet_text': tweet_text})

df = pd.merge(tweet_df, annot_data, on='tweet_id')[['tweet_id', 'tweet_text_x', 'text_info']]
print(df.head())

df.to_csv('classification_data.csv', index=False)