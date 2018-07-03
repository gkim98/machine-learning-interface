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

if __name__ == '__main__':
    app.run_server()