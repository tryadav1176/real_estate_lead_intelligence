# Real Estate Lead Intelligence Pipeline

A Python-based data engineering project designed to collect, validate, normalize, deduplicate, score, and store authorized real-estate intent signals for the Hadapsar and Fursungi micro-markets in Pune, Maharashtra.

**Candidate:** Tejas Rajendra Yadav  
**Target Role:** Lead Intelligence & Data Engineer – Real Estate  
**Evaluation Start:** 12 October 2026

## Project Objectives

- Discover suitable, authorized public data sources.
- Extract permitted, non-authenticated information.
- Standardize and validate records using Python, Pandas, and regex.
- Detect duplicate records and preserve data-quality information.
- Calculate explainable lead scores.
- Store validated records in SQLite or PostgreSQL.
- Export up to 100 clean, deduplicated, ranked prospect records.
- Maintain daily engineering reports and Git history.

## Technology Stack

- Python 3.12
- Pandas
- Playwright
- BeautifulSoup
- SQLite / PostgreSQL
- SQLAlchemy
- Pytest
- Git and GitHub

## Project Structure

```text
real_estate_lead_intelligence/
├── data/
│   ├── raw/sample_leads.csv       # synthetic test records only
│   └── processed/                 # generated outputs; not committed
├── src/
│   ├── scraper.py                 # reserved for an authorized extraction PoC
│   ├── source_audit.py            # conservative robots/source review utility
│   ├── cleaner.py                 # normalization and validation
│   ├── scorer.py                  # provisional explainable score
│   ├── database.py                # SQLite persistence and insert metrics
│   └── pipeline.py                # CSV-to-cleaned-output workflow
├── tests/
│   ├── test_cleaner.py
│   ├── test_scorer.py
│   └── test_source_audit.py
├── docs/
│   ├── scope_architecture.md
│   └── source_audit.md
├── evidence/                      # retained source-review evidence
├── reports/
│   ├── day1.md
│   ├── day2.md
│   └── robots_checks.csv
├── robots_check.py
├── requirements.txt
└── README.md
```

## Standardized Output Schema

| Field | Description |
|---|---|
| `Lead_Score` | Integer between 0 and 100 |
| `Prospect_Name` | Trimmed, title-cased name; default `Valued Prospect` |
| `Mobile_Number` | Validated 10-digit Indian mobile number starting with 6–9 |
| `Target_Zone` | `Hadapsar`, `Fursungi`, or `Adjacent_East_Pune` |
| `Requirement` | `1BHK`, `2BHK`, `3BHK`, or `Residential Plot` |
| `Source_Channel` | Public source domain or forum thread |

## Lead Scoring

The proposed scoring model has three components:

- Location: maximum 40 points
- Requirement: maximum 35 points
- Recency: maximum 25 points

The detailed scoring rules will be documented and confirmed before final implementation.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/tryadav1176/real_estate_lead_intelligence.git
cd real_estate_lead_intelligence
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Data Collection and Compliance

- Use only appropriately authorized data sources.
- Review source terms and `robots.txt` before extraction.
- Apply randomized request delays of 1.5–3.0 seconds where scraping is permitted.
- Do not bypass authentication or access controls.
- Handle personal information lawfully and appropriately.
- Record actual ingestion, validation, and deduplication metrics.

## Current Project Status

**Prototype status: source-audit tooling and synthetic-data pipeline are implemented.**

The current evidence records HTTP 403 responses for automated robots.txt requests to 99acres and MahaRERA. No source is confirmed as authorized for live prospect extraction, and no real prospect records are claimed. The scraper module remains intentionally inactive until the source, permitted fields, and terms are verified. The lead-scoring sub-rules are provisional.

Implementation status will be updated as components are completed and tested.

## Evaluation Deliverables

- Modular Python scripts
- Data validation and deduplication
- Database integration
- Clean and ranked CSV output
- Automated tests
- Daily Progress Reports
- Final README and repository handover

## Author

**Tejas Rajendra Yadav**

GitHub: [tryadav1176](https://github.com/tryadav1176)