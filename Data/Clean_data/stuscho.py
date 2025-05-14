import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np
import plotly.graph_objects as go
import matplotlib.ticker as mtick
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.patches as patches
from matplotlib.sankey import Sankey
from matplotlib.ticker import FuncFormatter, MultipleLocator
from plotly.subplots import make_subplots
import textwrap
import json
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import matplotlib.transforms as transforms
import io
import base64
from matplotlib.patches import Polygon,  Circle
import os
import json
import matplotlib
import warnings
matplotlib.use('Agg')

warnings.filterwarnings("ignore", category=DeprecationWarning)
config_path = 'config.json'

def load_config():
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    with open(config_path, 'r') as f:
        return json.load(f)

# Global dataset cache
_dataset_cache = {}

def safe_load_parquet(path):
    if not path:
        return None

    # Use cached version if available
    if path in _dataset_cache:
        return _dataset_cache[path]

    parquet_path = path.replace('.xlsx', '.parquet')

    # Load from parquet if exists
    if os.path.exists(parquet_path):
        try:
            df = pd.read_parquet(parquet_path)
            _dataset_cache[path] = df
            return df
        except Exception as e:
            print(f"[safe_load_parquet] Failed to read parquet: {e}")

    # Fallback: load from Excel and convert to parquet
    if os.path.exists(path):
        try:
            df = pd.read_excel(path, engine='openpyxl')
            df.to_parquet(parquet_path, index=False)
            _dataset_cache[path] = df
            return df
        except Exception as e:
            print(f"[safe_load_parquet] Failed to load Excel: {e}")

    return None

def load_data(path=None, dataset_key=None):
    config = load_config()

    # Use default key if none provided
    if dataset_key is None:
        dataset_key = 'dataset_path'

    if path is None:
        path = config.get(dataset_key)

    return safe_load_parquet(path)

def load_school_data():
    return load_data(dataset_key='school_dataset_path')

def load_student_data():
    return load_data(dataset_key='student_dataset_path')

def load_and_cache_data():
    # Load and cache the required datasets
    school_data = load_school_data()
    student_data = load_student_data()
    
    # Cache them for future reference
    _dataset_cache['school_data'] = school_data
    _dataset_cache['student_data'] = student_data

    return school_data, student_data

def clear_cache(dataset_key=None):
    if dataset_key:
        _dataset_cache.pop(dataset_key, None)
    else:
        _dataset_cache.clear()

df_school = load_data()

