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
from tkinter import Button
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from flatten_json import flatten
import json
import dash_bootstrap_components as dbc
from pycountry_convert import country_alpha2_to_continent_code, country_alpha2_to_country_name, country_name_to_country_alpha3, map_countries

external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css']

app = Dash(__name__, update_title=None, external_stylesheets = external_stylesheets, suppress_callback_exceptions=True)


def read_json_file(filename):
    f = open(filename, 'r')
    data = json.loads(f.read())
    f.close()
    return data

def get_flattened_dataframe(data):
    return pd.DataFrame([flatten(d, '.') for d in data])
    
def generate_dashboard_content(figure_name):
    dashboard_graph = dcc.Graph(
        id='dashboard-graph',
        figure=figure_name,
        style = {'height' : '100%'}
    )
    return dashboard_graph

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
    title="Incident Locations",
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


content = html.Div(id="page-content", style={'height' : '100%'})

app.title = "VCDB Dashboard"

app.layout =  html.Div([
    dcc.Location(id="url"),
    navbar,
    content
], style = {'height' : '90vh'}
)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return generate_dashboard_content(fig_error_variety)
    elif pathname == "/map":
        return generate_dashboard_content(fig_incident_locations)
    return [dbc.Alert("Invalid Endpoint", color="danger"),
            dbc.Button("Return Home", id="home-button", size="lg", color="primary")]

@app.callback(
    Output("url", "pathname"),
    [Input("home-button", "n_clicks")]
)
def on_home_button_click(n):
    if n is not None:
        return "/"


if __name__ == "__main__":
    app.run_server(debug=True)
