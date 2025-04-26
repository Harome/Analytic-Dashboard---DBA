# Imports
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np
import plotly.graph_objects as go
import matplotlib.ticker as mtick
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.patches as patches
from matplotlib.sankey import Sankey
from matplotlib.ticker import FuncFormatter, MultipleLocator
from plotly.subplots import make_subplots
import textwrap
import json
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import matplotlib.transforms as transforms
import io
import base64
from matplotlib.patches import Polygon,  Circle
import os
import json
import matplotlib
import warnings
matplotlib.use('Agg')

warnings.filterwarnings("ignore", category=DeprecationWarning)

config_path = 'config.json'
def load_config():
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    with open(config_path, 'r') as f:
        return json.load(f)
    
config = load_config()
path = config.get('dataset_path')
df_school = pd.read_excel(path)

def safe_load_excel(path):
    if path and os.path.exists(path):
        try:
            return pd.read_excel(path, engine='openpyxl')
        except Exception as e:
            print(f"[safe_load_excel] Failed to load {path}: {e}")
    return None

def load_school_data():
    config = load_config()

    school_df = safe_load_excel(config.get('school_dataset_path'))
    if school_df is not None:
        return school_df

    default_df = safe_load_excel(config.get('dataset_path'))
    if default_df is not None:
        return default_df

    return pd.DataFrame() 

def load_student_data():
    config = load_config()

    student_df = safe_load_excel(config.get('student_dataset_path'))
    if student_df is not None:
        return student_df

    default_df = safe_load_excel(config.get('dataset_path'))
    if default_df is not None:
        return default_df

    return pd.DataFrame()

region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

grade_columns_male = ['Kindergarten_Male', 'G1_Male', 'G2_Male', 'G3_Male', 'G4_Male', 'G5_Male', 'G6_Male',
                     'Elem_NG_Male', 'G7_Male', 'G8_Male', 'G9_Male', 'G10_Male', 'JHS_NG_Male',
                      'G11_ABM_Male', 'G11_HUMSS_Male', 'G11_STEM_Male', 'G11_GAS_Male',
                      'G11_PBM_Male', 'G11_TVL_Male', 'G11_SPORTS_Male', 'G11_ARTS_Male',
                      'G12_ABM_Male', 'G12_HUMSS_Male', 'G12_STEM_Male', 'G12_GAS_Male',
                      'G12_PBM_Male', 'G12_TVL_Male', 'G12_SPORTS_Male', 'G12_ARTS_Male']

grade_columns_female = ['Kindergarten_Female', 'G1_Female', 'G2_Female', 'G3_Female', 'G4_Female', 'G5_Female', 'G6_Female',
                      'Elem_NG_Female', 'G7_Female', 'G8_Female', 'G9_Female', 'G10_Female', 'JHS_NG_Female',
                      'G11_ABM_Female', 'G11_HUMSS_Female', 'G11_STEM_Female', 'G11_GAS_Female',
                      'G11_PBM_Female', 'G11_TVL_Female', 'G11_SPORTS_Female', 'G11_ARTS_Female',
                      'G12_ABM_Female', 'G12_HUMSS_Female', 'G12_STEM_Female', 'G12_GAS_Female',
                      'G12_PBM_Female', 'G12_TVL_Female', 'G12_SPORTS_Female', 'G12_ARTS_Female']

grade_levels = {"Kindergarten": ["Kindergarten_Male", "Kindergarten_Female"], "Grade 1": ["G1_Male", "G1_Female"],"Grade 2": ["G2_Male", "G2_Female"],
                "Grade 3": ["G3_Male", "G3_Female"], "Grade 4": ["G4_Male", "G4_Female"],
                "Grade 5": ["G5_Male", "G5_Female"],"Grade 6": ["G6_Male", "G6_Female"],
                "Elem NG": ["Elem_NG_Male", "Elem_NG_Female"],"Grade 7": ["G7_Male", "G7_Female"],
                "Grade 8": ["G8_Male", "G8_Female"],"Grade 9": ["G9_Male", "G9_Female"],
                "Grade 10": ["G10_Male", "G10_Female"],"JHS NG": ["JHS_NG_Male", "JHS_NG_Female"],
                "Grade 11": [col for col in df_school.columns if "G11" in col],"Grade 12": [col for col in df_school.columns if "G12" in col]}

elementary_male = ["Kindergarten_Male","G1_Male", "G2_Male", "G3_Male", "G4_Male", "G5_Male", "G6_Male", "Elem_NG_Male"]
elementary_female = ["Kindergarten_Female","G1_Female", "G2_Female", "G3_Female", "G4_Female", "G5_Female", "G6_Female", "Elem_NG_Female"]

junior_high_male = ["G7_Male", "G8_Male", "G9_Male", "G10_Male", "JHS_NG_Male"]
junior_high_female = ["G7_Female", "G8_Female", "G9_Female", "G10_Female", "JHS_NG_Female"]

senior_high_male = ["G11_ABM_Male", "G11_HUMSS_Male", "G11_STEM_Male", "G11_GAS_Male","G11_PBM_Male", "G11_TVL_Male", "G11_SPORTS_Male", "G11_ARTS_Male",
                    "G12_ABM_Male", "G12_HUMSS_Male", "G12_STEM_Male", "G12_GAS_Male","G12_PBM_Male", "G12_TVL_Male", "G12_SPORTS_Male", "G12_ARTS_Male"]
senior_high_female = ["G11_ABM_Female", "G11_HUMSS_Female", "G11_STEM_Female", "G11_GAS_Female", "G11_PBM_Female", "G11_TVL_Female", "G11_SPORTS_Female", "G11_ARTS_Female",
                      "G12_ABM_Female", "G12_HUMSS_Female", "G12_STEM_Female", "G12_GAS_Female", "G12_PBM_Female", "G12_TVL_Female", "G12_SPORTS_Female", "G12_ARTS_Female"]

shs_strands = {
    "ABM": ["G11_ABM_Male", "G11_ABM_Female", "G12_ABM_Male", "G12_ABM_Female"],
    "HUMSS": ["G11_HUMSS_Male", "G11_HUMSS_Female", "G12_HUMSS_Male", "G12_HUMSS_Female"],
    "STEM": ["G11_STEM_Male", "G11_STEM_Female", "G12_STEM_Male", "G12_STEM_Female"],
    "GAS": ["G11_GAS_Male", "G11_GAS_Female", "G12_GAS_Male", "G12_GAS_Female"],
    "PBM": ["G11_PBM_Male", "G11_PBM_Female", "G12_PBM_Male", "G12_PBM_Female"],
    "TVL": ["G11_TVL_Male", "G11_TVL_Female", "G12_TVL_Male", "G12_TVL_Female"],
    "SPORTS": ["G11_SPORTS_Male", "G11_SPORTS_Female", "G12_SPORTS_Male", "G12_SPORTS_Female"],
    "ARTS": ["G11_ARTS_Male", "G11_ARTS_Female", "G12_ARTS_Male", "G12_ARTS_Female"]}

Sector = ["Public", "Private", "SUCsLUCs", "PSO"]

sector_students = {
    "Public": ["Public"],
    "Private": ["Private"],
    "SUCsLUCs": ["SUCs/LUCs"],
    "PSO": ["PSO"]
}

sector_distribution = df_school.groupby("Sector").sum(numeric_only=True)

sector_distribution["Elementary_Total"] = sector_distribution[elementary_male].sum(axis=1) + sector_distribution[elementary_female].sum(axis=1)
sector_distribution["Junior_HS_Total"] = sector_distribution[junior_high_male].sum(axis=1) + sector_distribution[junior_high_female].sum(axis=1)
sector_distribution["Senior_HS_Total"] = sector_distribution[senior_high_male].sum(axis=1) + sector_distribution[senior_high_female].sum(axis=1)

sector_distribution["Total"] = sector_distribution[["Elementary_Total", "Junior_HS_Total", "Senior_HS_Total"]].sum(axis=1)

sector_distribution_totals = sector_distribution["Total"]

inner_labels = ["Elementary", "Junior High", "Senior High"]
inner_values = [
    df_school[elementary_male + elementary_female].sum().sum(),
    df_school[junior_high_male + junior_high_female].sum().sum(),
    df_school[senior_high_male + senior_high_female].sum().sum()
]

outer_labels = ["Private", "Public", "Other Sectors"]
sector_distribution = df_school.groupby("Sector").sum(numeric_only=True)
sector_distribution["Total"] = (
    sector_distribution[elementary_male + elementary_female].sum(axis=1) +
    sector_distribution[junior_high_male + junior_high_female].sum(axis=1) +
    sector_distribution[senior_high_male + senior_high_female].sum(axis=1)
)

