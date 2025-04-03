import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


path = r"/Users/annmargaretteconcepcion/dba/Analytic-Dashboard---DBA/Data/Raw data/ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)

grade_levels = {
    "Kindergarten": ["Kindergarten_Male", "Kindergarten_Female"],
    "Grade 1": ["G1_Male", "G1_Female"],"Grade 2": ["G2_Male", "G2_Female"],
    "Grade 3": ["G3_Male", "G3_Female"], "Grade 4": ["G4_Male", "G4_Female"],
    "Grade 5": ["G5_Male", "G5_Female"],"Grade 6": ["G6_Male", "G6_Female"],
    "Elem NG": ["Elem_NG_Male", "Elem_NG_Female"],"Grade 7": ["G7_Male", "G7_Female"],
    "Grade 8": ["G8_Male", "G8_Female"],"Grade 9": ["G9_Male", "G9_Female"],
    "Grade 10": ["G10_Male", "G10_Female"],"JHS NG": ["JHS_NG_Male", "JHS_NG_Female"],
    "Grade 11": [col for col in df.columns if "G11" in col],"Grade 12": [col for col in df.columns if "G12" in col],}
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
region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

df.rename(columns=lambda x: x.strip(), inplace=True)


df_region_population = df.groupby('Region')[[*grade_columns_male, *grade_columns_female]].sum()
df_region_population['Total Population'] = df_region_population.sum(axis=1)

df_region_population = df_region_population.loc[df_region_population.index.intersection(region_order)]
df_region_population = df_region_population.reindex(region_order)

avg_population = df_region_population['Total Population'].mean()
std_dev_population = df_region_population['Total Population'].std()
high_threshold = avg_population + std_dev_population
low_threshold = avg_population - std_dev_population

color_map = {"Significantly Higher": "#FADADD","Significantly Lower": "#9ac4f5","Average": "#C1E1C1"}

df_region_population['Category'] = df_region_population['Total Population'].apply(
    lambda x: "Significantly Higher" if x > high_threshold else
              "Significantly Lower" if x < low_threshold else "Average")

plt.figure(figsize=(12, 6))
bars = plt.bar(df_region_population.index, df_region_population['Total Population'],
               color=df_region_population['Category'].map(color_map))

plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))

plt.xlabel("Region", fontsize=12)
plt.ylabel("Total Student Population", fontsize=12)
plt.title("Student Population Rate per Region", fontsize=14)
plt.xticks(rotation=30, ha='right', fontsize=10)

legend_labels = [plt.Line2D([0], [0], color=color, lw=6, label=label) for label, color in color_map.items()]
plt.legend(handles=legend_labels, title="Population Category")

plt.show()