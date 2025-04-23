import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

# Load and prepare your data
df_school = pd.read_excel("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")
df_school.columns = df_school.columns.str.strip()
df_school['Region'] = df_school['Region'].str.strip()

region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

grade_columns_male = [col for col in df_school.columns if 'Male' in col]
grade_columns_female = [col for col in df_school.columns if 'Female' in col]

# Create Dash app
app = Dash(__name__)
app.title = "Data Comparison"

# App layout
app.layout = html.Div([
    html.H2("Total Student Enrollment by Gender per Region", style={
        'textAlign': 'center',
        'fontFamily': 'Arial Black',
        'fontSize': '28px',
        'marginBottom': '20px'
    }),

    html.Div([
        html.Label("Select Region:", style={
            'fontWeight': 'bold',
            'fontSize': '16px',
            'marginRight': '10px',
            'fontFamily': 'Arial'
        }),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': 'All Regions', 'value': 'All Regions'}] + [{'label': r, 'value': r} for r in region_order],
            value='All Regions',
            style={'width': '250px', 'fontFamily': 'Arial'},
        )
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'marginBottom': '30px',
        'gap': '10px'
    }),

    dcc.Graph(id='gender-line-graph')
],
style={
    'backgroundColor': 'white',
    'padding': '20px',
    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
    'borderRadius': '10px',
    'maxWidth': '900px',
    'margin': 'auto'
})

# Callback function to update the graph
@app.callback(
    Output('gender-line-graph', 'figure'),
    Input('region-dropdown', 'value')
)
def update_graph(selected_region):
    if selected_region == 'All Regions':
        gender_totals_by_region = df_school.groupby('Region')[grade_columns_male + grade_columns_female].sum()
        gender_totals_by_region['Total_Male'] = gender_totals_by_region[grade_columns_male].sum(axis=1)
        gender_totals_by_region['Total_Female'] = gender_totals_by_region[grade_columns_female].sum(axis=1)
        gender_totals_by_region = gender_totals_by_region.reindex(region_order)
        gender_totals_by_region = gender_totals_by_region.dropna(subset=['Total_Male', 'Total_Female'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=gender_totals_by_region.index,
            y=gender_totals_by_region['Total_Male'],
            mode='lines+markers',
            name='Male',
            line=dict(color='blue', width=3)
        ))

        fig.add_trace(go.Scatter(
            x=gender_totals_by_region.index,
            y=gender_totals_by_region['Total_Female'],
            mode='lines+markers',
            name='Female',
            line=dict(color='#ff2c2c', width=2, dash='dash'),
            fill='tozeroy',
            fillcolor='rgba(255, 105, 180, 0.3)'
        ))
    else:
        filtered_df = df_school[df_school['Region'] == selected_region]
        total_male = filtered_df[grade_columns_male].sum().sum()
        total_female = filtered_df[grade_columns_female].sum().sum()

        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=['Male', 'Female'],
            values=[total_male, total_female],
            hole=0.3,
            textinfo='label+percent',
            marker=dict(
                colors=['#5c6dc9', '#ee6b6e'],
                line=dict(color='black', width=2)
            ),
            hoverinfo='label+percent+value',
            pull=[0.05, 0.05]
        ))

    fig.update_layout(
        title={
            'text': f"<b>{selected_region}</b>",
            'y': 0.92,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(family="Arial Black", size=16)
        },
        xaxis_title='Region' if selected_region == 'All Regions' else 'Gender',
        yaxis_title='Number of Students',
        template='plotly_white',
        font=dict(family="Arial Black", size=12, color="black"),
        height=450,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="center",
            x=0.5
        )
    )
    return fig

## Grade Level
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

df_school.columns = df_school.columns.str.strip()
df_school['Region'] = df_school['Region'].str.strip()

region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Total Student Enrollment per Grade Level", style={
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
            options=[{'label': 'All Regions', 'value': 'All Regions'}] + [{'label': r, 'value': r} for r in region_order],
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

