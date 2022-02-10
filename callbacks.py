from dash import Input, Output, callback

## Button click handler for endpoint error screen button
@callback(
    Output("url", "pathname"),
    Input("home-button", "n_clicks")
)
def on_home_button_click(n):
    if n is not None:
        return "/"