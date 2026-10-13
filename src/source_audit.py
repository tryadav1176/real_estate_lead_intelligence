"""
Conservative source review utility.

This utility records robots.txt and minimal homepage review results.
It does not scrape property listings, collect personal data, or grant
permission to automate access to a website.
"""

import csv
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUDIT_OUTPUT = PROJECT_ROOT / "reports" / "source_checks.csv"

USER_AGENT = (
    "AmarRealtyResearchBot/0.1 "
    "(source review; contact: project contact to be confirmed)"
)
MIN_DELAY_SECONDS = 1.5
MAX_DELAY_SECONDS = 3.0
TIMEOUT_SECONDS = 15

AUDIT_FIELDS = [
    "checked_at_utc",
    "source_name",
    "base_url",
    "robots_url",
    "robots_http_status",
    "robots_allowed_for_root",
    "robots_error",
    "homepage_http_status",
    "homepage_result",
    "terms_reviewed",
    "automated_access_authorized",
]


def validate_base_url(url: str) -> str:
    """Accept a well-formed public HTTP(S) URL without credentials."""
    parsed = urlparse(url.strip())

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must start with http:// or https://")

    if not parsed.hostname:
        raise ValueError("URL must include a hostname")

    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not allowed")

    if parsed.query or parsed.fragment:
        raise ValueError("Provide a base URL without query or fragment")

    return f"{parsed.scheme}://{parsed.netloc}"


def check_robots(base_url: str) -> dict:
    """
    Fetch robots.txt and evaluate the declared user agent.

    An unavailable or inconclusive robots file is UNKNOWN, never
    interpreted as permission to collect data.
    """
    robots_url = f"{base_url}/robots.txt"

    result = {
        "robots_url": robots_url,
        "robots_http_status": "",
        "robots_allowed_for_root": "UNKNOWN",
        "robots_error": "",
    }

    try:
        response = requests.get(
            robots_url,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT_SECONDS,
            allow_redirects=False,
        )

        result["robots_http_status"] = response.status_code

        if response.status_code == 200:
            parser = RobotFileParser()
            parser.set_url(robots_url)
            parser.parse(response.text.splitlines())

            result["robots_allowed_for_root"] = (
                "YES"
                if parser.can_fetch(USER_AGENT, base_url + "/")
                else "NO"
            )

        elif response.status_code == 404:
            result["robots_error"] = (
                "robots.txt does not establish authorization; HTTP 404"
            )

        elif response.status_code in {401, 403, 407, 429}:
            result["robots_error"] = (
                f"Access denied or rate limited: HTTP "
                f"{response.status_code}; no retry attempted"
            )

        elif 300 <= response.status_code < 400:
            result["robots_error"] = (
                f"Redirect returned: HTTP {response.status_code}; "
                "manual review required"
            )

        else:
            result["robots_error"] = (
                "robots.txt could not be reliably evaluated; "
                "manual review required"
            )

    except requests.RequestException as exc:
        result["robots_error"] = f"{type(exc).__name__}: {exc}"

    return result


def append_audit_record(record: dict) -> None:
    """
    Append a record using a consistent CSV schema.

    Existing columns are preserved, and missing values are written
    as empty cells. This supports records with the same audit schema.
    """
    AUDIT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    file_exists = AUDIT_OUTPUT.exists() and AUDIT_OUTPUT.stat().st_size > 0

    with AUDIT_OUTPUT.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=AUDIT_FIELDS,
            extrasaction="ignore",
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            field: record.get(field, "")
            for field in AUDIT_FIELDS
        })


def review_source(name: str, url: str) -> dict:
    """
    Record a minimal robots and homepage review.

    This is not an authorization decision. The source's applicable
    terms, data-use conditions, and intended purpose must be reviewed
    separately before any collection beyond this limited check.
    """
    base_url = validate_base_url(url)

    time.sleep(random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS))
    robots = check_robots(base_url)

    record = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_name": name,
        "base_url": base_url,
        **robots,
        "homepage_http_status": "",
        "homepage_result": (
            "SKIPPED - robots status not confirmed allowed"
        ),
        "terms_reviewed": "NO",
        "automated_access_authorized": "NO",
    }

    if robots["robots_allowed_for_root"] == "YES":
        time.sleep(random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS))

        try:
            response = requests.get(
                base_url + "/",
                headers={"User-Agent": USER_AGENT},
                timeout=TIMEOUT_SECONDS,
                allow_redirects=False,
            )

            record["homepage_http_status"] = response.status_code

            if response.status_code in {401, 403, 407, 429}:
                record["homepage_result"] = (
                    f"Access denied or rate limited: HTTP "
                    f"{response.status_code}; no retry attempted"
                )
            elif 300 <= response.status_code < 400:
                record["homepage_result"] = (
                    f"Redirect returned: HTTP {response.status_code}; "
                    "manual review required"
                )
            elif 200 <= response.status_code < 300:
                record["homepage_result"] = (
                    "Homepage response recorded; terms and authorization "
                    "still require separate review"
                )
            else:
                record["homepage_result"] = (
                    f"Homepage returned HTTP {response.status_code}"
                )

        except requests.RequestException as exc:
            record["homepage_result"] = (
                f"Request failed: {type(exc).__name__}: {exc}"
            )

    append_audit_record(record)
    return record


if __name__ == "__main__":
    print("Source review utility is ready.")
    print(f"Audit output: {AUDIT_OUTPUT}")
    print("Importing this module does not make network requests.")
    print("Call review_source() only after reviewing the intended source.")