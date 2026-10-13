"""
Conservative source extraction module.

This module intentionally does not provide a default target website.
Only use a source after its terms, intended use, and collection method
have been reviewed and authorized.

Public accessibility or a permissive robots.txt file alone does not
establish permission to collect personal information.
"""

import random
import time
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

import requests


MIN_DELAY_SECONDS = 1.5
MAX_DELAY_SECONDS = 3.0
DEFAULT_TIMEOUT_SECONDS = 15

BLOCKED_STATUS_CODES = {401, 403, 407, 429}


class SourceNotAuthorizedError(RuntimeError):
    """Raised when source authorization has not been confirmed."""


class SourceAccessBlockedError(RuntimeError):
    """Raised when the source denies or limits access."""


@dataclass(frozen=True)
class SourceConfig:
    """
    Explicit configuration for an approved source.

    authorized must be True only after the intended collection,
    fields, retention, and use have been reviewed and approved.
    """

    base_url: str
    authorized: bool = False
    authorization_reference: Optional[str] = None
    user_agent: str = "RealEstateLeadIntelligence/1.0"
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS

    def validate(self):
        """Validate configuration before making a request."""
        parsed = urlparse(self.base_url)

        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("Source URL must be a valid HTTPS URL")

        if not self.authorized:
            raise SourceNotAuthorizedError(
                "Source is not approved for automated collection."
            )

        if not self.authorization_reference or not (
            self.authorization_reference.strip()
        ):
            raise SourceNotAuthorizedError(
                "An authorization reference is required."
            )

        if not self.user_agent.strip():
            raise ValueError("A descriptive User-Agent is required")

        if self.timeout_seconds <= 0:
            raise ValueError("Timeout must be positive")


def fetch_authorized_page(
    config,
    url,
    previous_request_time=None,
    sleep_function=time.sleep,
    random_function=random.uniform,
):
    """
    Fetch one page only after source authorization is configured.

    This function does not bypass HTTP errors, authentication,
    CAPTCHAs, or other access controls.

    The caller is responsible for confirming that the requested URL
    belongs to the approved source and that the particular page and
    fields are within the authorization scope.
    """
    config.validate()

    requested = urlparse(url)
    approved = urlparse(config.base_url)

    if (
        requested.scheme != "https"
        or requested.netloc != approved.netloc
    ):
        raise ValueError(
            "Requested URL must use HTTPS and match the approved host."
        )

    # Respect a minimum gap between requests when the caller supplies
    # the previous request's timestamp. Jitter does not grant permission.
    if previous_request_time is not None:
        elapsed = time.monotonic() - previous_request_time
        delay = random_function(
            MIN_DELAY_SECONDS,
            MAX_DELAY_SECONDS,
        )
        sleep_function(max(0.0, delay - elapsed))

    headers = {
        "User-Agent": config.user_agent,
        "Accept": "text/html,application/xhtml+xml",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=config.timeout_seconds,
            allow_redirects=False,
        )
    except requests.RequestException:
        # Do not retry automatically; preserve the failure for audit.
        raise

    if response.status_code in BLOCKED_STATUS_CODES:
        raise SourceAccessBlockedError(
            f"Source returned HTTP {response.status_code}; "
            "stop and document the result."
        )

    if 300 <= response.status_code < 400:
        raise SourceAccessBlockedError(
            f"Source returned redirect HTTP {response.status_code}; "
            "review the redirect and authorization before proceeding."
        )

    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "").lower()

    if "text/html" not in content_type:
        raise ValueError(
            "Unexpected response content type; expected HTML."
        )

    return {
        "url": response.url,
        "status_code": response.status_code,
        "content_type": content_type,
        "html": response.text,
    }


if __name__ == "__main__":
    print(
        "Scraper is inactive by default. Review and authorize a source "
        "before configuring an extraction proof of concept."
    )
