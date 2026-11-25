# C&S Air — Google Ads log (5563867754)

Registered in `contas.yaml` as of 2026-08-12 — found by listing all `customer_client` accounts
under the Topservdigital MCC (4155514468), since the client wasn't registered anywhere in this
workspace. HVAC, Mansfield TX. Account is named "(LSA) C&S Air, inc. / Derek O'Keefe" but carries
full PPC (Smart Campaign, Search x3, PMax) alongside the LOCAL_SERVICES campaign — same pattern as
Golden Plumbing / Watt's Right. A separate account literally named "C&S Air Inc." (3144198344)
exists under the same MCC but is CLOSED and inaccessible via the API — not usable, do not confuse
the two.

**Authority:** Edu, confirmed live-execution authority in-session, 2026-08-12.

---

## 2026-11-16 — fu-141 DECIDED: Heating Search PAUSED (0 leads after the last repair-only week) + fu-166 review top-up

**Read 11-10..11-15 (Heating Repair alone, $15/d, $12 cap):** $123.62 / 519 impr / 16 clicks / 0 conv (all_conversions 0: no calls from ads, no forms, no taps). CallRail 817-442-6949 (Google Ads tracker): only the 11-11 Branded existing-customer call, nothing from Heating; website-pool calls 11-10..11-16 carry no gclid. Search terms still troubleshooting ("troubleshooting my furnace", "why won t my heat turn on", "furnace fan keeps running with thermostat off", "my heat pump fan is not spinning"). Keywords: 'furnace not working' $46.65/7 clk, 'heating service' $27.17/3, 'heating repair' $25.15/3, 'heater not working' $17.22/2.
Campaign life 10-26..11-15: **$582.05 / 67 clicks / 0 leads** (Repair 35 clicks since 10-27). Nonbranded Search has now failed 5 times on this account: do not rebuild it without a client offer.

**APPLIED ~13:50 UTC (`cs_heating_pause_1116.py`, validate-only then --apply):** campaign `TSD_10.23_Search_Nonbranded_Heating` 24383234148 ENABLED → PAUSED, read-back PAUSED. Live now: Branded + LSA only (~$20-25/d + LSA).

**Review top-up (AT 03fff3a7, row 4387c0fc):** full cycle 10-17..11-15 = **$2,343.85 / 18 / $130.21** (was $2,062.53 / 16 / $128.91). Delta 11-13..11-15 = $281.32 (LSA $219.28 + Heating $62.04), 2 new LSA leads on 11-15 (msg 351893642 duct + dryer vent cleaning, new home/allergies, NEW, charged; call 352296435 urgent duct cleaning Mansfield, suspected dead animal, ACTIVE, charged, whisper transcript). Split: 5 new + 12 existing + 1 form. LSA $392.44 / 12 = $32.70; Branded $95.07; PMax+Cooling+Heating $1,381.01 for 0. Notes rewritten (heating pause, follow up on the 2 new LSA leads). Stage untouched (at Host Review Call, call 11-17 14:45 UTC).
Note: LSA spent $219 on 11-13..11-15 for 2 charged leads; watch the per-lead price.

---

## 2026-08-12 — full PPC audit + first-pass fixes

### Audit findings

- **True cost per lead is $78, not the $37–$55 the UI headline numbers imply.** YTD (Jan 1–Aug 11
  2026) PPC spend = $17,230.42. Real leads (verified phone calls + web lead forms only) = 221.0
  (216 calls, 5 forms). $17,230.42 / 221 = $77.97.
- **"TSD_03.13_Pmax_Evergreen" is a SMART campaign, not standard Performance Max**, despite the
  name. Its reported 310.5 "conversions" = 148.5 real leads + 162 soft actions (108 "Local actions
  - Directions" + 54 "Clicks to call") that get pulled into the primary Conversions column *only*
  on this campaign — every other campaign in the account correctly excludes those same conversion
  actions per the account-level `include_in_conversions_metric: false` flag. Confirmed at the
  segment row level, not inferred.
- **Nonbranded Search has failed twice**: March campaign (TSD_03.13_Search_NonBranded_Evergree,
  $5/day budget) — $763.03 spent, 0 conversions. July campaign
  (TSD_07.05_Leads_Search_Nonbranded_Cooling, $55/day) — $1,365.29 spent, 1 conversion. Root
  causes, not budget:
  - Core high-intent terms sat at QS 1–2 (`hvac repair near me` = 1, `ac repair near me` = 2).
  - Impression share on the July campaign was only 10%, split 59% lost-to-rank / 32%
    lost-to-budget — rank was the bigger constraint.
  - Zero competitor-brand negatives. Of visible search terms since Jul 1, 69% of spend ($336 of
    $484) went to competitor company names (Milestone, Derden, Compass, Houk, Casa Mechanical,
    O'Daniel, Anderson, Anthony, Christmas A/C, Copeland, Texas Air & Heat, The AC Lady, Chill
    Brothers, TK Mechanical, American Heating, Walker HVAC, Markl and Sons, "angies list") via
    broad match, with 0 conversions from any of them.
  - Bonus bug: the March campaign had "Arlington, **Virginia**" mixed into its otherwise correct
    DFW-Texas geo set.
- **The one campaign with 100% clean conversions was sitting paused**: "Leads-Performance Max [Feb
  18th 2026]" (real PMax) — 38 conversions, all verified calls/forms, $50.7 CPA. No data-backed
  reason found for it being off while the noisier Smart Campaign ran at $80/day.
- Branded Search is healthy: 81.4% impression share, QS 8–10 on all "C&S Air" variants, 33.5 clean
  call conversions, $50.6 CPA. 18.6% of impressions still lost to Ad Rank — headroom, not urgent.

### Actions taken (live, same session)

1. **Un-paused "Leads-Performance Max [Feb 18th 2026]"** (campaign 23584282933) — status
   PAUSED → ENABLED.
2. **Removed the "Arlington, Virginia" geo-target** (campaignCriteria/23655482784~1027027) from
   TSD_03.13_Search_NonBranded_Evergree.
3. **Added an 18-term competitor-brand negative keyword list** (PHRASE match) to both nonbranded
   Search campaigns (TSD_07.05_Leads_Search_Nonbranded_Cooling, TSD_03.13_Search_NonBranded_Evergree) —
   18/18 created on each.
4. **Attempted the same on the Smart Campaign (TSD_03.13_Pmax_Evergreen) — rejected, all 18/18.**
   Google's API returns `OPERATION_NOT_PERMITTED_FOR_CONTEXT` / trigger `EXPRESS(EXPRESS_SMART)`:
   Smart Campaigns do not accept manual negative keywords at all. This is a real structural
   limitation of the Smart Campaign product, confirmed via the API, not a workaround-able
   permission issue. Reinforces the case for eventually rebuilding this campaign as standard PMax.

### Still open (not executed — needs design/build work, not a toggle)

- **Consolidate the two nonbranded campaigns into one** — TSD_03.13_Search_NonBranded_Evergree
  ($5/day, 0 conversions ever) is redundant with TSD_07.05_Leads_Search_Nonbranded_Cooling and
  should likely be retired rather than relaunched. Left paused.
- **Rebuild TSD_03.13_Pmax_Evergreen as standard Performance Max** to match the clean campaign's
  reporting/control and to actually be able to apply negatives — this is a full campaign rebuild
  (new asset groups, audience signals, budget decision), not a same-session task.
- **Factual error in retired campaign's ad copy**: TSD_03.13_Search_NonBranded_Evergree's RSA
  (adGroupAd 194364221677~800648892371) has a headline "Family owned and operated since 1958" —
  contradicts the real site and every other live ad in the account, which correctly say "Since
  2005" / "20+ years." Not fixed (campaign is paused and slated for retirement, not relaunch), but
  flagged so it isn't accidentally reactivated as-is.

---

## 2026-08-12 (same day, cont'd) — QS root-cause fix + nonbranded relaunch

Checked the real site (candsair.com) instead of guessing, per house rule. Confirmed via WebFetch:
company founded 2005 (matches most ad copy, contradicts the "since 1958" headline noted above),
and three purpose-built service pages exist that map directly to the three failing ad groups:

- `/services/residential/air-conditioning/ac-repair/` — same-day repair, upfront pricing, 24/7
- `/services/residential/air-conditioning/ac-maintenance/` — tune-up/maintenance specific
- `/services/residential/air-conditioning/emergency-ac-repair/` — 24/7 emergency specific

Every RSA in TSD_07.05_Leads_Search_Nonbranded_Cooling (all 6 ads, 2 per ad group) was pointing at
the bare homepage `https://www.candsair.com/` instead of these pages — the same failure pattern
seen on Watt's Right (bare homepage instead of the purpose-built page that actually matches search
intent). Ad copy itself was already good/relevant per ad group; this was purely a post-click
landing-page-relevance problem, which is consistent with the QS 1–2 scores on core terms.

**Fixed:** updated `final_urls` on all 6 ads to their matching dedicated service page (AC Repair →
`/ac-repair/`, AC Maintenance → `/ac-maintenance/`, AC Emergency → `/emergency-ac-repair/`).

**Re-enabled TSD_07.05_Leads_Search_Nonbranded_Cooling** (PAUSED → ENABLED) now that both blockers
— competitor negatives and landing-page relevance — are addressed. Budget left unchanged at
$55/day (no budget approval needed, status toggle only). Watch QS on `ac repair near me` / `hvac
repair near me` over the next 1–2 weeks now that clicks land on relevant pages instead of the
homepage.

---

## 2026-08-12 (same day, cont'd) — closed out for the day

Decision: retire TSD_03.13_Search_NonBranded_Evergree now (it's already paused so there's no cost
to acting immediately, nothing gained by waiting), but hold the Smart Campaign → standard PMax
rebuild for a few days — that Smart Campaign is the account's single biggest lead source, a
migration deserves a proper asset build rather than a rush, and we're still mid-observation on two
other changes made today (real PMax re-enabled, nonbranded relaunched).

