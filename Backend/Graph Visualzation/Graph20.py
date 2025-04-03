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

grade_totals = [df[cols].sum().sum() for cols in grade_levels.values()]

# Identify highest and lowest enrollments
max_enrollment = max(grade_totals)
min_enrollment = min(grade_totals)

# Create a stem plot
plt.figure(figsize=(10, 6))
for grade, total in zip(grade_levels.keys(), grade_totals):
    color = 'red' if total == max_enrollment else 'green' if total == min_enrollment else 'blue'
    markerline, stemline, baseline = plt.stem([grade], [total], linefmt='b-', markerfmt='o', basefmt=' ')
    markerline.set_color(color)
    stemline.set_color(color)

# Add labels and title
plt.xlabel("Grade Level")
plt.ylabel("Total Students")
plt.title("Noticeable Decline in Student Population as Grade Levels Progress")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle="--", alpha=0.7)

# Add legend
plt.scatter([], [], color='red', label='Highest Enrollment')
plt.scatter([], [], color='green', label='Lowest Enrollment')
plt.legend()

plt.show()