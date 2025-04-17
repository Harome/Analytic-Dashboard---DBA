import pandas as pd
import plotly.graph_objects as go
from Initialization.enrollment_data_loader import load_school_data

# Load the school-level enrollment data
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")

# Extract necessary variables
df_school = data["df_school"]
region_order = data["region_order"]
regions = df_school["Region"].unique()

# Extract categories from data (includes school types, subclassifications, etc.)
categories = data["categories"]

# Retrieve school types, subclassifications, and modified COC from categories
school_type = categories.get("school_types", [])
school_subclassification = categories.get("subclassifications", [])
modified_coc = categories.get("modified_coc", [])

# Sample values
total_schools = df_school.shape[0]
sorted_regions = [r for r in region_order if r in regions]

# Convert to vertical text for hover tooltips
regions_text = "<br>".join(sorted_regions)
subclassifications_text = "<br>".join(sorted(school_subclassification))
types_text = "<br>".join(sorted(school_type))
modified_coc_text = "<br>".join(sorted(modified_coc))

# Create the figure
fig = go.Figure()

# Indicator for total number of schools
fig.add_trace(go.Indicator(
    mode="number",
    value=total_schools,
    title={
        "text": "<br><b><br><br><b>🏫<br><b>Total Number of Schools<br><b><span style='font-size:16px'>(under the Philippine Education System)</span></b>",
        "font": {"size": 24, "family": "Poppins, sans-serif"}
    },
    number={
        "valueformat": ",",
        "font": {"size": 60, "color": "red", "family": "Poppins, sans-serif"}
    },
    domain={"x": [0.05, 0.95], "y": [0.42, 0.9]}
))

# Define labels and hovers
labels = ["Regions |", "Subclassifications |", "Types |", "Modified COC"]
hover_texts = [regions_text, subclassifications_text, types_text, modified_coc_text]
x_positions = [0.10, 0.40, 0.60, 0.88]  # relative positions inside the box

# Add annotations instead of scatter
for x, label, hover in zip(x_positions, labels, hover_texts):
    fig.add_annotation(
        x=x, y=0.28, xref="paper", yref="paper",
        text=f"<b>{label}</b>",
        font=dict(family="Poppins, sans-serif", size=14, color="#333"),
        showarrow=False,
        hovertext=hover,
        hoverlabel=dict(font_size=12),
        align="center"
    )

# Layout and box styling
fig.update_layout(
    height=430,
    width=500,
    margin=dict(t=40, b=40, l=30, r=30),
    paper_bgcolor="rgba(255, 255, 255, 1)",
    plot_bgcolor="rgba(0, 0, 0, 0)",
    template="plotly_white",
    font=dict(family="Poppins, sans-serif"),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    shapes=[dict(
        type="rect",
        xref="paper", yref="paper",
        x0=0.03, y0=0.25, x1=0.97, y1=0.96,
        fillcolor="rgba(240, 248, 255, 1)",
        line=dict(color="rgba(30, 144, 255, 0.8)", width=2),
        layer="below"
    )]
)

fig.show()
