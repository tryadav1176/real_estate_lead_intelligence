# Scope & Architecture Memo
## Real Estate Lead Intelligence Pipeline

**Candidate:** Tejas Rajendra Yadav  
**Target Role:** Lead Intelligence & Data Engineer  
**Evaluation Start Date:** 12 October 2026

### 1. Project Objective

Develop a modular data pipeline to discover authorized public real-estate intent signals for the Hadapsar and Fursungi micro-markets in Pune.

The pipeline will extract permitted data, normalize and validate records, identify duplicates, calculate transparent lead scores, and store eligible records in a structured database.

### 2. Scope

- Discover suitable public data sources.
- Extract permitted, non-authenticated information.
- Normalize fields and validate data quality.
- Deduplicate records.
- Calculate lead scores from location, requirement, and recency.
- Store validated records in SQLite or PostgreSQL.
- Export up to 100 clean, deduplicated, ranked records.
- Generate daily operational metrics and progress reports.

### 3. Proposed Architecture

**Source discovery → Extraction → Raw storage → Validation and normalization → Deduplication → Lead scoring → Database storage → Ranked CSV export**

### 4. Technology Stack

- Python
- Pandas
- Playwright and/or BeautifulSoup
- SQLite initially, with PostgreSQL as an alternative
- Regex for field normalization
- Git for version control
- Pytest for automated testing

### 5. Standardized Output Schema

- `Lead_Score`: Integer from 0 to 100.
- `Prospect_Name`: Trimmed, title-cased name; default `Valued Prospect`.
- `Mobile_Number`: Validated 10-digit Indian mobile number beginning with 6–9.
- `Target_Zone`: `Hadapsar`, `Fursungi`, or `Adjacent_East_Pune`.
- `Requirement`: `1BHK`, `2BHK`, `3BHK`, or `Residential Plot`.
- `Source_Channel`: Public source domain or forum thread.

### 6. Lead Scoring

The proposed score consists of:

- Location: Maximum 40 points.
- Requirement: Maximum 35 points.
- Recency: Maximum 25 points.

The detailed scoring rules will be documented and confirmed with the technical evaluation team before final implementation.

### 7. Compliance and Data Quality

- Review applicable source terms and robots.txt rules.
- Apply randomized request delays of 1.5–3.0 seconds where scraping is permitted.
- Do not bypass authentication or access controls.
- Collect and use personal data only where appropriately authorized.
- Record invalid, missing, and duplicate records transparently.
- Never fabricate prospect information or pipeline metrics.

### 8. Delivery Plan

Day 1: Environment, source discovery, architecture, and initial ingestion prototype.

Day 2: Field normalization and validation.

Day 3: Deduplication and first pipeline benchmark.

Day 4: Lead scoring and database integration.

Day 5: Second pipeline benchmark and quality improvements.

Day 6: Testing, documentation, and reliability improvements.

Day 7: Final export, repository handover, and technical defense.

### 9. Current Limitations

No company dataset or approved target source has been supplied at the time of writing. Initial development and testing will use clearly labelled synthetic data until a suitable source is verified.

### 10. Expected Deliverables

- Modular Python scripts.
- Documented database schema.
- Automated tests.
- Clean and ranked CSV export.
- Daily Progress Reports.
- README with setup and execution instructions.