@app.callback(
    Output('grade-bar-graph', 'figure'),
    Input('grade-region-dropdown', 'value')
)
def update_bar_chart(selected_region):
    if selected_region == 'All Regions':
        df_filtered = df_school
    else:
        df_filtered = df_school[df_school['Region'] == selected_region]

    grade_totals = []
    for grade, cols in grade_levels.items():
        total = df_filtered[cols].sum().sum()
        grade_totals.append({"Grade Level": grade, "Total Students": total})

    df_grade_totals = pd.DataFrame(grade_totals)
    df_grade_totals['ColorScale'] = df_grade_totals.index

    fig = go.Figure()
    for i, row in df_grade_totals.iterrows():
        fig.add_trace(go.Bar(
            x=[row["Grade Level"]],
            y=[row["Total Students"]],
            name=row["Grade Level"],
            marker=dict(
                color=row["ColorScale"],
                colorscale="Bluered",
                cmin=df_grade_totals["ColorScale"].min(),
                cmax=df_grade_totals["ColorScale"].max(),
                line=dict(color="black", width=2)),
            width=0.9
        ))

    fig.update_layout(
        xaxis_title="Grade Level",
        yaxis_title="Total Students",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial Black", size=10),
        width=800,
        height=400,
        showlegend=True,
        legend=dict(orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="center",
            x=0.5,
            traceorder='normal',
            itemclick='toggleothers',
            itemsizing='constant',
            bgcolor='rgba(255, 255, 255, 0.8)',
        ),
        xaxis=dict(
            tickangle=0,
            tick_font=dict(size=8),
            title_font=dict(size=10)),
        yaxis=dict(
            title_font=dict(size=10),
            tick_font=dict(size=8)),
        margin=dict(b=60, t=80, l=60, r=60),
        bargap=0.2
    )

    return fig

## SHS Strand
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

df_school.columns = df_school.columns.str.strip()
df_school['Region'] = df_school['Region'].str.strip()

shs_strands = {
    "STEM": ['G11_STEM_Male', 'G11_STEM_Female', 'G12_STEM_Male', 'G12_STEM_Female'],
    "ABM": ['G11_ABM_Male', 'G11_ABM_Female', 'G12_ABM_Male', 'G12_ABM_Female'],
    "HUMSS": ['G11_HUMSS_Male', 'G11_HUMSS_Female', 'G12_HUMSS_Male', 'G12_HUMSS_Female'],
    "GAS": ['G11_GAS_Male', 'G11_GAS_Female', 'G12_GAS_Male', 'G12_GAS_Female'],
    "TVL": ['G11_TVL_Male', 'G11_TVL_Female', 'G12_TVL_Male', 'G12_TVL_Female'],}

region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

region_list = ['All Regions'] + region_order

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H2("SHS Enrollment by Strand", style={
                'textAlign': 'center',
                'fontFamily': 'Arial Black',
                'fontSize': '22px',
                'marginBottom': '10px'
            }),

            html.Div([
                html.Label("Select Region:", style={'fontWeight': 'bold', 'fontFamily': 'Arial'}),
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[{'label': r, 'value': r} for r in region_list],
                    value='All Regions',
                    style={'width': '60%', 'margin': 'auto'}
                )
            ], style={'textAlign': 'center', 'marginBottom': '20px', 'fontFamily': 'Arial'}),

            dcc.Graph(id='strand-pie')
        ],
        style={
            'backgroundColor': 'white',
            'padding': '20px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'borderRadius': '10px',
            'maxWidth': '600px',
            'margin': 'auto'})])])

@app.callback(
    Output('strand-pie', 'figure'),
    Input('region-dropdown', 'value'))
