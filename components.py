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
            dbc.NavLink("Data Loss", href="confidential_data_loss", active="exact")
        ),
        dbc.NavItem(dbc.NavLink("")),
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
    style={"padding-right": "120px", "padding-left": "10px"},
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
