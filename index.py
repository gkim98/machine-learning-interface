import dash_core_components as dcc   
import dash_html_components as html 
from dash.dependencies import Input, Output 

from app import app
from components import file_uploader
from components import create_dropdowns, algorithm_radio, slider_holder, subset_checkbox
from components import run_button
from components import metrics_graph, marker_info
from components import results_holder, download_button
import callbacks

app.layout = html.Div([
    file_uploader,
    html.Div(id='dropdown-holder', children=create_dropdowns(), 
        style=dict(width='100%')),
    html.Div([
        algorithm_radio, subset_checkbox
    ], style=dict(
        display='flex',
        justifyContent='space-between',
        marginTop='10px'
    )),
    html.Div([
        slider_holder, run_button
    ], style=dict(marginTop='20px')),
    html.Div([
        metrics_graph, marker_info
    ], style=dict(
        width='100%', 
        display='flex',
        alignItems='flex-start'
    )),
    download_button,


    results_holder
    
], style=dict(width='100%'))

if __name__ == '__main__':
    app.run_server(debug=True)