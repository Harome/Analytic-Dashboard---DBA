import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

regions = df["Region"].unique()

population_by_region = {
    region: {
        division: df[df["Region"] == region][columns].sum().sum() 
        for division, columns in grade_levels.items()
    } 
    for region in regions
}

x_labels = list(grade_levels.keys())
region_values = {region: [population_by_region[region][division] for division in x_labels] for region in regions}

fig, ax = plt.subplots(figsize=(10, 6))

bottom_values = np.zeros(len(x_labels))

for region in regions:
    ax.bar(x_labels, region_values[region], label=region, bottom=bottom_values)
    bottom_values += np.array(region_values[region])  # Update bottom values for stacking

ax.set_xlabel("Grade Division", fontsize=12)
ax.set_ylabel("Total Student Population", fontsize=12)
ax.set_title("Student Population per Grade Division Across All Regions", fontsize=14)

ax.legend(title="Regions", bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(axis='y', linestyle='--', alpha=0.7)

ax.set_xticklabels(x_labels, rotation=45, ha="right")

plt.tight_layout()
plt.show()