def preprocess_data(df_school):
    region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                    'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                    'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

    grade_columns_male = ['Kindergarten_Male', 'G1_Male', 'G2_Male', 'G3_Male', 'G4_Male', 'G5_Male', 'G6_Male',
                        'Elem_NG_Male', 'G7_Male', 'G8_Male', 'G9_Male', 'G10_Male', 'JHS_NG_Male',
                        'G11_ABM_Male', 'G11_HUMSS_Male', 'G11_STEM_Male', 'G11_GAS_Male',
                        'G11_PBM_Male', 'G11_TVL_Male', 'G11_SPORTS_Male', 'G11_ARTS_Male',
                        'G12_ABM_Male', 'G12_HUMSS_Male', 'G12_STEM_Male', 'G12_GAS_Male',
                        'G12_PBM_Male', 'G12_TVL_Male', 'G12_SPORTS_Male', 'G12_ARTS_Male']

    grade_columns_female = ['Kindergarten_Female', 'G1_Female', 'G2_Female', 'G3_Female', 'G4_Female', 'G5_Female', 'G6_Female',
                        'Elem_NG_Female', 'G7_Female', 'G8_Female', 'G9_Female', 'G10_Female', 'JHS_NG_Female',
                        'G11_ABM_Female', 'G11_HUMSS_Female', 'G11_STEM_Female', 'G11_GAS_Female',
                        'G11_PBM_Female', 'G11_TVL_Female', 'G11_SPORTS_Female', 'G11_ARTS_Female',
                        'G12_ABM_Female', 'G12_HUMSS_Female', 'G12_STEM_Female', 'G12_GAS_Female',
                        'G12_PBM_Female', 'G12_TVL_Female', 'G12_SPORTS_Female', 'G12_ARTS_Female']

    grade_levels = {"Kindergarten": ["Kindergarten_Male", "Kindergarten_Female"], "Grade 1": ["G1_Male", "G1_Female"],"Grade 2": ["G2_Male", "G2_Female"],
                    "Grade 3": ["G3_Male", "G3_Female"], "Grade 4": ["G4_Male", "G4_Female"],
                    "Grade 5": ["G5_Male", "G5_Female"],"Grade 6": ["G6_Male", "G6_Female"],
                    "Elem NG": ["Elem_NG_Male", "Elem_NG_Female"],"Grade 7": ["G7_Male", "G7_Female"],
                    "Grade 8": ["G8_Male", "G8_Female"],"Grade 9": ["G9_Male", "G9_Female"],
                    "Grade 10": ["G10_Male", "G10_Female"],"JHS NG": ["JHS_NG_Male", "JHS_NG_Female"],
                    "Grade 11": [col for col in df_school.columns if "G11" in col],"Grade 12": [col for col in df_school.columns if "G12" in col]}

    elementary_male = ["Kindergarten_Male","G1_Male", "G2_Male", "G3_Male", "G4_Male", "G5_Male", "G6_Male", "Elem_NG_Male"]
    elementary_female = ["Kindergarten_Female","G1_Female", "G2_Female", "G3_Female", "G4_Female", "G5_Female", "G6_Female", "Elem_NG_Female"]

    junior_high_male = ["G7_Male", "G8_Male", "G9_Male", "G10_Male", "JHS_NG_Male"]
    junior_high_female = ["G7_Female", "G8_Female", "G9_Female", "G10_Female", "JHS_NG_Female"]

    senior_high_male = ["G11_ABM_Male", "G11_HUMSS_Male", "G11_STEM_Male", "G11_GAS_Male","G11_PBM_Male", "G11_TVL_Male", "G11_SPORTS_Male", "G11_ARTS_Male",
                        "G12_ABM_Male", "G12_HUMSS_Male", "G12_STEM_Male", "G12_GAS_Male","G12_PBM_Male", "G12_TVL_Male", "G12_SPORTS_Male", "G12_ARTS_Male"]
    senior_high_female = ["G11_ABM_Female", "G11_HUMSS_Female", "G11_STEM_Female", "G11_GAS_Female", "G11_PBM_Female", "G11_TVL_Female", "G11_SPORTS_Female", "G11_ARTS_Female",
                        "G12_ABM_Female", "G12_HUMSS_Female", "G12_STEM_Female", "G12_GAS_Female", "G12_PBM_Female", "G12_TVL_Female", "G12_SPORTS_Female", "G12_ARTS_Female"]

    shs_strands = {
        "ABM": ["G11_ABM_Male", "G11_ABM_Female", "G12_ABM_Male", "G12_ABM_Female"],
        "HUMSS": ["G11_HUMSS_Male", "G11_HUMSS_Female", "G12_HUMSS_Male", "G12_HUMSS_Female"],
        "STEM": ["G11_STEM_Male", "G11_STEM_Female", "G12_STEM_Male", "G12_STEM_Female"],
        "GAS": ["G11_GAS_Male", "G11_GAS_Female", "G12_GAS_Male", "G12_GAS_Female"],
        "PBM": ["G11_PBM_Male", "G11_PBM_Female", "G12_PBM_Male", "G12_PBM_Female"],
        "TVL": ["G11_TVL_Male", "G11_TVL_Female", "G12_TVL_Male", "G12_TVL_Female"],
        "SPORTS": ["G11_SPORTS_Male", "G11_SPORTS_Female", "G12_SPORTS_Male", "G12_SPORTS_Female"],
        "ARTS": ["G11_ARTS_Male", "G11_ARTS_Female", "G12_ARTS_Male", "G12_ARTS_Female"]}

    Sector = ["Public", "Private", "SUCsLUCs", "PSO"]

    sector_students = {
        "Public": ["Public"],
        "Private": ["Private"],
        "SUCsLUCs": ["SUCs/LUCs"],
        "PSO": ["PSO"]
    }

    sector_distribution = df_school.groupby("Sector").sum(numeric_only=True)

    sector_distribution["Elementary_Total"] = sector_distribution[elementary_male].sum(axis=1) + sector_distribution[elementary_female].sum(axis=1)
    sector_distribution["Junior_HS_Total"] = sector_distribution[junior_high_male].sum(axis=1) + sector_distribution[junior_high_female].sum(axis=1)
    sector_distribution["Senior_HS_Total"] = sector_distribution[senior_high_male].sum(axis=1) + sector_distribution[senior_high_female].sum(axis=1)

    sector_distribution["Total"] = sector_distribution[["Elementary_Total", "Junior_HS_Total", "Senior_HS_Total"]].sum(axis=1)

    sector_distribution_totals = sector_distribution["Total"]


    regions = df_school['Region'].dropna().unique()
    school_subclassification = df_school['School_Subclassification'].dropna().unique()
    school_type = df_school['School_Type'].dropna().unique()
    modified_coc = df_school['Modified_COC'].dropna().unique()

    return sector_distribution, sector_distribution_totals, regions, school_subclassification, school_type, modified_coc, sector_students, Sector, shs_strands, region_order, grade_columns_female, grade_columns_male, grade_levels, elementary_male, elementary_female, junior_high_female, junior_high_male, senior_high_female, senior_high_male

