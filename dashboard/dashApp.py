#!/Users/liu/kouui/anaconda3/envs/dash_py38/bin/python
# -*- coding: utf-8 -*-


import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State

from Lib import *



##----------------------------------------------------------------------------

data = {}


##----------------------------------------------------------------------------

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H2("Machine Learning App"),
        #html.Img(src="/assets/title-icon.jpg")
    ], className="title"
    ),

    dcc.Tabs(
        id = "tabs",
        value = "tab-1",
        #parent_className = "custom-tabs",
        #className = "custom-tabs-container",
        children = [
            dcc.Tab(
                label = "Configuration",
                value = "tab-1",
                #className = "custom-tab",
                #selected_className = "custom-tab--selected",
                children = [
                    html.Br(),

                    ##-- data path input
                    html.Div([
                        html.Div(
                            dcc.Input(
                                id = "input-dataPath",
                                type = "text",
                                placeholder="/path/to/read/your/datafile",
                                className = "input-field",
                                persistence = False,
                                debounce=True
                            ),style={'display': 'inline-block'},
                        ),
                        html.Div(
                            html.P(
                                id="out-input-dataPath",
                                className = "P-output"
                            ),style={'display': 'inline-block'}
                        ),
                    ], style={'width': '100%', 'display': 'inline-block'}),

                    html.Br(),

                    #-- model save input
                    html.Div([
                        html.Div(
                            dcc.Input(
                                id = "input-modelPath",
                                type = "text",
                                placeholder="/path/to/save/your/modelfile",
                                className = "input-field",
                                persistence = False,
                                debounce=True
                            ),style={'display': 'inline-block'},
                        ),
                        html.Div(
                            html.P(
                                id="out-input-modelPath",
                                className = "P-output"
                            ),style={'display': 'inline-block'}
                        ),
                    ], style={'width': '100%', 'display': 'inline-block'}),

                    html.Br(),

                    #-- model save input
                    html.Div([
                        html.Div(
                            dcc.Input(
                                id = "input-trainPath",
                                type = "text",
                                placeholder="/path/to/read/your/train/function",
                                className = "input-field",
                                persistence = False,
                                debounce=True
                            ),style={'display': 'inline-block'},
                        ),
                        html.Div(
                            html.P(
                                id="out-input-trainPath",
                                className = "P-output"
                            ),style={'display': 'inline-block'}
                        ),
                    ], style={'width': '100%', 'display': 'inline-block'}),

                    ##-- train validation split

                    ##-- hyperparameter configuration

                    ##-- buttons
                    html.Div([
                        html.Div(
                            html.Button(
                                "Check",
                                id='btn-check',
                                n_clicks=0,
                                disabled = False,
                                className = "button-configuration"
                            ),style={'display': 'inline-block'},
                        ),
                        html.Div(
                            html.Button(
                                "Train",
                                id='btn-train',
                                n_clicks=0,
                                disabled = True,
                                className = "button-configuration"
                            ),style={'display': 'inline-block'},
                        ),
                        html.Div(
                            html.Button(
                                "Show Result",
                                id='btn-show',
                                n_clicks=0,
                                disabled = True,
                                className = "button-configuration"
                            ),style={'display': 'inline-block'},
                        ),
                        html.Div(
                            html.Button(
                                "Load",
                                id='btn-load',
                                n_clicks=0,
                                disabled = False,
                                className = "button-configuration"
                            ),style={'display': 'inline-block'},
                        ),
                        html.Div(
                            html.Button(
                                "Save",
                                id='btn-save',
                                n_clicks=0,
                                disabled = True,
                                className = "button-configuration"
                            ),style={'display': 'inline-block'},
                        ),
                    ], style={'width': '100%', 'display': 'inline-block'}),

                ]
            ),

            dcc.Tab(
                label = "Training",
                value = "tab-2",
                #className = "custom-tab",
                #selected_className = "custom-tab--selected"
            ),

            dcc.Tab(
                label = "Result",
                value = "tab-3",
                #className = "custom-tab",
                #selected_className = "custom-tab--selected"
                children = [
                    html.Div([
                        html.Div([
                            html.H3('Axis'),
                            dcc.Dropdown(
                                id='drop-1',
                                options=[
                                    {'label': 'New York City', 'value': 'NYC'},
                                    {'label': 'Montreal', 'value': 'MTL'},
                                    {'label': 'San Francisco', 'value': 'SF'}
                                ],
                                #value='NYC',
                                clearable = False,
                                className = "dropdown-result",
                            ),
                            dcc.Dropdown(
                                id='drop-2',
                                options=[
                                    {'label': 'New York City', 'value': 'NYC'},
                                    {'label': 'Montreal', 'value': 'MTL'},
                                    {'label': 'San Francisco', 'value': 'SF'}
                                ],
                                #value='NYC',
                                clearable = False,
                                className = "dropdown-result",
                            ),
                            ],
                            className="result-column-1",
                            style={'display': 'inline-block'}
                        ),

                        html.Div([
                            html.H3('Result'),
                            dcc.Graph(
                                id = "3dplot",
                            ),
                            ],
                            className="result-column-2",
                            style={'display': 'inline-block'}
                        ),

                        ],style={'width': '100%', 'display': 'inline-block'},
                    ),
                ],
            ),
        ],
        vertical = False,
    ),

    #html.Div(id="tabs-content")
])

@app.callback(Output("out-input-dataPath", "children"), [Input("input-dataPath", "value")])
def output_text_data_path(value):
    if value is None:
        value = ""
    data["data-path"] = value
    return "Data Path : " + value

@app.callback(Output("out-input-modelPath", "children"), [Input("input-modelPath", "value")])
def output_text_model_path(value):
    if value is None:
        value = ""
    data["model-path"] = value
    return "Model Path : " + value

@app.callback(Output("out-input-trainPath", "children"), [Input("input-trainPath", "value")])
def output_text_train_path(value):
    if value is None:
        return "train function from : "
    else:
        directory_, module_ = get_import_info_from_file_path(value)
        try:
            data["train"] = import_train_func_from_file_path(directory_, module_)
            return "train function from : " + value
        except ImportError as e :
            return f"Error: {e}"

if __name__ == "__main__":
    app.run_server("0.0.0.0", port=8050, debug=True)
