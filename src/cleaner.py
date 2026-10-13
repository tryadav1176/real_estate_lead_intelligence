import re
import pandas as pd

VALID_ZONES = {
    "Hadapsar",
    "Fursungi",
    "Adjacent_East_Pune",
}

VALID_REQUIREMENTS = {
    "1BHK",
    "2BHK",
    "3BHK",
    "Residential Plot",
}

# Deliberately strict: accepting a 10-digit number, or a 91-prefixed
# 12-digit number. Do not accept arbitrary text around the number.

MOBILE_PATTERN = re.compile(r"[6-9]\d{9}")
MOBILE_WITH_COUNTRY_CODE_PATTERN = re.compile(r"91[6-9]\d{9}")

def is_missing(value):
    """Return True for None, NaN, pandas NA, or Blank strings."""
    if value is None:
        return True
    try:
        if pd.isna(value):
            return True
    except (TypeError, ValueError):
        pass
    return isinstance(value, str) and not value.strip()

def normalize_name(value):
    """Normalize a name or use the required default."""
    if is_missing(value):
        return "Valued Prospect"

    return " ".join(str(value).split()).title()

def normalize_mobile(value):
    """
    Normalize an Indian mobile number.

    Accept:
      - 9876543210
      - 98765 43210
      - +91 98765 43210
      - 919876543210

    Reject arbitrary text, invalid starting digits, and other
    international prefixes. This validates format only; it does
    not verify ownership, activity, consent, or contact eligibility.
    """
    if is_missing(value):
        return None

    raw = str(value).strip()

    # Permit common separators and at most one leading plus sign.
    if not re.fullmatch(r"\+?[\d\s().-]+", raw):
        return None

    if "+" in raw and not raw.startswith("+"):
        return None

    if raw.count("+") > 1:
        return None

    digits = re.sub(r"\D", "", raw)


    if MOBILE_PATTERN.fullmatch(digits):
        return digits

    if MOBILE_WITH_COUNTRY_CODE_PATTERN.fullmatch(digits):
        return digits[2:]

    return None


def normalize_zone(value):
    """Normalize a known locality/zone to its canonical enum value."""
    if is_missing(value):
        return None

    key = re.sub(r"[\s-]+", "_", str(value).strip()).casefold()

    zone_aliases = {
        "hadapsar": "Hadapsar",
        "fursungi": "Fursungi",
        "adjacent_east_pune": "Adjacent_East_Pune",
    }

    return zone_aliases.get(key)


def normalize_requirement(value):
    """Normalize common property requirement variants."""
    if is_missing(value):
        return None

    key = re.sub(r"\s+", " ", str(value).strip()).casefold()

    requirement_aliases = {
        "1bhk": "1BHK",
        "1 bhk": "1BHK",
        "2bhk": "2BHK",
        "2 bhk": "2BHK",
        "3bhk": "3BHK",
        "3 bhk": "3BHK",
        "residential plot": "Residential Plot",
        "plot": "Residential Plot",
    }

    return requirement_aliases.get(key)


def normalize_source_channel(value):
    """Normalize a source label without inventing missing source details."""
    if is_missing(value):
        return None

    return str(value).strip()


def clean_records(df):
    """
    Normalize records and add an is_valid flag.

    Rows are retained for auditability. Filter to is_valid == True
    before treating rows as qualified records.
    """
    df = df.copy()

    required_columns = {
        "Prospect_Name",
        "Mobile_Number",
        "Target_Zone",
        "Requirement",
        "Source_Channel",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    df["Prospect_Name"] = df["Prospect_Name"].apply(normalize_name)
    df["Mobile_Number"] = df["Mobile_Number"].apply(normalize_mobile)
    df["Target_Zone"] = df["Target_Zone"].apply(normalize_zone)
    df["Requirement"] = df["Requirement"].apply(normalize_requirement)
    df["Source_Channel"] = df["Source_Channel"].apply(
        normalize_source_channel
    )

    # If the source reference or evidence columns exist, missing values
    # must not be silently represented as verified evidence.
    if "Source_Reference" in df.columns:
        df["Source_Reference"] = df["Source_Reference"].apply(
            normalize_source_channel
        )

    if "Intent_Evidence" in df.columns:
        df["Intent_Evidence"] = df["Intent_Evidence"].apply(
            normalize_source_channel
        )

    df["is_valid"] = (
        df["Mobile_Number"].notna()
        & df["Target_Zone"].isin(VALID_ZONES)
        & df["Requirement"].isin(VALID_REQUIREMENTS)
        & df["Source_Channel"].notna()
        & df["Source_Channel"].ne("")
    )

    # Format validation is not proof of mobile ownership or consent.
    df["Mobile_Format_Valid"] = df["Mobile_Number"].notna()

    return df


def remove_duplicates(df):
    """
    Remove invalid rows and duplicate mobile numbers.

    The first valid occurrence is retained. Invalid rows and duplicates
    are counted in DataFrame attrs for reporting.
    """
    df = df.copy()

    if "is_valid" not in df.columns:
        raise ValueError(
            "Missing 'is_valid' column. Run clean_records() first."
        )

    raw_count = len(df)

    valid_df = df[
        df["is_valid"].fillna(False)
        & df["Mobile_Number"].notna()
    ].copy()

    invalid_count = raw_count - len(valid_df)

    # Mobile numbers have already been normalized to a canonical format.
    deduplicated_df = valid_df.drop_duplicates(
        subset=["Mobile_Number"],
        keep="first",
    ).reset_index(drop=True)

    duplicate_count = len(valid_df) - len(deduplicated_df)

    deduplicated_df.attrs["input_count"] = raw_count
    deduplicated_df.attrs["invalid_count"] = invalid_count
    deduplicated_df.attrs["duplicate_count"] = duplicate_count
    deduplicated_df.attrs["output_count"] = len(deduplicated_df)

    return deduplicated_df


if __name__ == "__main__":
    # Synthetic fixtures for local development only.
    sample = pd.DataFrame([
        {
            "Prospect_Name": "  sample person ",
            "Mobile_Number": "+91 98765 43210",
            "Target_Zone": "hadapsar",
            "Requirement": "2 bhk",
            "Source_Channel": "synthetic-test-data",
        },
        {
            "Prospect_Name": "",
            "Mobile_Number": "abc9876543210xyz",
            "Target_Zone": "Unknown",
            "Requirement": "4BHK",
            "Source_Channel": "synthetic-test-data",
        },
        {
            "Prospect_Name": "Sample Duplicate",
            "Mobile_Number": "9876543210",
            "Target_Zone": "Hadapsar",
            "Requirement": "2BHK",
            "Source_Channel": "synthetic-test-data",
        },
    ])

    cleaned = clean_records(sample)
    result = remove_duplicates(cleaned)

    print("Synthetic demonstration only")
    print(cleaned.to_string(index=False))
    print("\nInput records:", len(sample))
    print("Invalid records:", result.attrs["invalid_count"])
    print("Duplicate records:", result.attrs["duplicate_count"])
    print("Output records:", result.attrs["output_count"])