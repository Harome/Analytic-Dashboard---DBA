import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Data.Clean_data.defineddata import (
    create_gender_plot, create_enrollment_bubble_chart,
    encoded_3, data_4, data_5, fig6,
    fig7, fig8, fig9, fig10, fig11
)

app = dash.Dash(__name__)
app.title = "Student Population Dashboard"

image_src_1 = create_gender_plot()
image_src_2 = create_enrollment_bubble_chart()

index_page = html.Div([
    html.H1("Welcome to Student Dashboard"),
    html.P("Choose a graph route.")
])

    # Graph 1: Main Dashboard - Student Data No. 1 (Gender Distribution of Enrollees)  

graph1_page = html.Div([
    html.Img(src=image_src_1, style={'width': '100%', 'maxWidth': '800px'})
    ], id="Graph_1")


    # Graph 2: Main Dashboard - Student Data No. 2 (Total Students Enrolled Per Region)

graph2_page = html.Div([
    html.Img(src=image_src_2, style={'width': '465px', 'height': '500px'})  # Fixed size
    ], id="Graph_2")


    # Graph 3 Main Dashboard - Student Data No. 3 (Student Population by Grade Division)

graph3_page = html.Img(
        src='data:image/png;base64,{}'.format(encoded_3),
        style={'width': '600px', 'height': 'auto'},
        id="Graph_3"
    )


    # Graph 4: Main Dashboard - School Data No. 1 (Distribution of Schools Per Region)

graph4_page = html.Div([
    html.Img(src="data:image/png;base64," + data_4)
    ], id="Graph_4")


    # Graph 5: Main Dashboard - School Data No. 2 (School Distribution per Sector)

graph5_page = html.Div([
    html.Img(src="data:image/png;base64," + data_5)
    ], id='Graph_5')


    # Graph 6: Main Dashboard - Philippine Heatmap (Philippine Regions<br>Student Population Heatmap)

graph6_page = html.Div([
    dcc.Graph(figure=fig6, id="student-heat-map")
    ])


    # Graph 7: Student Data Analytics - Column-Bar Chart (Student Population per Grade Level by Gender)

graph7_page = html.Div(
    children=[
        dcc.Graph(
            id='student-population-bar-chart',
            figure=fig7
            )
        ]
    )


    # Graph 8: Student Data Analytics - Area Chart (Student Distribution per SHS Strand by Sector)

graph8_page = html.Div([
    dcc.Graph(figure=fig8, id="Student-strand-area-chart")
    ]),


    # Graph 9: Student Data Analytics - Donut Chart (Student Distribution by Grade Division and School Sector)

graph9_page = html.Div([
    dcc.Graph(figure=fig9, id="Student-division-donut-chart")
    ]),


    # Graph 10: School Data Analytics - Sankey Chart (School Population per Sector, Sub-Classification, and Modified COC)

graph10_page = html.Div([
    dcc.Graph(figure=fig10, id="school-sankey-chart")
    ]),


    # Graph 11: School Data Analytics - Line-Bar Chart (School Count by School Type and Sector)

graph11_page = html.Div([
    dcc.Graph(figure=fig11, id="school-bar-line-chartt")
    ])


app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
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
    elif pathname == '/graph5':
        return graph5_page
    elif pathname == '/graph6':
        return graph6_page
    elif pathname == '/graph7':
        return graph7_page
    elif pathname == '/graph8':
        return graph8_page
    elif pathname == '/graph9':
        return graph9_page
    elif pathname == '/graph10':
        return graph10_page
    elif pathname == '/graph11':
        return graph11_page

    else:
        return index_page

if __name__ == '__main__':
    app.run(debug=False)
