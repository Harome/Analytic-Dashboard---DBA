import dash
from dash import dcc, html, dash_table, Input, Output, State, ctx, MATCH, ALL
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from flask import request, jsonify
from flask_cors import CORS
import base64
import time
import os
from Data.Clean_data.stuscho import (
    generate_graph7, generate_graph8, generate_graph9, generate_graph10, generate_graph11, load_student_data, load_school_data, load_data
)
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

last_update = {"student": 0, "school": 0}

@app.server.route("/last_update")
def get_last_update():
    return jsonify(last_update)

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
    ], style={"display": "flex", "justifyContent": "center", "alignItems": "center", 'paddingTop': '20px'})


# Graph 9: Student Data Analytics - Donut Chart (Student Distribution by Grade Division and School Sector)
graph9_page = html.Div([
    dcc.Graph(figure=fig9, id="Student-division-donut-chart")
    ], style={"display": "flex", "justifyContent": "center", "alignItems": "center", 'paddingTop': '20px'})


# Graph 10: School Data Analytics - Sankey Chart (School Population per Sector, Sub-Classification, and Modified COC)
graph10_page = html.Div([
    dcc.Graph(figure=fig10, id="school-sankey-chart")
    ], style={"display": "flex", "justifyContent": "center", "alignItems": "center", 'margin': '0px'})

# Graph 11: School Data Analytics - Line-Bar Chart (School Count by School Type and Sector)
graph11_page = html.Div([
    dcc.Graph(figure=fig11, id="school-bar-line-chartt")
    ], style={"display": "flex", "justifyContent": "center", "alignItems": "center", 'margin': '0px'})

upload_student_page = html.Div([
    html.H2("Upload Student Dataset"),
    dcc.Upload(
        id='upload-data-student',
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
    html.Div(id='file-selected-student', style={'marginTop': '20px', 'textAlign': 'center'}),
    html.Div(id='upload-response-student', style={'marginTop': '20px', 'textAlign': 'center'}),
    html.Div(id='upload-notification-student', style={'marginTop': '10px'}),
    dcc.Store(id='store-upload-context-student', data='student'), 
])

upload_school_page = html.Div([
    html.H2("Upload School Dataset"),
    dcc.Upload(
        id='upload-data-school',
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
    html.Div(id='file-selected-school', style={'marginTop': '20px', 'textAlign': 'center'}),
    html.Div(id='upload-response-school', style={'marginTop': '20px', 'textAlign': 'center'}),
    html.Div(id='upload-notification-school', style={'marginTop': '10px'}),
    dcc.Store(id='store-upload-context-school', data='school'), 
])

student_graphs_page = html.Div([
    html.H2("Student Dataset Visualizations"),
    graph7_page,
    graph8_page,
    graph9_page,
    html.Hr(),
    upload_student_page
])

school_graphs_page = html.Div([
    html.H2("School Dataset Visualizations"),
    graph10_page,
    graph11_page,
    html.Hr(),
    upload_school_page
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
        dcc.Graph(id='school-bar-line-chartt', figure=fig11),

        upload_student_page,

        upload_school_page,

        html.Div([
        html.A("📊 Student Graphs Page", href="/student_page", style={'marginRight': '20px'}),
        html.A("🏫 School Graphs Page", href="/school_page"),
        ], style={'paddingBottom': '20px'}),
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
    if pathname == '/student_page':
        return student_graphs_page
    elif pathname == '/school_page':
        return school_graphs_page
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
    elif pathname == '/upload_student':
        return upload_student_page
    elif pathname == '/upload_school':
        return upload_school_page
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
    Output('school-bar-line-chartt', 'figure'),  
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
    Input('upload-data-student', 'contents'),
    State('upload-data-student', 'filename'),
    State('store-upload-context-student', 'data'),
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
    Input('upload-data-school', 'contents'),
    State('upload-data-school', 'filename'),
    State('store-upload-context-school', 'data'),
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
    Output('upload-notification-student', 'children'),
    Input('store-student', 'data'),
    prevent_initial_call=True
)
def notify_upload_student(student_data):
    if ctx.triggered_id == 'store-student' and student_data:
        last_update["student"] = time.time()
        return html.Div("✅ Student data loaded successfully!", style={'color': 'green'})
    return dash.no_update

@app.callback(
    Output('upload-notification-school', 'children'),
    Input('store-school', 'data'),
    prevent_initial_call=True
)
def notify_upload_school(school_data):
    if ctx.triggered_id == 'store-school' and school_data:
        last_update["school"] = time.time()
        return html.Div("✅ School data loaded successfully!", style={'color': 'green'})
    return dash.no_update

if __name__ == '__main__':
    app.run(debug=False)