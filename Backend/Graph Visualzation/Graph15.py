
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = r"/Users/annmargaretteconcepcion/dba/Analytic-Dashboard---DBA/Data/Raw data/ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)
region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']
school_distribution = df.groupby(["Region", "Modified_COC"]).size().unstack(fill_value=0)

school_distribution = school_distribution.reindex(region_order)

fig, ax = plt.subplots(figsize=(8, 8))
colors = plt.cm.tab20.colors[:len(school_distribution)]  # Define colors

wedges, texts = ax.pie(school_distribution.sum(axis=1), labels=school_distribution.index,
       startangle=140, colors=colors, wedgeprops={'edgecolor': 'white'})

centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

plt.title("School Distribution Based on Modified COC per Region")
plt.show()