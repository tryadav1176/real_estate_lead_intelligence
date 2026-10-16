import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_FILE = PROJECT_ROOT / "data" / "processed" / "leads.db"


BASE_COLUMNS = [
    "Lead_Score",
    "Prospect_Name",
    "Mobile_Number",
    "Target_Zone",
    "Requirement",
    "Source_Channel",
]

OPTIONAL_COLUMNS = [
    "Source_Reference",
    "Intent_Evidence",
    "Verification_Status",
    "Deduplication_Status",
]


def get_connection():
    """Create a connection to the SQLite database."""
    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATABASE_FILE)


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Lead_Score INTEGER NOT NULL,
                Prospect_Name TEXT NOT NULL,
                Mobile_Number TEXT NOT NULL UNIQUE,
                Target_Zone TEXT NOT NULL,
                Requirement TEXT NOT NULL,
                Source_Channel TEXT NOT NULL,
                Source_Reference TEXT,
                Intent_Evidence TEXT,
                Intent_Type TEXT NOT NULL DEFAULT 'unknown', -- ADD THIS COLUMN
                Verification_Status TEXT NOT NULL DEFAULT 'Not verified',
                Deduplication_Status TEXT NOT NULL DEFAULT 'Unique'
            )
        """)

        # Add Intent_Type to the migrations list
        migrations = {
            "Source_Reference": "TEXT",
            "Intent_Evidence": "TEXT",
            "Intent_Type": "TEXT NOT NULL DEFAULT 'unknown'", # ADD THIS MIGRATION
            "Verification_Status": "TEXT NOT NULL DEFAULT 'Not verified'",
            "Deduplication_Status": "TEXT NOT NULL DEFAULT 'Unique'",
        }
        
        # SQLite CREATE TABLE IF NOT EXISTS does not update an existing
        # table. Add new fields individually for existing databases.
        existing_columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(leads)"
            ).fetchall()
        }

        migrations = {
            "Source_Reference": "TEXT",
            "Intent_Evidence": "TEXT",
            "Verification_Status": (
                "TEXT NOT NULL DEFAULT 'Not verified'"
            ),
            "Deduplication_Status": (
                "TEXT NOT NULL DEFAULT 'Unique'"
            ),
        }

        for column, sql_type in migrations.items():
            if column not in existing_columns:
                connection.execute(
                    f"ALTER TABLE leads ADD COLUMN {column} {sql_type}"
                )


def save_leads(df):
    """
    Insert valid new leads and return accurate insertion metrics.

    Invalid rows are not saved. Existing mobile numbers are skipped.
    A 10-digit format check is performed here as a defensive safeguard;
    this does not verify ownership, consent, or contact eligibility.
    """
    initialize_database()

    required_columns = set(BASE_COLUMNS)
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if df.empty:
        return {
            "input_count": 0,
            "invalid_count": 0,
            "duplicate_input_count": 0,
            "inserted_count": 0,
            "skipped_existing_count": 0,
            "rejected_count": 0,
        }

    records_df = df.copy()

    # Require explicit validation when provided by clean_records().
    if "is_valid" in records_df.columns:
        valid_mask = records_df["is_valid"].fillna(False).astype(bool)
    else:
        valid_mask = pd.Series(True, index=records_df.index)

    # Defensively validate mobile formatting again at the persistence layer.
    mobile_mask = records_df["Mobile_Number"].apply(
        lambda value: (
            isinstance(value, str)
            and len(value) == 10
            and value.isascii()
            and value.isdigit()
            and value[0] in "6789"
        )
    )

    invalid_mask = ~valid_mask | ~mobile_mask
    invalid_count = int(invalid_mask.sum())

    valid_df = records_df.loc[~invalid_mask].copy()

    # Count duplicate mobile numbers within this input batch. Keep the
    # first valid occurrence; existing database records are counted later.
    duplicate_input_mask = valid_df.duplicated(
        subset=["Mobile_Number"],
        keep="first",
    )
    duplicate_input_count = int(duplicate_input_mask.sum())

    unique_df = valid_df.loc[~duplicate_input_mask].copy()

    # Supply explicit defaults for optional fields without claiming
    # that source evidence or contact permission has been verified.
    defaults = {
        "Source_Reference": None,
        "Intent_Evidence": None,
        "Verification_Status": "Not verified",
        "Deduplication_Status": "Unique",
    }

    for column, default in defaults.items():
        if column not in unique_df.columns:
            unique_df[column] = default

    columns = BASE_COLUMNS + OPTIONAL_COLUMNS
    records = unique_df[columns].to_dict(orient="records")

    inserted_count = 0
    skipped_existing_count = 0

    with get_connection() as connection:
        for record in records:
            cursor = connection.execute("""
                INSERT INTO leads (
                    Lead_Score,
                    Prospect_Name,
                    Mobile_Number,
                    Target_Zone,
                    Requirement,
                    Source_Channel,
                    Source_Reference,
                    Intent_Evidence,
                    Verification_Status,
                    Deduplication_Status
                )
                VALUES (
                    :Lead_Score,
                    :Prospect_Name,
                    :Mobile_Number,
                    :Target_Zone,
                    :Requirement,
                    :Source_Channel,
                    :Source_Reference,
                    :Intent_Evidence,
                    :Verification_Status,
                    :Deduplication_Status
                )
                ON CONFLICT(Mobile_Number) DO NOTHING
            """, record)

            if cursor.rowcount == 1:
                inserted_count += 1
            else:
                skipped_existing_count += 1

    return {
        "input_count": len(records_df),
        "invalid_count": invalid_count,
        "duplicate_input_count": duplicate_input_count,
        "inserted_count": inserted_count,
        "skipped_existing_count": skipped_existing_count,
        "rejected_count": (
            invalid_count
            + duplicate_input_count
            + skipped_existing_count
        ),
    }


def get_leads():
    """Read all stored leads into a Pandas DataFrame."""
    initialize_database()

    with get_connection() as connection:
        return pd.read_sql_query(
            "SELECT * FROM leads ORDER BY Lead_Score DESC",
            connection,
        )


def verify_database():
    """Display stored record counts and lead scores."""
    df = get_leads()

    print(f"\nRecords currently in database: {len(df)}")

    if not df.empty:
        display_columns = [
            "Prospect_Name",
            "Target_Zone",
            "Requirement",
            "Lead_Score",
        ]

        print(df[display_columns].to_string(index=False))


if __name__ == "__main__":
    initialize_database()
    verify_database()
    print(f"Database initialized: {DATABASE_FILE}")
    print(f"Database verified: {len(get_leads())} records found.")
