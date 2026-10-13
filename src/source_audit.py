
"""Conservative source review utility for the Day 2 audit.

This tool checks robots.txt and records review evidence.
It does not scrape listings, collect personal data, or grant
permission to automate access to a website.
"""

import random
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUDIT_OUTPUT = PROJECT_ROOT / "reports" / "source_checks.csv"

USER_AGENT = "AmarRealtyResearchBot/0.1 (source review; contact: authorized project contact)"
MIN_DELAY_SECONDS = 1.5
MAX_DELAY_SECONDS = 3.0
TIMEOUT_SECONDS = 15


def validate_base_url(url: str) -> str:
    """Accept only a well-formed public HTTP(S) base URL."""
    parsed = urlparse(url.strip())

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must start with http:// or https://")

    if not parsed.hostname:
        raise ValueError("URL must include a hostname")

    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not allowed")

    return f"{parsed.scheme}://{parsed.netloc}"


def check_robots(base_url: str) -> dict:
    """Fetch robots.txt and evaluate permission for the declared user agent.

    An unavailable robots.txt is reported as unknown, not as permission.
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
                "YES" if parser.can_fetch(USER_AGENT, base_url + "/") else "NO"
            )
        elif response.status_code == 404:
            result["robots_allowed_for_root"] = "UNKNOWN"
            result["robots_error"] = (
                "robots.txt returned 404; this does not establish authorization"
            )
        else:
            result["robots_allowed_for_root"] = "UNKNOWN"
            result["robots_error"] = (
                "robots.txt could not be reliably evaluated; review manually"
            )

    except requests.RequestException as exc:
        result["robots_error"] = f"{type(exc).__name__}: {exc}"

    return result


def review_source(name: str, url: str) -> dict:
    """Record a minimal homepage response and robots.txt review result.

    Run only against sources that you are permitted to access.
    This function does not follow redirects or crawl page links.
    """
    base_url = validate_base_url(url)

    # Respect the required delay between network requests.
    time.sleep(random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS))

    robots = check_robots(base_url)

    # Do not proceed to a homepage request if robots status is unclear
    # or indicates disallow for the root path.
    if robots["robots_allowed_for_root"] != "YES":
        return {
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_name": name,
            "base_url": base_url,
            **robots,
            "homepage_http_status": "",
            "homepage_result": "SKIPPED - robots status not confirmed allowed",
            "terms_reviewed": "NO",
            "automated_access_authorized": "NO",
        }

    time.sleep(random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS))

    try:
        response = requests.get(
            base_url + "/",
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT_SECONDS,
            allow_redirects=False,
        )
        homepage_status = response.status_code
        homepage_result = (
            "HTTP response recorded; terms and authorization still require review"
        )
    except requests.RequestException as exc:
        homepage_status = ""
        homepage_result = f"Request failed: {type(exc).__name__}: {exc}"

    return {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_name": name,
        "base_url": base_url,
        **robots,
        "homepage_http_status": homepage_status,
        "homepage_result": homepage_result,
        "terms_reviewed": "NO",
        "automated_access_authorized": "NO",
    }


def append_audit_record(record: dict) -> None:
    """Append a review result to CSV without replacing earlier records."""
    import csv

    AUDIT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    file_exists = AUDIT_OUTPUT.exists()
    fields = list(record.keys())

    with AUDIT_OUTPUT.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        if not file_exists:
            writer.writeheader()

        writer.writerow(record)


if __name__ == "__main__":
    print("Source review utility created.")
    print("No website has been checked by importing this module.")
    print(f"Audit output: {AUDIT_OUTPUT}")
    print("Review applicable terms and authorization before running live checks.")

