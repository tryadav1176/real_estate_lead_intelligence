
import sqlite3

import pandas as pd
import pytest

import src.database as database
from src.cleaner import clean_records


@pytest.fixture
def temporary_database(tmp_path, monkeypatch):
    """Use an isolated database for each test."""
    db_path = tmp_path / "test_leads.db"
    monkeypatch.setattr(database, "DATABASE_FILE", db_path)
    database.initialize_database()
    return db_path


def make_leads(
    mobiles=None,
    source="synthetic-test-data",
):
    """Build synthetic records for database tests."""
    if mobiles is None:
        mobiles = ["9876543210"]

    records = []

    for index, mobile in enumerate(mobiles):
        records.append({
            "Lead_Score": 75,
            "Prospect_Name": f"Sample Person {index + 1}",
            "Mobile_Number": mobile,
            "Target_Zone": "Hadapsar",
            "Requirement": "2BHK",
            "Source_Channel": source,
            "Source_Reference": "synthetic-fixture",
            "Intent_Evidence": "Synthetic test record only",
            "Verification_Status": "Not verified",
            "Deduplication_Status": "Unique",
        })

    return pd.DataFrame(records)


def test_database_initialization(temporary_database):
    """The expected database schema should be created."""
    assert temporary_database.exists()

    with sqlite3.connect(temporary_database) as connection:
        columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(leads)"
            )
        }

    assert {
        "id",
        "Lead_Score",
        "Prospect_Name",
        "Mobile_Number",
        "Target_Zone",
        "Requirement",
        "Source_Channel",
        "Source_Reference",
        "Intent_Evidence",
        "Verification_Status",
        "Deduplication_Status",
    }.issubset(columns)


def test_insert_one_record(temporary_database):
    """A new valid record should be inserted once."""
    df = make_leads()

    metrics = database.save_leads(df)

    assert metrics["input_count"] == 1
    assert metrics["inserted_count"] == 1
    assert metrics["skipped_existing_count"] == 0
    assert metrics["rejected_count"] == 0
    assert len(database.get_leads()) == 1


def test_existing_record_is_skipped(temporary_database):
    """A repeated mobile should not create a second DB row."""
    df = make_leads()

    first = database.save_leads(df)
    second = database.save_leads(df)

    assert first["inserted_count"] == 1
    assert second["inserted_count"] == 0
    assert second["skipped_existing_count"] == 1
    assert second["rejected_count"] == 1
    assert len(database.get_leads()) == 1


def test_duplicate_numbers_within_input_batch(
    temporary_database,
):
    """Duplicates in the same batch should be counted."""
    df = make_leads([
        "9876543210",
        "9876543210",
        "8765432109",
    ])

    metrics = database.save_leads(df)

    assert metrics["input_count"] == 3
    assert metrics["duplicate_input_count"] == 1
    assert metrics["inserted_count"] == 2
    assert metrics["rejected_count"] == 1
    assert len(database.get_leads()) == 2


def test_invalid_mobile_is_rejected(temporary_database):
    """Invalid mobile formats must not enter the database."""
    df = make_leads([
        "9876543210",
        "12345",
        "abc9876543210xyz",
        "5876543210",
    ])

    metrics = database.save_leads(df)

    assert metrics["input_count"] == 4
    assert metrics["invalid_count"] == 3
    assert metrics["inserted_count"] == 1
    assert metrics["rejected_count"] == 3
    assert len(database.get_leads()) == 1


def test_cleaner_invalid_flag_is_respected(
    temporary_database,
):
    """Rows marked invalid by the cleaner should be rejected."""
    df = make_leads(["9876543210", "8765432109"])

    df.loc[1, "Requirement"] = "4BHK"

    cleaned = clean_records(df)
    cleaned["Lead_Score"] = 75

    metrics = database.save_leads(cleaned)

    assert metrics["input_count"] == 2
    assert metrics["invalid_count"] == 1
    assert metrics["inserted_count"] == 1
    assert len(database.get_leads()) == 1


def test_missing_required_columns_raises_error(
    temporary_database,
):
    """Required fields cannot be omitted."""
    df = pd.DataFrame([{
        "Prospect_Name": "Sample Person",
        "Mobile_Number": "9876543210",
    }])

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        database.save_leads(df)


def test_empty_dataframe(temporary_database):
    """An empty valid input should produce zero counts."""
    df = make_leads().iloc[0:0]

    metrics = database.save_leads(df)

    assert metrics["input_count"] == 0
    assert metrics["inserted_count"] == 0
    assert metrics["invalid_count"] == 0
    assert metrics["rejected_count"] == 0


def test_optional_fields_receive_defaults(
    temporary_database,
):
    """Missing evidence fields must not be fabricated."""
    df = make_leads().drop(columns=[
        "Source_Reference",
        "Intent_Evidence",
        "Verification_Status",
        "Deduplication_Status",
    ])

    metrics = database.save_leads(df)
    stored = database.get_leads()

    assert metrics["inserted_count"] == 1
    assert pd.isna(stored.iloc[0]["Source_Reference"])
    assert pd.isna(stored.iloc[0]["Intent_Evidence"])
    assert stored.iloc[0]["Verification_Status"] == "Not verified"
    assert stored.iloc[0]["Deduplication_Status"] == "Unique"


def test_existing_database_migration(
    temporary_database,
):
    """Older database schemas should receive the new columns."""
    with sqlite3.connect(temporary_database) as connection:
        connection.execute("DROP TABLE leads")
        connection.execute("""
            CREATE TABLE leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Lead_Score INTEGER NOT NULL,
                Prospect_Name TEXT NOT NULL,
                Mobile_Number TEXT NOT NULL UNIQUE,
                Target_Zone TEXT NOT NULL,
                Requirement TEXT NOT NULL,
                Source_Channel TEXT NOT NULL
            )
        """)

    database.initialize_database()

    with sqlite3.connect(temporary_database) as connection:
        columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(leads)"
            )
        }

    assert "Source_Reference" in columns
    assert "Intent_Evidence" in columns
    assert "Verification_Status" in columns
    assert "Deduplication_Status" in columns


def test_get_leads_sorted_by_score(temporary_database):
    """Higher-scored records should appear first."""
    df = make_leads(["9876543210", "8765432109"])
    df.loc[0, "Lead_Score"] = 55
    df.loc[1, "Lead_Score"] = 90

    database.save_leads(df)
    stored = database.get_leads()

    assert stored["Lead_Score"].tolist() == [90, 55]
