# Gillespie's Heating and Cooling — Google Ads log

CID `7410489772`. Brooksville, KY (Northern KY / Cincinnati OH metro). Site: gillespieheatingcooling.com.

---

## 2026-08-18 — Stage 1/2 audit: account is a blank slate, no conversion tracking exists

**Why.** Edu asked to launch this client's Google Ads. No client folder, `contas.yaml` entry, or AT-equivalent intake existed in this workspace — first touch on this account.

**Access.** Confirmed via TSD MCC (4155514468, `tsd.sh`/`.env.topserv`). Account `status = ENABLED`, `currency = USD`, `time_zone = America/New_York` (consistent with the KY/OH location once confirmed — multiple businesses nationally share the "Gillespie's HVAC" name, Edu confirmed this is the Brooksville KY one).

**Account inventory — effectively empty:**
- **One campaign total**, all statuses: the system-generated Local Services (LSA) campaign (`23940351598`), ENABLED, 7 clicks / 70 impressions / $0 cost lifetime so far. No Search/PPC campaign has ever been built here.
- **Zero extensions**, **zero negative keywords**, no shared negative lists.
- **Conversion actions: only the two LSA-native ones** (`local_services_phone_lead`, `local_services_message_lead`), both `MANY_PER_CLICK`, `category = PHONE_CALL_LEAD` / `UNKNOWN`. **No website form action, no call-tracking (CallRail/ServiceTitan) action, nothing biddable for a Search campaign exists in this account.**
- **No GA4 property linked** — checked `ga4.py properties` under the TSD login, no "Gillespie" property exists.

**This means Stage 3 (Conversion Tracking + End-to-End Lead Flow Test) of the Google Ads Launch SOP is not just incomplete — it hasn't started.** There is currently nothing for a Search campaign to optimize toward. Per the SOP this is a hard gate: no campaign build proceeds past Stage 4 until a real lead action (call or form) is proven to land in the client's CRM and shows up as the biddable Primary action in Ads.

**Site recon (gillespieheatingcooling.com), pulled directly since no Stage 1 brief exists:**
- **Services:** AC repair/install/replacement/tune-ups, furnace repair/install/replacement, boiler repair, heat pump install/repair, mini-split/ductless, commercial HVAC (rooftop units), indoor air quality (purifiers/humidifiers/filtration), 24/7 emergency HVAC.
- **Service-specific pages exist** (good — not a homepage-only site): `/air-conditioning/ac-repair/`, `/heating/furnace-repair/`, `/heating/boiler-repair/`, `/heating/heat-pump-installation/`, `/indoor-air-quality/`, `/commercial/`, `/emergency-hvac/`.
- **Cities served:** Newport, Florence, Covington, Alexandria, Erlanger, Maysville, Cynthiana, Fort Mitchell, Flemingsburg, Brooksville KY, and Cincinnati OH.
- **Phone:** (859) 445-6500. **Hours as published: "Mon–Fri 8am–5pm · 24/7 Emergency Line."** Flagging this exactly like the Cool Hand Electric precedent — a published "24/7" claim is not the same as a human actually answering nights/weekends; needs Edu/AM confirmation before it becomes the ad schedule, since ad-schedule restrictions (not bid modifiers) are the only lever that works under smart bidding.
- **Real offers on-site (usable verbatim):** "Free Estimates" / no-obligation quote, "Preferred financing" available, "Response within 1 business hour," "Upfront honest pricing — no hidden fees," 2-yr warranty as a Day & Night Elite Dealer.
- **Credentials:** Licensed & Insured in KY & OH, NATE-Certified, Family-Owned, 5.0★ Google rating. No years-in-business figure published.
- **No competitors named**, no consolidated "Areas We Service" page (location pages exist for Florence KY and Cincinnati OH only, but city list above comes from broader site copy).

**Open — blocking a real build/launch, not derivable from the site:**
1. **Approved monthly budget, in writing.** Hard rule, no exceptions — cannot size a single campaign budget without it.
2. **Conversion tracking path.** Does this client have CallRail, ServiceTitan, or GHL anywhere already (even unconnected to Ads), or are we starting from zero on call tracking? This decides whether Stage 3 is a quick hookup or a build-from-scratch.
3. **Primary lead type** to optimize toward: calls or form fills.
4. **Real phone-answering hours** — is "24/7 Emergency Line" an actual human, an answering service, or voicemail-to-callback? Decides the ad schedule.
5. **Service priority order** — which of the 7 service lines get ad groups first, and any the client does NOT want leads for (e.g. commercial, boiler).
6. **Local competitors by name**, if known — for the negative list.
7. **Lead capacity** — how many jobs/week can they actually take.

**Nothing built yet as of this entry.** See the 2026-08-18 build entry below — Edu gave the budget ($80/day each) and primary lead type (form fills) directly and is handling Stage 3 tracking in parallel, so the campaigns below were built to close out Stage 7 while that's in flight.

---

## 2026-08-18 — Branded + Non-Branded Search built (PAUSED), $80/day each

**Why.** Edu approved $80/day for branded and $80/day for non-branded, told me primary lead type = form fills, and is working conversion tracking (Stage 3) himself in parallel. Built per the Google Ads Launch SOP (`paid/sops/google-ads-launch-buildout.md`), Stage 7, everything PAUSED per Stage 7.9 #12 — nothing serves until tracking closes Stage 3 and QA (Stage 8) runs.

**Campaigns:**

| Campaign | ID | Budget | Bidding |
|---|---|---|---|
| TSD_08.18_Search_Branded_Evergreen | `24155673340` | $80/day | Manual CPC, per-keyword ceiling |
| TSD_08.18_Search_NonBranded_Evergreen | `24155674204` | $80/day | Manual CPC, per-ad-group ceiling |

**Bidding call:** the SOP's "launch on Maximize Clicks with a CPC ceiling" doesn't map cleanly onto this SDK — `create.py campaign` only exposes `target_cpa` / `maximize_conversions` / manual CPC (no true Target Spend), and `maximize_conversions` needs a conversion action to optimize toward, which this account doesn't have yet (Stage 3 still open). Used the documented workspace fallback (`aprendizados.md`): Manual CPC, enhanced CPC off, with a hard per-keyword/ad-group bid ceiling — functionally the same "never pay more than X" guardrail Max Clicks would give. **Once Edu's tracking work lands a real form-fill conversion action and it's verified biddable, migrate both campaigns to Maximize Conversions** (no target on branded; add a tCPA on non-branded only once there's real CPL data, per SOP 7.3/Stage 11 — never set from a guess).

**Geo:** 11 cities from the real site copy — Newport, Florence, Covington, Alexandria, Erlanger, Maysville, Cynthiana, Fort Mitchell, Flemingsburg, Brooksville KY + Cincinnati OH — added as city-level LOCATION criteria on both campaigns (site has no consolidated "Areas We Service" page, only 2 dedicated location pages, so pulled the full city list from body copy instead). `geo_target_type_setting.positive_geo_target_type = PRESENCE` set on both (presence-only, not presence-or-interest) via direct mutate since `create.py`/`update.py` don't expose it. English language criterion added the same way.

**Ad schedule:** left unrestricted (24/7 serving), by exception to SOP 7.5's normal "no default" rule. Reasoning: the schedule-restriction doctrine exists because *calls* bought at unattended hours can't convert — but the primary action here is **form fills**, which don't need a live pickup to be workable next business day. Site claims "24/7 Emergency Line" but real human-answering hours are still unconfirmed (same open item as Cool Hand Electric). **If Edu decides forms should also be schedule-restricted, or confirms real hours, this needs a follow-up campaign edit** — flagging, not deciding silently.

**Ad groups + keywords (PHRASE/EXACT only, no broad), themed to real landing pages found via the site's actual sitemap (`page-sitemap.xml`):**

