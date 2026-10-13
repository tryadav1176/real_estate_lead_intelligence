
import pandas as pd
import pytest

from src.cleaner import (
    clean_records,
    normalize_mobile,
    normalize_name,
    normalize_requirement,
    normalize_zone,
    remove_duplicates,
)


def make_record(
    name="sample person",
    mobile="9876543210",
    zone="Hadapsar",
    requirement="2BHK",
    source="synthetic-test-data",
):
    """Create a test fixture; these are not real prospect records."""
    return {
        "Prospect_Name": name,
        "Mobile_Number": mobile,
        "Target_Zone": zone,
        "Requirement": requirement,
        "Source_Channel": source,
    }


def test_name_is_normalized():
    assert normalize_name("  sample   person ") == "Sample Person"


def test_missing_name_uses_default():
    assert normalize_name("") == "Valued Prospect"
    assert normalize_name(None) == "Valued Prospect"


@pytest.mark.parametrize(
    "value, expected",
    [
        ("9876543210", "9876543210"),
        ("98765 43210", "9876543210"),
        ("+91 98765 43210", "9876543210"),
        ("919876543210", "9876543210"),
        ("(98765) 43210", "9876543210"),
    ],
)
def test_valid_mobile_formats(value, expected):
    assert normalize_mobile(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
        "12345",
        "5876543210",
        "0123456789",
        "abc9876543210xyz",
        "9876543210abc",
        "987654321",
        "98765432101",
        "+1 9876543210",
        "91987654321",
        "++++++++++",
    ],
)
def test_invalid_mobile_formats(value):
    assert normalize_mobile(value) is None


@pytest.mark.parametrize(
    "value, expected",
    [
        ("hadapsar", "Hadapsar"),
        (" HADAPSAR ", "Hadapsar"),
        ("Fursungi", "Fursungi"),
        ("fursungi", "Fursungi"),
        ("Adjacent East Pune", "Adjacent_East_Pune"),
        ("adjacent-east-pune", "Adjacent_East_Pune"),
        ("ADJACENT_EAST_PUNE", "Adjacent_East_Pune"),
        ("Unknown", None),
        ("", None),
        (None, None),
    ],
)
def test_zone_normalization(value, expected):
    assert normalize_zone(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("1bhk", "1BHK"),
        ("1 BHK", "1BHK"),
        ("2bhk", "2BHK"),
        (" 2 BHK ", "2BHK"),
        ("3BHK", "3BHK"),
        ("residential plot", "Residential Plot"),
        ("RESIDENTIAL PLOT", "Residential Plot"),
        ("plot", "Residential Plot"),
        ("4BHK", None),
        ("", None),
        (None, None),
    ],
)
def test_requirement_normalization(value, expected):
    assert normalize_requirement(value) == expected


def test_valid_record():
    df = pd.DataFrame([
        make_record(
            name="sample person",
            mobile="98765 43210",
            zone="hadapsar",
            requirement="2 bhk",
        )
    ])

    result = clean_records(df)

    assert bool(result.iloc[0]["is_valid"])
    assert result.iloc[0]["Prospect_Name"] == "Sample Person"
    assert result.iloc[0]["Mobile_Number"] == "9876543210"
    assert result.iloc[0]["Target_Zone"] == "Hadapsar"
    assert result.iloc[0]["Requirement"] == "2BHK"
    assert bool(result.iloc[0]["Mobile_Format_Valid"])


def test_invalid_record():
    df = pd.DataFrame([
        make_record(
            name="",
            mobile="12345",
            zone="Unknown",
            requirement="4BHK",
        )
    ])

    result = clean_records(df)

    assert not bool(result.iloc[0]["is_valid"])
    assert pd.isna(result.iloc[0]["Mobile_Number"])
    assert result.iloc[0]["Prospect_Name"] == "Valued Prospect"


def test_mobile_format_validity_does_not_mean_verified():
    df = pd.DataFrame([make_record(mobile="9876543210")])

    result = clean_records(df)

    assert bool(result.iloc[0]["Mobile_Format_Valid"])
    # The cleaner does not claim ownership or contact permission.
    assert "Verification_Status" not in result.columns


def test_missing_required_column_raises_error():
    df = pd.DataFrame([{
        "Prospect_Name": "Sample Person",
        "Mobile_Number": "9876543210",
    }])

    with pytest.raises(ValueError, match="Missing required columns"):
        clean_records(df)


def test_duplicate_mobile_is_removed():
    df = pd.DataFrame([
        make_record(name="Person One", mobile="9876543210"),
        make_record(
            name="Person Two",
            mobile="98765 43210",
            zone="Fursungi",
            requirement="3BHK",
        ),
    ])

    cleaned = clean_records(df)
    unique = remove_duplicates(cleaned)

    assert len(cleaned) == 2
    assert len(unique) == 1
    assert unique.iloc[0]["Prospect_Name"] == "Person One"
    assert unique.attrs["input_count"] == 2
    assert unique.attrs["invalid_count"] == 0
    assert unique.attrs["duplicate_count"] == 1
    assert unique.attrs["output_count"] == 1


def test_invalid_rows_are_excluded_from_deduplicated_output():
    df = pd.DataFrame([
        make_record(name="Valid Person", mobile="9876543210"),
        make_record(name="Invalid Person", mobile="12345"),
    ])

    cleaned = clean_records(df)
    unique = remove_duplicates(cleaned)

    assert len(unique) == 1
    assert unique.iloc[0]["Prospect_Name"] == "Valid Person"
    assert unique.attrs["invalid_count"] == 1
    assert unique.attrs["duplicate_count"] == 0


def test_remove_duplicates_requires_validation_flag():
    df = pd.DataFrame([make_record()])

    with pytest.raises(ValueError, match="is_valid"):
        remove_duplicates(df)


def test_empty_dataframe_with_required_columns():
    df = pd.DataFrame(columns=[
        "Prospect_Name",
        "Mobile_Number",
        "Target_Zone",
        "Requirement",
        "Source_Channel",
    ])

    cleaned = clean_records(df)
    unique = remove_duplicates(cleaned)

    assert len(cleaned) == 0
    assert len(unique) == 0
    assert unique.attrs["input_count"] == 0
    assert unique.attrs["invalid_count"] == 0
    assert unique.attrs["duplicate_count"] == 0
    assert unique.attrs["output_count"] == 0
