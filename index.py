import dash_core_components as dcc   
import dash_html_components as html 
from dash.dependencies import Input, Output 

from app import app 
from components import file_uploader
from components import create_dropdowns, algorithm_radio, slider_holder
from components import run_button
from components import metrics_graph
import callbacks


app.layout  = html.Div([
    file_uploader,
    html.Div(id='dropdown-holder', children=create_dropdowns(), 
        style=dict(width='100%')),
    algorithm_radio,
    html.Div([
        slider_holder, run_button
    ], style=dict(marginTop='20px')),
    metrics_graph
    
])









# # populates the dropdowns with variable options
# @app.callback(Output('cat-dropdown', 'options'),
#     [Input('upload-data', 'contents'),
#     Input('upload-data', 'filename'),
#     Input('upload-data', 'last_modified')])
# def fill_cat_dropdown(content, filename, data):
#     return get_variables(content, filename, data)

# @app.callback(Output('cont-dropdown', 'options'),
#     [Input('upload-data', 'contents'),
#     Input('upload-data', 'filename'),
#     Input('upload-data', 'last_modified')])
# def fill_cont_dropdown(content, filename, data):
#     return get_variables(content, filename, data)

# @app.callback(Output('target-dropdown', 'options'),
#     [Input('upload-data', 'contents'),
#     Input('upload-data', 'filename'),
#     Input('upload-data', 'last_modified')])
# def fill_target_dropdown(content, filename, data):
#     return get_variables(content, filename, data)

if __name__ == '__main__':
    app.run_server()