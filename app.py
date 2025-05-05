import dash
from dash import dcc, html, dash_table, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from flask import request, jsonify
from flask_cors import CORS
from io import BytesIO
import base64
import requests
import os
from Data.Clean_data.defineddata import (
    get_region_list,
    create_gender_comparison_figure,
    create_grade_level_comparison_figure,
    create_shs_strand_comparison_figure,
    create_grade_division_comparison_figure,
    create_sector_comparison_figure,
    create_school_type_comparison_figure,
    create_gender_plot, create_enrollment_bubble_chart,
    encoded_3, data_4, data_5, fig6,
    generate_graph7, generate_graph8, generate_graph9, generate_graph10, generate_graph11, total_schools_home, total_students_home, highest_population_home, load_student_data, load_school_data, load_data
)
from flask import request
import traceback  # Import the traceback module
from flask_executor import Executor


app = dash.Dash(__name__)
app.title = "Student Population Dashboard"
server = app.server
df_school = load_data()
fig7 = generate_graph7(df_school)
fig8 = generate_graph8(df_school)
fig9 = generate_graph9(df_school)
fig10 = generate_graph10(df_school)
fig11 = generate_graph11(df_school)

image_src_1 = create_gender_plot()
image_src_2 = create_enrollment_bubble_chart()

# Initialize Flask-Executor for asynchronous tasks
executor = Executor(server)

# Function to process uploaded files asynchronously
def process_uploaded_file(filepath, target_config):
    try:
        # Update config.json
        config_path = 'config.json'
        with open(config_path, 'r') as f:
            config = json.load(f)

        config[target_config] = filepath

        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)

        print(f"File {filepath} processed and config updated.")
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")

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
    
  
    data_type = request.form.get('type', '').lower()
    print(f"Received file: {file.filename} of type {data_type}")

    if data_type == 'school':
        target_config = 'school_dataset_path'
    elif data_type == 'student':
        target_config = 'student_dataset_path'
    else:
        return jsonify({'status': 'error', 'message': 'Missing or invalid type ("school" or "student")'}), 400

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

@server.route('/api/shs-strand-comparison', methods=['GET'])
def api_shs_strand_comparison():
    region = request.args.get('region', 'All Regions')
    try:
        fig = create_shs_strand_comparison_figure(region)
        return jsonify(fig.to_plotly_json())
    except Exception as e:
        print(f"[/api/shs-strand-comparison] Error: {e}")
        return jsonify({'error': str(e)}), 500

@server.route('/api/grade-division-comparison', methods=['GET'])
def api_grade_division_comparison():
    region = request.args.get('region', 'All Regions')
    try:
        fig = create_grade_division_comparison_figure(region)
        return jsonify(fig.to_plotly_json())
    except Exception as e:
        print(f"[/api/grade-division-comparison] Error: {e}")
        return jsonify({'error': str(e)}), 500

@server.route('/api/sector-comparison', methods=['GET'])
def api_sector_comparison():
    region = request.args.get('region', 'All Regions')
    try:
        fig = create_sector_comparison_figure(region)
        return jsonify(fig.to_plotly_json())
    except Exception as e:
        print(f"[/api/sector-comparison] Error: {e}")
        return jsonify({'error': str(e)}), 500

@server.route('/api/school-type-comparison', methods=['GET']) # New route for school type comparison
def api_school_type_comparison():
    region = request.args.get('region', 'All Regions')
    try:
        fig = create_school_type_comparison_figure(region)
        return jsonify(fig.to_plotly_json())
    except Exception as e:
        print(f"[/api/school-type-comparison] Error: {e}")
        return jsonify({'error': str(e)}), 500


# *** DASH CALLBACKS ***

@app.callback(
    Output('comparison-gender-graph', 'figure'),
    Input('comparison-gender-region-dropdown', 'value')
)
def update_gender_comparison(region):
    return create_gender_comparison_figure(region)

@app.callback(
    Output('comparison-grade-level-graph', 'figure'),
    Input('comparison-grade-level-region-dropdown', 'value')
)
def update_grade_level_comparison(region):
    return create_grade_level_comparison_figure(region)

