import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np

path = r"D:\zDonludoz\Git\Analytic-Dashboard---DBA\Data\Raw data\ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)
df.head()

region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

grade_levels = {
    "Kindergarten": ["Kindergarten_Male", "Kindergarten_Female"],
    "Grade 1": ["G1_Male", "G1_Female"],"Grade 2": ["G2_Male", "G2_Female"],
    "Grade 3": ["G3_Male", "G3_Female"], "Grade 4": ["G4_Male", "G4_Female"],
    "Grade 5": ["G5_Male", "G5_Female"],"Grade 6": ["G6_Male", "G6_Female"],
    "Elem NG": ["Elem_NG_Male", "Elem_NG_Female"],"Grade 7": ["G7_Male", "G7_Female"],
    "Grade 8": ["G8_Male", "G8_Female"],"Grade 9": ["G9_Male", "G9_Female"],
    "Grade 10": ["G10_Male", "G10_Female"],"JHS NG": ["JHS_NG_Male", "JHS_NG_Female"],
    "Grade 11": [col for col in df.columns if "G11" in col],"Grade 12": [col for col in df.columns if "G12" in col],}

if 'Region' in df.columns:
    df['Region'] = pd.Categorical(df['Region'], categories=region_order, ordered=True)
    df = df.sort_values('Region')

    region_grade_totals = df.groupby('Region', observed=False).sum()[sum(grade_levels.values(), [])]
    region_grade_totals = region_grade_totals.T.groupby(lambda x: next((k for k, v in grade_levels.items() if x in v), None)).sum().T

    plt.figure(figsize=(9, 6))
    ax = region_grade_totals.plot(kind='bar', stacked=True, colormap='viridis', alpha=0.8)
    plt.xlabel("Region")
    plt.ylabel("Total Students")
    plt.title("Distribution of Students per Grade Level Across Regions")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Grade Level")
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.0f}K'))

    plt.show()