import pandas as pd
import plotly.graph_objects as go

# Load the data from your 'enrollment_data_loader' file
file_path = '/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx'
df_school = pd.read_excel(file_path)

# Now proceed with your original code
df_grouped = df_school.groupby(['School_Type', 'Sector']).size().reset_index(name='count')
pivot_df = df_grouped.pivot(index='School_Type', columns='Sector', values='count').fillna(0)

sector_colors = {
    'Public': '#FF5733',
    'SUCsLUCs': '#2ECC71',
    'Private': '#33C3FF',
    'PSO': '#1D3557'
}

line_traces = [
    go.Scatter(
        x=pivot_df.index,
        y=pivot_df[sector],
        mode='lines+markers',
        name=sector.replace('SUCsLUCs', 'SUCs/LUCs'),
        line=dict(width=5, color=sector_colors[sector]),
        marker=dict(size=12, color=sector_colors[sector], line=dict(color='white', width=3))
    ) for sector in pivot_df.columns
]

school_counts = df_school.groupby('School_Type').size().reset_index(name='count')
bar_trace = go.Bar(
    x=school_counts['School_Type'],
    y=school_counts['count'],
    name='Total Schools',
    marker=dict(color='#FFB533'),
    text=[f'{count:,}' for count in school_counts['count']],
    textposition='outside',
    textfont=dict(size=12, family='Arial Black', color='black')
)

fig = go.Figure(data=line_traces + [bar_trace])

fig.update_layout(
    title="<b>School Count by School Type and Sector</b>",
    title_x=0.5,
    xaxis=dict(
        title='<b>School Type</b>',
        tickangle=45,
        tickfont=dict(size=12, )
    ),
    yaxis=dict(
        title='<b>Number of Schools</b>',
        tickformat=',',
        showgrid=True,
        gridcolor='gray',
        ticksuffix=' ',
        tickfont=dict(size=12, color='black')
    ),
    height=600,
    width=900,
    showlegend=True,
    legend=dict(
        x=1.05,
        y=1,
        orientation='v',
        title=dict(text='School Categories', font=dict(size=14, family='Arial Black')),
        font=dict(size=12, color='black'),
        borderwidth=1,
        bordercolor='black',
        bgcolor='rgba(255,255,255,0.8)'
    ),
    barmode='group',
    margin=dict(l=100, r=150, t=100, b=100),
    template='plotly_white',
    shapes=[dict(
        type="rect", xref="paper", yref="paper",
        x0=0.01, y0=0, x1=1, y1=1.06,
        line=dict(color="black", width=2),
    )]
)

fig.show()
