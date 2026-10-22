# Real Estate Lead Intelligence Pipeline

A Python-based data engineering project for discovering authorized real-estate information sources, normalizing and validating data, deduplicating records, calculating explainable scores based on intent and recency, and storing eligible property-intent records for the Hadapsar, Fursungi, and adjacent East Pune micro-markets.

**Candidate:** Tejas Rajendra Yadav  
**Target Role:** Lead Intelligence & Data Engineer – Real Estate  
**Evaluation Status:** Final Submission (Day 7)

## 📌 Project Overview

This repository contains a robust, DPDP-compliant ETL pipeline designed to ingest, clean, deduplicate, score, and persist real estate prospect data for Hadapsar, Fursungi, and adjacent East Pune.

Built with a strict adherence to ethical data collection, the architecture features a "deny-by-default" extraction layer that respects `robots.txt`, enforces rate-limiting, and strictly separates genuine pipeline mechanics from unauthorized PII scraping.

## 🏗️ Architecture & Compliance Highlights

**Modular Adapters (`src/adapter.py`):** Utilizes a `BaseSourceAdapter` pattern. Currently implements a `SimulatedOptInAdapter` to process authorized structured test fixtures (simulating a DPDP-compliant opt-in form) without exposing live PII.
**Strict Validation & Deduplication (`src/cleaner.py`):** Enforces 10-digit mobile validation (6-9 prefix), normalizes free-text zones/requirements, and drops invalid or duplicate inputs.
**Intent Classification & Scoring (`src/scorer.py`):** Calculates a 100-point composite `Lead_Score` utilizing a 6-tier intent classification taxonomy (direct purchase, emerging purchase, rental, seller listing, geographic context, unknown) and recency decay weighting.
**Ethical Extraction (`src/scraper.py`):** Hardcoded 1.5s–3.0s random delay jitter. Raises explicit exceptions on HTTP 401/403/429 rather than attempting unauthorized bypasses.


## 1. Project Objectives

- Construct a DPDP-compliant ETL pipeline with a "deny-by-default" extraction layer that respects `robots.txt`, ToS, and access restrictions.
- Collect information strictly through authorized access methods, avoiding unauthorized bulk scraping of live PII from commercial portals.
- Normalize locality, property requirement, and validate Indian mobile numbers via strict regular expressions.
- Classify prospect intent into a rigorous 6-tier taxonomy.
- Calculate explainable, weighted lead scores using Intent, Location, Requirement, and Recency factors.
- Persist clean, deduplicated records in an SQLite database.
- Export ranked, actionable records via automated routines.

## 2. Technology Stack

- **Core:** Python 3.12, Pandas
- **Persistence:** SQLite3 (Schema extensible for PostgreSQL)
- **Quality Assurance:** Pytest (132/132 automated test suite)
- **Version Control:** Git & GitHub
- **Extraction Protocol:** `urllib`, `requests` (with hardcoded 1.5s–3.0s jitter)

## 3. Project Structure

```text
real_estate_lead_intelligence/
├── data/
│   ├── raw/
│   │   └── simulated_opt_in_leads.csv   # Authorized Route (a) test fixtures
│   └── processed/
│       └── final_exported_leads.csv     # Automated pipeline output
├── src/
│   ├── scraper.py                 # Extraction with mandatory compliance jitter
│   ├── adapter.py                 # BaseSourceAdapter and SimulatedOptInAdapter
│   ├── cleaner.py                 # Regex validation and deduplication
│   ├── scorer.py                  # 6-tier intent classification and scoring
│   ├── database.py                # SQLite persistence and deduplication logic
│   └── pipeline.py                # End-to-end execution workflow
├── tests/                         # 132 Unit and regression tests
│   ├── test_cleaner.py
│   ├── test_scorer.py
│   ├── test_source_audit.py
│   └── test_database.py
├── docs/
│   ├── intent_classification_guide.md
│   └── source_discovery.md        # Final compliance audit and ToS reviews
├── evidence/                      # Source-review evidence (robots.txt logs)
├── reports/                       # Daily Progress Reports (Day 1 - Day 7)
├── requirements.txt
└── README.md
```

## 4. Standardized Record Schema

