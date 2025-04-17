# enrollment_visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from Initialization.enrollment_data_loader import load_school_data  # Make sure the .py file is in the same directory or set Python path

# Load the data from Excel file
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")

# Extract the sector totals
sector_totals = data["sector_distribution"]["Total"]

# Calculate total number of schools
total_schools = sector_totals.sum()

# Calculate percentage per sector
public_total = sector_totals.get("Public", 0)
sucslucs_total = sector_totals.get("SUCsLUCs", 0)
pso_total = sector_totals.get("PSO", 0)
private_total = sector_totals.get("Private", 0)
sucslucs_pso_total = sucslucs_total + pso_total

percent_public = f"{(public_total / total_schools * 100):.2f}%"
percent_sucslucs = f"{(sucslucs_total / total_schools * 100):.2f}%"
percent_private = f"{(private_total / total_schools * 100):.2f}%"
percent_pso = f"{(pso_total / total_schools * 100):.2f}%"

# Drawing function
def draw_pencil(x_offset, color, height, label, percentage, percentage_offset, left_value):
    pencil_body = patches.Rectangle((x_offset - 50, -100), 100, height, linewidth=1, edgecolor='black', facecolor=color)
    ax.add_patch(pencil_body)

    wood_part = patches.Polygon([(x_offset - 50, height - 100), (x_offset + 50, height - 100), (x_offset, height - 30)],
                                 closed=True, facecolor='#DEB887', edgecolor='black')
    ax.add_patch(wood_part)

    tip_y = height - 30
    graphite_tip = patches.Circle((x_offset, tip_y), 5, facecolor='black', edgecolor='black')
    ax.add_patch(graphite_tip)

    eraser = patches.Rectangle((x_offset - 50, -100), 100, 20, linewidth=1, edgecolor='black', facecolor='pink')
    ax.add_patch(eraser)

    visible_gap = 10
    line_start_y = tip_y + 5 + visible_gap
    ax.plot([x_offset, x_offset], [line_start_y, line_start_y + 45], color='black', linestyle='-', linewidth=1.5)

    label_y = -50 + height / 2
    ax.text(x_offset, label_y, label, ha='center', va='center', fontsize=10, color='black', rotation=90, fontweight="bold")

    percentage_y = label_y + percentage_offset
    ax.text(x_offset + 25, percentage_y, percentage, ha='left', va='center', fontsize=10, color=color, fontweight='bold')

    ax.text(x_offset - 25, line_start_y + 15, str(left_value), ha='right', va='center', fontsize=10, color=color, fontweight='bold')


# Start plotting
fig, ax = plt.subplots(figsize=(12, 6))

# Draw pencils using data
draw_pencil(-300, '#1b8e3e', 350, 'Public', percent_public, 230, f'Public sector\nhas {int(public_total):,}\nschools')
draw_pencil(-60, '#FDD85D', 250, 'SUCs/LUCs', percent_sucslucs, 180, f'SUCs/LUCs sector\nhas {int(sucslucs_total):,}\nschools')
draw_pencil(180, '#2262bd', 300, 'Private', percent_private, 205, f'Private sector\nhas {int(private_total):,}\nschools')
draw_pencil(420, '#ba4141', 200, 'PSO', percent_pso, 150, f'PSO sector\nhas {int(pso_total):,}\nschools')

# Final formatting
plt.title("School Distribution per Sector", fontsize=14, fontweight='bold')
ax.set_xlim(-400, 550)
ax.set_ylim(-150, 470)
ax.set_aspect('equal')
ax.axis('off')

plt.show()
