import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_daq as daq
import base64
import io
import json
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # Upload raw twitter json
    html.Div(
        'Upload raw Twitter data in json format', 
        id='upload-json-text'
    ),

    dcc.Upload(
        id='upload-json-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # accept='text/json'
    ),

    # Annotated data available?
    html.Div(
        'Is human annotated data available?'
    ),
    daq.ToggleSwitch(
        id='annotation-toggle',
        value=False,
        style = {
            'width': '200px'
        }
    ),

    # Upload Annotated data
    
    html.Div(
        id='upload-annotated-data-block'
    ),

    html.Div(id='json-data-display'),
    html.Div(id='annotat-data-display')
])

@app.callback(
    Output('json-data-display', 'children'),
    Input('upload-json-data', 'contents'),
    State('upload-json-data', 'filename')
)
def parse_json(raw_data, filename):
    # print(raw_data)
    content_type, content_string = raw_data.split(',')

    print(type(content_string))
    decoded = base64.b64decode(content_string)
    f = decoded.decode()
    f = f.split('\n')

    df = pd.DataFrame(columns=['id', 'timestamp_ms', 'created_at', 'lat', 'lon'])
    try:
        for jsonObj in f:
            # print("dasj")
            data = json.loads(jsonObj)
            if data['place'] != None or data['coordinates'] != None:
                for i in range(4):
                    df.loc[len(df.index)] = [
                        data['id'],
                        data['timestamp_ms'], 
                        data['created_at'],
                        data['place']['bounding_box']['coordinates'][0][i][0],
                        data['place']['bounding_box']['coordinates'][0][i][1]
                    ]
                # break
    except Exception as e:
        print(e)
        # return html.Div([
        #     'There was an error processing this file.'
        # ])
    
    return html.Div([
        html.H5(filename),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            page_size=50
        ),

        html.Hr(),  # horizontal line

        dcc.Graph(
            id='tweet-location',
            figure=px.scatter_mapbox(
                df,
                lat="lon",
                lon="lat",
                # color="informative",
                zoom=3,
                height=600,
            )
        )
    ])

@app.callback(
    Output('upload-annotated-data-block', 'children'),
    Input('annotation-toggle', 'value')
)
def add_upload_annotated_data_block(toggle_value):
    if toggle_value:
        return [html.Div(
            'Upload Annotated data in csv/tsv/xls format', 
            id='upload-annotated-text'
        ),
        dcc.Upload(
            id = 'upload-annotated-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # accept='text/json'
        )]

@app.callback(
    Output('annotat-data-display', 'children'),
    Input('upload-annotated-data', 'contents'),
    State('upload-annotated-data', 'filename')
)
def parse_annotat(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'tsv' in filename:
            # Assume that the user uploaded a TSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), sep='\t')
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            page_size=50
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
