#!/usr/bin/env python3
# coding=utf-8
# =============================================================================
# Author: Luke Etherington
# Email: sc18lge@leeds.ac.uk
# Module: COMP3932 - Synoptic project
# Supervisor: Nick Efford
#
# Visualising Data Security Incidents using VCDB
#
# app.py
# =============================================================================

from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from components import navbar, endpoint_error
import graphs
import callbacks

external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css']

app = Dash(__name__, update_title=None, external_stylesheets = external_stylesheets, suppress_callback_exceptions=True)
app.title = "VCDB Dashboard"


## Main page layout
app.layout =  html.Div([
    dcc.Location(id="url"),
    navbar,
    html.Div(id="page-content", style={'height' : '100%'})
], style = {'height' : '90vh'}
)

## Given a specified Plotly Express figure object, returns an appropriate DCC graph object containing the figure
def generate_dashboard_content(figure):
    dashboard_graph = dcc.Graph(
        id='dashboard-graph',
        figure = figure,
        style = {'height' : '100%'})
    return dashboard_graph


## Page navigation callback handler
@callback(
    Output("page-content", "children"), 
    Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return generate_dashboard_content(graphs.fig_error_variety)
    elif pathname == "/map":
        return generate_dashboard_content(graphs.fig_incident_locations)
    return endpoint_error

if __name__ == "__main__":
    app.run_server(debug=True)
