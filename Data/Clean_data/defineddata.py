import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

path = r"D:\zDonludoz\Git\Analytic-Dashboard---DBA\Data\Raw_data\ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx"
df = pd.read_excel(path)
df.head()

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

grade_levels = {
    "Kindergarten": ["Kindergarten_Male", "Kindergarten_Female"],
    "Grade 1": ["G1_Male", "G1_Female"],"Grade 2": ["G2_Male", "G2_Female"],
    "Grade 3": ["G3_Male", "G3_Female"], "Grade 4": ["G4_Male", "G4_Female"],
    "Grade 5": ["G5_Male", "G5_Female"],"Grade 6": ["G6_Male", "G6_Female"],
    "Elem NG": ["Elem_NG_Male", "Elem_NG_Female"],"Grade 7": ["G7_Male", "G7_Female"],
    "Grade 8": ["G8_Male", "G8_Female"],"Grade 9": ["G9_Male", "G9_Female"],
    "Grade 10": ["G10_Male", "G10_Female"],"JHS NG": ["JHS_NG_Male", "JHS_NG_Female"],
    "Grade 11": [col for col in df.columns if "G11" in col],"Grade 12": [col for col in df.columns if "G12" in col],}

elementary_male = ["G1_Male", "G2_Male", "G3_Male", "G4_Male", "G5_Male", "G6_Male", "Elem_NG_Male"]
elementary_female = ["G1_Female", "G2_Female", "G3_Female", "G4_Female", "G5_Female", "G6_Female", "Elem_NG_Female"]

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

# Graph 1 Data
total_male = df[grade_columns_male].sum().sum()
total_female = df[grade_columns_female].sum().sum()
total_students = total_male + total_female

df_total_enrollees = pd.DataFrame({
    'Gender': ['Male', 'Female'],
    'Total Enrollees': [total_male, total_female]
})

# Graph 2 Data
if 'Region' in df.columns:
    df['Region'] = pd.Categorical(df['Region'], categories=region_order, ordered=True)
    df = df.sort_values('Region')

    region_grade_totals = df.groupby('Region', observed=False).sum()[sum(grade_levels.values(), [])]
    region_grade_totals = region_grade_totals.T.groupby(
        lambda x: next((k for k, v in grade_levels.items() if x in v), None)
    ).sum().T

    fig2 = px.bar(
        region_grade_totals,
        x=region_grade_totals.index,
        y=region_grade_totals.columns,
        title="Distribution of Students per Grade Level Across Regions",
        labels={"value": "Total Students", "Region": "Region"},
        barmode="stack"
    )
    fig2.update_layout(xaxis_tickangle=-45)

# Graph 3 Data: Student Population by Year Level (All Regions)
year_level_totals = {level: df[columns].sum().sum() for level, columns in grade_levels.items()}

labels3 = list(year_level_totals.keys())
sizes3 = list(year_level_totals.values())
colors3 = px.colors.qualitative.Plotly

fig3 = go.Figure(go.Bar(
    x=sizes3,
    y=labels3,
    orientation='h',
    marker=dict(color=colors3),
    text=[f"{v:,}" for v in sizes3],
    textposition='outside'
))

fig3.update_layout(
    title="Student Population Distribution by Year Level (All Regions)",
    xaxis_title="Total Students",
    yaxis_title="Year Level",
    yaxis=dict(autorange="reversed")
)

# Graph 4 Data: Student Population per Grade Division by Region
region_population = df.groupby("Region").sum(numeric_only=True)
region_population["Elementary_Total"] = region_population[elementary_male].sum(axis=1) + region_population[elementary_female].sum(axis=1)
region_population["Junior_HS_Total"] = region_population[junior_high_male].sum(axis=1) + region_population[junior_high_female].sum(axis=1)
region_population["Senior_HS_Total"] = region_population[senior_high_male].sum(axis=1) + region_population[senior_high_female].sum(axis=1)

region_population_totals = region_population[["Elementary_Total", "Junior_HS_Total", "Senior_HS_Total"]].reset_index()

fig4 = px.bar(
    region_population_totals,
    y="Region",
    x=["Elementary_Total", "Junior_HS_Total", "Senior_HS_Total"],
    orientation="h",
    barmode="stack",
    title="Student Population per Grade Division by Region",
    labels={"value": "Total Students", "Region": "Region"}
)

fig4.update_layout(
    legend_title="Education Level",
    xaxis=dict(tickformat=",d")
)

