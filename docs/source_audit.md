# Day 2 - Public Source Authorization Audit

**Project:** Amar Realty Lead Intelligence  
**Target markets:** Hadapsar and Fursungi, Pune  
**Audit date:** 13 October 2026

## Purpose
Identify public sources that may lawfully and technically support real-estate market research and prospect-intent analysis.

## Source review log

| Source | Intended use | robots.txt review | Terms reviewed | Automated access authorized | Decision |
|---|---|---|---|---|---|
| 99acres | Property-market context; buyer-intent use unconfirmed | Automated requests returned HTTP 403. Manual review notes are preserved in `evidence/robots.txt`. | Pending | No | Excluded from automated extraction pending permission and terms review |
| Reddit | Public discussion research | Not needed to reach the current exclusion decision | Reviewed according to project notes; retain official policy evidence if available | No | Exclude from automated extraction pending required permission |
| MahaRERA | Registered-project and market context | Automated requests returned HTTP 403; `evidence/robots.txt` records the manual Forbidden response | Pending | No | Excluded pending permission and a reliable access method |
| data.gov.in | Open-data market context | Not checked in the recorded evidence | Pending | Pending | Candidate only; review before use |
| OpenStreetMap Overpass API | Public amenity/geographic context | Not checked in the recorded evidence | Pending | Pending | Candidate only; review usage policy and rate limits before use |

## Evidence inventory
- `reports/robots_checks.csv`: four recorded source/path checks. The CSV has been repaired to a consistent 13-column schema. All four recorded automated robots.txt requests returned HTTP 403.
- `evidence/robots.txt`: manual browser notes for 99acres robots.txt and the MahaRERA Forbidden response.
- `evidence/robots.log`: output from the earlier checker run. This file is UTF-16 encoded; read it as UTF-16 or use a text editor that detects encoding.
- No screenshot file is included in the provided project archive. Do not refer to a screenshot as an attached deliverable unless one is added.

## Findings
- The recorded automated requests to 99acres and MahaRERA returned HTTP 403 for robots.txt. These results are treated as blocked; no attempt to bypass them was recorded.
- The manually viewed 99acres robots.txt lists disallowed paths including `/projects/`, `/top-projects/`, `/search/property/`, `/dealersearch/`, `/project_data/`, and `/registry-transactions*`.
- An HTTP 403 does not tell us the complete robots policy; it is not permission to proceed. The project therefore excludes both sources from automated extraction.
- A robots.txt allowance alone would not establish permission under terms of service or applicable privacy requirements.
- No source has been confirmed as authorized for collecting prospect contact data. No live prospect extraction is claimed.

## Compliance rules
- Do not bypass authentication, access controls, CAPTCHAs, or blocks.
- Review applicable terms and robots.txt before extraction.
- If a source is approved for automated access, respect the source's own rate limits and use a randomized delay of 1.5 to 3 seconds between requests where compatible with its policy.
- Collect only data necessary for an authorized purpose.
- Do not collect personal phone numbers from public discussions without an appropriate authorization and lawful basis.
- A syntactically valid phone number does not establish accuracy, ownership, consent, or permission to contact.
- Record actual request counts, outcomes, errors, and review findings. Do not claim unperformed checks.

## Day 2 status
Source-review tooling and tests are implemented. Live-source authorization and extraction remain pending. Project files do not independently verify whether a technical query email was sent or whether a response was received; confirm the actual email status before reporting it as sent or acknowledged.
