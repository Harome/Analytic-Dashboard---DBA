import pandas as pd
import plotly.express as px
import json
from Initialization.enrollment_data_loader import load_school_data

# Load your dataset using your custom loader
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")
df_school = data['df_school']

region_code_name = {
    "PH00": "NCR", "PH01": "Region I", "PH02": "Region II", "PH03": "Region III",
    "PH05": "Region V", "PH06": "Region VI", "PH07": "Region VII", "PH08": "Region VIII",
    "PH09": "Region IX", "PH10": "Region X", "PH11": "Region XI", "PH12": "Region XII",
    "PH13": "CARAGA", "PH14": "BARMM", "PH15": "CAR", "PH40": "Region IV-A", "PH41": "MIMAROPA"
}

school_data = df_school.groupby('Region').count()
school_data = school_data["Division"].rename('Total Schools').drop(index='PSO').to_dict()

student_data = (
    df_school.drop(columns=['BEIS_School_ID'])
    .groupby('Region').sum(numeric_only=True)
    .sum(axis=1).rename('Total Students')
    .drop(index='PSO')
    .to_dict()
)

student_data = dict(sorted(student_data.items(), key=lambda x: x[1], reverse=True))
school_data = dict(sorted(school_data.items(), key=lambda x: x[1], reverse=True))

name_to_code = {v: k for k, v in region_code_name.items()}

df = pd.DataFrame({
    'RegionName': list(student_data.keys()),
    'RegionCode': [name_to_code[name] for name in student_data.keys()],
    'Population': list(student_data.values()),
    'School Count': list(school_data.values())
})

# Load your GeoJSON file (adjust path as needed)
with open('/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Backend/Graph Visualz/Additional/ph.json') as f:
    geojson = json.load(f)

fig = px.choropleth_mapbox(
    df,
    geojson=geojson,
    locations='RegionCode',
    featureidkey='properties.id',
    color='Population',
    hover_name='RegionName',
    hover_data={'School Count': ':,.0f','RegionCode': False, 'Population': ':,.0f'},
    color_continuous_scale=[
        [0.0, '#33C3FF'],
        [0.5, '#31587A'],
        [1.0, '#1D3557']
    ],
    mapbox_style='white-bg',
    center={'lat': 12.5, 'lon': 121.7},
    zoom=4.5,
    opacity=1.0,
    range_color=(0, 4000000),
    title='Philippine Regions<br>Student Population Heatmap'
)

fig.update_layout(
    width=500, height=700,
    margin=dict(l=30, r=30, t=70, b=30),
    shapes=[dict(
        type='rect', xref='paper', yref='paper',
        x0=0, y0=0, x1=1, y1=1,
        line=dict(color='black', width=2)
    )],
    title=dict(
        x=0.5, xanchor='center',
        font=dict(size=16, family='Arial Black', color='black')
    ),
    coloraxis_colorbar=dict(
        title_font=dict(family='Arial Black', size=14, color='black'),
        tickfont=dict(family='Arial', size=12, color='black'),
        outlinecolor='black', outlinewidth=1,
        tickprefix=' ',
        ticks='outside', ticklen=5,
        len=1
    )
)

fig.show()