outer_values = [
    sector_distribution.loc["Private", "Total"],
    sector_distribution.loc["Public", "Total"],
    sector_distribution.loc[["SUCsLUCs", "PSO"], "Total"].sum()
]

regions = df_school['Region'].dropna().unique()
school_subclassification = df_school['School_Subclassification'].dropna().unique()
school_type = df_school['School_Type'].dropna().unique()
modified_coc = df_school['Modified_COC'].dropna().unique()



# Graph 1: Main Dashboard - Student Data No. 1 (Gender Distribution of Enrollees)
def create_gender_plot():
    fig1, ax = plt.subplots(figsize=(5, 4))
    ax.set_aspect('equal')
    ax.axis('off')

    ax.set_xlim(5, 10)
    ax.set_ylim(2.5, 10.5)

    def draw_gender_pie(x, y, pie_center, r, percent, color, symbol, label_offset=(0, -1.7), rotate=False):
        ax.text(x, y, symbol, fontsize=80, ha='center', va='center', color='black')
        angle = 360 * (percent / 100)
        if not rotate:
            ax.add_patch(patches.Wedge(pie_center, r, 90, 90 - angle, color=color, zorder=5))
            ax.add_patch(patches.Wedge(pie_center, r, 90 - angle, -270, color='#f1f1f1', zorder=4))
        else:
            ax.add_patch(patches.Wedge(pie_center, r, 270, 270 - angle, color=color, zorder=5))
            ax.add_patch(patches.Wedge(pie_center, r, 270 - angle, -90, color='#f1f1f1', zorder=4))
        ax.add_patch(patches.Circle(pie_center, r, edgecolor='black', facecolor='none', linewidth=1, zorder=6))
        offset_x, offset_y = label_offset
        ax.text(x + offset_x, y + offset_y, f"{percent}%", ha='center', fontsize=8, weight='bold', color=color)

    center_x = 8

    draw_gender_pie(
        x=center_x, y=7.8, pie_center=(center_x - 0.25, 7.76), r=0.65, percent=51.2,
        color='#2262bd', symbol='\u2642', label_offset=(-1.1, 0.8)
    )
    draw_gender_pie(
        x=center_x, y=3.8, pie_center=(center_x, 4.3), r=0.65, percent=48.8,
        color='#d12e1e', symbol='\u2640', label_offset=(1.0, -0.39), rotate=True
    )

    ax.text(center_x, 6.3, 'Male\n13,854,090', ha='center', va='center', fontsize=10, weight='bold', color='#2262bd')
    ax.text(center_x, 1.85, 'Female\n13,227,202', ha='center', va='center', fontsize=10, weight='bold', color='#d12e1e')
    ax.text(center_x, 9.8, "Gender Distribution of Enrollees", fontsize=12, weight='bold', ha='center')

    buf1 = io.BytesIO()
    plt.savefig(buf1, format="png", bbox_inches='tight', pad_inches=0)
    plt.close(fig1)
    buf1.seek(0)
    encoded_1 = base64.b64encode(buf1.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_1}"



# Graph 2: Main Dashboard - Student Data No. 2 (Total Students Enrolled Per Region)
def create_enrollment_bubble_chart():
    regions = [
        ("Region I", "1,244,604"), ("Region II", "899,159"), ("Region III", "2,966,748"),
        ("Region IV-A", "3,951,663"), ("MIMAROPA", "887,334"), ("Region V", "1,733,251"),
        ("Region VI", "2,012,930"), ("Region VII", "2,106,461"), ("Region VIII", "1,219,378"),
        ("Region IX", "1,048,341"), ("Region X", "1,330,705"), ("Region XI", "1,384,153"),
        ("Region XII", "1,178,506"), ("CARAGA", "767,014"), ("BARMM", "1,061,213"),
        ("CAR", "432,266"), ("NCR", "2,834,118"), ("PSO", "23,448")
    ]

    watercolor_colors = [
        '#264653', '#287271', '#2A9D8F', '#BAB170', '#E9C46A', '#EFB306',
        '#F4A261', '#EE8959', '#E76F51', '#E63946', '#EC9A9A', '#F1FAEE',
        '#CDEAE5', '#A8DADC', '#77ABBD', '#457B9D', '#31587A', '#1D3557'
    ]

    names = [r[0] for r in regions]
    pops = [int(r[1].replace(',', '')) for r in regions]
    min_size, max_size = 20, 100
    sizes = np.interp(pops, (min(pops), max(pops)), (min_size, max_size))

    np.random.seed(42)
    positions = np.random.rand(len(regions), 2) * 0.6 + 0.2

    pso_position = [(positions[4][0] + positions[9][0]) / 2, (positions[4][1] + positions[9][1]) / 2]
    positions[16] = pso_position

    def adjust_positions(positions, sizes, max_iterations=300, min_dist_factor=1.46):
        adjusted_positions = positions.copy()
        for _ in range(max_iterations):
            overlap = False
            for i, (x1, y1) in enumerate(adjusted_positions):
                for j, (x2, y2) in enumerate(adjusted_positions):
                    if i != j:
                        dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                        min_dist = np.sqrt(sizes[i] + sizes[j]) / 100 * min_dist_factor
                        if dist < min_dist:
                            overlap = True
                            direction = np.array([x2 - x1, y2 - y1])
                            direction /= np.linalg.norm(direction)
                            displacement = (min_dist - dist) / 2
                            adjusted_positions[i] -= direction * displacement
                            adjusted_positions[j] += direction * displacement
            if not overlap:
                break
        return adjusted_positions

    adjusted_positions = adjust_positions(positions, sizes)

    text_colors = [
        'white', 'white', 'white', 'black', 'black', 'black',
        'black', 'black', 'black', 'white', 'black', 'black',
        'black', 'black', 'black', 'white', 'white', 'white'
    ]

    fig2, ax = plt.subplots(figsize=(8, 6))
    for i, ((x, y), size, color, name, pop) in enumerate(zip(adjusted_positions, sizes, watercolor_colors, names, pops)):
        radius = np.sqrt(size) / 100

        shadow = Circle((x + 0.005, y - 0.005), radius=radius * 1.03, facecolor='black', alpha=0.2, linewidth=0)
        ax.add_patch(shadow)

        circle = Circle((x, y), radius=radius, facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.9)
        ax.add_patch(circle)

        highlight = Circle((x - radius * 0.35, y + radius * 0.35), radius=radius * 0.35, facecolor='white', alpha=0.1, linewidth=0)
        ax.add_patch(highlight)

        pop_text = f"{pop:,}"
        label = f"{name}\n{pop_text}"
        ax.text(x, y, label, ha='center', va='center', fontsize=7.5, color=text_colors[i], weight='bold')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Total Students Enrolled Per Region", fontsize=16, fontweight='bold')
    plt.tight_layout()

    # Convert to base64 image
    buf2 = io.BytesIO()
    plt.savefig(buf2, format="png", bbox_inches='tight')
    plt.close(fig2)
    buf2.seek(0)
    encoded_2 = base64.b64encode(buf2.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_2}"

# Graph 3 Main Dashboard - Student Data No. 3 (Student Population by Grade Division)
fig3, ax = plt.subplots()

y_shift = -0.3

book_width = 1
book_height = 5
green_book_height = 4
blue_book_height = 3

x_positions = [1, 3, 4.19]
colors = ['#ba4141', '#1b8e3e', '#2262bd']

red_book = patches.FancyBboxPatch(
    (x_positions[0], 0 + y_shift), book_width, book_height,
    boxstyle="round,pad=0.05", linewidth=1, edgecolor='black', facecolor=colors[0])
ax.add_patch(red_book)

green_transform = transforms.Affine2D().rotate_deg_around(x_positions[1], 0 + y_shift, 12) + ax.transData
green_book = patches.FancyBboxPatch(
    (x_positions[1], 0 + y_shift), book_width, green_book_height,
    boxstyle="round,pad=0.05", linewidth=1, edgecolor='black', facecolor=colors[1],
    transform=green_transform)
ax.add_patch(green_book)

blue_book = patches.FancyBboxPatch(
    (x_positions[2], 0 + y_shift), book_width, blue_book_height,
    boxstyle="round,pad=0.05", linewidth=1, edgecolor='black', facecolor=colors[2])
ax.add_patch(blue_book)

plt.title("Student Population Distribution by Grade Division", fontsize=14, fontweight='bold')

