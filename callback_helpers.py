import json
from six.moves.urllib.parse import quote
import pandas as pd
import plotly.graph_objs as go
import dash_html_components as html

from components import create_dropdowns, create_slider, metrics_graph
from helpers import parse_contents
from model_evaluation import model_evaluation


# adds options to dropdown
def dropdown_helper(content, filename, date):
    return parse_contents(content, filename, date, add_dropdown_options)

def add_dropdown_options(df):
    if df is None:
        return create_dropdowns()
    variables = list(df.columns)
    options = [{'label': i, 'value': i} for i in variables]
    return create_dropdowns(options)


# updates slider
def slider_helper(cat_options, cont_options, subsets):
    if cat_options is None : cat_options=[]
    if cont_options is None : cont_options=[]
    num_features = len(cat_options) + len(cont_options)
    subsets = subsets[0] if len(subsets) > 0 else 'subsets'
    return create_slider(num_features, subsets)


# stores results in hidden div
def results_helper(n, cats, conts, target, size, alg, content, filename, date):
    if cats is None : cats=[]
    if conts is None : conts=[]
    min_features = size[0]

    get_results = lambda x: model_evaluation(x, target, min_features, alg, cats, conts)
    results_df = parse_contents(content, filename, date, get_results)
    return results_df.to_json(date_format='iso', orient='split')


# visualizes results on scatter plot
def graph_helper(results_data):
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


# displays marker data
def marker_helper(hoverData, results):
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


# prepares results data for download
def download_helper(results):
    df = pd.read_json(results, orient='split')
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
    return csv_string