@app.callback(
    Output('comparison-shs-strand-graph', 'figure'),
    Input('comparison-shs-strand-region-dropdown', 'value')
)
def update_shs_strand_comparison(region):
    return create_shs_strand_comparison_figure(region)

@app.callback(
    Output('comparison-grade-division-graph', 'figure'),
    Input('comparison-grade-division-region-dropdown', 'value')
)
def update_grade_division_comparison(region):
    return create_grade_division_comparison_figure(region)

@app.callback(
    Output('comparison-sector-graph', 'figure'),
    Input('comparison-sector-region-dropdown', 'value')
)
def update_sector_comparison(region):
    return create_sector_comparison_figure(region)

@app.callback( # New callback for school type comparison
    Output('comparison-school-type-graph', 'figure'),
    Input('comparison-school-type-region-dropdown', 'value')
)
def update_school_type_comparison(region):
    return create_school_type_comparison_figure(region)

@server.route('/totalschools')
def serve_total_schools():
    return jsonify(total_schools_home)

@server.route('/totalstudents')
def serve_total_students():
    return jsonify(int(total_students_home))

@server.route('/highestpopulation')
def serve_highest_population():
    return str(highest_population_home)

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
    ),

# Graph 8: Student Data Analytics - Area Chart (Student Distribution per SHS Strand by Sector)
graph8_page = html.Div([
    dcc.Graph(figure=fig8, id="Student-strand-area-chart")
    ]),


# Graph 9: Student Data Analytics - Donut Chart (Student Distribution by Grade Division and School Sector)
graph9_page = html.Div([
    dcc.Graph(figure=fig9, id="Student-division-donut-chart")
    ])


# Graph 10: School Data Analytics - Sankey Chart (School Population per Sector, Sub-Classification, and Modified COC)
graph10_page = html.Div([
    dcc.Graph(figure=fig10, id="school-sankey-chart")
    ]),

# Graph 11: School Data Analytics - Line-Bar Chart (School Count by School Type and Sector)
graph11_page = html.Div([
    dcc.Graph(figure=fig11, id="school-bar-line-chartt")
    ])


# Data Comparison Graph - Gender
comparison_gender_page =  html.Div([
    html.Div([
        html.Div([
            html.H2("Data Comparison - Gender Analysis", style={
                'textAlign': 'center',
                'fontFamily': 'Arial Black',
                'fontSize': '22px',
                'marginBottom': '10px'
            }),

            html.Div([
                html.Label("Select Region:", style={
                    'fontWeight': 'bold',
                    'fontFamily': 'Arial',
                    'marginBottom': '5px'
                }),
                dcc.Dropdown(
                    id='comparison-gender-region-dropdown',
                    options=[{'label': r, 'value': r} for r in get_region_list()],
                    value='All Regions',
                    style={'width': '150px', 'fontFamily': 'Arial'}
                )
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'flex-start',
                'marginBottom': '20px',
                'fontFamily': 'Arial'
            }),

            dcc.Graph(id='comparison-gender-graph')
        ],
        style={
            'backgroundColor': 'white',
            'padding': '20px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'borderRadius': '10px',
            'maxWidth': '600px',
            'margin': 'auto'
        })
    ])
])

# Data Comparison Graph - Grade Level
comparison_grade_level_page = html.Div([
    html.H2("Data Comparison - Grade Level Analysis", style={
        'textAlign': 'center',
        'fontFamily': 'Arial Black',
        'fontSize': '22px',  # Reduced font size
        'marginBottom': '20px'
    }),

    html.Div([
        html.Label("Select Region:", style={
            'fontWeight': 'bold',
            'fontFamily': 'Arial',
            'fontSize': '14px',  # Reduced font size
            'marginRight': '10px'
        }),

        dcc.Dropdown(
            id='comparison-grade-level-region-dropdown',
            options=[{'label': r, 'value': r} for r in get_region_list()],
            value='All Regions',
            style={'width': '150px'}
        )
    ], style={
        'display': 'flex',
        'justifyContent': 'flex-start',
        'fontFamily': 'Arial',
        'alignItems': 'center',
        'marginBottom': '8px',
        'gap': '10px'
    }),

    dcc.Graph(id='comparison-grade-level-graph', style={'marginTop': '8px'})
],
style={
    'backgroundColor': 'white',
    'padding': '12px',  # Reduced padding
    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
    'borderRadius': '10px',
    'maxWidth': '620px',  # Reduced max width
    'margin': 'auto'
})