ax.plot([x_positions[0], x_positions[0] + book_width], [book_height - 0.1 + y_shift, book_height - 0.1 + y_shift], color='#ffb2a2', linewidth=2)
ax.plot([x_positions[0], x_positions[0] + book_width], [book_height - 0.3 + y_shift, book_height - 0.3 + y_shift], color='#ffb2a2', linewidth=2)

ax.plot([x_positions[2], x_positions[2] + book_width], [blue_book_height - 0.1 + y_shift, blue_book_height - 0.1 + y_shift], color='#87ceeb', linewidth=2)
ax.plot([x_positions[2], x_positions[2] + book_width], [blue_book_height - 0.3 + y_shift, blue_book_height - 0.3 + y_shift], color='#87ceeb', linewidth=2)

green_line_transform = transforms.Affine2D().rotate_deg_around(x_positions[1], 0 + y_shift, 12) + ax.transData
ax.plot([x_positions[1], x_positions[1] + book_width],
        [green_book_height - 0.1 + y_shift, green_book_height - 0.1 + y_shift], color='#98fb09', linewidth=2, transform=green_line_transform)
ax.plot([x_positions[1], x_positions[1] + book_width],
        [green_book_height - 0.3 + y_shift, green_book_height - 0.3 + y_shift], color='#98fb09', linewidth=2, transform=green_line_transform)

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
    rect_height = 0.8
    rect_x = head_center[0] + 0.15
    rect_y = head_center[1] - rect_height / 2
    color_map = {
        x_positions[0]: '#ffb2a2',
        x_positions[1] - 0.5: '#98fb98',
        x_positions[2]: '#add8e6',}
    ax.add_patch(patches.Rectangle(
        (rect_x, rect_y), rect_width, rect_height,
        facecolor=color_map.get(x_pos, 'gray'), edgecolor='black', linewidth=0.2))

draw_stick_man(x_positions[0], book_height, book_width, 0.7)
draw_stick_man(x_positions[1] - 0.5, green_book_height, book_width, 0.7)
draw_stick_man(x_positions[2], blue_book_height, book_width, 0.7)

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

# Helper function to add text with line spacing adjustment
def add_multiline_text_with_spacing(x, y, text, ax, line_spacing=1.2, fontsize=7, color='black', fontweight='bold'):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        ax.text(x, y + i * line_spacing, line, fontsize=fontsize, color=color, va='center', ha='left', fontweight=fontweight)

# Adjusting text with line spacing
add_multiline_text_with_spacing(
    x_positions[0] + book_width / 2 + 0.2,
    book_height / 2 + y_shift + 3,
    "Elementary School\nStudents: 13,154,595\nPercentage: 52.5%",
    ax,
    line_spacing=0.2,
    fontsize=7,
    color='black',
    fontweight='bold'
)

add_multiline_text_with_spacing(
    x_positions[0] + book_width / 1 + 1.22,
    book_height / 2.12 + y_shift + 2.15,
    "Junior Highschool\nStudents: 7,749,265\nPercentage: 31%",
    ax,
    line_spacing=0.2,
    fontsize=7,
    color='black',
    fontweight='bold'
)

add_multiline_text_with_spacing(
    x_positions[2] + book_width / 2 + 0.18,
    book_height / 2.15 + y_shift + 1.2,
    "Senior Highschool\nStudents: 4,130,076\nPercentage: 16.5%",
    ax,
    line_spacing=0.2,
    fontsize=7,
    color='black',
    fontweight='bold'
)

ax.text(x_positions[0] + book_width / 2, book_height / 2 + y_shift, "Elementary School", rotation=90,
        va='center', ha='center', fontsize=10, color='white', fontweight='bold')

ax.text(x_positions[1] + book_width / 2, green_book_height / 2 + y_shift, "Junior Highschool", rotation=102,
        va='center', ha='center', fontsize=10, color='white', fontweight='bold', transform=green_transform)

ax.text(x_positions[2] + book_width / 2, blue_book_height / 2 + y_shift, "Senior Highschool", rotation=90,
        va='center', ha='center', fontsize=10, color='white', fontweight='bold')

ax.set_xlim(0, 7)
ax.set_ylim(0, 6)
ax.axis('off')
plt.gca().set_aspect('equal', adjustable='box')

# Convert to image
buf3 = io.BytesIO()
plt.savefig(buf3, format="png", bbox_inches='tight')
buf3.seek(0)
encoded_3 = base64.b64encode(buf3.read()).decode('utf-8')
buf3.close()

plt.close(fig3)

# Graph 4: Main Dashboard - School Data No. 1 (Distribution of Schools Per Region)
# Data and plotting logic (unchanged)
regions = [("Region I", 3393), ("Region II", 2916), ("Region III", 5194), ("Region IV-A", 6007),
    ("MIMAROPA", 2684), ("Region V", 4467), ("Region VI", 5037), ("Region VII", 4697),
    ("Region VIII", 4466), ("Region IX", 2868), ("Region X", 3106), ("Region XI", 2704),
    ("Region XII", 2541), ("Caraga", 2355), ("BARMM", 2932), ("CAR", 2080),
    ("NCR", 2687), ("PSO", 33)]  # PSO value set to 33

# Recalculate the total and region_percent
total = sum(val for _, val in regions)
regions_percent = [(name, val, round((val / total) * 100, 2)) for name, val in regions]
region_dict = {name: (name, val, perc) for name, val, perc in regions_percent}

# Modify rows to include PSO
rows = [[region_dict["Region I"], region_dict["Region II"], region_dict["Region III"]],
        [region_dict["Region IV-A"], region_dict["MIMAROPA"], region_dict["Region V"]],
        [region_dict["Region VI"], region_dict["Region VII"], region_dict["Region VIII"]],
        [region_dict["Region VIII"], region_dict["Region IX"], region_dict["Region X"], region_dict["Region XI"]],
        [region_dict["Region XII"], region_dict["Caraga"], region_dict["BARMM"],
         region_dict["CAR"], region_dict["NCR"], region_dict["PSO"]]]  # Keep PSO in rows

scale = 1.2
box_height = 2
spacing = 0.3
x_center = 25
y_start = 100
fixed_fontsize = 12

fig4, ax = plt.subplots(figsize=(10, 6), dpi=80)
ax.set_aspect('equal')
ax.axis('off')

roof_base_x = []
roof_base_y = []

plt.text(x_center, y_start + 3.5, "Distribution of Schools per Region",
         fontsize=18, fontweight='bold', ha='center')

colors = ['#F94449', '#5C6DC9', '#529A86', '#F1B04C']

min_x_draw = float('inf')
max_x_draw = float('-inf')

# Add label coordinates for PSO
pso_x = 0
pso_y = 0

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
    for i, (region, count, percent) in enumerate(row):
        width = percent * scale
        color = colors[i % len(colors)]
        box = patches.Rectangle((x, y), width, box_height, facecolor=color, edgecolor='black', alpha=0.9)
        ax.add_patch(box)

        # Only display label for regions that have a non-zero value
        if count > 0 and region != "PSO":
            ax.text(x + width / 2, y + box_height / 2,
                    f"{region}\n{count}",
                    ha='center', va='center',
                    fontsize=fixed_fontsize, fontweight='bold')

        # Track PSO's position to move the label to the side
        if region == "PSO":
            pso_x = x + width + 0.2  # Position to the right of the bar
            pso_y = y + box_height / 2  # Center vertically

        min_x_draw = min(min_x_draw, x)
        max_x_draw = max(max_x_draw, x + width)
        x += width + spacing

# Add triangle roof
if roof_base_x:
    roof_gap = 0.3
    triangle_top = ((roof_base_x[0] + roof_base_x[1]) / 2, roof_base_y[0] + 3 + roof_gap)
    triangle = Polygon(
        [(roof_base_x[0], roof_base_y[0] + roof_gap),
         (roof_base_x[1], roof_base_y[1] + roof_gap),
         triangle_top],
        closed=True, facecolor='#BE7158', edgecolor='black')
    ax.add_patch(triangle)

ax.set_xlim(min_x_draw - 1, max_x_draw + 1)
ax.set_ylim(last_row_y - 1, y_start + 6)

# Display PSO label on the side
ax.text(pso_x, pso_y, f"PSO\n33", ha='left', va='center', fontsize=fixed_fontsize, fontweight='bold')

plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.08)

# Convert to image
buf4 = io.BytesIO()
fig4.savefig(buf4, format="png", bbox_inches='tight')
data_4 = base64.b64encode(buf4.getbuffer()).decode("ascii")

plt.close(fig4)

