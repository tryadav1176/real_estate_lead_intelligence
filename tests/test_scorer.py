
import pytest

from src.scorer import calculate_lead_score, score_record


def test_calculate_total_score():
    assert calculate_lead_score(40, 35, 25) == 100


def test_calculate_zero_score():
    assert calculate_lead_score(0, 0, 0) == 0


def test_score_cannot_exceed_component_limit():
    with pytest.raises(ValueError):
        calculate_lead_score(41, 35, 25)


def test_score_record_for_hadapsar_2bhk():
    record = {
        "Target_Zone": "Hadapsar",
        "Requirement": "2BHK",
    }

    assert score_record(record) == 75
