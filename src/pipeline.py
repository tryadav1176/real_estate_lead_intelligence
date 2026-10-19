from pathlib import Path
import pandas as pd

from src.cleaner import clean_records, remove_duplicates
from src.scorer import score_record
from src.database import save_leads, get_leads
from src.adapter import SimulatedOptInAdapter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "simulated_opt_in_leads.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "final_exported_leads.csv"

def run_pipeline():
    # 1. Ingest via Adapter
    adapter = SimulatedOptInAdapter(INPUT_FILE)
    raw_df = adapter.fetch_data()
    raw_count = len(raw_df)

    # 2. Normalize & Clean
    cleaned_df = clean_records(raw_df)
    
    # 3. Deduplicate
    unique_df = remove_duplicates(cleaned_df)
    
    # 4. Score & Classify (Intent logic applied here)
    unique_df["Lead_Score"] = unique_df.apply(lambda row: score_record(row.to_dict()), axis=1)
    
    # 5. Persist to Database
    database_metrics = save_leads(unique_df)
    
    # 6. Export Automation: Pull verified records from DB to final CSV
    final_db_extract = get_leads()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    final_db_extract.to_csv(OUTPUT_FILE, index=False)

    print("\n--- Day 6 Pipeline Integration Complete ---")
    print(f"Raw records ingested via Adapter: {raw_count}")
    print(f"Records inserted into database: {database_metrics['inserted_count']}")
    print(f"Export Automation Complete: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_pipeline()