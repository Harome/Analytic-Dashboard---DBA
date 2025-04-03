import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = r"/Users/annmargaretteconcepcion/dba/Analytic-Dashboard---DBA/Data/Raw data/ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)

region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

school_distribution = df.groupby(["Region", "Sector"]).size().unstack(fill_value=0)

school_distribution = school_distribution.reindex(region_order)

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['blue', 'green', 'red', 'purple']

school_distribution.plot(kind='barh', stacked=True, color=colors, ax=ax)
ax.set_xlabel("Number of Schools")
ax.set_ylabel("Region")
ax.set_title("School Distribution Based on Sector per Region")
ax.legend(title="Sector")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()