import pandas as pd
import plotly.graph_objects as go
import textwrap
from Initialization.enrollment_data_loader import load_school_data

# Load the dataset
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")
df_school = data["df_school"]

# Rename columns to match expected format
df_school = df_school.rename(columns={
    "School_Subclassification": "School Subclassification",
    "Modified_COC": "Modified COC"
})

# Drop rows where key fields are missing
df_school = df_school.dropna(subset=["Sector", "School Subclassification", "Modified COC"])

# Group data by relevant fields
flows = df_school.groupby(["Sector", "School Subclassification", "Modified COC"]).size().reset_index(name='count')

# Format labels for Sankey nodes
def format_label(label):
    wrapped = "<br>".join(textwrap.wrap(label.title(), width=20))
    return f"<b>{wrapped}</b>"

labels_raw = pd.unique(flows[["Sector", "School Subclassification", "Modified COC"]].values.ravel()).tolist()
labels = [format_label(label) for label in labels_raw]
label_index = {label: i for i, label in enumerate(labels_raw)}

# Define colors per sector
sector_colors = {
    "Public": "rgba(255, 87, 51, 0.7)",
    "Private": "rgba(51, 195, 255, 0.7)",
    "SUCs/LUCs": "rgba(46, 204, 113, 0.7)",
    "PSO": "rgba(255, 181, 51, 0.7)",
    "Others": "rgba(200, 200, 200, 0.7)"
}

sources = []
targets = []
values = []
colors = []

# First layer: Sector → Subclassification
for _, row in flows.iterrows():
    source = label_index[row["Sector"]]
    target = label_index[row["School Subclassification"]]
    value = row["count"]
    color = sector_colors.get(row["Sector"], "rgba(128, 128, 128, 0.4)")
    
    sources.append(source)
    targets.append(target)
    values.append(value)
    colors.append(color)

# Second layer: Subclassification → Modified COC
for _, row in flows.iterrows():
    source = label_index[row["School Subclassification"]]
    target = label_index[row["Modified COC"]]
    value = row["count"]
    color = sector_colors.get(row["Sector"], "rgba(128, 128, 128, 0.4)")

    sources.append(source)
    targets.append(target)
    values.append(value)
    colors.append(color)

# Create Sankey Diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=20,
        line=dict(color="black", width=1),
        label=labels,
        color="rgba(200, 200, 200, 0.2)"
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=colors
    )
)])

fig.update_layout(
    title=dict(
        text="<b>School Population per Sector, Sub-Classification, and Modified COC</b>",
        x=0.5,
        xanchor='center',
        font_color='black'
    ),
    title_font_size=15,
    font_color='black',
    font_size=10,
    height=450,
    width=950,
    template='plotly_white'
)

fig.show()
