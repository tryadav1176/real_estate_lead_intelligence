from datetime import datetime, timedelta, timezone

import pytest

from src.scorer import (
    calculate_lead_score,
    calculate_recency_score,
    parse_source_timestamp,
    score_record,
)


def test_calculate_total_score():
    assert calculate_lead_score(40, 35, 25) == 100


def test_calculate_zero_score():
    assert calculate_lead_score(0, 0, 0) == 0


@pytest.mark.parametrize(
    "location, requirement, recency",
    [
        (41, 35, 25),
        (40, 36, 25),
        (40, 35, 26),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
    ],
)
def test_component_scores_must_be_within_limits(
    location,
    requirement,
    recency,
):
    with pytest.raises(ValueError):
        calculate_lead_score(location, requirement, recency)


@pytest.mark.parametrize(
    "location, requirement, recency",
    [
        (True, 10, 10),
        (10, False, 10),
        (10, 10, True),
        (float("nan"), 10, 10),
        (10, float("inf"), 10),
        (10, 10, float("-inf")),
    ],
)
def test_component_scores_must_be_finite_numbers(
    location,
    requirement,
    recency,
):
    with pytest.raises(ValueError):
        calculate_lead_score(location, requirement, recency)


def test_score_record_for_hadapsar_2bhk():
    record = {
        "Target_Zone": "Hadapsar",
        "Requirement": "2BHK",
    }

    # No source timestamp means no recency points.
    assert score_record(record) == 75


def test_unknown_zone_gets_no_location_points():
    record = {
        "Target_Zone": "Unknown",
        "Requirement": "2BHK",
    }

    assert score_record(record) == 35


def test_unknown_requirement_gets_no_requirement_points():
    record = {
        "Target_Zone": "Hadapsar",
        "Requirement": "4BHK",
    }

    assert score_record(record) == 40


def test_recent_source_timestamp_adds_recency_points():
    reference_time = datetime(
        2026, 10, 13, 12, 0, tzinfo=timezone.utc
    )

    record = {
        "Target_Zone": "Hadapsar",
        "Requirement": "2BHK",
        "Source_Timestamp": (
            reference_time - timedelta(days=3)
        ).isoformat(),
    }

    assert score_record(
        record,
        reference_time=reference_time,
    ) == 100


def test_missing_source_timestamp_gets_zero_recency():
    assert calculate_recency_score(None) == 0
    assert calculate_recency_score("") == 0


def test_malformed_source_timestamp_gets_zero_recency():
    assert calculate_recency_score("not-a-timestamp") == 0


def test_future_source_timestamp_gets_zero_recency():
    reference_time = datetime(
        2026, 10, 13, 12, 0, tzinfo=timezone.utc
    )
    future_time = reference_time + timedelta(days=1)

    assert calculate_recency_score(
        future_time.isoformat(),
        reference_time=reference_time,
    ) == 0


@pytest.mark.parametrize(
    "age_days, expected_score",
    [
        (0, 25),
        (7, 25),
        (8, 15),
        (30, 15),
        (31, 5),
        (90, 5),
        (91, 0),
    ],
)
def test_recency_thresholds(age_days, expected_score):
    reference_time = datetime(
        2026, 10, 13, 12, 0, tzinfo=timezone.utc
    )
    timestamp = reference_time - timedelta(days=age_days)

    assert calculate_recency_score(
        timestamp.isoformat(),
        reference_time=reference_time,
    ) == expected_score


def test_parse_source_timestamp_accepts_iso8601():
    timestamp = parse_source_timestamp(
        "2026-10-13T12:00:00+00:00"
    )

    assert timestamp == datetime(
        2026, 10, 13, 12, 0, tzinfo=timezone.utc
    )


def test_parse_source_timestamp_rejects_timezone_naive_value():
    assert parse_source_timestamp(
        "2026-10-13T12:00:00"
    ) is None


def test_parse_source_timestamp_rejects_non_string_value():
    assert parse_source_timestamp(12345) is None