# Graph 5: Main Dashboard - School Data No. 2 (School Distribution per Sector)
# Create the figure
fig5, ax = plt.subplots(figsize=(12, 6))

def draw_pencil(x_offset, color, height, label, percentage, percentage_offset, left_value, shadow_color):
    pencil_bottom = -100
    pencil_top = pencil_bottom + height
    pencil_body = patches.Rectangle((x_offset - 50, pencil_bottom), 100, height, linewidth=1, edgecolor='black', facecolor=color)
    ax.add_patch(pencil_body)

    left_line_x = x_offset - 20
    line_height = height * 0.80
    center_y = pencil_bottom + height / 2
    shadow_offset = 1.5

    ax.plot([left_line_x + shadow_offset, left_line_x + shadow_offset],
            [center_y - line_height / 2 + shadow_offset, center_y + line_height / 2 + shadow_offset],
            color=shadow_color, linewidth=1.5, alpha=0.6)

    ax.plot([left_line_x, left_line_x],
            [center_y - line_height / 2, center_y + line_height / 2],
            color='black', linewidth=1.5)

    groove_x = x_offset + 30
    split_gap = 9
    split_half = line_height / 2 - split_gap

    ax.plot([groove_x + shadow_offset, groove_x + shadow_offset],
            [center_y - split_half - split_gap + shadow_offset, center_y - split_gap + shadow_offset],
            color=shadow_color, linewidth=1.5, alpha=0.6)

    ax.plot([groove_x, groove_x],
            [center_y - split_half - split_gap, center_y - split_gap],
            color='black', linewidth=1.5)

    ax.plot([groove_x + shadow_offset, groove_x + shadow_offset],
            [center_y + split_gap + shadow_offset, center_y + split_half + split_gap + shadow_offset],
            color=shadow_color, linewidth=1.5, alpha=0.6)

    ax.plot([groove_x, groove_x],
            [center_y + split_gap, center_y + split_half + split_gap],
            color='black', linewidth=1.5)

    wood_part = patches.Polygon([(x_offset - 50, height - 100), (x_offset + 50, height - 100), (x_offset, height - 30)],
                                closed=True, facecolor='#DEB887', edgecolor='black')
    ax.add_patch(wood_part)

    tip_y = height - 30
    graphite_tip = patches.Circle((x_offset, tip_y), 5, facecolor='black', edgecolor='black')
    ax.add_patch(graphite_tip)

    eraser = patches.Rectangle((x_offset - 50, pencil_bottom), 100, 20, linewidth=1, edgecolor='black', facecolor='pink')
    ax.add_patch(eraser)

    visible_gap = 10
    line_start_y = tip_y + 5 + visible_gap
    ax.plot([x_offset, x_offset], [line_start_y, line_start_y + 45], color='black', linestyle='-', linewidth=1.5)

    label_y = pencil_bottom + 7
    ax.text(x_offset, label_y, label, ha='center', va='center', fontsize=9, color='black', fontweight="bold")

    percentage_y = -50 + height / 2 + percentage_offset
    ax.text(x_offset + 25, percentage_y, percentage, ha='left', va='center', fontsize=10, color=color, fontweight='bold')

    ax.text(x_offset - 25, line_start_y + 15, str(left_value), ha='right', va='center', fontsize=10, color=color, fontweight='bold')

# Draw pencils (same data as before)
draw_pencil(-300, '#1b8e3e', 350, 'Public', '79.45%', 230, 'Public sector\nhas 47,818\nschools', '#0a4d2c')
draw_pencil(-60, '#ffa900', 250, 'SUCs/LUCs', '0.34%', 180, 'SUCs/LUCs\nsector has\n203 schools', '#b38600')
draw_pencil(180, '#2262bd', 300, 'Private', '20.16%', 205, 'Private sector\nhas 12,133\nschools', '#0b3d91')
draw_pencil(420, '#ba4141', 200, 'PSO', '0.05%', 150, 'PSO sector\nhas 33\nschools', '#660000')

plt.title("School Distribution per Sector", fontsize=14, fontweight='bold', y=0.92)
ax.set_xlim(-450, 550)
ax.set_ylim(-150, 470)
ax.set_aspect('equal')
ax.axis('off')

# Convert to base64 PNG
buf5 = io.BytesIO()
fig5.savefig(buf5, format="png", bbox_inches='tight')
data_5 = base64.b64encode(buf5.getbuffer()).decode("ascii")

plt.close(fig5)

# Graph 6: Main Dashboard - Philippine Heatmap (Philippine Regions<br>Student Population Heatmap)
heat_map_file = r'Data/Raw_data/ANALYZED_SY_2023-2024_Schl_Level_Data_on_Official_Enrollment_13.xlsx'
heatmap_df = pd.read_excel(heat_map_file)

region_code_name = {
    "PH00": "NCR", "PH01": "Region I", "PH02": "Region II", "PH03": "Region III",
    "PH05": "Region V", "PH06": "Region VI", "PH07": "Region VII", "PH08": "Region VIII",
    "PH09": "Region IX", "PH10": "Region X", "PH11": "Region XI", "PH12": "Region XII",
    "PH13": "CARAGA", "PH14": "BARMM", "PH15": "CAR", "PH40": "Region IV-A", "PH41": "MIMAROPA"
}

school_data = heatmap_df.groupby('Region').count()
school_data = school_data["Division"].rename('Total Schools').drop(index='PSO').to_dict()

student_data = (
    heatmap_df.drop(columns=['BEIS_School_ID'])
    .groupby('Region').sum(numeric_only=True)
    .sum(axis=1).rename('Total Students')
    .drop(index='PSO')
    .to_dict()
)

student_data = dict(sorted(student_data.items(), key=lambda x: x[1], reverse=True))
school_data = dict(sorted(school_data.items(), key=lambda x: x[1], reverse=True))

name_to_code = {v: k for k, v in region_code_name.items()}

df_heatmap = pd.DataFrame({
    'RegionName': list(student_data.keys()),
    'RegionCode': [name_to_code[name] for name in student_data.keys()],
    'Student<br>Population': list(student_data.values()),
    'School Count': list(school_data.values())
})

heat_file_path = 'Data/Raw_data/ph.json'

geojson = None  # Initialize geojson to avoid NameError

if os.path.exists(heat_file_path):
    with open(heat_file_path) as f:
        geojson = json.load(f)  # Load the geojson data
else:
    print(f"Error: File not found at {heat_file_path}. Please ensure the file exists.")
    # Optionally, you can raise an exception or provide a fallback mechanism here.

# Ensure geojson is not used if it is None
if geojson is None:
    print("GeoJSON data is not available. Please check the file path and content.")

fig6 = px.choropleth_mapbox(
    df_heatmap,
    geojson=geojson,
    locations='RegionCode',
    featureidkey='properties.id',
    color='Student<br>Population',
    hover_name='RegionName',
    hover_data={'Student<br>Population': True, 'School Count': True, 'RegionCode': False},
    color_continuous_scale=[
        [0.0, '#FFFB97'],
        [0.5, '#FE7F42'],
        [1.0, '#B32C1A']
    ],
    mapbox_style='white-bg',
    center={'lat': 12.5, 'lon': 121.7},
    zoom=4.4,
    opacity=1.0,
    range_color=(0, 4000000),
    title='Philippine Regions<br>Student Population Heatmap'
)

fig6.update_traces(
    hovertemplate=(
        '<b style="color:black; font-family:Arial Black;"> %{hovertext}</b><br><br>' +
        '<b style="color:black; font-family:Arial Black;">Total Students:</b> %{customdata[0]:,}<br>' +
        '<b style="color:black; font-family:Arial Black;">Total Schools:</b> %{customdata[1]:,}<extra></extra>'
    )
)

fig6.update_layout(
    width=350, height=700,
    margin=dict(l=18, r=18, t=80, b=10),
    shapes=[dict(
        type='rect', xref='paper', yref='paper',
        x0=0, y0=0, x1=1, y1=1,
        line=dict(color='black', width=2)
    )],
    title=dict(
        x=0.5, xanchor='center',
        font=dict(size=16, family='Arial Black', color='black')
    ),
    coloraxis_colorbar=dict(
        title = dict(side="bottom"),
        title_font=dict(family='Arial Black', size=12, color='black'),
        tickfont=dict(family='Arial', size=10, color='black'),
        outlinecolor='black', outlinewidth=1,
        tickprefix=' ',
        ticks='outside',  ticklen=5,
        len=1,
        thickness=15,
        x=0.5,            # center it horizontally
        xanchor='center',
        y=-0.005,           # push it below the plot (adjust as needed)
        yanchor='top',
        orientation = 'h'

    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=13,
        font_family="Arial"
    )
)

