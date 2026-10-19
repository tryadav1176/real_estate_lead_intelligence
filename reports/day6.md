# CANDIDATE DAILY PROGRESS REPORT (DPR)

- **Candidate Name:** Tejas Rajendra Yadav
- **Target Role:** Lead Intelligence & Data Engineer
- **Evaluation Day:** Day 6
- **Date:** 19/10/2026
- **Git Commit Hash:** `2cfe3a9` 
- **Repository:** https://github.com/tryadav1176/real_estate_lead_intelligence

## Status summary (completed vs pending)

| Desk task | Status | Detail |
|---|---|---|
| 1. Identify usable lead sources | **Done (Simulated)** | Approved Route (a) via structured test fixtures (simulated opt-in form) authorized by the Technical Desk. |
| 2. Demonstrate actual intent discovery | **Done (Simulated)** | Ingested and classified intent from the simulated fixture using the newly implemented 6-tier `classify_intent` logic. |
| 3. Demonstrate working pipeline | **Done** | `SimulatedOptInAdapter` successfully wired to `pipeline.py`. End-to-end execution completed. 132/132 automated tests passed. |
| 4. Report actual results | **Done** | Metrics updated for the simulated batch (4 raw ingested, 1 dropped, 1 deduplicated, 2 clean stored). |
| 5. Submit Day 6 evidence | **Done** | Code updates, test fixtures, test logs, and exported CSV committed. |

## 1. Daily Engineering Tasks Completed

- Integrated `SimulatedOptInAdapter` into `src/pipeline.py` to ingest DPDP-compliant structured test fixtures, as explicitly authorized by the Technical Desk for Day 6.
- Upgraded the scoring engine in `src/scorer.py` to calculate a calibrated 100-point composite score utilizing Intent classification weights (40pts max) and Recency decay (15pts max) alongside location and requirement parameters.
- Implemented export automation in `src/pipeline.py` to extract verified, deduplicated records from the SQLite database via `get_leads()` and automatically export them to `final_exported_leads.csv`.
- Refactored unit tests in `tests/test_scorer.py` to support the new scoring thresholds and rigorous `ValueError` parameter validations. 
- Executed the full automated test suite successfully: 132 passed, 0 failed.

## 2. Technical Stack Utilized

Python, pandas, SQLite3, pytest, Git/GitHub. (No commercial scraping APIs utilized).

## 3. Compliance & Scraping Throttling Audit

- **Targets tested:** Local CSV fixture (`simulated_opt_in_leads.csv`).
- **Robots.txt Adherence:** N/A for local fixtures. B2C automated extraction remains strictly halted to respect commercial ToS and evaluation compliance mandates.
- **Requests made:** 0 network requests made during this pipeline run. 
- **Responses:** N/A.
- **Rate limiting:** The 1.5s-3.0s jitter is fully implemented and tested in the guarded scraper (`src/scraper.py`) for future network requests.
- **Access restrictions:** None bypassed. No User-Agent spoofing, proxies, mirror sites or browser automation.

## 4. Pipeline Operational Metrics

| Metric | Value |
|---|---|
| Authorized sources successfully used | 1 (Simulated Opt-In Form) |
| Genuine source records collected | 0 (Using authorized test fixtures) |
| Unique records processed | 3 |
| Genuine property-intent signals identified | 0 (Using simulated intent) |
| Valid Indian mobile numbers obtained through permitted means | 2 (Simulated) |
| Qualified prospects meeting the agreed criteria | 2 (Simulated) |
| Raw Ingestion Count / Records Dropped / Duplicates Removed | 4 / 1 / 1 |
| Cumulative Clean Prospects Stored | 2 / 100 |

*Note: Processed data consists of approved simulated test fixtures to demonstrate pipeline capability without live PII exposure, as authorized by the Technical Desk for Day 6.*

## 5. Technical Challenges & Proof of Concept (PoC) Solutions

**Blocker:** Reconciling strict 100-point scoring caps across diverse intent and recency parameters without breaking existing pipeline validation tests.

**Resolution so far:** Abstracted intent classification into `classify_intent()`, injected the result into the record dictionary during the mapping phase, and added stringent `ValueError` parameter bounding in `calculate_lead_score()`. Refactored `tests/test_scorer.py` to ensure unit test coverage aligned perfectly with the new calibration, achieving a 100% pass rate.

**Incomplete or untested components:**
- Google Trends manual export (market-level indicator) remains pending as an alternative geographic context layer.
- Free-text normalization is only tested on exact aliases (edge cases like "Hadapsar, Pune" or "2-BHK" are not tested).
- Policy reviews pending: OSM / Overpass usage policy, IGR website policy.

**Next actions:** Prepare the codebase and local environment for the Day 7 Technical Defense and Architecture Walkthrough.

## 6. Attached Deliverables

`src/adapter.py`, `src/scorer.py`, `tests/test_scorer.py`, `src/pipeline.py`, `data/raw/simulated_opt_in_leads.csv`, `data/processed/final_exported_leads.csv`, `reports/day6.md`