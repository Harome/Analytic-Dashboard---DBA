import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np

path = r"D:\zDonludoz\Git\Analytic-Dashboard---DBA\Data\Raw data\ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)
df.head()

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

total_male = df[grade_columns_male].sum().sum()
total_female = df[grade_columns_female].sum().sum()
total_students = total_male + total_female

df_total_enrollees = pd.DataFrame({
    'Gender': ['Male', 'Female'],
    'Total Enrollees': [total_male, total_female]})

df_total_enrollees['Total Enrollees'] = df_total_enrollees['Total Enrollees'].apply(lambda x: f"{x:,}")

styled_df = df_total_enrollees.style.set_properties(**{
    'border': '1px solid black', 'text-align': 'center','background-color': '#FADADD', 'color': '#333', 'font-size': '14px'
}).set_caption(f"📍 Total Male and Female Enrollees Across All Regions<br><br> Total Students Enrolled:<br>{total_students:,}")\
.set_table_styles([
    {'selector': 'th', 'props': [('background-color', '#C1E1C1'), ('color', 'black'), ('text-align', 'center')]},
    {'selector': 'td', 'props': [('padding', '8px'), ('border', '1px solid #000801')]},
    {'selector': 'caption', 'props': [('font-size', '16px'), ('color', 'black'), ('text-align', 'center')]}])

html_path = "styled_df.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(styled_df.to_html())

print(f"Styled table saved to {html_path}. Open it in a browser to view.")