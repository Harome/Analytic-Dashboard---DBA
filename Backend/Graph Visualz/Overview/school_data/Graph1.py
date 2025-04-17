import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
from Initialization.enrollment_data_loader import load_school_data

# Load the school-level enrollment data
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")

# Extract the school data
df_school = data["df_school"]
region_order = data["region_order"]

# Count the number of schools per region (adjust if needed based on data structure)
region_counts = df_school['Region'].value_counts().reindex(region_order, fill_value=0)
num_schools = region_counts.sum()

# Set up the figure and axes for the visualization
fig, ax = plt.subplots()
fig.set_size_inches(9, 6)
ax.set_xlim(1.5, 10)
ax.set_ylim(2.5, 8.5)
ax.set_aspect('equal')
ax.axis('off')

# Add a rectangle to represent a screen
screen = patches.Rectangle((2.5, 5.5), 5, 3, linewidth=2, edgecolor='black', facecolor='#d3d3d3')
ax.add_patch(screen)

# Inner rectangle representing a different screen area
inner_screen = patches.Rectangle((2.7, 5.7), 4.6, 2.6, linewidth=1, edgecolor='black', facecolor='#faf8f7')
ax.add_patch(inner_screen)

# Blue background for the screen
blue_bg = patches.Rectangle((2.7, 5.7), 4.6, 2.6, linewidth=1, edgecolor='none', facecolor='#2262bd', alpha=0.8)
ax.add_patch(blue_bg)

# Add text lines for labels
text_lines = [("Total Number of Schools", 17, 0.0, '#fcf7ed'),
              ("(under the Philippine Education System)", 9, -0.4, '#2a1617'),
              (f"{num_schools:,}", 35, -1.0, '#FDD85D')]

x_center = 5.0
y_base = 7.7

# Render the text lines in the figure
for text, size, offset, color in text_lines:
    y_pos = y_base + offset
    ax.text(x_center, y_pos, text,
            ha='center', va='center',
            fontsize=size, color=color, fontweight='bold')

    if text == f"{num_schools:,}":
        underline_width = 2.3
        underline_height = 0.33
        ax.plot([x_center - underline_width / 2, x_center + underline_width / 2],
                [y_pos - underline_height, y_pos - underline_height],
                color=color, linewidth=1.3)

# Add school buildings in the visualization (represented as rectangles)
start_x = 3.2
spacing = 0.4
y_building = 5.8
building_width = 0.2
building_height = 0.3

color1 = '#8ab17d'
color2 = '#ba4141'

# Create buildings based on the number of regions
for i in range(num_schools):
    x = start_x + i * spacing

    if i % 2 == 0:
        building_color = color1
    else:
        building_color = color2

    building = patches.Rectangle((x - building_width / 2, y_building), building_width, building_height,
                                 edgecolor='black', facecolor=building_color)
    ax.add_patch(building)

    window_width = 0.05
    window_height = 0.1
    for j in range(2):
        ax.add_patch(patches.Rectangle((x - building_width / 4 + j * window_width, y_building + 0.1),
                                      window_width, window_height, edgecolor='black', facecolor='white'))

    ax.plot([x - building_width / 2, x, x + building_width / 2],
            [y_building + building_height, y_building + building_height + 0.1, y_building + building_height],
            color='black', linewidth=2)

# Add a stand and base
stand = patches.Rectangle((4.7, 4.9), 1.1, 0.6, linewidth=1, edgecolor='black', facecolor='#808080')
ax.add_patch(stand)
base_stand = patches.Rectangle((4.4, 4.6), 1.7, 0.3, linewidth=1, edgecolor='black', facecolor='#606060')
ax.add_patch(base_stand)

# Add CPU, CD slot, power button, vents
cpu = patches.Rectangle((7.7, 4.8), 1.5, 3.7, linewidth=2, edgecolor='black', facecolor='#888888')
ax.add_patch(cpu)
cd_slot = patches.Rectangle((8.0, 7.9), 1.0, 0.1, linewidth=1, edgecolor='black', facecolor='#2e2e2e')
ax.add_patch(cd_slot)
power_button = patches.Circle((8.45, 5.3), 0.15, edgecolor='black', facecolor='green')
ax.add_patch(power_button)

for i in range(4):
    vent = patches.Rectangle((8.0, 6.9 - i * 0.3), 1.0, 0.08, edgecolor='black', facecolor='#444444')
    ax.add_patch(vent)

# Add keyboard base and keys
keyboard_base = patches.Rectangle((2.83, 2.83), 4.3, 1.2, linewidth=2, edgecolor='black', facecolor='#2f2f2f')
ax.add_patch(keyboard_base)

key_h = 0.2
gap = 0.03
rows = [(3, [0.3]*9 + [0.35] + [0.45] + [0.2]),
        (3, [0.5] + [0.3]*5 + [1] + [0.4] + [0.4]),
        (3, [0.8] + [0.3]*7 + [0.9]),
        (3, [0.2, 0.4] + [0.5] + [1.4, 0.3] + [0.48] + [0.3, 0.25]),]

y = 3.9 - key_h
for row_index, (x_start, widths) in enumerate(rows):
    x = x_start
    for i, w in enumerate(widths):
        shadow_offset = 0.03
        shadow = patches.Rectangle((x + shadow_offset, y - shadow_offset), w, key_h, linewidth=0.5, edgecolor='none', facecolor='#555555')
        ax.add_patch(shadow)

        key = patches.Rectangle((x, y), w, key_h, linewidth=0.5, edgecolor='black', facecolor='#bbbbbb')
        ax.add_patch(key)

        x += w + gap
    y -= key_h + gap

# Add mouse and scroll wheel
mouse = patches.Ellipse((7.8, 3.4), 0.6, 1.0, edgecolor='black', facecolor='#cccccc', linewidth=1.5)
ax.add_patch(mouse)
scroll_wheel = patches.Rectangle((7.78, 3.65), 0.04, 0.15, edgecolor='black', facecolor='black')
ax.add_patch(scroll_wheel)

# Show the plot
plt.show()
