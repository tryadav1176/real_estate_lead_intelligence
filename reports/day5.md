# CANDIDATE DAILY PROGRESS REPORT (DPR)

- **Candidate Name:** Tejas Rajendra Yadav
- **Target Role:** Lead Intelligence & Data Engineer
- **Evaluation Day:** Day 5
- **Date:** 16/10/2026
- **Git Commit Hash:** `d5a15ef` 
- **Repository:** https://github.com/tryadav1176/real_estate_lead_intelligence

## Status summary (completed vs pending)

| Desk task | Status | Detail |
|---|---|---|
| 1. Identify usable lead sources | **Partial / blocked** | 13 sources named, 8 hosts robots.txt-tested, 0 authorized for automated collection. 3 policy reviews complete, 5 pending. |
| 2. Demonstrate actual intent discovery | **Not done / blocked** | No authorized source. Reddit sample on hold, as instructed, until policy review is complete and the desk confirms. 0 intent signals. |
| 3. Demonstrate working pipeline | **Partial** | 132 automated tests pass. Not run on source data because none is permitted. Untested or incomplete items listed in Section 5. |
| 4. Report actual results | **Done** | All six required metrics reported as 0 (Section 4). |
| 5. Submit Day 5 evidence | **Partial** | Register, robots.txt log and test log committed. Pending items listed in Section 5. |

## 1. Daily Engineering Tasks Completed

- Completed review of Reddit's Public Content Policy and Privacy Policy, and YouTube's API Services Developer Policies. Findings are recorded in `docs/source_discovery.md`.
- Corrected the source audit log `reports/robots_checks.csv` (13 rows, one per robots.txt request/URL, no duplicates) and recorded a decision for every source.
- Rewrote `docs/source_discovery.md` with named sources, access results, policy findings, permitted-route options and actual metrics.
- Ran the full automated test suite and saved the output: 132 passed in 3.82s (`evidence/pytest_day5.log`).
- Evaluated alternative routes: YouTube Data API (unsuitable for a persistent prospect database because of its 30-day storage limit and other restrictions), Google Trends manual export (aggregate demand only), a consent-based opt-in form, and Amar Realty's own channels (the last two need desk confirmation).
- Query on acceptable permitted-source routes sent to tech@amarrealty.co.in: **[FILL: date and time IST, or "not yet sent"]**.

## 2. Technical Stack Utilized

Python, requests, urllib.robotparser, pandas, SQLite3, pytest, Git/GitHub.

## 3. Compliance & Scraping Throttling Audit

- **Targets tested (robots.txt only):** 99acres, MahaRERA, IGR e-search, PMC Open Data, PMC Development Plan PDF host, MagicBricks, Reddit, OpenStreetMap Overpass.
- **Robots.txt Adherence:** only robots.txt files were requested. No page content was fetched from any source, and no disallowed path was requested.
- **Requests made:** 11 robots.txt requests in total (4 on 13/10, 7 on 15/10), one per host per run, with an identified User-Agent.
- **Responses:** HTTP 403 x7 (from 4 hosts: 99acres, MahaRERA, PMC plan PDF host, MagicBricks); HTTP 404 x2 (IGR, PMC Open Data); HTTP 200 x2 (Reddit: `Disallow: /` for all bots; Overpass: `Disallow: /api/`).
- **Rate limiting:** the 1.5s-3.0s jitter is implemented in the guarded scraper and covered by tests, but no content requests were made, so it was not exercised against any source.
- **Access restrictions:** none bypassed. No User-Agent spoofing, proxies, mirror sites or browser automation.

## 4. Pipeline Operational Metrics

| Metric | Value |
|---|---|
| Authorized sources successfully used | 0 |
| Genuine source records collected | 0 |
| Unique records processed | 0 |
| Genuine property-intent signals identified | 0 |
| Valid Indian mobile numbers obtained through permitted means | 0 |
| Qualified prospects meeting the agreed criteria | 0 |
| Raw Ingestion Count / Records Dropped / Duplicates Removed | 0 / 0 / 0 |
| Cumulative Clean Prospects Stored | 0 / 100 |

No synthetic data was processed or committed as a Day 5 result. The test suite uses in-code fixtures, which are test evidence and are not counted above. Mobile-number format validation does not establish ownership, consent or eligibility for contact.

## 5. Technical Challenges & Proof of Concept (PoC) Solutions

**Blocker:** no source has been authorized for genuine, permitted property-intent collection. Sources that expose individuals' posts (Reddit, YouTube) restrict lead harvesting; listing and registry portals returned HTTP 403 or are supply-side data.

**Resolution so far:** documented each source with its evidence, did not bypass any restriction, evaluated alternatives, and asked the desk which route it accepts.

**Test evidence:** `python -m pytest -v` gives 132 passed (`evidence/pytest_day5.log`). Coverage: mobile validation, normalization, deduplication, scoring, database persistence and migration, guarded scraper behaviour, source-audit tooling.

**Incomplete or untested components:**
- Automated intent classification is not implemented in code; the rules are documented in `docs/intent_classification_guide.md`.
- No source adapter exists yet, because no source is approved.
- Free-text normalization is only tested on exact aliases (for example "Hadapsar, Pune" and "2-BHK" are not tested).
- CSV loading with blank mobile cells is not yet handled safely (needs `dtype=str`).
- No saved processing log yet.
- Policy reviews pending: Reddit Developer Terms and User Agreement, PMC Open Data licence, OSM / Overpass usage policy, IGR website policy.
- Google Trends manual export not yet done.

**Next actions:** act on the desk's reply; read and quote the five pending policies; Google Trends export as a market-level indicator only; add intent handling and a source adapter; fix the CSV and normalization gaps.

## 6. Attached Deliverables

`robots_check.py`, `reports/robots_checks.csv`, `docs/source_discovery.md`, `docs/intent_classification_guide.md`, `src/intent_summary.py`, `evidence/` (robots.txt copies, run logs, `pytest_day5.log`), `reports/day5.md`