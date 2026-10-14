# Gillespie's Heating and Cooling — Meta Ads log

Ad account `2014320269203822` ("Gillespie's Heating and Cooling"), owned by Gillespie's own Meta business (`1728244028382959`, not the Topservdigital business manager) but TSD-managed and Ads MCP-queryable. Not previously logged in this workspace — first touch on this account from the paid team's side.

---

## 2026-08-21 — First check-in: account has been live since July 2026, missed in the initial weekly report

**Why.** Building the first weekly report for Gillespie's (mirroring the GC Home Service format) and initially reported "no Meta presence" based only on the workspace's Google Ads/GTM logs, which only cover the Search build. Edu flagged that a Meta campaign exists. Checked directly via `ads_get_ad_accounts` / `ads_get_ad_entities` instead of trusting the absence of a workspace log, and found a real, active campaign predating this workspace's Gillespie's folder.

**Account inventory:**
- **Campaign:** `Lead Gen | HVAC | NKY & Cincinnati | Jul 2026` (`6992159403634`), objective `OUTCOME_LEADS`, ACTIVE, running since July 2026.
- **One ad set:** `NKY & Cincinnati | 30+ | Instant Form | $50/day` (`6992159408234`), $50/day, native Meta Instant Form lead ads (not website-pixel-based — leads are captured inside Meta, which is why the GTM container's still-filler Meta Pixel ID, noted in `google-ads-log.md`, hasn't blocked lead capture on this channel specifically. It would still matter for any future website-conversion or retargeting use of Meta.).
- **Five ads, all direct-response/consideration creative, no awareness/brand-building creative in rotation:**
  - `Gillespie | 2nd Opinion Testimonial | Jul 2026` — ACTIVE
  - `Gillespie | Seasonal Tune-Up | Jul 2026` — ACTIVE
  - `Gillespie | Top Notch Value | Jul 2026` — ACTIVE
  - `Gillespie | Repair vs Replace | Jul 2026` — ACTIVE
  - `Gillespie | Heat Pump & Mini-Split | Jul 2026` — PAUSED

**Performance, last 7 days (2026-08-15 to 2026-08-21):** 11,784 impressions, 241 clicks, $337.92 spent, CTR 2.05%, CPC $1.40, reach 4,342, frequency 2.71, cost per lead $112.64 (~3 leads).

**Performance, lifetime (since July launch):** 35,358 impressions, 764 clicks, $1,062.93 spent, CTR 2.16%, CPC $1.39, reach 8,512, cost per lead $96.63 (~11 leads).

**Flag, not yet actioned — Edu's note:** the whole creative set is bottom-funnel direct response (testimonial, seasonal offer, value prop, repair-vs-replace). Nothing at the awareness stage. **Next time we talk to this client, bring an awareness-layer campaign as a recommendation** — the account has been running lead-gen only since July with a single ad set and rising frequency (2.71 over the last week alone), and has no top-of-funnel content building reach/brand recall ahead of the direct-response asks.

**Open items:**
1. Confirm with the client/AM whether TSD is meant to be actively managing this Meta account, or whether it predates the engagement and needs a proper handoff/audit (budget approval on file, scope, etc., same written-approval rule as Google).
2. Real Meta Pixel ID is still filler in the GTM container (`gtm-log.md`), fine for the current Instant Form mechanism, but blocks any future website-conversion tracking or retargeting audience build on this account.
3. Decide whether the paused "Heat Pump & Mini-Split" ad should be resumed, replaced, or left retired.

---

## 2026-09-11 — Backfill: awareness campaign launched, lead-gen campaign now paused

**Why.** Pulling a full-lifecycle Google + Meta report for Edu, found the account structure had moved substantially since the 08-21 entry above, none of it logged in between.

**What actually happened (reconstructed from daily-level pulls, since it isn't in this log elsewhere):**
- The awareness-layer campaign flagged as an open recommendation on 08-21/08-24 was built and launched: `TSD_2026-08_TOF_AWARENESS_CBO_Evergreen` (`7000989212234`), objective `OUTCOME_AWARENESS`, one ad set `08/24/2026 - ZIP Codes | Broad`, four video ads (three testimonials plus a "What to Expect" piece). Live since August 24.
- It ran in parallel with the original `Lead Gen | HVAC | NKY & Cincinnati | Jul 2026` campaign (`6992159403634`) from August 24 through September 8, the lead-gen side still spending its normal ~$50/day and still producing leads the whole time.
- Lead-gen dropped to $5.02 on September 9 and shows zero delivery on September 10. Campaign-level status now reads `PAUSED`. **Confirmed with Edu 2026-09-11: intentional.** Right now the account has no active lead-capturing campaign, only the awareness campaign is live.

**Full lifecycle numbers (2026-07-01 to 2026-09-10):**
- Account total: 117,887 impressions, 1,477 clicks, $2,196.87 spent, 27 leads, $81.37 blended CPL, reach 28,493, frequency 4.14, CTR 1.25%.
- Lead Gen campaign (now paused): 80,903 impressions, 1,330 clicks, $2,024.13 spent, 27 leads, $74.97 CPL.
- Awareness campaign (active): 36,984 impressions, 147 clicks, $172.74 spent, no lead objective so none reported.
- By month: July $74.81/1 lead (very quiet, the campaign's real ramp didn't start until August), August $1,625.52/17 leads ($95.62 CPL), September 1 to 10 $496.54/9 leads ($55.17 CPL, best month on record so far, likely reflecting the lead-gen campaign's last strong week before pausing).

**Open item carried forward:** no timeline logged yet for when/if lead-gen comes back online alongside the awareness work. Worth a check-in next pull rather than assuming it stays paused indefinitely.

Client-facing full report (Google + Meta combined) built same day: `Gillespies-Heating-Cooling-Full-Report-Google-Meta_2026-09-10.html`.

---

## 2026-10-07: Meta account no longer visible to TSD

**Found during** the Growth Engine pull revision (`paid/relatorios/growth-engine-pull-2026-09/`). The account `2014320269203822` no longer appears in `ads_get_ad_accounts` (both pages checked). A direct `ads_get_ad_entities` call returns "Ad account not found or you do not have access." It was readable on 2026-09-28, when the 12-month pull ran, and Alex's agency-token baseline from the same day also has it.

**Context:** the account is owned by Gillespie's own business (`1728244028382959`), not Topservdigital, so the client side controls TSD's access. This could be the client removing TSD's partner access, as On The Way did with Google on 10-05, or a connector-side issue. **Not verified yet.**

**Last known state (09-28):** the awareness campaign `TSD_2026-08_TOF_AWARENESS_CBO_Evergreen - Ad Recall Lift` (`7000989212234`) was active. 12-month spend was $668.53, 141,858 impressions, $4.71 CPM.

**Open:** check in Business Manager whether TSD still has partner access to this account, then confirm with the AM before treating it as a client action.
