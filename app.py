import dash
from dash import dcc, html, dash_table, Input, Output

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Data.Clean_data.defineddata import total_students, df_total_enrollees, fig2, fig3, fig4

app = dash.Dash(__name__)
app.title = "Student Population Dashboard"

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

graph1_page = html.Div([
    html.H3("Graph 1: Total Enrollees Table"),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_total_enrollees.columns],
        data=df_total_enrollees.to_dict('records'),
        style_table={'overflowX': 'auto', 'border': '1px solid black'},
        style_header={
            'backgroundColor': '#C1E1C1', 'fontWeight': 'bold', 'textAlign': 'center'
        },
        style_cell={
            'textAlign': 'center', 'backgroundColor': '#FADADD', 'color': '#333',
            'fontSize': 14, 'padding': '8px'
        }
    ),
    html.P(f"📍 Total Students Enrolled: {total_students:,}",
           style={"textAlign": "center", "fontSize": "16px", "marginTop": "10px"})
], style={'marginBottom': '50px'})

index_page = html.Div([
    html.H1("Welcome to Student Dashboard"),
    html.P("Choose a graph route.")
])

graph2_page = html.Div([
    html.H3("Graph 2: Distribution of Students per Grade Level Across Regions"),
    dcc.Graph(figure=fig2)
])

graph3_page = html.Div([
    html.H3("Graph 3: Student Population Distribution by Year Level (All Regions)"),
    dcc.Graph(figure=fig3)
])

graph4_page = html.Div([
    html.H3("Graph 4: Student Population per Grade Division by Region"),
    dcc.Graph(figure=fig4)
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/graph1':
        return graph1_page
    elif pathname == '/graph2':
        return graph2_page
    elif pathname == '/graph3':
        return graph3_page
    elif pathname == '/graph4':
        return graph4_page
    else:
        return index_page

if __name__ == '__main__':
    app.run(debug=True)