- Tried `update.py campaign --status REMOVED` on TSD_03.13_Search_NonBranded_Evergree —
  **the Google Ads API rejects `REMOVED` via the standard campaign update path**
  (`INVALID_ENUM_VALUE`); removal requires a separate `remove` operation the tool doesn't expose
  (deliberately — it's destructive/hard to reverse). Left the campaign PAUSED, which already
  achieves "not running, not spending" — full deletion wasn't necessary to close out the risk.
- Instead fixed the actual residual risk directly: the false "Family owned and operated since
  1958" description on that campaign's RSA (`ads/800648892371`) was removed via a direct
  `AdService.mutate_ads` update to `responsive_search_ad.descriptions` (3 remaining descriptions,
  above RSA's minimum of 2). Verified post-update: the false claim is gone, the other 3
  descriptions are intact. Campaign can now sit paused indefinitely with no live factual error, no
  further action needed even if the client or someone else stumbles into it.

**C&S Air closed out for 2026-08-12.** Next actions are calendar-gated, not open work: check QS on
the nonbranded terms in ~1–2 weeks, then revisit the Smart Campaign → PMax rebuild once the
re-enabled campaigns have a real performance track record.

---

## 2026-09-03 — calendar-gated check-in (read-only)

- **"Leads-Performance Max [Feb 18th 2026]" — the account's cleanest lead source — has been dark
  for 30+ days despite showing `status: ENABLED`.** `campaign.primary_status` = `ENDED`,
  `primary_status_reasons` = `[CAMPAIGN_ENDED, MISSING_CALL_EXTENSION]`. Zero impressions/clicks in
  both LAST_7_DAYS and LAST_30_DAYS. Root cause: an `end_date` in the past — not visible via
  `read.py campaigns`/`insights.py` (plain `status` field only), only via a raw `campaign.primary_status`
  / `primary_status_reasons` GAQL pull. `campaign.start_date`/`end_date` themselves throw
  `UNRECOGNIZED_FIELD` on this account. **Not fixed** — flagged for Edu's call since it touches a
  campaign specifically re-enabled by client-facing decision on 8/12; needs a decision on whether
  clearing/extending the end date needs approval per budget-approval doctrine (it shouldn't, since
  total budget is unchanged, but flagged rather than executed).
- **The 8/12 landing-page fix on nonbranded Search did not move Quality Score after 3 weeks.**
  "hvac repair near me" QS 1, "ac repair near me" QS 2 — unchanged. 30-day totals for
  TSD_07.05_Leads_Search_Nonbranded_Cooling: 205 clicks, $1,198, 0 conversions. Competitor-negative
  list from 8/12 is holding (no competitor brand names in 30d search terms).
- Weekly pulse: $1,195/7d total spend, 2 real conversions (both LSA, $65 CPL). No live changes made
  — read-only check.

---

## 2026-09-07 — nonbranded "0 conversions" investigation → full Google Ads + GTM + GA4 tracking audit

Edu asked why nonbranded Search (`TSD_07.05_Leads_Search_Nonbranded_Cooling`, campaign
`23828098448`) shows 0 conversions in Google Ads and whether GA4 tells a different story. This
turned into a full cross-system audit once the GA4 data didn't hold up to scrutiny.

### Part 1 — GA4 vs Ads reconciliation for nonbranded (30-day window)

- Google Ads confirmed: 242 clicks, $1,437 spent, **0.0 conversions** on campaign `23828098448`.
- GA4 (property `310229049`, "C&S Air Inc. - GA4"), traffic tagged to that exact campaign ID showed
  187 sessions and real engagement — but most of it was **page-view-style custom events, not
  leads**: `contact_us` (32) fires on every load of `/contact-us/`, not on form submit;
  `apply_for_financing` (6) is the same pattern on its own page. The real submitted-lead event,
  `generate_lead`, fired **zero times** from this campaign in 30 days (only 4 total site-wide,
  all on `/contact-us/`). So on actual submitted leads, GA4 agrees with Ads: real number is 0, not
  a hidden pool of missed conversions.
- The one real signal Ads missed: **4 `phone_click` (tap-to-call) events** from this campaign.
  Edu pushed back asking to confirm this wasn't undercounted given a large chunk of google/cpc
  traffic in GA4 shows no campaign name at all (`(referral)`/`(not set)`, 95 phone_clicks in that
  bucket). Cross-checked by landing page: the nonbranded campaign's ads only point to 3 pages
  (`/ac-repair/`, `/ac-maintenance/`, `/emergency-ac-repair/`); 85 of those 95 unattributed
  phone_clicks landed on the **homepage**, which nonbranded never sends traffic to — that bucket
  belongs to the Smart Campaign, not nonbranded. **Confirmed: 4 is the real number**, not an
  undercount. At $1,437 spend that's ~$359 per click-to-call — doesn't change the QS-driven
  diagnosis from 8/12–09/03, just moves the floor from 0 to 4.

### Part 2 — full tracking audit (Google Ads + GTM + GA4), account-wide

Edu asked for a complete audit across all three systems. Findings, most impactful first:

1. **CallRail is installed but its Google Ads integration is dead.** Two conversion actions exist
   in the account — `First Time Phone Call` and `Repeat Phone Call` (category `DEFAULT`, i.e.
   generic website-tag conversions, not native call-forwarding tracking like
   `local_services_phone_lead`/`Calls from ads`) — both **ENABLED with zero conversions in 30+
   days, account-wide**, despite GA4 logging 181–604 real `phone_call` events (30d/90d) that don't
   originate from the audited GTM container at all (almost certainly CallRail pushing straight to
   GA4 via its own integration, bypassing Ads). These two action names are CallRail's standard
   default naming for its native Ads integration — it was set up at some point and is now
   disconnected or never finished. **This is the single biggest lever in the account**: fixing it
   would surface real call volume as real conversions for every campaign, not just nonbranded.
2. **GA4 property has zero Google Ads link.** Confirmed via Admin API
   (`properties.googleAdsLinks.list` returns empty). No gclid → friendly-campaign-name resolution,
   no conversion-import path as a backup.
3. **Account-level manual UTM tracking template stacks with auto-tagging** (`customer.auto_tagging_enabled
   = True` + `customer.tracking_url_template = {lpurl}?utm_source=google&utm_medium=paid&utm_campaign={campaignid}...`).
   No campaign-level overrides — applies uniformly to all 6 campaigns. Combined with #2, this is why
   GA4 shows raw numeric campaign IDs (`23828098448`, etc.) instead of names, and why a chunk of
   Smart Campaign traffic loses attribution entirely — Smart Campaigns are known to apply
   account-level tracking templates inconsistently.
4. **GA4's configured key events are stale, from a form system that no longer exists.** Admin API
   shows 4 key events: `purchase` (irrelevant default), `form_submit_contact_us`,
   `form_submit_installation`, `form_submit_schedule_service`, `click`. Checked 90 days — the three
   `form_submit_*` events have **fired zero times**; they're leftovers from a form plugin that
   predates the site's move to embedded GoHighLevel forms. The GHL form's real event
   (`generate_lead`, 23 fires/90d, a genuinely working signal) was **never added as a key event**.
   So GA4's "conversions" metric has been meaningless for months — counting a generic `click` event,
   missing the one event that represents an actual submitted lead.
5. **GTM container (`GTM-P2MR2T2`, confirmed live version 7 matches the audited draft workspace 8)
   has exactly one path from the site into an Ads conversion**: GHL form submit (via a
   `postMessage` listener on `msgsndr.com`) → `form_submitted` → the one "Google Ads | Event |
   Lead" tag (`awct`, conversion label `CAD6CJj9lIYcELXz3tEC`, mapped to the `Submit lead form -
   Web` action). **No tag anywhere fires an Ads conversion off a phone click** — the `tel:` click
   trigger only feeds GA4 and Meta. This is account-wide, not nonbranded-specific.
   - Ruled out a wrong-account mismatch: GTM's Ads conversion ID variable (`AW-708295093` /
     `708295093`) matches `customer.conversion_tracking_setting.conversion_tracking_id` exactly.
6. **Bonus, same container: Meta Pixel ID variable is the literal placeholder `123456789`.** Every
   Meta tag (Lead, PageView, Phone Click, Email Click) has been firing into a fake pixel — if Meta
   ads are supposed to be running/optimizing off this, they're getting nothing.
7. **Two GA4 web data streams on the same property, different measurement IDs**, both pointed at
   candsair.com: `G-XYVZWLC9T8` ("C&S Air, Inc") and `G-CNKY2157HM` ("C&S Air Inc. - GA4", the one
   the live GTM container actually uses). Worth checking once the site's stable whether the first
   one is still firing from some legacy plugin (possible double-counting or dead cruft).

**Conclusion for the original question:** nonbranded's "0 conversions" isn't nonbranded-specific.
The account has exactly one working path into Ads (a rare GHL form widget, ~1 fire per 4 days
site-wide) and zero path for phone activity except when Google's own native call-extension
tracking happens to catch it directly in the ad — which nonbranded doesn't have. Other campaigns
show partial call conversions only because of that native ad-level tracking, unrelated to the
site/GTM/GA4 stack. The 4 confirmed click-to-calls were never going to become an Ads conversion
regardless, because that pipe doesn't exist for any campaign.

### Part 3 — site outage found mid-audit (unresolved)

While pulling landing pages, every URL on candsair.com (home, contact, all 3 nonbranded landing
pages, even `/wp-admin/`) returned a WordPress "critical error" (HTTP 500), confirmed via headers
as a real WordPress.com/Atomic-hosted response, not a bot block. GA4's daily trend showed real
sessions recorded earlier the same day, so this looked like a fresh outage — flagged to Edu as
urgent.

**Edu reported the site loads fine for him.** Re-tested from a second, independent vantage point
(WebFetch, different network entirely from the original curl) — **also got a 500**, 6/6 failures
across both methods. Working theory: the response carries `Vary: Cookie`, and my requests carry no
cookies (fresh visitor) while Edu's browser likely already had cookies for the domain from a prior
visit. If a plugin crashes specifically on a *missing* cookie, that would break the page for every
brand-new visitor — i.e. everyone arriving from a paid ad click — while looking completely fine to
anyone who's been there before, including a manual check in an already-cookied browser. **Not yet
confirmed.** Asked Edu to test candsair.com in a private/incognito window (guarantees zero
cookies) to confirm or kill the theory. Still open as of end of session.

### Ad-hoc scripts written this session (kept in `.claude/skills/google-ads-ratos/scripts/`, not cleaned up — same convention as other one-off `*_conv_by_action.py` files in that dir)

- `cs_air_conv_by_action.py` — conversions by action + campaign, plus full conversion-action config list.
- `cs_air_gtm_detail.py` — full tag/trigger parameter dump for the GTM container.
- `cs_air_gtm_vars.py` — GTM variable values (GA4 measurement ID, Ads conversion ID, Meta pixel ID) + full raw tag/trigger/variable listing.
- `cs_air_ads_tracking_audit.py` — account/campaign tracking template + auto-tagging settings, full conversion action detail, link checks.
- `cs_air_ga4_adslink.py` — GA4↔Ads link check, data stream listing, Admin API key-events list.
- `cs_air_gtm_live_check.py` — confirms the live published GTM container version matches the draft workspace that was audited.

### Open items (not executed, need Edu's call or the client's involvement)

1. Confirm/resolve the site-500-for-fresh-visitors theory (incognito test, pending).
2. Reconnect CallRail → Google Ads call conversion integration.
3. Add a phone-click or confirmed-call conversion path into Ads via GTM.
4. Link GA4 property `310229049` to Ads account `5563867754`.
5. Clean up GA4 key events (drop the 3 dead `form_submit_*` + `click`, add `generate_lead`).
6. Once #4 is done, consider dropping the manual account-level tracking template in favor of auto-tagging alone.
7. Fix or remove the placeholder Meta Pixel ID.
8. Still calendar-gated from 09-03: the PMax `end_date`/`primary_status: ENDED` issue is still unresolved.

---

## 2026-09-15 — weekly PPC snapshot (read-only)

Standard 7-day metric pull (LAST_7_DAYS), PPC only — LOCAL_SERVICES campaign excluded per the usual split.

- Spend: $1,326.10 | CPC: $1.33 | CPL: $221.02 | Total Conversions: 6 | Conv Rate: 0.60%
- Branded: 5 conversions, $47.23 CPL (TSD_03.13_Search_Branded_Evergreen)
- Unbranded: 0 conversions, $400.12 spent, CPL N/A (TSD_07.05_Leads_Search_Nonbranded_Cooling)
- Impression Share (Search, account-level): 18.10%
- LSA (excluded from above): 30 clicks, $130 spend, 2 conversions, $65 CPL

Two caveats carried forward from the 09-07 audit, still unresolved:
- 1 of the 6 total conversions comes from the Smart Campaign (TSD_03.13_Pmax_Evergreen), which per the
  08-12 finding still pulls Directions-clicks/phone-icon-taps into its Conversions column — likely not a
  real lead.
- Unbranded's 0 conversions may be an undercount, not a true zero — CallRail's call-tracking integration
  to Ads is still dead account-wide as of 09-07, so no phone-call conversions reach Ads from any campaign.

No live changes made this session.

---

## 2026-09-15 — Tracking rebuild

**Reported by Edu via chat, not executed by Claude this session.**

Tracking rebuilt and fixed. Old tags deactivated to make sure they don't disrupt or interfere with
the new setup.

---

## 2026-10-05 — Weekly 7-day optimization (Agency Titan task): 17 Nonbranded negatives, 1 DIY keyword paused

**Authority:** Edu, in chat ("go to C&S"). Negatives + 1 keyword pause only. No budget, bid or campaign status changes.
Script `csair_apply_1005.py` (in this folder); all changes read back from the account.

**Last 7 days (09-28 → 10-04), PPC only, LSA excluded:**

| Campaign | Spend | Clicks | Conv | CPL |
|---|---|---|---|---|
| TSD_03.13_Pmax_Evergreen (Smart Campaign) | $585.11 | 2,689 | 9 | $65 |
| TSD_07.05_Leads_Search_Nonbranded_Cooling | $399.85 | 47 | 0 | – |
| TSD_03.13_Search_Branded_Evergreen | $138.23 | 17 | 1 | $138 |
| **Total** | **$1,123.19** | **2,753** | **10** | **$112** |

Prior week: $959.96, 17 conv, $56 CPL. Account search IS 19.3% (64% lost to rank, 17% to budget). LSA same week: $65, 1 lead.

**Found:**
1. **The Smart Campaign is now ~100% Display.** $584.78 of its $585 went to CONTENT, 2,685 clicks at $0.22 (prior week
   888 clicks). All 9 of its conversions are `[TSD] Click to call` (a tap on the number, not a confirmed call). Smart
   Campaigns don't expose network settings or negatives through the API (see 08-12), so this is a keep / pause / rebuild
   as PMax call for Edu. Not touched.
2. **Nonbranded keeps failing:** $399.85 / 47 clicks / 0 conv this week, $1,667 / 3 conv over 30d ($556 CPL), still on
   Max Clicks with a $10 cap. Top 30d spenders with 0 conv: "licensed ac repair" $410, "air conditioning repair service"
   $332 (QS 3), "ac not cooling fix" $217, "annual ac maintenance" $161. Only "ac repair cost estimate" converted (3).
   The CallRail→Ads gap from 09-07 may still undercount calls here (tracking rebuilt 09-15, not re-audited).
3. Search terms: new competitor names, DIY/informational questions ("how often should ac filters be changed", "what does
   ac maintenance include", "why my ac is not turning on") and RV AC (dometic).

**Changed:**
- Nonbranded `23828098448`, campaign-level PHRASE (17): michael and sons, lex hvac, trutex, always there air, a 1 air,
  comfort masters, family first comfort, matco, airplex, barnett ac, burnside, enoch hvac, klund, minuteman heating,
  how often, what does, dometic. Replayed against 30d terms: 13 clicks / $85.62 blocked, 0 conversions, no active keyword.
- Keyword "ac not cooling fix" (PHRASE, AC Repair ad group `197197281278`, criterion `1571435633198`) ENABLED → PAUSED.
  DIY intent, $216.77 / 31 clicks / 0 conv in 30d.

**Open (Edu's call):**
- [ ] Smart Campaign on Display: pause, or rebuild as standard PMax with brand exclusions (also the long-standing rec).
- [ ] Nonbranded: pause it, or keep testing with fewer keywords ("licensed ac repair" and "air conditioning repair
  service" are the next pause candidates).
- [ ] "Leads-Performance Max [Feb 18th 2026]" still ENABLED + ENDED (since 09-03), decision still pending.
- [ ] Re-check whether phone calls from the site reach Ads after the 09-15 tracking rebuild.

---

## 2026-10-05 (cont.) — Recommendations, not executed (Edu to revisit 2026-10-06)

**Context:** Edu asked for recommendations after the weekly pass above. Nothing below has been done.

**Checked first:** the site-500 theory from 09-07 is not happening now. Homepage, `/ac-repair/`, `/ac-maintenance/` and
`/emergency-ac-repair/` all return 200 to a cookie-less visitor (curl, 10-05). Load time is 2.6–4.8s on desktop.

**In order of impact:**

1. **Fix call tracking before judging anything else.** Last 14 days, every conversion Ads saw except 1 form and 1 call
   from ads was a `[TSD] Click to call` tap. `First Time Phone Call` / `Repeat Phone Call` (CallRail) have logged 0 since
   the 09-15 rebuild. Bidding is learning from taps, and Nonbranded's "0 leads" may be an undercount.
   Fix: reconnect CallRail → Google Ads, or link GA4 to Ads and import the GA4 `phone_call` event (hundreds of real calls
   per month in GA4 per the 09-07 audit, none reaching Ads). Then make the tap action secondary.
2. **Swap the Smart Campaign for the ended PMax.** `TSD_03.13_Pmax_Evergreen` (Smart, $80/d, ~half of PPC) went ~100%
   Display this week and its conversions are taps. `Leads-Performance Max [Feb 18th 2026]` had 100% clean conversions
   at ~$51 CPA before its end date killed it. In the UI: clear its end date, add the missing call asset, add brand
   exclusions, move the Smart Campaign's $80/d into it (constant total, no ticket). Do it after #1, or PMax learns from
   taps too. Reported conversions will drop when the Smart Campaign's taps go away, so tell the AM first.
3. **Trim Nonbranded, don't kill it yet.** Pause the 3 biggest 0-conversion spenders: "licensed ac repair" ($410/30d),
   "air conditioning repair service" ($332, QS 3), "annual ac maintenance" ($161), ~$900/mo for nothing. Keep "ac repair
   cost estimate" (the only converter) and the emergency terms. Add heating ad groups (furnace / heater repair): it's
   October, the campaign is AC-only, and the site sells heating. If it's still at 0 two weeks after calls are tracked
   properly, pause it and move the budget.
4. **Leave Branded alone.** $38 CPL over 30d, 82% IS. This week's single $138 lead is noise.
5. **Lower priority:** landing page speed (could help Nonbranded's QS 1–3), GA4 ↔ Ads link (also the route for #1),
   placeholder Meta Pixel ID `123456789` in GTM.

**What Claude can execute via API:** the #3 keyword pauses and (likely) building the heating ad groups. The #2 end-date
clear probably needs the UI (end date isn't even readable via GAQL on this account). #1 is CallRail / GA4 side.

### Decide on 10-06
- [ ] #1 tracking route: CallRail reconnect or GA4 import
- [ ] #2 Smart Campaign → PMax swap (and timing)
- [ ] #3 keyword pauses + heating ad groups

---

## 2026-10-06 — Weekly 7-day task (next cycle, 1 day after the 10-05 pass): no changes

**Read-only.** Last 7 days (09-29 → 10-05), PPC only: $1,085.46, 2,884 clicks, 10 conv, $108.55 CPL, Search IS 19.7%.
Smart Campaign $560.87 / 2,818 clicks / 9 conv (all `[TSD] Click to call` taps); Nonbranded $386.13 / 47 / 0;
Branded $138.46 / 19 / 1. LSA $175.23, 2 leads.

The 10-05 negatives are working: "lex hvac", "always there air", "a 1 air" now show EXCLUDED. New Nonbranded terms since
the change are real service searches (hvac repair, hvac services, central air conditioner repair near me).

**Agency Titan:** task `e7b4a5bc` closed; KPI - Google Search entry 10-06 with the full note in Lead Quality Notes.
The 10-05 recommendations (call tracking, Smart → PMax swap, trim Nonbranded + heating) are still waiting on Edu.


---

## 2026-10-09 — Revisit of the 10-05 recommendations (read-only, nothing changed)

Script: `google-ads-ratos/scripts/cs_air_revisit_1009.py`. Change history 10-05 → 10-09: only Edu's 10-05 API changes
(17 Nonbranded negatives + 1 keyword pause). **None of the three recommendations has been acted on.**

**Last 7 days, PPC only:** Smart $554.39 / 3,309 clicks / 16 conv · Nonbranded $415.04 / 48 / 1 · Branded $133.22 / 21 / 3.
LSA $110.23 / 1.

1. **Tracking: still broken for website calls.** By conversion date 09-15 → 10-08: `First Time Phone Call` /
   `Repeat Phone Call` (CallRail uploads) = **0**. What counted: `[TSD] Click to call` 57 (Smart 43, Branded 12, NB 2),
   `Calls from ads` 2, `Calls from Smart Campaign Ads` 2, `[TSD] Submit lead form` 2 (NB; the rebuilt form tag works),
   LSA 3. call_view since 09-15: 7 calls from ads, 4 over 60s. GA4 `310229049` still has **no Google Ads link**, so the
   GA4 `phone_call` import route isn't ready either (also a new `click` key event in GA4, junk but harmless while unlinked).
2. **Smart Campaign: worse.** 7d $554.29 of $554.39 on Display (CONTENT), 3,307 clicks; tap conversions up 9 → 16.
   30d $2,467.58 / 46 conv. Feb PMax `23584282933` still ENABLED + ENDED (`CAMPAIGN_ENDED`, `MISSING_CALL_EXTENSION`).
3. **Nonbranded: same story.** 30d $1,706.88 / 228 clicks / 4 conv = **$427 CPL**. Status LIMITED (bid strategy).
   The 3 pause candidates, 30d, all still ENABLED: "licensed ac repair" $447.95 / 57 / 0, "air conditioning repair
   service" $360.86 / 49 / 0 (QS 3), "annual ac maintenance" $154.64 / 22 / 0 → **$963 for 0**. Only converter:
   "ac repair cost estimate" $264.89 / 4 conv. Still no heating ad groups (AC Maintenance / AC Repair / AC Emergency).
4. Branded: 30d $537.20 / 16 conv ($34), mostly click-to-call taps.

**Still waiting on Edu:** tracking route (CallRail reconnect vs GA4 link + import), Smart → PMax swap (UI for the end
date), go on the 3 keyword pauses + heating ad groups.

## 2026-10-09 (cont.) — Smart Campaign PAUSED

**Authority:** Edu, in chat ("pause that"). `TSD_03.13_Pmax_Evergreen` (`9313861131`, Smart, $80/d) ENABLED → **PAUSED**
via `update.py campaign --status PAUSED`, read back: `PAUSED / CAMPAIGN_PAUSED`.

Why: 7d $554 of $554 on Display, conversions = phone-number taps; Smart Campaigns take no negatives and no network settings.
Cost of the pause: since 09-15 it also drove 4 real calls from ads (2 over 60s) + 2 `Calls from Smart Campaign Ads`.

**Effects to flag:**
- Account total spend drops ~$550/week (budget out of rotation: $80/d). Not moved anywhere yet: the Feb PMax
  `23584282933` is still ENDED + missing a call asset, so the swap needs the UI (clear end date, call asset, brand
  exclusions, then $80/d). Serving now: Branded $80/d, Nonbranded $55/d, LSA $23/d.
- Reported conversions will drop (~16 taps/week gone). Not a real lead drop.
- Total spend change → AM ticket (same as Zen Air's NB pause on 10-08).

## 2026-10-09 (cont. 2) — CallRail checked directly (API, read-only). Corrects the 10-05 tracking theory.

Access: CallRail API key from Edu, saved in `topserv-workspace/.env.callrail` (gitignored), helper
`google-ads-ratos/scripts/callrail.py`. Account 792265907 "TopServ Digital Clients", C&S company 580688522.

**Integrations (company 580688522):**
- **Google Ads: state FAILED.** Points at the right place (MCC 4155514468 → 5563867754), first-time vs repeat. This is
  why `First Time Phone Call` / `Repeat Phone Call` read 0. Fix = reconnect in CallRail UI (Integrations → Google Ads).
- GA4: active, sends ALL calls to `G-CNKY2157HM` (this is where the GA4 `phone_call` events come from).
- Google Business Profile: FAILED, tied to TSD's OLD Google login (Cornerstone Marketing Solutions = TSD's former
  name, thecsms@gmail.com). Same login on all 10 GBP integrations in TSD's CallRail (9 failed, 1 pending): C&S,
  Spencer, Napps, Integrate Comfort, All Seasons Air, Supreme, JR Michalski, Cartwright, Cornerstone itself, All Heart
  (pending). Of 7 Google Ads integrations, only C&S's is failed. Reconnect with TSD's current login (Edu, via browser).
  The GBP tracking number itself keeps working (306 calls), so this is housekeeping, not lost calls.

**Calls Aug 1 → Oct 9: 393, all inbound.**
- 306 on the GBP tracking number + 31 website calls whose visitor came from GBP → **~86% of all calls are Google
  Business Profile.** Then Google organic 17, **Facebook Ads 7 website calls (+2)** (utm_source=facebook, campaigns
  "promo"/"non_promo": someone runs Meta for C&S, not TSD), referral sites (expertise.com 7, insurancexdate.com 4),
  Direct 6, ChatGPT 3.
- **Website calls from Google Ads visitors: 0 in 10 weeks.** No call has a gclid. Not a tracking break: swap.js
  (company 580688522) is on all pages, and the ad landing URLs 301 to /services/... keeping `?gclid=` intact (tested).
- CallRail "Google Ads" tracker 817-442-6949 (the Nonbranded call asset): 6 calls since Aug, 1 since 09-15.
- Smart and Branded call buttons use the main line (817) 477-2665, so those calls bypass CallRail; Google logs them
  itself (`Calls from ads` / `Calls from Smart Campaign Ads`: 7 calls since 09-15 in call_view, 4 over 60s).
- Weekly calls ~40–50 Aug to mid-Sep → 27 (wk 09-28) → 18 (Oct 5–9): seasonal, GBP-driven.

**What this changes vs 10-05:**
- The "hundreds of GA4 `phone_call` events not reaching Ads" were **GBP and organic calls**, not missing ad calls.
  Importing them via GA4 would not surface hidden ad leads. Reconnecting CallRail → Ads is still worth doing
  (cheap, needed going forward) but **will not reveal a backlog**: there were ~0 gclid calls to upload.
- **Nonbranded's near-zero is real**, not an undercount. Paid Google is a small call source for C&S: ~2–3 real ad
  calls/week + a few forms, vs ~35 GBP calls/week.
- Strategic read: GBP + LSA are the call engine. Before rebuilding Nonbranded, weigh moving that money to LSA
  (if LSA is budget-limited) and keeping Branded + a revived PMax.

## 2026-10-09 (cont. 3) — CallRail reconnected by Edu (access@topservdigital.com), verified via API

- **Google Ads integration: failed → ACTIVE**, now linked directly to 5563867754 (was via MCC 4155514468), first-time
  vs repeat, send calls on. Expect few uploads: ~0 calls with gclid (see cont. 2).
- **GBP integration: failed → ACTIVE** on access@topservdigital.com.
- ⚠ Side effect in the same session: the CallRail Google Ads integrations for Spencer, Integrate Comfort and All Heart
  (all routed through MCC 4155514468) went active → DISABLED. Spencer was receiving 25 call conversions/30d. Logged in
  their client logs; needs re-enabling.
- GBP integrations for Spencer, Napps, ICS, All Seasons Air still FAILED on the old thecsms@gmail.com login.
- Noticed: Napps, All Seasons Air and Supreme Google Ads integrations send to 8810470846 (not the clients' own Ads
  accounts), so those accounts get no CallRail conversions. Separate check.

## 2026-10-09 (cont. 4) — Nonbranded trimmed; Feb PMax can't be revived in place

**Authority:** Edu, in chat: "Revive the Feb PMax but keep within the current budget / Trim nonbranded as suggested".
Also: **"We CANNOT stop counting lead taps as of right now because they might generate calls"** → `[TSD] Click to call`
stays in the lead category, biddable. Don't re-propose making it secondary until Edu revisits.

**Applied** (`csair_apply_1009.py`, read back): Nonbranded keywords PAUSED: "licensed ac repair" (crit 326155282700),
"air conditioning repair service" (1425607556), "annual ac maintenance" (297465191423). $963 / 30d, 0 conv.

**Feb PMax `23584282933` facts (corrects earlier notes):** it only ran **Feb 18 → Mar 31 2026** (end_date_time
2026-03-31), $1,927 / 296 clicks / 38 conv (37 `Calls from ads`, 1 form) ≈ $51. Max Conversions, tCPA $50. Geo Mansfield
city, PRESENCE_OR_INTEREST. 1 asset group, homepage, 50 assets (NOT_ELIGIBLE while ended). Only biddable goal:
PHONE_CALL_LEAD / CALL_FROM_ADS. No call asset. (GAQL: use `campaign.end_date_time`, not `end_date`.)

**Blocked by Google (validate_only):** budget is a $3,000 CUSTOM_PERIOD total. Swapping in a daily budget →
CANNOT_CHANGE_BUDGET_PERIOD; extending the end date → "Duration too long for total budget" (counts from Feb 18).
→ **Path: copy it in the UI with a $30/day daily budget** (Edu via Claude extension, with brand exclusions). Once the
copy is live: Nonbranded budget $55 → $25 so the account total stays the same. Not done yet.

LSA note: spends ~$12/day of its $23/day budget → not budget-limited, can't absorb Nonbranded money.

## 2026-10-09 (cont. 5) — Feb PMax rebuilt as a copy and LIVE; Nonbranded $55 → $25 (constant total)

**Authority:** Edu: "can't you just duplicate the campaign or copy it?" (after "revive the Feb PMax but keep within the
current budget"). API has no copy endpoint → rebuilt 1:1 from the same asset IDs (`csair_pmax_copy_1009.py`), then
enabled + funded (`csair_enable_pmax_1009.py`). Both read back.

**New campaign `TSD_10.09_PMax_Leads_Mansfield` `24336822932`** (asset group `6757854855`): ENABLED / LEARNING.
- $30/day DAILY, Max Conversions tCPA $50, no end date, start 2026-10-09.
- Mansfield (1026591) **PRESENCE** (old was presence or interest), English.
- Brand guidelines: business name "C & S Air", logo 360×360, landscape logo. 6 sitelinks. **Call asset 817-442-6949**
  (CallRail Google Ads tracker, new vs the old campaign).
- Asset group: homepage, 15 headlines, 5 long headlines, 5 descriptions, 20 images, search themes AC Repair / heating /
  Furnace Install / hvac. Image extraction off, final URL expansion on (as before).
- Differences vs the old one, forced by Google: 2 headlines + 3 long headlines dropped (old group was over today's caps:
  "Get Your AC Ready", "Call to set an appointment", "Call our HVAC experts to set an appointment", "Top-rated residential
  and commercial services", "1 Trusted Heating and AC Experts Mansfield, TX | C&S Air"); 2nd logo 333622193251 rejected
  (dimensions); audience signal not reusable (bound to the old asset group).
- Biddable goals: PHONE_CALL_LEAD/CALL_FROM_ADS (calls + taps, per Edu), SUBMIT_LEAD_FORM/WEBSITE (forms), DEFAULT/WEBSITE
  (CallRail calls). SIGNUP/WEBSITE (GA4 "Sign Up") set non-biddable. Old campaign bid on calls from ads only.
- Copy to refresh later: description "Keep cool this summer!…" and "Their team of experts…" (3rd person).

**Nonbranded `23828098448` budget $55 → $25/day.** Net: $55 = $25 + $30, account total unchanged → no budget ticket.
Old Feb PMax `23584282933` untouched (ENABLED + ENDED). Brand exclusions on the new PMax: pending (Edu via Claude extension).
**Check ~10-23:** PMax spend vs $30, conversions by action (real calls vs taps vs forms), search terms/placements.

## 2026-10-09 (cont. 6) — Brand exclusion verified; budget total restored to $238/day

**Brand exclusion** (Edu via Claude extension): account-level brand list "C&S Air brand" (C&S Air, Inc / candsair.com,
already in Google's directory) excluded on the new PMax only. API read-back: BRAND_LIST negative, shared set 12264921928.

**Budget.** Edu: "make whatever is needed to keep the same ad spend, reallocate, pause - whatever. Of course, in a clever
way." + no AM ticket when the overall budget doesn't change. Last week's real spend ≈ $1,212 (~$173/d). Branded (spends
~$15–20/d of $80, target IS) and LSA (~$12/d of $23) can't absorb more; Nonbranded 14d = 2 conv / $748, not worth it.
Applied (`csair_rebalance_1009.py`, read back):
- New PMax `24336822932`: **$30 → $110/day** (takes the Smart's $80 slot). Geo: Mansfield only → **the same 10 locations
  Branded/Nonbranded target** (Arlington, Burleson, Fort Worth, Grand Prairie, Kennedale, Mansfield, Midlothian,
  Benbrook, Rendon, Westover Hills), PRESENCE. tCPA $50 kept as the efficiency guardrail.
- Branded `23653583753`: target-IS CPC ceiling **$10 → $15** (14d IS 77%, 23% lost to rank, avg CPC $6.92).
- Serving budgets: PMax $110 + NB $25 + Branded $80 + LSA $23 = **$238/d = this morning's total → no AM ticket.**
  Expected real spend ~$170/d if PMax finds leads at ~$50; if it underspends, that's the tCPA holding, revisit at check.
- Campaign name still says "_Mansfield" though geo is now the full service area.

## 2026-10-09 (cont. 7) — Branded call asset moved to the CallRail number

**Authority:** Edu, "go for it on #1". Branded `23653583753`: call asset (817) 477-2665 (main line, asset 339651005960,
bypassed CallRail) removed, CallRail Google Ads tracker 817-442-6949 (asset 343525874146) linked
(`csair_branded_call_asset_1009.py`). Read back: **all 3 live campaigns (Branded, Nonbranded, new PMax) now use
817-442-6949**, which forwards to the same main line. Calls from ads now show in both Google (call_view) and CallRail.

**Visibility after today:** every call (source, duration, first-time, answered/missed) via CallRail API; website calls
from ad clicks upload to Ads (integration fixed); ad call-button calls in CallRail + Ads; forms in Ads.
**Still blind:** lead quality / booked jobs. 0 of 393 calls have a CallRail lead status; no CRM outcomes in Ads. Next:
find out what C&S books jobs in, then offline conversions (or CallRail qualification). GA4 not linked to Ads, stale key
events (reporting only). Facebook ads run by someone else, no access.

## 2026-10-13 — Weekly 7-day pass (Agency Titan task): read-only, KPI entry logged, changes staged

**Numbers (PPC only):** $1,154.71, 34 conv, $33.96 CPL (prior $107.86/10). All 34 are [TSD] Click to call taps, no call_view calls. New PMax (live 10-09) $459.71 in 4 days, 18 taps, $25.54 — **99% of it on Display ($456)**, same pattern as the Smart campaign it replaced; early flag for fu-032 (10-23). Smart $288.21 10-06..08 (13 taps). Nonbranded $270.95/31 clk/1 tap. Branded $135.83/18 clk/2 taps, 80% IS, $7.55 CPC. KPI Health = Mixed.
**Search terms:** Branded phrase 'CS Air' matched airlines ($39: great southern / china southern airlines); Nonbranded 'cost to fix ac leak in car', coil price research, competitors (texas best, honest abe).
**Staged, not applied:** Branded phrase negatives 'airlines', 'airline', 'southern'; Nonbranded phrase negative 'car'.
**LSA:** $0, 0 leads, 42 impr, 6 clicks, top impression 95.7%, budget $23.26/d (Underspending). Prior week $175.23/2 leads.
AT tasks closed: Google 6673eb2c (KPI 61bd5fea), LSA 2b937ad8 (KPI ee4ca0c8).

Pull: `paid/weekly-7day/weekly_pull.py` (window 10-06..10-12 vs 09-29..10-05), summary/KPI via `weekly_summary.py` / `weekly_kpi.py`. Full note is in the AT KPI entry's Lead Quality Notes.

## 2026-10-20 — Weekly 7-day + 14-day pass (Agency Titan tasks, Gui): read-only, KPI entries logged, changes staged

**Numbers (PPC only, 10-13..10-19 vs 10-06..10-12):** $1,099.43, 20 conv, $54.97 CPL (prior $1,146.26 / 34). 19 of 20 = [TSD] Click to call taps; call_view shows 1 real call (Branded, 60s+), 0 forms. PMax 24336822932 $796.65 / 304 clk / 17 taps, **100% Display (content network) again**, budget-limited at $110/d. Branded $164.82 / 20 clk / 3 conv, 80% IS, $8.24 CPC. Nonbranded $137.96 / 16 clk / 0 conv, 21% IS (75% rank-lost). KPI Health = Mixed.
**Search terms:** NB paying for DIY questions ('what to do if your ac is not cooling', 'why is ac not cooling properly'), coil cleaning research, competitors (airtron, frontdoor). Branded 'CS Air' phrase still matches china southern / southern airline ($0 this week).
**14-day (10-06..10-19):** QS 1-2 on 5 core repair kws; maintenance kws $7.90-9.60 CPC at QS 3; Branded RSAs both AVERAGE; no audiences anywhere; same 10 service-area geos, Presence only, nothing leaking; NB is cooling-only going into heating season. PMax 14d $1,249.62 / 35 taps / 0 real calls.
**Staged, not applied:** pause 'ac tune up cost', 'best ac repair near me', 'hvac repair near me'; NB phrase negatives what to do / why is / whats included / airtron / frontdoor / car; Branded phrase negatives airlines / airline / southern / china; Branded RSA refresh; observation audiences; dismiss opt-in recs; PMax Display question → fu-032 (10-23).
**LSA:** $0, 39 impr, 4 clk, top impr 100%; lead report 2 phone leads (1 booked, 1 active), both uncharged. Budget $23.26/d, Underspending (reach-limited).
AT tasks completed 10-20: Google ce4a9827 (KPI 726c2e79), 14-day ecc58c10 (toggles must be set in UI), LSA bab8023c (KPI bb0987bb), Meta 79c812a8 (KPI a1ee2c75, still no ad account).

## 2026-10-20 — APPLIED the 10-13 staged negatives (Edu: "the staged changes, they are ALL approved")

`paid/weekly-7day/staged_1013_apply_2026-10-20.py`, read-back confirmed. Branded 23653583753 PHRASE negatives **airlines, airline, southern** (30d: blocks china/great
southern airlines etc., $39, 0 conv). Nonbranded 23828098448 PHRASE **car** (car AC repair questions, $14.22, 0 conv). No
conflict with live keywords.

## 2026-10-22 — Pre-read for the two-week check (fu-032), read-only, 10-09..10-21 vs 09-26..10-08

Pulled one day early (Edu asked). `weekly_pull.py` with 13-day windows. CallRail API returned 429 on the agency account, so the CallRail side of the check is still owed.

**PPC total:** $2,179.63, 46 conv, $47.38 CPL (prior 13d: $1,946.63, 27 conv, $72.10).
- **New PMax 24336822932:** $1,468.19 (~$113/d, full $110 budget, status BUDGET_CONSTRAINED), 39 conv, $37.65 CPL, under the $50 tCPA. **But $1,464.54 of it (99.8%) is Display**, $0 on Search, $1.51 YouTube. All 39 conversions are [TSD] Click to call taps from Display. Same pattern as the Smart campaign it replaced. Brand exclusion is attached (10-09, web UI).
- **Branded 23653583753:** $346.37, 39 clk, 5 conv (3 taps + 2 calls from ads, both 60s+), IS 78.4% (was 77%), rank-lost 21.6%. CPC $8.88 vs $6.82 before, so the $15 ceiling raised cost ~30% for +1.4 pts of IS. The airline terms ($29.14 'great southern airlines') were 10-11, before the 10-20 negatives.
- **Nonbranded 23828098448:** $303.11, 35 clk, **0 conv** (prior 13d $715.73 / 1). QS 1–3 where reported. Terms are mostly price/DIY research ('ac tune up cost', 'evaporator coil cost', 'why is ac not cooling'). Spent $47.22 on 10-21 vs $25 budget.
- **Smart 9313861131:** paused 10-09, $61.96 tail.
- **LSA:** $43.16, 2 leads (1 tap, 1 message), all on 10-21.
- Real calls from ads (call_view): 2, both Branded, both 60s+. No forms.
- PMax description still says "Keep cool this summer!" (asset group text, not changed).

**Read:** the account's cost per lead looks better only because Display taps are cheap. PMax has bought no Search traffic in 13 days. Taps stay counted (Edu's rule), but whether these taps become real calls is the open question, and it needs CallRail (calls by source 10-09..10-21, answered 60s+).
**Options for Edu (not applied):** (1) PMax can't be kept off Display by a setting, so the lever is budget: move part of the $110 to Branded/LSA or a phrase/exact Search build, once CallRail shows whether the taps were real calls; (2) Nonbranded: pause the price/DIY keywords ('ac tune up cost', 'ac repair cost estimate') or pause the campaign, 0 conv in 26 days at ~$1,000; (3) swap the summer description for a heating one.

## 2026-10-22 (later) — Action plan after the two-week read (Edu asked), nothing applied yet

**What Google already shows about PMax (no CallRail needed):** `[TSD] Click to call` is type CLICK_TO_CALL = taps on the call button in the ad. 38 of 39 PMax taps were on mobile, from Display. Google logged **0 counted "Calls from ads" from PMax** (the only 2 are Branded), and **0 First Time / Repeat Phone Call uploads** in 10-09..10-22 (so no website calls with a gclid either). PMax optimizes to the taps because taps are its primary conversion, and Display is where taps are cheapest. CallRail tracker 817-442-6949 (the call asset on all 3 campaigns) will show how many taps became actual calls; API was 429 on 10-22.

**Plan:**
1. **10-23, CallRail:** calls on 817-442-6949 from 10-09 to 10-22: count, answered, 60s+, first-time. Decision rule: if PMax's 39 taps produced only a handful of real 60s+ calls, PMax is not buying leads.
2. **PMax ($110/d):** if (1) confirms, cut to ~$30/d or pause. Root cause for Edu to decide: as long as taps are primary (Edu's 10-09 rule), PMax keeps buying cheap Display taps. Options: (a) keep the rule and starve PMax, or (b) make taps secondary on PMax only, with "Calls from ads" + CallRail calls as the goal.
3. **Nonbranded (Cooling, $25/d):** $1,018 and 0 conversions in 26 days, all AC keywords in late October. Pause it and build a small heating Search campaign (furnace/heater/heat pump repair, phrase + exact, Mansfield service area, Max Clicks with a CPC cap, pointing at the site's heating page). Money comes from the PMax cut, total stays inside $238/d.
4. **Branded:** keep. Optionally go back from $15 to a $12 ceiling: the $15 bought +1.4 pts IS for ~30% higher CPC.
5. **Copy:** replace "Keep cool this summer!" in the PMax asset group with a heating line.
6. If total spend ends up lower than today because PMax is cut and heating takes time to ramp, tell the AM (spend drop, not a budget increase).
7. **Recheck** ~10-30.

## 2026-10-23 — CallRail check (fu-085): PMax produced 0 calls

CallRail API back (the 10-22 400s after the 429 were the helper URL-encoding commas in `fields`; fixed in `paid/weekly-7day/callrail_calls_pull.py`).
- **Ad call number 817-442-6949, 10-09..10-22: 4 calls total** (10-16 38s first-time; 10-19 84s first-time; 10-19 105s repeat; 10-20 95s first-time). Before that, 1 call since 09-26.
- **Google call_view / phone_calls 10-09..10-22:** PMax 24336822932 = **25,214 phone impressions, 0 phone calls**. Branded = 2 calls (10-19 84s, 10-20 95s). Nonbranded 0. Old Smart 0.
- **Website calls from Google Ads clicks: 0** (no gclid, no google/cpc in 23 pool calls; they are organic, GBP, Facebook Ads (someone else's), referral, direct).
- Whole account: 110 CallRail calls 09-26..10-22, 83 of them (75%) on the GBP number.

**Conclusion:** PMax's 39 "conversions" (10-09..10-21) were taps on the ad's call button that never became phone calls. $1,468 bought 0 calls and 0 forms. The action plan from 10-22 (later) stands. Waiting on Edu: cut or pause PMax, pause Cooling NB + heating Search build, and whether taps stay the goal.

## 2026-10-23 (later) — APPLIED: PMax + Cooling Nonbranded PAUSED (Edu: "Let's kill the C&S Pmax and Cooling campaigns")

`update.py campaign --status PAUSED` with explicit --customer-id, read-back via GAQL: TSD_10.09_PMax_Leads_Mansfield 24336822932 PAUSED ($110/d), TSD_07.05_Leads_Search_Nonbranded_Cooling 23828098448 PAUSED ($25/d). Live now: Branded 23653583753 ($80/d budget) + LSA ($23.26/d). Nothing else changed.

**Budget freed: $135/d of budget (~$136/d of actual spend 10-09..10-21, ~$4,100/month).** Branded and LSA can't absorb it:
- Branded spends ~$27/d of its $80 (13d: $346). Impression share 78%, 0% lost to budget, 22% lost to rank. More budget does nothing; raising the $15 CPC ceiling could buy part of the missing 22% for maybe +$5–10/d.
- LSA spends ~$9/d of its $23 (30d: $283, 198 impressions, 10 leads, 4 booked). It's limited by impressions, not budget. More reach needs settings (service area, job types, hours, reviews), not money.
- So account spend drops from ~$170/d to ~$36–45/d unless something new is built. Options for Edu: (a) heating Search campaign (phrase + exact, Max Clicks with a cap) at ~$25–40/d, (b) LSA settings review, (c) tell the AM spend drops ~$4k/month.

## 2026-10-23 (later 2) — BUILT PAUSED: TSD_10.23_Search_Nonbranded_Heating 24383234148 (Edu: "Build it for me")

`build_search_heating_1023.py`, validated (146 ops) then applied as one atomic mutate. Read-back: PAUSED, Maximize Clicks with a **$12 CPC cap**, **$30/day**, Google Search only (no partners, no Display), presence-only geo = the same 10 locations as Branded, English, AI Max text + URL expansion opted out.
- **Heating Repair** (ad group 196718543930, 17 keywords: phrase furnace/heater/heating/heat pump repair, furnace/heater/heat not working, no heat, furnace/heating/heater service + 6 exact 'near me'/Mansfield) → /services/residential/heating/heating-repair/. RSA 829360703689.
- **Heating Replacement** (ad group 198402775381, 15 keywords: furnace replacement/installation, new furnace, heat pump replacement/installation, new heating system...) → /services/residential/heating/heating-replacement/. RSA 829312302192.
- Assets: call asset 343525874146 (CallRail 817-442-6949), 7 sitelinks (3 new: Heating Repair, Heating Replacement, Heating Maintenance + Schedule Service, Reviews, Financing, About), 7 callouts (3 new: Upfront Pricing, All Makes & Models, Background-Checked Techs + Family Owned, Licensed & Insured, 20+ Years, Same Day Service), business name + logo.
- Negatives: 73 phrase (water heater/tankless/pool/space heaters, car/rv/auto, how to/diy/manual/parts, jobs, retail, cost/price/cheap, ~30 competitors from the Cooling terms) + 'Competitos May' list. The Cooling campaign's 708 negatives were NOT copied (they block furnace, heat, replacement, burner, not working).
- Copy: only claims from the heating pages (checked 10-23). No '24/7', no 'Since 1958'.
- Both RSAs REVIEW_IN_PROGRESS. Launch = enable the campaign on Edu's go once approved.

## 2026-10-26 — AT optimization tasks (Gui, via Claude)

**90-Day Google (https://app.agencytitan.com/tasks/instance/3fe702b7-83fe-4112-8d0f-64eec2906df3), read-only, completed.** 07-28..10-25 PPC: $12,883.94 / 12,411 clk / 141 conv / $91.38 (prev 90 $8,656.69 / 76). 85% of it is now paused: Smart $5,858.90 (10-09), NB Cooling $3,520.65 / 4 conv = $880 CPL (10-23), new PMax $1,594.93 / 40 taps / 0 calls (10-23). Live: Branded $1,909.45 / 33.7 conv / $56.73, IS 81.2% (rank-lost 18.8%); **Heating Search 24383234148 ENABLED by Edu 10-26 08:08** ($30/d, Max Clicks $12 cap, both ads approved, 32 kws eligible, no data yet).
Conv = 102 taps (72%), 18 Calls from ads (Branded), 18 Smart calls, 3 forms. **Stalled:** CallRail First/Repeat 0 in 90d (no gclid calls to upload), forms 0 in 30d (last 09-25), Smart / Local actions / Sign Up dead primaries. Staged: tracking task (Gui to create): form test incl. heating pages, demote dead primaries, check heating call asset + call_view after week 1.
Hours: Branded real calls all 08:27-17:43, 21-06h $150.80 / 0 conv, Sunday $190.50 / 0; Cooling NB 6pm-6am $1,885.20 / 1 conv. Demographics too thin. No audiences (lists: all visitors 2,700, converters 72). Geo 100% in the 10 service-area locations (PRESENCE).
**Staged, not applied:** heating ad schedule 6:00-20:00 Mon-Sat; optional Branded schedule 6:00-21:00; observation audiences on Branded + heating; pause/rewrite Branded RSA 800192030388 (3.9% vs 15.1% conv rate); 'CandS Air'/'CS Air' headline; dismiss partners / Display expansion / Max Conv / budget / keyword recs. First heating read ~11-02. Toggles (UI): Stalled Conversions Found = Yes, Schedule Adjusted = No, Demographics Excluded = No, Audiences Excluded = No, Locations Excluded = No.

## 2026-10-26 — LAUNCHED: TSD_10.23_Search_Nonbranded_Heating 24383234148 (Edu: "turn the campaign on")
Both RSAs (829360703689, 829312302192) REVIEWED / APPROVED before launch. `update.py campaign --status ENABLED` with explicit --customer-id; read-back: ENABLED, primary_status ELIGIBLE, Max Clicks $12 cap, $30/d; all 17 campaign assets (7 sitelinks, 7 callouts, call 817-442-6949, name, logo) ELIGIBLE. Live now: Branded ($80/d budget, ~$27/d actual) + LSA ($23/d) + Heating ($30/d). First check ~11-02 (fu-095): spend vs $30/d, CPC vs cap, search terms (water heater/car/price/competitors), calls on 817-442-6949 + forms.

## 2026-10-27 — AT optimization tasks (Gui, via Claude)

Read-only, nothing applied, no budget changes. Toggles to set in the UI are listed at the end.

**7-Day Google (https://app.agencytitan.com/tasks/instance/68c403ef-2ec9-4c93-9cfa-9a76a3c8149d), completed, KPI 245e5ce3 (Health Mixed).** 10-20..10-26 PPC: $617.95, 158 clicks, 7 conv, $88.28 CPL, $3.91 CPC (prior $1,093.91 / 20 / $54.70). 6 of 7 conv were taps (5 PMax before its 10-23 pause, 1 Branded). 1 real call (Branded, 95s, 10-20). 0 forms. Branded $200.68 / 23 clicks / IS 91.3% (rank-lost 8.8%), spending about $29/d of $80. PMax $350.84 was 100% Display up to the pause. Cooling NB $66.43 / 0. Heating 24383234148 got 1 day (10-26): 10 impr, 0 clicks, learning, so no verdict. Search IS 33.0%. Staged: Branded phrase negative 'products' ('c&s air products' $3.66), Heating first read 11-02, Branded RSA 800192030388 pause/rewrite, tell AM the live total dropped (fu-088).
**30-Day Google (https://app.agencytitan.com/tasks/instance/20dbd773-c3f7-4df0-be4d-1dbe6b4e59b3), completed.** 09-27..10-26: $4,216.39 / 74 conv / $56.98 (prev $4,751.57 / 42 / $113.13). 72 of 74 = taps, 2 real calls (Branded 10-19, 10-20), 0 forms. Google rates no RSA assets yet (all 157 labels NOT_APPLICABLE). All 10 ads approved. The API returns no speed score. No structured snippets anywhere. The 3 callouts created 10-23 have no Heating impressions yet. Stalled primaries: CallRail uploads (First/Repeat/Phone Call/Form Capture), both form actions, Sign Up, Smart x4, Clicks to call, Local actions x4. Geo: 100% of PPC spend is in targeted locations. LSA spend came from Joshua / Fort Worth / Mansfield, so no exclusions are needed. Staged: structured snippet on Branded + Heating, form test incl. heating pages, demote dead primaries, Branded RSA rewrite. Toggles (UI): Extensions & Assets Updated = No, Geo Exclusions Added = No, Landing Page Issues Found = Yes (0 forms tracked in 30d), Session Recordings Audited = No, Blockers to Escalate = Yes (freed budget / AM, fu-088).
- **LSA 7-Day (https://app.agencytitan.com/tasks/instance/1fbd7310-764d-4086-a562-196f6fade7af), completed.** $108.16, 4 leads (3 calls, 1 msg), 2 charged → $27.04/lead, $54.08/charged. Prior week $0 / 2 uncharged. 78 impressions, top impression rate 100%. Pacing 66% of 7 x $23.26 = On Pace. The 10-21 message lead (install_ac) is still NEW, so the AM needs to get it answered.
- **LSA 30-Day (https://app.agencytitan.com/tasks/instance/2e28ddf5-fb83-4dd1-b90d-fe090b1a485d), completed.** $283.39, 10 leads (9 calls, 1 msg), 4 charged → $70.85 per charged lead = true CPL (0 disputes, 0 credits). 4/10 BOOKED (40%). Impressions 197 vs 509 prior 30 (-61%). Budget use 41%, so reach is the limit, not budget. Staged: dispute review on the charged DECLINED 09-29 call (lead 342890473) before its window closes, and an LSA profile check in the UI (job types, area, reviews). KPI - LSA 457b534c (weekly + 30-day keys). Toggle (UI): Blockers to Escalate = No.

## 2026-11-02 — Heating Search first week (fu-095), read-only

Window 10-26..11-02 (live 10-26, first spend 10-27; 11-02 partial). Pull: `weekly_pull.py` + CallRail (cs-air, 26 calls).
- **TSD_10.23_Search_Nonbranded_Heating 24383234148:** $226.20, 24 clicks, CPC $9.43 (cap $12), 727 impr, **0 conversions, 0 ad calls** (call_view empty; CallRail: 0 calls on 817-442-6949, 0 website calls with a gclid). Spends its $30/d (~$32/d). IS 20%, lost 66% to rank, 14% to budget.
- **Where the money goes:** 'new heating system' PHRASE $102 (45%), 'heater service' $52, 'new furnace' $22, 'new heat pump' $20. Repair keywords barely serve (heating repair 13 impr, no heat 3, furnace not working 1 click). Only $56 of $226 of terms visible; those are product research: empire furnaces, heat pump, gas furnace, infinity 20 heat pump, what is a good heat pump, a c furnace. Impression-only terms: competitors (prime time heating and air, bock services, service champs, silver spur, burke mechanical, christmas ac, encore hvac, hat plumbing), model numbers (gc9s800603an, 59tp6c), brands/research (best hvac brands, goodman heat pump reviews, carrier furnace error codes, ao smith vortex), window/mobile-home/floor heating.
- **Rest of the account:** Branded $82.62, 10 clicks, IS 98%, 1 tap; LSA $65, 1 lead. CallRail 26 calls, 20 on the GBP number, rest website pool (organic/direct), none from Google Ads.
- **Read:** 24 clicks is too few to judge (1-2 leads would be normal), but the Replacement side buys research. Account total ~$55/d vs $238/d approved.

**Proposed (not applied, Edu's go):** phrase negatives on Heating for research/brand/competitor terms (what is, best, reviews, brands, error codes, window, mobile home, floor heating, empire, infinity, ao smith, prime time, bock, service champs, silver spur, burke, christmas, encore, hat plumbing); exact negatives for bare product lookups (heat pump, gas furnace, furnace, a c furnace, electric furnace, central heater, gas heating unit); keep the $12 cap and $30/d one more week. Spare budget (fu-091): heating can't take more until it books a lead; options left = LSA settings review or tell the AM spend runs ~$55-75/d.

## 2026-11-02 (later) — APPLIED: 26 heating negatives (Edu: "Apply the negatives and keep the cap where it is")
Script `cs_apply_1102_heating_negs.py` (guards passed, validated, applied, read back: 0 missing). Campaign negatives 73 → 99. Cap $12 + $30/d unchanged.
- 19 PHRASE: what is, best, reviews, brands, error codes, window, mobile home, floor heating, empire, infinity, ao smith, prime time, bock, service champs, silver spur, burke, christmas, encore, hat plumbing.
- 7 EXACT: heat pump, gas furnace, furnace, a c furnace, electric furnace, central heater, gas heating unit.
- 14-day replay: blocks $56 of $56 visible clicked spend (all 0 conv) + the impression-only research/competitor terms. Note 'mobile home' also blocks 'mobile home furnace replacement near me' (1 impr) — remove it if C&S services mobile homes.
Recheck with fu-091 on 11-09.

## 2026-11-02 (later 2) — LSA insurance PASSED + LSA budget $23.26 → $55/day (APPLIED, Edu: "It passed, can you do the budget increase?")
- Edu uploaded the valid COI (Drive 'Insurance' folder, GL 6D57934, 7/31/2026–7/31/2027) in the LSA dashboard. API: new INSURANCE artifact 2026-11-02 11:43 PASSED, customer insurance status PASSED. Review: `2026-11-02-lsa-review.md`.
- `cs_lsa_budget_1102.py` (guards: insurance PASSED, budget $23.26 unshared), validated, applied, read back $55.00/day (~$385/week, ~6 charged leads/week at $65).
- Budget approval: reallocation inside the $238/day approved total (PMax $110 + Cooling $25 paused 10-23). Account now ≈ Branded ~$27 + Heating $30 + LSA up to $55 ≈ $112/day max.
- Watch (fu-116 ~11-05, then fu-091 11-09): impressions back to 60–90/day, leads, booked rate. If reach recovers but $55 is fully used with good booked rate, step up again.

## 2026-11-02 (later 3) — Branded RSA 800192030388 descriptions rewritten (APPLIED, Edu: "Yes, go for it")
- Found: 'Keep cool this summer!' is NOT in Branded; it's text asset 332814404255 in the two PMax asset groups (new PMax paused, Feb PMax ended, $0), so nothing live shows it. Swap it only if PMax relaunches.
- Branded RSA 800192030388 had weak descriptions instead. `cs_branded_rsa_desc_1102.py` (validated, applied, read back; headlines untouched, 8):
  - "1 Trusted Heating and AC Experts Mansfield, TX | C&S Air" → "Heating and AC repair, maintenance and installs in Mansfield and DFW. Call C&S Air."
  - "Reliable HVAC services in Mansfield, TX. Expert AC repair and maintenance. Call us today!" → "Furnace acting up? Our techs fix all makes and models. Upfront pricing, no surprises."
  - "Trust the experts at C&S Air Inc. for all your heating and cooling needs. 20+ years of exp" → "Family-owned and serving Mansfield for over 20 years. Licensed and insured HVAC team."
  - Kept: "Call our HVAC experts to set an appointment".
- Status after: ENABLED, REVIEW_IN_PROGRESS. RSA 816861066466 keeps serving meanwhile. Check approval tomorrow.

## 2026-11-06 — fu-116: LSA after insurance PASSED + $55/day (read-only, nothing changed)

- Insurance + license both **PASSED** (customer.local_services_settings, HVAC, geo 21176).
- **Impressions/day roughly tripled but are not back:** 10-23..11-01 avg ~5/day (1-12) → 11-02..11-05 **28 / 19 / 25 / 26** (pre-collapse 60-90). Ranking recovers slowly after verification.
- **$55/day unused:** spend $0 since 11-02. The 3 leads since then were all uncharged (11-02 BOOKED, 11-04 ACTIVE hvac_maintenance, 11-05 ACTIVE). Last charged lead 10-30 ($65, BOOKED).
- Since 10-20: 11 LSA leads, 4 DECLINED by C&S (free), 3 BOOKED (2 charged), 4 ACTIVE.
- No change needed. Read again with fu-091 on 11-09 (impressions trend, first charged leads at $55). If impressions stall under ~30/day, check LSA service area / job types / hours in the dashboard.

## 2026-11-09 — fu-091: second heating week, LSA after insurance, and where the spare budget can go (read-only, nothing changed)

`cs_recheck_1109.py` + CallRail (company 580688522, 10-27..11-09, 36 calls).

- **Account spend 11-03..11-08: $341.63 = ~$57/day vs $238/day approved**, so ~$180/day is unspent (~$5.4k/month). More than the "~$100" in the follow-up title, because LSA is at $0.
- **Heating 24383234148, week 2 (11-03..11-08, after the 26 negatives): $193.14 / 22 clicks / CPC $8.78 / 0 conversions / 0 ad calls.** Since launch (10-27..11-09): **$458.43 / 51 clicks / 0 leads** (Replacement $284.04 / 32 clicks, Repair $174.39 / 19 clicks). IS 15%, 62% lost to rank, 23% to budget; keywords QS 0–5. Clicked terms are still research: 'heat pump ratings by brand' $24.44 / 3 clicks, 'heating unit for house' $14.16 / 2, 'gas furnace attic' $8.09. Impression-only: troubleshooting questions, model numbers, error codes, boilers / geothermal / radiant.
- **CallRail:** 1 Google Ads call in 14 days (11-06 08:54, 297s, answered, repeat caller, from the Branded call asset). 0 website calls with a gclid. The other 35: Business Profile 27, website pool 8.
- **Branded:** 11-03..11-08 $148.49 / 14 clicks / CPC $10.61 / IS 94% / abs-top 81%; 1 tap + the 296s ad call. Target IS = top of page 95%, ceiling $15; 'c&s air' itself pays $12.77 a click. Search terms brand only. RSA 800192030388 (rewritten 11-02) APPROVED, strength AVERAGE.
- **LSA:** insurance + license PASSED. Impressions/day 11-02..11-08: 28, 19, 25, 26, 17, 13, 6 = **19/day**, vs 7/day during the collapse (09-11..11-01) and 22/day before it (08-01..09-10, same campaign metric; the 60–90/day quoted in the 11-02 review does not match this metric). Reach is roughly back. **Spend $0 since 11-02:** 3 leads (11-02 BOOKED, 11-04 ACTIVE, 11-05 ACTIVE), none charged. Before the collapse LSA spent ~$26/day. Since 10-20: 11 leads, 4 DECLINED by C&S, 3 BOOKED, 4 ACTIVE.

**Read:** nothing live in Google can take the spare money. Branded is at 94–98% IS. LSA has its reach back but uses $0–26/day of its $55. Heating has no lead after 51 clicks, and nonbranded Search has now failed four times on this account (March, July, Cooling, Heating).

**Proposed (Edu's go, nothing applied):**
1. **AM note, owed since 10-23:** spend runs ~$57/day vs $238 approved, why (PMax 0 calls, Cooling 0 leads, both paused), what works (LSA booked jobs, brand), and what we propose for the rest.
2. **Heating:** pause the Replacement ad group (62% of the spend, research traffic). Keep Repair one more week at $15/day with extra negatives (ratings, by brand, why, how much, code, thermostat, boiler, geothermal, radiant, gas log, pilot light). Pause it too if still 0 leads on 11-16.
3. **Spare budget → brand awareness on Meta** (TSD doctrine; ~86% of C&S calls come through the Business Profile, i.e. people who already know the name). Local benchmark: Cool Hand's ARL campaign in Mansfield–Arlington–S Fort Worth, Sep 9–Oct 8, CPM $5.04, 35,423 reached. At that CPM about **$75/day** holds ~35k adults at 3x/week (rough, another client's CPM). Needs an ad account, Page access, a real pixel (GTM still has the 123456789 placeholder), creative, and the client's OK through the AM (fu-018).
4. **LSA:** keep $55/day. Ask the AM why C&S declines ~4 in 10 leads, and to mark the ACTIVE ones.
5. **Optional:** Branded ceiling $15 → $10 as a test (saves ~$5-10/day, does not absorb anything).

## 2026-11-09 (later) — "What else can bump results?" (Edu asked): lever hunt, read-only, nothing changed

Scratch pulls (not kept): LSA leads + conversations since 08-01, GA4 310229049 landing pages 10-27..11-09, Keyword Planner (Mansfield + Arlington + Fort Worth + Burleson), CallRail 10-27..11-09.

- **LSA lead handling is the biggest lever.** Since 08-01: 49 leads = **25 DECLINED (51%)**, 18 BOOKED, 6 ACTIVE. **11 of the declined were charged** (~$715 at $65) and none shows a credit (credit_state UNSPECIFIED). Many declined calls are long: 195s, 316s, 323s, 616s, 522s, 238s, 287s, 880s. By month: Aug 9 declined / 6 booked, Sep 12 / 6, Oct 4 / 5. Why they decline is unknown: recordings 09-15..11-09 pulled + transcribed locally (call-wins), read next.
- **Someone else's Facebook campaign is sending junk traffic.** GA4: `facebook / cpc`, campaign "promo", **790 sessions in 14 days** (761 users, all to the homepage), ~1 second average engagement. CallRail website pool in the same window: 8 calls, **0 from Facebook**, 0 from Google Ads (5 direct, 2 organic, 1 referral; plus 1 GBP-tagged). Not TSD's. Ask the AM who runs it and what it costs.
- **Paid clicks do reach the site.** Heating campaign: 48 GA4 sessions for 51 clicks. Visitors stay 31s on /heating-replacement (27 sessions) and 12s on /heating-repair (17). On those landings: 6 scroll events, 0 phone clicks, 0 forms. (candsair.com serves a "Confirm you are human" 403 page to my headless browser from Brazil, so I could not inspect the mobile page; GA4 shows US visitors get through. PageSpeed API quota was exhausted, speed not measured.)
- **Search can't be fixed with bids.** Keyword Planner top-of-page range in the 4 cities: 'ac repair near me' $31.78–100.63, 'hvac repair near me' $37.34–76.85, 'hvac company near me' $26.40–72.76, vs our $12 cap. Heating terms are small: furnace repair 480/month, furnace repair near me 320, heating repair 170, heater repair near me 170 (no bid data). Top of page would mean $30+ clicks and several hundred dollars a lead vs $65 on LSA.
- **Phones are answered:** CallRail 34 of 36 answered; 24 first-time callers in 14 days, 20 through the Business Profile, 4 through the website.
- **No current offer:** the site still shows the Lennox $1,600 rebate that ended 01/31/2026 (EOY offers sweep). Holiday-offer approvals are due 11-13 (fu-131).

## 2026-11-09 (later 2) — LSA declined leads: what the calls actually are (call-wins, 09-15..11-09, read-only)

`pull_lsa.py` + local transcription, 23 leads / 21 recordings. Detail in `lsa-call-wins-log.md` (section "Added 2026-11-09"). **This corrects the entry above:** the declined leads are not lost jobs.

- **"Declined" = the office marking calls that aren't a new job.** Of the 9 declined since 09-15: 2 job seekers, 1 C&S employee, 1 existing customer solved by phone, 1 reschedule, 2 calls from a contractor about warranty work on a past commercial job, 1 commercial prospect chasing a quote, 1 no-connection. No real residential job was turned away.
- **LSA brings almost no new customers.** In 8 weeks the new-customer leads are 10-05 (Joshua, price-shopping), 10-21 (message, install), 10-22 (Fort Worth, came by referral) and the 09-17 commercial prospect. About 12 of 23 leads are existing customers using the ad as the phone number (mostly free). Google's "Booked" count overstates ad-driven jobs: the charged "Booked" lead of 10-30 is a filter-size question.
- **Charged leads to dispute:** 09-29 (C&S employee, 287s) and 10-30 (filter-size question). The 9 declined + charged leads of 08-01..09-09 were not pulled.
- **Callbacks owed to commercial clients (for the AM, not an ads issue):** 09-17 proposal never sent; Midland warranty job, called 10-23 and again 10-29; hotel owner 11-05 with a room offline ~2 months.
- **Things C&S sells that an offer could use** (heard on the calls): $89 service-call trip charge, free replacement estimates, a $165/year membership with two visits.

**Read:** paid Search and LSA mostly catch people who already know C&S. New-customer volume from paid is close to zero, so the lever is new demand (an offer + awareness), not more bidding.

## 2026-11-09 (later 3) — APPLIED: Heating Replacement paused, Repair alone at $15/day + 26 negatives; AM note drafted in Agency Titan

Edu: "for Heating Search, do what you think is better" and "Write the task for Angela on AT but keep on draft".

**Pre-flight (10-27..11-09, read-only):**
- Replacement $284.04 / 32 clicks / 0 leads; 'new heating system' alone $172.43 / 20 clicks, QS 0.
- Repair $174.39 / 19 clicks / 0 leads: 'heater service' $108.50 / 12 clicks and 'heating service' $37.51 / 4 clicks (QS 5). The pure repair keywords (furnace repair, heating repair, heater repair, the near-me exacts) got 0–28 impressions and 0 clicks. Google shows only $20.77 / 2 of Repair's 19 clicks by search term.
- Repair by hour: 27% of spend 20:00–05:59 (5 clicks, mostly 20–23h), so no ad schedule added. Budget not shared.

**APPLIED ~11:25 CT (`cs_heating_trim_1109.py`, one atomic mutate, validate-only first, read-back OK):**
- Ad group Heating Replacement 198402775381 → PAUSED.
- Budget $30 → $15/day. $12 CPC cap unchanged. Heating Repair 196718543930 keeps running alone.
- 26 campaign PHRASE negatives (99 → 125): code, codes, pilot light, blinking · boiler, boilers, geothermal, radiant, gas log, gas logs, navien, dometic, heat and glo · ratings, rating, brand, how much, largest, biggest · service champions, varsity zone, bacon hvac, matco, reliant, southern air, willard.
- Left out on purpose: 'why' and 'thermostat' (both in the morning's proposal). They block "why is my heater not working" and "thermostat on but no heat", which are people with a broken heater, the one thing Repair is there to catch.

**Why one more week for Repair:** 19 clicks is too few to call (at a 10% call rate, 0 of 19 happens about 13% of the time). About 30 clicks by 11-16 makes it a fair read. **Decision 11-16 (fu-141): still 0 leads → pause the campaign.**

**Budget wording corrected:** the "$238/day approved" used in this log since 10-09 is the sum of the daily caps before the 10-23 pauses, not a figure the client approved. Agency Titan's client record shows an ads budget of **$5,500/month** (~$181/day). Spend now is ~$57/day ≈ $1,700/month. The AM note uses the $5,500/month figure.

**Agency Titan:** Internal Request DRAFT `9d3573c2` "Google Ads update: low spend, heating ads and what we need from the client" (https://app.agencytitan.com/tasks/instance/9d3573c2-1d16-4e70-a993-f73af2fd7112). Client C&S Air, department Account Management/Customer Success, Intake = Edu, Execution = Angela, Review & Close = Edu. Left in Intake: Edu reviews and clicks Submit Request (fu-139). Contents: spend vs budget, today's heating change, what the LSA calls show, then the asks: (1) a heating offer by 11-13, (2) who runs the Facebook 'promo' campaign, (3) OK for ~$75/day Meta awareness + Page / ad account access, (4) 2 LSA leads to dispute (09-29 08:42, 10-30 13:16) + mark Active leads, (5) 3 commercial callbacks, plus a Business Profile review push.


## 2026-11-13 — Client Strategy Review "Oct Review" (AT 03fff3a7, Gui's copy): Paid row WRITTEN with data thru 11-12

Cycle 10-17..11-15, call Mon 11-17 09:45 ET. Detail: `strategy-review-oct-2026.md`.
- KPI row **4387c0fc-8e6f-4079-92e8-fc8bf110511d** linked to the client: ad spend 2062.53 (Branded $570.40, Heating $520.01, PMax $684.55, Cooling $114.41, LSA $173.16), **16 qualified = Google 6 (5 Branded ad calls on 817-442-6949, all transcribed: 1 new + 4 existing, + 1 form 11-03) + LSA 10 of 12 (2 new + 8 existing)**, CPL 128.91 (Branded $95, LSA $17, PMax/Cooling/Heating $1,319 for 0), rec 5500 (keep approved). Two weak existing ones (10-20 solved by phone, 10-30 filter question) kept per the 11-12 rule; without them 14 / $147.32.
- Notes written to `additional_paid_ads_notes`. Stage NOT submitted. Twin fd5eb77f untouched. Top-up for 11-13..11-15 = fu-166 (11-16).
- 11-12 AM note 9d3573c2 was submitted by Edu with only 2 asks (heating offer, commercial callbacks); Meta and Facebook 'promo' asks dropped, so the review doesn't push them.

## 2026-11-03 — AT optimization tasks (Gui, via Claude)

Read-only, nothing applied, no budget changes. Edu worked the account himself on 11-02 (below), so this pass builds on that.

**Edu 11-02 (change_event):** 26 heating negatives (what is, best, reviews, brands, error codes, window, mobile home, floor heating, empire, infinity, ao smith, prime time, bock, service champs, silver spur, burke, christmas, encore, hat plumbing + exact heat pump, gas furnace, furnace, a c furnace, electric furnace, central heater, gas heating unit); LSA budget $23.26 -> $55/d; Branded RSA 800192030388 descriptions rewritten (heating copy, pending review).

**7-Day Google (https://app.agencytitan.com/tasks/instance/d256c944-ac30-47a1-8739-54e804b40218), completed, KPI 44e1a9cc (Health Poor).** 10-27..11-02 PPC: $335.74 / 35 clicks / 1 conv (Branded tap 10-29) / $335.74 CPL / $9.59 CPC (prior $617.95 / 7). 0 verified leads: call_view 0, CallRail 0 calls on 817-442-6949 and 0 pool calls from paid, forms untracked. Branded $94.89 / 9 clk / IS 97.6%, ~$13.60/d of $80. Search IS 20.2%. Live total ~$57/d vs $238/d plan (fu-088).
**Heating Search 24383234148, first read (10-26..11-02):** $240.85 / 756 impr / 26 clicks / 0 calls / 0 taps / 0 tracked forms; CPC $9.26, CTR 3.4%, IS 18.8% (rank-lost 57.8%, budget-lost 23.4%). 'new heating system' = $110.53 (46%), where most brand/model research matched. QS 3 on furnace repair / heat pump repair / heater not working / furnace replacement near me; QS 5 heating/heater service. 52% of spend 20:00-05:59. 20/26 clicks mobile. Fort Worth 45% of spend, Mansfield $0. Only $64.67 of spend visible by search term. Too early to call volume; blind on web leads until forms are tracked.
**14-Day Google (https://app.agencytitan.com/tasks/instance/0845bb08-5e39-47e2-ad4f-399f7809d70e), completed.** 10-20..11-02 PPC $953.69 / 193 clk / 8 conv (7 taps, 1 real Branded call 10-20). Branded CPCs $12-15 on own brand under Target IS ($15 ceiling); heating RSAs EXCELLENT; no audiences; recs open (81 heating keyword recs, partners, display, Max Conv, lead form asset). Checklist ticked except 'Update ads until good QS' (nothing changed).
**Staged, not applied:** heating phrase negatives matco, lynco, varsity zone, southern air, willard, reliant, gradient, mini split, pellet, pilot light, inducer; heating schedule 6:00-20:00; 'new heating system' pause/exact on 11-09 if still 0 leads; AM to confirm Watauga / NRH / Richland Hills are service area; Branded ceiling $15 -> $12 test; Branded neg 'products'; observation audiences; dismiss partners/display/Max Conv/keyword recs; tracking task (form test + CallRail swap on heating pages, Gui to create); tell AM the live total (fu-088). Toggles (UI, 14-day): High-CPC Keywords Reviewed = Yes, Keyword Warnings Reviewed = Yes, Keywords Paused or Fixed = No, Geo Targeting Adjusted = No, Audience added = No, Blockers to Escalate = Yes. 7-day toggles: Negatives Added = No, Ads Paused = No, Policy Issues = No, Tracking Firing = No (forms), Blockers to Escalate = Yes.
- **LSA 7-Day (https://app.agencytitan.com/tasks/instance/e60184e3-371d-4c7f-ac2c-ef46b91ecfd3), completed, KPI - LSA 1218649d.** $65.00 / 5 call leads / $13.00 per lead; 1 charged (10-30 BOOKED) = $65 per charged lead; 2 BOOKED, 1 ACTIVE, 2 DECLINED (uncharged). Prior $108.16 / 4 leads. Impr 59 (-24%), top impr 97.4%. Budget was $23.26/d all week (40% used = Underspending, reach-limited); Edu raised to $55/d 11-02, which won't spend by itself.

## 2026-11-10 — AT optimization tasks (Gui, via Claude)

Read-only, nothing applied. KPI rows 11-10: Google 247a568e (Poor), LSA be6c1448.

**Edu 11-09 (change_event, API):** heating Search 24383234148: ad group **Heating Replacement PAUSED** (Heating Repair only now), budget **$30 → $15/d**, 26 phrase negatives (code(s), pilot light, blinking, boiler(s), geothermal, radiant, gas log(s), navien, dometic, heat and glo, rating(s), brand, how much, largest, biggest, service champions, varsity zone, bacon hvac, matco, reliant, southern air, willard), so most of the 11-03 staged list is now applied.
**7-Day Google (https://app.agencytitan.com/tasks/instance/7e1587a6-4481-4707-bd19-dce350a58ecd), completed.** 11-03..11-09 PPC $392.53 / 41 clk / 1 conv (Branded tap) / CPL $392.53 / CPC $9.57 (prior $335.74 / 35 / 1). Branded $174.95 / 16 clk / IS 94.3%, call_view 1 call 60s+, and 1 '[TSD] Submit lead form' (secondary): first tracked web form, check whether it was real. Heating $217.58 / 25 clk / 0 conv / CPC $8.70 / IS 14.6% (rank-lost 60.6%, budget-lost 24.8%); 2 weeks = $458 / 51 clk / 0 leads. Night spend 12% (was 52%). Waste: 'heat pump ratings by brand' $24.44 (now blocked by 'ratings'), 'heating unit for house' $14.16, 'heat and cool near me' $11.08, 'a and c air conditioning' $9.69, 'gas furnace attic' $8.09. Live: Branded ~$25/d actual, heating $15, LSA $0 vs $238/d plan (fu-088).
**Staged, not applied:** judge heating after 7 days on Repair only; negs 'a and c', 'unit for house'; schedule 6:00-20:00; tracking task (form test + CallRail on heating pages, Gui to create); AM: live total (fu-088) + who runs the Facebook ads. Toggles (UI): Tracking Firing = No, Blockers To Escalate = Yes.
- **LSA 7-Day (https://app.agencytitan.com/tasks/instance/e6656e7a-b188-44e3-886b-0ec2356b8890), completed.** $0.00 (prior $65), 2 call leads, neither charged (11-04, 11-05), impr 137 (prior 59), top impr 90.8%. $55/d budget (Edu 11-02) = 0% used: volume-limited, not budget. 30d $173.16 / 13 leads / 4 BOOKED. Still the old LSA campaign type.

## 2026-11-17 — AT optimization tasks (Gui, via Claude)

Read-only, nothing applied, no budget changes. KPI rows 11-17: Google fc42a7f9 (Poor), LSA 046eab19, Meta 16f6c6ed.

**Edu 11-16 07:50 (change_event):** Heating Search 24383234148 PAUSED (fu-141 decision). Live now = Branded + LSA only.
**7-Day Google (https://app.agencytitan.com/tasks/instance/edb975af-781a-4a04-92ff-cb586d5105bf), completed.** 11-10..11-16 PPC $226.99 / 26 clk / 1 conv / CPL $226.99 / CPC $8.73 (prior $392.53 / 41 / 1). The 1 conv = Branded 'Calls from ads' 11-11 205s, existing customer booking maintenance (counts). Branded $98.70 / 9 clk / IS 89.7%, ~$14/d of $80. Heating $128.29 / 17 clk / 0 conv, clicks were DIY troubleshooting ('my heat pump fan is not spinning', 'troubleshooting my furnace'...). Heating lifetime 10-26..11-16 = $586.72 / 68 clk / 0 leads. Search IS 14.5% (weighted).
**14-Day Google (https://app.agencytitan.com/tasks/instance/f94f542e-5d51-4345-ae67-e3571aa88ec1), completed.** 11-03..11-16 $619.52 / 67 clk / 2 conv (1 tap, 1 ad call) vs $953.69 / 193 / 8. Both Branded ad calls (11-06, 11-11) = existing customers. All spend in targeted locations; 13% at night; no audiences; Branded RSA 800192030388 AVERAGE vs 816861066466 GOOD. Open recs: 83 keyword + Max Conv on paused heating, search partners, lead form assets. Checklist ticked except 'Update ads until good QS'.
- **LSA 7-Day (https://app.agencytitan.com/tasks/instance/92984695-f167-4cb2-aad8-cafdd06a8b33), completed.** $219.28, all on 11-15: 2 leads (1 message duct cleaning NEW, 1 call duct repair ACTIVE), both charged = **$109.64 per charged lead** (was $65 on 10-30). Impr 185 (prior 137), top impr 98.1%. $55/d = 57% used (Underspending, volume-limited). 30d $392.44 / 14 leads / 5 charged = $78.49 per charged lead. Still old LSA campaign type. Lead rating not done (fu-161): rate the two 11-15 leads.
**Staged, not applied:** Branded phrase neg 'products' ('c&s air products' $7.68); keep heating paused (no new NB build); add 2-3 headlines to Branded RSA 800192030388; dismiss heating keyword / Max Conv / partners / lead form recs; watch LSA cost per charged lead (flag to Edu if > ~$100 again); spare budget vs $5,500/mo = Edu's call (strategy review 11-17).
**Toggles for Gui (UI):** 7-Day Google: Negatives Added = No, Ads Paused = No, Policy Issues Found = No, Tracking Firing = Yes (ad call recorded), Blockers To Escalate = Yes (spend far under budget). 14-Day: High-CPC Keywords Reviewed = Yes, Keyword Warnings Reviewed = Yes, Keywords Paused or Fixed = No, Geo Targeting Adjusted = No, Audience added = No, Blockers to Escalate = Yes. LSA: Blockers To Escalate = No.

## 2026-11-24 — AT tasks (Gui, via Claude)

Read-only, nothing applied, no budget changes. KPI rows 11-24: Google 9cf2e014 (Mixed), LSA eebfe118, Meta 18dd60c9 ($0 N/A). Only change since last pass: Edu's 11-16 07:50 Heating Search pause.

**7-Day Google (https://app.agencytitan.com/tasks/instance/0969105b-6967-4e7e-8f7e-484bd563027e), completed.** 11-17..11-23 PPC (Branded only) $349.52 / 31 clk / 2 conv / CPL $174.76 / CPC $11.27 (prior $226.99 / 26 / 1). Branded IS 98.2%, QS 8-10, 212 impr (prior 66). 11-18 Lennox app glitch = 131 impr / 12 clk / $125.79 of it; the 11-18 tap + 16:11 (58s) and 16:17 (26s) ad calls sit in the glitch window. Realistic real leads = 1 (11-17 07:28 132s ad call, not transcribed: CallRail API 429). No impressions 11-21/22. All search terms brand variants.
- **LSA 7-Day (https://app.agencytitan.com/tasks/instance/bc377ab7-d73b-4408-97ac-53778b02805c), completed.** $821.83 / 12 charged (11 calls + 1 message) = $68.49 (prior $219.28 / 2). 11-18 glitch day = $455 (7 charged at $65, rated 11-20: 6 credit PENDING, 353050671 no credit state). Net of 11-18 = $366.83 / 5 charged, 95% of $385/wk. Impr 1,384, top impr 99.5%. Charged non-glitch: 11-19 09:23 146s (credit PENDING, not rated by TSD), 11-19 17:33 300s, 11-23 13:48 66s, 11-23 15:31 46s duct cleaning, 11-23 17:30 message maintenance; not listened to. 30d $1,106.11 / 15 charged = $73.74. Still old LSA campaign type.
- **Meta 7-Day (https://app.agencytitan.com/tasks/instance/337fe8be-4ed5-4e79-bb0b-22e0d31f0f42), completed as N/A** (no C&S Meta account on either page of accessible accounts).
**Staged, not applied:** Branded phrase neg 'products' (still open from 11-17); rate 11-15/11-19/11-23 LSA leads after listening (fu-161); check the 7 glitch credits + 353050671 next pass; spare budget vs $5,500/mo = Edu's call.
**Toggles for Gui (UI):** 7-Day Google: Negatives Added = No, Ads Paused = No, Policy Issues Found = No, Tracking Firing = Yes, Blockers To Escalate = Yes. LSA: Blockers To Escalate = No. Meta: Blockers to Escalate = Yes if Edu wants the recurring task switched off.
