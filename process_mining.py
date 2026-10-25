
import pandas as pd
from pathlib import Path

def main():
    # Step 1: Define input and output paths
    input_file = Path("data/raw/hospital_event_logs.csv")
    output_dir = Path("data/processed")

    # Step 2: Check whether the CSV file exists
    if not input_file.exists():
        print("ERROR: Hospital event log file not found.")
        print("Expected location:", input_file.resolve())
        return

    # Step 3: Load the dataset
    df = pd.read_csv(input_file)

    # Step 4: Validate required columns
    required_columns = [
        "Case_ID",
        "Activity_Name",
        "Timestamp"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("ERROR: Missing required columns:", missing_columns)
        print("Available columns:", list(df.columns))
        return

    # Step 5: Convert timestamps
    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"], errors="coerce"
    )

    df = df.dropna(subset=["Timestamp"])

    # Step 6: Sort event logs
    df = df.sort_values(
        by=["Case_ID", "Timestamp"]
    )

    # Step 7: Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 8: Save processed dataset
    output_file = output_dir / "processed_event_logs.csv"
    df.to_csv(output_file, index=False)

    print("SUCCESS: Event logs processed.")
    print("Total records:", len(df))
    print("Output file:", output_file.resolve())
    print(df.head())

if __name__ == "__main__":
    main()