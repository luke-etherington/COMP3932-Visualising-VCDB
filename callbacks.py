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
# callbacks.py
# =============================================================================

from dash import Input, Output, callback


## Button click handler for endpoint error screen button
@callback(Output("url", "pathname"), Input("home-button", "n_clicks"))
def on_home_button_click(n):
    if n is not None:
        return "/"
