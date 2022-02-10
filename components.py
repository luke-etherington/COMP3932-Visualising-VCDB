import dash_bootstrap_components as dbc

## Navbar component used on main page layout
navbar = dbc.NavbarSimple([
    dbc.NavItem(dbc.NavLink("Map", href="map", active="exact"))
    ],
    brand="VCDB Vis",
    brand_href="/",
    color="primary",
    dark=True,
    fluid=True
)

## Component displayed on invalid endpoint request
endpoint_error = [
    dbc.Alert("Invalid Endpoint", color="danger"), 
    dbc.Button("Return Home", id="home-button", size="lg", color="primary")
    ]

