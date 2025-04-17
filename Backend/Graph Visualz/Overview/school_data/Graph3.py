import plotly.graph_objects as go
from plotly.subplots import make_subplots
from Initialization.enrollment_data_loader import load_school_data

# Load the school-level enrollment data
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")

# Extract the school data
df_school = data["df_school"]

# Normalize the 'Sector' column by replacing 'SUCsLUCs' with 'SUCs/LUCs'
df_school['Sector'] = df_school['Sector'].str.strip().replace('SUCsLUCs', 'SUCs/LUCs')

# Verify the unique values in 'Sector'
print(df_school['Sector'].unique())

# Define sector labels and their colors
sector_labels = ['Public', 'Private', 'SUCs/LUCs', 'PSO']
colors = ['#FF5733', '#33C3FF', '#2ECC71', '#FFB533']
border_colors = ['#FF0000', '#0000FF','#0e6936', '#b5b50d']

# Calculate school counts per sector
school_counts = [
    df_school[df_school['Sector'] == 'Public'].shape[0],
    df_school[df_school['Sector'] == 'Private'].shape[0],
    df_school[df_school['Sector'] == 'SUCs/LUCs'].shape[0],
    df_school[df_school['Sector'] == 'PSO'].shape[0]
]

# Create the subplot grid
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{'type': 'polar'}, {'type': 'polar'}],
           [{'type': 'polar'}, {'type': 'polar'}]],
    subplot_titles=[f"<b>{label}</b>" for label in sector_labels],
    vertical_spacing=0.1, horizontal_spacing=0.1
)

# Define radial ranges for each sector
ranges = {'Public': [0, 50000], 'Private': [0, 20000],
          'SUCs/LUCs': [0, 250], 'PSO': [0, 50]}

# Define a row-column map for positioning subplots
row_col_map = [(1, 1), (1, 2), (2, 1), (2, 2)]

# Add data traces to the plot
for i, (label, count, color, border_color) in enumerate(zip(sector_labels, school_counts, colors, border_colors)):
    row, col = row_col_map[i]
    fig.add_trace(go.Barpolar(
        r=[count], theta=[label],
        marker=dict(color=color, line=dict(color=border_color, width=4)),
        name=label, opacity=0.5, text=[f"{label} = {count:,}"],
        hoverinfo="text"), row=row, col=col)

    # Adjust radial range for each subplot based on the sector
    fig.layout[f'polar{(row - 1) * 2 + col}'].radialaxis.range = ranges[label]
    fig.layout[f'polar{(row - 1) * 2 + col}'].radialaxis.showticklabels = False
    fig.layout[f'polar{(row - 1) * 2 + col}'].angularaxis.showticklabels = False
    fig.layout[f'polar{(row - 1) * 2 + col}'].angularaxis.tickfont = dict(size=12)

# Update layout for the entire figure
fig.update_layout(
    height=600, width=700, title='<b>School Distribution per Sector</b>',
    title_font_size=20, title_font=dict(family='Poppins, sans-serif', size=20, color='black'),
    title_x=0.5, font=dict(family='Poppins, sans-serif', size=13, color='black'),
    showlegend=False, paper_bgcolor='white', margin=dict(t=80, b=60, l=50, r=50)
)

# Show the plot
fig.show()
