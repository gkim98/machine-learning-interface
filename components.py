import dash_core_components as dcc   
import dash_html_components as html  
import plotly.graph_objs as go  


# component for uploading files 
file_uploader = dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select Files')
    ]),
    style=dict(
        width='95%',
        height='60px',
        lineHeight='60px',
        borderWidth='1px',
        borderStyle='dashed',
        borderRadius='5px',
        textAlign='center',
        marginLeft='2.5%',
        marginRight='2.5%',
        marginTop='10px'
    ),
    multiple=False
)

# dropdown for categorical variables
def create_cat_dropdown(options=[]):
    return html.Div(dcc.Dropdown(id='cat-dropdown',
        options=options, multi=True, placeholder='Categorical Features'), 
        style=dict(
            width='40%',
            marginTop='10px',
            marginLeft='2.5%',
            marginRight='1%',
            display='inline-block'
        ))

# dropdown for continuous variables
def create_cont_dropdown(options=[]):
    return html.Div(dcc.Dropdown(id='cont-dropdown',
        options=options, multi=True, placeholder='Continuous Features'), 
        style=dict(
            width='40%',
            marginTop='10px',
            marginRight='1%',
            display='inline-block'
        ))

# dropdown for target variable
def create_target_dropdown(options=[]):
    return html.Div(dcc.Dropdown(id='target-dropdown',
        options=options, multi=False, placeholder='Target Variable'), 
        style=dict(
            width='13%',
            marginTop='10px',
            marginRight='2.5%',
            display='inline-block'
        ))

# creates all the dropdowns at once
def create_dropdowns(options=[]):
    return [
        create_cat_dropdown(options),
        create_cont_dropdown(options),
        create_target_dropdown(options)
    ]

# radio items for algorithm choice
algorithms=[('Logistic Regression', 'lr'), ('Random Forest', 'rf'), ('SVM', 'svm'), ('XGBoost', 'xgb')]
algorithm_radio = dcc.RadioItems(id='algorithm-radio', 
    options=[{'label': i[0], 'value': i[1]} for i in algorithms], value='xgb', 
    labelStyle=dict(
        paddingRight='1%'
    ), style=dict(
        marginLeft='2.5%',
        width='50%'
    ))

# checkbox for subsets
subset_checkbox = dcc.Checklist(id='subset-checkbox', 
    options=[{'label': 'No Subsets', 'value': 'no_subsets'}], values=['no_subsets'],
    style=dict(
        marginRight='2.5%'
    ))

# range slider for number of features in model
def create_slider(num_features=1, subsets='no_subsets'):
    if subsets == 'no_subsets':
        return dcc.RangeSlider(
            id='feature-slider', disabled=True,
            min=1, max=num_features, step=1, value=[num_features, num_features], 
            marks={i: i for i in range(num_features+1)}
        )
    return dcc.RangeSlider(
        id='feature-slider',
        min=1, max=num_features, step=1, value=[1, num_features], 
        marks={i: i for i in range(num_features+1)}
    )

slider_holder = html.Div(id='slider-holder', 
    children=create_slider(),
    style=dict(
        marginLeft='2.5%',
        marginRight='5%',
        width='70%',
        display='inline-block'
    ))

# button to run model evaluation
run_button = html.Button(
    'Run', id='run-button', style=dict(
        float='right',
        marginRight='2.5%',
        width='7.5%',
        borderRadius='5px',
        outline='none'
    )
)

# graph for metrics
metrics_graph = html.Div(dcc.Graph(id='metrics-graph',
  figure=dict(
      data=[],
      layout=go.Layout(
          xaxis=dict(title='auc'),
          yaxis=dict(title='f-score'),
          margin=dict(r=0)
      )
  ), config=dict(displayModeBar=False)  
), style=dict(
    width='60%'
))

# displays info of marker
marker_info = html.Div(id='marker-info',
    style=dict(
        width='35%',
        marginLeft='2.5%',
        marginTop='100px'
    ))

# hidden div for storing result dataframe
results_holder = html.Div(id='results-holder', children=[],
    style=dict(display='none'))

# button for downloading results
download_button = html.Div(html.A(
    'Download Results', id='download-button',
    download='results.csv', href='', target='_blank' 
), style=dict(marginLeft='2.5%'))