def generate_graph7(df_school_1):

    grade_levels = {"Kindergarten": ["Kindergarten_Male", "Kindergarten_Female"], "Grade 1": ["G1_Male", "G1_Female"],"Grade 2": ["G2_Male", "G2_Female"],
                    "Grade 3": ["G3_Male", "G3_Female"], "Grade 4": ["G4_Male", "G4_Female"],
                    "Grade 5": ["G5_Male", "G5_Female"],"Grade 6": ["G6_Male", "G6_Female"],
                    "Elem NG": ["Elem_NG_Male", "Elem_NG_Female"],"Grade 7": ["G7_Male", "G7_Female"],
                    "Grade 8": ["G8_Male", "G8_Female"],"Grade 9": ["G9_Male", "G9_Female"],
                    "Grade 10": ["G10_Male", "G10_Female"],"JHS NG": ["JHS_NG_Male", "JHS_NG_Female"],
                    "Grade 11": [col for col in df_school_1.columns if "G11" in col],"Grade 12": [col for col in df_school_1.columns if "G12" in col]}
    
    # Graph 7: Student Data Analytics - Column-Bar Chart (Student Population per Grade Level by Gender)
    grade_labels = []
    male_counts = []
    female_counts = []

    for grade, columns in grade_levels.items():
        male_counts.append(df_school_1[columns[0]].sum())
        female_counts.append(df_school_1[columns[1]].sum())
        grade_labels.append(grade)

    fig7 = go.Figure()

    fig7.add_trace(go.Bar(
        x=[label for label in grade_labels],
        y=male_counts,
        name='Male',
        marker_color='#33C3FF',
        hovertemplate='<b style="color:black; font-family: Arial Black;">%{x}</b><br><b style="color:black;">Gender:</b> Male<br><b style="color:black;">Students:</b> %{y:,}<extra></extra>'

    ))


    fig7.add_trace(go.Bar(
        x=[label for label in grade_labels],
        y=female_counts,
        name='Female',
        marker_color= '#FF746C',
        hovertemplate='<b  style="color:black; font-family: Arial Black;">%{x}</b><br><b style="color:black;">Gender:</b> Female<br><b style="color:black;">Students:</b> %{y:,}<extra></extra>'
    ))

    fig7.update_layout(
        title=dict(
            text='',
            x=0.5,
            xanchor='center',
            font=dict(
                family='Arial Black',
                size=20,
                color='black'
            )
        ), height=620,
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=2)
            )
        ],
        showlegend=True,
        legend=dict(
        orientation='h',  # Horizontal layout
        x=0.5,            # Centered horizontally
        y=1.1,           # Positioned above the graph area
        xanchor='center',
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='black',
        borderwidth=1,
        font=dict(size=11, color='black', family='Arial')
        ),
        xaxis_title='Grade Level<br>',
        yaxis_title='<br>Student Population',
        barmode='group',
        xaxis=dict(
            title='Grade Level<br>',
            title_standoff=10,
            tickangle=45,
            tickfont=dict(size=12, family='Arial Black')
        ),
        uniformtext=dict(
            minsize=10,
            mode='show'
        ),
        yaxis=dict(
            tickformat=',',
            dtick=100000,
            gridcolor='gray',
            ticklen=10,
            title_standoff=5,
            automargin=True,
            tickfont=dict(size=12, family='Arial Black'),
            tick0=0,
            ticksuffix="   "
        ),
        template='plotly_white',
        margin=dict(l=100, r=100, t=40, b=40),
        font=dict(family='Arial Black'),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )

    return fig7

