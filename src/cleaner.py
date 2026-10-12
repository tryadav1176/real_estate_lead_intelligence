
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


def normalize_name(value):
    """Normalize a name or use the required default."""
    if pd.isna(value) or not str(value).strip():
        return "Valued Prospect"

    return str(value).strip().title()


def normalize_mobile(value):
    """Accept only 10-digit Indian mobile numbers starting 6-9."""
    if pd.isna(value):
        return None

    digits = re.sub(r"\D", "", str(value))

    # Do not silently accept international prefixes.
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]

    if re.fullmatch(r"[6-9]\d{9}", digits):
        return digits

    return None


def clean_records(df):
    """Normalize fields and flag invalid records."""
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

    df["Prospect_Name"] = df["Prospect_Name"].apply(
        normalize_name
    )

    df["Mobile_Number"] = df["Mobile_Number"].apply(
        normalize_mobile
    )

    df["Target_Zone"] = (
        df["Target_Zone"]
        .astype("string")
        .str.strip()
        .replace({
            "hadapsar": "Hadapsar",
            "fursungi": "Fursungi",
            "adjacent_east_pune": "Adjacent_East_Pune",
        })
    )

    df["Requirement"] = (
        df["Requirement"]
        .astype("string")
        .str.strip()
        .replace({
            "1bhk": "1BHK",
            "2bhk": "2BHK",
            "3bhk": "3BHK",
            "residential plot": "Residential Plot",
        })
    )

    df["Source_Channel"] = (
        df["Source_Channel"].astype("string").str.strip()
    )

    df["is_valid"] = (
        df["Mobile_Number"].notna()
        & df["Target_Zone"].isin(VALID_ZONES)
        & df["Requirement"].isin(VALID_REQUIREMENTS)
        & df["Source_Channel"].notna()
        & df["Source_Channel"].ne("")
    )

    return df


if __name__ == "__main__":
    sample = pd.DataFrame([
        {
            "Prospect_Name": "  sample person ",
            "Mobile_Number": "98765 43210",
            "Target_Zone": "hadapsar",
            "Requirement": "2bhk",
            "Source_Channel": "synthetic-test-data",
        },
        {
            "Prospect_Name": "",
            "Mobile_Number": "12345",
            "Target_Zone": "Unknown",
            "Requirement": "4BHK",
            "Source_Channel": "synthetic-test-data",
        },
    ])

    result = clean_records(sample)

    print(result.to_string(index=False))
    print("\nValid records:", int(result["is_valid"].sum()))
    print("Invalid records:", int((~result["is_valid"]).sum()))

def remove_duplicates(df):
    """Remove duplicate prospect records using normalized mobile numbers."""
    df = df.copy()

    # Keep only valid records with a mobile number
    valid_df = df[
        df["is_valid"] & df["Mobile_Number"].notna()
    ].copy()

    # Keep the first record for each mobile number
    deduplicated_df = valid_df.drop_duplicates(
        subset=["Mobile_Number"],
        keep="first"
    )

    return deduplicated_df.reset_index(drop=True)