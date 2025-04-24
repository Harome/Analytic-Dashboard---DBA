import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from Data.Clean_data.defineddata import (
    get_region_list,
    create_gender_comparison_figure,
    create_grade_level_comparison_figure,
    create_shs_strand_comparison_figure, # Import the new function
    create_gender_plot, create_enrollment_bubble_chart,
    encoded_3, data_4, data_5, fig6,
    fig7, fig8, fig9, fig10, fig11
)
from flask import request
import traceback  # Import the traceback module


app = dash.Dash(__name__)
app.title = "Student Population Dashboard"
server = app.server

image_src_1 = create_gender_plot()
image_src_2 = create_enrollment_bubble_chart()

index_page = html.Div([
    html.H1("Welcome to Student Dashboard"),
    html.P("Choose a graph route.")
])

CORS(server)
UPLOAD_FOLDER = 'Data/Raw_data/'
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@server.route('/upload_dataset', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400

    # Save the file to your target folder
    filename = file.filename
    filepath = os.path.join(server.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Update config.json
    config_path = 'config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)

    config['dataset_path'] = filepath

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

    return jsonify({'status': 'success', 'message': f'File {filename} uploaded and config updated.'}), 200

@server.route('/api/gender-comparison', methods=['GET'])
def api_gender_comparison():
    region = request.args.get('region', 'All Regions')
    print(f"[/api/gender-comparison] Received region: {region}")
    try:
        print("[/api/gender-comparison] Calling create_gender_comparison_figure...")
        fig = create_gender_comparison_figure(region)
        print("[/api/gender-comparison] Plotly Figure (dict) before JSON:")
        print(json.dumps(fig.to_dict(), indent=4))
        json_data = jsonify(fig.to_plotly_json())
        print("[/api/gender-comparison] JSON data sent to client:")
        print(json.dumps(fig.to_plotly_json(), indent=4))
        return json_data
    except Exception as e:
        print(f"[/api/gender-comparison] Error in /api/gender-comparison: {e}")
        print(traceback.format_exc())  # Log the full traceback
        return jsonify({'error': str(e)}), 500

@server.route('/api/grade-level-comparison', methods=['GET'])
def api_grade_level_comparison():
    region = request.args.get('region', 'All Regions')
    try:
        fig = create_grade_level_comparison_figure(region)
        return jsonify(fig.to_plotly_json())
    except Exception as e:
        print(f"[/api/grade-level-comparison] Error: {e}")
        return jsonify({'error': str(e)}), 500

@server.route('/api/shs-strand-comparison', methods=['GET']) # New route for SHS strand comparison
def api_shs_strand_comparison():
    region = request.args.get('region', 'All Regions')
    try:
        fig = create_shs_strand_comparison_figure(region)
        return jsonify(fig.to_plotly_json())
    except Exception as e:
        print(f"[/api/shs-strand-comparison] Error: {e}")
        return jsonify({'error': str(e)}), 500


# *** DASH CALLBACKS ***

@app.callback(
    Output('comparison-gender-graph', 'figure'),
    Input('comparison-region-dropdown', 'value')
)
def update_gender_comparison(region):
    return create_gender_comparison_figure(region)

@app.callback(
    Output('comparison-grade-level-graph', 'figure'),
    Input('comparison-grade-level-region-dropdown', 'value')
)
def update_grade_level_comparison(region):
    return create_grade_level_comparison_figure(region)

@app.callback( # New callback for SHS strand comparison
    Output('comparison-shs-strand-graph', 'figure'),
    Input('comparison-shs-strand-region-dropdown', 'value')
)
def update_shs_strand_comparison(region):
    return create_shs_strand_comparison_figure(region)


# *** END DASH CALLBACKS ***

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

# Data Comparison Gender Page
comparison_gender_page = html.Div([
    html.H2("Data Comparison - Gender Analysis", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
        id='comparison-region-dropdown',
        options=[{'label': r, 'value': r} for r in get_region_list()],
        value='All Regions'
)
    ], style={'width': '300px', 'margin': '0 auto'}),
    dcc.Graph(id='comparison-gender-graph')
], style={'padding': '20px'})

# Data Comparison Grade Level Page
comparison_grade_level_page = html.Div([
    html.H2("Data Comparison - Grade Level Analysis", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
        id='comparison-grade-level-region-dropdown',
        options=[{'label': r, 'value': r} for r in get_region_list()],
        value='All Regions'
)
    ], style={'width': '300px', 'margin': '0 auto'}),
    dcc.Graph(id='comparison-grade-level-graph')
], style={'padding': '20px'})

# Data Comparison SHS Strand Page
comparison_shs_strand_page = html.Div([
    html.H2("Data Comparison - SHS Strand Analysis", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
        id='comparison-shs-strand-region-dropdown', # New dropdown ID
        options=[{'label': r, 'value': r} for r in get_region_list()],
        value='All Regions'
)
    ], style={'width': '300px', 'margin': '0 auto'}),
    dcc.Graph(id='comparison-shs-strand-graph') # New graph ID
], style={'padding': '20px'})


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
    elif pathname == '/data-comparison-gender':
        return comparison_gender_page
    elif pathname == '/data-comparison-grade-level':
        return comparison_grade_level_page
    elif pathname == '/data-comparison-shs-strand': # New route for SHS strand comparison
        return comparison_shs_strand_page
    else:
        return index_page

if __name__ == '__main__':
    app.run(debug=False)