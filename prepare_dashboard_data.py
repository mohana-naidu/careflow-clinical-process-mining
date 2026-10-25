
import pandas as pd
from pathlib import Path

def main():
    input_file = Path("data/raw/hospital_event_logs.csv")
    output_dir = Path("data/processed")

    # Step 1: Check whether the input file exists
    if not input_file.exists():
        print("ERROR: Input CSV file not found.")
        print("Expected location:", input_file.resolve())
        print("Please check the data/raw folder.")
        return

    # Step 2: Read the CSV file
    try:
        df = pd.read_csv(input_file)
    except Exception as error:
        print("ERROR: Could not read the CSV file.")
        print(type(error).__name__ + ":", str(error))
        return

    # Step 3: Check required columns
    required_columns = [
        "Case_ID",
        "Activity_Name",
        "Timestamp"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("ERROR: Required columns are missing:", missing_columns)
        print("Available columns:", list(df.columns))
        return

    # Step 4: Clean and prepare the data
    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Case_ID", "Activity_Name", "Timestamp"]
    )

    df = df.sort_values(
        ["Case_ID", "Timestamp"]
    ).copy()

    if df.empty:
        print("ERROR: No valid event records found.")
        return

    # Step 5: Find the next activity for each case
    df["Next_Activity"] = (
        df.groupby("Case_ID")["Activity_Name"].shift(-1)
    )

    df["Next_Timestamp"] = (
        df.groupby("Case_ID")["Timestamp"].shift(-1)
    )

    # Step 6: Calculate elapsed minutes between activities
    df["Minutes_To_Next_Activity"] = (
        df["Next_Timestamp"] - df["Timestamp"]
    ).dt.total_seconds() / 60

    transitions = df.dropna(
        subset=["Next_Activity", "Next_Timestamp"]
    ).copy()

    if transitions.empty:
        print("ERROR: No activity transitions found.")
        return

    # Step 7: Create a transition summary
    summary = (
        transitions.groupby(
            ["Activity_Name", "Next_Activity"]
        )["Minutes_To_Next_Activity"]
        .agg(
            Transition_Count="count",
            Average_Minutes="mean",
            Maximum_Minutes="max"
        )
        .reset_index()
        .round(2)
        .sort_values(
            "Average_Minutes",
            ascending=False
        )
    )

    # Step 8: Create the output folder
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Step 9: Save the output CSV files
    transition_file = (
        output_dir / "dashboard_transitions.csv"
    )

    summary_file = (
        output_dir / "dashboard_summary.csv"
    )

    try:
        transitions.to_csv(
            transition_file,
            index=False
        )

        summary.to_csv(
            summary_file,
            index=False
        )

    except Exception as error:
        print("ERROR: Could not save the output files.")
        print(type(error).__name__ + ":", str(error))
        return

    # Step 10: Display the results
    print("\n--- CareFlow Dashboard Data Summary ---")
    print("Total valid events:", len(df))
    print("Total patient cases:", df["Case_ID"].nunique())
    print("Total activity transitions:", len(transitions))
    print("Unique transition types:", len(summary))

    print("\nFiles created successfully:")
    print(transition_file.resolve())
    print(summary_file.resolve())

if __name__ == "__main__":
    main()