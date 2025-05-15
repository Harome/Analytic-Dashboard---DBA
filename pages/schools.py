import dash
from dash import dcc, html
from Data.Clean_data.stuscho import (
    generate_graph10, generate_graph11, load_data
)

dash.register_page(__name__, path="/school")
df_school = load_data()
fig10 = generate_graph10(df_school)
fig11 = generate_graph11(df_school)

layout = html.Div([
    html.H2("School Dataset Graphs"),
    dcc.Graph(id='school-sankey-chart', figure=fig10),
    dcc.Graph(id='school-bar-line-chart', figure=fig11),
])