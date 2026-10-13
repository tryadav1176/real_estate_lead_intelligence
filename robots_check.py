"""Check robots.txt rules for SPECIFIC URLs and save dated evidence.

Usage (run from your project root, on your own machine):

    python robots_check.py --contact you@example.com \
        https://example.gov.in/projects/search https://example.gov.in/agents

What it does
  * Fetches https://<host>/robots.txt (follows up to 5 redirects, per RFC 9309)
  * Saves the exact robots.txt text to evidence/robots_<host>_<UTC time>.txt
  * Tells you, for each URL you pass, whether YOUR bot may fetch that path
  * Reports Crawl-delay / Request-rate / Sitemap lines
  * Appends one row per URL to reports/robots_checks.csv

What it does NOT do
  * It does not read Terms of Service. robots.txt answers "may a bot fetch this
    path?"; the ToS answers "am I allowed to use this data this way?". You must
    read the ToS yourself and record the clause (see docs/source_audit.md).
  * "ALLOWED" is never the same as "authorized".
"""

import argparse
import csv
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests

BOT_NAME = "AmarRealtyResearchBot"
TIMEOUT = 15
EVIDENCE_DIR = Path("evidence")
CSV_PATH = Path("reports") / "robots_checks.csv"


def fetch_robots(host_base: str, user_agent: str) -> dict:
    """Return robots.txt status and text. Conservative on errors."""
    url = f"{host_base}/robots.txt"
    out = {"robots_url": url, "http_status": "", "state": "", "text": "", "note": ""}
    try:
        r = requests.get(
            url,
            headers={"User-Agent": user_agent},
            timeout=TIMEOUT,
            allow_redirects=True,  # RFC 9309: follow up to 5 redirects
        )
        if len(r.history) > 5:
            out.update(state="UNKNOWN", note="More than 5 redirects; treat as do-not-crawl")
            return out
        out["http_status"] = r.status_code
        if 200 <= r.status_code < 300:
            out.update(state="RULES", text=r.text)
        elif r.status_code in (401, 403):
            out.update(state="DISALLOW_ALL", note="Access to robots.txt is restricted; treat as blocked")
        elif 400 <= r.status_code < 500:
            out.update(
                state="NO_RULES",
                note="No robots.txt published. This is NOT permission; the ToS still decides.",
            )
        else:
            out.update(state="UNKNOWN", note="Server error; do not crawl until it resolves")
    except requests.RequestException as exc:
        out.update(state="UNKNOWN", note=f"{type(exc).__name__}: {exc}")
    return out


def evaluate(url: str, robots: dict, bot: str, user_agent: str) -> dict:
    """Decide for one URL. Returns a result row."""
    row = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "url": url,
        "robots_url": robots["robots_url"],
        "robots_http_status": robots["http_status"],
        "robots_state": robots["state"],
        "can_fetch": "NO",
        "crawl_delay": "",
        "request_rate": "",
        "sitemaps": "",
        "note": robots["note"],
        "terms_url": "",          # fill in by hand
        "terms_clause_quoted": "",  # fill in by hand
        "authorized_decision": "PENDING",  # fill in by hand after reading ToS
    }

    if robots["state"] == "RULES":
        parser = RobotFileParser()
        parser.parse(robots["text"].splitlines())
        row["can_fetch"] = "YES" if parser.can_fetch(bot, url) else "NO"
        delay = parser.crawl_delay(bot)
        rate = parser.request_rate(bot)
        row["crawl_delay"] = delay if delay is not None else ""
        row["request_rate"] = f"{rate.requests}/{rate.seconds}s" if rate else ""
        row["sitemaps"] = " ".join(parser.site_maps() or [])
    elif robots["state"] == "NO_RULES":
        row["can_fetch"] = "YES (no robots.txt; ToS still required)"
    return row


def save_evidence(host: str, robots: dict) -> str:
    EVIDENCE_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_host = re.sub(r"[^A-Za-z0-9.-]", "_", host)
    path = EVIDENCE_DIR / f"robots_{safe_host}_{stamp}.txt"
    header = (
        f"# Fetched: {datetime.now(timezone.utc).isoformat()}\n"
        f"# URL: {robots['robots_url']}\n"
        f"# HTTP status: {robots['http_status']}\n"
        f"# State: {robots['state']}\n\n"
    )
    path.write_text(header + robots["text"], encoding="utf-8")
    return str(path)


def append_csv(rows: list) -> None:
    CSV_PATH.parent.mkdir(exist_ok=True)
    new_file = not CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if new_file:
            w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="+", help="Exact page URLs you intend to fetch")
    ap.add_argument("--contact", required=True, help="Your real email or URL, placed in the User-Agent")
    args = ap.parse_args()

    user_agent = f"{BOT_NAME}/0.1 (research; contact: {args.contact})"

    by_host: dict = {}
    for u in args.urls:
        p = urlparse(u)
        if p.scheme not in ("http", "https") or not p.hostname or p.username or p.password:
            print(f"SKIP invalid URL: {u}")
            continue
        by_host.setdefault(f"{p.scheme}://{p.netloc}", []).append(u)

    all_rows = []
    for base, urls in by_host.items():
        robots = fetch_robots(base, user_agent)
        saved = save_evidence(urlparse(base).netloc, robots) if robots["text"] else "(no text to save)"
        print(f"\n== {base}  robots.txt HTTP {robots['http_status'] or 'n/a'}  state={robots['state']}")
        print(f"   evidence file: {saved}")
        if robots["note"]:
            print(f"   note: {robots['note']}")
        for u in urls:
            row = evaluate(u, robots, BOT_NAME, user_agent)
            all_rows.append(row)
            print(f"   {row['can_fetch']:<8} {u}")
            if row["crawl_delay"] != "":
                print(f"            Crawl-delay: {row['crawl_delay']}s (use max of this and your 1.5-3.0s jitter)")
            if row["sitemaps"]:
                print(f"            Sitemaps: {row['sitemaps']}")

    if all_rows:
        append_csv(all_rows)
        print(f"\nLogged {len(all_rows)} row(s) to {CSV_PATH}")
        print("Next: read the site's Terms of Service by hand and fill the terms_* and authorized_decision columns.")


if __name__ == "__main__":
    main()