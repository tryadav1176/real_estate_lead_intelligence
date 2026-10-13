import csv
from types import SimpleNamespace

import pytest

from src import source_audit


def fake_response(status_code, text="", headers=None):
    return SimpleNamespace(
        status_code=status_code,
        text=text,
        headers=headers or {},
        url="https://example.com/",
        raise_for_status=lambda: None,
    )


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


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com?query=value",
        "https://example.com#section",
    ],
)
def test_reject_query_or_fragment_in_base_url(url):
    with pytest.raises(ValueError):
        source_audit.validate_base_url(url)


def test_robots_404_is_unknown(monkeypatch):
    monkeypatch.setattr(
        source_audit.requests,
        "get",
        lambda *args, **kwargs: fake_response(404),
    )

    result = source_audit.check_robots("https://example.com")

    assert result["robots_http_status"] == 404
    assert result["robots_allowed_for_root"] == "UNKNOWN"
    assert "does not establish authorization" in result["robots_error"]


def test_robots_disallow_root(monkeypatch):
    monkeypatch.setattr(
        source_audit.requests,
        "get",
        lambda *args, **kwargs: fake_response(
            200,
            "User-agent: *\nDisallow: /\n",
        ),
    )

    result = source_audit.check_robots("https://example.com")

    assert result["robots_allowed_for_root"] == "NO"


def test_robots_allow_root(monkeypatch):
    monkeypatch.setattr(
        source_audit.requests,
        "get",
        lambda *args, **kwargs: fake_response(
            200,
            "User-agent: *\nAllow: /\n",
        ),
    )

    result = source_audit.check_robots("https://example.com")

    assert result["robots_allowed_for_root"] == "YES"


@pytest.mark.parametrize("status_code", [401, 403, 407, 429])
def test_robots_blocked_or_rate_limited_status_is_unknown(
    monkeypatch,
    status_code,
):
    monkeypatch.setattr(
        source_audit.requests,
        "get",
        lambda *args, **kwargs: fake_response(status_code),
    )

    result = source_audit.check_robots("https://example.com")

    assert result["robots_allowed_for_root"] == "UNKNOWN"
    assert result["robots_http_status"] == status_code
    assert "no retry attempted" in result["robots_error"]


def test_robots_redirect_is_not_followed(monkeypatch):
    calls = []

    def fake_get(url, **kwargs):
        calls.append((url, kwargs))
        return fake_response(301)

    monkeypatch.setattr(source_audit.requests, "get", fake_get)

    result = source_audit.check_robots("https://example.com")

    assert len(calls) == 1
    assert calls[0][1]["allow_redirects"] is False
    assert result["robots_allowed_for_root"] == "UNKNOWN"
    assert "Redirect returned" in result["robots_error"]


def test_unknown_robots_status_skips_homepage(
    monkeypatch,
    tmp_path,
):
    request_count = {"value": 0}

    def fake_get(*args, **kwargs):
        request_count["value"] += 1
        return fake_response(404)

    monkeypatch.setattr(source_audit.requests, "get", fake_get)
    monkeypatch.setattr(source_audit.time, "sleep", lambda _: None)
    monkeypatch.setattr(
        source_audit,
        "AUDIT_OUTPUT",
        tmp_path / "source_checks.csv",
    )

    result = source_audit.review_source(
        "Example",
        "https://example.com",
    )

    assert request_count["value"] == 1
    assert result["automated_access_authorized"] == "NO"
    assert result["terms_reviewed"] == "NO"
    assert result["homepage_http_status"] == ""
    assert result["robots_allowed_for_root"] == "UNKNOWN"
    assert (tmp_path / "source_checks.csv").exists()


