import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
path = r"/Users/annmargaretteconcepcion/dba/Analytic-Dashboard---DBA/Data/Raw data/ANALYZED SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
df = pd.read_excel(path)

# Count unique districts per region
district_counts = df.groupby("Region")["District"].nunique().reset_index()
district_counts.columns = ["Region", "Total Districts"]

# Sort data by total districts
district_counts = district_counts.sort_values(by="Total Districts", ascending=False)

# Plot
plt.figure(figsize=(12, 6))
sns.barplot(data=district_counts, x="Total Districts", y="Region", palette="Blues_r")

# Titles & Labels
plt.xlabel("Total Districts", fontsize=12)
plt.ylabel("Region", fontsize=12)
plt.title("Total Districts per Region", fontsize=14, fontweight='bold')

# Show values on bars
for index, value in enumerate(district_counts["Total Districts"]):
    plt.text(value + 1, index, str(value), va='center', fontsize=10, color='black')

plt.show()
