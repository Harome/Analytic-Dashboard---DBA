import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = r"/Users/annmargaretteconcepcion/dba/Analytic-Dashboard---DBA/Data/Raw data/ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)
region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

school_distribution = df.groupby(["Region", "School_Subclassification"]).size().unstack(fill_value=0)

school_distribution = school_distribution.reindex(region_order)

fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.get_cmap("tab10", len(school_distribution.columns)).colors  

school_distribution.plot(kind='bar', stacked=True, color=colors, ax=ax)
ax.set_xticklabels(school_distribution.index, rotation=45, ha="right")
ax.set_ylabel("Number of Schools")
ax.set_xlabel("Region")
ax.set_title("School Distribution Based on Subclassification per Region")
ax.legend(title="School Subclassification", loc='upper right')
plt.grid(axis='y', linestyle="--", alpha=0.6)
plt.show()