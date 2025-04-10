from dash import Dash, html
import dash.dcc as dcc 

def create_layout(app: Dash):
    layout = html.Div([
        html.H1("Welcome to the Dash Application"),
        html.Div("This is a simple layout for the Dash app."),
        dcc.Input(id='input-component-id', type='text'),  # ✅ Use dcc.Input
        html.Div(id='output-component-id') 
    ])
    return layout

