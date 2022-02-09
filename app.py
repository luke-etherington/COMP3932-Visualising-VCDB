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
from cProfile import label
from gc import callbacks
from itertools import groupby
from dash import Dash, html, dcc, Input, Output
from numpy import dtype, size
import plotly.express as px
import pandas as pd
from flatten_json import flatten
import json
import dash_bootstrap_components as dbc
from pycountry_convert import country_alpha2_to_continent_code, country_alpha2_to_country_name, country_name_to_country_alpha3, map_countries

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

continents = {
    'NA': 'North America',
    'SA': 'South America', 
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe'
}

data = read_json_file(DATA_FILE)
df = get_flattened_dataframe(data)
df['victim.country.alpha3'] = df['victim.country.0'].apply(lambda c : c if c == 'Unknown' else country_name_to_country_alpha3(country_alpha2_to_country_name(c)))
df['victim.continent'] = df['victim.country.0'].apply(lambda c: c if c == 'Unknown' else 'Asia' if c == 'TL' else 'North America' if c == 'UM' else continents[country_alpha2_to_continent_code(c)])


fig_error_variety = px.bar(df['action.error.variety.0'].value_counts().rename("count").reset_index(), 
    x='index', 
    y='count', 
    color='index',
    labels={
        "index" : "Error Variety",
        "count" : "Count"
    },
    title="Count of Error Variety"
)

fig_incident_locations = px.scatter_geo(df[df['victim.country.alpha3'] != 'Unknown']['victim.country.alpha3'].value_counts()[lambda x: x > 10].rename("count").reset_index(), 
    locations='index', 
    size='count', 
    size_max=100,
    color='index',
    projection='natural earth',
    labels={
        'index' : "Country",
        'count' : "# of Incidents"
    })

navbar = dbc.NavbarSimple([
    dbc.NavItem(dbc.NavLink("Map", href="map", active="exact"))
    ],
    brand="VCDB Vis",
    brand_href="/",
    color="primary",
    dark=True,
    fluid=True
)

dashboard_graph = dcc.Graph(
        id='dashboard-graph',
        style = {'height' : '100%'}
    )

app.title = "VCDB Dashboard"

app.layout =  html.Div([
    dcc.Location(id="url"),
    navbar,
    dashboard_graph
], style = {'height' : '90vh'}
)

@app.callback(Output("dashboard-graph", "figure"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return fig_error_variety
    elif pathname == "/map":
        return fig_incident_locations
    return None


if __name__ == "__main__":
    app.run_server(debug=True)#
