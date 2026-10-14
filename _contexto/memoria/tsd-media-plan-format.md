---
name: tsd-media-plan-format
description: "TSD quarterly Media Plan recipe — Gillespie's is the format precedent, plain B/W (not navy/gold), ratios over fixed dollars, ops guidelines stay internal"
metadata: 
  node_type: memory
  type: reference
  originSessionId: c5d51eba-01ec-4363-ad2a-423f7a70d50a
  modified: 2026-08-05T21:13:22.455Z
---

TSD client-facing **quarterly Media Plans** follow the **Gillespie's Heating and Cooling** doc as the format precedent (Edu found it on Slack; it was built on another machine and is not in the workspace). First one built in-workspace: `topserv-workspace/clients/lilypad-septic/` (see [[tsd-lilypad-septic]]). Second: `topserv-workspace/clients/cool-hand-electric/` (see [[tsd-cool-hand-electric]]), a 5-month bridge plan (Aug–Dec) rather than a strict quarter, and proof the channel mix isn't fixed — that one runs Google Ads (Search + YouTube) + Meta, no LSA at all, because Edu excluded an already-live LSA campaign from TSD's scope.

**Section order:** header block (client, quarter, city/site/phone, budget, platforms, market, tagline) → Overview (+ budget note) → What Each Channel Does → Who We're Targeting (personas) → Monthly Budget & Strategy (table + logic + Meta split) → Monthly Messaging (per month: Angle / Message / Channel focus) → KPIs → "Prepared for X · <quarter>".

**Styling:** plain black-and-white document look, gray rules, light-gray table header. **Not** the navy/gold used for TSD client *reports* ([[topserv-client-report-format]]). Target 3 pages.

**Why (Edu's calls, 2026-07-20):**
- **Ratios lead, dollars follow.** Build the plan on channel ratios (e.g. LSA 45% / Google 37% / Meta 18%) with dollar scenarios at 2–3 tiers, so it holds at any spend and survives a budget that isn't set yet.
- **Operational Guidelines do NOT go in the client PDF.** Gillespie's had them; Edu cut them from Lilypad's. Pre-launch gates, confirm-items, caveats and benchmark confidence go in a sibling `internal-notes.md`.
- No "(Confidential)" marker and no "to be confirmed before launch" closing line.

**How to apply:** write the md as source of truth, build with a per-client `build_plan.py` (md → HTML → Chrome headless → PDF). **Chrome's CLI cannot do a repeating per-page footer** — a `position: fixed` footer prints once, mid-document, overlapping text. Stamp the footer + page numbers on afterwards with PyMuPDF. Copy `clients/lilypad-septic/build_plan.py` as the starting point. Voice per [[tsd-client-facing-voice]].

Seasonality, benchmarks and channel logic must come from real research per client — Lilypad's LSA finding ("Sewage system" is a standalone LSA category, not a Plumbers sub-type) is the kind of thing that changes the whole channel structure and should never be assumed from the previous plan.

**Two more lessons from Cool Hand Electric ([[tsd-cool-hand-electric]], 2026-08-05):**
- **Always pull the account's real Google Ads data before assuming blank-slate.** Cool Hand looked like a fresh build from the intake alone, but the CID already had a live LSA campaign with real leads and spend. Query the account first (`google-ads-ratos`'s `tsd.sh` wrapper — MCC 4155514468, `.env.topserv` profile) — it can completely change what "channel mix" even means for the plan.
- **Verify specific marketing claims against the client's live site before writing monthly messaging copy** — see [[tsd-verify-specifics-before-copy]]. Don't fill seasonal messaging with generic-sounding specifics ("same-day service") without checking; real guarantees/offers/financing are often sitting on the site unused and make stronger copy anyway.
