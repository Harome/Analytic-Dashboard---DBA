import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Data.Clean_data.defineddata import (
    fig3, fig4,
    create_gender_plot, create_enrollment_bubble_chart,
    encoded_3, data_4, data_5, data_6,
    fig7, fig8, fig9, fig10, fig11, fig12
)

app = dash.Dash(__name__)
app.title = "Student Population Dashboard"

image_src_1 = create_gender_plot()
image_src_2 = create_enrollment_bubble_chart()

index_page = html.Div([
    html.H1("Welcome to Student Dashboard"),
    html.P("Choose a graph route.")
])

graph1_page = html.Div([
        html.Img(src=image_src_1, style={'width': '100%', 'maxWidth': '800px'})
    ], id="Graph_1"),

graph2_page = html.Div([
        html.Img(src=image_src_2, style={'width': '465px', 'height': '500px'})
    ], id="Graph_2"),


graph3_page = html.Div([
        html.H3("Graph 3: Student Population Distribution by Year Level (All Regions)"),
        dcc.Graph(figure=fig3)
    ])

graph4_page = html.Div([
        html.H3("Graph 4: Student Population per Grade Division by Region"),
        dcc.Graph(figure=fig4)
    ])

graph5_page = html.Div([
        html.H3("Graph 5: Gender-Based Enrollment"),
        html.Img(src=image_src_1, style={'width': '100%', 'maxWidth': '800px'})
    ])

graph6_page = html.Div([
        html.H3("Graph 6: Enrollment Bubble Chart"),
        html.Img(src=image_src_2, style={'width': '465px', 'height': '500px'})
    ])

graph7_page = html.Div([
        html.H3("Graph 7: Encoded PNG Chart"),
        html.Img(src='data:image/png;base64,{}'.format(encoded_3), style={'width': '600px', 'height': 'auto'})
    ])

graph8_page = html.Div([
        html.H3("Graph 8: Schools by Category"),
        html.Img(src="data:image/png;base64," + data_4)
    ])

graph9_page = html.Div([
        html.H3("Graph 9: More School Data"),
        html.Img(src="data:image/png;base64," + data_5)
    ])

graph10_page = html.Div([
        html.H3("Graph 10: Schools Detailed"),
        html.Img(src="data:image/png;base64," + data_6)
    ])

graph11_page = html.Div([
        html.H3("Graph 11: Heat Map"),
        dcc.Graph(figure=fig7)
    ])

graph12_page = html.Div([
        html.H3("Graph 12: Student Population Bar Chart"),
        dcc.Graph(id='student-population-bar-chart', figure=fig8)
    ])

graph13_page = html.Div([
        html.H3("Graph 13: Student Strand Area Chart"),
        dcc.Graph(figure=fig9)
    ])

graph14_page = html.Div([
        html.H3("Graph 14: Student Division Donut Chart"),
        dcc.Graph(figure=fig10)
    ])

graph15_page = html.Div([
        html.H3("Graph 15: School Sankey Chart"),
        dcc.Graph(figure=fig11)
    ])

graph16_page = html.Div([
        html.H3("Graph 16: School Bar and Line Chart"),
        dcc.Graph(figure=fig12)
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
    elif pathname == '/graph12':
        return graph12_page
    elif pathname == '/graph13':
        return graph13_page
    elif pathname == '/graph14':
        return graph14_page
    elif pathname == '/graph15':
        return graph15_page
    elif pathname == '/graph16':
        return graph16_page
    else:
        return index_page

if __name__ == '__main__':
    app.run(debug=False)