| Ad group | Campaign | Keywords | CPC ceiling | Final URL |
|---|---|---|---|---|
| AC-Repair-Install | NonBranded | 10 | $15.00 | `/air-conditioning/ac-repair/` |
| Furnace-Heating-Repair | NonBranded | 9 | $16.00 | `/heating/furnace-repair/` |
| Heat-Pump-Services | NonBranded | 8 | $12.00 | `/heating/heat-pump-installation/` |
| HVAC-General-Company | NonBranded | 8 | $18.00 | `/` (mixed-intent catch-all, no single matching service page) |
| Brand-Terms | Branded | 8 (all EXACT) | $8.00 | `/` |

CPC ceilings sized off real Keyword Planner data pulled for this ad group's core terms in the Cincinnati DMA (200515) — e.g. furnace repair low-end top-of-page bid $12.58, "hvac repair near me" (HIGH competition) $9.19–79.41. Full keyword lists and researched volumes are in the build scripts, not duplicated here.

**Deliberately deferred, not built:** Boiler Repair, Commercial HVAC, and Indoor Air Quality ad groups — all three have real landing pages but thin Keyword Planner volume (30–140/mo at the full DMA level, so real local volume is smaller still) and would have thinned the $80/day non-branded budget further. Also skipped a dedicated Emergency/24-7 ad group and any "emergency"/"24/7" claims in ad copy, same call as Cool Hand Electric, given the unconfirmed answering-hours conflict above.

**Negatives (34 total on non-branded, campaign-level):**
- **Cross-negatives:** all 8 branded terms, EXACT, so brand queries route to the branded campaign.
- **Base list:** `plumbing/plumber/electrician/electrical/roofing/roofer/job/jobs/career/careers/hiring/employment` (BROAD, off-service + hiring intent), `diy/how to/wiring diagram/capacitor/manual/salary/used hvac/craigslist/home depot/lowes/hvac school/hvac certification/warranty claim/recall lawsuit` (PHRASE).
- **Deliberately did NOT negative** `free`/`cheap` (their real offer is "Free Estimates" — blocking it would block their own value prop) or bare `warranty`/`recall` (catches legit "does my unit have a warranty" queries; only the lawsuit/claim-fraud phrasing is blocked). Same over-negation trap the SOP calls out explicitly.
- No competitor names in the list — none were given and none are named on the client's own site. **Open item for Edu:** any local competitors to negative by name.

**Ad copy:** 15/12 headlines + 4 descriptions per RSA (branded capped at 12 — ran out of distinct real claims rather than pad with filler), built only from verified facts (site fetch + `page-sitemap.xml`): Free Estimates, financing, "response within 1 business hour," no-hidden-fees/upfront pricing, 2-yr warranty, Licensed & Insured (KY & OH), NATE-Certified, Family-Owned, 5.0★ Google rating, major brands carried. **First attempt included the phone number in ad text and was rejected by Google's `PHONE_NUMBER_IN_AD_TEXT` policy** (phone numbers belong in call assets, not headlines/descriptions) — fixed by replacing with "Get A Free Estimate" as the CTA.

**Extensions:** 8 callouts + 4 sitelinks (Commercial HVAC, Indoor Air Quality, About Us, Contact Us), all from real pages/facts, linked to both campaigns.

**QA verified before closing this entry:** both campaigns PAUSED, budgets $80/day each, all 5 ad groups PAUSED, keyword counts match plan (35 non-branded + 8 branded = 43), all 5 RSAs PAUSED with correct final URLs and 4 descriptions each, 34 negatives confirmed on non-branded, 12 extension assets confirmed linked to both campaigns.

**Not done — blocks Stage 8 (QA) and Stage 9 (Launch), not Stage 7:**
1. **Stage 3 conversion tracking** — Edu working this now. Once a form-fill conversion action exists and is verified biddable, it needs to be confirmed as the campaigns' Primary goal (nothing to bind it to yet, so no conversion goal override was set on either campaign).
2. Real phone-answering hours, for the ad-schedule decision above.
3. Local competitor names, for the negative list.
4. Written monthly budget approval on file with the AM (Edu authorized the $80/$80 directly — per MasterOps this should still get a ticket for the record, same pattern as the All Heart / GC Home Service / Zen Air budget changes logged elsewhere in this workspace).
5. QA by someone other than the builder, per Stage 8's explicit requirement.

---

## 2026-08-18, same day — Launched