def generate_graph7(df_school):
    df_school = load_student_data()
    # Graph 7: Student Data Analytics - Column-Bar Chart (Student Population per Grade Level by Gender)
    grade_labels = []
    male_counts = []
    female_counts = []

    for grade, columns in grade_levels.items():
        male_counts.append(df_school[columns[0]].sum())
        female_counts.append(df_school[columns[1]].sum())
        grade_labels.append(grade)

    fig7 = go.Figure()

    fig7.add_trace(go.Bar(
        x=[label for label in grade_labels],
        y=male_counts,
        name='Male',
        marker_color='#33C3FF',
        hovertemplate='<b style="color:black; font-family: Arial Black;">%{x}</b><br><b style="color:black;">Gender:</b> Male<br><b style="color:black;">Students:</b> %{y:,}<extra></extra>'

    ))


    fig7.add_trace(go.Bar(
        x=[label for label in grade_labels],
        y=female_counts,
        name='Female',
        marker_color= '#FF746C',
        hovertemplate='<b  style="color:black; font-family: Arial Black;">%{x}</b><br><b style="color:black;">Gender:</b> Female<br><b style="color:black;">Students:</b> %{y:,}<extra></extra>'
    ))

    fig7.update_layout(
        title=dict(
            text='',
            x=0.5,
            xanchor='center',
            font=dict(
                family='Arial Black',
                size=20,
                color='black'
            )
        ),
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=2)
            )
        ],
        showlegend=True,
        legend=dict(
            title=dict(text='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Gender', font=dict(size=12, family='Arial Black')),
            x=1.01,
            y=1.05,
            orientation='v',
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='black',
            borderwidth=1,
            font=dict(size=11, family='Arial')
        ),
        xaxis_title='Grade Level<br>',
        yaxis_title='<br>Student Population',
        barmode='group',
        xaxis=dict(
            title='Grade Level<br>',
            title_standoff=10,
            tickangle=45,
            tickfont=dict(size=12, family='Arial Black')
        ),
        uniformtext=dict(
            minsize=10,
            mode='show'
        ),
        yaxis=dict(
            tickformat=',',
            gridcolor='gray',
            ticklen=10,
            title_standoff=5,
            automargin=True,
            tickfont=dict(size=12, family='Arial Black'),
            tick0=20,
            ticksuffix="   "
        ),
        template='plotly_white',
        margin=dict(l=100, r=100, t=100, b=100),
        font=dict(family='Arial Black'),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )

    return fig7

def generate_graph8(df_school):
    df_school = load_student_data()
    # Graph 8: Student Data Analytics - Area Chart (Student Distribution per SHS Strand by Sector)
    sector_distribution = df_school.groupby("Sector").sum(numeric_only=True)
    sector_values = {
        strand: sector_distribution[cols].sum(axis=1)
        for strand, cols in shs_strands.items()
    }
    strand_df = pd.DataFrame(sector_values)
    strand_df.loc["SUCs/LUCs & PSO"] = strand_df.loc["SUCsLUCs"] + strand_df.loc["PSO"]
    strand_df = strand_df.drop(index=["SUCsLUCs", "PSO"])

    sector_colors = {
        "Private": ('#33C3FF', "rgba(168, 218, 220, 0.4)"),
        "Public":  ("#FF746C", "rgba(255, 178, 162, 0.4)"),
        "SUCs/LUCs & PSO": ('#2ECC71', "rgba(138, 177, 125, 0.4)")
    }

    fig8 = go.Figure()

    for sector in ["Public", "Private", "SUCs/LUCs & PSO"]:
        line_color, fill_color = sector_colors.get(sector, ("gray", "rgba(128,128,128,0.2)"))
        fig8.add_trace(go.Scatter(
            x=strand_df.columns,
            y=strand_df.loc[sector],
            mode='lines+markers',
            name=sector,
            line=dict(color=line_color, width=5),
            marker=dict(size=12, color=line_color, line=dict(color='white', width=3)),
            fill='tozeroy',
            fillcolor=fill_color,
            hovertemplate= f'<b style="color:black; font-family: Arial Black; f">{sector}</b>' + '<br><b>Strand:</b> %{x}<br><b>Students:</b> %{y:,}<extra></extra>'
        ))

    fig8.update_layout(
        title=dict(
            text='',
            x=0.5,
            xanchor='center',
            font=dict(size=20, family='Arial Black', color='black')
        ),
        xaxis=dict(
            title='SHS Strand<br>',
            title_font=dict(size=16, family='Arial Black', color='black'),
            tickmode='array',
            tickvals=strand_df.columns,
            tickangle=45,
            showgrid=True,
            gridcolor='lightgray',
            range=[-0.1, 7.1]
        ),
        yaxis=dict(
            title='<br>Number of Students<br>',
            title_font=dict(size=16, family='Arial Black', color='black'),
            showgrid=True,
            gridcolor='gray',
            rangemode='tozero',
            ticksuffix='   ',
            tickfont=dict(family='Arial Black', size=12),
            range=[-35000, strand_df.values.max() + 100000]
        ),
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=2)
            )
        ],
        legend_title="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;School Sector",
        legend=dict(
            x=0.99,
            y=0.99,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            borderwidth=1,
            title_font=dict(size=12, family='Arial Black'),
            font=dict(size=11, family="Arial")
        ),
        font=dict(family="Arial Black", size=12),
        plot_bgcolor='white',
        height=500,
        width=900,
        margin=dict(l=30, r=30, t=60, b=80),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial"
        )
    )

    return fig8

def generate_graph9(df_school):
    df_school = load_student_data()
    # Graph 9: Student Data Analytics - Donut Chart (Student Distribution by Grade Division and School Sector)
    total_students = sum(inner_values)
    outer_percentages = np.array(outer_values)
    outer_mid_angles = np.cumsum(outer_percentages) - outer_percentages / 2
    outer_mid_angles *= 360

    fig9 = go.Figure()
    colorss = ['#FF746C', '#33C3FF', '#2ECC71']


    fig9.add_trace(go.Pie(
        labels=inner_labels,
        values=inner_values,
        hole=0.55,
        textinfo="percent+label",
        textposition="inside",
        textfont=dict(family="Arial Black", size=7, color="black", weight="bold"),
        marker=dict(colors=['#33C3FF', "#FF746C", '#2ECC71'], line=dict(color='black', width=0.8)),
        hovertemplate='<b style="color: black; font-family: Arial Black;">%{label}</b><br><b style="color: black;">Students:</b> %{value:,}<extra></extra>',
        showlegend=False,
        domain=dict(x=[0, 1], y=[0.2, 0.9]),
        insidetextorientation="auto",
    ))

    fig9.add_trace(go.Pie(
        labels=outer_labels,
        values=outer_values,
        hole=0.9,
        textinfo="percent+label",
        textposition="outside",
        textfont=dict(family="Arial Black", size=7, color="black", weight="bold"),
        marker=dict(colors=['#33C3FF', "#FF746C", '#2ECC71'], line=dict(color='black', width=0.8)),
        hovertemplate="<b style='color: black; font-family: Arial Black;'>%{label}</b><br><b style='color: black;'>Total:</b> %{value:,}<extra></extra>",
        showlegend=False,
        domain=dict(x=[0, 1], y=[0.1, 1]),
        insidetextorientation="auto"
    ))

    fig9.add_annotation(
        text=f"Student Population<br>{total_students:,.0f}",
        y=0.55,
        font=dict(family="Arial Black", size=9, color="black", weight="bold"),
        showarrow=False,
        align="center"
    )

    fig9.update_layout(
        title="",
        title_font_size=20,
        title_font_weight="bold",
        title_x=0.5,
        title_y=0.95,
        height=650,
        width=650,
        xaxis=dict(tickfont=dict(family="Arial Black")),
        yaxis=dict(tickfont=dict(family="Arial Black")),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial"
        )
    )

    return fig9

