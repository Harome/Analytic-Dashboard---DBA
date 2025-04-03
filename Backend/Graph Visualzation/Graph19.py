import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = r"/Users/annmargaretteconcepcion/dba/Analytic-Dashboard---DBA/Data/Raw data/ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)

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

plt.figure(figsize=(10, 6))

for grade, cols in grade_levels.items():
    grade_totals = df.groupby("Region", observed=False)[cols].sum().sum(axis=1)
    grade_totals = grade_totals.reindex(region_order)
    plt.plot(grade_totals.index, grade_totals.values, marker='o', linestyle='-', label=grade)

    # Highlight highest and lowest points with different colors
    max_idx = grade_totals.idxmax()
    min_idx = grade_totals.idxmin()

    plt.scatter(max_idx, grade_totals[max_idx], color='red', s=100, zorder=3)
    plt.scatter(min_idx, grade_totals[min_idx], color='blue', s=100, zorder=3)

plt.xlabel("Region")
plt.ylabel("Total Students")
plt.title("Total Student Enrollment per Grade Level Across Regions")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle="--", alpha=0.7)
plt.legend(title="Grade Levels", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()