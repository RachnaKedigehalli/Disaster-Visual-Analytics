import pandas as pd
import plotly.graph_objects as go

data = pd.read_csv("model_clustering_data.csv")
columns = data.columns[3:]
# columns = ['text_info', 'KMeans(n_clusters=2)', 'Birch(n_clusters=2)', 'AgglomerativeClustering()', 'ensemble']
columns = ['text_info', 'ensemble', 'text_info', 'KMeans(n_clusters=2)', 'ensemble', 'text_info', 'Birch(n_clusters=2)', 'ensemble', 'text_info', 'AgglomerativeClustering()', 'ensemble']
print(columns)

models = []
for model in columns:
    models.append((model, data[model].value_counts()[0], data[model].value_counts()[1]))

nodes = []
for node in columns:
    nodes.append(node + "_0")
    nodes.append(node + "_1")

source = []
target = []
value = []
for i in range(len(models)):
    # for j in range(i+1, len(models)):
    j = i+1
    if j<len(models):
        # 0-0, 0-1, 1-1, 1-0
        source.extend([2*i, 2*i, 2*i+1, 2*i+1])
        target.extend([2*j, 2*j+1, 2*j+1, 2*j])
        # value.extend([abs(models[i][1]-models[j][1]), abs(models[i][1]-models[j][2]), abs(models[i][2]-models[j][2]), abs(models[i][2]-models[j][1])])
        value.append(len(data[data[models[i][0]] == 0][data[models[j][0]] == 0]))
        value.append(len(data[data[models[i][0]] == 0][data[models[j][0]] == 1]))
        value.append(len(data[data[models[i][0]] == 1][data[models[j][0]] == 1]))
        value.append(len(data[data[models[i][0]] == 1][data[models[j][0]] == 0]))

# print(nodes)
# print(source)

fig = go.Figure(data=[go.Sankey(
    node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = nodes,
        color = "blue"
    ),
    link = dict(
        source = source, # indices correspond to labels, eg A1, A2, A1, B1, ...
        target = target,
        value = value
  ))])

fig.update_layout(title_text="How each model is similar to ground truth and the ensemble output", font_size=12)
fig.show()