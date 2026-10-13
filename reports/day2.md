# CANDIDATE DAILY PROGRESS REPORT (DPR)

**Candidate Name:** Tejas Rajendra Yadav  
**Target Role:** Lead Intelligence & Data Engineer  
**Evaluation Day:** Day 2  
**Date:** 13/10/2026  
**Git Commit Hash:** [PASTE OUTPUT OF `git rev-parse --short HEAD`]  
**Repository:** https://github.com/tryadav1176/real_estate_lead_intelligence

## 1. Daily Engineering Tasks Completed

- Built `src/source_audit.py` and `tests/test_source_audit.py` (mocked HTTP) for URL validation, robots.txt review and conservative authorization decisions.
- Built `robots_check.py`, a standalone checker that tests specific URLs against a site's robots.txt, saves a dated copy of the file as evidence, reports Crawl-delay, and logs results to `reports/robots_checks.csv`.
- Ran the checker against candidate sources (see Section 3) and reviewed 99acres robots.txt manually in a browser after the automated request was blocked.
- Updated `.gitignore` so real extracted data under `data/raw/` cannot be committed (only the synthetic sample is tracked).
- Sent a technical query with proof of concept to tech@amarrealty.co.in on [DATE/TIME IST] asking which source is authorized for prospect data.
- Existing cleaning, deduplication, scoring, CSV and SQLite pipeline unchanged.

**Extraction status:** No live extraction was performed. No source has been confirmed as authorized.

## 2. Technical Stack Utilized

Python, requests, urllib.robotparser, Pandas, SQLite3, pytest, Git/GitHub. BeautifulSoup and Playwright installed; not used for live extraction.

## 3. Compliance & Scraping Throttling Audit

| Source | robots.txt result | Terms reviewed | Decision |
|---|---|---|---|
| 99acres | Automated request: HTTP 403. Manual browser review: allows the city landing page; disallows `/projects/`, `/top-projects/`, `/search/property/`, `/dealersearch/`, `/project_data/`, `/registry-transactions*`. Evidence: `evidence/robots_99acres_manual_20261013.txt` | [YES/NO; quote clause in `docs/source_audit.md`] | Excluded from automated extraction |
| MahaRERA | Automated request: HTTP 403. Browser also showed "Forbidden" for [EXACT URL]. Evidence: [screenshot filename] | [YES/NO] | Excluded pending written permission |
| data.gov.in | [HTTP status / result, or "not yet checked"] | [YES/NO] | [decision] |
| Overpass API | [HTTP status / result, or "not yet checked"] | [YES/NO] | [decision] |

- **Robots.txt Adherence:** Checked before any content request. No disallowed path was requested, and no block was bypassed (no User-Agent spoofing, proxies or browser impersonation).
- **Rate Limiting:** Randomized 1.5s–3.0s delay is implemented in `source_audit.py`. `robots_check.py` makes one robots.txt request per host per run. Total requests made: [N, from `reports/robots_checks.csv` and your run history].
- **HTTP Errors:** 403 from 99acres and MahaRERA (robots.txt). [Add others.]

## 4. Pipeline Operational Metrics

| Metric | Live result (Day 2) |
|---|---:|
| Live content requests | 0 |
| Raw Ingestion Count | 0 |
| Records Dropped (Invalid/Junk) | 0 |
| Duplicate Count Removed | 0 |
| Cumulative Clean Prospects Stored | 0 / 100 |

Synthetic regression test (not real prospects): 5 raw, 1 invalid, 1 duplicate, 3 clean. Automated tests: [19 passed, re-run `python -m pytest` and confirm]. `robots_check.py` is not yet covered by pytest.

## 5. Technical Challenges & Proof of Concept (PoC) Solutions

**Blocker:** The two main candidate sources actively block automated access, and no authorized source has been confirmed for prospect contact data. A valid mobile number is not proof of consent or permission to contact, and collection must be consistent with DPDP.

**PoC:** `python robots_check.py --contact [EMAIL] "https://www.99acres.com/Pune-Real-Estate.htm" "https://www.maharera.maharashtra.gov.in/"` returned HTTP 403 for both robots.txt requests. Log and CSV are in `evidence/` and `reports/`.

**Resolution:** Excluded both sources, preserved evidence, and escalated to the technical desk with three questions: (1) which source is authorized or will one be supplied, (2) what lawful basis applies to mobile numbers, (3) whether Day 3 and Day 5 benchmarks may use clearly labelled synthetic data. Awaiting response (SLA: 10:00 AM IST next business day).

## 6. Attached Deliverables

- `robots_check.py`
- `reports/robots_checks.csv`
- `evidence/` (robots.txt copies, run log, screenshot)
- `src/source_audit.py`, `tests/test_source_audit.py`
- `docs/source_audit.md`
- `.gitignore`
- `reports/day2.md`

## 7. Next-Day Plan

- Apply the tech desk's reply to source selection. If an approved source is confirmed, build a minimal extraction proof of concept in `src/scraper.py` (currently empty) with robots checks and 1.5s–3.0s jitter enforced.
- Cover `robots_check.py` with unit tests.
- Fix `save_leads()` to report rows actually inserted.
- Update README structure and status.