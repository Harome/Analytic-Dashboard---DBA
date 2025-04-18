import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
from Initialization.enrollment_data_loader import load_school_data  # Import the module

# Load the data
file_path = '/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx'
data = load_school_data(file_path)

# Extract total student populations for the levels
elementary_students = data["total_by_level"]["Elementary"]
junior_high_students = data["total_by_level"]["Junior High"]
senior_high_students = data["total_by_level"]["Senior High"]

# Calculate percentages
total_students = elementary_students + junior_high_students + senior_high_students
elementary_percentage = (elementary_students / total_students) * 100
junior_high_percentage = (junior_high_students / total_students) * 100
senior_high_percentage = (senior_high_students / total_students) * 100

fig, ax = plt.subplots()

y_shift = -0.3

book_width = 1
book_height = 5
green_book_height = 4
blue_book_height = 3

x_positions = [1, 3, 4.19]
colors = ['#ba4141', '#1b8e3e', '#2262bd']

# Red book (Elementary)
red_book = patches.FancyBboxPatch(
    (x_positions[0], 0 + y_shift), book_width, book_height,
    boxstyle="round,pad=0.05", linewidth=1, edgecolor='black', facecolor=colors[0])
ax.add_patch(red_book)

# Green book (Junior High)
green_transform = transforms.Affine2D().rotate_deg_around(x_positions[1], 0 + y_shift, 12) + ax.transData
green_book = patches.FancyBboxPatch(
    (x_positions[1], 0 + y_shift), book_width, green_book_height,
    boxstyle="round,pad=0.05", linewidth=1, edgecolor='black', facecolor=colors[1],
    transform=green_transform)
ax.add_patch(green_book)

# Blue book (Senior High)
blue_book = patches.FancyBboxPatch(
    (x_positions[2], 0 + y_shift), book_width, blue_book_height,
    boxstyle="round,pad=0.05", linewidth=1, edgecolor='black', facecolor=colors[2])
ax.add_patch(blue_book)

# Title
plt.title("Student Population Distribution by Grade Division", fontsize=14, fontweight='bold')

# Add lines to connect
ax.plot([x_positions[0], x_positions[0] + book_width], [book_height - 0.1 + y_shift, book_height - 0.1 + y_shift], color='#ffb2a2', linewidth=2)
ax.plot([x_positions[0], x_positions[0] + book_width], [book_height - 0.3 + y_shift, book_height - 0.3 + y_shift], color='#ffb2a2', linewidth=2)
ax.plot([x_positions[2], x_positions[2] + book_width], [blue_book_height - 0.1 + y_shift, blue_book_height - 0.1 + y_shift], color='#87ceeb', linewidth=2)
ax.plot([x_positions[2], x_positions[2] + book_width], [blue_book_height - 0.3 + y_shift, blue_book_height - 0.3 + y_shift], color='#87ceeb', linewidth=2)

# Green line transformation
green_line_transform = transforms.Affine2D().rotate_deg_around(x_positions[1], 0 + y_shift, 12) + ax.transData
ax.plot([x_positions[1], x_positions[1] + book_width],
        [green_book_height - 0.1 + y_shift, green_book_height - 0.1 + y_shift], color='#98fb09', linewidth=2, transform=green_line_transform)
ax.plot([x_positions[1], x_positions[1] + book_width],
        [green_book_height - 0.3 + y_shift, green_book_height - 0.3 + y_shift], color='#98fb09', linewidth=2, transform=green_line_transform)

