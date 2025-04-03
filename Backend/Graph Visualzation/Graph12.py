import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = r"/Users/annmargaretteconcepcion/dba/Analytic-Dashboard---DBA/Data/Raw data/ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)

regions = df["Region"].unique()
shs_strands = {
    "ABM": ["G11_ABM_Male", "G11_ABM_Female", "G12_ABM_Male", "G12_ABM_Female"],
    "HUMSS": ["G11_HUMSS_Male", "G11_HUMSS_Female", "G12_HUMSS_Male", "G12_HUMSS_Female"],
    "STEM": ["G11_STEM_Male", "G11_STEM_Female", "G12_STEM_Male", "G12_STEM_Female"],
    "GAS": ["G11_GAS_Male", "G11_GAS_Female", "G12_GAS_Male", "G12_GAS_Female"],
    "PBM": ["G11_PBM_Male", "G11_PBM_Female", "G12_PBM_Male", "G12_PBM_Female"],
    "TVL": ["G11_TVL_Male", "G11_TVL_Female", "G12_TVL_Male", "G12_TVL_Female"],
    "SPORTS": ["G11_SPORTS_Male", "G11_SPORTS_Female", "G12_SPORTS_Male", "G12_SPORTS_Female"],
    "ARTS": ["G11_ARTS_Male", "G11_ARTS_Female", "G12_ARTS_Male", "G12_ARTS_Female"]}

population_by_region = {region: {strand: df[df["Region"] == region][columns].sum().sum() for strand, columns in shs_strands.items()} for region in regions}

x_labels = list(shs_strands.keys())
region_values = {region: [population_by_region[region][strand] for strand in x_labels] for region in regions}

stack_values = np.array([list(region_values[region]) for region in regions])

fig, ax = plt.subplots(figsize=(10, 6))
ax.stackplot(x_labels, stack_values, labels=regions, alpha=0.8)

ax.set_xlabel("SHS Strands")
ax.set_ylabel("Total Student Population")
ax.set_title("Student Population in SHS Strands Across All Regions")
ax.legend(title="Regions", bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()