def generate_graph8(df_school_1):
 # Graph 8: Student Data Analytics - Area Chart (Student Distribution per SHS Strand by Sector)
    shs_strands = {
        "ABM": ["G11_ABM_Male", "G11_ABM_Female", "G12_ABM_Male", "G12_ABM_Female"],
        "HUMSS": ["G11_HUMSS_Male", "G11_HUMSS_Female", "G12_HUMSS_Male", "G12_HUMSS_Female"],
        "STEM": ["G11_STEM_Male", "G11_STEM_Female", "G12_STEM_Male", "G12_STEM_Female"],
        "GAS": ["G11_GAS_Male", "G11_GAS_Female", "G12_GAS_Male", "G12_GAS_Female"],
        "PBM": ["G11_PBM_Male", "G11_PBM_Female", "G12_PBM_Male", "G12_PBM_Female"],
        "TVL": ["G11_TVL_Male", "G11_TVL_Female", "G12_TVL_Male", "G12_TVL_Female"],
        "SPORTS": ["G11_SPORTS_Male", "G11_SPORTS_Female", "G12_SPORTS_Male", "G12_SPORTS_Female"],
        "ARTS": ["G11_ARTS_Male", "G11_ARTS_Female", "G12_ARTS_Male", "G12_ARTS_Female"]}

    sector_distribution = df_school_1.groupby("Sector").sum(numeric_only=True)
    sector_values = {
        strand: sector_distribution[cols].sum(axis=1)
        for strand, cols in shs_strands.items()
    }
    strand_df = pd.DataFrame(sector_values)
    strand_df.loc["SUCs/LUCs & PSO"] = strand_df.loc["SUCsLUCs"] + strand_df.loc["PSO"]
    strand_df = strand_df.drop(index=["SUCsLUCs", "PSO"])

    sector_colors = {
        "Private": ('#33C3FF', "rgba(168, 218, 220, 0.4)"),
        "Public":  ("#FF746C", "rgba(255, 178, 162, 0.4)"),
        "SUCs/LUCs & PSO": ('#2ECC71', "rgba(138, 177, 125, 0.4)")
    }

    fig8 = go.Figure()

    for sector in ["Public", "Private", "SUCs/LUCs & PSO"]:
        line_color, fill_color = sector_colors.get(sector, ("gray", "rgba(128,128,128,0.2)"))
        fig8.add_trace(go.Scatter(
            x=strand_df.columns,
            y=strand_df.loc[sector],
            mode='lines+markers',
            name=sector,
            line=dict(color=line_color, width=5),
            marker=dict(size=12, color=line_color, line=dict(color='white', width=3)),
            fill='tozeroy',
            fillcolor=fill_color,
            hovertemplate= f'<b style="color:black; font-family: Arial Black; f">{sector}</b>' + '<br><b>Strand:</b> %{x}<br><b>Students:</b> %{y:,}<extra></extra>'
        ))

    fig8.update_layout(
        title=dict(
            text='',
            x=0.5,
            xanchor='center',
            font=dict(size=20, family='Arial Black', color='black')
        ),
        xaxis=dict(
            title='SHS Strand<br>',
            title_font=dict(size=16, family='Arial Black', color='black'),
            tickmode='array',
            tickvals=strand_df.columns,
            tickangle=45,
            showgrid=True,
            gridcolor='lightgray',
            range=[-0.1, 7.1],
            dtick=100000
        ),
        yaxis=dict(
            title='<br>Number of Students',
            title_font=dict(size=16, family='Arial Black', color='black'),
            showgrid=True,
            gridcolor='gray',
            rangemode='tozero',
            ticksuffix='   ',
            tickfont=dict(family='Arial Black', size=12),
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
        legend=dict(
            orientation="h",  # horizontal layout
            yanchor="bottom",
            y=1.03,  # position above the plot
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            borderwidth=1,
            title_font=dict(size=12, family='Arial Black'),
            font=dict(size=12, family="Arial")
        ),
        font=dict(family="Arial Black", size=12),
        plot_bgcolor='white',
        margin=dict(l=0,r=0),
        height=570,
        width=720,
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial"

        )
    )

    return fig8

