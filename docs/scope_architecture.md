# Scope & Architecture Memo
## Real Estate Lead Intelligence Pipeline

**Candidate:** Tejas Rajendra Yadav  
**Target Role:** Lead Intelligence & Data Engineer  
**Evaluation Status:** Finalized (Day 7)

### 1. Project Objective

Develop a modular, DPDP-compliant data pipeline to ingest, validate, score, and persist real estate prospect data for the Hadapsar, Fursungi, and adjacent East Pune micro-markets. 

The pipeline strictly enforces ethical data collection, utilizing a "deny-by-default" extraction layer to prevent unauthorized scraping of Personal Identifiable Information (PII) from commercial portals.

### 2. Finalized Architecture Workflow

**Source Adapters → Validation & Normalization → Intent Classification → Deduplication → Lead Scoring → SQLite Persistence → Automated CSV Export**

### 3. Technology Stack

- **Core:** Python 3.12, Pandas
- **Extraction/Adapters:** `urllib`, `requests` (with compliance jitter), Custom `BaseSourceAdapter`
- **Database:** SQLite3 (Schema extensible to PostgreSQL)
- **Quality Assurance:** Pytest (132/132 coverage)
- **Version Control:** Git / GitHub

### 4. Modular Adapter Design

To abstract data ingestion and ensure strict compliance, the pipeline utilizes an adapter pattern (`src/adapter.py`). 
- **`BaseSourceAdapter`:** The foundational interface for all data ingestion.
- **`SimulatedOptInAdapter`:** The active implementation used to ingest Route (a) DPDP-compliant structured test fixtures, proving the pipeline mechanics without exposing live PII.

### 5. Validation and Deduplication (`src/cleaner.py`)

- **Mobile Validation:** Strict regular expressions enforce 10-digit Indian mobile formats (6–9 prefix).
- **Normalization:** Standardizes zone aliases (`Hadapsar`, `Fursungi`, `Adjacent_East_Pune`) and property requirements (`1BHK`, `2BHK`, `3BHK`, `Residential Plot`).
- **Deduplication:** Drops duplicates within the ingestion batch and uses database `UNIQUE` constraints (`src/database.py`) to prevent historical duplication.

### 6. Intent Classification & Scoring (`src/scorer.py`)

The pipeline algorithmically routes text inputs into a **6-tier intent taxonomy** and applies a **100-point calibrated score**:

*   **Intent Classification (Max 40 points):** `direct_purchase` (40), `emerging_purchase` (25), `rental` (10), `seller_listing` (0), `geographic_context` (0), `unknown` (0).
*   **Location Alignment (Max 25 points):** `Hadapsar`/`Fursungi` (25), `Adjacent_East_Pune` (15).
*   **Requirement Weight (Max 20 points):** Weighted by developer inventory priority.
*   **Recency Decay (Max 15 points):** 0-7 days (15), 8-30 days (10), 31-90 days (5).

Scores falling outside the finite 0-100 bounds raise explicit `ValueError` exceptions.

### 7. Database Schema (`leads` table)

- `ID` (Primary Key, Auto-increment)
- `Lead_Score` (Integer, 0-100)
- `Prospect_Name` (Text)
- `Mobile_Number` (Text, Unique constraint)
- `Target_Zone` (Text)
- `Requirement` (Text)
- `Intent_Type` (Text)
- `Source_Channel` (Text)
- `Source_Reference` (Text)
- `Source_Timestamp` (DateTime)
- `Processed_Timestamp` (DateTime)