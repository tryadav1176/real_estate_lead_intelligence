# Day 4 Daily Progress Report — Source Discovery and Intent Classification

**Project:** Amar Realty — Lead Intelligence & Data Engineer Evaluation  
**Candidate:** Tejas Rajendra Yadav  
**Date:** 15 October 2026  
**Evaluation Day:** Day 4 of 7  
**Repository:** https://github.com/tryadav1176/real_estate_lead_intelligence  
**Day 4 commit:** `6ed2eb3` — `Day 4: rewrite source discovery register and add intent log kit`  
**Target geography:** Hadapsar, Fursungi, and adjacent East Pune  
**Status:** Source-access assessment and intent-classification toolkit committed. No source is currently authorized for automated lead collection. Manual intent review and terms/licence checks remain pending.

## 1. Objective

Move from broad source categories to a specific source register, assess observed `robots.txt` responses, distinguish genuine property-demand signals from market/geographic context, and prepare a traceable intent-classification workflow without bypassing access restrictions or representing synthetic data as genuine prospects.

## 2. Work completed

- Updated `docs/source_discovery.md` with the Days 3–4 source and compliance assessment.
- Added `docs/intent_classification_guide.md` to define intent categories and a consistent classification approach.
- Added `src/intent_summary.py` to summarize the intent-signal log.
- Added `data/intent_log/intent_signal_log.csv` as the structured log for any future permitted manual intent review.
- Recorded source-review findings and outstanding checks, including the distinction between `robots.txt` results and actual authorization.
- Committed and pushed the four-file Day 4 change set to `main`.

**Git evidence:** Commit `6ed2eb3` was reported by the terminal as pushed successfully to `origin/main`. The source-discovery register also references earlier audit commits `843cc35` and `0b7a45c`.

## 3. Source review and access findings

The source-discovery register records eight hosts tested through the `robots_check.py` workflow, with 11 `robots.txt` requests reported in the register.

| Result recorded | Hosts/sources | Interpretation |
|---|---|---|
| HTTP 403 | 99acres, MahaRERA, PMC Development Plan PDF host, Magicbricks | Treated as blocked under the current audit workflow; no bypass attempted |
| HTTP 404 / no `robots.txt` found | IGR Maharashtra e-search, PMC Open Data | No `robots.txt` rules were obtained; this is not permission to automate collection |
| HTTP 200 with bot-disallowing rules | Reddit, Overpass `/api/` path | Automated access is not cleared under the current assessment |

No source is currently authorized for automated lead collection. The current assessment records no use of User-Agent spoofing, proxies, mirror sites, or browser automation to bypass restrictions.

The register also identifies Housing.com, OLX India, and data.gov.in as sources not yet tested in the current assessment. These remain candidates only; no access permission or dataset suitability is claimed.

## 4. Intent classification and data handling

The intent guide distinguishes the following classes:

- `direct_purchase` — an explicit statement of a current or near-term purchase requirement.
- `emerging_purchase` — purchase consideration or research without a firm request.
- `rental` — a rental/lease requirement, reported separately from purchase demand.
- `seller_listing` — supply-side property advertising, not buyer intent.
- `geographic_context` — project, locality, amenity, infrastructure, or market information used for enrichment only.
- `unknown` — advice, opinion, or unclear need.

A mention of a property or locality is not sufficient to classify a person as a buyer. An intent signal is not a qualified prospect unless there is a permitted and valid contact basis. The planned manual sample, if approved, will avoid recording usernames, phone numbers, or other personal data and will not involve contacting authors.

## 5. Proof-of-concept status

| Component | Status | Evidence/notes |
|---|---|---|
| Source register | Completed | `docs/source_discovery.md` |
| Intent-classification guide | Completed | `docs/intent_classification_guide.md` |
| Intent summary utility | Added and committed | `src/intent_summary.py`; execution results not provided in this report |
| Structured intent log | Added and committed | `data/intent_log/intent_signal_log.csv` |
| `robots.txt` assessment | Completed as recorded | `reports/robots_checks.csv` and files under `evidence/` |
| Terms/licence review | Pending | Relevant clauses have not yet been reviewed and quoted in the register |
| Manual review of 15–20 posts | Pending | Awaiting technical desk confirmation; no posts manually reviewed yet |
| Geographic enrichment from an open dataset | Pending | Dataset selection and licence review not completed |
| Genuine prospects from an authorized source | Not achieved | No source authorized and no source records received |

