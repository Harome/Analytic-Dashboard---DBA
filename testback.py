import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Data.Clean_data.defineddata import total_students, df_total_enrollees, fig2, fig3, fig4

app = dash.Dash(__name__)
app.title = "Student Population Dashboard"

app.layout = html.Div([
    html.H1("📊 Student Population Overview", style={"textAlign": "center"}),

    html.Div([
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
                'fontSize': 10, 'padding': '8px'
            }
        ),
        html.P(f"📍 Total Students Enrolled: {total_students:,}",
               style={"textAlign": "center", "fontSize": "10px", "marginTop": "10px"})
    ], style={'marginBottom': '30px'}),

    html.Div([
        html.H3("Graph 2: Distribution of Students per Grade Level Across Regions"),
        dcc.Graph(figure=fig2)
    ]),

    html.Div([
    html.H3("Graph 3: Student Population Distribution by Year Level (All Regions)"),
    dcc.Graph(figure=fig3)
    ], style={'marginBottom': '50px'}),

    html.Div([
        html.H3("Graph 4: Student Population per Grade Division by Region"),
        dcc.Graph(figure=fig4)
    ], style={'marginBottom': '50px'}),


])

if __name__ == '__main__':
    app.run(debug=True)