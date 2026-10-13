# Day 2 - Public Source Authorization Audit

**Project:** Amar Realty Lead Intelligence
**Target markets:** Hadapsar and Fursungi, Pune
**Audit date:** 13 October 2026

## Purpose
Identify public sources that may lawfully and technically support real-estate market research and prospect-intent analysis.

## Source review log

| Source | Intended use | robots.txt checked | Terms reviewed | Automated access authorized | Decision |
|---|---|---|---|---|---|
| 99acres | Property-market context; buyer-intent use unconfirmed | Pending | Pending | Pending | Do not scrape until verified |
| Reddit | Public discussion research | Not required to establish policy decision | Reviewed | No - authorization not obtained | Exclude from automated extraction pending permission |
| Official MahaRERA website | Registered-project and market context | Pending | Pending | Pending | Review official access rules first |

## Compliance rules
- Do not bypass authentication, access controls, CAPTCHAs, or blocks.
- Review applicable terms and robots.txt before automated requests.
- Where permitted, use a random delay of 1.5 to 3 seconds between requests.
- Collect only data necessary for an authorized purpose.
- Do not extract or infer personal phone numbers from public discussions without an appropriate authorization and lawful basis.
- A syntactically valid phone number is not proof of accuracy, consent, or permission to contact.
- Record actual request counts, outcomes, errors, and review findings. Never report unperformed checks as completed.

## Day 2 status
Source authorization is not yet confirmed. No live extraction should begin until the source's applicable rules have been reviewed.