| Field | Description |
|---|---|
| `Lead_Score` | Integer score from 0 to 100 |
| `Prospect_Name` | Normalized name, with `Valued Prospect` as the missing-name default |
| `Mobile_Number` | Normalized 10-digit Indian mobile number beginning with 6–9 |
| `Target_Zone` | `Hadapsar`, `Fursungi`, or `Adjacent_East_Pune` |
| `Requirement` | `1BHK`, `2BHK`, `3BHK`, or `Residential Plot` |
| `Source_Channel` | Source domain or identifiable source channel |
| `Source_Reference` | URL or other reproducible reference to the supporting source |
| `Intent_Evidence` | Evidence supporting the stated property requirement |
| `Verification_Status` | Explicit status; defaults to `Not verified` |
| `Deduplication_Status` | Status describing duplicate handling |

## 5. Validation and Deduplication

The src/cleaner.py and src/database.py modules operate in tandem to ensure absolute data hygiene:

- Validates mobile numbers using strict regex bounds.
- Normalizes supported locality and property-requirement aliases.
- Explicitly marks invalid records (e.g., spam, malformed fields) and excludes them from downstream processing.
- Drops duplicate records within the ingestion batch.
- Employs database-level constraint handling to skip records that already exist in the system, preventing historical duplication.

## 6. Lead Scoring

The scoring model (src/scorer.py) applies a strict 100-point calibrated algorithm. It evaluates free-text intent signals and structural metadata to rank prospects:

- **Intent Classification:** Maximum 40 points (direct purchase = 40, emerging purchase = 25, rental = 10, others = 0).
- **Location Alignment:** Maximum 25 points (Hadapsar/Fursungi = 25, Adjacent_East_Pune = 15).
- **Requirement Weight:** Maximum 20 points (Weighted based on developer inventory priority).
- **Recency Decay:** Maximum 15 points (0-7 days = 15, 8-30 days = 10, 31-90 days = 5).
- Scores falling outside the finite 0-100 bounds raise explicit ValueError exceptions to prevent corrupted analytics.

## 7. Local Setup Instructions

1. **Clone the repository:**
```bash
git clone [https://github.com/tryadav1176/real_estate_lead_intelligence.git](https://github.com/tryadav1176/real_estate_lead_intelligence.git)
cd real_estate_lead_intelligence
```

2. **Create and activate a virtual environment:**
```
python -m venv .venv
```

### On Windows:
```
.venv\Scripts\activate
```
### On Mac/Linux:
```
source .venv/bin/activate
```

3. **Install dependencies:**

```

pip install -r requirements.txt

```

## 8. Execution Guide

1. **Run the Data Pipeline**
Execute the end-to-end pipeline. This will ingest the simulated test fixtures, clean the data, apply the scoring engine, persist records to the SQLite database, and automate the final CSV export.

```
python -m src.pipeline
```

2. **Run the Automated Test Suite**

The repository includes 132 unit tests covering regex validation, score calibration, exception handling, and database migrations.

```
python -m pytest -v
```

## 9. Database Schema (leads table)

The SQLite/PostgreSQL persistence layer (src/database.py) is structured to house clean, actionable prospects:

- ID (Primary Key, Auto-increment)
- Prospect_Name (Text)
- Mobile_Number (Text, Unique constraint for deduplication)
- Target_Zone (Text)
- Requirement (Text)
- Intent_Type (Text - 6-tier taxonomy)
- Lead_Score (Integer - 100-point scale)
- Source_Channel (Text)
- Source_Reference (Text)
- Source_Timestamp (DateTime)
- Processed_Timestamp (DateTime)

## 10. Documentation & Evidence

**Source Audit & Decisions:** See docs/source_discovery.md for a comprehensive log of robots.txt outcomes, ToS reviews, and ethical exclusion decisions for commercial portals.
**Intent Taxonomy:** See docs/intent_classification_guide.md for the classification rubric.
**Evaluation Logs:** See the reports/ folder for Daily Progress Reports (DPRs).

## Author

**Tejas Rajendra Yadav**

GitHub: https://github.com/tryadav1176

Repository: https://github.com/tryadav1176/real_estate_lead_intelligence
