
from pathlib import Path

import pandas as pd

from src.cleaner import clean_records, remove_duplicates
from src.scorer import score_record
from src.database import save_leads


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "sample_leads.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "cleaned_leads.csv"


def run_pipeline():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input CSV not found: {INPUT_FILE}\n"
            "Create data/raw/sample_leads.csv first."
        )

    raw_df = pd.read_csv(INPUT_FILE)
    raw_count = len(raw_df)

    cleaned_df = clean_records(raw_df)
    valid_df = cleaned_df[cleaned_df["is_valid"]].copy()
    invalid_count = raw_count - len(valid_df)

    unique_df = remove_duplicates(cleaned_df)
    duplicate_count = len(valid_df) - len(unique_df)

    unique_df["Lead_Score"] = unique_df.apply(
        lambda row: score_record(row.to_dict()), axis=1
    )

    unique_df = unique_df.sort_values(
        "Lead_Score", ascending=False
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    unique_df.to_csv(OUTPUT_FILE, index=False)

    save_leads(unique_df)
    print("Database records saved or existing duplicates skipped.")
    
    print("Pipeline completed successfully!")
    print(f"Raw records: {raw_count}")
    print(f"Invalid records: {invalid_count}")
    print(f"Duplicate records removed: {duplicate_count}")
    print(f"Final clean records: {len(unique_df)}")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_pipeline()
