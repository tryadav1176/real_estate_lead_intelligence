# Intent Signal Log: Classification Guide

Purpose: demonstrate how genuine property-demand signals are identified and
separated from listings, geography and general discussion. This is a
**manually reviewed evaluation sample**, not automated collection. Reddit's
robots.txt disallows bots (evidence: `evidence/robots_www.reddit.com_20261015T100607Z.txt`),
so posts are read by a human in a normal browser only.

## What you record (one row per post)

| Column | What to enter |
|---|---|
| Source_Channel | e.g. `reddit-manual-review` |
| Source_Reference | Post URL (must be unique) |
| Post_Date | YYYY-MM-DD |
| Review_Method | `manual_browser` |
| Prospect_Name | **Leave blank. Never record a username.** |
| Mobile_Number | **Leave blank. Never copy a number.** |
| Target_Zone | `Hadapsar`, `Fursungi`, `Adjacent_East_Pune`, or `Other` |
| Requirement | `1BHK`, `2BHK`, `3BHK`, `Residential Plot`, `Other`, `Unspecified` |
| Intent_Type | One of the six classes below |
| Intent_Evidence | Your own short paraphrase (about 25 words max), no quotes, no names |
| Contact_Visible_In_Post | `yes` or `no`. Only whether a contact appears, never the contact itself |
| Reviewer_Notes | Optional. No personal data |

## The six intent classes

| Class | Test | Treatment |
|---|---|---|
| `direct_purchase` | Person says they want to **buy** now or soon | Strongest buyer-side signal |
| `emerging_purchase` | Person is **considering or researching** a purchase, no firm request | Keep separate from direct |
| `rental` | Person wants to **rent or lease** | Buyer-side but not a purchase lead; report separately |
| `seller_listing` | Person is **advertising** a property (owner, broker, builder) | Supply side, not intent |
| `geographic_context` | Talks about a place, project, amenity or infrastructure | Context only, never a lead |
| `unknown` | Advice thread, opinion, joke, or unclear need | Not a lead |

## Illustrative examples (invented for training; NOT real posts)

- "We want to buy a 2 BHK in Hadapsar before March." -> `direct_purchase`, Hadapsar, 2BHK
- "Thinking about investing in East Pune next year, any areas to watch?" -> `emerging_purchase`
- "Need a 1 BHK to rent near Fursungi, budget 15k." -> `rental`, Fursungi, 1BHK
- "3 BHK flat for sale, Hadapsar, call owner." -> `seller_listing`
- "The new road near Magarpatta has improved traffic." -> `geographic_context`
- "Which broker platform is best for property searches?" -> `unknown`

## Decision checklist (apply in order)

1. Is the post about a person **seeking** a property? If it is advertising one -> `seller_listing`.
2. Is it advice, opinion or discussion with no stated personal need? -> `unknown`.
3. Is the need to **rent**? -> `rental`.
4. Is a **purchase** firm and current? -> `direct_purchase`; tentative or exploratory -> `emerging_purchase`.
5. Is it only about a place or infrastructure? -> `geographic_context`.
6. Locality outside Hadapsar, Fursungi and adjacent East Pune -> set Target_Zone `Other` (still log it; do not drop it).

## Sampling rules

- Review **15-20 posts**, deliberately including non-intent ones, so the log shows the distinction.
- Do not cherry-pick only strong signals. Record what you actually saw.
- One row per post URL. No duplicates.
- Do not open private messages, join private groups, or contact any poster.
- Do not store usernames, phone numbers, emails or profile links, even if shown.

## How to report it

Run `python -m src.intent_summary` and copy the counts into the DPR. Say plainly:

- This is a manual sample from a source whose robots.txt disallows automated access.
- No mobile numbers were collected, so **0 qualified prospects** come from it.
- Reddit's Public Content Policy may restrict commercial reuse; it has [not yet / now] been reviewed.
- Pipeline results on labelled synthetic data are reported separately and are not genuine prospects.
