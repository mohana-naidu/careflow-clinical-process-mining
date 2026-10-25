import pandas as pd
from pathlib import Path

# Load the generated hospital event log

file_path = Path("data/raw/hospital_event_logs.csv")
df = pd.read_csv(file_path)

# Convert Timestamp column into datetime format

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# 1. Display first five records

print("\n--- First 5 Events ---")
print(df.head())

# 2. Display dataset information

print("\n--- Dataset Information ---")
print("Total events:", len(df))
print("Total patient cases:", df["Case_ID"].nunique())
print("Unique activities:", df["Activity_Name"].nunique())

# 3. Count each activity

print("\n--- Activity Counts ---")
print(df["Activity_Name"].value_counts())

# 4. Show activities for each patient

print("\n--- Patient Journey ---")
for case_id, group in df.groupby("Case_ID"):
    activities = group.sort_values("Timestamp")["Activity_Name"]
print(case_id, " -> ".join(activities))

# 5. Check missing values

print("\n--- Missing Values ---")
print(df.isnull().sum())
