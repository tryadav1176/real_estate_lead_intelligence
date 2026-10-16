from pathlib import Path

import pandas as pd

from src.cleaner import clean_records, remove_duplicates
from src.scorer import score_record
from src.database import save_leads


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "sample_leads.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "cleaned_leads.csv"


def run_pipeline():
    """Run normalization, validation, deduplication, scoring, and storage."""
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input CSV not found: {INPUT_FILE}\n"
            "Create data/raw/sample_leads.csv first."
        )

    # 1. Load source records.
    # Update this line in src/pipeline.py
    raw_df = pd.read_csv(
        INPUT_FILE, 
        dtype={"Mobile_Number": str, "Requirement": str, "Target_Zone": str}
    )
    raw_count = len(raw_df)

    # 2. Normalize fields and identify invalid rows.
    cleaned_df = clean_records(raw_df)
    valid_df = cleaned_df[
        cleaned_df["is_valid"].fillna(False)
    ].copy()

    invalid_count = raw_count - len(valid_df)

    # 3. Remove duplicate mobile numbers among valid records.
    unique_df = remove_duplicates(cleaned_df)
    duplicate_count = len(valid_df) - len(unique_df)

    # 4. Score only valid, deduplicated records.
    unique_df["Lead_Score"] = unique_df.apply(
        lambda row: score_record(row.to_dict()),
        axis=1,
    )

    unique_df = unique_df.sort_values(
        "Lead_Score",
        ascending=False,
    ).reset_index(drop=True)

    # 5. Save the processed CSV.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    unique_df.to_csv(OUTPUT_FILE, index=False)

    # 6. Persist records and capture actual database insertion counts.
    database_metrics = save_leads(unique_df)

    # 7. Report each stage accurately.
    print("\nPipeline completed.")
    print("Input data:", INPUT_FILE)
    print(f"Raw records: {raw_count}")
    print(f"Invalid records excluded: {invalid_count}")
    print(f"Duplicate records removed from input: {duplicate_count}")
    print(f"Clean unique records: {len(unique_df)}")
    print(f"Records inserted into database: {database_metrics['inserted_count']}")
    print(
        "Records skipped (already in database): "
        f"{database_metrics['skipped_existing_count']}"
    )
    print(
        "Invalid records rejected by database layer: "
        f"{database_metrics['invalid_count']}"
    )
    print(
        "Duplicate records within database input batch: "
        f"{database_metrics['duplicate_input_count']}"
    )
    print(f"Processed CSV: {OUTPUT_FILE}")

    # The current CSV is a processed dataset, not proof of genuine
    # prospects or permission to contact anyone.
    return {
        "raw_count": raw_count,
        "invalid_count": invalid_count,
        "duplicate_count": duplicate_count,
        "clean_count": len(unique_df),
        "database_metrics": database_metrics,
        "output_file": str(OUTPUT_FILE),
    }


if __name__ == "__main__":
    run_pipeline()