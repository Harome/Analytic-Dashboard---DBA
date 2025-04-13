import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np
from IPython.display import display

path = r"D:\zDonludoz\Git\Analytic-Dashboard---DBA\Data\Raw data\ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)
df.head()

grade_levels = {
    "Kindergarten": ["Kindergarten_Male", "Kindergarten_Female"],
    "Grade 1": ["G1_Male", "G1_Female"],"Grade 2": ["G2_Male", "G2_Female"],
    "Grade 3": ["G3_Male", "G3_Female"], "Grade 4": ["G4_Male", "G4_Female"],
    "Grade 5": ["G5_Male", "G5_Female"],"Grade 6": ["G6_Male", "G6_Female"],
    "Elem NG": ["Elem_NG_Male", "Elem_NG_Female"],"Grade 7": ["G7_Male", "G7_Female"],
    "Grade 8": ["G8_Male", "G8_Female"],"Grade 9": ["G9_Male", "G9_Female"],
    "Grade 10": ["G10_Male", "G10_Female"],"JHS NG": ["JHS_NG_Male", "JHS_NG_Female"],
    "Grade 11": [col for col in df.columns if "G11" in col],"Grade 12": [col for col in df.columns if "G12" in col],}

year_level_totals = {level: df[columns].sum().sum() for level, columns in grade_levels.items()}

labels = list(year_level_totals.keys())
sizes = list(year_level_totals.values())
colors = plt.cm.get_cmap("tab20", len(labels)).colors

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(labels, sizes, color=colors, edgecolor="black")

for i, v in enumerate(sizes):
    ax.text(v + max(sizes) * 0.01, i, f"{v:,}", va='center', fontsize=5, fontweight='bold')

ax.set_xlabel("Student Population")
ax.set_ylabel("Year Level")
ax.set_title("Student Population Distribution by Year Level (All Regions)")
plt.gca().invert_yaxis()
plt.show()