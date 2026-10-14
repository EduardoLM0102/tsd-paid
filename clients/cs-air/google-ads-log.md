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