def generate_graph9(df_school_1):

    elementary_male = ["Kindergarten_Male","G1_Male", "G2_Male", "G3_Male", "G4_Male", "G5_Male", "G6_Male", "Elem_NG_Male"]
    elementary_female = ["Kindergarten_Female","G1_Female", "G2_Female", "G3_Female", "G4_Female", "G5_Female", "G6_Female", "Elem_NG_Female"]

    junior_high_male = ["G7_Male", "G8_Male", "G9_Male", "G10_Male", "JHS_NG_Male"]
    junior_high_female = ["G7_Female", "G8_Female", "G9_Female", "G10_Female", "JHS_NG_Female"]

    senior_high_male = ["G11_ABM_Male", "G11_HUMSS_Male", "G11_STEM_Male", "G11_GAS_Male","G11_PBM_Male", "G11_TVL_Male", "G11_SPORTS_Male", "G11_ARTS_Male",
                        "G12_ABM_Male", "G12_HUMSS_Male", "G12_STEM_Male", "G12_GAS_Male","G12_PBM_Male", "G12_TVL_Male", "G12_SPORTS_Male", "G12_ARTS_Male"]
    senior_high_female = ["G11_ABM_Female", "G11_HUMSS_Female", "G11_STEM_Female", "G11_GAS_Female", "G11_PBM_Female", "G11_TVL_Female", "G11_SPORTS_Female", "G11_ARTS_Female",
                        "G12_ABM_Female", "G12_HUMSS_Female", "G12_STEM_Female", "G12_GAS_Female", "G12_PBM_Female", "G12_TVL_Female", "G12_SPORTS_Female", "G12_ARTS_Female"]


    inner_labels = ["Elementary", "Junior High", "Senior High"]
    inner_values = [
        df_school_1[elementary_male + elementary_female].sum().sum(),
        df_school_1[junior_high_male + junior_high_female].sum().sum(),
        df_school_1[senior_high_male + senior_high_female].sum().sum()
    ]

    outer_labels = ["Private", "Public", "Other Sectors"]
    sector_distribution = df_school_1.groupby("Sector").sum(numeric_only=True)
    sector_distribution["Total"] = (
        sector_distribution[elementary_male + elementary_female].sum(axis=1) +
        sector_distribution[junior_high_male + junior_high_female].sum(axis=1) +
        sector_distribution[senior_high_male + senior_high_female].sum(axis=1)
    )

    outer_values = [
        sector_distribution.loc["Private", "Total"],
        sector_distribution.loc["Public", "Total"],
        sector_distribution.loc[["SUCsLUCs", "PSO"], "Total"].sum()
    ]

    # Graph 9: Student Data Analytics - Donut Chart (Student Distribution by Grade Division and School Sector)
    total_students = sum(inner_values)
    outer_percentages = np.array(outer_values)
    outer_mid_angles = np.cumsum(outer_percentages) - outer_percentages / 2
    outer_mid_angles *= 360

    fig9 = go.Figure()
    colorss = ['#FF746C', '#33C3FF', '#2ECC71']


    fig9.add_trace(go.Pie(
        labels=inner_labels,
        values=inner_values,
        hole=0.55,
        textinfo="percent+label",
        textposition="inside",
        textfont=dict(family="Arial Black", size=10, color="black", weight="bold"),
        marker=dict(colors=['#33C3FF', "#FF746C", '#2ECC71'], line=dict(color='black', width=0.8)),
        hovertemplate='<b style="color: black; font-family: Arial Black;">%{label}</b><br><b style="color: black;">Students:</b> %{value:,}<extra></extra>',
        showlegend=False,
        domain=dict(x=[0, 1], y=[0.2, 0.9]),
        insidetextorientation="auto",
    ))

    fig9.add_trace(go.Pie(
        labels=outer_labels,
        values=outer_values,
        hole=0.9,
        textinfo="percent+label",
        textposition="outside",
        textfont=dict(family="Arial Black", size=11, color="black", weight="bold"),
        marker=dict(colors=['#33C3FF', "#FF746C", '#2ECC71'], line=dict(color='black', width=0.8)),
        hovertemplate="<b style='color: black; font-family: Arial Black;'>%{label}</b><br><b style='color: black;'>Total:</b> %{value:,}<extra></extra>",
        showlegend=False,
        domain=dict(x=[0, 1], y=[0.1, 1]),
        insidetextorientation="auto"
    ))

    fig9.add_annotation(
        text=f"Student Population<br>{total_students:,.0f}",
        y=0.55,
        font=dict(family="Arial Black", size=11, color="black", weight="bold"),
        showarrow=False,
        align="center"
    )

    fig9.update_layout(
    height=600,
    margin=dict(l=0,t=0,b=0,r=0),
    width=725,
    xaxis=dict(tickfont=dict(family="Arial Black")),
    yaxis=dict(tickfont=dict(family="Arial Black")),
    hoverlabel=dict(
        bgcolor="white",
        font_size=13,
        font_family="Arial"
    )
)

    return fig9