# Data Comparison SHS Strand Page
comparison_shs_strand_page = html.Div([
    html.Div([
        html.Div([
            html.H2("Data Comparison - SHS Strand Analysis", style={
            'textAlign': 'center',
            'fontFamily': 'Arial Black',
            'fontSize': '22px',
            'marginBottom': '10px'
        }),

            html.Div([
                html.Label("Select Region:", style={
                'fontWeight': 'bold',
                'fontFamily': 'Arial Black',
                'marginBottom': '5px'
                }),
                dcc.Dropdown(
                    id='comparison-shs-strand-region-dropdown',
                    options=[{'label': r, 'value': r} for r in get_region_list()],
                    value='All Regions',
                    style={'width': '50%', 'fontFamily': 'Arial'}
                )
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'flex-start',
                'marginBottom': '20px',
                'fontFamily': 'Arial'
            }),
            html.Div([
            dcc.Graph(id='comparison-shs-strand-graph')], style={
            'display': 'flex',
            'justifyContent': 'center'
        })
        ],
        style={
        'backgroundColor': 'white',
        'padding': '20px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
        'borderRadius': '10px',
        'maxWidth': '600px',
        'margin': 'auto'
        })
    ])
])

# Data Comparison Grade Division Page
comparison_grade_division_page = html.Div([
    html.H2("Data Comparison - Grade Division Analysis", style={
        'textAlign': 'center',
        'fontFamily': 'Arial Black',
        'fontSize': '28px',
        'marginBottom': '10px'
    }),

    html.Div([
        html.Label("Select Region:", style={
            'fontWeight': 'bold',
            'fontFamily': 'Arial',
            'fontSize': '16px',
            'marginRight': '10px'
            }),
        dcc.Dropdown(
            id='comparison-grade-division-region-dropdown',
            options=[{'label': r, 'value': r} for r in get_region_list()],
            value='All Regions',
            style={'width': '150px', 'fontFamily': 'Arial'}
        )
    ], style={
        'display': 'flex',
        'justifyContent': 'flex-start',
        'alignItems': 'center',
        'marginTop': '10px',
        'gap': '10px'
    }),

    dcc.Graph(id='comparison-grade-division-graph')

], style={
    'backgroundColor': 'white',
    'padding': '20px',
    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
    'borderRadius': '10px',
    'maxWidth': '800px',
    'margin': 'auto'
})

# Data Comparison Sector Page
comparison_sector_page = html.Div(style={'backgroundColor': 'transparent', 'padding': '20px'}, children=[
    html.Div(style={
        'maxWidth': '750px',
        'margin': '0 auto',
        'padding': '20px',
        'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.1)',
        'borderRadius': '10px',
        'backgroundColor': 'white',
    }, children=[


    html.H1("Data Comparison - Sector Analysis", style={
            'textAlign': 'center',
            'fontFamily': 'Arial Black',
            'fontSize': '20px',
            'marginBottom': '10px'
        }),

        html.Div([
            html.Div([
                html.Label("Select Region:", style={
                    'fontFamily': 'Arial Black',
                    'fontSize': '16px',
                    'marginRight': '10px'
                }),
                dcc.Dropdown(
                    id='comparison-sector-region-dropdown',
                    options=[{'label': r, 'value': r} for r in get_region_list()],
                    value="All Regions",
                    clearable=False,
                    style={'width': '150px', 'fontFamily': 'Arial'}
                )
            ], style={
                'display': 'flex',
                'justifyContent': 'flex-start',
                'alignItems': 'center',
                'marginBottom': '0.01px',
                'paddingLeft': '50px'
            }),

            html.Div([
                dcc.Graph(id='comparison-sector-graph')
            ], style={'display': 'flex', 'justifyContent': 'center'})
        ], style={'fontFamily': 'Arial'})
    ])
])