def generate_graph10(df_school):
    df_school = load_school_data()

    def format_label(label):
        wrapped = "<br>".join(textwrap.wrap(label.title(), width=20))
        return f"<b>{wrapped}</b>"

    flows = df_school.groupby(['Sector', 'School_Subclassification', 'Modified_COC']).size().reset_index(name='count')

    labels_raw = pd.unique(flows[['Sector', 'School_Subclassification', 'Modified_COC']].values.ravel()).tolist()
    labels = [format_label(label) for label in labels_raw]
    label_index = {label: i for i, label in enumerate(labels_raw)}

    sector_colors_10 = {
        "Public": "rgba(255, 87, 51, 0.7)",
        "Private": "rgba(51, 195, 255, 0.7)",
        "SUCs/LUCs": "rgba(46, 204, 113, 0.7)",
        "PSO": "rgba(255, 181, 51, 0.7)",
        "Others": "rgba(200, 200, 200, 0.7)"
    }

    sources, targets, values, colors, custom_hovertext = [], [], [], [], []
    node_totals = {i: 0 for i in range(len(labels_raw))}

    for _, row in flows.iterrows():
        source = label_index[row['Sector']]
        target = label_index[row['School_Subclassification']]
        value = row['count']
        color = sector_colors_10.get(row['Sector'], "rgba(128, 128, 128, 0.4)")

        sources.append(source)
        targets.append(target)
        values.append(value)
        colors.append(color)
        node_totals[source] += value
        node_totals[target] += value

        hover = (
            f"<b style='color: black; font-family: Arial Black;'>From:</b> {row['Sector']}<br>"
            f"<b style='color: black; font-family: Arial Black;'>To:</b> {row['School_Subclassification']}<br>"
            f"<b style='color: black; font-family: Arial Black;'>Students:</b> {value:,}"
        )
        custom_hovertext.append(hover)

    for _, row in flows.iterrows():
        source = label_index[row['School_Subclassification']]
        target = label_index[row['Modified_COC']]
        value = row['count']
        color = sector_colors_10.get(row['Sector'], "rgba(128, 128, 128, 0.4)")

        sources.append(source)
        targets.append(target)
        values.append(value)
        colors.append(color)
        node_totals[source] += value
        node_totals[target] += value

        hover = (
            f"<b>From:</b> {row['School_Subclassification']}<br>"
            f"<b>To:</b> {row['Modified_COC']}<br>"
            f"<b>Students:</b> {value:,}"
        )
        custom_hovertext.append(hover)

    node_hovertext = [f"<b>{label_raw}</b><br><b>Total Students:</b> {node_totals[i]:,}" for i, label_raw in enumerate(labels_raw)]

    fig10 = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            line=dict(color="black", width=1),
            label=labels,
            color="rgba(200, 200, 200, 0.2)",
            customdata=node_hovertext,
            hovertemplate="%{customdata}<extra></extra>"
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=colors,
            customdata=custom_hovertext,
            hovertemplate="%{customdata}<extra></extra>"
        )
    )])

    fig10.update_layout(
        title=dict(text="", x=0.5, xanchor='center', font_color='black'),
        title_font_size=15,
        font_color='black',
        font_size=10,
        height=450,
        width=900,
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Arial")
    )
    return fig10

def generate_graph11(df_school):
    df_school = load_school_data()

    df_grouped = df_school.groupby(['School_Type', 'Sector']).size().reset_index(name='count')
    pivot_df = df_grouped.pivot(index='School_Type', columns='Sector', values='count').fillna(0)

    sector_colors_11 = {
        'Public': '#FF746C',
        'SUCsLUCs': '#2ECC71',
        'Private': '#33C3FF',
        'PSO': '#1D3557'
    }

    line_traces = [
        go.Scatter(
            x=pivot_df.index,
            y=pivot_df[sector],
            mode='lines+markers',
            name=sector.replace('SUCsLUCs', 'SUCs/LUCs'),
            line=dict(width=5, color=sector_colors_11[sector]),
            marker=dict(size=12, color=sector_colors_11[sector], line=dict(color='white', width=3)),
            hovertemplate=(
                "<b style='color: black; font-family: Arial Black;'>School Type:</b> %{x}<br>" +
                f"<b style='color: black; font-family: Arial Black;'>Sector:</b> {sector.replace('SUCsLUCs', 'SUCs/LUCs')}<br>" +
                "<b style='color: black; font-family: Arial Black;'>Count:</b> %{y:,}<extra></extra>"
            )
        ) for sector in pivot_df.columns
    ]

    school_counts = df_school.groupby('School_Type').size().reset_index(name='count')
    bar_trace = go.Bar(
        x=school_counts['School_Type'],
        y=school_counts['count'],
        name='Total Schools',
        marker=dict(color='#FFB533'),
        text=[f'{count:,}' for count in school_counts['count']],
        textposition='outside',
        textfont=dict(size=12, family='Arial Black', color='black'),
        hovertemplate="<b>School Type:</b> %{x}<br><b>Total Schools:</b> %{y:,}<extra></extra>"
    )

    fig11 = go.Figure(data=line_traces + [bar_trace])

    fig11.update_layout(
        title="",
        title_x=0.5,
        xaxis=dict(title='<b>School Type</b>', tickangle=45, tickfont=dict(size=12)),
        yaxis=dict(title='<b>Number of Schools</b>', tickformat=',', showgrid=True, gridcolor='gray', ticksuffix=' ', tickfont=dict(size=12, color='black')),
        height=600,
        width=900,
        showlegend=True,
        legend=dict(
            x=1.05,
            y=1,
            orientation='v',
            title=dict(text='School Categories', font=dict(size=14, family='Arial Black')),
            font=dict(size=12, color='black'),
            borderwidth=1,
            bordercolor='black',
            bgcolor='rgba(255,255,255,0.8)'
        ),
        barmode='group',
        margin=dict(l=100, r=150, t=100, b=100),
        template='plotly_white',
        shapes=[dict(type="rect", xref="paper", yref="paper", x0=0.01, y0=0, x1=1, y1=1.06, line=dict(color="black", width=2))],
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Arial")
    )
    return fig11

# Additional Functions

# Additional Functions

def plot_total_number_of_schools_by_sector():
    # Example implementation for plotting total number of schools by sector
    sector_distribution = df_school.groupby("Sector").size()
    fig, ax = plt.subplots(figsize=(8, 6))
    sector_distribution.plot(kind='bar', ax=ax, color=['#33C3FF', '#FF5733', '#2ECC71', '#FFC300'])
    ax.set_title("Total Number of Schools by Sector")
    ax.set_xlabel("Sector")
    ax.set_ylabel("Number of Schools")
    plt.tight_layout()
    return fig


def plot_total_number_of_schools_by_region():
    # Example implementation for plotting total number of schools by region
    region_distribution = df_school.groupby("Region").size()
    fig, ax = plt.subplots(figsize=(10, 6))
    region_distribution.plot(kind='bar', ax=ax, color='#1f77b4')
    ax.set_title("Total Number of Schools by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Number of Schools")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

#data comparison - gender
def create_gender_comparison_figure(selected_region):

    df_school.columns = df_school.columns.str.strip()
    df_school['Region'] = df_school['Region'].str.strip()

    region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                    'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                    'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

    grade_columns_male = [col for col in df_school.columns if 'Male' in col]
    grade_columns_female = [col for col in df_school.columns if 'Female' in col]

    if selected_region == 'All Regions':
        gender_totals_by_region = df_school.groupby('Region')[grade_columns_male + grade_columns_female].sum()
        gender_totals_by_region['Total_Male'] = gender_totals_by_region[grade_columns_male].sum(axis=1)
        gender_totals_by_region['Total_Female'] = gender_totals_by_region[grade_columns_female].sum(axis=1)
        gender_totals_by_region = gender_totals_by_region.reindex(region_order)
        gender_totals_by_region = gender_totals_by_region.dropna(subset=['Total_Male', 'Total_Female'])

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=gender_totals_by_region.index,
            y=gender_totals_by_region['Total_Male'],
            mode='lines+markers',
            name='Male',
            line=dict(color='blue', width=3),
            hovertemplate=(
                "<b>Male</b><br>"
                "<b style='color: rgb(65, 65, 65);'>Region:</b> %{x}<br>"
                "<b style='color: rgb(65, 65, 65);'>Enrollment:</b> %{y}<extra></extra>"
            ),
            hoverlabel=dict(
                bgcolor='white',
                font=dict(
                    family="Arial",
                    size=12,
                    color="black"
                )
            )
        ))

        fig.add_trace(go.Scatter(
            x=gender_totals_by_region.index,
            y=gender_totals_by_region['Total_Female'],
            mode='lines+markers',
            name='Female',
            line=dict(color='#ff2c2c', width=2, dash='dash'),
            fill='tozeroy',
            fillcolor='rgba(255, 105, 180, 0.3)', 
            hovertemplate=(
                "<b>Female</b><br>"
                "<b style='color: rgb(65, 65, 65);'>Region:</b> %{x}<br>"
                "<b style='color: rgb(65, 65, 65);'>Enrollment:</b> %{y}<extra></extra>"
            ),
            hoverlabel=dict(
                bgcolor='white',
                font=dict(
                    family="Arial",
                    size=12,
                    color="black"
                )
            )
        ))

    else:
        filtered_df = df_school[df_school['Region'] == selected_region]
        total_male = filtered_df[grade_columns_male].sum().sum()
        total_female = filtered_df[grade_columns_female].sum().sum()

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=['Male', 'Female'],
            values=[total_male, total_female],
            hole=0.3,
            textinfo='label+percent',
            marker=dict(
                colors=['#5c6dc9', '#ee6b6e'],
                line=dict(color='black', width=2)
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "<b style='color: rgb(65, 65, 65);'>Region:</b> " + selected_region + "<br>"
                "<b style='color: rgb(65, 65, 65);'>Enrollment:</b> %{value}<extra></extra>"
            ),
            hoverlabel=dict(
                bgcolor='white',
                font=dict(
                    family="Arial Black",
                    size=12,
                    color="black"
                )
            ),
            pull=[0.05, 0.05]
        ))

    fig.update_layout(
        xaxis_title='Region' if selected_region == 'All Regions' else 'Gender',
        yaxis_title='Number of Students',
        template='plotly_white',
        font=dict(family="Arial Black", size=12, color="black"),
        height=400,
        margin=dict(t=20, b=20, l=30, r=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="center",
            x=0.5
        )
    )

    return fig