The existing Day 3 pipeline demonstration used clearly labelled synthetic sample data. Those results demonstrate local processing only and are not genuine source-derived prospects.

## 6. Actual metrics recorded

| Metric | Value | Qualification |
|---|---:|---|
| Sources named in the register | 11 | Includes tested and not-yet-tested candidates |
| Hosts with `robots.txt` checks | 8 | As recorded in the source-discovery register |
| `robots.txt` requests | 11 | As recorded in the source-discovery register |
| Hosts returning HTTP 403 | 4 | Blocked under the current audit workflow |
| Hosts returning HTTP 404 / no `robots.txt` | 2 | Not evidence of permission |
| Hosts/path rules disallowing bots | 2 | Reddit and Overpass `/api/` path |
| Sources authorized for automated collection | 0 | Terms and permitted use not yet confirmed |
| Raw records received from an authorized source | 0 | No authorized source ingestion performed |
| Manually reviewed intent signals | 0 | Manual sample pending desk confirmation |
| Genuine qualified prospects | 0 | No qualifying source-backed records collected |

These counts are source-review metrics. They must not be combined with synthetic fixture counts from the Day 3 pipeline.

## 7. Blockers and risks

1. **Source authorization:** No source is confirmed as authorized for automated lead collection.
2. **Terms and licence review:** Review and record the relevant clauses for Reddit, PMC Open Data, OpenStreetMap/Overpass, and IGR before deciding whether a particular use is permitted.
3. **Manual intent sample:** The proposed sample of 15–20 posts is pending technical desk confirmation. It has not been completed and must not be reported as completed.
4. **Geographic enrichment:** No specific open dataset has yet been selected, licence-checked, downloaded, and processed as part of this Day 4 work.
5. **Prospect qualification:** No genuine qualified prospects have been collected. Market context and intent signals must remain separate from qualified contacts.

## 8. Next actions

1. Send the technical query to `tech@amarrealty.co.in` asking whether a small manual, no-personal-data intent-classification sample is acceptable. Attach the relevant Reddit `robots.txt` evidence and `reports/robots_checks.csv`.
2. Until the desk responds, keep the manual sample marked **Pending — awaiting technical desk confirmation**.
3. Review and quote the relevant terms/licence clauses for Reddit, PMC Open Data, OpenStreetMap/Overpass, and IGR; update the register only when the review is actually completed.
4. If manual review is approved, review 15–20 posts under the confirmed limits, log only permitted fields, and run `python -m src.intent_summary`. Record actual output and counts.
5. If manual review is not approved, document the limitation and continue to demonstrate pipeline processing with clearly labelled synthetic data.
6. Consider a geographic-context proof of concept only after selecting a specific dataset and confirming its licence and permitted access method.
7. Update the DPR with evidence from any completed follow-up work; do not claim source authorization, ingestion, or prospect collection without supporting results.

## 9. Evidence and repository references

- `docs/source_discovery.md`
- `docs/intent_classification_guide.md`
- `src/intent_summary.py`
- `data/intent_log/intent_signal_log.csv`
- `reports/robots_checks.csv`
- `evidence/` — `robots.txt` copies and run logs, as applicable
- Day 4 commit: `6ed2eb3`
- Earlier audit commits referenced in the source register: `843cc35`, `0b7a45c`

## 10. Day 4 conclusion

Day 4 produced a more specific source register, an intent-classification guide, a structured intent log, and a summary utility. The access assessment recorded eight hosts and 11 `robots.txt` requests, but it did not authorize automated collection. No source records were received from an authorized source, no intent signals were manually reviewed, and no genuine qualified prospects were collected.

The next milestone is to complete the documented terms/licence review and obtain the technical desk's decision on the proposed manual sample, or otherwise continue with a clearly labelled synthetic-data demonstration.
