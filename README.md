# Real Estate Lead Intelligence Pipeline

A Python-based data engineering project for discovering authorized real-estate information sources, normalizing and validating data, deduplicating records, calculating explainable scores, and storing eligible property-intent records for the Hadapsar, Fursungi, and adjacent East Pune micro-markets.

**Candidate:** Tejas Rajendra Yadav  
**Target Role:** Lead Intelligence & Data Engineer – Real Estate  
**Evaluation Start:** 12 October 2026
**Project Status:** Development and source-authorization assessment

## 1. Project Objectives

- Identify and assess appropriate data sources for the target geography.
- Collect information only through authorized access methods.
- Normalize locality, property requirement, and mobile-number fields.
- Exclude records that fail required validation.
- Detect duplicates and report accurate record counts.
- Maintain source references and evidence supporting property intent.
- Calculate explainable lead scores using location, requirement, and recency.
- Persist eligible records in SQLite, with PostgreSQL as a potential extension.
- Export clean, deduplicated, ranked records when sufficient authorized data is available.
- Maintain tests, source-review evidence, daily progress reports, and Git history.

The target of up to 100 clean prospects is conditional on suitable, authorized data being available. It is not a guaranteed record count.

## 2. Technology Stack

- Python 3.12
- Pandas
- Regular expressions
- SQLite
- Pytest
- Git and GitHub
- BeautifulSoup and Playwright for future extraction only when explicitly authorized
- PostgreSQL as a potential database extension

## 3. Project Structure

```text
real_estate_lead_intelligence/
├── data/
│   ├── raw/
│   │   └── sample_leads.csv       # Synthetic fixtures only
│   └── processed/                 # Generated outputs
├── src/
│   ├── scraper.py                 # Reserved for authorized extraction
│   ├── source_audit.py            # Source/robots review utility
│   ├── cleaner.py                 # Normalization and validation
│   ├── scorer.py                  # Provisional explainable scoring
│   ├── database.py                # SQLite persistence and metrics
│   └── pipeline.py                # Processing and storage workflow
├── tests/
│   ├── test_cleaner.py
│   ├── test_scorer.py
│   ├── test_source_audit.py
│   └── test_database.py
├── docs/
│   ├── scope_architecture.md
│   ├── source_audit.md
│   └── source_discovery.md
├── evidence/                      # Source-review evidence
├── reports/
│   ├── day1.md
│   ├── day2.md
│   ├── day3.md
│   └── robots_checks.csv
├── robots_check.py
├── requirements.txt
└── README.md
```

This is the intended structure; the actual repository should be checked before treating every listed file as present.

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

The pipeline may include additional internal fields, such as `is_valid` and `Mobile_Format_Valid`, for validation and processing.

**Important:** A valid mobile-number format does not establish ownership, identity, consent, or permission to contact. A record must not be described as a verified prospect unless the applicable verification criteria have actually been met.

## 5. Validation and Deduplication

The cleaning stage is designed to:

1. Normalize names and standardize missing-name values.
2. Validate mobile numbers using strict regular-expression rules.
3. Normalize supported locality aliases to canonical zone values.
4. Normalize property-requirement aliases to the allowed enum values.
5. Require a usable source channel.
6. Mark invalid records rather than silently treating them as qualified prospects.
7. Remove duplicate valid records using normalized mobile numbers.
8. Retain accurate counts of input, invalid, duplicate, and output records.

The persistence layer separately tracks new insertions and records skipped because the mobile number already exists in the database.

## 6. Lead Scoring

The proposed scoring model has three components:

- **Location:** maximum 40 points
- **Requirement:** maximum 35 points
- **Recency:** maximum 25 points

The score is provisional until the component rules, evidence requirements, and recency calculation have been reviewed and validated.

A score is a ranking aid, not proof of buying intent, identity, or contact eligibility. Missing or unsupported evidence must not be replaced with invented values.

## 7. Setup Instructions

### Step 1 — Clone the repository

```powershell
git clone https://github.com/tryadav1176/real_estate_lead_intelligence.git
cd real_estate_lead_intelligence
```

### Step 2 — Create a virtual environment

```powershell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3 — Install dependencies

```powershell
python -m pip install -r requirements.txt
```

Install Playwright's Chromium browser only if required by an authorized and permitted future workflow:

```powershell
python -m playwright install chromium
```

### Step 4 — Run the pipeline

From the repository root:

```powershell
python -m src.pipeline
```

The pipeline reads `data/raw/sample_leads.csv`, processes the records, writes a cleaned CSV to `data/processed/cleaned_leads.csv`, and stores eligible records in the SQLite database.

The sample input is intended for development and testing. Its records must not be reported as genuine prospects.

## 8. Testing

The project uses Pytest.

Run the complete test suite from the repository root:

```powershell
python -m pytest -q
```

The suite is intended to cover normalization, invalid mobile formats, enum validation, duplicate removal, database persistence, and source-audit behavior.

Report the test result only after the test command has actually completed.

## 9. Data Collection and Compliance

- Assess source terms, applicable policies, and `robots.txt` before considering automated collection.
- Use only access methods authorized for the intended purpose.
- Apply request delays, including 1.5–3.0 second jitter, only where automated access is permitted and the service's policies allow it.
- Do not bypass authentication, CAPTCHA, HTTP 403 responses, or other access controls.
- Do not assume that publicly visible information can be collected, retained, or used for commercial outreach.
- Minimize personal information and retain source references and evidence needed for auditability.
- Separate geographic enrichment from person-level prospect data.
- Record actual access results, validation counts, deduplication counts, and blockers.
- Do not invent prospect identities, phone numbers, source references, intent evidence, or verification status.

If source permission is unavailable or unclear, document the issue and use an appropriate alternative proof of concept rather than attempting to circumvent restrictions.

## 10. Source Discovery

The initial source assessment is maintained in `docs/source_discovery.md`.

Candidate categories include:

- **MahaRERA:** official project and regulatory information for market context.
- **OpenStreetMap / Overpass:** geographic enrichment, not buyer-intent data.
- **Housing.com:** potential property-market information, subject to applicable terms and authorization.
- **OLX India:** automated collection is not approved without the necessary express authorization.
- **Public community discussions:** potential intent signals only where platform rules and the proposed use permit collection.
- **Government open data:** contextual analysis under the relevant dataset licence.

A candidate source is not considered approved merely because it has been identified. Authorization and successful access must be recorded separately.

## 11. Current Project Status

The project includes a synthetic-data pipeline and source-audit work. The source-discovery document records candidate sources and outstanding authorization questions.

The current implementation and test status must be confirmed from the repository before making final claims.

No genuine prospect count should be claimed unless supported by actual authorized collection, source evidence, validation, and deduplication results.

The scraper remains inactive until an appropriate source and permitted access method have been established. The scoring rules remain provisional.

## 12. Evaluation Deliverables

- Modular Python pipeline
- Normalization and validation module
- Regex-based mobile validation and tests
- Deduplication and accurate record metrics
- Database persistence and insertion counts
- Source discovery and compliance assessment
- Ranked CSV output when supported by suitable data
- Automated tests
- Daily Progress Reports
- Source-review evidence
- Final README and repository handover

## 13. Author

**Tejas Rajendra Yadav**

GitHub: https://github.com/tryadav1176
Repository: https://github.com/tryadav1176/real_estate_lead_intelligence
