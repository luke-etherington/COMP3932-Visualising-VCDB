# !/usr/bin/env python3
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

from dash import Dash, Input, Output, callback, dcc, html

import graphs
from components import endpoint_error, navbar

external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)
app.title = "VCDB Dashboard"


## Main page layout
app.layout = html.Div(
    [
        dcc.Location(id="url"),
        navbar,
        html.Div(id="page-content", style={"height": "100%", "width": "100%"}),
    ],
    style={"height": "90vh"},
)

## Given a specified Plotly Express figure object, returns an appropriate DCC graph object containing the figure
def generate_graph_object(figure):
    graph = dcc.Graph(figure=figure, style={"height": "100%"})
    return graph


def generate_dashboard(figure_1, figure_2, figure_3, figure_4):
    dashboard_layout = [
        html.Div(
            [
                html.Div(
                    [generate_graph_object(figure_1)],
                    id="graph-1",
                    style={"height": "50%"},
                ),
                html.Div(
                    [generate_graph_object(figure_2)],
                    id="graph-2",
                    style={"height": "50%"},
                ),
            ],
            style={"height": "100%", "width": "50%", "float": "left"},
        ),
        html.Div(
            [
                html.Div(
                    [generate_graph_object(figure_3)],
                    id="graph-3",
                    style={"height": "50%"},
                ),
                html.Div(
                    [generate_graph_object(figure_4)],
                    id="graph-4",
                    style={"height": "50%"},
                ),
            ],
            style={"height": "100%", "width": "50%", "float": "right"},
        ),
    ]
    return dashboard_layout


## Page navigation callback handler
@callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return generate_dashboard(
            graphs.fig_incident_year,
            graphs.fig_data_variety,
            graphs.fig_error_variety,
            graphs.fig_avg_incident_month,
        )
    elif pathname == "/incident_location_map":
        return generate_graph_object(graphs.fig_incident_locations)
    elif pathname == "/actor_location_map":
        return generate_graph_object(graphs.fig_actor_locations)
    elif pathname == "/incident_victims":
        return generate_graph_object(graphs.fig_incident_victims)
    elif pathname == "/summary_table":
        return graphs.summary_table
    return endpoint_error


if __name__ == "__main__":
    app.run_server(debug=True)
