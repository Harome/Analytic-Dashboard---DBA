import pandas as pd
import plotly.graph_objects as go
import numpy as np
from Initialization.enrollment_data_loader import load_school_data

# Load data using your custom loader
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")

# Extract the school-level DataFrame
df_school = data["df_school"]
shs_strands = data["shs_strands"]

# Group data by sector and sum values
sector_distribution = df_school.groupby("Sector").sum(numeric_only=True)

# Aggregate strand values per sector
sector_values = {
    strand: sector_distribution[cols].sum(axis=1)
    for strand, cols in shs_strands.items()
}
strand_df = pd.DataFrame(sector_values)

# Combine SUCs/LUCs and PSO into a new category
strand_df.loc["SUCs/LUCs & PSO"] = strand_df.loc["SUCsLUCs"] + strand_df.loc["PSO"]
strand_df = strand_df.drop(index=["SUCsLUCs", "PSO"])

# Set correct labels for the inner pie chart (these should correspond to grade divisions)
inner_labels = ['Junior High', 'Senior High', 'Elementary']  # Use the correct grade divisions
inner_values = strand_df.sum(axis=0).values  # Sum of values for each grade division

# Set outer labels for the sectors
outer_labels = strand_df.index.tolist()
outer_values = strand_df.sum(axis=1).values

# Total student population
total_students = sum(inner_values)

# Mid angles for outer pie chart labels
outer_percentages = np.array(outer_values) / total_students
outer_mid_angles = np.cumsum(outer_percentages) - outer_percentages / 2
outer_mid_angles *= 360

# Create the Pie chart figure
fig = go.Figure()

# Inner Pie Chart (represents the grade divisions)
fig.add_trace(go.Pie(
    labels=inner_labels,
    values=inner_values,
    hole=0.6,
    textinfo="percent+label",
    textposition="inside",
    textfont=dict(family="Arial Black", size=12, color="black", weight="bold"),
    marker=dict(colors=['#33C3FF', "#FF5733", '#2ECC71'], line=dict(color='black', width=0.8)),
    hoverinfo="label+percent",
    showlegend=False,
    domain=dict(x=[0, 1], y=[0.2, 0.9]),
    insidetextorientation="horizontal"
))

# Outer Pie Chart (represents the sectors)
fig.add_trace(go.Pie(
    labels=outer_labels,
    values=outer_values,
    hole=0.9,
    textinfo="percent+label",
    textposition="outside",
    textfont=dict(family="Arial Black", size=12, color="black", weight="bold"),
    marker=dict(colors=['#33C3FF', "#FF5733", '#2ECC71'], line=dict(color='black', width=0.8)),
    hoverinfo="label+percent",
    showlegend=False,
    domain=dict(x=[0, 1], y=[0.1, 1]),
    insidetextorientation="horizontal"
))

# Annotation for total student population
fig.add_annotation(
    text=f"Student Population<br>{total_students:,.0f}",
    y=0.55,
    font=dict(family="Arial Black", size=20, color="black", weight="bold"),
    showarrow=False,
    align="center"
)

# Update layout for styling
fig.update_layout(
    title="Student Distribution by Grade Division and School Sector",
    title_font_size=20,
    title_font_weight="bold",
    title_x=0.5,
    title_y=0.95,
    height=800,
    width=800,
    xaxis=dict(tickfont=dict(family="Arial Black")),
    yaxis=dict(tickfont=dict(family="Arial Black"))
)

fig.show()
