import dash
from dash import dcc, html
from Data.Clean_data.stuscho import (
    generate_graph7, generate_graph8, generate_graph9, load_data
)

dash.register_page(__name__, path="/student")
df_school = load_data()
fig7 = generate_graph7(df_school)
fig8 = generate_graph8(df_school)
fig9 = generate_graph9(df_school)

layout = html.Div([
    html.H2("Student Dataset Graphs"),
    dcc.Graph(id='student-population-bar-chart', figure=fig7),
    dcc.Graph(id='Student-strand-area-chart', figure=fig8),
    dcc.Graph(id='Student-division-donut-chart', figure=fig9),
])