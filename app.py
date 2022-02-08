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
import json

app = Dash(__name__)

DATA_FILE = "./data/vcdb_1-of-1.json"

df = pd.read_json(DATA_FILE)

df_error = df[[i for i in map(lambda x: 'error' in x.keys(), df['action'])]]
df_error_action_normalised = pd.json_normalize(df_error['action'])
df_error_action_normalised['error.variety'] =  df_error_action_normalised['error.variety'].map(lambda l: ' '.join(map(str,l)))
df_error_variety_group_by_count = df_error_action_normalised.groupby('error.variety').size()
df_error_variety_group_by_count = df_error_variety_group_by_count.to_frame(name='count').reset_index()
fig = px.bar(df_error_variety_group_by_count, x='error.variety', y='count', color='error.variety')

app.layout =  html.Div( children=[
    html.H1(children='VBCB Vis'),

    dcc.Graph(
        id='Error Variety',
        figure = fig
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)#
