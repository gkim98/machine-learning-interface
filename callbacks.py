from app import app
from helpers import parse_contents
from components import create_dropdowns, create_slider
from dash.dependencies import Input, Output


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
    
    