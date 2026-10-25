import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

output_file = Path("data/raw/hospital_event_logs.csv")
output_file.parent.mkdir(parents=True, exist_ok=True)

pathways = [
    ["Registration", "Triage", "X-Ray", "Doctor",
     "Treatment", "Discharge"],

    ["Registration", "Triage", "Doctor",
     "Treatment", "Discharge"],

    ["Registration", "Triage", "X-Ray", "Triage",
     "Doctor", "Treatment", "Discharge"],
]

events = []
start_time = datetime(2026, 10, 5, 8, 0)

for patient_number in range(1, 21):
    case_id = f"P{patient_number:03d}"
    pathway = random.choice(pathways)

    current_time = start_time + timedelta(
        minutes=random.randint(0, 120)
    )

    for activity in pathway:
        events.append({
            "Case_ID": case_id,
            "Activity_Name": activity,
            "Timestamp": current_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        })

        current_time += timedelta(
            minutes=random.randint(5, 45)
        )

events.sort(
    key=lambda event: (
        event["Case_ID"],
        event["Timestamp"]
    )
)

with output_file.open(
    "w", newline="", encoding="utf-8"
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "Case_ID",
            "Activity_Name",
            "Timestamp"
        ]
    )
    writer.writeheader()
    writer.writerows(events)

print(f"Generated {len(events)} events.")
print(f"Output file: {output_file}")