#data comparison - grade level

def create_grade_level_comparison_figure(selected_region):

    df_school.columns = df_school.columns.str.strip()
    df_school['Region'] = df_school['Region'].str.strip()

    region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                    'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                    'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

    if selected_region == 'All Regions':
        df_filtered = df_school
    else:
        df_filtered = df_school[df_school['Region'] == selected_region]

    grade_totals = []
    for grade, cols in grade_levels.items():
        total = df_filtered[cols].sum().sum()
        grade_totals.append({"Grade Level": grade, "Total Students": total})

    df_grade_totals = pd.DataFrame(grade_totals)
    df_grade_totals['ColorScale'] = df_grade_totals.index

    fig = go.Figure()
    for i, row in df_grade_totals.iterrows():
        fig.add_trace(go.Bar(
            x=[row["Grade Level"]],
            y=[row["Total Students"]],
            name=row["Grade Level"],
            marker=dict(
                color=row["ColorScale"],
                colorscale="Bluered",
                cmin=df_grade_totals["ColorScale"].min(),
                cmax=df_grade_totals["ColorScale"].max(),
                line=dict(color="black", width=2)
            ),
            width=0.8,  # Slightly reduced bar width
            hovertemplate=(
                "<b>%{x}</b><br>"
                "<b style='color: rgb(65, 65, 65);'>Region:</b> " + selected_region + "<br>"
                "<b style='color: rgb(65, 65, 65);'>Students:</b> %{y}<extra></extra>"
            ),
            hoverlabel=dict(
                bgcolor='white',
                font=dict(
                    family="Arial",
                    size=12,
                    color="black"
                )
            )
        ))

    fig.update_layout(
        xaxis_title="Grade Level",
        yaxis_title="Total Students",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial Black", size=10),
        width=600,  # Reduced width
        height=350,  # Reduced height
        showlegend=True,
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=1,
                    xanchor="center",
                    x=0.5,
                    traceorder='normal',
                    itemclick='toggleothers',
                    itemsizing='constant',
                    bgcolor='rgba(255, 255, 255, 0.8)'),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=10),
            title_font=dict(size=12)),
        yaxis=dict(
            title_font=dict(size=10),
            tickfont=dict(size=8)),
        margin=dict(b=60, t=80, l=60, r=60),
        bargap=0.3  # Increased gap between bars
    )

    return fig


#data comparison - shs strand
def create_shs_strand_comparison_figure(selected_region):
    df = df_school.copy()
    df.columns = df.columns.str.strip()
    df['Region'] = df['Region'].str.strip()

    # Define SHS strands and their corresponding columns
    shs_strands = {
    "STEM": ['G11_STEM_Male', 'G11_STEM_Female', 'G12_STEM_Male', 'G12_STEM_Female'],
    "ABM": ['G11_ABM_Male', 'G11_ABM_Female', 'G12_ABM_Male', 'G12_ABM_Female'],
    "HUMSS": ['G11_HUMSS_Male', 'G11_HUMSS_Female', 'G12_HUMSS_Male', 'G12_HUMSS_Female'],
    "GAS": ['G11_GAS_Male', 'G11_GAS_Female', 'G12_GAS_Male', 'G12_GAS_Female'],
    "TVL": ['G11_TVL_Male', 'G11_TVL_Female', 'G12_TVL_Male', 'G12_TVL_Female'],
}


    if selected_region == 'All Regions':
        filtered_df = df_school
    else:
        filtered_df = df_school[df_school['Region'] == selected_region]

    shs_totals = []
    for strand, cols in shs_strands.items():
        total = filtered_df[cols].sum().sum()
        shs_totals.append({"SHS Strand": strand, "Total Students": total})

    df_shs_totals = pd.DataFrame(shs_totals)

    colors = ['#e1bbd9', '#6cc24a', '#5c6dc9', '#f1b04c', '#ee6b6e']

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=df_shs_totals['SHS Strand'],
        values=df_shs_totals['Total Students'],
        hole=0.3,
        textinfo='label+percent',
        marker=dict(
            colors=colors,
            line=dict(color='black', width=2)
        ),
        hovertemplate=(
            "<b>%{label}</b><br>"
            f"<b style='color: rgb(65, 65, 65);'>Region:</b> {selected_region}<br>"
            "<b style='color: rgb(65, 65, 65);'>Enrollment:</b> %{value}<extra></extra>"
        ),
        hoverlabel=dict(
            bgcolor='white',
            font=dict(
                family="Arial",
                size=12,
                color="black"
            )
        ),
        pull=[0.05] * len(df_shs_totals)
    ))

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
            font=dict(family="Arial", size=10)
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial Black", size=12),
        margin=dict(l=40, r=40, t=50, b=50),
        showlegend=True,
        width=500,
        height=400
    )

    return fig
#data-comparison - grade division




def create_grade_division_comparison_figure(selected_region):

    
    df_school.columns = df_school.columns.str.strip()
    df_school['Region'] = df_school['Region'].str.strip()

    grouped = df_school.groupby("Region")

    def compute_region_totals():
        data = {"Region": [], "Elementary": [], "JuniorHigh": [], "SeniorHigh": []}
        for region in region_order[1:]:
            group = grouped.get_group(region)
            data["Region"].append(region)
            data["Elementary"].append(group[elementary_male + elementary_female].sum().sum())
            data["JuniorHigh"].append(group[junior_high_male + junior_high_female].sum().sum())
            data["SeniorHigh"].append(group[senior_high_male + senior_high_female].sum().sum())
        return pd.DataFrame(data)

    df_region_totals = compute_region_totals()

    if selected_region != 'All Regions':
        df_region_totals = df_region_totals[df_region_totals['Region'] == selected_region]

    fig = go.Figure()

    if selected_region == 'All Regions':
        fig.add_trace(go.Bar(
            name='Elementary',
            x=df_region_totals['Region'],
            y=df_region_totals['Elementary'],
            marker_color='#5c6dc9',
            hovertemplate="<b>Elementary</b> <br><b>Region:</b> %{x}<br><b>Enrollment:</b> %{y}<extra></extra>",
            hoverlabel=dict(bgcolor='white')
        ))
        fig.add_trace(go.Bar(
            name='Junior High',
            x=df_region_totals['Region'],
            y=df_region_totals['JuniorHigh'],
            marker_color='#919bf1',
            hovertemplate="<b>Junior High</b> <br><b>Region:</b> %{x}<br><b>Enrollment:</b> %{y}<extra></extra>",
            hoverlabel=dict(bgcolor='white')
        ))
        fig.add_trace(go.Bar(
            name='Senior High',
            x=df_region_totals['Region'],
            y=df_region_totals['SeniorHigh'],
            marker_color='#a0aadf',
            hovertemplate="<b>Senior High</b> <br><b>Region:</b> %{x}<br><b>Enrollment:</b> %{y}<extra></extra>",
            hoverlabel=dict(bgcolor='white')
        ))

        fig.update_layout(
            xaxis_title='Region',
            yaxis_title='Enrollment',
            barmode='stack',
            font=dict(family="Arial Black", size=11),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=50, b=50),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            xaxis=dict(tickangle=20)
        )
        return fig

    else:
        region_data = df_region_totals.iloc[0]

        fig.add_trace(go.Pie(
            labels=['Elementary', 'Junior High', 'Senior High'],
            values=[region_data['Elementary'], region_data['JuniorHigh'], region_data['SeniorHigh']],
            hole=0.3,
            textinfo='label+percent',
            marker=dict(
                colors=['#5c6dc9', '#919bf1', '#a0aadf'],
                line=dict(color='black', width=2)
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                f"<b>Region:</b> {selected_region}<br>"
                "<b>Enrollment:</b> %{value}<br>"
            ),
            hoverlabel=dict(
                bgcolor='white',
                font=dict(
                    family='Arial',
                    size=12,
                    color='black'
                )
            )
        ))

        fig.update_layout(
            title=selected_region,
            title_x=0.5,
            showlegend=True,
            font=dict(family="Arial Black", size=11),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=60, r=60, t=60, b=60),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="center",
                x=0.5
            )
        )

        return fig

