# Day 3 — Source Discovery and Compliance Assessment

**Project:** Amar Realty — Lead Intelligence & Data Engineer Evaluation
**Target geography:** Hadapsar, Fursungi, and adjacent East Pune
**Assessment date:** 13 October 2026
**Status:** Initial desk research; source authorization and live collection are not yet confirmed.

## 1. Objective

Identify potential sources of property-market information and explicit buyer-intent signals within the target geography. Assess each source for geographic relevance, available information, permitted access methods, restrictions, and suitability for the lead-intelligence pipeline.

The objective is to produce accurate, auditable records—not to maximize record count by collecting personal information without appropriate authorization.

## 2. Candidate source assessment

### Source A — Maharashtra Real Estate Regulatory Authority (MahaRERA)

- **Official URL:** https://www.maharera.maharashtra.gov.in/
- **Relevant page:** https://maharera.maharashtra.gov.in/project-updates
- **Geographic relevance:** Registered real-estate projects across Maharashtra, including projects potentially relevant to Pune and the target micro-markets.
- **Information potentially available:** Project registrations, project status, construction progress, promoter information, and regulatory updates.
- **Access method:** Review publicly accessible official pages manually. Investigate whether an authorized export, dataset, or API is available before implementing automated collection.
- **Restrictions and checks:** Confirm applicable website terms, data-use conditions, and any restrictions on automated access or reuse. Do not assume that publicly visible project information grants permission to collect personal information.
- **Intent classification:** Geographic and market context; not direct buyer intent.
- **Suitability:** Suitable for authorized market and project enrichment. Not a standalone source of qualified buyer leads.
- **Current status:** Candidate identified; automated access and reuse authorization not yet confirmed.

### Source B — OpenStreetMap and Overpass API

- **Official project:** https://www.openstreetmap.org/
- **Overpass API documentation:** https://wiki.openstreetmap.org/wiki/Overpass_API
- **OSMF API usage policy:** https://operations.osmfoundation.org/policies/api/
- **Tile usage policy:** https://operations.osmfoundation.org/policies/tiles/
- **Geographic relevance:** Locality boundaries and nearby geographic features in Hadapsar, Fursungi, and adjacent East Pune, subject to the available mapped data.
- **Information potentially available:** Mapped roads, neighbourhoods, amenities, and other geographic features.
- **Access method:** Use a suitable read-only Overpass service or an authorized regional extract. Review the selected service's usage limits and applicable data licence.
- **Restrictions and checks:** Respect service capacity, request limits, attribution requirements, and applicable policies. The standard OSM editing API is not intended for read-only bulk extraction. Use a suitable read-only service instead.
- **Intent classification:** Geographic context only.
- **Suitability:** Useful for locality normalization, geographic enrichment, and mapping. It does not establish a person's identity, property requirement, buyer intent, or contact permission.
- **Current status:** Candidate for a small geographic proof of concept; no live extraction results are claimed in this document.

### Source C — Housing.com

- **Official URL:** https://housing.com/
- **Terms of use:** https://housing.com/terms-of-use
- **Geographic relevance:** Property listings and market information potentially covering the target Pune localities.
- **Information potentially available:** Advertised property type, locality, asking price, and listing details, depending on the listing.
- **Access method:** Manual review for source evaluation, or an expressly authorized feed, API, or written permission for programmatic collection.
- **Restrictions and checks:** Review the current terms and privacy policy. Confirm that the intended collection, storage, analysis, and commercial use are permitted before implementing automation.
- **Intent classification:** Primarily property supply/listing information. A listing alone does not prove that its author is a buyer.
- **Suitability:** Potential market research or listing enrichment source if authorized. Not approved for automated lead extraction until permission and intended use are established.
- **Current status:** Authorization pending; no automated scraping performed or claimed.

### Source D — OLX India

- **Official URL:** https://www.olx.in/
- **Terms of use:** https://help.olx.in/hc/en-us/articles/10957378342173-Terms-of-Use
- **Geographic relevance:** Classified listings that may include property advertisements in Pune and surrounding areas.
- **Information potentially available:** Advertised property details and listing descriptions.
- **Access method:** Manual policy review. Automated collection requires express permission or a licence that covers the intended use.
- **Restrictions and checks:** The published terms restrict automated scraping and the collection of personal data for commercial or unlawful purposes. Do not build a scraper or collect user contact details without the necessary express authorization.
- **Intent classification:** Depends on the listing. A seller's advertisement is not buyer intent; a buyer-seeking advertisement would still require careful review of permitted use and contact eligibility.
- **Suitability:** Not approved for automated lead extraction without express authorization.
- **Current status:** Excluded from automated collection unless written authorization is obtained.

### Source E — Public community discussions and forums

- **Candidate discovery:** Public community discussions concerning buying, purchasing, or seeking residential property in Hadapsar, Fursungi, or adjacent East Pune.
- **Geographic relevance:** Potentially high when the author explicitly identifies the locality.
- **Information potentially available:** Self-expressed property requirements, preferred locality, budget ranges, and timing, where voluntarily disclosed.
- **Access method:** Review platform policies and community rules. Prefer authorized APIs, explicit permission, or a manual review process that complies with the platform's terms.
- **Restrictions and checks:** Public visibility does not establish permission to scrape, retain personal information, build marketing profiles, or contact an author commercially. Do not extract private contact details or infer a phone number from a username.
- **Intent classification:** Potential direct or emerging buyer intent only when supported by explicit, contextual evidence. Rental requests must be classified separately.
- **Suitability:** Potentially valuable if an authorized collection method is confirmed. Do not automate collection until permission and intended use are established.
- **Current status:** Candidate category only; no specific community has been approved for collection.

