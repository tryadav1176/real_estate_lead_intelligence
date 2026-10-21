# Public Source Authorization Audit

**Project:** Amar Realty Lead Intelligence  
**Target markets:** Hadapsar, Fursungi, and adjacent East Pune  
**Audit Status:** Finalized (Day 7)

## Purpose
Identify public sources that may lawfully and technically support real-estate market research and prospect-intent analysis without violating commercial Terms of Service, DPDP mandates, or `robots.txt` directives.

## Final Source Review Log

| Source | Intended Use | robots.txt / ToS Review | Automated Access Authorized? | Final Decision |
|---|---|---|---|---|
| 99acres | Commercial listings | HTTP 403. Manual review confirmed paths are disallowed. | No | Excluded. Strictly blocked by ToS and access controls. |
| Reddit (r/pune) | Public discussion | HTTP 200 (`Disallow: /`). Developer Terms restrict bulk commercial lead gen. | No | Excluded. All manual and automated scraping abandoned to ensure compliance. |
| MahaRERA | Project registry | HTTP 403 (Forbidden response). | No | Excluded from automated extraction. |
| PMC Open Data | Geographic context | HTTP 404 (No robots.txt). GODL Licence permits reuse. | Yes (Context Only) | Approved solely for geographic/locality enrichment. |
| Simulated Opt-In | Demonstration | Authorized Route (a) local test fixtures. | Yes | Approved by Tech Desk to demonstrate pipeline architecture securely. |

## Evidence Inventory
- `reports/robots_checks.csv`: Records automated `robots.txt` request outcomes.
- `evidence/`: Contains copies of manual browser notes for 99acres and MahaRERA.

## Compliance Findings & Guardrails
- **Zero Bypass Policy:** HTTP 403 responses and bot disallows were respected immediately. No User-Agent spoofing, CAPTCHA solving, or proxy networks were utilized to circumvent commercial security.
- **Strict Throttling:** For any future authorized extraction, a randomized request delay (jitter) of 1.5 to 3.0 seconds is hardcoded into the scraper module (`src/scraper.py`).
- **No PII Scraping:** Because major real estate and community platforms restrict automated commercial data harvesting, **0 unverified B2C leads were scraped**. 
- **Architectural Pivot:** The pipeline utilizes `SimulatedOptInAdapter` to process authorized test fixtures, proving the ETL capabilities without compromising data ethics.