# Function to draw stick man
def draw_stick_man(x_pos, book_height, book_width, offset_y):
    head_radius = 0.1
    body_height = 0.3
    leg_length = 0.2
    leg_offset = 0.05
    head_center = (x_pos + book_width / 2, book_height + offset_y + y_shift)

    head = plt.Circle(head_center, head_radius, edgecolor='black', facecolor='none', linewidth=2)
    ax.add_patch(head)

    ax.plot([head_center[0], head_center[0]], [head_center[1] - head_radius, head_center[1] - head_radius - body_height], color='black', linewidth=2)
    ax.plot([head_center[0] - 0.1, head_center[0] + 0.1],
            [head_center[1] - head_radius - 0.15, head_center[1] - head_radius - 0.15], color='black', linewidth=2)

    legs_start_y = head_center[1] - head_radius - body_height - leg_offset
    ax.plot([head_center[0], head_center[0] - 0.15], [legs_start_y, legs_start_y - leg_length], color='black', linewidth=2)
    ax.plot([head_center[0], head_center[0] + 0.15], [legs_start_y, legs_start_y - leg_length], color='black', linewidth=2)

    rect_width = 2
    rect_height = 0.7
    rect_x = head_center[0] + 0.15
    rect_y = head_center[1] - rect_height / 2
    color_map = {
        x_positions[0]: '#ffb2a2',
        x_positions[1] - 0.5: '#98fb98',
        x_positions[2]: '#add8e6',}
    ax.add_patch(patches.Rectangle(
        (rect_x, rect_y), rect_width, rect_height,
        facecolor=color_map.get(x_pos, 'gray'), edgecolor='black', linewidth=1))

# Draw stick men
draw_stick_man(x_positions[0], book_height, book_width, 0.7)
draw_stick_man(x_positions[1] - 0.5, green_book_height, book_width, 0.7)
draw_stick_man(x_positions[2], blue_book_height, book_width, 0.7)

# Highlights
highlight_alpha = 0.2
highlight_color = 'black'

red_highlight = patches.Rectangle((x_positions[0], 0 + y_shift), book_width, book_height,
                                  linewidth=1.5, edgecolor=highlight_color, facecolor=highlight_color, alpha=highlight_alpha)
ax.add_patch(red_highlight)

green_highlight = patches.Rectangle((x_positions[1], 0 + y_shift), book_width, green_book_height,
                                    linewidth=1.5, edgecolor=highlight_color, facecolor=highlight_color, alpha=highlight_alpha,
                                    transform=green_transform)
ax.add_patch(green_highlight)

blue_highlight = patches.Rectangle((x_positions[2], 0 + y_shift), book_width, blue_book_height,
                                   linewidth=1.5, edgecolor=highlight_color, facecolor=highlight_color, alpha=highlight_alpha)
ax.add_patch(blue_highlight)

# Add text labels with actual data
ax.text(x_positions[0] + book_width / 2 + 1.17, book_height / 2 + y_shift + 3.2,
        f"Elementary School\nStudents: {elementary_students:,}\nPercentage: {elementary_percentage:.1f}%",
        va='center', ha='center', fontsize=7, color='black', fontweight='bold')

ax.text(x_positions[1] + book_width / 2 + 1.6, green_book_height / 2.12 + y_shift + 2.50,
        f"Junior Highschool\nStudents: {junior_high_students:,}\nPercentage: {junior_high_percentage:.1f}%",
        va='center', ha='center', fontsize=7.5, color='black', fontweight='bold', transform=green_transform)

ax.text(x_positions[2] + book_width / 2 + 1.15, blue_book_height / 2.12 + y_shift + 2.3,
        f"Senior Highschool\nStudents: {senior_high_students:,}\nPercentage: {senior_high_percentage:.1f}%",
        va='center', ha='center', fontsize=7.5, color='black', fontweight='bold')

# Add labels
ax.text(x_positions[0] + book_width / 2, book_height / 2 + y_shift, "Elementary School", rotation=90,
        va='center', ha='center', fontsize=10, color='white', fontweight='bold')

ax.text(x_positions[1] + book_width / 2, green_book_height / 2 + y_shift, "Junior Highschool", rotation=102,
        va='center', ha='center', fontsize=10, color='white', fontweight='bold', transform=green_transform)

ax.text(x_positions[2] + book_width / 2, blue_book_height / 2 + y_shift, "Senior Highschool", rotation=90,
        va='center', ha='center', fontsize=10, color='white', fontweight='bold')

# Set plot limits and aspect ratio
ax.set_xlim(0, 7)
ax.set_ylim(0, 6)
ax.axis('off')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
