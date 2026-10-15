"""Summarize and sanity-check the hand-reviewed intent signal log.

Usage (from the project root):
    python -m src.intent_summary
    python -m src.intent_summary data/intent_log/intent_signal_log.csv

It reports counts only. It also WARNS if a row seems to contain personal
data (a phone-like number, an @handle, or a u/username), because the log
must never store those.
"""

import re
import sys
from pathlib import Path

import pandas as pd

DEFAULT_PATH = Path("data/intent_log/intent_signal_log.csv")

REQUIRED_COLUMNS = [
    "Source_Channel", "Source_Reference", "Post_Date", "Review_Method",
    "Prospect_Name", "Mobile_Number", "Target_Zone", "Requirement",
    "Intent_Type", "Intent_Evidence", "Contact_Visible_In_Post",
    "Reviewer_Notes",
]
VALID_INTENT_TYPES = {
    "direct_purchase", "emerging_purchase", "rental",
    "seller_listing", "geographic_context", "unknown",
}
VALID_ZONES = {"Hadapsar", "Fursungi", "Adjacent_East_Pune", "Other"}
VALID_REQUIREMENTS = {"1BHK", "2BHK", "3BHK", "Residential Plot", "Other", "Unspecified"}
BUYER_SIDE = {"direct_purchase", "emerging_purchase", "rental"}

PHONE_LIKE = re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)")
HANDLE_LIKE = re.compile(r"(?:^|\s)(?:u/|@)\w+")


def load_log(path=DEFAULT_PATH):
    return pd.read_csv(path, dtype=str).fillna("")


def check_log(df):
    """Return a list of human-readable problems (empty list = clean)."""
    problems = []

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return [f"Missing columns: {missing}"]

    for i, row in df.iterrows():
        line = i + 2  # CSV line number, header is line 1
        if row["Intent_Type"] not in VALID_INTENT_TYPES:
            problems.append(f"line {line}: invalid Intent_Type '{row['Intent_Type']}'")
        if row["Target_Zone"] not in VALID_ZONES:
            problems.append(f"line {line}: invalid Target_Zone '{row['Target_Zone']}'")
        if row["Requirement"] not in VALID_REQUIREMENTS:
            problems.append(f"line {line}: invalid Requirement '{row['Requirement']}'")
        if not row["Source_Reference"].strip():
            problems.append(f"line {line}: missing Source_Reference")
        if not row["Intent_Evidence"].strip():
            problems.append(f"line {line}: missing Intent_Evidence")
        if row["Contact_Visible_In_Post"] not in {"yes", "no"}:
            problems.append(f"line {line}: Contact_Visible_In_Post must be yes or no")
        if row["Mobile_Number"].strip():
            problems.append(f"line {line}: PRIVACY - Mobile_Number must stay blank in this log")
        if row["Prospect_Name"].strip():
            problems.append(f"line {line}: PRIVACY - Prospect_Name must stay blank in this log")

        free_text = " ".join([row["Intent_Evidence"], row["Reviewer_Notes"]])
        if PHONE_LIKE.search(free_text):
            problems.append(f"line {line}: PRIVACY - phone-like number in free text")
        if HANDLE_LIKE.search(free_text):
            problems.append(f"line {line}: PRIVACY - username/handle in free text")

    dupes = df[df["Source_Reference"].str.strip().ne("")].duplicated(
        subset=["Source_Reference"], keep="first"
    )
    for i in df[df["Source_Reference"].str.strip().ne("")][dupes].index:
        problems.append(f"line {i + 2}: duplicate Source_Reference")

    return problems


def summarize(df):
    buyer_side = df[df["Intent_Type"].isin(BUYER_SIDE)]
    in_area = df[df["Target_Zone"].isin({"Hadapsar", "Fursungi", "Adjacent_East_Pune"})]
    return {
        "posts_reviewed": len(df),
        "by_intent_type": df["Intent_Type"].value_counts().to_dict(),
        "by_target_zone": df["Target_Zone"].value_counts().to_dict(),
        "buyer_side_signals": len(buyer_side),
        "buyer_side_in_target_area": int(
            buyer_side["Target_Zone"].isin({"Hadapsar", "Fursungi", "Adjacent_East_Pune"}).sum()
        ),
        "posts_with_visible_contact": int((df["Contact_Visible_In_Post"] == "yes").sum()),
        "posts_in_target_area": len(in_area),
        # Mobile numbers are deliberately NOT collected in this log, so no
        # record here can be a qualified prospect.
        "qualified_prospects": 0,
    }


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    df = load_log(path)
    problems = check_log(df)

    print(f"Log file: {path}")
    if problems:
        print(f"\n{len(problems)} problem(s) found:")
        for p in problems:
            print("  -", p)
    else:
        print("No problems found.")

    if len(df) == 0:
        print("\nLog is empty. Add reviewed posts first.")
        return

    result = summarize(df)
    print("\nSummary (counts from the hand-reviewed sample):")
    for key, value in result.items():
        print(f"  {key}: {value}")
    print("\nNote: intent signals are not qualified prospects. No mobile numbers are stored here.")


if __name__ == "__main__":
    main()