def update_pie(selected_region):
    if selected_region == 'All Regions':
        filtered_df = df_school
    else:
        filtered_df = df_school[df_school['Region'] == selected_region]

    shs_totals = []
    for strand, cols in shs_strands.items():
        total = filtered_df[cols].sum().sum()
        shs_totals.append({"SHS Strand": strand, "Total Students": total})

    df_shs_totals = pd.DataFrame(shs_totals)

    custom_colors = ['#e1bbd9', '#6cc24a', '#5c6dc9', '#f1b04c', '#ee6b6e']

    fig = px.pie(
        df_shs_totals,
        names="SHS Strand",
        values="Total Students",
        color="SHS Strand",
        color_discrete_sequence=custom_colors
    )

    fig.update_traces(
        marker=dict(line=dict(color='black', width=2))
    )

    fig.update_layout(
        title={
            'text': f"<b>{selected_region}</b>",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(family="Arial Black", size=16)
        },
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial Black", size=14),
        margin=dict(l=40, r=40, t=50, b=50),
        showlegend=True,
        width=500,
        height=400
    )

    return fig
##grade Division
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

df_school.columns = df_school.columns.str.strip()
df_school['Region'] = df_school['Region'].str.strip()

region_order = ['All Regions', 'Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

grouped = df_school.groupby("Region")

def compute_region_totals():
    data = {"Region": [], "Elementary": [], "JuniorHigh": [], "SeniorHigh": []}
    for region in region_order[1:]:
        group = grouped.get_group(region)
        data["Region"].append(region)
        data["Elementary"].append(group[elementary_male + elementary_female].sum().sum())
        data["JuniorHigh"].append(group[junior_high_male + junior_high_female].sum().sum())
        data["SeniorHigh"].append(group[senior_high_male + senior_high_female].sum().sum())
    return pd.DataFrame(data)

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Total Enrolled Students per Region by Division", style={
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
            id='region-selector',
            options=[{'label': r, 'value': r} for r in region_order],
            value='All Regions',
            style={'width': '250px', 'fontFamily': 'Arial'}
        )
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'marginTop': '10px',
        'gap': '10px'
    }),

    dcc.Graph(id='division-chart'),
], style={
    'backgroundColor': 'white',
    'padding': '20px',
    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
    'borderRadius': '10px',
    'maxWidth': '900px',
    'margin': 'auto'
})

@app.callback(
    Output('division-chart', 'figure'),
    Input('region-selector', 'value')
)
def update_division_chart(selected_region):

    df_region_totals = compute_region_totals()

    if selected_region != 'All Regions':
        df_region_totals = df_region_totals[df_region_totals['Region'] == selected_region]

    fig = go.Figure()

    if selected_region == 'All Regions':
        fig.add_trace(go.Bar(
            name='Elementary',
            x=df_region_totals['Region'],
            y=df_region_totals['Elementary'],
            marker_color='#5c6dc9',
            width=0.8
        ))
        fig.add_trace(go.Bar(
            name='Junior High',
            x=df_region_totals['Region'],
            y=df_region_totals['JuniorHigh'],
            marker_color='#919bf1',
            width=0.8
        ))
        fig.add_trace(go.Bar(
            name='Senior High',
            x=df_region_totals['Region'],
            y=df_region_totals['SeniorHigh'],
            marker_color='#a0aadf',
            width=0.8
        ))

        fig.update_layout(
            xaxis_title='Region',
            yaxis_title='Enrollment',
            xaxis_tickfont=dict(size=9),
            yaxis_tickfont=dict(size=10),
            height=400,
            width=800,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial Black", size=11),
            margin=dict(l=60, r=60, t=80, b=60),
            legend=dict(
                title='',
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            ),
            bargap=0.1,
            bargroupgap=0.1,
            barmode='stack',
            xaxis=dict(tickangle=20, automargin=True),
            yaxis=dict(automargin=True)
        )
        return fig

    else:
        region_data = df_region_totals.iloc[0]

        fig.add_trace(go.Pie(
            labels=['Elementary', 'Junior High', 'Senior High'],
            values=[region_data['Elementary'], region_data['JuniorHigh'], region_data['SeniorHigh']],
            marker_colors=['#5c6dc9', '#919bf1', '#a0aadf'],
            marker=dict(
                line=dict(color='black', width=2)),
        ))

        # Add title for pie chart
        fig.update_layout(
          title="{}".format(selected_region),
          title_x=0.5,
          title_y=0.93,
          plot_bgcolor='white',
          paper_bgcolor='white',
          font=dict(family="Arial Black", size=11),
          margin=dict(l=60, r=60, t=80, b=60),
          legend=dict(
              orientation="h",
              yanchor="bottom",
              y=1,
              xanchor="center",
              x=0.5,
              font=dict(size=10)
          ),
          xaxis=dict(automargin=True),
          yaxis=dict(automargin=True)
        )

        return fig

