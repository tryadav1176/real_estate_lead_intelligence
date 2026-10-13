from datetime import datetime, timezone
import math


MAX_LOCATION_SCORE = 40
MAX_REQUIREMENT_SCORE = 35
MAX_RECENCY_SCORE = 25
MAX_LEAD_SCORE = 100

# Provisional rules, pending confirmation from Amar Realty.
LOCATION_SCORES = {
    "Hadapsar": 40,
    "Fursungi": 40,
    "Adjacent_East_Pune": 25,
}

REQUIREMENT_SCORES = {
    "1BHK": 25,
    "2BHK": 35,
    "3BHK": 30,
    "Residential Plot": 20,
}


def calculate_lead_score(
    location_score,
    requirement_score,
    recency_score,
):
    """Calculate a validated score out of 100."""
    components = {
        "location": (location_score, MAX_LOCATION_SCORE),
        "requirement": (requirement_score, MAX_REQUIREMENT_SCORE),
        "recency": (recency_score, MAX_RECENCY_SCORE),
    }

    for name, (score, maximum) in components.items():
        if (
            not isinstance(score, (int, float))
            or isinstance(score, bool)
            or not math.isfinite(score)
        ):
            raise ValueError(f"{name} score must be a finite number")

        if not 0 <= score <= maximum:
            raise ValueError(
                f"{name} score must be between 0 and {maximum}"
            )

    return round(
        location_score + requirement_score + recency_score
    )



def parse_source_timestamp(value):
    """
    Parse an explicitly supplied source timestamp.

    Accept datetime objects and ISO-8601 strings only when a timezone
    is present. Return None for missing, malformed, or timezone-naive
    timestamps so ambiguous dates do not receive recency credit.
    """

    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return None

        try:
            # Support ISO-8601 timestamps ending in Z.
            value = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )
        except ValueError:
            return None

    if not isinstance(value, datetime):
        return None

    if value.tzinfo is None:
        return None

    return value.astimezone(timezone.utc)


def calculate_recency_score(
    source_timestamp,
    reference_time=None,
):
    """
    Return a provisional recency score from 0 to 25.

    Policy:
      - No valid timestamp: 0
      - Future timestamp: 0
      - Within 7 days: 25
      - Within 30 days: 15
      - Within 90 days: 5
      - Older than 90 days: 0

    These thresholds are provisional and should be confirmed with
    Amar Realty before being used for operational prioritization.
    """
    timestamp = parse_source_timestamp(source_timestamp)

    if timestamp is None:
        return 0

    if reference_time is None:
        reference_time = datetime.now(timezone.utc)
    elif not isinstance(reference_time, datetime):
        raise ValueError("reference_time must be a datetime")

    if reference_time.tzinfo is None:
        raise ValueError("reference_time must include a timezone")

    reference_time = reference_time.astimezone(timezone.utc)

    age = reference_time - timestamp

    if age.total_seconds() < 0:
        return 0

    age_days = age.total_seconds() / 86400

    if age_days <= 7:
        return 25

    if age_days <= 30:
        return 15

    if age_days <= 90:
        return 5

    return 0


def score_record(record, reference_time=None):
    """
    Score a record using provisional, explainable rules.

    The source timestamp must represent a supported source event,
    not the time the pipeline happened to process the record.
    """
    zone = record.get("Target_Zone")
    requirement = record.get("Requirement")

    location_score = LOCATION_SCORES.get(zone, 0)
    requirement_score = REQUIREMENT_SCORES.get(requirement, 0)

    source_timestamp = record.get("Source_Timestamp")

    recency_score = calculate_recency_score(
        source_timestamp,
        reference_time=reference_time,
    )

    return calculate_lead_score(
        location_score,
        requirement_score,
        recency_score,
    )


if __name__ == "__main__":
    sample_record = {
        "Target_Zone": "Hadapsar",
        "Requirement": "2BHK",
        # No source timestamp: recency score remains zero.
    }

    print("Synthetic example score:", score_record(sample_record))
