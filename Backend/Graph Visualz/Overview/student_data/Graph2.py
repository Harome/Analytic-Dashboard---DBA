from Initialization.enrollment_data_loader import load_school_data
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import numpy as np

# Load school data
data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")
df_school = data["df_school"]

# Clean & prepare: group by region and sum total enrollment
df_school['Total Enrollment'] = df_school.filter(like='Male').sum(axis=1) + df_school.filter(like='Female').sum(axis=1)
region_totals = df_school.groupby('Region')['Total Enrollment'].sum().sort_values(ascending=False)

# Prepare values
regions = region_totals.index.tolist()
region_values = region_totals.values.tolist()
region_labels = [(r, f"{v:,}") for r, v in zip(regions, region_values)]

# Color palette
watercolor_colors = ['#264653', '#287271', '#2A9D8F', '#BAB170', '#E9C46A', '#EFB306',
    '#F4A261', '#EE8959', '#E76F51', '#E63946', '#EC9A9A', '#F1FAEE',
    '#CDEAE5', '#A8DADC', '#77ABBD', '#457B9D', '#31587A', '#1D3557']

# Resize circles based on population percentages
total_population = sum(region_values)
percentages = [v / total_population for v in region_values]
min_radius = 0.15
max_radius = 0.42
scaled_radii = [min_radius + (np.sqrt(p) * (max_radius - min_radius) / np.sqrt(max(percentages)))
    for p in percentages]

# Layout
rows, cols = 3, 6
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_xlim(-1.5, cols + 0.5)
ax.set_ylim(-0.5, rows + 1)
ax.set_aspect('equal')
ax.axis('off')

# Paint tray background
ax.add_patch(patches.FancyBboxPatch(
    (0, 0), cols, rows, boxstyle="round,pad=0.05", linewidth=2,
    edgecolor="gray", facecolor="#f0f0f0"))

# Draw each "paint"
for i, ((region, value), color) in enumerate(zip(region_labels, watercolor_colors)):
    col = i % cols
    row = rows - 1 - (i // cols)
    cx, cy = col + 0.5, row + 0.5

    # White tray
    tray = patches.FancyBboxPatch(
        (col + 0.1, row + 0.1), 0.8, 0.8, boxstyle="round,pad=0.02",
        linewidth=1, edgecolor="dimgray", facecolor="white")
    ax.add_patch(tray)

    # Paint circle
    paint = patches.Circle(
        (cx, cy), scaled_radii[i], facecolor=color, edgecolor='gray',
        linewidth=0.6, alpha=0.95)
    ax.add_patch(paint)

    # Choose label color based on brightness
    rgb = mcolors.to_rgb(color)
    brightness = sum(rgb) / 3
    text_color = 'black' if brightness > 0.22 else 'white'

    ax.text(cx, cy + 0.12, region, ha='center', va='center', fontsize=7.2, color=text_color)
    ax.text(cx, cy - 0.15, value, ha='center', va='center', fontsize=8, color=text_color, fontweight='bold')

# Paintbrush decorations (optional, fun aesthetic)
ax.plot([-0.08, -0.3], [0.2, 3.2], color='#457B9D', linewidth=10, solid_capstyle='round', zorder=10)
ax.add_patch(patches.Polygon([[-0.3, 3.2], [-0.45, 3.4], [-0.15, 3.4]], closed=True, facecolor='black', edgecolor='black', zorder=10))

ax.plot([-0.2, -0.4], [0.5, 2.5], color='#2A9D8F', linewidth=8, solid_capstyle='round', zorder=10)
ax.add_patch(patches.Circle((-0.4, 2.5), radius=0.1, facecolor='black', edgecolor='black', zorder=11))

ax.plot([-0.15, -0.35], [0.3, 3.8], color='#E76F51', linewidth=6, solid_capstyle='round', zorder=10)
ax.add_patch(patches.Polygon([[-0.35, 3.8], [-0.55, 4.0], [-0.25, 4.0]], closed=True, facecolor='black', edgecolor='black', zorder=11))

# Title
ax.text(0.56, 0.89, "Distribution of Students Across Philippine Regions",
        ha='center', va='center', fontsize=12, fontweight='bold', transform=ax.transAxes)

plt.show()
