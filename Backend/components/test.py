import pandas as pd

data = pd.read_csv(r"D:\zDonludoz\Git\Analytic-Dashboard---DBA\Data\Raw data\sample_data.csv")

print("CSV Loaded Successfully!")
print("CSV Columns:", data.columns)  # ✅ Print column names
print("First 5 Rows:\n", data.head())