## Sector
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

sector_region_data = df_school.groupby(['Region', 'Sector']).sum(numeric_only=True).reset_index()
sector_region_data['Total'] = sector_region_data[grade_columns_male + grade_columns_female].sum(axis=1)
sector_region_pivot = sector_region_data.pivot_table(index='Region', columns='Sector', values='Total', aggfunc='sum', fill_value=0)
sector_region_pivot = sector_region_pivot.reindex(region_order)
sector_region_pivot = sector_region_pivot.reset_index()

def create_figure(selected_region):
    sector_colors = ['#f1b04c', '#f94449', '#5c6dc9', '#6bb0a6']
    if selected_region != "All Regions":
        filtered_data = sector_region_pivot[sector_region_pivot['Region'] == selected_region]
        fig = go.Figure(data=[go.Pie(
            labels=filtered_data.columns[1:],
            values=filtered_data.iloc[0, 1:],
            marker=dict(
                colors=sector_colors[:len(filtered_data.columns[1:])],
                line=dict(color='black', width=2)
            )
        )])
        fig.update_layout(
            font=dict(family="Arial Black", size=11, color="black"),
            title_font=dict(size=20, color="black"),
            width=800, height=500,
            margin=dict(l=60, r=60, t=100, b=60),
            showlegend=True,
            title=None
        )
    else:
        filtered_data = sector_region_pivot
        fig = go.Figure()
        for sector in filtered_data.columns[1:]:
            fig.add_trace(go.Scatter(
                x=filtered_data['Region'], y=filtered_data[sector],
                name=sector, mode='lines+markers',
                fill='tonexty', marker=dict(size=6), line=dict(width=2)
            ))
        fig.update_layout(
            font=dict(family="Arial Black", size=11, color="black"),
            title_font=dict(size=20, color="black"),
            width=800, height=500,
            margin=dict(l=60, r=60, t=100, b=60),
            xaxis=dict(
                categoryorder='array',
                categoryarray=region_order,
                tickfont=dict(color="black"),
                titlefont=dict(color="black")),
            yaxis=dict(
                tickfont=dict(color="black"),
                titlefont=dict(color="black")),
            hovermode="x unified",
            legend=dict(
                orientation="h", yanchor="top",
                y=1.1, xanchor="center",
                x=0.5, font=dict(color="black")),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)'
        )
    return fig

app = dash.Dash(__name__)
region_options = ['All Regions'] + [r for r in region_order if r != 'All Regions']

app.layout = html.Div(style={'backgroundColor': 'transparent', 'padding': '20px'}, children=[
    html.H1("Total Students Enrolled by Sector per Region", style={
        'textAlign': 'center',
        'fontFamily': 'Arial Black',
        'fontSize': '24px',
        'marginBottom': '10px'
    }),
    html.Div([
        html.Div([
            dcc.Graph(id='sector-distribution-graph', figure=create_figure("All Regions"), style={'marginTop': '50px'})
        ], style={'display': 'flex', 'justifyContent': 'center'}),
        html.Div([
            html.Div("Select Region:", style={
                'textAlign': 'center',
                'fontFamily': 'Arial Black',
                'fontSize': '16px',
                'marginBottom': '5px'
            }),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': r, 'value': r} for r in region_options],
                value="All Regions",
                clearable=False,
                style={'width': '300px', 'margin': '0 auto'}
            )
        ], style={
            'position': 'absolute',
            'top': '10px',
            'left': '50%',
            'transform': 'translateX(-50%)',
            'zIndex': '10',
            'width': '100%',
            'textAlign': 'center'
        })
    ], style={'position': 'relative', 'height': '500px', 'fontFamily': 'Arial'})
])

