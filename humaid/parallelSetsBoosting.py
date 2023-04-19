import plotly.express as px
import pandas as pd
data = pd.read_csv("boosting.csv")

fig = px.parallel_categories(data, dimensions=['predicted_class', 'class', 'predicted_xgboost'],
                # color="size", color_continuous_scale=px.colors.sequential.Inferno,
                # labels={'sex':'Payer sex', 'smoker':'Smokers at the table', 'day':'Day of week'}
                )
fig.show()