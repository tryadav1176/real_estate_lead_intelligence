
import pandas as pd
import pytest

from src.cleaner import (
    clean_records,
    normalize_mobile,
    normalize_name,
    remove_duplicates,
)


def test_name_is_normalized():
    assert normalize_name("  sample person ") == "Sample Person"


def test_missing_name_uses_default():
    assert normalize_name("") == "Valued Prospect"


def test_valid_mobile_number():
    assert normalize_mobile("98765 43210") == "9876543210"


def test_invalid_mobile_number():
    assert normalize_mobile("12345") is None


def test_valid_record():
    df = pd.DataFrame([{
        "Prospect_Name": "sample person",
        "Mobile_Number": "9876543210",
        "Target_Zone": "hadapsar",
        "Requirement": "2bhk",
        "Source_Channel": "synthetic-test-data",
    }])

    result = clean_records(df)

    assert result.iloc[0]["is_valid"] == True
    assert result.iloc[0]["Target_Zone"] == "Hadapsar"
    assert result.iloc[0]["Requirement"] == "2BHK"


def test_invalid_record():
    df = pd.DataFrame([{
        "Prospect_Name": "",
        "Mobile_Number": "12345",
        "Target_Zone": "Unknown",
        "Requirement": "4BHK",
        "Source_Channel": "synthetic-test-data",
    }])

    result = clean_records(df)

    assert result.iloc[0]["is_valid"] == False

def test_duplicate_mobile_is_removed():
    df = pd.DataFrame([
        {
            "Prospect_Name": "Person One",
            "Mobile_Number": "9876543210",
            "Target_Zone": "Hadapsar",
            "Requirement": "2BHK",
            "Source_Channel": "synthetic-test-data",
        },
        {
            "Prospect_Name": "Person Two",
            "Mobile_Number": "9876543210",
            "Target_Zone": "Fursungi",
            "Requirement": "3BHK",
            "Source_Channel": "synthetic-test-data",
        },
    ])

    cleaned = clean_records(df)
    unique = remove_duplicates(cleaned)

    assert len(cleaned) == 2
    assert len(unique) == 1