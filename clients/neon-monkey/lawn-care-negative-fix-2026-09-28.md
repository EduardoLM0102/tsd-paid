# Lawn care call leakage — fix (2026-09-28)

## Ticket
Client reported receiving calls for lawn care from Google Ads. Asked to ensure no
verbiage related to lawn care/lawn service is being used.

## Investigation
- Checked RSA headlines/descriptions on both live Search campaigns (`TSD_08.05_Leads_Search_Nonbranded_Trimming`,
  `TSD_04.09_Search_Branded_Evergreen_Mix`) — no lawn-related wording in any ad copy. All copy is tree
  trimming/stump removal specific.
- Checked keyword lists on both campaigns — all EXACT/PHRASE match, all tree-related (no "lawn" keywords
  anywhere). Ruled out ad copy and keyword *authoring* as the source.
- Pulled account-wide `search-terms` report, last 30 days (907 rows). Found 68 distinct search terms
  containing "lawn" (e.g. "lawn care fort worth", "lawn service near me", "buffalo outdoor lawn care",
  "jakes lawn care fort worth"), 902 of 907 total rows landing on
  `TSD_08.05_Leads_Search_Nonbranded_Trimming` (campaign `23825900343`).
- Impact from lawn-only search terms in that 30-day window: 133 impressions, 14 clicks, **$524.80 spend**,
  **3 conversions** (i.e. 3 actual calls/leads that were people looking for lawn care, not tree service) —
  matches the client's complaint directly.
- Root cause: `23825900343` and `23739724064` (Search Branded) had **zero negative keywords at any level**.
  Even with EXACT/PHRASE-only keyword lists, Google's close-variant/intent matching pulled in lawn care
  queries. By contrast, `TSD_04.25_PMAX_Evergreen` (PMax) already had "lawn" (PHRASE) negatived at the
  campaign level — that protection was just never extended to the two Search campaigns.

## Fix applied
Added `lawn` as a campaign-level negative keyword (PHRASE match) to:
- `TSD_08.05_Leads_Search_Nonbranded_Trimming` (`23825900343`) — root cause, where all the leakage was
- `TSD_04.09_Search_Branded_Evergreen_Mix` (`23739724064`) — preventive, brings it in line with PMax policy

All 3 live campaigns now carry the same "lawn" negative. No budget change, no approval needed (standard
negative-keyword hygiene).

## Not actioned (flagging, not fixing)
Same search-terms pull also surfaced ~50+ landscaping-company-name search terms on `23825900343`
(e.g. "cody landscape" 2 clicks/$125.80, "petersons landscaping", "kelley landscaping" — no conversions).
Landscaping is a distinct vertical from lawn care/tree service and wasn't part of this ticket. Worth a
follow-up negative-keyword pass if the client wants tighter targeting, but didn't touch it here to stay
in scope.

## Verify
Re-pull `read.py search-terms --customer-id 7953905280 --date-range LAST_7_DAYS` in ~1 week and confirm
no new "lawn" terms are accumulating spend on the live Search campaigns.
