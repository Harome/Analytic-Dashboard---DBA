import pandas as pd
import plotly.graph_objects as go
from Initialization.enrollment_data_loader import load_school_data

# Load data using your custom loader
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")

# Extract necessary parts
df_school = data["df_school"]
grade_columns_male = data["grade_columns_male"]
grade_columns_female = data["grade_columns_female"]

# Define grade level groupings
elementary_male = grade_columns_male[1:7] + ["Elem_NG_Male"]
elementary_female = [col.replace("Male", "Female") for col in elementary_male]

junior_high_male = grade_columns_male[8:13]
junior_high_female = [col.replace("Male", "Female") for col in junior_high_male]

senior_high_male = grade_columns_male[13:]
senior_high_female = [col.replace("Male", "Female") for col in senior_high_male]

# Recalculate totals for each division per region
region_population = df_school.groupby("Region").sum(numeric_only=True)

region_population["Elementary_Total"] = region_population[elementary_male].sum(axis=1) + region_population[elementary_female].sum(axis=1)
region_population["Junior_HS_Total"] = region_population[junior_high_male].sum(axis=1) + region_population[junior_high_female].sum(axis=1)
region_population["Senior_HS_Total"] = region_population[senior_high_male].sum(axis=1) + region_population[senior_high_female].sum(axis=1)

# Get the national total for each level
region_population_totals = region_population[["Elementary_Total", "Junior_HS_Total", "Senior_HS_Total"]].sum()

# Pie chart data
labels = ["Elementary School", "Junior High School", "Senior High School"]
colors = ['#FF5733', '#33C3FF', '#2ECC71']  # red, blue, green

fig = go.Figure(data=[
    go.Pie(
        labels=labels,
        values=region_population_totals,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        hole=0.45,
        textinfo='percent',
        textfont=dict(size=13, family='Poppins, sans-serif', color='black'),
        insidetextfont=dict(size=13, color='black'),
        pull=[0.03, 0.03, 0.03],
        hovertemplate='%{label}<br>Students: %{value:,}<br>Percentage: %{percent}<extra></extra>'
    )
])

fig.update_layout(
    title_text="Student Population Distribution by Grade Division",
    title_font=dict(size=18, family='Poppins, sans-serif', color='black'),
    title_x=0.5,
    paper_bgcolor='rgba(255,255,255,0.7)',
    plot_bgcolor='rgba(255,255,255,0.7)',
    legend=dict(
        title="Grade Division",
        font=dict(size=11, family='Poppins, sans-serif'),
        title_font=dict(size=12, family='Poppins, sans-serif', color='#1b8e3e')
    )
)

fig.show()