def test_review_source_records_homepage_response(
    monkeypatch,
    tmp_path,
):
    responses = [
        fake_response(200, "User-agent: *\nAllow: /\n"),
        fake_response(200, "<html></html>"),
    ]
    request_count = {"value": 0}

    def fake_get(*args, **kwargs):
        response = responses[request_count["value"]]
        request_count["value"] += 1
        return response

    monkeypatch.setattr(source_audit.requests, "get", fake_get)
    monkeypatch.setattr(source_audit.time, "sleep", lambda _: None)
    monkeypatch.setattr(
        source_audit,
        "AUDIT_OUTPUT",
        tmp_path / "source_checks.csv",
    )

    result = source_audit.review_source(
        "Example",
        "https://example.com",
    )

    assert request_count["value"] == 2
    assert result["homepage_http_status"] == 200
    assert result["automated_access_authorized"] == "NO"
    assert result["terms_reviewed"] == "NO"


@pytest.mark.parametrize("status_code", [401, 403, 407, 429])
def test_blocked_homepage_is_recorded_without_retry(
    monkeypatch,
    tmp_path,
    status_code,
):
    responses = [
        fake_response(200, "User-agent: *\nAllow: /\n"),
        fake_response(status_code),
    ]
    request_count = {"value": 0}

    def fake_get(*args, **kwargs):
        response = responses[request_count["value"]]
        request_count["value"] += 1
        return response

    monkeypatch.setattr(source_audit.requests, "get", fake_get)
    monkeypatch.setattr(source_audit.time, "sleep", lambda _: None)
    monkeypatch.setattr(
        source_audit,
        "AUDIT_OUTPUT",
        tmp_path / "source_checks.csv",
    )

    result = source_audit.review_source(
        "Example",
        "https://example.com",
    )

    assert request_count["value"] == 2
    assert result["homepage_http_status"] == status_code
    assert "no retry attempted" in result["homepage_result"]


def test_redirected_homepage_is_recorded(
    monkeypatch,
    tmp_path,
):
    responses = [
        fake_response(200, "User-agent: *\nAllow: /\n"),
        fake_response(302),
    ]
    request_count = {"value": 0}

    def fake_get(*args, **kwargs):
        response = responses[request_count["value"]]
        request_count["value"] += 1
        return response

    monkeypatch.setattr(source_audit.requests, "get", fake_get)
    monkeypatch.setattr(source_audit.time, "sleep", lambda _: None)
    monkeypatch.setattr(
        source_audit,
        "AUDIT_OUTPUT",
        tmp_path / "source_checks.csv",
    )

    result = source_audit.review_source(
        "Example",
        "https://example.com",
    )

    assert result["homepage_http_status"] == 302
    assert "manual review required" in result["homepage_result"]


def test_append_audit_record_uses_consistent_columns(
    monkeypatch,
    tmp_path,
):
    output = tmp_path / "source_checks.csv"
    monkeypatch.setattr(source_audit, "AUDIT_OUTPUT", output)

    source_audit.append_audit_record({
        "source_name": "Example A",
        "base_url": "https://example.com",
    })
    source_audit.append_audit_record({
        "source_name": "Example B",
        "base_url": "https://example.org",
        "homepage_http_status": 200,
    })

    with output.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 2
    assert rows[0]["source_name"] == "Example A"
    assert rows[1]["source_name"] == "Example B"
    assert rows[0]["homepage_http_status"] == ""
    assert rows[1]["homepage_http_status"] == "200"
    assert rows[0]["automated_access_authorized"] == ""


def test_network_failure_is_recorded(
    monkeypatch,
    tmp_path,
):
    def fake_get(*args, **kwargs):
        raise source_audit.requests.ConnectionError("simulated failure")

    monkeypatch.setattr(source_audit.requests, "get", fake_get)
    monkeypatch.setattr(source_audit.time, "sleep", lambda _: None)
    monkeypatch.setattr(
        source_audit,
        "AUDIT_OUTPUT",
        tmp_path / "source_checks.csv",
    )

    result = source_audit.review_source(
        "Example",
        "https://example.com",
    )

    assert result["robots_allowed_for_root"] == "UNKNOWN"
    assert "ConnectionError" in result["robots_error"]
    assert result["automated_access_authorized"] == "NO"