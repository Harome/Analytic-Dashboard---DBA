import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

path = r"/Users/annmargaretteconcepcion/dba/Analytic-Dashboard---DBA/Data/Raw data/ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)

grade_levels = {
    "Kindergarten": ["Kindergarten_Male", "Kindergarten_Female"],
    "Grade 1": ["G1_Male", "G1_Female"], "Grade 2": ["G2_Male", "G2_Female"],
    "Grade 3": ["G3_Male", "G3_Female"], "Grade 4": ["G4_Male", "G4_Female"],
    "Grade 5": ["G5_Male", "G5_Female"], "Grade 6": ["G6_Male", "G6_Female"],
    "Elem NG": ["Elem_NG_Male", "Elem_NG_Female"], "Grade 7": ["G7_Male", "G7_Female"],
    "Grade 8": ["G8_Male", "G8_Female"], "Grade 9": ["G9_Male", "G9_Female"],
    "Grade 10": ["G10_Male", "G10_Female"], "JHS NG": ["JHS_NG_Male", "JHS_NG_Female"],
    "Grade 11": [col for col in df.columns if "G11" in col],  # All G11-related columns
    "Grade 12": [col for col in df.columns if "G12" in col]   # All G12-related columns
}

grade_labels = []
male_counts = []
female_counts = []

for grade, columns in grade_levels.items():
    if isinstance(columns[0], list):  # SHS (G11 & G12) has multiple columns
        male_total = df[[col for col in columns if "Male" in col]].sum().sum()
        female_total = df[[col for col in columns if "Female" in col]].sum().sum()
    else:
        male_total = df[columns[0]].sum()
        female_total = df[columns[1]].sum()
    
    male_counts.append(male_total)
    female_counts.append(female_total)
    grade_labels.append(grade)

grade_indices = np.arange(len(grade_labels))

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(grade_indices, male_counts, color='blue', linestyle='--', marker='o', label="Male")
ax.plot(grade_indices, female_counts, color='pink', linestyle='--', marker='o', label="Female")

ax.fill_between(grade_indices, male_counts, color='blue', alpha=0.4)
ax.fill_between(grade_indices, female_counts, color='pink', alpha=0.4)

ax.set_xticks(grade_indices)
ax.set_xticklabels(grade_labels, rotation=45)
ax.set_xlabel("Grade Level")
ax.set_ylabel("Student Population")
ax.set_title("Student Population per Grade Level by Gender (All Regions)")
ax.legend()

plt.show()
