import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import json
import pandas as pd
from six.moves.urllib.parse import quote

from application import app
from helpers import parse_contents
from components import create_dropdowns, create_slider, metrics_graph
from model_evaluation import model_evaluation


# populates dropdown with feature options
@app.callback(Output('dropdown-holder', 'children'),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('upload-data', 'last_modified')])
def update_dropdowns(content, filename, date):
    return parse_contents(content, filename, date, add_dropdown_options)

def add_dropdown_options(df):
    if df is None:
        return create_dropdowns()
    variables = list(df.columns)
    options = [{'label': i, 'value': i} for i in variables]
    return create_dropdowns(options)


# defines range of feature subset size
@app.callback(Output('slider-holder', 'children'),
    [Input('cat-dropdown', 'value'),
    Input('cont-dropdown', 'value'),
    Input('subset-checkbox', 'values')])
def update_slider(cat_options, cont_options, subsets):
    if cat_options is None : cat_options=[]
    if cont_options is None : cont_options=[]
    num_features = len(cat_options) + len(cont_options)
    subsets = subsets[0] if len(subsets) > 0 else 'subsets'
    return create_slider(num_features, subsets)


# stores results of model evaluation in hidden div
@app.callback(Output('results-holder', 'children'),
    [Input('run-button', 'n_clicks')],
    [State('cat-dropdown', 'value'),
    State('cont-dropdown', 'value'),
    State('target-dropdown', 'value'),
    State('feature-slider', 'value'),
    State('algorithm-radio', 'value'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')])
def store_results(n, cats, conts, target, size, alg, content, filename, date):
    if cats is None : cats=[]
    if conts is None : conts=[]
    min_features = size[0]

    get_results = lambda x: model_evaluation(x, target, min_features, alg, cats, conts)
    results_df = parse_contents(content, filename, date, get_results)
    return results_df.to_json(date_format='iso', orient='split')


# visualizes results on scatter plot
@app.callback(Output('metrics-graph', 'figure'),
    [Input('results-holder', 'children')])
def update_metrics_graph(results_data):
    df = pd.read_json(results_data, orient='split')
    return graph_data(df)

def graph_data(df):
    try:
        x=df['auc']
        y=df['fscore']
    except KeyError:
        return metrics_graph.children.figure
  
    return dict(
        data=[go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=dict(
                size=15,
                opacity=0.5,
                line=dict(width=0.5, color='white')
            )
        )],
        layout=go.Layout(
            xaxis=dict(title='auc'),
            yaxis=dict(title='f-score'),
            margin=dict(r=0),
            hovermode='closest'
        )
    )


# displays results info of model hovered over
@app.callback(Output('marker-info', 'children'),
    [Input('metrics-graph', 'hoverData')],
    [State('results-holder', 'children')])
def display_marker_info(hoverData, results):
    if hoverData is None : return ''
    df = pd.read_json(results, orient='split')

    index = hoverData['points'][0]['pointIndex']
    feat_importances = df.iloc[index]['feat_importance'].split(", ")
    importance_list = [html.P(feat, style=dict(
        marginLeft='20px'
    )) for feat in feat_importances]

    info = html.Div([
        html.P('Features: {}'.format(df.iloc[index]['features'] + '\n'), style=dict(
            lineHeight='100%'
        )),
        html.P('\nAUC: {}'.format(round(df.iloc[index]['auc'], 3))),
        html.P('F-score: {}'.format(round(df.iloc[index]['fscore'], 3))),
        html.P('Feature Importance:'),
        html.Div(importance_list)
    ], style=dict(
        lineHeight='20%'
    ))

    return info


# changes dataframe for csv download
@app.callback(Output('download-button', 'href'),
    [Input('results-holder', 'children')])
def update_download(results):
    df = pd.read_json(results, orient='split')
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
    return csv_string






