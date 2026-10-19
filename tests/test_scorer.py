import math
from datetime import datetime, timedelta, timezone
import pytest

from src.scorer import (
    calculate_lead_score,
    calculate_recency_score,
    parse_source_timestamp,
    score_record,
)

def test_calculate_total_score():
    assert calculate_lead_score(40, 25, 20, 15) == 100

def test_calculate_zero_score():
    assert calculate_lead_score(0, 0, 0, 0) == 0

@pytest.mark.parametrize(
    "intent, location, requirement, recency",
    [
        (41, 25, 20, 15),
        (40, 26, 20, 15),
        (40, 25, 21, 15),
        (40, 25, 20, 16),
        (-1, 0, 0, 0),
        (0, -1, 0, 0),
        (0, 0, -1, 0),
        (0, 0, 0, -1),
    ],
)
def test_component_scores_must_be_within_limits(intent, location, requirement, recency):
    with pytest.raises(ValueError):
        calculate_lead_score(intent, location, requirement, recency)

@pytest.mark.parametrize(
    "intent, location, requirement, recency",
    [
        (True, 25, 20, 15),
        (40, False, 20, 15),
        (40, 25, True, 15),
        (40, 25, 20, False),
        (float("nan"), 25, 20, 15),
        (40, float("inf"), 20, 15),
        (40, 25, float("-inf"), 15),
    ],
)
def test_component_scores_must_be_finite_numbers(intent, location, requirement, recency):
    with pytest.raises(ValueError):
        calculate_lead_score(intent, location, requirement, recency)

def test_score_record_for_hadapsar_2bhk():
    record = {
        "Target_Zone": "Hadapsar",
        "Requirement": "2BHK",
    }
    # Unknown intent (0) + Hadapsar (25) + 2BHK (20) + No timestamp (0) = 45
    assert score_record(record) == 45

def test_unknown_zone_gets_no_location_points():
    record = {
        "Target_Zone": "Unknown",
        "Requirement": "2BHK",
    }
    # Unknown intent (0) + Unknown zone (0) + 2BHK (20) + No timestamp (0) = 20
    assert score_record(record) == 20

def test_unknown_requirement_gets_no_requirement_points():
    record = {
        "Target_Zone": "Hadapsar",
        "Requirement": "4BHK",
    }
    # Unknown intent (0) + Hadapsar (25) + Unknown req (0) + No timestamp (0) = 25
    assert score_record(record) == 25

def test_recent_source_timestamp_adds_recency_points():
    reference_time = datetime(2026, 10, 13, 12, 0, tzinfo=timezone.utc)
    record = {
        "Target_Zone": "Hadapsar",
        "Requirement": "2BHK",
        "Source_Timestamp": (reference_time - timedelta(days=3)).isoformat(),
    }
    # Unknown intent (0) + Hadapsar (25) + 2BHK (20) + Recency (15) = 60
    assert score_record(record, reference_time=reference_time) == 60

def test_missing_source_timestamp_gets_zero_recency():
    assert calculate_recency_score(None) == 0
    assert calculate_recency_score("") == 0
    assert calculate_recency_score("   ") == 0

def test_malformed_source_timestamp_gets_zero_recency():
    assert calculate_recency_score("invalid-date") == 0
    assert calculate_recency_score("2026-99-99") == 0

def test_future_source_timestamp_gets_zero_recency():
    reference_time = datetime(2026, 10, 13, 12, 0, tzinfo=timezone.utc)
    future_time = reference_time + timedelta(days=1)
    assert calculate_recency_score(future_time.isoformat(), reference_time=reference_time) == 0

@pytest.mark.parametrize(
    "age_days, expected_score",
    [
        (0, 15),
        (7, 15),
        (8, 10),
        (30, 10),
        (31, 5),
        (90, 5),
        (91, 0),
    ],
)
def test_recency_thresholds(age_days, expected_score):
    reference_time = datetime(2026, 10, 13, 12, 0, tzinfo=timezone.utc)
    timestamp = reference_time - timedelta(days=age_days)
    assert calculate_recency_score(
        timestamp.isoformat(),
        reference_time=reference_time,
    ) == expected_score

def test_parse_source_timestamp_accepts_iso8601():
    dt = parse_source_timestamp("2026-10-13T12:00:00+00:00")
    assert dt.tzinfo is not None

def test_parse_source_timestamp_rejects_timezone_naive_value():
    assert parse_source_timestamp("2026-10-13T12:00:00") is None

def test_parse_source_timestamp_rejects_non_string_value():
    assert parse_source_timestamp(2026) is None
    assert parse_source_timestamp(["2026-10-13T12:00:00Z"]) is None