#data comparison sector
def create_sector_comparison_figure(selected_region):
    sector_region_data = df_school.groupby(['Region', 'Sector']).sum(numeric_only=True).reset_index()
    sector_region_data['Total'] = sector_region_data[grade_columns_male + grade_columns_female].sum(axis=1)
    sector_region_pivot = sector_region_data.pivot_table(index='Region', columns='Sector', values='Total', aggfunc='sum', fill_value=0)
    sector_region_pivot = sector_region_pivot.reindex(region_order)
    sector_region_pivot = sector_region_pivot.reset_index()

    sector_colors = ['#f1b04c', '#f94449', '#5c6dc9', '#6bb0a6']

    if selected_region != "All Regions":
        # Pie chart for specific region
        filtered_data = sector_region_pivot[sector_region_pivot['Region'] == selected_region]
        fig = go.Figure(data=[go.Pie(
            labels=filtered_data.columns[1:],
            values=filtered_data.iloc[0, 1:],
            marker=dict(
                colors=sector_colors[:len(filtered_data.columns[1:])],
                line=dict(color='black', width=2)
            ),
            textinfo='none',  # No percentage on the pie chart itself
            hovertemplate='<b>%{label}</b><br>'
                          '<span style="color: rgb(65,65,65)">Enrolled: %{value:,}</span><br>'
                          '<span style="color: rgb(65,65,65)">Percentage: %{percent}</span><extra></extra>',
            hoverlabel=dict(
                font=dict(family="Arial", color="black"),
                bgcolor="white",
                bordercolor="black"
            )
        )])
        fig.update_layout(
            font=dict(family="Arial", size=10, color="black"),
            title_font=dict(size=18, color="black"),
            width=650, height=400,
            margin=dict(l=40, r=40, t=60, b=40),
            showlegend=True,
            title=None
        )
    else:
        # Line chart for all regions
        filtered_data = sector_region_pivot
        fig = go.Figure()
        for sector in filtered_data.columns[1:]:
            fig.add_trace(go.Scatter(
                x=filtered_data['Region'], y=filtered_data[sector],
                name=sector, mode='lines+markers',
                fill='tonexty', marker=dict(size=5), line=dict(width=1.5)
            ))
        fig.update_layout(
            font=dict(family="Arial Black", size=10, color="black"),
            title_font=dict(size=18, color="black"),
            width=650, height=400,
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(
                categoryorder='array',
                categoryarray=region_order,
                tickfont=dict(color="black"),
                title_font=dict(color="black")),
            yaxis=dict(
                tickfont=dict(color="black"),
                title_font=dict(color="black")),
            hovermode="x unified",
            hoverlabel=dict(
                font=dict(family="Arial Black", color="black"),
                bgcolor="white",
                bordercolor="black"
            ),
            legend=dict(
                orientation="h", yanchor="top",
                y=1.1, xanchor="center",
                x=0.5, font=dict(color="black")),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)'
        )

    return fig

# data comparison - school type

def create_school_type_comparison_figure(selected_region):
    df_school["Total_Students"] = df_school[[
    *elementary_male, *elementary_female,
    *junior_high_male, *junior_high_female,
    *senior_high_male, *senior_high_female
    ]].sum(axis=1)

    if selected_region == "All Regions":
        filtered_df = df_school.copy()
        school_distribution = filtered_df.groupby(["Region", "School_Type"])["Total_Students"].sum().reset_index()
        school_distribution["Region"] = pd.Categorical(school_distribution["Region"], categories=region_order, ordered=True)
        school_distribution = school_distribution.sort_values("Region")

        fig = go.Figure()

        # Define a list of red shades for the bar chart
        red_shades = ["#e74c3c", "#c0392b", "#ff6f61", "#ff4d4d"]

        for school_type in school_distribution["School_Type"].unique():
            df_sub = school_distribution[school_distribution["School_Type"] == school_type]

            # Assign a color from the red_shades list
            color = red_shades[school_distribution["School_Type"].unique().tolist().index(school_type) % len(red_shades)]

            fig.add_trace(go.Bar(
                x=df_sub["Region"],  # x: Regions
                y=df_sub["Total_Students"],  # y: Number of students
                name=school_type,
                orientation="v",  # Now vertical bars
                hovertemplate=(
                    f"<b>{school_type}</b><br>"
                    "<b style='color: rgb(65, 65, 65);'>Region:</b> %{x}<br>"
                    "<b style='color: rgb(65, 65, 65);'>Students:</b> %{y}<extra></extra>"
                ),
                hoverlabel=dict(
                    bgcolor='white',
                    font=dict(
                        family="Arial",
                        size=12,
                        color="black"
                    )
                ),
                marker=dict(color=color)
            ))

        fig.update_layout(
            barmode="stack",
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1.4,
                xanchor="left",
                x=0.7,
                font=dict(size=10),
                bordercolor="white",
                borderwidth=0,
                bgcolor="white"
            ),
            title=None,
            height=400,
            width=700,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Arial Black", size=12),
            margin=dict(l=60, r=60, t=80, b=60),
            bargap=0.25,
            xaxis=dict(title="Region", categoryorder='array', categoryarray=region_order),
            yaxis=dict(title="Number of Students")
        )

    else:
        filtered_df = df_school[df_school["Region"] == selected_region]
        school_distribution = filtered_df.groupby("School_Type")["Total_Students"].sum().reset_index()

        total_students_region = school_distribution["Total_Students"].sum()

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=school_distribution["School_Type"],
            values=school_distribution["Total_Students"],
            hole=0.3,
            textinfo="percent",
            marker=dict(
                colors=["#e74c3c", "#c0392b", "#ff6f61", "#ff4d4d"],
                line=dict(color='black', width=1)
            ),
            hovertemplate=(
                "<b>%{label}</b><br>" +
                f"<b style='color: rgb(65, 65, 65);'>Region:</b> {selected_region}<br>" +
                "<b style='color: rgb(65, 65, 65);'>Students:</b> %{value}<extra></extra>"
            ),
            hoverlabel=dict(
                bgcolor='white',
                font=dict(
                    family="Arial",
                    size=12,
                    color="black"
                )
            ),
        ))

        fig.update_layout(
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=0.9,
                font=dict(size=10),
                bordercolor="white",
                borderwidth=0,
                bgcolor="white"
            ),
            title=None,
            height=400,
            width=700,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(family="Arial Black", size=12),
            margin=dict(l=60, r=60, t=80, b=60),
            xaxis=dict(title="School Type"),
            yaxis=dict(title="Total Students")
        )
    
    return fig

def get_region_list():
    # This will include all regions from region_order in the dropdown
    # regardless of whether they are present in the data.
    # Regions not in the data will show up in the dropdown but will likely
    # result in empty or zero-value graphs when selected.
    return ['All Regions'] + region_order

# Home Counter Numbers

home_numbers = pd.read_excel(heat_map_file)

total_schools_home = int(home_numbers["Region"].count())

total_students_home = int(home_numbers.sum(numeric_only=True).drop(index = 'BEIS_School_ID').sum())

highest_population_home = str(home_numbers.groupby("Region").sum(numeric_only=True).sum(axis=1).idxmax())

# Home Counter Numbers

home_numbers = pd.read_excel(heat_map_file)

total_schools_home = int(home_numbers["Region"].count())

total_students_home = int(home_numbers.sum(numeric_only=True).drop(index = 'BEIS_School_ID').sum())

highest_population_home = str(home_numbers.groupby("Region").sum(numeric_only=True).sum(axis=1).idxmax())

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