### Source F — Government open-data resources

- **Candidate portal:** https://www.data.gov.in/
- **Geographic relevance:** Potentially relevant official datasets covering population, infrastructure, urban development, or other contextual indicators.
- **Information potentially available:** Dataset-dependent geographic, demographic, or public-sector indicators.
- **Access method:** Use published downloads or APIs under the applicable dataset licence and portal terms.
- **Restrictions and checks:** Review the licence, attribution requirements, update frequency, and any personal-data restrictions for each dataset.
- **Intent classification:** Geographic and market context, unless a specific authorized dataset explicitly supports another classification.
- **Suitability:** Useful for contextual analysis and enrichment, not inherently a source of identified buyers or qualified prospects.
- **Current status:** Candidate identified; no specific dataset has yet been selected or validated.

## 3. Intent classification rules

| Classification | Evidence required | Pipeline treatment |
|---|---|---|
| Direct purchase intent | Explicit statement of seeking to buy a property, supported by a permitted source reference | Candidate for qualification if the other required fields and contact conditions are satisfied |
| Emerging purchase intent | Contextual statement suggesting a possible future purchase without a clear current buying request | Keep separate from confirmed direct intent |
| Rental intent | Explicit request to rent or lease a property | Exclude from purchase-lead qualification unless the assignment explicitly includes rental prospects |
| Seller/listing intent | Person is advertising a property for sale | Treat as supply-side information, not buyer intent |
| Geographic context | Project, locality, amenity, infrastructure, or other geographic information | Use for enrichment only; never count as a buyer lead by itself |
| Unknown or unsupported intent | No reliable evidence of the person's requirement | Do not qualify as a buyer lead |

## 4. Minimum evidence required for a qualified record

A record must not be treated as a qualified prospect merely because a mobile number passes a regular-expression check.

Before qualifying a record, confirm:

1. The source and collection method are permitted for the intended use.
2. The source reference is recorded and reproducible.
3. The available evidence explicitly supports the stated property requirement.
4. The target locality and property requirement map to the project's allowed enums.
5. The mobile number passes strict format validation.
6. The source and available evidence support the identity-to-number association, where required.
7. Any applicable contact eligibility and consent requirements are satisfied.

**Important:** Format validation is not phone ownership verification, identity verification, consent, or permission to contact. A record that lacks a valid permitted contact method must not be counted as a qualified mobile lead.

## 5. Compliant proof-of-concept plan

The initial proof of concept will demonstrate the data pipeline without relying on unauthorized personal-data collection.

1. Use clearly labelled synthetic fixtures to exercise normalization, validation, scoring, and deduplication.
2. If needed, use an authorized geographic dataset to demonstrate locality enrichment.
3. Keep geographic reference records separate from person-level prospect records.
4. Record the source URL, retrieval date, access method, applicable licence or terms, and the outcome of each source review.
5. Before collecting actual buyer leads, obtain confirmation that the selected source and proposed use are permitted.
6. If a source blocks access or permission remains unclear, stop the attempted collection and document the blocker. Do not bypass authentication, CAPTCHA, HTTP 403 responses, or other access controls.

The proposed 1.5–3 second request jitter applies only where automated requests are authorized and the service's own policies permit them. It does not make otherwise prohibited scraping acceptable.

## 6. Source audit register

The following status labels describe the current assessment, not completed collection activity.

| Source | Current status | Next action |
|---|---|---|
| MahaRERA | Candidate identified | Confirm permitted access and reuse |
| OpenStreetMap / Overpass | Candidate for geographic PoC | Select a suitable service and verify its policy |
| Housing.com | Authorization pending | Review terms and obtain permission if required |
| OLX India | Automated extraction not approved | Obtain express authorization before considering automation |
| Public forums | Specific platform not yet approved | Identify a platform and confirm permitted access and use |
| data.gov.in | Dataset not yet selected | Select a relevant dataset and review its licence |

No source should be marked approved, accessible, or successfully tested until the relevant review or test has actually been completed.

## 7. Metrics and reporting

Record these metrics from actual executions:

- Candidate sources identified.
- Sources reviewed and sources with authorization confirmed.
- Source requests attempted, where applicable and permitted.
- Successful responses, denied requests, and other errors.
- Raw records received from each authorized source.
- Invalid records excluded.
- Duplicate records removed.
- Qualified prospects supported by source evidence.
- Records rejected because of missing evidence or unresolved permission.
- Geographic enrichment records, reported separately from prospects.

Do not substitute synthetic fixture counts for real prospect counts.

## 8. References

1. MahaRERA project registration: https://www.maharera.maharashtra.gov.in/project-registration-0
2. MahaRERA project updates: https://maharera.maharashtra.gov.in/project-updates
3. OpenStreetMap API usage policy: https://operations.osmfoundation.org/policies/api/
4. OpenStreetMap tile usage policy: https://operations.osmfoundation.org/policies/tiles/
5. Housing.com terms of use: https://housing.com/terms-of-use
6. OLX India terms of use: https://help.olx.in/hc/en-us/articles/10957378342173-Terms-of-Use
7. Government Open Data Platform: https://www.data.gov.in/

**Document status:** Initial source-discovery assessment. Live source validation, authorization checks, and genuine prospect collection remain separate tasks that must be documented only after completion.
