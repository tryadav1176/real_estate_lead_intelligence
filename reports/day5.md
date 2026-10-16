# CANDIDATE DAILY PROGRESS REPORT (DPR)

- **Candidate Name:** Tejas Rajendra Yadav
- **Target Role:** Lead Intelligence & Data Engineer
- **Evaluation Day:** Day 5
- **Date:** 16/10/2026
- **Git Commit Hash:** `
- **Repository:** https://github.com/tryadav1176/real_estate_lead_intelligence

## Status summary (completed vs pending)

| Desk task | Status | Detail |
|---|---|---|
| 1. Identify usable lead sources | **Partial / blocked** | 13 sources named, 8 hosts robots.txt-tested, 0 authorized for automated B2C collection. Policy reviews for Reddit Developer Terms and PMC Open Data (GODL) completed. |
| 2. Demonstrate actual intent discovery | **Not done / blocked** | No authorized source. Reddit sample on hold, as instructed, until the desk confirms. 0 actual intent signals processed. |
| 3. Demonstrate working pipeline | **Partial** | Automated intent classification and `BaseSourceAdapter` implemented. CSV ingest bug fixed. Not run on genuine source data because none is authorized yet. |
| 4. Report actual results | **Done** | All six required metrics reported as 0 (Section 4). |
| 5. Submit Day 5 evidence | **Partial** | Register, robots.txt log, pipeline updates, and test log committed. Google Trends alternative pending. |

## 1. Daily Engineering Tasks Completed

- Completed policy review for Government Open Data (PMC / data.gov.in) noting the Government Open Data Licence - India (GODL) permits commercial/non-commercial reuse with attribution. Documented in `docs/source_discovery.md`.
- Completed policy review for Reddit, documenting that Developer Terms strictly restrict third-party access to official APIs and prohibit bulk scraping for commercial lead generation without direct consent.
- Implemented `classify_intent` logic in `src/scorer.py` mapping text to the six required taxonomy categories: direct purchase, emerging purchase, rental, seller listing, geographic context, and unknown.
- Created `src/adapter.py` establishing a `BaseSourceAdapter` and `ApprovedAPIAdapter` architecture to dynamically handle ingestion once a source is authorized.
- Resolved the CSV loading gap in `src/pipeline.py` by enforcing `dtype={"Mobile_Number": str}` to safely handle blank mobile cells and prevent float conversion failures.
- Ran the full automated test suite and saved the output (`evidence/pytest_day5.log`).
- Sent query on acceptable permitted-source routes to tech@amarrealty.co.in: **[FILL: time IST]**.

## 2. Technical Stack Utilized

Python, requests, urllib.robotparser, pandas, SQLite3, pytest, Git/GitHub. (No commercial scraping APIs utilized)[cite: 3].

## 3. Compliance & Scraping Throttling Audit

- **Targets tested (robots.txt only):** 99acres, MahaRERA, IGR e-search, PMC Open Data, PMC Development Plan PDF host, MagicBricks, Reddit, OpenStreetMap Overpass.
- **Robots.txt Adherence:** only robots.txt files were requested. No page content was fetched from any source, and no disallowed path was requested[cite: 3].
- **Requests made:** 11 robots.txt requests in total (4 on 13/10, 7 on 15/10), one per host per run, with an identified User-Agent.
- **Responses:** HTTP 403 x7 (from 4 hosts: 99acres, MahaRERA, PMC plan PDF host, MagicBricks); HTTP 404 x2 (IGR, PMC Open Data); HTTP 200 x2 (Reddit: `Disallow: /` for all bots; Overpass: `Disallow: /api/`).
- **Rate limiting:** the 1.5s-3.0s jitter is implemented in the guarded scraper, but no content requests were made, so it was not exercised against any source[cite: 2, 3].
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

No synthetic data was processed or committed as a Day 5 result[cite: 3]. Mobile-number format validation does not establish ownership, consent or eligibility for contact[cite: 3].

## 5. Technical Challenges & Proof of Concept (PoC) Solutions

**Blocker:** No source has been authorized for genuine, permitted property-intent collection[cite: 3]. Sources that expose individuals' posts (Reddit, YouTube) restrict lead harvesting[cite: 3]; listing and registry portals returned HTTP 403 or are supply-side data[cite: 3].

**Resolution so far:** Documented each source with its evidence, bypassed no restrictions[cite: 3], evaluated alternatives, and asked the desk which route it accepts[cite: 3]. Upgraded pipeline with modular adapters and explicit classification logic to ingest data immediately upon approval.

**Incomplete or untested components:**
- Free-text normalization is only tested on exact aliases (for example, edge cases like "Hadapsar, Pune" or "2-BHK" are not tested).
- No saved processing log yet.
- Policy reviews pending: OSM / Overpass usage policy, IGR website policy.
- Google Trends manual export (market-level indicator) not yet done.

**Next actions:** Act on the desk's reply; read and quote the remaining pending policies; perform Google Trends export as a market-level indicator; expand free-text normalization tests.

## 6. Attached Deliverables

`src/adapter.py`, `src/scorer.py`, `src/pipeline.py`, `reports/robots_checks.csv`, `docs/source_discovery.md`, `evidence/` (robots.txt copies, run logs, `pytest_day5.log`), `reports/day5.md`[cite: 3]