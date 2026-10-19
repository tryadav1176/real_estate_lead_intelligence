from datetime import datetime, timezone
import math
import pandas as pd

# Recalibrated to 100 points to include Intent_Type
MAX_INTENT_SCORE = 40
MAX_LOCATION_SCORE = 25
MAX_REQUIREMENT_SCORE = 20
MAX_RECENCY_SCORE = 15
MAX_LEAD_SCORE = 100

INTENT_SCORES = {
    "direct purchase": 40,
    "emerging purchase": 25,
    "rental": 10,
    "seller listing": 0,
    "geographic context": 0,
    "unknown": 0,
}

LOCATION_SCORES = {
    "Hadapsar": 25,
    "Fursungi": 25,
    "Adjacent_East_Pune": 15,
}

REQUIREMENT_SCORES = {
    "1BHK": 10,
    "2BHK": 20,
    "3BHK": 15,
    "Residential Plot": 10,
}

def classify_intent(text):
    if not isinstance(text, str) or not text.strip():
        return "unknown"
    text_lower = text.lower()
    if any(kw in text_lower for kw in ["sell my", "selling", "available for sale", "broker"]):
        return "seller listing"
    elif any(kw in text_lower for kw in ["looking to buy", "want to purchase", "immediate buyer"]):
        return "direct purchase"
    elif any(kw in text_lower for kw in ["future investment", "what are the rates", "price trends"]):
        return "emerging purchase"
    elif any(kw in text_lower for kw in ["on rent", "looking for flatmates", "tenant"]):
        return "rental"
    elif any(kw in text_lower for kw in ["traffic", "construction", "water supply", "development plan"]):
        return "geographic context"
    return "unknown"

def calculate_lead_score(intent_score, location_score, requirement_score, recency_score):
    """Calculate a validated score out of 100."""
    components = {
        "intent": (intent_score, MAX_INTENT_SCORE),
        "location": (location_score, MAX_LOCATION_SCORE),
        "requirement": (requirement_score, MAX_REQUIREMENT_SCORE),
        "recency": (recency_score, MAX_RECENCY_SCORE),
    }
    for name, (score, maximum) in components.items():
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not math.isfinite(score):
            raise ValueError(f"{name} score must be a finite number")
        if not 0 <= score <= maximum:
            raise ValueError(f"{name} score must be between 0 and {maximum}")
    return round(intent_score + location_score + requirement_score + recency_score)

def parse_source_timestamp(value):
    if pd.isna(value) or value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if not isinstance(value, datetime) or value.tzinfo is None:
        return None
    return value.astimezone(timezone.utc)

def calculate_recency_score(source_timestamp, reference_time=None):
    timestamp = parse_source_timestamp(source_timestamp)
    if timestamp is None:
        return 0
    if reference_time is None:
        reference_time = datetime.now(timezone.utc)
    reference_time = reference_time.astimezone(timezone.utc)
    age_days = (reference_time - timestamp).total_seconds() / 86400

    if age_days < 0: return 0
    if age_days <= 7: return 15
    if age_days <= 30: return 10
    if age_days <= 90: return 5
    return 0

def score_record(record, reference_time=None):
    zone = record.get("Target_Zone")
    requirement = record.get("Requirement")
    intent_text = record.get("Source_Reference", "")
    
    intent_type = classify_intent(intent_text)
    record["Intent_Type"] = intent_type

    intent_score = INTENT_SCORES.get(intent_type, 0)
    location_score = LOCATION_SCORES.get(zone, 0)
    requirement_score = REQUIREMENT_SCORES.get(requirement, 0)
    recency_score = calculate_recency_score(record.get("Source_Timestamp"), reference_time)

    return calculate_lead_score(intent_score, location_score, requirement_score, recency_score)