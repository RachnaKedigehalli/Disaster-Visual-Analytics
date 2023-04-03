import plotly.express as px
import pandas as pd
data = pd.read_csv("model_clustering_data.csv")

fig = px.parallel_categories(data, dimensions=['text_info', 'ensemble', 'text_info', 'KMeans(n_clusters=2)', 'ensemble', 'text_info', 'Birch(n_clusters=2)', 'ensemble', 'text_info', 'AgglomerativeClustering()', 'ensemble'],
                # color="size", color_continuous_scale=px.colors.sequential.Inferno,
                # labels={'sex':'Payer sex', 'smoker':'Smokers at the table', 'day':'Day of week'}
                )
fig.show()