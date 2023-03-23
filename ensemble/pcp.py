import pandas as pd
import plotly.express as px

data = pd.read_csv("model_clustering_data.csv")

fig = px.parallel_coordinates(data, dimensions=data.columns[3:])

fig.show()