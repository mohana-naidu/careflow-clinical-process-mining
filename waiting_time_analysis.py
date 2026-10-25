import pandas as pd
from pathlib import Path

# Load event log data

file_path = Path("data/raw/hospital_event_logs.csv")
df = pd.read_csv(file_path)

# Convert timestamps to datetime

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sort events by patient and time

df = df.sort_values(["Case_ID", "Timestamp"]).copy()

# Get the next activity and its timestamp for each patient

df["Next_Activity"] = (
df.groupby("Case_ID")["Activity_Name"].shift(-1)
)

df["Next_Timestamp"] = (
df.groupby("Case_ID")["Timestamp"].shift(-1)
)

# Calculate time until the next recorded activity

df["Minutes_To_Next_Activity"] = (
df["Next_Timestamp"] - df["Timestamp"]
).dt.total_seconds() / 60

# Remove final activities that have no next event

transitions = df.dropna(subset=["Next_Activity"]).copy()

print("\n--- Patient Activity Transitions ---")
print(
transitions[
[
"Case_ID",
"Activity_Name",
"Next_Activity",
"Minutes_To_Next_Activity",
]
].head(15).to_string(index=False)
)

# Average time between each activity and the next one

print("\n--- Average Time Between Activities (Minutes) ---")

summary = (
transitions.groupby(
["Activity_Name", "Next_Activity"]
)["Minutes_To_Next_Activity"]
.agg(["count", "mean", "max"])
.round(2)
.sort_values("mean", ascending=False)
)

print(summary)

# Save the transition data for further analysis

output_file = Path("data/processed/activity_waiting_times.csv")
output_file.parent.mkdir(parents=True, exist_ok=True)

transitions.to_csv(output_file, index=False)

print(f"\nSaved transition analysis to: {output_file}")