**Why.** Edu said the tracking work was done in a parallel session and asked to turn the campaigns on. Before flipping status, verified the Stage 3 gate directly rather than taking the claim alone:
- **Conversion action is real and biddable, not just cosmetic.** `TSD - Lead Form` (`7725242585`), type `WEBPAGE`, category `SUBMIT_LEAD_FORM`, `ONE_PER_CLICK`, `ENABLED`. Checked past the `primary_for_goal` trap (`aprendizados.md` — that field alone doesn't make something biddable): `customer_conversion_goal` for `SUBMIT_LEAD_FORM/WEBSITE` shows `biddable: true`, and both campaigns inherit it as `biddable: true` at the `campaign_conversion_goal` level with no override needed.
- **First check found the GTM snippet NOT on the live site** (checked via direct fetch of gillespieheatingcooling.com, no `GTM-` reference, no `googletagmanager.com` script). Flagged this to Edu before enabling anything — he confirmed it was installed and asked me to check again.
- **Re-verified after that:** snippet is now live on the page (both the `gtm.js` loader and the `ns.html` noscript iframe reference `GTM-WJVDZBVF`), and the container has an actual **published live version** (v5, "Restore Meta tags," 22 tags / 14 triggers) — not just edits sitting in an unpublished workspace. Also noticed mid-check that the working workspace had moved from 2 → 8 and a `diag-test` workspace (3) had been created, consistent with real, active work having happened in between my two checks.
- Did not get a screenshot of an actual end-to-end test lead (Stage 3.4's literal requirement) — proceeding on Edu's direct authorization plus the three independently-verified technical facts above, not on the claim alone.

**What was enabled, in order (campaign → ad groups → ads, per the skill's activation rule):**
- Both campaigns: `TSD_08.18_Search_Branded_Evergreen` (`24155673340`), `TSD_08.18_Search_NonBranded_Evergreen` (`24155674204`)
- All 5 ad groups: Brand-Terms, AC-Repair-Install, Furnace-Heating-Repair, Heat-Pump-Services, HVAC-General-Company
- All 5 RSAs

**Confirmed post-launch:** every object above reads back `ENABLED`. Ad policy `approval_status` isn't populated yet in either RSA — normal for ads seconds after going live, not yet a disapproval signal. **Follow-up within the next few hours: re-check `read.py ads` for actual policy approval** (not just status), since nothing here has been through Google's review yet.

**Open items carried forward, now that this is live (not paused):**
1. Real phone-answering hours — still unconfirmed, still relevant even with forms as primary (affects whether an ad-schedule restriction should be added later).
2. Written budget approval on file with the AM for this $80/$80 — Edu authorized directly, same pattern as other budget moves in this book that got an after-the-fact AM ticket.
3. **Stage 10 (3-day check) is now scheduled**, not optional: is it spending, lost to rank or budget, are conversions actually recording (watch this closely given today's tracking history), first search-term sweep on the non-branded campaign.
4. The stale Proud-Pops-specific GTM triggers noted in `gtm-log.md` (Instant Roof Quote, Schedule Online buttons, Book Now/Contact-Us link fragments that don't exist on this site) are still sitting in the live container. They're dead weight, not a correctness bug (they can't fire off buttons that don't exist), but worth cleaning up.

---

## 2026-08-18, same day — Budget cut to match the media plan ($1,100/mo)

**Why.** Edu flagged the original $80/day + $80/day ($4,864/mo combined) was above the media plan's approved number. Target: land on $1,100/mo total.

**Math:** $1,100 ÷ 30.4 = $36.18/day total. Split 10% branded / 90% non-branded — same ratio Cool Hand Electric's media plan used for its branded carve-out, and defensible here given brand search volume is tiny (~10/mo per Keyword Planner).

| Campaign | Old | New | New monthly |
|---|---|---|---|
| Branded | $80.00/day | **$3.62/day** | ~$110/mo |
| Non-branded | $80.00/day | **$32.57/day** | ~$990/mo |

Total: $36.19/day × 30.4 ≈ **$1,100.18/mo**.

---

## 2026-08-24 — Weekly snapshot + Search Partners/Display network fix

**Why.** Standard weekly PPC pull, first full read on the account since the 08-18 launch. Blended 7-day numbers looked fine on the surface (24 clicks, 2 conversions, $216.42 spend, $108.21 CPL) but didn't match the conversion action quality check.

**Found:** both campaigns had `network_settings.target_search_network = true` and `target_content_network = true` — this is the same `create.py` hardcoding bug already found and fixed on Zen Air and Cool Hand Electric earlier in the week (no opt-out flag existed at the time these were built). Breaking down Non-Branded's week by `segments.ad_network_type`:

| Network | Clicks | Impressions | Conversions | Cost |
|---|---|---|---|---|
| Search (real) | 12 | 258 | 1 | $190.25 |
| Search Partners | 11 | 41 | 0 | $25.05 |
| Display (Content) | 1 | 18 | 1 | $1.12 |

The Display "conversion" converted on the very first click for $1.12 — matches the bot/junk pattern we've seen on other accounts' Display leakage, not a real lead. So the honest picture for the week is closer to **1 real lead at ~$190 CPL**, not 2 at $108 blended. Branded campaign (`24155673340`) got zero impressions all week despite being enabled — flagged as an open item, not yet investigated (budget may be too thin at $3.62/day, or brand-term volume may just be that low).

**Fixed same day:** mutated both campaigns' `network_settings` to `target_search_network=False` / `target_content_network=False`, verified live via read-back (not just the mutation's success response). Script: `clients/gillespie-heating-cooling/fix_search_network.py`.

```
Verified: TSD_08.18_Search_Branded_Evergreen | target_search_network = False | target_content_network = False
Verified: TSD_08.18_Search_NonBranded_Evergreen | target_search_network = False | target_content_network = False
```

**Open items carried forward:**
1. Branded campaign zero impressions all week — investigate budget vs. brand-term volume.
2. Total impression share was ~10% account-level this week — track whether it recovers now that spend isn't leaking to Search Partners.
3. Meta account (`2014320269203822`) frequency at 2.65 over the same 7 days on a single always-on ad set — reinforces the standing awareness-layer-campaign recommendation for the next client call (see `meta-ads-log.md`).

**Flagging, not changing:** the non-branded ad group CPC ceilings (AC-Repair-Install $15, Furnace-Heating-Repair $16, Heat-Pump-Services $12, HVAC-General-Company $18) were sized for the original $80/day budget. Against $32.57/day split across 4 ad groups, one or two clicks on the pricier ad groups can now eat most of a day's non-branded budget, which could starve the other ad groups of impressions on a given day. Left as-is since only the budget was asked for — worth revisiting if the search-term sweep shows spend concentrating in one ad group instead of spreading across the four.

---

## 2026-09-11 — Backfill: non-branded budget confirmed at $65/day (not the logged $32.57/day)

**Why.** Pulling a full-lifecycle report (launch through 2026-09-10) for Edu, `read.py campaigns` showed the live non-branded budget at $65.00/day and branded at $1.00/day — not the $32.57/$3.62 split logged on 08-18. Daily spend in the trend data confirms the jump: ~$35/day through 08-31, then ~$65-85/day from 09-01 onward, consistent with a budget change effective right around Sept 1. No campaign edit for this appears earlier in this log.

**Resolved with Edu directly:** he authorized the increase. Backfilling here since the change itself wasn't logged at the time — non-branded is live at **$65.00/day (~$1,978/mo)**, branded at **$1.00/day (~$30/mo)**, total ~**$2,008/mo**, up from the $1,100/mo media-plan figure logged 08-18. **Written approval on file with the AM is still open** — same standing item as the original $80/$80 launch budget (see 08-18 entries above), now doubly relevant given the total moved further from the last number that got a paper trail.

**Impression share context:** lifetime average (08-18–09-10) is ~80% budget-lost on branded, ~76.5% budget-lost / ~15.6% rank-lost on non-branded. Despite the higher live budget, the account is still budget-constrained on both campaigns, not rank-constrained — worth watching whether delivery keeps climbing at the new budget level or plateaus, which would point at a rank/QS ceiling instead.

**Full-lifecycle numbers (08-18 to 09-10), network-clean:** 87 clicks, 1,696 impressions, real Search cost $1,132.99, real Search conversions 6 (the account-level "7" includes 1 junk Display conversion from before the 08-24 network fix, $1.12, converted on first click — same bot pattern as the Search Partners leak). Branded: 2 impressions, 0 clicks, 24 days live — still no real delivery. Client-facing full report built same day: `Gillespies-Heating-Cooling-Full-PPC-Report_2026-09-10.html`.

**Revised same day:** Edu asked to strip sentence-interruption em dashes from the PDF prose per [[tsd-client-facing-voice]] (5 instances, all cut/reworded, no numbers changed). Re-rendered and re-QA'd, delivered as `Gillespies - Full PPC Report.pdf`.

**Second deliverable, same day:** a separate combined Google + Meta version of this report was also built per Edu's request, kept as its own file so this PPC-only one stays untouched. Meta side (awareness campaign live, lead-gen campaign paused) is logged in `meta-ads-log.md`'s 2026-09-11 entry, not duplicated here. Delivered as `Gillespies-Heating-Cooling-Full-Report-Google-Meta_2026-09-10.html` / `Gillespies - Full Report (Google + Meta).pdf`.

---

## 2026-09-17 — Deep dive: last-7-day conversions flatlined to zero, root cause not isolated (needs GHL access)

**Why.** Edu asked for a deep dive into why performance has been poor the last 7 days and what to do about it.

**Headline finding — this is a tracking cliff, not a demand/delivery problem.** Last 7 days (account level): 31 clicks, 400 impressions, $496.14 spent, **0 conversions**, 9.99% search impression share — all on Non-Branded (`24155674204`); Branded (`24155673340`, still $1.00/day) got zero impressions again. Pulling the daily trend 08-25→09-16 shows the **last real conversion was 2026-09-08**. Every day since (09-09 through 09-16, 8 straight days) has normal clicks (4-5/day) and normal spend (~$65-80/day) — in-range with the prior 3 weeks — but zero conversions. Clean, sudden cutoff, not a gradual decline, and not explained by less traffic or less spend.

**Ruled out, with evidence:**
1. **Search Partners/Display leak** — the 08-24 fix is still holding; this week's non-branded traffic is 100% real `SEARCH` network, confirmed via `segments.ad_network_type` breakdown (31 clicks / 400 impressions / $496.14, all `SEARCH`).
2. **Conversion action itself** — `TSD - Lead Form` (`7725242585`) still `ENABLED`, `SUBMIT_LEAD_FORM`, `ONE_PER_CLICK`. Not touched.
3. **GTM container** (`GTM-WJVDZBVF`, account 6360204363, container 255120208) — checked the actual **live/published** version via the Tag Manager API (`versions().live()`, not just the workspace draft): it's version 5 ("Restore Meta tags"), and its fingerprint timestamp resolves to **2026-08-18** — unchanged since launch day. (Found unlogged intermediate versions 4 "Dedupe GHL listener" and 5 "Restore Meta tags" that happened same-day 08-18 but were never written up here — both superseded by what's live now, no impact.) Versions 6 and 7 also exist (20 tags each, 2 fewer than live's 22) but are **not published** — sitting as unpublished drafts, harmless. The live tag chain itself is intact: `05 | G.Ads - Lead` tag (id 75, `awct`, not paused) fires on triggers `cEvent - Lead` / `cEvent - Appointment Scheduled` (custom-event triggers matching dataLayer `_event == 'ghl_form_submit'` / `'Appointment Scheduled'`), with the real `conversionId`/`conversionLabel` (`zIcSCNmx1-McEPvcovRD`) still wired in. The GHL listener tag (`00 | cHTML - Listener`, id 46) that pushes `ghl_form_submit` to the dataLayer on a valid postMessage from `leadnurturemachine.com`/`leadconnectorhq.com`/`msgsndr.com` is also live and unpaused.
4. **Account-level Google Ads changes** — queried `change_event` for the last 14 days: only **2 events total**, both `ASSET / CREATE` on 2026-09-08 09:49am by `access@topservdigital.com` (`INTERNAL_TOOL`) — matches 5 new sitelink assets already in the account (Furnace Installation, Heat Pump Repair, Furnace Repair, AC Repair, AC Installation). Nothing touched budgets, keywords, ad groups, or the conversion action.
5. **Site/landing pages** — all 4 ad-group landing pages + `/contact/` return `200`, all carry the `GTM-WJVDZBVF` snippet. Rendered `/contact/` in headless Chromium (Playwright): the GHL lead form (`link.leadnurturemachine.com/widget/form/91xd7DrEGhXA2CyAODYM`, wrapped in what looks like a WordPress-theme lazy-load-on-scroll wrapper, `class="uc-tp-wrapper"`) does render after scrolling, and `window.__ghlFormListener` initializes correctly. Did **not** submit a real test lead — that would create a fake entry in the client's actual GHL inbox, not something to do without coordinating first.

**Found existing but unlogged diagnostic scripts dated 2026-09-08** (`gillespie_check_09_08.py`, `gillespie_30d_check.py`, `gillespie_conv_action_detail.py`, `gillespie_gtm_tag72.py`, `gillespie_is_check.py`) — someone was already investigating this exact account the same day the conversion cutoff happened, but no findings ever made it into this log. Re-ran all of them as part of this session; nothing in their output contradicts the above.

**Not resolved — the actual fork in the road, and I don't have the access to close it:** whether real leads are still landing in the client's GHL CRM since 09-09.
- **If leads ARE showing up in GHL but not registering as Ads conversions** → the break is in the postMessage handoff or the browser-side attribution (GHL widget script change, a consent/ITP issue, or an origin mismatch) — a tracking fix, not a media fix.
- **If NO leads are showing up in GHL at all since 09-09** → the funnel itself is broken (form/widget stopped accepting submissions, or a GHL-side automation/webhook problem) — a GHL/CRM issue, no amount of Ads work fixes it.
- **Next step, needs Edu or whoever holds the GHL login:** pull the GHL submissions log for the last 8 days, or run one supervised live test submission with GTM Preview mode open to watch whether the dataLayer event and gtag conversion ping actually fire. This is the Stage 3.4 end-to-end lead-flow test that was flagged as never done even at original launch (see 2026-08-18 entry above).

**Secondary, longer-running structural issues — not new this week, but compounding the account's overall weak performance, surfaced while pulling this data:**
1. **Branded campaign still functionally dead.** $1.00/day, zero impressions again this week — unresolved since first flagged 2026-08-24, now 3+ weeks running. `search_rank_lost_impression_share` reads 90% on branded even though it's really a budget-starvation issue at this level. Brand volume is tiny (~10/mo per Keyword Planner) — funding this properly (even $5-10/day) would cost almost nothing and should capture close to all of it.
2. **Quality Score / landing-page-experience drag.** Of the keywords Google has scored, all show `BELOW_AVERAGE` `post_click_quality_score` (landing page experience) and mostly `BELOW_AVERAGE` `search_predicted_ctr`: "new furnace cost" (QS 1), "ac repair"/"air conditioner repair"/"ac tune up" (QS 3, AC-Repair-Install ad group). This drags Ad Rank account-wide and likely contributes to the account's chronic ~10% impression share — worth an actual landing-page review, not just a budget lever.
3. **Budget concentration in the broadest, least-qualified ad group.** `HVAC-General-Company` ("hvac company," "hvac service") is eating roughly half of lifetime non-branded spend ($765 + $295 of ~$1,482 lifetime shown in the quality-score pull) at an $18 CPC ceiling — flagged as a risk on 08-24, never revisited. This week's search-terms report shows this ad group's phrase match pulling in a long tail of low-relevance 1-2-impression queries: competitor names ("howard heating and air harlan ky," "hubbard mechanical paris ky," "corcoran & harnist heating & air," "custom air danville ky," "fresh air hvac," "blue collar heating and air"), brand/parts lookups ("daikin hvac," "bryant hvac," "goodman daikin," part numbers), and DIY/informational queries ("how much does it cost to replace hvac," "average hvac costs"). None of this drove this week's cost (mostly $0.00, 1-2 impressions each) but it's negative-list debt worth clearing.
4. **Non-branded is 82.9% budget-lost / 10.2% rank-lost this week** (`search_budget_lost_impression_share` / `search_rank_lost_impression_share` on campaign `24155674204`) — consistent with the account's whole history (08-24 entry above logged ~76.5%/~15.6% lifetime), so not new, but confirms the $65/day budget is still the binding constraint on delivery, separate from the QS issue above.
5. **No GA4 property for this client is visible to the TSD login** (`ga4.py properties` still comes back with no "Gillespie" property, same gap flagged at the 2026-08-18 audit) — even though `G-V636WJ3PSD` is wired into the live GTM container as "real." Either it's owned under a Google account TSD doesn't have access to, or it needs re-confirming with Edu. Doesn't block Google Ads conversion tracking (that's independent of GA4) but blocks using GA4 as a second way to check whether `generate_lead` events are firing.

**Recommended order of operations, not yet executed:** (1) check GHL for leads since 09-09 — this is the fork that tells tracking-bug vs. funnel-actually-broken; (2) if tracking, run one supervised live test with GTM Preview open; (3) once conversions are trusted again, raise branded off $1/day, tackle the QS/landing-page issue on the scored keywords, rebalance budget out of HVAC-General-Company's broad terms, and add the competitor/DIY negatives above.

---

## 2026-09-17, same day — Fork resolved (funnel is broken, not tracking); root cause found (form buried below the fold); both campaigns PAUSED

**Why.** Continuation of the same-day deep dive above. Edu checked GHL directly: **confirmed zero real leads landing there since 09-09** — not a GHL-receiving-but-mishandling problem, nothing is being generated in the first place. That resolves the fork from the entry above: this is a funnel/site problem, not a Google Ads or GTM tracking problem.

**Root cause found.** Edu asked to verify whether the ads are actually landing on the homepage. Checked the live `final_urls` on all 5 RSAs directly (not what the 08-18 build doc says):

| Ad group | Live final URL |
|---|---|
| HVAC-General-Company (biggest spender — ~half of lifetime non-branded spend) | `/` (homepage) |
| Brand-Terms | `/` (homepage) |
| AC-Repair-Install | `/air-conditioning/ac-repair/` |
| Furnace-Heating-Repair | `/heating/furnace-repair/` |
| Heat-Pump-Services | `/heating/heat-pump-installation/` |

So it's not universally "goes to the homepage" — 3 of 5 ad groups do land on their matching service page. That turned out not to be the real problem.

**The actual problem:** simulated a true cold ad click (Playwright, mobile viewport 390×844, bare final URL, zero scroll, zero click — just load and wait) on both the homepage and the AC-repair page. The GHL lead-form widget (`link.leadnurturemachine.com/widget/form/91xd7DrEGhXA2CyAODYM`, wrapped in a WordPress lazy-load container, `class="uc-tp-wrapper"`) does inject into the DOM on its own after ~5 seconds — no scroll gesture needed, so the earlier "needs scroll to trigger" theory from this morning's entry was wrong. But it's positioned absurdly far down every page:

| Page | `#request-estimate` position | Full page height | Screens of scrolling (mobile, 1048px viewport) |
|---|---|---|---|
| Homepage | 5,653px | 15,517px | ~5.4 |
| AC-repair page (dedicated ad landing page) | 12,485px | 16,955px | ~11.9 |
| `/contact/` (where most on-page CTAs route) | 2,711px | 11,261px | ~2.6 |

A visitor landing on the AC-Repair-Install ad group's own dedicated landing page has to scroll through roughly **12 phone-screens** before the lead form even exists in the DOM. That's the real explanation for zero conversions — not a broken script, not a broken conversion action, not GHL. Nobody scrolls that far.

**Separate, still-open loose end:** there's a sticky/fixed header (`class="gs-hdr"`) with a click-to-call number (859-445-6500) visible immediately on every page without scrolling, wired to its own Ads conversion action (`Click to call`, id `7728360430`/`7725368783`, `AD_CALL`/`CLICK_TO_CALL`). That conversion action is also at zero for the last 7 days. Since there's no CallRail connected, GHL has no visibility into phone calls at all — Edu's "no leads in GHL" confirmation only speaks to the form channel. **Open question for Edu/AM to put to the client directly: has the phone actually been ringing?** If yes, that's a second independent tracking gap (click-to-call trigger not firing) separate from the landing-page problem. If no, it reinforces that this is a landing-page/UX failure across the board, not channel-specific.

**Action taken:** both Search campaigns PAUSED —`TSD_08.18_Search_NonBranded_Evergreen` (`24155674204`) and `TSD_08.18_Search_Branded_Evergreen` (`24155673340`) — verified via read-back (`status=PAUSED` on both). No point buying more clicks into a page nobody can convert on. LSA campaign (`23940351598`, system-generated, out of TSD PPC scope) left untouched — separate, near-zero-volume, not implicated in this problem.

**Task filed:** `tarefas.md`, Gillespie's section — pausing PPC to rebuild the landing page ASAP, target same-day (2026-09-17).

**Do not re-enable until:** (1) the form is moved high enough on the page that real paid traffic can actually reach it (or the on-page CTAs are changed to jump straight to it), (2) a real end-to-end test lead is confirmed landing in GHL, (3) the phone-ringing question above is answered.

---

## 2026-09-17, same day — Two new landing pages built, final URLs swapped on the two matching ad groups

**Why.** Edu had two new pages already built with tracking set up and tested: `/emergency-ac-repair/` and `/emergency-furnace-repair/`. Directly addresses the root cause above (form buried 6-12 screens down) with pages built to fix it.

**Verified before swapping** (didn't just take "tracking is tested" on faith for the one thing that actually matters here — form position): both return `200`, both carry the `GTM-WJVDZBVF` snippet. Headless mobile check (390×844 viewport, cold load, zero scroll): on `/emergency-ac-repair/` the form wrapper sits at **970px down** (~1.1 screens) and the `#request-estimate` anchor at 168px (first screen); on `/emergency-furnace-repair/` the form renders with `#request-estimate` at 178px (first screen, no separate `.uc-tp-wrapper` detected — likely a non-lazy embed on this page, but the iframe still renders). Both a massive improvement over the old pages' 5,653-12,485px. Click-to-call number also immediately visible (~103-114px) on both.

**Swapped final URLs** via `update.py ad --final-urls`, verified via read-back:

| Ad group | Old final URL | New final URL |
|---|---|---|
| AC-Repair-Install (ad `821307379177`) | `/air-conditioning/ac-repair/` | `/emergency-ac-repair/` |
| Furnace-Heating-Repair (ad `821380505447`) | `/heating/furnace-repair/` | `/emergency-furnace-repair/` |

**Not touched — no matching new page provided, flagging rather than guessing:**
- **HVAC-General-Company** (`/`) — the single biggest-spending ad group, still homepage. No "emergency general HVAC" page was given; forcing it onto either emergency-AC or emergency-furnace would mismatch the query intent (this ad group's top terms are generic "hvac company"/"hvac service," not AC- or furnace-specific).
- **Heat-Pump-Services** (`/heating/heat-pump-installation/`) — still the original service page, still deep on the site (not re-measured this session, but same page as before, no reason to assume it changed).
- **Brand-Terms** (`/`) — still homepage, normal for branded.

**Both campaigns remain PAUSED** from the entry above — this swap doesn't re-enable anything by itself. Still waiting on: confirmation of what (if anything) HVAC-General-Company and Heat-Pump-Services should point to, then a real end-to-end test lead through the new pages before flipping back on.

---

## 2026-09-17, same day — All remaining ad groups moved off the homepage (and off an even-worse page found in the process)

**Why.** Edu: "change them all, let's not use the homepage as of right now — since it's not working."

**Before moving anything, checked the two still-open ad groups' actual current pages** (same headless mobile check as the rest of this session):
- **Heat-Pump-Services** (`/heating/heat-pump-installation/`) — form at **14,888px down**, page total 19,476px. That's **~14.2 screens** on mobile — worse than every other page measured today, including the original homepage (5,653px) and the pre-fix AC-repair page (12,485px). This page's burial problem was never actually fixed by anything above; it just hadn't been re-checked yet.
- **`/contact/`** (re-checked) — no separate `.uc-tp-wrapper` match on this pass (the class drops once the real iframe swaps in, a timing/selector artifact, not a real change — the earlier same-session measurement of **2,711px down / 11,261px total, ~2.6 screens** stands as the real number). Still the best-positioned page in the account besides the two brand-new emergency pages.

**No dedicated "emergency" page exists for general/brand/heat-pump queries**, so routed all three remaining ad groups to `/contact/` as the stopgap — a real, verified improvement over both the homepage and the heat-pump page, even though at ~2.6 screens it's not as good as the two purpose-built emergency pages (~1 screen). Swapped via `update.py ad --final-urls`, verified via read-back:

| Ad group | Old final URL | New final URL |
|---|---|---|
| HVAC-General-Company | `/` (homepage) | `/contact/` |
| Heat-Pump-Services | `/heating/heat-pump-installation/` | `/contact/` |
| Brand-Terms | `/` (homepage) | `/contact/` |

**Current state, all 5 ad groups:**

| Ad group | Final URL |
|---|---|
| AC-Repair-Install | `/emergency-ac-repair/` |
| Furnace-Heating-Repair | `/emergency-furnace-repair/` |
| HVAC-General-Company | `/contact/` |
| Heat-Pump-Services | `/contact/` |
| Brand-Terms | `/contact/` |

No page in the account is worse than ~2.6 screens now. Both campaigns **remain PAUSED** — none of this re-enables spend by itself. Worth a longer-term follow-up once this is stable: a dedicated heat-pump emergency page (same treatment as the AC/furnace ones) would likely outperform routing that traffic through `/contact/`.

---

## 2026-09-17, same day — Final destination assignment: everyone onto the two emergency LPs except Brand-Terms

**Why.** Edu: send all ad groups to the new landing pages, except Brand-Terms which goes back to the homepage. Neither HVAC-General-Company (fully generic terms) nor Heat-Pump-Services (heat pumps do both heating and cooling, so no clean topical fit) maps to one new LP over the other by content alone — asked Edu directly rather than guess. Confirmed: HVAC-General → AC-repair LP, Heat-Pump-Services → Furnace-repair LP.

**Swapped, verified via read-back — final state, all 5 ad groups:**

| Ad group | Final URL |
|---|---|
| AC-Repair-Install | `/emergency-ac-repair/` |
| HVAC-General-Company | `/emergency-ac-repair/` |
| Furnace-Heating-Repair | `/emergency-furnace-repair/` |
| Heat-Pump-Services | `/emergency-furnace-repair/` |
| Brand-Terms | `/` (homepage — branded searchers already know the company, this one's intentional, not a leftover) |

`/contact/` is no longer used as a destination for anyone — it was only ever the stopgap for HVAC-General and Heat-Pump before this reassignment.

**Both campaigns remain PAUSED.** Everything is now pointed at a good page; the only remaining gate before re-enabling is a real end-to-end test lead landing in GHL through one of the new pages, per the standing condition set in the first pause entry above.

---

## 2026-09-17, same day — Both campaigns re-enabled

**Why.** Edu asked to turn both campaigns back on, now that all 5 ad groups point to verified, non-buried pages (see the two entries above). Confirmed ad groups (`HVAC-General-Company`, `Furnace-Heating-Repair`, `AC-Repair-Install`, `Heat-Pump-Services`, `Brand-Terms`) and all 5 ads were already `ENABLED` the whole time — only the campaign-level status had been paused, so no lower-level re-activation was needed.

**Enabled, verified via read-back:**

| Campaign | Status | Budget |
|---|---|---|
| `TSD_08.18_Search_NonBranded_Evergreen` (`24155674204`) | `ENABLED` | $65.00/day (unchanged) |
| `TSD_08.18_Search_Branded_Evergreen` (`24155673340`) | `ENABLED` | $1.00/day (unchanged) |

**Same-day summary for anyone picking this up cold:** account went from zero conversions since 09-08 (funnel confirmed dead, not a tracking issue) → both campaigns paused → root cause found (lead form buried 5-14 screens down depending on page) → two new pages built with the form near the top, tracking pre-verified → all 5 ad groups repointed to good pages (AC-Repair-Install + HVAC-General-Company → `/emergency-ac-repair/`; Furnace-Heating-Repair + Heat-Pump-Services → `/emergency-furnace-repair/`; Brand-Terms → homepage, intentional) → campaigns re-enabled same day, budgets untouched.

---

## 2026-09-18 — End-to-end test done; decision to hold Manual CPC for now

**End-to-end test.** Edu confirmed he ran the live end-to-end lead-flow test himself (through one of the new pages) on 09-17. **Outcome not stated to me** — he said the test was done, not that it succeeded — so this is logged as "test performed," not "fix confirmed." Next real confirmation should come from actual paid-traffic conversions accumulating post-relaunch, not just the one manual test.

**Bidding strategy question — should the account move off Manual CPC now that tracking is trusted again?** Recommended **no, not yet**. Reasoning:
1. **No trustworthy post-fix volume.** Lifetime real conversions pre-fix were ~6 over 24 days (~0.25/day), and that history doesn't carry over anyway since the destination pages changed completely on 09-17 — the account is starting a fresh read at zero real-world conversions on the new funnel.
2. **Don't stack two live variables.** Landing pages + re-enablement happened same-day (09-17). Handing bidding to an algorithm on top of that would make it impossible to tell whether any wobble is the page, the algorithm's learning phase, or both.
3. **Matches the plan already on file.** The 2026-08-18 build entry above flagged Manual CPC as a placeholder specifically until a trustworthy conversion action existed, with an explicit migration path: Maximize Conversions once verified biddable (no target on branded), Target CPA on non-branded only once real CPL data exists. Today's fix gets tracking to "verified biddable" but not yet to "real CPL data on the current funnel."
4. **Branded isn't a Smart Bidding candidate regardless** — $1.00/day won't generate enough volume for any bidding algorithm to act on; that's a budget question, not a strategy one.

**Plan, not yet executed:** hold Manual CPC on both campaigns for a couple of weeks post-relaunch, get a real conversion count (target 15-30+) and a trustworthy CPL on the new pages, then migrate non-branded to Maximize Conversions (no target) first, adding a Target CPA only once that CPL number is real. Branded stays Manual CPC until its budget/volume situation changes.

**Follow-up:** added a dated check-in to `tarefas.md` (Gillespie's section) to revisit this in ~2 weeks (~2026-10-01) once real post-relaunch conversion data exists.

**Open, not yet done:** a real end-to-end test lead hasn't been confirmed landing in GHL through either new page — worth doing in the next day or two rather than assuming the fix holds. Also still open: the click-to-call tracking question (conversion action showed zero for 7 days, unclear if the phone was actually ringing — see the fork-resolution entry above), and written AM ticket/approval trail for today's pause+resume (no budget changed, but the account went dark and back up same day on Edu's direct call).

---

## 2026-09-23 — Two dead-weight ad groups paused: AC-Repair-Install, Heat-Pump-Services

**Why.** Edu reviewed historical performance across the non-branded campaign's 4 ad groups and found these two barely converting while still pulling from the shared $65/day non-branded budget: **AC-Repair-Install 1 conversion**, **Heat-Pump-Services 0 conversions**, neither generating phone calls either. Diluting budget away from the two ad groups actually producing leads (HVAC-General-Company, Furnace-Heating-Repair) for no return.

**Action taken by Edu:** both ad groups set to PAUSED. Confirmed via read-back (`read.py ad-groups`, non-branded campaign `24155674204`):

| Ad group | Status | Lifetime clicks | Lifetime conversions | Lifetime cost |
|---|---|---|---|---|
| AC-Repair-Install (`202443542394`) | **PAUSED** | 18 | 1 | $227.19 |
| Heat-Pump-Services (`197137071057`) | **PAUSED** | 7 | 0 | $83.71 |

Remaining ENABLED ad groups in the same campaign, for reference:

| Ad group | Status | Lifetime clicks | Lifetime conversions | Lifetime cost |
|---|---|---|---|---|
| HVAC-General-Company (`199263226493`) | ENABLED | 72 | 4 | $1,180.38 |
| Furnace-Heating-Repair (`199028708869`) | ENABLED | 19 | 0 | $294.93 |

Note Furnace-Heating-Repair also shows 0 lifetime conversions in this same pull — flagged, not paused, since Edu's instruction named only AC-Repair-Install and Heat-Pump-Services. Worth asking Edu whether Furnace-Heating-Repair should get the same treatment next review.

**Not changed:** campaign budget ($65/day non-branded) untouched — this is a reallocation within the existing budget toward the two ad groups still producing, not a budget change, so no AM-ticket approval is needed under the "total budget only" rule (see [[tsd-budget-approval-scope]]). Final URLs, keywords, and negatives on both paused ad groups left as-is in case they get reactivated later.

---

## 2026-09-26 — Snapshot + rebuild: two new campaigns on Maximize Conversions, live

**Why.** Edu asked to snapshot the live Google ads (headlines and descriptions) and recreate the two Search campaigns from scratch on Maximize Conversions, then publish and turn them live.

**State found before the rebuild (none of this was in the log):**
- Edu paused both Search campaigns himself on 2026-09-26 at 06:53 UTC (Google Ads web client). They had been re-enabled 09-17 and spent ~$65-80/day through 09-25.
- 2026-09-22, also Edu, via API: 5 phrase negatives added to Non-Branded (`cheap`, `quote`, `price`, `cost`, `how much`) and 2 keywords removed (one from AC-Repair-Install, one from Furnace-Heating-Repair). The rebuild carries the live post-edit lists.
- **Zero conversions since 09-08.** 09-09 to 09-26: $1,169.69, 73 clicks, 0 conversions. Since the 09-17 relaunch on the emergency pages: $602.77, 38 clicks, 0 conversions.
- **Lifetime conversions are 7:** Click to call 5 (button taps, `ONE_PER_CLICK`, no duration threshold), Calls from ads 1, TSD - Lead Form 1.

**Snapshot.** `google-ads-snapshot_2026-09-26.md` (RSAs verbatim, 41 keywords, 39 negatives, geo, assets, conversion setup) plus raw API output in `google-ads-snapshot_2026-09-26_raw/`.

**Built** with `rebuild_maxconv_2026-09-26.py` (state in `rebuild_maxconv_state.json`). Same structure as the old campaigns, Maximize Conversions with no target, Google Search only, PRESENCE geo, English, 11 cities, the same 12 campaign-level assets (4 sitelinks, 8 callouts):

| Campaign | ID | Budget |
|---|---|---|
| `TSD_09.26_Search_NonBranded_Evergreen` | `24297839425` | $65.00/day |
| `TSD_09.26_Search_Branded_Evergreen` | `24297891262` | $1.00/day |

Budgets equal the old campaigns' ($66/day combined), so the total account budget is unchanged. 5 ad groups, 41 keywords, 5 RSAs (headlines and descriptions diffed against the snapshot, all identical), 39 negatives on Non-Branded.

**Enabled:** both campaigns, plus HVAC-General-Company (`200605259677`), Furnace-Heating-Repair (`200440295933`), Brand-Terms (`199251996166`) and their RSAs. **AC-Repair-Install (`198894512565`) and Heat-Pump-Services (`201454645198`) were built but left PAUSED**, matching Edu's 09-23 pause of the originals. The old `TSD_08.18_*` campaigns stay PAUSED. Everything verified by GAQL read-back, not from the update.py output: both new campaigns `ENABLED`, primary status `LEARNING` (`BIDDING_STRATEGY_LEARNING`).

**Left as inherited, not decided:** both conversion goals (form fill and call) are biddable on the new campaigns, same as the old ones. With 5 of 7 lifetime conversions being Click to call taps, Maximize Conversions will mostly learn from taps until real form fills accumulate. Switching a campaign to form-only is a `campaign_conversion_goal.biddable` change.

**Open:**
1. Ads were `REVIEW_IN_PROGRESS` right after enabling. Same text was approved on the old campaigns, but re-check policy approval on `read.py ads`.
2. Written AM budget approval for the $65/$1 split is still open (unchanged from the 08-18 and 09-11 entries).
3. Branded at $1/day is unchanged and is still not a workable budget (2 impressions lifetime).
4. Ad claims to re-verify against the site: "Response Within 1 Hour" (site says "1 business hour"), "2-Yr No Hassle Warranty", and the "Trane, Carrier, Lennox" brand list.
5. The ~2026-10-01 check-in in `tarefas.md` (deciding when to leave Manual CPC) is now moot. Replace it with a review of the new campaigns' conversion volume.

---

## 2026-09-26, same day — Two paused ad groups removed from the new Non-Branded campaign

**Why.** Edu wanted only the two ad groups that were active in the old campaign (HVAC-General-Company, Furnace-Heating-Repair) in the new one. The other two, turned off 09-23, had been rebuilt paused in the entry above.

**Done.** Removed `AC-Repair-Install` (`198894512565`) and `Heat-Pump-Services` (`201454645198`) from `TSD_09.26_Search_NonBranded_Evergreen` with `delete.py ad-group` (`update.py --status REMOVED` is rejected by the API, use delete.py). Read-back confirms both `REMOVED`. The new Non-Branded campaign now has HVAC-General-Company (8 keywords) and Furnace-Heating-Repair (8 keywords), both with an enabled RSA. Brand-Terms on the new Branded campaign is unchanged. The old `TSD_08.18_*` ad groups, including the two paused ones (`202443542394`, `197137071057`), were not touched. Both new campaigns still `ENABLED` and in learning.

---

## 2026-09-26, same day — Geo targeting corrected: client service-area ZIPs added, Cincinnati OH removed

**Why.** Edu pasted the client's service area (37 ZIPs, 12 counties plus Brooksville, KY and OH) and asked whether the campaigns reach roughly the right area.

**Findings (old campaigns, same 11-city geo the rebuild copied):**
- Kentucky side roughly right: 7 of the 14 client ZIPs sit inside a targeted city, the other 7 are 3 to 14 miles from one. 7 of the 10 KY counties have a targeted city (Grant, Robertson, Lewis do not).
- **Ohio side missed entirely:** 0 of 23 client Ohio ZIPs covered (rural Brown/Adams County towns, 25 to 78 miles from Cincinnati). The only Ohio target was Cincinnati, and none of the client's ZIPs are Cincinnati city ZIPs (452xx).
- Actual spend by user location, 08-18 to 09-26 (`user_location_view`): **$1,268 of $2,207 (57%) and 90 of 152 clicks (59%) came from Cincinnati-area Ohio locations** (Cincinnati, Wyoming, Sharonville, Groesbeck, Lockland and similar), outside the client's list. Kentucky took the other 43%, mostly Kenton/Boone/Campbell suburbs. Brooksville/Bracken County got $0. No impressions came from the client's Ohio ZIP area.
- ZIP-to-city matching used a public ZIP lookup, county placement is from general knowledge, so treat the coverage counts as approximate.

**Changed (both `TSD_09.26_*` campaigns only):**
1. Added **33 Postal Code targets** (14 KY + 19 OH) via `add_zip_targeting_2026-09-26.py`.
2. Skipped 4 ZIPs, 45105, 45115, 45119, 45618: Google's geo table marks all four `REMOVAL_PLANNED`.
3. Removed **Cincinnati, OH (`1023626`)** with `delete.py location` (first attempt was blocked by the auto-mode classifier and ran after Edu allowed it).

Read-back: each new campaign has 43 locations (10 KY cities + 33 ZIPs), Cincinnati not targeted, PRESENCE setting unchanged. The old `TSD_08.18_*` campaigns (paused) still carry the original 11 cities.

**Open:** the client's site and the 08-18 recon list Cincinnati OH as a served city, but it is not in this service-area list. If the client wants the metro, add specific Hamilton County ZIPs rather than the whole city. Also: Grant, Robertson and Lewis counties have no ZIPs in the list and no city target, so they get nothing beyond the ZIPs supplied.

---

## 2026-09-28 — Weekly client report built (Sep 21-27)

**Why.** Edu asked for a 1-page weekly report, same format as the last one (Sep 11-17).

**Built.** `Gillespies-Heating-Cooling-Weekly-Update_2026-09-27.html` → `Gillespies - Weekly Report (Sep 21-27).pdf`, same structure and CSS as the 09-17 report (plain Times New Roman, no navy/gold, 1 page). Chrome is no longer on this Mac; rendered with Playwright's bundled Chromium instead of the documented headless-Chrome recipe.

**Content, verified against the live account (GAQL) and this log's own entries, not from memory:**
- Search-term negatives added 09-22 (cheap/quote/price/cost/how much) and the 2 keyword removals, framed as refining for booking-ready searches.
- AC-Repair-Install and Heat-Pump-Services ad groups paused 09-23, framed as concentrating budget on the two stronger-performing groups.
- The 09-26 Maximize Conversions rebuild, framed as the automated-bidding move flagged in the prior report. Confirmed both new campaigns are ENABLED, LEARNING, and their 3 live RSAs are now APPROVED/REVIEWED (open item from the 09-26 entries, now closed).
- The 09-26 geo correction (client-supplied ZIPs added, Cincinnati OH removed), framed as matching the client's real coverage. Cincinnati's removal surfaced as a client-facing question in "What's Next" rather than left silent.

**Deliberately left out, per [[topserv-client-report-format]]'s golden rule:** no performance numbers for the week. Sep 21-27 real numbers (pulled, not published): old Non-Branded ran through 09-26 (paused that morning), 21 clicks / 299 impr / $341.18, zero conversions the entire week, continuing the streak since 09-08. New Non-Branded's first day live (09-27) logged 13 impressions, 0 clicks, $0 spent. Branded had no activity either campaign. Matches the 09-17 report's own precedent of omitting weekly result numbers when there's nothing good to show, rather than the Aug-21 report's format, which did include a results bullet.

---

## 2026-10-01 — Check-in on the 09-26 rebuild (first 5 days live)

**Why.** Edu asked to check the account after the 09-26 changes. Read-only, nothing changed.

**New campaigns, 09-27 to 10-01 (10-01 partial):**

| | Impr | Clicks | Spend | Conv | Avg CPC |
|---|---|---|---|---|---|
| `TSD_09.26_Search_NonBranded_Evergreen` | 298 | 9 | $243.97 | 2 | $27.11 |
| `TSD_09.26_Search_Branded_Evergreen` | 1 | 1 | $1.99 | 0 | $1.99 |

Non-Branded by day: 09-27 13 impr / $0, 09-28 71 / 2 clicks / $13.53, 09-29 139 / 5 / $101.79 / 1 conv, 09-30 75 / 2 / $128.65 / 1 conv, 10-01 12 / 0 so far. Impression share went 21% → 26% → 38% → 64%, all of the lost share is rank (budget-lost 0%). Still `LEARNING` (`LEARNING_NEW`).

**Conversions, cross-checked in GA4 (property 541432580):**
1. 09-29, `TSD - Lead Form`: real form submit, GA4 `generate_lead` from google / cpc. Keyword `heating repair` (phrase), search term "gas fireplace service florence ky", $16.20 click, ZIP 41042 Florence. First form lead since the one before 09-08. Not confirmed the client services gas fireplaces.
2. 09-30, `Click to call`: a button tap (GA4 `phone_click` google / cpc), not a confirmed call. Keyword `hvac contractor` (phrase), **one click cost $116.03**, also ZIP 41042.

**Baseline for comparison:** old Non-Branded 09-09 to 09-26 was $1,169.69 / 73 clicks / 0 conversions, about $16 per click. The new campaign broke the conversion drought but paid ~70% more per click, and the $116 click alone is almost 2 days of budget. Max Conversions has no CPC ceiling at campaign level (`cpc_bid_ceiling_micros` is portfolio-only).

**Geo fix is working:** no Cincinnati OH traffic, 11 of the client's Ohio ZIPs got impressions (first time ever, 0 clicks yet). Non-ZIP impressions came from Alexandria, Covington, Erlanger, Maysville KY.

**Other:**
- 3 live RSAs `APPROVED`. Network Google Search only.
- Branded shows `primary_status MISCONFIGURED` (reasons `BIDDING_STRATEGY_LEARNING` + `UNKNOWN`) but `serving_status SERVING`; most likely the $1/day budget under Max Conversions. Got its first click ever.
- Search terms (impressions only, no clicks): competitor names (Adam, Folk and Sons, Chuck's, Doc Rusk, Tom Rechtin, Schaefer, Jefferson, Johnson, Logan, Peters, Titan, Airtron, P3 Mechanical), supply houses (Johnstone, Ferguson), equipment brands (Trane, Toshiba, Rheem), out-of-area towns (Newton NJ, Lexington, Georgetown, Morehead). Same pattern as the open negatives task in `tarefas.md`. 8 of the 9 clicks fall under hidden search terms.
- A system-generated LSA campaign (`23940351598`) exists in this account, ENABLED, 0 impressions all of September.

**Open:** let learning run (no bid changes this week). If another $50+ click shows up, move Non-Branded to a portfolio Max Conversions with a CPC ceiling. Add the negatives above. Click to call taps are still biddable and are half of this week's conversions.

---

## 2026-10-01, same day — 287 negatives added to the new Non-Branded campaign

**Why.** Edu asked to fix the competitor-name and junk searches flagged in the check-in above.

**Built from** every Non-Branded search term since launch (08-18 to 10-01, old and new campaign, 764 terms), not only this week's. Script: `add_negatives_2026-10-01.py` (validate-only by default, `--apply` for live). Campaign-level on `TSD_09.26_Search_NonBranded_Evergreen` (`24297839425`) only. Branded is exact brand terms, so it doesn't need them.

| Group | Match | Count | Examples |
|---|---|---|---|
| Local competitors | PHRASE | ~150 | geiler, knock knock, doc rusk, thomas and galbraith, reinhart, rechtin, chuck's heating, 333help, folk and sons |
| Supply houses, DIY, research | PHRASE | ~42 | johnstone, ferguson, habegger, re michel, supply, parts, store, btu, aciq, brands, manufacturers, for sale |
| Car / window / portable AC | PHRASE | 11 | car, auto, window ac, portable ac |
| Plurals of Edu's 09-22 negatives | PHRASE | 5 | prices, pricing, costs, quotes, cheapest (negatives don't match close variants) |
| Out-of-area places | PHRASE | ~25 | lexington, louisville, morehead, georgetown ky, dayton ohio, columbus, nj |
| Brand-only and "best system" research | EXACT | ~75 | carrier hvac system, trane hvac, goodman furnace, best hvac systems |

**Safety checks (in the script, run before the mutation):** none of the 287 blocks an active keyword, a search term that ever converted ("gas fireplace service florence ky", "hvac near me"), or the client's brand. Replaying the list against the 764 historical terms: it would have blocked 309 terms, 20 clicks, $305.43, 0 conversions. Eyeballed all 309, no false positives found.

**Deliberately left open:** commercial and boiler (client offers both), gas fireplace (the 09-29 form lead), financing/bad-credit searches (ads say "Financing Available"), brand + install/dealer/near me searches. In-area town names are not negated: union (41091), georgetown OH (45121), fayetteville OH (45118), winchester OH (45697), dayton KY (next to Newport), mason, butler, burlington, hillsboro, goshen, cincinnati (still an open client question). That is why the out-of-area list uses "georgetown ky" and "dayton ohio" instead of the bare names.

**Read-back (GAQL):** campaign has 326 keyword negatives (12 BROAD, 223 PHRASE, 91 EXACT = 39 old + 287 new), campaign still ENABLED. Negative-keyword changes don't reset Max Conversions learning.

**Not done, open questions for the client:** duct cleaning (many searches, unclear if offered), pellet stoves, water heaters, mobile homes.

---

## 2026-10-02 (found 10-05) — Both 09-26 campaigns paused, new Non-Branded removed

**Backfill.** Not logged when it happened; found in `change_event` during the 10-05 weekly check.
- 10-02 11:47:22 ET, `eduardo@topservdigital.com`, Google Ads web UI: `TSD_09.26_Search_NonBranded_Evergreen`
  (`24297839425`) ENABLED → PAUSED.
- 11:47:24: `TSD_09.26_Search_Branded_Evergreen` (`24297891262`) ENABLED → PAUSED.
- 11:47:32: `24297839425` PAUSED → **REMOVED**.

Old `TSD_08.18_*` campaigns stay PAUSED. Only the system LSA campaign `23940351598` is ENABLED (0 impressions). So no
Google Search is live for this client. **Reason for the pause isn't recorded anywhere, add it here.**

Last week before the pause (09-28 → 10-01): $346.84, 14 clicks, 2 conversions (1 real form lead 09-29, 1 Click to call
tap 09-30), $173.42 CPL, Search IS 39.0% (50.4% lost to rank).

## 2026-10-05 — Weekly 7-day check (Agency Titan task): nothing to optimize

**Read-only.** No Search campaign live (see above). AT task closed with a note; KPI - Google Search entry 10-05: $346.84,
2 leads, $173.42 CPL, Account Health "Poor".

