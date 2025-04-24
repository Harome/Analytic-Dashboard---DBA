import dash
from dash import dcc, html, dash_table, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import dash_uploader as du
import base64
import io
import os
from Data.Clean_data.defineddata import (
    create_grade_level_comparison_figure,
    get_region_list,
    create_gender_plot, create_enrollment_bubble_chart, df_school,
    encoded_3, data_4, data_5, generate_graph6,
    generate_graph7, generate_graph8, generate_graph9, generate_graph10, generate_graph11
)
from flask import request
import traceback  # Import the traceback module


app = dash.Dash(__name__)
app.title = "Student Population Dashboard"
server = app.server
fig6 = generate_graph6(df_school)
fig7 = generate_graph7(df_school)
fig8 = generate_graph8(df_school)
fig9 = generate_graph9(df_school)
fig10 = generate_graph10(df_school)
fig11 = generate_graph11(df_school)

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
    
    if 'school' in file.filename.lower():
        target_config = 'school_dataset_path'
    else:
        target_config = 'student_dataset_path'

    # Save the file to your target folder
    filename = file.filename
    filepath = os.path.join(server.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Update config.json
    config_path = 'config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)

    config[target_config] = filepath

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

    return jsonify({'status': 'success', 'message': f'File {filename} uploaded and config updated.'}), 200

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        print(f"Parsed DataFrame: {df.head()}")
        return df
    except Exception as e:
        print(f"Error processing file: {e}")
        return pd.DataFrame()  # Return empty DataFrame on erro
    
def process_school_file(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df_school = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df_school.to_dict('records')  # Or whatever structure your app expects
    except Exception as e:
        print(f"[process_school_file] Error: {e}")
        return []

def process_student_file(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df_student = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df_student.to_dict('records')  # Same here
    except Exception as e:
        print(f"[process_student_file] Error: {e}")
        return []

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

# DASH CALLBACK for Gender Comparison
@app.callback(
    Output('comparison-gender-graph', 'figure'),  # Update the 'figure' property of the graph
    Input('comparison-region-dropdown', 'value')   # When the 'value' of the dropdown changes
)
def update_gender_comparison(region):
    return create_gender_comparison_figure(region)  # Get the new figure data

@server.route('/api/grade-comparison', methods=['GET'])
def api_grade_comparison():
    region = request.args.get('region', 'All Regions')
    fig = create_grade_level_comparison_figure(region)
    return jsonify(fig.to_plotly_json())

# DASH CALLBACK for Grade Level Comparison
@app.callback(
    Output('grade-bar-graph', 'figure'),  # Update the 'figure' property of the graph
    Input('grade-region-dropdown', 'value')   # When the 'value' of the dropdown changes
)
def update_grade_level_comparison(selected_region):
    return create_grade_level_comparison_figure(selected_region)


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

graph7_pag = html.Div(
    children=[
        dcc.Graph(
            id='graph-7'  # ID must match the one you're updating in the callback
        )
    ]
)

# Graph 8: Student Data Analytics - Area Chart (Student Distribution per SHS Strand by Sector)
graph8_page = html.Div([
    dcc.Graph(figure=fig8, id="Student-strand-area-chart")
    ]),

graph8_pag = html.Div([
    dcc.Graph(id="graph-8")  # Match callback target ID
]),

# Graph 9: Student Data Analytics - Donut Chart (Student Distribution by Grade Division and School Sector)
graph9_page = html.Div([
    dcc.Graph(figure=fig9, id="Student-division-donut-chart")
    ]),

graph9_pag = html.Div([
    dcc.Graph(id="graph-9")  # Match callback target ID
])

# Graph 10: School Data Analytics - Sankey Chart (School Population per Sector, Sub-Classification, and Modified COC)
graph10_page = html.Div([
    dcc.Graph(figure=fig10, id="school-sankey-chart")
    ]),

graph10_pag = html.Div([
    dcc.Graph(id="graph-10")  # Match callback target ID
])

# Graph 11: School Data Analytics - Line-Bar Chart (School Count by School Type and Sector)
graph11_page = html.Div([
    dcc.Graph(figure=fig11, id="school-bar-line-chartt")
    ])

graph11_pag = html.Div([
    dcc.Graph(id="graph-11")  # Match callback target ID
])

# Data Comparison Graph - Gender
comparison_page_gender = html.Div([
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

# Data Comparison Graph - Grade Level
comparison_page_grade = html.Div([
    html.H2("Data Comparison - Grade Level Analysis", style={
        'textAlign': 'center',
        'fontFamily': 'Arial Black',
        'fontSize': '28px',
        'marginBottom': '20px'
    }),

    html.Div([
        html.Label("Select Region:", style={
            'fontWeight': 'bold',
            'fontFamily': 'Arial',
            'fontSize': '16px',
            'marginRight': '10px'
        }),
        dcc.Dropdown(
            id='grade-region-dropdown',
            options=[{'label': 'All Regions', 'value': 'All Regions'}] + [{'label': r, 'value': r} for r in get_region_list()],
            value='All Regions',
            style={'width': '250px'}
        )
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'fontFamily': 'Arial',
        'alignItems': 'center',
        'marginBottom': '8px',
        'gap': '10px'
    }),

    dcc.Graph(id='grade-bar-graph', style={'marginTop': '8px'})
],
style={
    'backgroundColor': 'white',
    'padding': '20px',
    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
    'borderRadius': '10px',
    'maxWidth': '900px',
    'margin': 'auto'
})

app.layout = html.Div([
    dcc.Store(id='dataset-store', storage_type='memory'),  # Store for dataset
    
    # File upload components for school and student datasets
    html.Div([
        du.Upload(id='upload-school-data', text='Upload School Data'),
        du.Upload(id='upload-student-data', text='Upload Student Data'),
    ]),
    
    # Graphs for school data (Graph 10, 11)
    html.Div([
        dcc.Graph(id='graph-10'),
        dcc.Graph(id='graph-11'),
    ]),
    
    # Graphs for student data (Graph 7, 8, 9)
    html.Div([
        dcc.Graph(id='graph-7'),
        dcc.Graph(id='graph-8'),
        dcc.Graph(id='graph-9'),
    ]),
])

# Data Comparison Graph - Strand

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
    elif pathname == '/data-comparison-gender': # New route for gender comparison
        return comparison_page_gender
    elif pathname == '/data-comparison-grade': # New route for grade level comparison
        return comparison_page_grade
    else:
        return index_page
    
@app.callback(
    Output('graph-10', 'figure'),
    Output('graph-11', 'figure'),
    Input('dataset-store', 'data'),
    prevent_initial_call=True
)
def update_school_graphs(data):
    df_school = pd.DataFrame(data['school_data'])  # Convert the stored dict back to DataFrame
    
    # Use the imported functions to generate the figures
    fig_10 = generate_graph10(df_school)
    fig_11 = generate_graph11(df_school)
    
    return fig_10, fig_11

# Callback to update Graph 7, 8, 9 (Student data)
@app.callback(
    Output('graph-7', 'figure'),
    Output('graph-8', 'figure'),
    Output('graph-9', 'figure'),
    Input('dataset-store', 'data'),
    prevent_initial_call=True
)
def update_student_graphs(data):
    df_student = pd.DataFrame(data['student_data'])  # Convert the stored dict back to DataFrame
    
    # Use the imported functions to generate the figures
    fig_7 = generate_graph7(df_student)
    fig_8 = generate_graph8(df_student)
    fig_9 = generate_graph9(df_student)
    
    return fig_7, fig_8, fig_9

@app.callback(
    Output('store-student', 'data'),
    Input('upload-data', 'isCompleted'),
    State('upload-data', 'fileNames'),
    prevent_initial_call=True
)
def update_store_after_upload(is_completed, filenames):
    if is_completed and filenames:
        uploaded_path = os.path.join("./uploads", filenames[0])
        
        # Load based on file type
        if uploaded_path.endswith('.csv'):
            df = pd.read_csv(uploaded_path)
        elif uploaded_path.endswith('.xlsx'):
            df = pd.read_excel(uploaded_path)
        else:
            return dash.no_update
        
        return df.to_dict('records')  # For app-wide usage
    return dash.no_update


@app.callback(
    [Output('graph10', 'figure'), Output('graph11', 'figure'), Output('graph9', 'figure'), Output('graph8', 'figure'), Output('graph7', 'figure')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def update_graphs(contents, filename, last_modified):
    # Process the uploaded file and create the dataframe
    if contents is None:
        return dash.no_update, dash.no_update
    
    # Parse the dataset into a DataFrame
    df_school = parse_contents(contents, filename)  # You should define `parse_contents` to handle the file parsing

    # Generate Graph 10 and Graph 11 using the dataset
    fig7 = generate_graph10(df_school)
    fig8 = generate_graph10(df_school)
    fig9 = generate_graph10(df_school)
    fig10 = generate_graph10(df_school)
    fig11 = generate_graph11(df_school)

    return fig7, fig8, fig9, fig10, fig11

if __name__ == '__main__':
    app.run(debug=False)
