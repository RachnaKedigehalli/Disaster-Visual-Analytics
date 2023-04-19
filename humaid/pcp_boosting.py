import pandas as pd
import plotly.express as px

data = pd.read_csv("boosting1.csv")

fig = px.parallel_coordinates(data, dimensions=['predicted_class', 'class', 'predicted_xgboost'])

fig.show()