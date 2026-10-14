# Hawkins Siding — Google Ads: Car-Window Lead Issue

**Account:** Hawkins Siding and Exterior (Google Ads `2198608170`)
**Date:** July 6, 2026
**Prepared by:** Paid Ads (Edu)
**Status:** Resolved — fix live. Follow-up recommended.

---

## The issue (client complaint)
The client reported receiving a couple of leads asking about **car windows / auto glass** — not home siding or windows. These are wasted, off-service inquiries that cost ad budget and the client's time.

## What was happening
The client's active Search campaign was matching **generic "glass" searches** — e.g. *"glass repair near me," "glass company," "glass fixing near me."* People searching those terms are often looking to fix a **car window**, and they were landing on Hawkins' ads and calling in.

## Root cause
Hawkins' account already has a strong, ~400-term list of "blocked" (negative) keywords — including *car, auto, truck* — built to keep exactly these searches out.

**That block list was applied to the older campaigns, but never copied onto the current live Search campaign** (launched Apr 29). So the active campaign was running with **no protection at all** against off-service searches. This was a setup gap, now closed.

## What was done (fix is live)
Added automotive block terms to the active campaign so these searches can no longer trigger the ads:

> **car, auto, automotive, windshield, windscreen, vehicle, truck, car window, auto glass, window tint**

**Result:** car-window / auto-glass searches are now blocked going forward. Verified live in the account.

## Impact
- Stops budget leaking to auto-glass clicks.
- Cleaner lead flow for the client — fewer off-service calls.
- No effect on legitimate home-window demand (we deliberately kept genuine window-replacement searches, which are converting).

## Recommended next steps
1. **Sync the full block list** onto the active campaign (only the automotive slice is on it so far) — ideally as a **shared list** so any future campaign is protected by default and this gap can't recur.
2. **Monitor** remaining generic "glass" searches; add more blocks if car-glass calls continue.
3. **Tighten keyword match settings** on the window ad group to further reduce loosely-related searches.

---
*Internal note: full technical detail in `clients/hawkins-siding/google-ads-log.md`.*