def generate_graph10(df_school_2):

    def format_label(label):
        wrapped = "<br>".join(textwrap.wrap(label.title(), width=20))
        return f"<b>{wrapped}</b>"

    flows = df_school_2.groupby(['Sector', 'School_Subclassification', 'Modified_COC']).size().reset_index(name='count')

    labels_raw = pd.unique(flows[['Sector', 'School_Subclassification', 'Modified_COC']].values.ravel()).tolist()
    labels = [format_label(label) for label in labels_raw]
    label_index = {label: i for i, label in enumerate(labels_raw)}

    sector_colors_10 = {
        "Public": "rgba(255, 87, 51, 0.7)",
        "Private": "rgba(51, 195, 255, 0.7)",
        "SUCs/LUCs": "rgba(46, 204, 113, 0.7)",
        "PSO": "rgba(255, 181, 51, 0.7)",
        "Others": "rgba(200, 200, 200, 0.7)"
    }

    sources, targets, values, colors, custom_hovertext = [], [], [], [], []
    node_totals = {i: 0 for i in range(len(labels_raw))}

    for _, row in flows.iterrows():
        source = label_index[row['Sector']]
        target = label_index[row['School_Subclassification']]
        value = row['count']
        color = sector_colors_10.get(row['Sector'], "rgba(128, 128, 128, 0.4)")

        sources.append(source)
        targets.append(target)
        values.append(value)
        colors.append(color)
        node_totals[source] += value
        node_totals[target] += value

        hover = (
            f"<b style='color: black; font-family: Arial Black;'>From:</b> {row['Sector']}<br>"
            f"<b style='color: black; font-family: Arial Black;'>To:</b> {row['School_Subclassification']}<br>"
            f"<b style='color: black; font-family: Arial Black;'>Students:</b> {value:,}"
        )
        custom_hovertext.append(hover)

    for _, row in flows.iterrows():
        source = label_index[row['School_Subclassification']]
        target = label_index[row['Modified_COC']]
        value = row['count']
        color = sector_colors_10.get(row['Sector'], "rgba(128, 128, 128, 0.4)")

        sources.append(source)
        targets.append(target)
        values.append(value)
        colors.append(color)
        node_totals[source] += value
        node_totals[target] += value

        hover = (
            f"<b>From:</b> {row['School_Subclassification']}<br>"
            f"<b>To:</b> {row['Modified_COC']}<br>"
            f"<b>Students:</b> {value:,}"
        )
        custom_hovertext.append(hover)

    node_hovertext = [f"<b>{label_raw}</b><br><b>Total Students:</b> {node_totals[i]:,}" for i, label_raw in enumerate(labels_raw)]

    fig10 = go.Figure(data=[go.Sankey(
        node=dict(
            pad=25,
            thickness=20,
            line=dict(color="black", width=1),
            label=labels,
            color="rgba(200, 200, 200, 0.2)",
            customdata=node_hovertext,
            hovertemplate="%{customdata}<extra></extra>"
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=colors,
            customdata=custom_hovertext,
            hovertemplate="%{customdata}<extra></extra>"
        )
    )])

    fig10.update_layout(
        font_color='black',
        font_size=10,
        height=550,
        width=765,
        margin=dict(l=0, r=0),
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Arial")
    )
    return fig10

