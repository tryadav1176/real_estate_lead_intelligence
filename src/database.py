
import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_FILE = PROJECT_ROOT / "data" / "processed" / "leads.db"


def get_connection():
    """Create a connection to the SQLite database."""
    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATABASE_FILE)


def initialize_database():
    """Create the leads table if it does not already exist."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Lead_Score INTEGER NOT NULL,
                Prospect_Name TEXT NOT NULL,
                Mobile_Number TEXT NOT NULL UNIQUE,
                Target_Zone TEXT NOT NULL,
                Requirement TEXT NOT NULL,
                Source_Channel TEXT NOT NULL
            )
        """)


def save_leads(df):
    """Insert new leads and skip mobile numbers already stored."""
    initialize_database()

    columns = [
        "Lead_Score",
        "Prospect_Name",
        "Mobile_Number",
        "Target_Zone",
        "Requirement",
        "Source_Channel",
    ]

    records = df[columns].to_dict(orient="records")

    with get_connection() as connection:
        connection.executemany("""
            INSERT INTO leads (
                Lead_Score,
                Prospect_Name,
                Mobile_Number,
                Target_Zone,
                Requirement,
                Source_Channel
            )
            VALUES (
                :Lead_Score,
                :Prospect_Name,
                :Mobile_Number,
                :Target_Zone,
                :Requirement,
                :Source_Channel
            )
            ON CONFLICT(Mobile_Number) DO NOTHING
        """, records)

    return len(records)


def get_leads():
    """Read all stored leads into a Pandas DataFrame."""
    initialize_database()

    with get_connection() as connection:
        return pd.read_sql_query(
            "SELECT * FROM leads ORDER BY Lead_Score DESC",
            connection,
        )


def verify_database():
    """Display the number of stored leads and their scores."""
    df = get_leads()

    print(f"\nRecords currently in database: {len(df)}")

    if not df.empty:
        print(
            df[
                [
                    "Prospect_Name",
                    "Target_Zone",
                    "Requirement",
                    "Lead_Score",
                ]
            ].to_string(index=False)
        )


if __name__ == "__main__":
    initialize_database()
    verify_database()
    print(f"Database initialized: {DATABASE_FILE}")
    print(f"Database verified: {len(get_leads())} records found.")