# Data Comparison School Type Page
comparison_school_type_page = html.Div(style={'backgroundColor': 'white', 'padding': '20px'}, children=[
    html.Div(style={
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
        'borderRadius': '8px',
        'padding': '20px',
        'backgroundColor': 'white',
        'margin': '0 auto',
        'maxWidth': '750px',
        'height': '500px',
        'overflow': 'hidden'
    }, children=[
        html.H1("Data Comparison - School Type Analysis", style={
            'textAlign': 'center',
            'fontFamily': 'Arial Black',
            'fontSize': '20px',
            'marginBottom': '10px'
        }),
        
    html.Div([
            html.Div([
                dcc.Graph(id='comparison-school-type-graph', style={'marginTop': '20px'})
            ], style={'display': 'flex', 'justifyContent': 'center'}),

            html.Div([
                html.Div("Select Region:", style={
                    'textAlign': 'left',
                    'fontFamily': 'Arial Black',
                    'fontSize': '16px',
                    'marginBottom': '5px'
                }),

                dcc.Dropdown(
                id='comparison-school-type-region-dropdown',
                options=[{'label': r, 'value': r} for r in get_region_list()],
                value="All Regions",
                clearable=False,
                style={'width': '150px'}
            )
        ], style={
                'position': 'absolute',
                'top': '20px',
                'left': '30px',
                'zIndex': '10',
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'flex-start',
            })
        ], style={'position': 'relative', 'height': '490px', 'fontFamily': 'Arial'})
    ])
])


