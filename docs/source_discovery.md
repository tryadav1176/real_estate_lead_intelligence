# Source Discovery and Compliance Assessment (Days 3-4)

**Project:** Amar Realty - Lead Intelligence & Data Engineer Evaluation
**Target geography:** Hadapsar, Fursungi, and adjacent East Pune
**Assessment dates:** 13 October 2026 and 15 October 2026
**Status:** robots.txt testing complete for 8 hosts. No source is authorized for automated lead collection. Terms and licence review, and the manual intent sample, are pending.

## 1. Objective

Find specific public sources of property-demand signals and geographic context for the target area, test their access rules, and decide what each can lawfully support. The aim is accurate, auditable records, not record count.

## 2. What counts as genuine demand

A building, a listing or a place name is not a buyer. Only a person stating a property requirement is an intent signal, and even then it is not a qualified prospect without a permitted, valid contact.

| Class | Evidence required | Pipeline treatment |
|---|---|---|
| direct_purchase | Person says they want to buy now or soon | Strongest buyer-side signal |
| emerging_purchase | Person is considering or researching a purchase, no firm request | Keep separate from direct |
| rental | Person wants to rent or lease | Buyer-side but not a purchase lead; report separately |
| seller_listing | Person is advertising a property | Supply side, not intent |
| geographic_context | Project, locality, amenity or infrastructure information | Enrichment only, never a lead |
| unknown | Advice, opinion or unclear need | Not a lead |

Full rules and a decision checklist: `docs/intent_classification_guide.md`.

## 3. Source register (tested)

All robots.txt requests were made with an identified User-Agent, one request per host per run, using `robots_check.py`. Results are logged in `reports/robots_checks.csv`, with evidence in `evidence/`. Terms and licence columns say "not yet reviewed" until a clause has actually been read and quoted.

| # | Source | URL tested | Type | Intent value | robots.txt result | Terms / licence reviewed | Decision |
|---|---|---|---|---|---|---|---|
| 1 | 99acres | https://www.99acres.com/Pune-Real-Estate.htm | Commercial listing portal | Supply side, not intent | HTTP 403 (13 Oct). Manual browser view of robots.txt: listing, project and dealer paths disallowed | Not yet reviewed | Excluded |
| 2 | MahaRERA | https://www.maharera.maharashtra.gov.in/projects-search-result | Regulator project registry | Supply side, not intent | HTTP 403 (13 and 15 Oct); browser also showed Forbidden | Not yet reviewed | Excluded |
| 3 | IGR Maharashtra e-search | https://esearchigr.maharashtra.gov.in/ | Registered document records | Completed transactions, not intent; may contain personal data | HTTP 404, no robots.txt (15 Oct) | Not yet reviewed | Not authorized for automated collection; manual reference only |
| 4 | PMC Open Data | https://opendata.pmc.gov.in/ | Civic datasets | Geographic context | HTTP 404, no robots.txt (15 Oct) | Licence not yet reviewed | Candidate for geographic context only |
| 5 | PMC Development Plan PDF | https://adc-ecos.enlightcloud.com/.../DP-Report-2021-vol-1.pdf | Planning report | Geographic context | HTTP 403 (15 Oct) | Not yet reviewed | No automated fetch; manual download only |
| 6 | MagicBricks rates page | https://www.magicbricks.com/Property-Rates-Trends/Multistorey-Apartment-rates-Fursungi-in-Pune | Commercial price-trend page | Market data, not intent | HTTP 403 (15 Oct) | Not yet reviewed | Excluded |
| 7 | Reddit (r/pune, r/PuneClassifieds) | https://www.reddit.com/r/pune/ and two thread URLs | Public forum | Potential genuine intent signals | HTTP 200: `User-agent: *` / `Disallow: /` (15 Oct) | Public Content Policy not yet reviewed | Excluded from automated collection; manual sample pending desk confirmation |
| 8 | OpenStreetMap Overpass API | https://overpass-api.de/api/status | Open geographic API | Geographic context | HTTP 200: `Disallow: /api/` (15 Oct) | Usage policy not yet reviewed | Not cleared for automated requests; no queries sent |

## 4. Sources identified but not yet tested

| Source | URL | Note |
|---|---|---|
| Housing.com | https://housing.com/terms-of-use | Listing portal (supply side). robots.txt not tested; terms not yet quoted. |
| OLX India | https://help.olx.in/hc/en-us/articles/10957378342173-Terms-of-Use | Classifieds. robots.txt not tested; terms clause not yet quoted in this register. |
| data.gov.in | https://www.data.gov.in/ | Open datasets. robots.txt not tested; no dataset selected. |

## 5. Findings

- **No source is authorized for automated lead collection.** Four hosts blocked the bot with HTTP 403 (99acres, MahaRERA, the PMC plan PDF host, MagicBricks). Two published no robots.txt (IGR, PMC Open Data), which is not permission. Two published rules that disallow bots (Reddit: all paths; Overpass: `/api/`).
- No block was bypassed: no User-Agent spoofing, proxies, mirror sites, or browser automation.
- **Intent signals exist on Reddit,** but robots.txt forbids bots, so the only possible route is a human reviewer reading posts in a normal browser, or the official API (separate terms; not applied for).
- Posts typically ask people to message the author, so mobile numbers are rarely present. No contact data is to be collected, so intent signals cannot become qualified prospects.
- **Geographic context** is available through manual download of open datasets (PMC Open Data, PMC Development Plan PDF), subject to licence review. It supports locality normalization and must be kept separate from prospect records.

## 6. Proof-of-concept status

| Component | Status |
|---|---|
| Source testing and access decisions (8 hosts, 11 robots.txt requests) | Complete |
| Manual intent sample (15-20 posts into `data/intent_log/intent_signal_log.csv`) | **Pending:** awaiting technical desk confirmation that a manual, no-personal-data sample is acceptable |
| Terms and licence review (Reddit Public Content Policy, PMC Open Data, OSM / Overpass policy, IGR) | **Pending** |
| Pipeline demonstration on labelled synthetic data | Done separately (Day 3); not genuine prospects |
| Geographic enrichment from a manually downloaded open dataset | Pending licence review |

If the desk does not confirm the manual sample, the limitation will be documented and the pipeline demonstrated on labelled synthetic data only.

## 7. Metrics (actual)

| Metric | Value |
|---|---|
| Sources named | 11 |
| Hosts robots.txt-tested | 8 |
| robots.txt requests made | 11 |
| Blocked with HTTP 403 | 4 hosts |
| No robots.txt (404) | 2 hosts |
| robots.txt disallows bots | 2 hosts (Reddit, Overpass `/api/`) |
| Sources authorized for automated collection | 0 |
| Raw records received from any source | 0 |
| Intent signals manually reviewed | 0 (pending) |
| Genuine qualified prospects | 0 |

Synthetic fixture counts are reported separately and are not substituted for any of the above.

## 8. Next actions

1. Send the technical desk the manual-sample question, with the Reddit robots.txt evidence attached.
2. Read and quote one clause from each: Reddit Public Content Policy, PMC Open Data licence, OSM / Overpass usage policy, IGR website policy.
3. If the desk confirms, complete the manual intent sample and run `python -m src.intent_summary`.
4. Test robots.txt for data.gov.in, OLX and Housing.com only if they will be used.
5. Update the register after each step. A source is marked authorized only after its terms are read and the permitted use is confirmed.

## 9. Evidence references

- `reports/robots_checks.csv` (13 rows)
- `evidence/` robots.txt copies and run logs
- Commits: `843cc35`, `0b7a45c`