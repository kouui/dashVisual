#!/Users/liu/kouui/anaconda3/envs/dash_py38/bin/python
# -*- coding: utf-8 -*-


import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State

import plotly.graph_objs as go

import os


##----------------------------------------------------------------------------
# test dataframe
##----------------------------------------------------------------------------


##----------------------------------------------------------------------------
# setup application
##----------------------------------------------------------------------------

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets=[dbc.themes.BOOTSTRAP]
#external_stylesheets = ["https://raw.githubusercontent.com/kouui/external-files/master/css/mybootstrap.dash.min.css"]
#external_stylesheets = [ "/Users/liu/kouui/python/django/dashVisual/dashboard/data/bootstrap.min.css" ]
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
_Debug = False
if _Debug:
    from debug import pandas_df_util as pdutil
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    #app = dash.Dash(__name__)
else:
    from .debug import pandas_df_util as pdutil
    from django_plotly_dash import DjangoDash
    app = DjangoDash("dashApp_1", external_stylesheets=external_stylesheets,
                     #serve_locally=True,
                     add_bootstrap_links=True)


##----------------------------------------------------------------------------
# left plot
##----------------------------------------------------------------------------

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Country"),
                dcc.Dropdown(
                    id="plot1-country",
                    options=[
                        {"label": val, "value": val} for val in pdutil._get_countries()
                    ],
                    value=pdutil.default_country,
                ),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="plot1-x-variable",
                    options=[
                        {"label": val, "value": val} for val in pdutil._get_x_variables()
                    ],
                    value=pdutil._get_x_variables()[0],
                ),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="plot1-y-variable",
                    options=[
                        {"label": val, "value": val} for val in pdutil._get_y_variables()
                    ],
                    value=pdutil._get_y_variables()[0],
                ),
            ]
        ),

        html.Hr(),

        dbc.FormGroup(
            [
                dbc.Label("Year"),
                dcc.Dropdown(
                    id="plot2-year",
                    options=[
                        {"label": str(val), "value": int(val)} for val in pdutil._get_years()
                    ],
                    value=int(pdutil._get_years()[0]),
                ),
            ]
        ),


    ],
    body=True,
)

controls_2 = dbc.Row(
                [
                    dbc.Label("Continent", width=2),
                    dbc.Col(
                        dcc.Dropdown(
                            id="plot3-continent",
                            options=[
                                {"label": val, "value": val} for val in pdutil._get_continents()
                            ],
                            value=pdutil._get_continents()[0],
                            multi=True,
                        ),
                        width=10,
                    ),
                ]
            )

app.layout = dbc.Container(
    [
        html.H1(""),
        html.Hr(),


        dbc.Col([

            dbc.Card([
                dbc.Row(
                    [
                        dbc.Col(controls, md=2),
                        dbc.Col(dcc.Graph(id="plot1-graph"), md=4),
                        dbc.Col(dcc.Graph(id="plot2-graph"), md=5),
                    ],
                    align="center",
                ),
            ],body=True),

            html.Br(),

            dbc.Card([
                controls_2,
                dbc.Table(children=None, id="plot3-table",
                          bordered=True, striped=True,
                          #className="data-table",
                          style = {
                            "height" : "300px",
                            "overflow" : "auto",
                            "display" : "block"
                          },
                ),
            ],body=True),

        ],md=11),

    ],
    fluid=True,
)

##----------------------------------------------------------------------------
# make figure
##----------------------------------------------------------------------------
@app.callback(
    Output("plot1-graph", "figure"),
    [
        Input("plot1-x-variable", "value"),
        Input("plot1-y-variable", "value"),
        Input("plot1-country", "value"),
    ],
)
def _make_plot1(_x, _y, _country):
    _df1 = pdutil._get_sub_df(_value=_country)

    _data = [
        go.Scatter(
            x=_df1[_x],
            y=_df1[_y],
            mode="markers+lines" if _x=="year" else "markers",
            marker={"size": 12},
            #name="Cluster {}".format(c),
        ),
    ]

    _layout = {
        "xaxis": {
            "title": {
                'text': _x,
                "font" : {"size": 14},
                "standoff" : 5,
            },
            "autorange" : True,
            "showgrid": True,
            "zeroline": False,
            "showline": True,
            "ticks": 'inside',
            "showticklabels": True,
        },
        "yaxis": {
            "title": {
                'text': _y,
                "font" : {"size": 14},
                "standoff" : 5,
            },
            "autorange" : True,
            "showgrid": True,
            "zeroline": False,
            "showline": True,
            "ticks": 'inside',
            "showticklabels": True,
        },
        "title" : {
            'text': f"GDP per cap according to Country {_country}",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            "font" : {"size": 14},
        },
        "margin" : {
            "l" : 5,
            "r" : 5,
            "b" : 5,
            "t" : 50,
            "pad" : 5,
        },
    }

    return go.Figure(data=_data, layout=_layout)

@app.callback(
    Output("plot2-graph", "figure"),
    [
        Input("plot2-year", "value"),
    ],
)
def _make_plot2(_year):

    _labels, _values = pdutil._get_pie_data(_year)

    _data = [
        go.Pie(labels=_labels, values=_values,
               hoverinfo='label+percent', hole=.3),
    ]

    _layout = {
        "margin" : {
            "l" : 5,
            "r" : 5,
            "b" : 5,
            "t" : 5,
        },
        "autosize" : False,
    }

    return go.Figure(data=_data, layout=_layout)

##----------------------------------------------------------------------------
# make table
##----------------------------------------------------------------------------
@app.callback(
        Output("plot3-table", "children"),
        [
            Input("plot3-continent", "value"),
        ],
)
def _make_plot3(_value):
    if not isinstance(_value, list):
        _value = [_value,]

    _df1 = pdutil._get_sub_df(_key="continent", _value=_value, _sort_key=None)

    _table_header = [
        html.Thead(html.Tr( [html.Th(_col) for _col in _df1.columns] ))
    ]

    _body_list = []
    for _index, _row in _df1.iterrows():
        _body_list.append(
            html.Tr([ html.Td(_row[_col]) for _col in _df1.columns ])
        )
    _table_body = [html.Tbody(_body_list)]

    return _table_header + _table_body

##----------------------------------------------------------------------------
# disable duplicated option in dropdown menu
##----------------------------------------------------------------------------
# make sure that x and y values can't be the same variable
def _filter_options(_v, _options):
    """Disable option v"""
    return [
        {"label": _val, "value": _val, "disabled": _val == _v}
        for _val in [_item["label"] for _item in _options]
    ]


# functionality is the same for both dropdowns, so we reuse filter_options
app.callback(Output("plot1-x-variable", "options"),
             [Input("plot1-y-variable", "value")],
             [State("plot1-x-variable", "options")])( _filter_options )
app.callback(Output("plot1-y-variable", "options"),
             [Input("plot1-x-variable", "value")],
             [State("plot1-y-variable", "options")])( _filter_options )




if __name__ == "__main__":
    app.run_server("0.0.0.0", port=8050, debug=True)