def generate_graph11(df_school_2):
    df_grouped = df_school_2.groupby(['School_Type', 'Sector']).size().reset_index(name='count')
    pivot_df = df_grouped.pivot(index='School_Type', columns='Sector', values='count').fillna(0)

    # Apply label replacements
    label_replacements = {
        'Annex or Extension school(s)': 'Annex or<br>Extension School(s)',
        'Mobile School(s)/Center(s)': 'Mobile School(s)<br>Center(s)',
        'School with no Annexes': 'School with<br>no Annexes'
    }
    pivot_df.index = pivot_df.index.to_series().replace(label_replacements)

    sector_colors_11 = {
        'Public': '#FF746C',
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
            line=dict(width=5, color=sector_colors_11[sector]),
            marker=dict(size=12, color=sector_colors_11[sector], line=dict(color='white', width=3)),
            hovertemplate=(
                "<b style='color: black; font-family: Arial Black;'>School Type:</b> %{x}<br>" +
                f"<b style='color: black; font-family: Arial Black;'>Sector:</b> {sector.replace('SUCsLUCs', 'SUCs/LUCs')}<br>" +
                "<b style='color: black; font-family: Arial Black;'>Count:</b> %{y:,}<extra></extra>"
            )
        ) for sector in pivot_df.columns
    ]

    school_counts = df_school_2.groupby('School_Type').size().reset_index(name='count')
    school_counts['School_Type'] = school_counts['School_Type'].replace(label_replacements)

    bar_trace = go.Bar(
        x=school_counts['School_Type'],
        y=school_counts['count'],
        name='Total Schools',
        marker=dict(color='#FFB533'),
        text=[f'{count:,}' for count in school_counts['count']],
        textposition='outside',
        textfont=dict(size=12, family='Arial Black', color='black'),
        hovertemplate="<b>School Type:</b> %{x}<br><b>Total Schools:</b> %{y:,}<extra></extra>"
    )

    fig11 = go.Figure(data=line_traces + [bar_trace])

    fig11.update_layout(
        title="",
        title_x=0.5,
        xaxis=dict(title=dict(text='<b>School Type</b>', font=dict(size=12, color='black', family='Arial Black')), tickangle=45, tickfont=dict(size=12, color='black', family='Arial Black')),
        yaxis=dict(title=dict(text='<b>Number of Schools</b>', font=dict(size=12, color='black', family='Arial Black')), tickformat=',', showgrid=True, gridcolor='gray', ticksuffix=' ', tickfont=dict(size=12, color='black', family='Arial Black')),
        height=580,
        width=700,
        showlegend=True,
        legend=dict(
        orientation='h',
        x=0.5,
        y=1.15,
        xanchor='center',
        yanchor='bottom',
        title=dict(font=dict(size=14, family='Arial Black')),
        font=dict(size=12, color='black', family='Arial Black'),
        borderwidth=1,
        bordercolor='black',
        bgcolor='rgba(255,255,255,0.8)'
        ),
        barmode='group',
        margin=dict(l=0, r=0, t=100, b=100),
        template='plotly_white',
        shapes=[dict(type="rect", xref="paper", yref="paper", x0=0.01, y0=0, x1=1, y1=1.06, line=dict(color="black", width=2))],
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Arial")
    )
    return fig11

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
