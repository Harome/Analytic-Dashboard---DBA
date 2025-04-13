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

elementary_male = ["G1_Male", "G2_Male", "G3_Male", "G4_Male", "G5_Male", "G6_Male", "Elem_NG_Male"]
elementary_female = ["G1_Female", "G2_Female", "G3_Female", "G4_Female", "G5_Female", "G6_Female", "Elem_NG_Female"]

junior_high_male = ["G7_Male", "G8_Male", "G9_Male", "G10_Male", "JHS_NG_Male"]
junior_high_female = ["G7_Female", "G8_Female", "G9_Female", "G10_Female", "JHS_NG_Female"]

senior_high_male = ["G11_ABM_Male", "G11_HUMSS_Male", "G11_STEM_Male", "G11_GAS_Male","G11_PBM_Male", "G11_TVL_Male", "G11_SPORTS_Male", "G11_ARTS_Male",
                    "G12_ABM_Male", "G12_HUMSS_Male", "G12_STEM_Male", "G12_GAS_Male","G12_PBM_Male", "G12_TVL_Male", "G12_SPORTS_Male", "G12_ARTS_Male"]
senior_high_female = ["G11_ABM_Female", "G11_HUMSS_Female", "G11_STEM_Female", "G11_GAS_Female", "G11_PBM_Female", "G11_TVL_Female", "G11_SPORTS_Female", "G11_ARTS_Female",
                      "G12_ABM_Female", "G12_HUMSS_Female", "G12_STEM_Female", "G12_GAS_Female", "G12_PBM_Female", "G12_TVL_Female", "G12_SPORTS_Female", "G12_ARTS_Female"]

region_population = df.groupby("Region").sum(numeric_only=True)
region_population["Elementary_Total"] = region_population[elementary_male].sum(axis=1) + region_population[elementary_female].sum(axis=1)
region_population["Junior_HS_Total"] = region_population[junior_high_male].sum(axis=1) + region_population[junior_high_female].sum(axis=1)
region_population["Senior_HS_Total"] = region_population[senior_high_male].sum(axis=1) + region_population[senior_high_female].sum(axis=1)

region_population_totals = region_population[["Elementary_Total", "Junior_HS_Total", "Senior_HS_Total"]]

fig, ax = plt.subplots(figsize=(10, 8))
region_population_totals.plot(kind="barh", colormap="plasma", edgecolor="black", ax=ax)
plt.title("Student Population per Grade Division by Region")
plt.ylabel("Region")
plt.xlabel("Total Student Population")
plt.legend(title="Education Level")
plt.grid(axis="x", linestyle="--", alpha=0.7)

def format_func(value, tick_number):
    return f"{int(value)}"
ax.xaxis.set_major_formatter(plt.FuncFormatter(format_func))

plt.show()