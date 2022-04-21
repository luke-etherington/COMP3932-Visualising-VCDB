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
# components.py
# =============================================================================

import dash_bootstrap_components as dbc

## Navbar component used on main page layout
navbar = dbc.NavbarSimple(
    [
        dbc.NavItem(
            dbc.NavLink(
                "Incident Location Map", href="incident_location_map", active="exact"
            )
        ),
        dbc.NavItem(
            dbc.NavLink("Actor Location Map", href="actor_location_map", active="exact")
        ),
        dbc.NavItem(
            dbc.NavLink("Incident Victims", href="incident_victims", active="exact")
        ),
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Incident Summaries", href="/summary_table"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="VCDB Dashboard",
    brand_href="/",
    color="primary",
    dark=True,
    fluid=True,
    style={"paddingRight": "120px", "paddingLeft": "10px"},
)

## Component displayed on invalid endpoint request
endpoint_error = [
    dbc.Alert(
        [
            "Invalid Endpoint",
            dbc.Button(
                "Return Home",
                id="home-button",
                color="primary",
                style={"margin-left": "10px"},
            ),
        ],
        color="danger",
    ),
]
