
import pytest
import requests

from src.scraper import (
    SourceConfig,
    SourceNotAuthorizedError,
    SourceAccessBlockedError,
    fetch_authorized_page,
)


@pytest.fixture
def authorized_config():
    """Synthetic configuration for mocked tests only."""
    return SourceConfig(
        base_url="https://example.com",
        authorized=True,
        authorization_reference="TEST-AUTH-001",
        user_agent="TestAgent/1.0",
    )


def make_response(
    status_code=200,
    text="<html><body>Test</body></html>",
    headers=None,
):
    """Create a minimal mocked HTTP response."""
    class FakeResponse:
        def __init__(self):
            self.status_code = status_code
            self.text = text
            self.headers = headers or {
                "Content-Type": "text/html; charset=utf-8"
            }
            self.url = "https://example.com/test"

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.HTTPError(
                    f"HTTP {self.status_code}"
                )

    return FakeResponse()


def test_unauthorized_source_is_rejected(monkeypatch):
    def unexpected_request(*args, **kwargs):
        pytest.fail("HTTP request must not occur for an unauthorized source")

    monkeypatch.setattr(
        "src.scraper.requests.get",
        unexpected_request,
    )

    config = SourceConfig(
        base_url="https://example.com",
        authorized=False,
        authorization_reference=None,
    )

    with pytest.raises(SourceNotAuthorizedError):
        fetch_authorized_page(config, "https://example.com/page")


def test_missing_authorization_reference_is_rejected():
    config = SourceConfig(
        base_url="https://example.com",
        authorized=True,
        authorization_reference=" ",
    )

    with pytest.raises(SourceNotAuthorizedError):
        fetch_authorized_page(config, "https://example.com/page")


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com/page",
        "https://another-example.com/page",
        "https://example.com.evil.test/page",
    ],
)
def test_unapproved_url_is_rejected(
    authorized_config,
    url,
    monkeypatch,
):
    def unexpected_request(*args, **kwargs):
        pytest.fail("No request should be made to an unapproved URL")

    monkeypatch.setattr(
        "src.scraper.requests.get",
        unexpected_request,
    )

    with pytest.raises(ValueError):
        fetch_authorized_page(authorized_config, url)


def test_invalid_base_url_is_rejected():
    config = SourceConfig(
        base_url="http://example.com",
        authorized=True,
        authorization_reference="TEST-AUTH-001",
    )

    with pytest.raises(ValueError):
        config.validate()


def test_successful_html_response(
    authorized_config,
    monkeypatch,
):
    expected = make_response()

    def fake_get(url, **kwargs):
        assert url == "https://example.com/test"
        assert kwargs["allow_redirects"] is False
        assert kwargs["timeout"] > 0
        assert "User-Agent" in kwargs["headers"]
        return expected

    monkeypatch.setattr(
        "src.scraper.requests.get",
        fake_get,
    )

    result = fetch_authorized_page(
        authorized_config,
        "https://example.com/test",
    )

    assert result["status_code"] == 200
    assert "text/html" in result["content_type"]
    assert result["html"] == "<html><body>Test</body></html>"
    assert result["url"] == "https://example.com/test"


@pytest.mark.parametrize("status_code", [401, 403, 407, 429])
def test_blocked_responses_raise_without_retry(
    authorized_config,
    monkeypatch,
    status_code,
):
    calls = []

    def fake_get(url, **kwargs):
        calls.append(url)
        return make_response(status_code=status_code)

    monkeypatch.setattr(
        "src.scraper.requests.get",
        fake_get,
    )

    with pytest.raises(SourceAccessBlockedError):
        fetch_authorized_page(
            authorized_config,
            "https://example.com/test",
        )

    assert len(calls) == 1


@pytest.mark.parametrize("status_code", [301, 302, 307, 308])
def test_redirects_are_not_followed(
    authorized_config,
    monkeypatch,
    status_code,
):
    calls = []

    def fake_get(url, **kwargs):
        calls.append(kwargs["allow_redirects"])
        return make_response(status_code=status_code)

    monkeypatch.setattr(
        "src.scraper.requests.get",
        fake_get,
    )

    with pytest.raises(SourceAccessBlockedError):
        fetch_authorized_page(
            authorized_config,
            "https://example.com/test",
        )

    assert calls == [False]


def test_non_html_response_is_rejected(
    authorized_config,
    monkeypatch,
):
    monkeypatch.setattr(
        "src.scraper.requests.get",
        lambda *args, **kwargs: make_response(
            headers={"Content-Type": "application/pdf"}
        ),
    )

    with pytest.raises(ValueError, match="expected HTML"):
        fetch_authorized_page(
            authorized_config,
            "https://example.com/test",
        )


def test_network_failure_is_not_retried(
    authorized_config,
    monkeypatch,
):
    calls = []

    def fake_get(*args, **kwargs):
        calls.append(1)
        raise requests.ConnectionError("Synthetic network failure")

    monkeypatch.setattr(
        "src.scraper.requests.get",
        fake_get,
    )

    with pytest.raises(requests.ConnectionError):
        fetch_authorized_page(
            authorized_config,
            "https://example.com/test",
        )

    assert len(calls) == 1


def test_request_delay_uses_monotonic_elapsed_time(
    authorized_config,
    monkeypatch,
):
    sleeps = []

    monkeypatch.setattr(
        "src.scraper.time.monotonic",
        lambda: 100.0,
    )
    monkeypatch.setattr(
        "src.scraper.requests.get",
        lambda *args, **kwargs: make_response(),
    )

    fetch_authorized_page(
        authorized_config,
        "https://example.com/test",
        previous_request_time=99.0,
        sleep_function=sleeps.append,
        random_function=lambda minimum, maximum: 2.0,
    )

    # Two seconds requested minus one second already elapsed.
    assert sleeps == [1.0]
