import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
import pandas as pd
from Initialization.enrollment_data_loader import load_school_data

# Load the data using your data loader function
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")

# Extract region names and their corresponding total school counts from the data
regions = []

# Since the region names are in `region_order`, and we need to extract the total number of schools,
# let's assume the total schools per region are in a specific row of `sector_distribution` like 'Private', 'Public', etc.

# Adjust the region access accordingly
for region in data["region_order"]:
    try:
        # We will assume you want to get the total number of schools from a specific sector like 'Private', 'Public', etc.
        total_schools = data["sector_distribution"].loc["Private", "Total"]  # Example for 'Private'
    except KeyError:
        print(f"KeyError: Region {region} not found in 'sector_distribution'.")
        continue

    regions.append((region, total_schools))

# Calculate the total number of schools
total = sum(val for _, val in regions)

# Calculate percentages for each region
regions_percent = [(name, val, round((val / total) * 100, 2)) for name, val in regions]
region_dict = {name: (name, val, perc) for name, val, perc in regions_percent}

# Reorganize into rows (group regions in rows)
rows = [
    [region_dict["Region I"], region_dict["Region II"], region_dict["Region III"]],
    [region_dict["Region IV-A"], region_dict["MIMAROPA"], region_dict["Region V"]],
    [region_dict["Region VI"], region_dict["Region VII"], region_dict["Region VIII"]],
    [region_dict["Region VIII"], region_dict["Region IX"], region_dict["Region X"], region_dict["Region XI"]],
    [region_dict["Region XII"], region_dict["CARAGA"], region_dict["BARMM"],
     region_dict["CAR"], region_dict["NCR"], region_dict["PSO"]]]

scale = 1.2
box_height = 2.5
spacing = 0.3
x_center = 25
y_start = 100
fixed_fontsize = 10

fig, ax = plt.subplots(figsize=(30, 22))
ax.set_aspect('equal')
ax.axis('off')

roof_base_x = []
roof_base_y = []

roof_mid_x = (roof_base_x[0] + roof_base_x[1]) / 2 if roof_base_x else x_center
plt.text(roof_mid_x, y_start + 3.5, "Distribution of Schools per Region",
         fontsize=35, fontweight='bold', ha='center')

colors = ['#ba4141', '#2262bd', '#1b8e3e', '#FDD85D']

roof_base_x = []
roof_base_y = []

# Plot each region as a box
for row_index, row in enumerate(rows):
    widths = [p * scale for _, _, p in row]
    total_row_width = sum(widths) + (len(row) - 1) * spacing
    x_start = x_center - total_row_width / 2
    y = y_start - (row_index + 1) * (box_height + 0.3)

    if row_index == 0:
        roof_base_x = [x_start, x_start + total_row_width]
        roof_base_y = [y + box_height, y + box_height]
    if row_index == len(rows) - 1:
        last_row_y = y

    x = x_start
    for i, (region, _, percent) in enumerate(row):
        width = percent * scale
        color = colors[i % len(colors)]
        box = patches.Rectangle((x, y), width, box_height, facecolor=color, edgecolor='black')
        ax.add_patch(box)

        ax.text(x + width / 2, y + box_height / 2,
                f"{region}\n{_}",
                ha='center', va='center',
                fontsize=fixed_fontsize, fontweight='bold')
        x += width + spacing

# Draw roof if needed
if roof_base_x:
    roof_gap = 0.3
    triangle_top = ((roof_base_x[0] + roof_base_x[1]) / 2, roof_base_y[0] + 3 + roof_gap)
    triangle = Polygon(
        [(roof_base_x[0], roof_base_y[0] + roof_gap),
         (roof_base_x[1], roof_base_y[1] + roof_gap),
         triangle_top],
        closed=True, facecolor='#7a4b47', edgecolor='black')
    ax.add_patch(triangle)

ax.set_xlim(0, 50)
ax.set_ylim(last_row_y - 1, y_start + 6)

plt.show()
