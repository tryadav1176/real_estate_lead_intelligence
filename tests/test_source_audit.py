
from types import SimpleNamespace

import pytest

from src import source_audit


def test_validate_https_url():
    assert (
        source_audit.validate_base_url("https://example.com/path")
        == "https://example.com"
    )


def test_validate_http_url():
    assert (
        source_audit.validate_base_url("http://example.com")
        == "http://example.com"
    )


def test_reject_non_http_scheme():
    with pytest.raises(ValueError):
        source_audit.validate_base_url("ftp://example.com")


def test_reject_url_without_hostname():
    with pytest.raises(ValueError):
        source_audit.validate_base_url("https://")


def test_reject_url_with_credentials():
    with pytest.raises(ValueError):
        source_audit.validate_base_url(
            "https://user:password@example.com"
        )


def test_robots_404_is_unknown(monkeypatch):
    monkeypatch.setattr(
        source_audit.requests,
        "get",
        lambda *args, **kwargs: SimpleNamespace(status_code=404, text=""),
    )

    result = source_audit.check_robots("https://example.com")

    assert result["robots_http_status"] == 404
    assert result["robots_allowed_for_root"] == "UNKNOWN"


def test_robots_disallow_root(monkeypatch):
    monkeypatch.setattr(
        source_audit.requests,
        "get",
        lambda *args, **kwargs: SimpleNamespace(
            status_code=200,
            text="User-agent: *\nDisallow: /\n",
        ),
    )

    result = source_audit.check_robots("https://example.com")

    assert result["robots_allowed_for_root"] == "NO"


def test_unknown_robots_status_skips_homepage(monkeypatch):
    request_count = {"value": 0}

    def fake_get(*args, **kwargs):
        request_count["value"] += 1
        return SimpleNamespace(status_code=404, text="")

    monkeypatch.setattr(source_audit.requests, "get", fake_get)
    monkeypatch.setattr(source_audit.time, "sleep", lambda _: None)

    result = source_audit.review_source(
        "Example",
        "https://example.com",
    )

    assert request_count["value"] == 1
    assert result["automated_access_authorized"] == "NO"
    assert result["terms_reviewed"] == "NO"
    assert result["homepage_http_status"] == ""
    assert result["robots_allowed_for_root"] == "UNKNOWN"
