import plotly.graph_objects as go
from Initialization.enrollment_data_loader import load_school_data

# Load the school-level enrollment data
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")

# Extract the school data
df_school = data["df_school"]
region_order = data["region_order"]

# Calculate the region counts
region_counts = df_school['Region'].value_counts().reindex(region_order, fill_value=0)
labels = region_counts.index.tolist()
sizes = region_counts.values.tolist()

# Create the figure
fig = go.Figure()

# Add the scatter plot for the region counts
fig.add_trace(go.Scatter(
    x=labels, y=sizes, mode='lines+markers',
    line=dict(color='blue', width=3), fill='tozeroy',
    fillcolor='rgba(0, 123, 255, 0.3)',
    marker=dict(symbol='diamond', size=10, color='red',
                line=dict(color='green', width=2)), showlegend=False))

# Update layout settings
fig.update_layout(
    title=dict(text="<b>Distribution of Schools per Region</b>", x=0.5,
               font=dict(size=20, family="Poppins, sans-serif", weight='bold')),
    xaxis=dict(
        title="<b>Regions</b>", tickangle=45, tickfont=dict(size=12, family="Poppins, sans-serif", weight='bold'),
        showgrid=True, gridcolor='lightgray', ticks="outside", ticklen=8, range=[-0.5, len(labels) - 0.5]),
    yaxis=dict(
        title="<b>Number of Schools</b>", range=[-1000, 7500], showgrid=True, gridcolor='lightgray',
        tickfont=dict(size=12, family="Poppins, sans-serif", weight='bold'), ticks="outside", ticklen=8, autorange=False),
    plot_bgcolor='white',
    margin=dict(t=80, b=100, l=80, r=80), height=500, width=800,
    font=dict(family="Poppins, sans-serif", weight='bold'),
    shapes=[dict(
        type='rect', x0=0, x1=1, y0=0, y1=1, xref='paper', yref='paper',
        line=dict(color='black', width=2), layer='above')])

# Show the plot
fig.show()
