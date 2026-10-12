
from datetime import datetime, timezone


def calculate_lead_score(location_score, requirement_score, recency_score):
    """
    Calculate a lead score out of 100.

    Each component must stay within its assigned maximum.
    """
    components = {
        "location": (location_score, 40),
        "requirement": (requirement_score, 35),
        "recency": (recency_score, 25),
    }

    for name, (score, maximum) in components.items():
        if not isinstance(score, (int, float)) or isinstance(score, bool):
            raise ValueError(f"{name} score must be numeric")

        if not 0 <= score <= maximum:
            raise ValueError(
                f"{name} score must be between 0 and {maximum}"
            )

    return round(
        location_score + requirement_score + recency_score
    )


def score_record(record):
    """
    Score one record using provisional example rules.

    Replace these example rules if Amar Realty supplies
    its official scoring criteria.
    """
    zone = str(record.get("Target_Zone", "")).strip()
    requirement = str(record.get("Requirement", "")).strip()

    # Provisional location scoring
    location_scores = {
        "Hadapsar": 40,
        "Fursungi": 40,
        "Adjacent_East_Pune": 25,
    }
    location_score = location_scores.get(zone, 0)

    # Provisional requirement scoring
    requirement_scores = {
        "1BHK": 25,
        "2BHK": 35,
        "3BHK": 30,
        "Residential Plot": 20,
    }
    requirement_score = requirement_scores.get(requirement, 0)

    # Recency requires a verified source timestamp.
    # Do not award recency points without one.
    recency_score = 0

    return calculate_lead_score(
        location_score,
        requirement_score,
        recency_score,
    )


if __name__ == "__main__":
    sample_record = {
        "Target_Zone": "Hadapsar",
        "Requirement": "2BHK",
    }

    print("Example lead score:", score_record(sample_record))
