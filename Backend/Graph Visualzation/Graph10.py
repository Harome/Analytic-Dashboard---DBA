import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

# Renaming columns to ensure there are no leading/trailing spaces
path = r"/Users/annmargaretteconcepcion/dba/Analytic-Dashboard---DBA/Data/Raw data/ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)
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

# Summing male and female student population by region and sector
df_sector_population = df.groupby(['Region', 'Sector'])[[*grade_columns_male, *grade_columns_female]].sum()
df_sector_population['Total Population'] = df_sector_population.sum(axis=1)
df_sector_population = df_sector_population.reset_index()

# Pivot the data to have regions as the index and sectors as columns
df_pivot = df_sector_population.pivot(index='Region', columns='Sector', values='Total Population')
df_pivot = df_pivot.reindex(region_order)

# Plot the data
plt.figure(figsize=(10, 6))

# Create a stacked line plot by plotting each sector as a separate line
for sector in df_pivot.columns:
    plt.plot(df_pivot.index, df_pivot[sector], marker='o', linestyle='-', label=sector)

# Adding titles and labels
plt.xlabel("Region", fontsize=14)
plt.ylabel("Total Student Population", fontsize=14)
plt.title("Student Population per Sector in Each Region", fontsize=16, fontweight='bold')

# Rotate the x-axis labels for better visibility
plt.xticks(rotation=45, ha='right', fontsize=12)

# Format the y-axis to show numbers with commas
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Add a legend to the plot
plt.legend(title="Sector", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

# Adding gridlines for better readability
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Show the plot
plt.tight_layout()  # Ensures that labels and title do not overlap
plt.show()