upload_student_page = html.Div([
    html.H2("Upload Student Dataset"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '2px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='file-selected', style={'marginTop': '20px', 'textAlign': 'center'}),
    dcc.Store(id='store-uploaded-file'), 
    dcc.Store(id='store-upload-context', data='student'), 
    html.Div(id='submit-button-container', style={'marginTop': '20px', 'textAlign': 'center'}),\
    html.Div(id='upload-response', style={'marginTop': '20px', 'textAlign': 'center'}),
])

upload_school_page = html.Div([
    html.H2("Upload School Dataset"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '2px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='file-selected', style={'marginTop': '20px', 'textAlign': 'center'}),
    dcc.Store(id='store-uploaded-file'),  
    dcc.Store(id='store-upload-context', data='school'), 
    html.Div(id='submit-button-container', style={'marginTop': '20px', 'textAlign': 'center'}),\
    html.Div(id='upload-response', style={'marginTop': '20px', 'textAlign': 'center'}),
])


index_page = html.Div([
    html.H1("Welcome to Student Dashboard"),
    html.P("Graphs 7–11 preview below for quick visualization:"),

    html.Div([
        html.H3("Graph 7: Student Population by Grade Level"),
        dcc.Graph(id='student-population-bar-chart', figure=fig7),

        html.H3("Graph 8: Student Strand Area Chart"),
        dcc.Graph(id='Student-strand-area-chart', figure=fig8),

        html.H3("Graph 9: Student Division Donut Chart"),
        dcc.Graph(id='Student-division-donut-chart', figure=fig9),

        html.H3("Graph 10: School Sankey Chart"),
        dcc.Graph(id='school-sankey-chart', figure=fig10),

        html.H3("Graph 11: School Bar-Line Chart"),
        dcc.Graph(id='school-bar-line-chart', figure=fig11),

        html.H2("Upload Student Dataset"),
        upload_student_page,
    ], style={'padding': '20px'})
])

app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='store-upload-context'),
        dcc.Store(id='store-student'),    
        dcc.Store(id='store-school'),  
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
    elif pathname == '/data-comparison-shs-strand':
        return comparison_shs_strand_page
    elif pathname == '/data-comparison-grade-division':
        return comparison_grade_division_page
    elif pathname == '/data-comparison-sector':
        return comparison_sector_page
    elif pathname == '/data-comparison-school-type': 
        return comparison_school_type_page
    elif pathname == '/upload_student':
        return upload_student_page, 'student'
    elif pathname == '/upload_school':
        return upload_student_page, 'school'
    else:
        return index_page
    
@app.callback(
    Output('student-population-bar-chart', 'figure'), 
    Output('Student-strand-area-chart', 'figure'), 
    Output('Student-division-donut-chart', 'figure'), 
    Input('store-student', 'data'),
    prevent_initial_call=True 
)
def update_graph_student(data):
    if not data:
        raise dash.exceptions.PreventUpdate
    try:
        df = load_student_data()
        fig7 = generate_graph7(df)
        fig8 = generate_graph8(df)
        fig9 = generate_graph9(df)
        return fig7, fig8, fig9
    except Exception as e:
        print("Error generating student graphs:", e)
        raise dash.exceptions.PreventUpdate

@app.callback(
    Output('school-sankey-chart', 'figure'), 
    Output('school-bar-line-chart', 'figure'),  
    Input('store-school', 'data'),
    prevent_initial_call=True
)
def update_graph_school(data):
    if not data:
        raise dash.exceptions.PreventUpdate
    try:
        df = load_school_data()
        fig10 = generate_graph10(df)
        fig11 = generate_graph11(df)
        return fig10, fig11
    except Exception as e:
        print("Error generating school graphs:", e)
        raise dash.exceptions.PreventUpdate

    
@app.callback(
    Output('store-student', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('store-upload-context', 'data'),
    prevent_initial_call=True
)
def update_store_after_upload_student(contents, filename, upload_type):
    if contents and filename and upload_type == "student":
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        uploaded_path = os.path.join("Data/Raw_data", filename)

        try:
            with open(uploaded_path, 'wb') as f:
                f.write(decoded)

            df = pd.read_excel(uploaded_path) if uploaded_path.endswith('.xlsx') else pd.read_csv(uploaded_path)

            # Debugging statement
            print(f"Student dataset uploaded: {df.head()}")

            # Update config.json
            with open('config.json', 'r') as f:
                config = json.load(f)
            config['student_dataset_path'] = uploaded_path
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)

            return df.to_dict('records')
        except Exception as e:
            print(f"Error processing uploaded student file: {e}")
            return dash.no_update
    return dash.no_update

@app.callback(
    Output('store-school', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('store-upload-context', 'data'),
    prevent_initial_call=True
)
def update_store_after_upload_school(contents, filename, upload_type):
    if contents and filename and upload_type == "school":
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        uploaded_path = os.path.join("Data/Raw_data", filename)

        try:
            with open(uploaded_path, 'wb') as f:
                f.write(decoded)

            df = pd.read_excel(uploaded_path) if uploaded_path.endswith('.xlsx') else pd.read_csv(uploaded_path)

            # Debugging statement
            print(f"School dataset uploaded: {df.head()}")

            # Update config.json
            with open('config.json', 'r') as f:
                config = json.load(f)
            config['school_dataset_path'] = uploaded_path
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)

            return df.to_dict('records')
        except Exception as e:
            print(f"Error processing uploaded school file: {e}")
            return dash.no_update
    return dash.no_update

@app.callback(
    Output('upload-response', 'children'),
    Input('submit-upload', 'n_clicks'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('store-upload-context', 'data'),
    prevent_initial_call=True
)
def submit_upload(n_clicks, contents, filename, upload_context):
    if n_clicks == 0 or contents is None:
        return ''

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    files = {
        'file': (filename, BytesIO(decoded))
    }
    data = {
        'type': upload_context
    }

    try:
        response = requests.post('http://localhost:8050/upload_dataset', files=files, data=data)

        if response.status_code == 200:
            # Debugging statement
            print(f"Upload successful: {filename}")
            return html.Div([
                html.H4('Upload Successful!', style={'color': 'green'})
            ])
        else:
            print(f"Upload failed: {response.text}")
            return html.Div([
                html.H4('Upload Failed!', style={'color': 'red'}),
                html.Pre(response.text)
            ])
    except Exception as e:
        print(f"Error during upload: {e}")
        return html.Div([
            html.H4('Error during upload!', style={'color': 'red'}),
            html.Pre(str(e))
        ])

if __name__ == '__main__':
    app.run(debug=False)
