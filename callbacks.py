from app import app
from helpers import parse_contents
from components import create_dropdowns, create_slider
from dash.dependencies import Input, Output, State
from model_evaluation import model_evaluation
import plotly.graph_objs as go


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


@app.callback(Output('slider-holder', 'children'),
    [Input('cat-dropdown', 'value'),
    Input('cont-dropdown', 'value')])
def update_slider(cat_options, cont_options):
    if cat_options is None : cat_options=[]
    if cont_options is None : cont_options=[]
    num_features = len(cat_options) + len(cont_options)
    return create_slider(num_features)
    

@app.callback(Output('metrics-graph', 'figure'),
    [Input('run-button', 'n_clicks')],
    [State('cat-dropdown', 'value'),
    State('cont-dropdown', 'value'),
    State('target-dropdown', 'value'),
    State('feature-slider', 'value'),
    State('algorithm-radio', 'value'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')])
def update_metrics_graph(n, cats, conts, target, size, alg, content, filename, date):
    if cats is None : cats=[]
    if conts is None : conts=[]
    min_features = size[0]

    test = lambda x: print('yay')

    # pass in model_evaluation function with available parameters
    get_results = lambda x: model_evaluation(x, target, test, min_features, alg, cats, conts)
    return parse_contents(content, filename, date, get_results)

def graph_data(df):
    x=df['auc']
    y=df['fscore']

    return dict(
        data=[go.Scatter(
            x=x,
            y=y,
            mode='markers'
        )],
        layout=go.Layout(
            xaxis=dict(title='auc'),
            yaxis=dict(title='f-score'),
            margin=dict(r='0'),
            hovermode='closest'
        )
    )