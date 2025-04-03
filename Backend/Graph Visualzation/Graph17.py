import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = r"/Users/annmargaretteconcepcion/dba/Analytic-Dashboard---DBA/Data/Raw data/ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)
region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

school_distribution = df.groupby(["Region", "District"]).size().unstack(fill_value=0)

school_distribution = school_distribution.reindex(region_order)

fig, ax = plt.subplots(figsize=(12, 6))

school_distribution.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')

ax.set_xlabel("Region")
ax.set_ylabel("Number of Schools")
ax.set_title("School Distribution Based on District per Region")
ax.legend(title="District", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle="--", alpha=0.7)

plt.show()