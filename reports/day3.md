# Day 3 Daily Progress Report — Data Hygiene and Source Discovery

**Project:** Amar Realty — Lead Intelligence & Data Engineer Evaluation
**Candidate:** Tejas Rajendra Yadav
**Evaluation date:** 13 October 2026
**Target geography:** Hadapsar, Fursungi, and adjacent East Pune
**Milestone:** Hygiene, Regex Cleansing and Deduplication Logic

## 1. Objective

Improve the data-cleaning and persistence workflow, document potential data sources, strengthen regression-test coverage, and preserve a clear distinction between synthetic test records and genuine prospects collected through authorized methods.

## 2. Engineering Work Prepared

The following code and documentation changes have been prepared during this editing session. They must be saved and checked against the actual repository before being reported as completed and validated.

- **`src/cleaner.py`** — stricter Indian mobile-number format validation, locality normalization, property-requirement normalization, and duplicate-removal metrics.
- **`src/database.py`** — database schema migration for optional source-evidence fields, defensive mobile-format checks, and insertion/skipping metrics.
- **`src/pipeline.py`** — integration of validation, deduplication, scoring, CSV export, and database metrics.
- **`src/scorer.py`** — bounded component scoring and provisional recency rules using a source timestamp.
- **`src/scraper.py`** — conservative extraction helper that requires an authorization configuration and does not retry blocked requests.
- **`src/source_audit.py`** — source-review logging, consistent CSV fields, and explicit treatment of inconclusive or blocked access.
- **`tests/test_cleaner.py`** — expanded normalization, validation, and deduplication test cases.
- **`tests/test_database.py`** — new database test module using temporary SQLite databases.
- **`tests/test_scorer.py`** — expanded scoring and timestamp test cases.
- **`tests/test_source_audit.py`** — expanded source-audit test cases using mocked responses.
- **`docs/source_discovery.md`** — candidate source inventory and authorization assessment.
- **`README.md`** — updated project overview, schema, setup, compliance, and status documentation.

## 3. Source Discovery

Candidate sources identified for assessment include:

1. **MahaRERA** — project registration and regulatory information; suitable for market context, not direct buyer intent.
2. **OpenStreetMap / Overpass** — geographic enrichment; not a source of verified buyer leads.
3. **Housing.com** — potential property-market information, subject to the applicable terms and authorization.
4. **OLX India** — automated extraction is not approved without the necessary express authorization.
5. **Public community discussions** — potential purchase-intent signals only if the specific platform's rules and intended use permit collection.
6. **Government open-data resources** — contextual analysis subject to the relevant dataset licence.

**Authorization status:** No source is confirmed as authorized for live prospect extraction based solely on this candidate assessment.

The source-discovery document records the intended geographic relevance, information type, access considerations, and outstanding checks for each candidate.

## 4. Data Quality and Compliance

The planned pipeline distinguishes:

- Raw input records.
- Invalid records excluded by validation.
- Duplicate valid records removed from the input batch.
- Clean, unique records exported.
- Records newly inserted into the database.
- Records skipped because their mobile numbers already exist.
- Synthetic test records versus genuine source-backed prospects.

A mobile number that matches the required format is not necessarily verified, owned by the named person, or eligible for commercial contact. Missing source references and unsupported property intent must not be invented.

Public visibility and robots.txt permission alone do not establish authorization for personal-data collection or marketing use.

## 5. Test and Pipeline Results

**Status: Pending final execution.**

The tests and pipeline have not yet been rerun following the current set of edits.

| Metric | Result |
|---|---|
| Test suite | Pending |
| Pipeline execution | Pending |
| Raw input count | Pending |
| Invalid records excluded | Pending |
| Duplicate records removed | Pending |
| Clean unique output records | Pending |
| New database insertions | Pending |
| Existing database records skipped | Pending |
| Genuine authorized prospects collected | Not established |

No production collection count is claimed in this report.

## 6. Blockers and Risks

- Authorization for automated collection from candidate property platforms remains unresolved.
- The proposed scoring weights and recency thresholds remain provisional pending confirmation.
- Genuine purchase-intent evidence and eligible contact information must be established through an authorized source.
- The new code changes and regression tests require a final integrated test run.
- Any request blocked by access controls must be documented, not bypassed.

## 7. Next Actions

1. Finish reviewing and saving all source and test files.
2. Update any remaining documentation and report references.
3. Run the complete test suite once.
4. Run the pipeline and record its actual output.
5. Inspect generated CSV/database metrics for consistency.
6. Update this report with verified results and any unresolved failures.
7. Commit the completed changes and record the actual Git commit hash.

## 8. Evidence and Reporting Integrity

This report records the work prepared and the outstanding validation steps. It does not claim that the 7:00 PM IST reporting deadline was met, that a technical query was sent, or that real prospect data was collected unless independent evidence establishes those facts.

**Final status:** Day 3 implementation and validation are in progress; final results pending.
