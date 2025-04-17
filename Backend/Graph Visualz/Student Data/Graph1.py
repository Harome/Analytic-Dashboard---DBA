
import pandas as pd
import plotly.graph_objects as go
from Initialization.enrollment_data_loader import load_school_data

# Load data
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")

# Extract necessary parts
df_school = data["df_school"]
grade_columns_male = data["grade_columns_male"]
grade_columns_female = data["grade_columns_female"]

# Compute national total by grade
grade_labels = []
male_counts = []
female_counts = []

for male_col, female_col in zip(grade_columns_male, grade_columns_female):
    grade_name = male_col.replace("_Male", "")  # clean label
    male_total = df_school[male_col].sum()
    female_total = df_school[female_col].sum()
    
    grade_labels.append(grade_name)
    male_counts.append(male_total)
    female_counts.append(female_total)

# Setup bar chart
fig = go.Figure()

text_position_males = []
text_position_females = []
color_females = []
color_males = []

for count in male_counts:
    if count >= 200000:
        text_position_males.append("inside")
        color_males.append("white")
    else:
        text_position_males.append("outside")
        color_males.append('#33C3FF')

for count in female_counts:
    if count >= 200000:
        text_position_females.append("inside")
        color_females.append("white")
    else:
        text_position_females.append("outside")
        color_females.append("#FF5733")

fig.add_trace(go.Bar(
    x=grade_labels,
    y=male_counts,
    name='Male',
    marker_color='#33C3FF',
    text=[f'{count:,}' for count in male_counts],
    textposition=text_position_males,
    textangle=90,
    textfont=dict(size=10, family='Poppins, sans-serif', color=color_males)
))

fig.add_trace(go.Bar(
    x=grade_labels,
    y=female_counts,
    name='Female',
    marker_color='#FF5733',
    text=[f'{count:,}' for count in female_counts],
    textposition=text_position_females,
    textangle=90,
    textfont=dict(size=10, family='Poppins, sans-serif', color=color_females)
))

fig.update_layout(
    title=dict(
        text="Student Population per Grade Level by Gender",
        x=0.5,
        xanchor='center',
        font=dict(family='Poppins, sans-serif', size=18, color='black')
    ),
    xaxis_title='Grade Level',
    yaxis_title='Student Population',
    barmode='group',
    xaxis=dict(
        tickangle=45,
        tickfont=dict(size=12, family='Poppins, sans-serif')
    ),
    yaxis=dict(
        tickformat=',',
        gridcolor='lightgray',
        tickfont=dict(size=12, family='Poppins, sans-serif'),
        title_standoff=5
    ),
    legend=dict(
        title='Gender',
        font=dict(size=11, family='Poppins, sans-serif'),
        title_font=dict(size=12, family='Poppins, sans-serif')
    ),
    margin=dict(l=60, r=60, t=80, b=100),
    template='plotly_white'
)

fig.show()