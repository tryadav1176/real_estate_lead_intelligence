# Day 2 - Public Source Authorization Audit

**Project:** Amar Realty Lead Intelligence
**Target markets:** Hadapsar and Fursungi, Pune
**Audit date:** 13 October 2026

## Purpose
Identify public sources that may lawfully and technically support real-estate market research and prospect-intent analysis.

## Source review log

| Source | Intended use | robots.txt checked | Terms reviewed | Automated access authorized | Decision |
|---|---|---|---|---|---|
| 99acres | Property-market context; buyer-intent use unconfirmed | Yes, 13/10/2026. Automated request returned HTTP 403. Manual browser review: city landing page not disallowed; `/projects/`, `/top-projects/`, `/search/property/`, `/dealersearch/`, `/project_data/`, `/registry-transactions*` disallowed | Pending | No | Excluded from automated extraction |
| Reddit | Public discussion research | Not required to establish policy decision | Reviewed | No - authorization not obtained | Exclude from automated extraction pending permission |
| Official MahaRERA website | Registered-project and market context | Attempted, 13/10/2026. Automated request returned HTTP 403; browser also showed "Forbidden" | Pending | No | Excluded pending written permission |
| data.gov.in | Open-data market context | [Result, or "Not yet checked"] | [Pending / Reviewed] | [Pending] | [Decision] |
| OpenStreetMap Overpass API | Public amenity and agent-office data | [Result, or "Not yet checked"] | [Pending / Reviewed] | [Pending] | [Decision] |

## Evidence
- `reports/robots_checks.csv`: logged results of automated robots.txt requests (2 requests as of this review; update if more are run).
- `evidence/robots_99acres_manual_20261013.txt`: robots.txt text viewed manually in a browser.
- `evidence/run_20261013.log`: terminal output of the checker.
- `evidence/` MahaRERA "Forbidden" screenshot: [filename].
- Reproduce with `python robots_check.py --contact <email> "<url>"`.

## Findings
- 99acres and MahaRERA both returned HTTP 403 to an identified, rate-limited bot. This is treated as blocked, and no attempt was made to bypass it (no User-Agent spoofing, proxies, or browser impersonation).
- A robots.txt result of "allowed" does not establish authorization; the Terms of Use still govern, and they have not yet been reviewed for 99acres or MahaRERA.
- No source has been confirmed as authorized for collecting prospect contact data.

## Compliance rules
- Do not bypass authentication, access controls, CAPTCHAs, or blocks.
- Review applicable terms and robots.txt before automated requests.
- Where permitted, use a random delay of 1.5 to 3 seconds between requests.
- Collect only data necessary for an authorized purpose.
- Do not extract or infer personal phone numbers from public discussions without an appropriate authorization and lawful basis.
- A syntactically valid phone number is not proof of accuracy, consent, or permission to contact.
- Record actual request counts, outcomes, errors, and review findings. Never report unperformed checks as completed.

## Day 2 status
Source authorization is not yet confirmed. No live extraction has been performed. A technical query with proof of concept was sent to tech@amarrealty.co.in on [DATE/TIME IST] asking which source is authorized, what lawful basis applies to mobile numbers, and whether synthetic data may be used for Day 3 and Day 5 benchmarks. Awaiting response; any written reply will be recorded here before a source is used.