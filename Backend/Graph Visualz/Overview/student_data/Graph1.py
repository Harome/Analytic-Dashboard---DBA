from Initialization.enrollment_data_loader import load_school_data
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Load data
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")
df_school = data["df_school"]

# Sum all columns that end in '_Male' and '_Female'
male_enrollment = df_school.filter(like='_Male').sum().sum()
female_enrollment = df_school.filter(like='_Female').sum().sum()

# Calculate percentages
total = male_enrollment + female_enrollment
male_percent = round((male_enrollment / total) * 100, 1)
female_percent = round((female_enrollment / total) * 100, 1)

# Convert raw numbers to readable format
male_str = f"{int(male_enrollment):,}"
female_str = f"{int(female_enrollment):,}"

# Start drawing
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_aspect('equal')
plt.axis('off')
ax.set_xlim(0, 16)
ax.set_ylim(2, 11.5)

# Notepad background
notepad_bg = patches.Rectangle((0, 0), 16, 11.5, facecolor='#fcf7ed')
ax.add_patch(notepad_bg)
ax.plot([1.5, 1.5], [0, 11.5], color='red', linewidth=1.5)
for y in range(2, 11):
    ax.plot([0, 16], [y, y], color='skyblue', linewidth=0.75)
for hole_y in [10.5, 6.5, 2.5]:
    ax.add_patch(patches.Circle((0.7, hole_y), 0.2, color='lightgray'))

def draw_gender_pie(x, y, pie_center, r, percent, color, symbol, label_offset=(0, -2.2), rotate=False):
    ax.text(x, y, symbol, fontsize=160, ha='center', va='center', color='black')
    angle = 360 * (percent / 100)
    if not rotate:
        ax.add_patch(patches.Wedge(pie_center, r, 90, 90 - angle, color=color, zorder=5))
        ax.add_patch(patches.Wedge(pie_center, r, 90 - angle, -270, color='#f1f1f1', zorder=4))
    else:
        ax.add_patch(patches.Wedge(pie_center, r, 270, 270 - angle, color=color, zorder=5))
        ax.add_patch(patches.Wedge(pie_center, r, 270 - angle, -90, color='#f1f1f1', zorder=4))
    ax.add_patch(patches.Circle(pie_center, r, edgecolor='black', facecolor='none', linewidth=1, zorder=6))
    offset_x, offset_y = label_offset
    ax.text(x + offset_x, y + offset_y, f"{percent}%", ha='center', fontsize=12, weight='bold', color=color)

# Draw pie charts
draw_gender_pie(
    x=5, y=5.6, pie_center=(4.58, 5.59),
    r=1.05, percent=male_percent,
    color='#2262bd', symbol='\u2642',
    label_offset=(-2, -1.4))

draw_gender_pie(
    x=11, y=5.8, pie_center=(11, 6.7),
    r=1.05, percent=female_percent,
    color='#d12e1e', symbol='\u2640',
    label_offset=(2, 0.1), rotate=True)

# Text labels
ax.text(5, 8.4, f"Male\n{male_str}", ha='center', va='center', fontsize=14, weight='bold', color='#2262bd')
ax.text(11, 8.4, f"Female\n{female_str}", ha='center', va='center', fontsize=14, weight='bold', color='#d12e1e')
ax.text(8, 9.6, "Gender Distribution of Enrollees", fontsize=18, weight='bold', ha='center')

plt.show()
