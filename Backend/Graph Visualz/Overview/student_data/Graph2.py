import pandas as pd
import plotly.graph_objects as go
from Initialization.enrollment_data_loader import load_school_data

# Load data from the enrollment_data_loader
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")

# Extract necessary variables from the loaded data
df_school = data["df_school"]
region_order = data["region_order"]
grade_columns_male = data["grade_columns_male"]
grade_columns_female = data["grade_columns_female"]

# Define grade_levels dynamically
grade_levels = {
    "Elementary": grade_columns_male[1:7] + ["Elem_NG_Male"] + [col.replace("Male", "Female") for col in grade_columns_male[1:7]] + ["Elem_NG_Female"],
    "Junior High": grade_columns_male[8:13] + [col.replace("Male", "Female") for col in grade_columns_male[8:13]],
    "Senior High": grade_columns_male[13:] + [col.replace("Male", "Female") for col in grade_columns_male[13:]]
}

# Check if 'Region' column exists and process the data
if 'Region' in df_school.columns:
    # Sort by region based on the custom region order
    df_school['Region'] = pd.Categorical(df_school['Region'], categories=region_order, ordered=True)
    df = df_school.sort_values('Region')

    # Group by region and calculate totals for each grade level
    region_grade_totals = df.groupby('Region', observed=False).sum()[sum(grade_levels.values(), [])]
    
    # Aggregate totals by grade level
    region_grade_totals = region_grade_totals.T.groupby(
        lambda x: next((k for k, v in grade_levels.items() if x in v), None)
    ).sum().T

    # Sum the totals for each region
    region_totals = region_grade_totals.sum(axis=1)

    # Define pastel color palette for regions
    pastel_colors = ['#33C3FF', '#FF5733']
    theme_colors = [pastel_colors[i % 2] for i in range(len(region_totals))]

    # Create the bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=region_totals.index,
            y=region_totals.values,
            marker_color=theme_colors,
            hovertemplate='%{x}<br>Total Students: %{y:,}<extra></extra>'
        )
    ])

    # Update layout and appearance of the figure
    fig.update_layout(
    title="Distribution of Students Across Philippine Regions",
    title_x=0.5,
    plot_bgcolor='rgba(255,255,255,0.7)',
    paper_bgcolor='rgba(255,255,255,0.7)',
    font=dict(color='#1b8e3e', size=13, family="Poppins, sans-serif"),
    xaxis=dict(
        title="Regions",
        tickangle=45,
        tickfont=dict(size=11, color='#333', family='Poppins, sans-serif'),
    ),
    yaxis=dict(
        title="Total Students",
        tickformat=',~s'
    )
)

    # Show the plot
    fig.show()
