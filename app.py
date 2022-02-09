#!/usr/bin/env python3
# coding=utf-8
# =============================================================================
"""
Author: Luke Etherington
Email: sc18lge@leeds.ac.uk
Module: COMP3932 - Synoptic project
Supervisor: Nick Efford
"""
# =============================================================================
""" Visualising Data Security Incidents using VCDB

app.py

"""
from itertools import groupby
from dash import Dash, html, dcc
from numpy import dtype
import plotly.express as px
import pandas as pd
from flatten_json import flatten
import json
import dash_bootstrap_components as dbc

external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css']

app = Dash(__name__, update_title=None, external_stylesheets = external_stylesheets)

def read_json_file(filename):
    f = open(filename, 'r')
    data = json.loads(f.read())
    f.close()
    return data

def get_flattened_dataframe(data):
    return pd.DataFrame([flatten(d, '.') for d in data])

DATA_FILE = "./data/vcdb_1-of-1.json"

data = read_json_file(DATA_FILE)
df = get_flattened_dataframe(data)

fig = px.bar(df['action.error.variety.0'].value_counts().rename("count").reset_index(), 
    x='index', 
    y='count', 
    color='index',
    labels={
        "index" : "Error Variety",
        "count" : "Count"
    },
    title="Count of Error Variety"
)

navbar = dbc.NavbarSimple([],
brand="VCDB Vis",
brand_href="#",
color="primary",
dark=True,
fluid=True)

app.title = "VCDB Dashboard"

app.layout =  html.Div([
    navbar,

    dcc.Graph(
        id='dashboard-graph',
        figure = fig,
        style = {'height' : '100%'}
    )

], style = {'height' : '90vh'}
)



if __name__ == "__main__":
    app.run_server(debug=True)#
