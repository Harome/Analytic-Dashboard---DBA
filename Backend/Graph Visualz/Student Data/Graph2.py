import pandas as pd
import plotly.graph_objects as go
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

# Define color themes for each sector
sector_colors = {
    "Private": ('#33C3FF', "rgba(168, 218, 220, 0.4)"),
    "Public":  ("#FF5733", "rgba(255, 178, 162, 0.4)"),
    "SUCs/LUCs & PSO": ('#2ECC71', "rgba(138, 177, 125, 0.4)")
}

# Create the area chart
fig = go.Figure()

for sector in ["Public", "Private", "SUCs/LUCs & PSO"]:
    line_color, fill_color = sector_colors.get(sector, ("gray", "rgba(128,128,128,0.2)"))
    fig.add_trace(go.Scatter(
        x=strand_df.columns,
        y=strand_df.loc[sector],
        mode='lines+markers',
        name=sector,
        line=dict(color=line_color, width=5),
        marker=dict(size=12, color=line_color, line=dict(color='white', width=3)),
        fill='tozeroy',
        fillcolor=fill_color,
        hoverinfo='x+y+name'
    ))

# Update layout styling
fig.update_layout(
    title=dict(
        text='Student Distribution per SHS Strand by Sector',
        x=0.5,
        xanchor='center',
        font=dict(size=20, family='Poppins, sans-serif', color='black')
    ),
    xaxis=dict(
        title='SHS Strand',
        title_font=dict(size=16, family='Poppins, sans-serif', color='black'),
        tickmode='array',
        tickvals=strand_df.columns,
        tickangle=45,
        showgrid=True,
        gridcolor='lightgray',
        range=[-0.1, len(strand_df.columns) - 0.9]
    ),
    yaxis=dict(
        title='Number of Students',
        title_font=dict(size=16, family='Poppins, sans-serif', color='black'),
        showgrid=True,
        gridcolor='gray',
        rangemode='tozero',
        ticksuffix='   ',
        tickfont=dict(family='Poppins, sans-serif', size=12),
        range=[-35000, strand_df.values.max() + 100000]
    ),
    shapes=[
        dict(
            type="rect",
            xref="paper", yref="paper",
            x0=0, y0=0, x1=1, y1=1,
            line=dict(color="black", width=2)
        )
    ],
    legend_title="School Sector",
    legend=dict(
        x=0.99,
        y=0.99,
        xanchor="right",
        yanchor="top",
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="black",
        borderwidth=1,
        title_font=dict(size=12, family='Poppins, sans-serif'),
        font=dict(size=11, family='Poppins, sans-serif'),
    ),
    font=dict(family="Poppins, sans-serif", size=12),
    plot_bgcolor='white',
    height=500,
    width=900,
    margin=dict(l=30, r=30, t=60, b=80)
)

fig.show()