@app.callback(
    Output('sector-distribution-graph', 'figure'),
    Input('region-dropdown', 'value')
)
def update_graph(selected_region):
    return create_figure(selected_region)

## School Type
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df_school["Total_Students"] = df_school[
    elementary_male + elementary_female +
    junior_high_male + junior_high_female +
    senior_high_male + senior_high_female
].sum(axis=1)

app = dash.Dash(__name__)

def create_figure(selected_region):
    if selected_region == "All Regions":
        filtered_df = df_school.copy()
        school_distribution = filtered_df.groupby(["Region", "School_Type"])["Total_Students"].sum().reset_index()
        school_distribution["Region"] = pd.Categorical(school_distribution["Region"], categories=region_order, ordered=True)
        school_distribution = school_distribution.sort_values("Region")

        fig = px.bar(
            school_distribution,
            x="Total_Students",
            y="Region",
            color="School_Type",
            orientation="h",
            labels={"Region": "Region", "Total_Students": "Total Number of Students"},
            category_orders={"Region": region_order},
            color_discrete_sequence=["#e74c3c", "#c0392b", "#ff6f61", "#ff4d4d"]
        )
    else:
        filtered_df = df_school[df_school["Region"] == selected_region]
        school_distribution = filtered_df.groupby("School_Type")["Total_Students"].sum().reset_index()

        fig = px.pie(
            school_distribution,
            names="School_Type",
            values="Total_Students",
            labels={"Total_Students": "Total Number of Students"},
            title=f"School Distribution for {selected_region}",
            hole=0.3,
            color_discrete_sequence=["#e74c3c", "#c0392b", "#ff6f61", "#ff4d4d"]
        )

        fig.update_traces(
            marker=dict(line=dict(color='black', width=1))
        )

    fig.update_layout(
        title=None,
        height=500,
        width=800,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial Black", size=12),
        margin=dict(l=60, r=60, t=80, b=60),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.9,
            xanchor="left",
            x=1.05,
            font=dict(size=10),
            bordercolor="black",
            borderwidth=1,
            bgcolor="white"
        )
    )

    return fig

app.layout = html.Div(style={'backgroundColor': 'white', 'padding': '20px'}, children=[
    html.H1("Number of Students Enrolled by School Type", style={
        'textAlign': 'center',
        'fontFamily': 'Arial Black',
        'fontSize': '24px',
        'marginBottom': '10px'
    }),

    html.Div([
        html.Div([
            dcc.Graph(id='school-type-graph', figure=create_figure("All Regions"), style={'marginTop': '50px'})
        ], style={'display': 'flex', 'justifyContent': 'center'}),

        html.Div([
            html.Div("Select Region:", style={
                'textAlign': 'center',
                'fontFamily': 'Arial Black',
                'fontSize': '16px',
                'marginBottom': '5px'
            }),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': r, 'value': r} for r in region_order],
                value="All Regions",
                clearable=False,
                style={'width': '300px', 'margin': '0 auto'}
            )
        ], style={
            'position': 'absolute',
            'top': '10px',
            'left': '50%',
            'transform': 'translateX(-50%)',
            'zIndex': '10',
            'width': '100%',
            'textAlign': 'center'
        })
    ], style={'position': 'relative', 'height': '500px', 'fontFamily': 'Arial'})
])

@app.callback(
    Output('school-type-graph', 'figure'),
    Input('region-dropdown', 'value')
)
def update_graph(selected_region):
    return create_figure(selected_region)


if __name__ == '__main__':
    app.run(debug=True)