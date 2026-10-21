# Intent Signal Classification Guide

**Purpose:** This document outlines the 6-tier intent classification taxonomy utilized by the automated scoring engine (`src/scorer.py`) to evaluate property-demand signals. 

Due to strict adherence to ToS and `robots.txt` compliance, commercial portals and social forums (e.g., Reddit) were excluded from automated extraction. Therefore, this classification logic is demonstrated in the pipeline using DPDP-compliant structured test fixtures (Route A) simulating an authorized opt-in form.

## 1. The Six Intent Classes & Scoring Weights

The pipeline automatically maps free-text inputs (from `Source_Reference`) into one of the following categories, assigning a strict numerical weight to the final `Lead_Score`.

| Class | Definition | Pipeline Treatment | Score Weight |
|---|---|---|---|
| `direct_purchase` | Prospect explicitly states intent to buy immediately or soon. | Strongest buyer-side signal. | **40 points** |
| `emerging_purchase` | Prospect is considering, researching, or asking about price trends. | Top-of-funnel buyer signal. | **25 points** |
| `rental` | Prospect is looking to rent or lease a property. | Non-purchase lead; tracked separately. | **10 points** |
| `seller_listing` | Individual advertising a property for sale (owner/broker). | Supply-side data. | **0 points** |
| `geographic_context` | Discussion of locality, infrastructure, traffic, or water supply. | Context/Enrichment only. | **0 points** |
| `unknown` | General advice, unclear need, or spam. | Dropped/Ignored. | **0 points** |

## 2. Pipeline Implementation (Automated Heuristics)

The `classify_intent()` function in `src/scorer.py` evaluates the `Source_Reference` text using keyword heuristics. 

**Illustrative Routing Examples:**
*   *"I am looking to buy a 2BHK immediately."* -> Trigger: "looking to buy" -> `direct_purchase`
*   *"What are the rates for future investment in East Pune?"* -> Trigger: "future investment" -> `emerging_purchase`
*   *"Looking for flatmates in Hadapsar."* -> Trigger: "looking for flatmates" -> `rental`
*   *"3 BHK flat for sale, call owner."* -> Trigger: "available for sale" -> `seller_listing`
*   *"The new road has improved traffic."* -> Trigger: "traffic" -> `geographic_context`
*   *"Which broker platform is best?"* -> Trigger: None -> `unknown`

## 3. Decision Checklist (Algorithmic Routing)

When a record passes through the scoring pipeline, the logic applies the following hierarchy:
1. **Supply Check:** Does the text indicate the user is selling? -> `seller_listing`.
2. **High-Intent Check:** Are there strong buyer keywords ("purchase", "immediate buyer")? -> `direct_purchase`.
3. **Research Check:** Are they asking about trends ("price trends", "investment")? -> `emerging_purchase`.
4. **Rental Check:** Is it a tenancy request? -> `rental`.
5. **Context Check:** Is it purely about local infrastructure? -> `geographic_context`.
6. **Fallback:** If no clear intent is detected -> `unknown`.

## 4. Compliance Note

This classification is performed exclusively on authorized data. Validating intent text does not override the necessity of valid consent. A record must possess a valid, 10-digit mobile number and originate from an authorized adapter to be successfully persisted to the SQLite database.