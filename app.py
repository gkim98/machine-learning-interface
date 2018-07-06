import dash
import dash_html_components as html 
from dash.dependencies import Input, Output, State 

import components as cc
import callback_helpers as ch


# create dash app
app = dash.Dash(__name__)
server = app.server 
app.scripts.config.serve_locally=True
app.config.suppress_callback_exceptions=True 

app.css.append_css({
    'external_url': (
        'https://rawgit.com/lwileczek/Dash/master/undo_redo5.css'
    )
})


# layout for the app
app.layout = html.Div([
    cc.file_uploader,
    html.Div(id='dropdown-holder', children=cc.create_dropdowns(), 
        style=dict(width='100%')),
    html.Div([
        cc.algorithm_radio, cc.subset_checkbox
    ], style=dict(
        display='flex',
        justifyContent='space-between',
        marginTop='10px'
    )),
    html.Div([
        cc.slider_holder, cc.run_button
    ], style=dict(marginTop='20px')),
    html.Div([
        cc.metrics_graph, cc.marker_info
    ], style=dict(
        width='100%', 
        display='flex',
        alignItems='flex-start'
    )),
    cc.download_button,


    cc.results_holder
    
], style=dict(width='100%'))


# callback functions for app events
@app.callback(Output('dropdown-holder', 'children'),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('upload-data', 'last_modified')])
def update_dropdowns(content, filename, date):
    return ch.dropdown_helper(content, filename, date)

@app.callback(Output('slider-holder', 'children'),
    [Input('cat-dropdown', 'value'),
    Input('cont-dropdown', 'value'),
    Input('subset-checkbox', 'values')])
def update_slider(cat_options, cont_options, subsets):
    return ch.slider_helper(cat_options, cont_options, subsets)

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
    return ch.results_helper(n, cats, conts, target, size, alg, content, filename, date)

@app.callback(Output('metrics-graph', 'figure'),
    [Input('results-holder', 'children')])
def update_metrics_graph(results_data):
    return ch.graph_helper(results_data)

@app.callback(Output('marker-info', 'children'),
    [Input('metrics-graph', 'hoverData')],
    [State('results-holder', 'children')])
def display_marker_info(hoverData, results):
    return ch.marker_helper(hoverData, results)

@app.callback(Output('download-button', 'href'),
    [Input('results-holder', 'children')])
def update_download(results):
    return ch.download_helper(results)


# run server
if __name__ == '__main__':
    app.run_server()