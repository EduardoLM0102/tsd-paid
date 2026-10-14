# Neon Monkey — PMax Reactivation (2026-08-10)

**Trigger:** Follow-up to the [call-drop diagnosis](call-drop-diagnosis-2026-07-28.md), which found the early-July budget cut (pausing `TSD_04.25_PMAX_Evergreen` ~Jul 21) took the account's main reach engine offline and dropped call volume with it.
**Accounts:** PPC `7953905280` (MCC `4155514468`). Data/actions via `google-ads-ratos` skill (`tsd.sh` → `.env.topserv`).
**Approval:** Confirmed by Edu that Brock has signed off on re-enabling PMax.

## Pre-reactivation checks

**Conversion quality (Search campaigns, last 30 days):** found that `NMS-Website - GA4 (web) contact_us`, the largest conversion action on Nonbranded Trimming (28 of 43 total), is not a real lead — confirmed via GA4 Admin/Data API that `contact_us` is a duplicate of `page_view` scoped to `/contact/` (88 `contact_us` fires vs. 87 `page_view` fires on that page, same 28-day window). It fires on page load, not on form submit. Real form submits go through a separate GTM-confirmed path (`generate_lead`, fired off an actual `form_submitted` dataLayer push from the embedded GHL form). Stripping `contact_us` out:
- Trimming: 43 → 5 confirmed / 15 including an unverified-source "Phone Call" bucket. CPL moves from a headline $61 to $175–527.
- Branded: 2.37 → 0 confirmed conversions on $362.88 spend in the window.
- LSA (separate account, `1219885876`) unaffected — still the account's strongest real lead source at ~$70 CPL.

**Budget headroom vs. the $6,930/month Google Ads budget:**
- July actual: $4,368 (63% of budget; includes PMax through ~Jul 21).
- August MTD (Aug 1–10): $958.65, ~$105/day average — well under the $200/day nominal cap on the two live Search campaigns, because they're impression-share-limited (28–31% IS), not budget-limited.
- Remaining budget for the rest of August: $5,971.35 over 21 days ≈ $284/day of room.
- PMax's last configured budget, $110/day, fits inside that room alongside current Search burn without needing an increase — flagged that PMax previously averaged ~$227/day in June against what was then a higher budget, so watch the first few days in case delivery tries to outspend the $110 target.

## Action taken

Re-enabled `TSD_04.25_PMAX_Evergreen` (`21225221220`), status `PAUSED` → `ENABLED`, budget left unchanged at **$110/day**.

Live PPC footprint is now back to all 3 campaigns: PMax Evergreen ($110/day), Search Branded ($100/day), Search Nonbranded Trimming ($100/day) — $310/day nominal combined.

## Open items

- [ ] Monitor PMax daily spend vs. $110/day target for the first week; escalate if it's pushing well past it.
- [x] **Clean up the `contact_us` conversion action — done 2026-08-31.** Turned off `biddable` on the `CONTACT/WEBSITE` campaign_conversion_goal for both live Search campaigns (Nonbranded Trimming `23825900343`, Branded `23739724064`) via `update.py conversion-goal`; verified `False` on read-back. PMax (`21225221220`) already had that goal non-biddable, no change needed. Confirmed first that the CONTACT/WEBSITE bucket held no real lead signal on this account — only the junk GA4 `contact_us` duplicate plus a dead Universal-Analytics-era "Contact Us" goal and a hidden GA4 duplicate. Effect: `contact_us` now drops out of the **Conversions**/CPL column on both campaigns (per [[tsd-google-conversion-goals-mechanics]], it still reports under **All Conversions** — use that metric for any week-over-week comparison spanning this change, e.g. the 08-31 pull's $82.97 CPL headline will look worse next week purely from this fix, not from real performance decay). Reversible by flipping `biddable` back to `TRUE` on either campaign if needed.
- [ ] Geo-targeting cleanup (West Fort Worth concentration) is still blocked on Brock's location list — see [geo-targeting-review-2026-07-20.md](geo-targeting-review-2026-07-20.md). Re-enabling PMax at its old geo settings reintroduces the Grand Prairie/Dallas-side spillover noted there; worth revisiting once the location list comes in.
