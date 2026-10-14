# Cool Hand Electric — Google Ads log

CID `9865206319`. See `internal-notes.md` for scope/hours/tracking context and `README.md` for the media plan.

---

## 2026-08-10 — 3 Search campaigns built (PAUSED), Electrical/HVAC/Branded

**Why.** Client approved $5,000/mo total budget. Requested 3 Search campaigns (Electrical, HVAC, Branded) with Electrical/HVAC split 60/40 — the only change from the Aug–Dec media plan, which otherwise didn't split Search by vertical.

**Budget math.** Plan's August ratio is 75% Search / 10% YouTube / 15% Meta (Peak AC Repair month). $5,000 × 75% = $3,750/mo Search (lead-gen) budget. Branded carved out at 10% of that ($375/mo) per Edu's call, remaining $3,375 split 60/40 Electrical/HVAC. Daily budgets use monthly ÷ 30.4:

| Campaign | Monthly | Daily | Campaign ID |
|---|---|---|---|
| TSD_Search_Electrical | $2,025 (60% of remainder) | $67/day | 24123995882 |
| TSD_Search_HVAC | $1,350 (40% of remainder) | $44/day | 24118511502 |
| TSD_Search_Branded | $375 (10% of Search pool) | $12/day | 24123995948 |

**Needs monthly revisiting** — plan's Search ratio shifts 65% (Sep) → 70% (Oct) → 75% (Nov) → 60% (Dec). Budgets above are sized to August only.

**Bidding:** Maximize Conversions, no target CPA (none client-approved; intake's CPA/conv-rate fields are blank). Non-shared budgets (required for Max Conv, per `aprendizados.md`).

**Geo targeting:** Client didn't have the intake's exact "6 cities + 9 zips" list on hand. Pulled the real, current list instead from the live site's own "Areas We Service" page: Burleson, Ennis, Fort Worth, Mansfield, Midlothian, Pantego, Red Oak, South Arlington, Waxahachie. Targeted at city level (8 geo-target IDs — Arlington used to cover both Pantego and South Arlington since neither is independently geo-targetable). Language: English. All 3 campaigns share this same geo set.

**Structure — 15 ad groups total, one RSA each, final URLs matched to real per-service landing pages found on the live site (not the homepage):**

*Electrical (8 ad groups):* Electrician-General, Panel-Upgrade, Generator-Installation, Ceiling-Fan-Installation, Circuit-Breaker-Repair, Outlet-Installation, Smoke-CO-Detector, Surge-Protection.

*HVAC (6 ad groups):* AC-Repair, AC-Installation, Furnace-Heating (generic hvac terms → homepage), Furnace-Repair, Furnace-Replacement, Heat-Pump-Repair.

*Branded (1 ad group):* Brand-Terms — "cool hand electric" has real search volume (~110–390/mo, trending down since Jan 2026 peak).

Two empty leftover ad groups from an early build pass — `Outlets-Fixtures` (Electrical) and `test-debug` (Electrical) — have no keywords/ads, won't serve, but weren't deletable via the skill's tooling (no ad-group delete command). Safe to remove manually in the UI.

**Cross-negatives** added so Electrical and HVAC campaigns don't compete against each other in auction (e.g. HVAC negatives out "electrician," "generator," etc.; Electrical negatives out "ac repair," "furnace," etc.). Both also negative plumbing/jobs/DIY terms (plumbing is explicitly out of scope per `internal-notes.md`).

**Ad copy constraints:** Confirmed via live site fetch — no "financing" or "same-day" language on site (didn't use), but did find a real "Easy Payment Plans" page, a work guarantee, "Licensed" and "Family Owned" claims, all used. Deliberately avoided "emergency"/"24/7" claims — the site itself says "Emergency Available" but `internal-notes.md` flags the Mon–Fri 8–5 hours conflict as unresolved; sided with the internal caution. **Edu should confirm this call** now that he has current hours (Mon–Fri 8–5, Sat 8–12, Sun closed).

**Conversion goals verified** (not just assumed — `primary_for_goal` alone doesn't make something biddable, per `aprendizados.md`): all 3 lead actions ([TSD] Contact Form, [TSD] Book Now Form, Click to call) map to biddable `customer_conversion_goal` rows (`SUBMIT_LEAD_FORM/WEBSITE` and `PHONE_CALL_LEAD/CALL_FROM_ADS`), and all 3 new campaigns correctly inherit both as biddable `campaign_conversion_goal` — no per-campaign override needed.

**Open item:** phone number discrepancy — live site's click-to-call link is `469-550-1102` (this is what GTM/conversion tracking is wired to), but Edu's contact info pull shows `469-874-0523`. Worth confirming which is current before using either elsewhere.

**Status: ACTIVATED same day (2026-08-10), Edu's explicit go-ahead.** All 3 campaigns, 15 ad groups, 15 ads → ENABLED, in that order. `serving_status = SERVING` confirmed on all 3 campaigns. The 2 empty leftover ad groups (`Outlets-Fixtures`, `test-debug`) were left PAUSED — no keywords/ads, can't serve.

---

## 2026-08-21 — First performance check-in (Ryan/AM ticket), client update built

**Why.** AM ticket: client asked how things are going, Ryan followed up. Deliverable:
`Cool-Hand-Electric-Performance-Update_2026-08-21.html/.pdf`, plain Times New Roman per
[[tsd-client-report-plain-design]]. Meta MCP queried directly (`ads_get_ad_accounts`, full
paginated list) to confirm — **no Cool Hand Electric ad account exists yet anywhere in the
accessible list.** This isn't just "creatives not delivered" as the ticket assumed — the Meta
account/pixel/campaign build itself hasn't started either, consistent with `internal-notes.md`'s
"tracking is a blank slate for the new channels" flag from the original media plan. Both facts
(brand awareness + Beat the Heat offer, designer finishing creative, launch targeted Monday
2026-08-24) came from Edu directly this session.

**Google Ads, Aug 10–20 (11 days live), pulled via `.env.topserv` profile (this CID is NOT under
the skill's default `.env` profile — needed `GADS_ENV_PATH=.env.topserv`, TSD's separate OAuth
profile per `tsd.sh`):**

| Campaign | Impr. | Clicks | CTR | Avg CPC | Spend | Conv. | Cost/Conv. | Impr. Share |
|---|---|---|---|---|---|---|---|---|
| TSD_Search_Electrical | 5,835 | 242 | 4.1% | $3.22 | $780.18 | 15 | $52.01 | ~10% |
| TSD_Search_HVAC | 4,915 | 238 | 4.8% | $2.14 | $510.19 | 21 | $24.29 | ~10% |
| TSD_Search_Branded | 694 | 56 | 8.1% | $2.43 | $135.93 | 5 | $27.19 | ~55% |
| **Total** | **11,444** | **536** | **4.7%** | **$2.66** | **$1,426.30** | **41** | **$34.79** | |

**Conversion composition (verified via segmented `conversion_action_name` query, not assumed):**
of the 41 standard "conversions," **40 are `Click to call`** (CALL_FROM_ADS tap-to-call, a click on
the ad's phone number — not a confirmed connected call) **and 1 is `[TSD] Contact Form`.**
`[TSD] Book Now Form` fired **zero** times across all 3 campaigns in the full 11-day window. Same
pattern flagged on [[tsd-gc-home-service]] and [[tsd-proud-pops-tracking]] — the headline number is
real ad-interaction volume, not verified booked jobs. Not alarming at 11 days in (this is exactly
what call-heavy electrical/HVAC intent looks like early), but don't let "41 conversions" get read
internally as 41 leads-in-CRM without this caveat.

**Cross-check via GA4** (property `549427279`, numeric ID — the `G-ZHH3FSDC4J` measurement ID does
NOT work as the API property identifier, use `ga4.py properties` to resolve it): same window shows
`book_now_lead` 3, `contact_form_lead` 2 (5 real on-site lead completions, independent of the Ads
click-to-call number), `phone_click` 51 (site tel: taps, separate signal from the ad-level
click-to-call), `book_now_widget_open` 56. Directionally consistent with the Ads data, gives a
second read on real engagement.

**Client copy deliberately left out** (per [[topserv-client-report-format]] scope-cut precedent):
LSA context (separate, TSD-excluded, do not blend into this deliverable's numbers), the click-to-call
vs. verified-booking distinction above, and the full Meta-account-doesn't-exist-yet detail — client
version says Meta "isn't live yet, account build and creative in progress," which is true and
sufficient without the granular gap list.

---

## 2026-08-24 — Weekly PPC check-in surfaces Search Partners/Display leak, fixed same session

**Why.** Routine weekly snapshot (spend/CPL/CPC/leads/conv rate + branded vs. unbranded + total IS),
LSA excluded per scope. Ran the network trust check from `tsd-weekly-ppc-snapshot` on top of the
usual pull — this account turned out to be one of the 11 in today's book-wide audit still affected
by the `create.py` bug (`target_search_network=True` hardcoded, no opt-out) plus manually-set
`target_content_network=True` on all 3 campaigns (Display never had an opt-out at all — implies UI
wizard edit at some point, same pattern as the other affected accounts).

**Last 7 days, PPC only (LSA excluded):**

| | Clicks | Conv. | Cost | CPL | Impr. Share |
|---|---|---|---|---|---|
| Branded | 53 | 6 | $80.48 | $13.41 | 57.3% |
| Nonbranded (Electrical+HVAC) | 348 | 37 | $694.00 | $18.76 | ~10.0% |
| **Total** | **401** | **43** | **$774.48** | **$18.01** | |

Nonbranded impression share loss is now split ~40% budget / ~57% rank — rank loss has overtaken
budget cap as the bigger constraint since the 8/21 read.

**Network breakdown (the actual finding):**

| Campaign | Real Search | Search Partners | Display/Content |
|---|---|---|---|
| TSD_Search_HVAC | 15 clk / $16.94 | 40 clk / $107.57 | 95 clk / $146.97 |
| TSD_Search_Electrical | 30 clk / $112.64 | 25 clk / $68.66 | 143 clk / $241.22 |
| TSD_Search_Branded | 18 clk / $37.72 | 0 clk / $0 | 35 clk / $42.76 |

Real Google.com Search was only **16% of clicks, 12% of conversions, 22% of spend** across the
account — the other 78% of the $774.48 weekly spend was going to Search Partners and Display, on
campaigns configured and named as Search-only. Of the 43 PPC conversions, 40 are still `Click to
call` (ad tap, not confirmed connected call) and 3 are `[TSD] Contact Form` — same
click-to-call-heavy composition as 8/21.

**Fix applied same session** (`clients/cool-hand-electric/fix_search_network.py`, same pattern as
Zen Air's correction earlier today — [[tsd-zen-air]]): `target_search_network` and
`target_content_network` both set to `False` on all 3 campaigns (24118511502, 24123995882,
24123995948). Read-back confirmed via GAQL, not just the mutation's success response — all 3 now
match branded's original Search-only config. Cool Hand Electric is no longer in the "still open"
list from the 8/24 book-wide audit.

**Not yet done:** no re-pull since the fix — next weekly check should compare real-Search-only
volume/CPL against this week's blended numbers to size the actual impact of the leak.

**Lifetime numbers, launch to date (2026-08-10 to 2026-08-24, 15 days), PPC only, LSA excluded:**

| Metric | Value |
|---|---|
| Total leads | 65 |
| Call leads (`Click to call`) | 62 |
| Form leads (`[TSD] Contact Form`) | 3 |
| Spend | $1,789.15 |
| Blended CPL | $27.53 |

Implied CPL by type (total spend ÷ count of each type — Google Ads doesn't split cost by
conversion action, same clicks drive both call and form conversions, so these aren't independently
priced, just a volume read): **call CPL $28.86, form CPL $596.38.** Form volume is the real gap (3
in 15 days vs. 62 call taps) — this lifetime window still includes the pre-fix Search
Partners/Display leak, so blended CPL should trend down from here.

---

## 2026-08-26 — Client asked for Google Ads vs. LSA breakdown, PPC-only update built

**Why.** AM ticket: Luke asked for a clearer breakdown of advertising performance, specifically
wanting Google Ads (Search) separated from Local Services Ads rather than blended, since LSA can
pull the blended CPL down significantly. Edu's direction for this pass: **disregard LSA entirely**
— don't pull or present its numbers, just make the structural separation explicit and give a clean
PPC-only breakdown by campaign. Consistent with the existing scope decision in `internal-notes.md`
(TSD doesn't manage this account's LSA), so "separating" it here means stating plainly that Search
and LSA are different products on the account and only Search is reported, not building out a
second LSA table.

**Deliverable:** `Cool-Hand-Electric-Performance-Update_2026-08-26.html/.pdf`, same plain Times New
Roman format as the 08-21 update, per [[tsd-client-report-plain-design]].

**Google Ads Search, Aug 10–25 (16 days live), pulled fresh via `.env.topserv` profile:**

| Campaign | Impr. | Clicks | CTR | Avg CPC | Spend | Conv. | Cost/Conv. | Impr. Share |
|---|---|---|---|---|---|---|---|---|
| TSD_Search_Electrical | 9,190 | 361 | 3.9% | $2.71 | $977.32 | 24 | $40.72 | ~10% |
| TSD_Search_HVAC | 6,914 | 321 | 4.6% | $1.99 | $640.29 | 31 | $20.65 | ~10% |
| TSD_Search_Branded | 1,113 | 97 | 8.7% | $2.02 | $196.05 | 11 | $17.82 | 55.9% |
| **Total** | **17,217** | **779** | **4.5%** | **$2.33** | **$1,813.66** | **66** | **$27.48** | |

LSA campaign (`LocalServicesCampaign:SystemGenerated:00062514e057f1df`, ID `21835713533`) pulled
for internal reference only, **not included in the client deliverable per Edu's disregard call**:
same 16-day window shows 146 clicks / 2,164 impr. / 15 conv. / $1,206.49 spend / $80.43 CPL. Kept
here so nobody re-derives it later and accidentally blends it back in.

**Client copy also notes** the 08-24 network-settings fix (framed as a routine efficiency check,
not as "we found a leak," per [[topserv-client-report-format]] golden rule) and offers to add LSA
as its own section in future updates if the client wants combined visibility rather than just
structural separation.

**Follow-up same day:** Edu asked to also show phone calls vs. form submissions. Pulled
`segments.conversion_action_name` by campaign for the same Aug 10–25 window (`.claude/skills/
google-ads-ratos/scripts/cool_hand_conv_by_action.py`) using `metrics.conversions` (not
`all_conversions`, which also pulls in non-primary "Local actions" engagements — confirmed the
`conversions` split reconciles exactly to the report's 24/31/11 campaign totals, `all_conversions`
does not).

| Campaign | Phone Calls | Form Submissions | Total |
|---|---|---|---|
| Electrical | 22 | 2 | 24 |
| HVAC | 30 | 1 | 31 |
| Branded | 10 | 1 | 11 |
| **Total** | **62** | **4** | **66** |

Added as a new "Conversions by Type" table in the client deliverable, same window, right after
the campaign table. Noted plainly that Google Ads doesn't split cost by conversion type, so
cost/conversion above stays a blended figure across both — no per-type CPL fabricated.

**PDF rendering note:** system Chrome (`/Applications/Google Chrome.app`, the path `build_plan.py`
uses) isn't present in this environment. Rendered via Playwright's bundled Chromium instead
(`python3 -c "from playwright.sync_api import sync_playwright..."`, same `page.pdf()` approach,
Letter size + 0.85in/1in margins to match the `@page` CSS). Output matches the original layout.

**Second follow-up same day:** Edu asked for a 1-page version. Condensed to a single Google Ads
table (dropped Impressions/Clicks/CTR/Avg. CPC, kept Spend/Conversions/Cost-per-Conv./Phone
Calls/Forms — the metrics the ticket actually asked for), cut the network-settings bullet (not
part of the ticket ask), folded the three commentary bullets into one paragraph, and shortened
the LSA section to a single paragraph with a plain header ("Not Managed by TopServ") instead of
a separate "On Local Services" close. Confirmed 1 page via `fitz.open(...).page_count`. Same
`.html`/`.pdf` filenames, re-rendered in place — no new files.

**Third follow-up same day:** Edu asked to split cost/call and cost/form separately. Added
Cost/Call and Cost/Form columns, computed as each campaign's total Search spend divided by that
conversion type's count (Electrical $44.42 / $488.66, HVAC $21.34 / $640.29, Branded $19.61 /
$196.05, total $29.25 / $453.42). Flagged to Edu before building it in: Google Ads doesn't
allocate cost by conversion action, so this is an implied split off the same spend pool, not a
true per-type price — same caveat as the 08-24 lifetime pull ($28.86 call / $596.38 form).
Client copy states this plainly and notes Cost/Form will swing a lot given only 1–2 form fills
per campaign — framed as an expected volume signal, not a problem, per
[[topserv-client-report-format]] golden rule. Still 1 page. Re-rendered in place, same files.

**Fourth follow-up same day:** Edu asked to add a note that a dedicated landing page is already
built, held back until the bid strategy has enough conversion history to use it well, so it
launches as a single clean, measurable change rather than stacking it on top of an account still
calibrating. Added as a new short section "Coming Next: Dedicated Landing Page" between the
Google Ads table and the LSA section. Still 1 page. Re-rendered in place, same files.

**Fifth follow-up same day:** Edu asked for the filename without dashes. Renamed both artifacts:
`Cool-Hand-Electric-Performance-Update_2026-08-26.html/.pdf` &rarr;
`Cool Hand Electric Performance Update Aug 26 2026.html/.pdf`. Same folder, same content — rename
only. The 08-21 update keeps its original dashed filename (not asked to change).

---

## 2026-08-31 — Weekly check-in, Meta launch gap found, Search Ad Rank overhaul

**Why.** Routine weekly check-in. Turned into a full session: baseline pull → Meta status check →
diagnosis of why HVAC/Electrical are stuck at ~10% impression share → three rounds of fixes
(negatives, budget reallocation, extensions, keyword restructure), each executed live and
confirmed via read-back, not just the mutation's success response.

### Baseline — last 7 days, PPC only (LSA excluded per scope)

| | Clicks | Leads | Cost | CPL | Conv. rate |
|---|---|---|---|---|---|
| Branded | 27 | 3 | $52.64 | $17.55 | 11.1% |
| Electrical | 107 | 4 | $496.72 | $124.18 | 3.7% |
| HVAC | 68 | 1 | $304.65 | $304.65 | 1.5% |
| YouTube (Demand Gen) | 944 | 4 | $126.86 | $31.71 | — |
| **Total PPC** | **1,146** | **12** | **$980.87** | **$81.74** | **1.05%** |

Total Search impression share 10.4% (account-level). LSA (excluded from scope, context only): 45
clicks / 4 conv. / $267.77.

**Lead quality check passed:** conversion actions are real (`PHONE_CALL_LEAD`, `SUBMIT_LEAD_FORM`,
`BOOK_APPOINTMENT`), no junk actions. Majority are still `Click to call` taps, not confirmed
connected calls — same caveat as 08-21/08-26.

**08-24 Search Partners/Display fix confirmed holding:** re-ran the network-type breakdown: every
off-network click in the trailing 7 days landed on 08-24 itself (same-day residue from before that
day's fix went live) — zero `SEARCH_PARTNERS`/`CONTENT` clicks 08-25 through 08-31.

### Meta — launch slipped, flagged to Edu

Queried the Meta MCP directly (full paginated `ads_get_ad_accounts` list, per
[[tsd-verify-meta-account-live]]): the "Cool Hand Electric" ad account (`1517373248873821`,
business `436575148084981`) now exists and is ACTIVE + queryable — confirms the account got
provisioned as planned. But **zero campaigns exist**, checked at both `last_7d` and `maximum` date
ranges, live and draft. Nothing has actually launched, a full week past the 08-24 target Edu gave
for brand awareness + the "Beat the Heat" AC offer (now losing runway into September). Not yet
resolved as of this log.

### Ad Rank diagnosis

Pulled `search_impression_share` lost-to-budget vs. lost-to-rank per campaign (last 7 days):

| Campaign | Impr. Share | Lost to Rank | Lost to Budget |
|---|---|---|---|
| Branded | 56.9% | 13.8% | **29.2%** |
| HVAC | 10.0% | **79.6%** | 11.2% |
| Electrical | 11.5% | **75.4%** | 13.1% |

This corrects the standing assumption in this log (08-05/08-21 entries) that HVAC/Electrical
headroom was budget-capped — it's overwhelmingly **rank**-capped instead. Branded is the one
campaign where budget really is the constraint, and it's the cheapest/best-converting segment.

**Search terms audit (14 days)** surfaced real waste with zero conversions: competitor-brand
queries (`waldrop electric ennis tx`, `encore electricity`, `silver spur hvac`, `aerocool hvac`,
`family first comfort`) slipping through via phrase-match close-variant expansion, plus off-topic
queries (`how do you install an air conditioner`, `kohler generators dealers near me`). Checked
existing keyword hygiene first: all keywords are PHRASE match (no broad), decent existing
cross-negatives already in place (electrician/plumber/hvac cross-negs, diy/how to, careers/jobs) —
but **zero competitor-name negatives** anywhere in the account, which is the actual gap.

**Quality Score pull** (`read.py quality-scores`, account-wide): `electrician` (Electrical →
Electrician-General, highest-volume Electrical keyword by impressions) and `hvac companies near
me` (HVAC → Furnace-Heating) both sat at **QS 1/10**, flagged BELOW_AVERAGE on creative and
predicted CTR. Branded keywords sit at QS 7–8 by contrast. Pulled the actual RSA copy too — ad
groups already do some tailored theming (2 keyword-specific headlines/descriptions layered on 6–8
shared ones), so this isn't a wholesale copy problem, just concentrated on the broadest head terms
sharing ad groups with more specific siblings.

**Extensions audit** (`read.py extensions`): 14 sitelinks (solid), but only one callout and one
structured snippet existed account-wide, both literally named `ZZ UNUSED test asset` — built once,
never finished or linked. **Zero call-type assets existed anywhere**, despite tap-to-call being the
majority of real conversions.

### Fix 1 — Negative keywords (campaign-level, PHRASE)

- Electrical: `waldrop electric`, `encore electric`, `kohler`, `how do`
- HVAC: `silver spur hvac`, `aerocool hvac`, `family first comfort`, `how do`

### Fix 2 — Budget reallocation into Branded

HVAC $44/day → **$36/day**; Branded $12/day → **$20/day**. Rationale: HVAC is rank-capped (80%
rank-lost IS), so extra budget wasn't buying it reach anyway, and it's the worst-performing
campaign; Branded was losing 29.2% IS to budget despite being the cheapest, best-converting
segment. Total PPC daily budget held flat at $148/day (Electrical and YouTube untouched).

**Compliance flag raised same session:** this workspace's `CLAUDE.md` states budget changes need
written client approval via an AM ticket, and Paid never executes first and informs after. This
move was executed directly on Edu's explicit instruction, without a prior AM ticket. Flagged to
Edu; resolution (retroactive ticket vs. revert) still open as of this log.

### Fix 3 — Extensions built (Call, Callouts, Structured Snippet)

All linked to Electrical, HVAC, and Branded; confirmed live via `campaign_asset` read-back.

- **Call extension:** `469-550-1102`, US, wired to `USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION`
  (account already has a biddable `CALL_FROM_ADS` conversion goal). **Verified live against the
  site directly** — resolves the open phone-number discrepancy flagged in the 08-10 entry
  (`469-550-1102` vs. `469-874-0523`); confirmed `469-550-1102` is current.
- **5 callouts** (all pulled from the live site, none invented): Licensed & Insured, Family-Owned
  Since 2015, Financing Available, Work Guaranteed, $37 Safety Inspection.
- **1 structured snippet**, header "Services," 10 values drawn from the account's own ad group
  structure: Panel Upgrades, Generator Installation, AC Repair & Installation, Furnace Repair,
  Surge Protection, Smoke & CO Detectors, Outlet Installation, Ceiling Fan Installation, EV Charger
  Installation, Circuit Breaker Repair.
- `create.py` has no `call` or `structured-snippet` subcommand (only `sitelink`/`callout`) — built
  via a one-off script following the same `AssetOperation` + `CampaignAssetOperation` pattern.
  Script lives only in this session's scratchpad, not committed to the repo — worth formalizing
  into the skill if another client needs the same.

### Fix 4 — Ad group restructure for the two QS-1 keywords

- `electrician`: removed from Electrician-General, moved into new ad group **Electrician-Broad**
  (`200481852420`, campaign `24123995882`) with a dedicated 10-headline/4-description RSA mirroring
  the exact term. Landing page unchanged: `https://coolhandelectric.com/electrician-mansfield-tx/`.
- `hvac companies near me`: removed from Furnace-Heating, moved into new ad group
  **HVAC-General-Broad** (`199432346123`, campaign `24118511502`) with a dedicated RSA. Landing
  page left at the homepage — **checked the live site's nav first and confirmed no unified
  HVAC/heating-and-cooling page exists** (site splits everything into AC-specific and
  furnace-specific pages: ac-repair, ac-installation-replacement, ac-maintenance, furnace-repair,
  furnace-installation-replacement, furnace-maintenance, heat-pump, plus shared
  duct-cleaning/indoor-air-quality/thermostat pages) — homepage is the least-bad real destination,
  not an oversight. Possible future site-side idea for Edu: a unified HVAC landing page.
- Both new ad groups + RSAs set to ENABLED (created PAUSED by default, per the skill's safety
  rule) and confirmed live via read-back. Old keyword placements REMOVED (not paused) so each term
  runs in exactly one ad group, no internal auction competition.

**Not yet done:** no re-pull since these fixes — next weekly check-in should compare fresh
IS/QS/CPL against this session's baseline to size actual impact. Meta launch and the budget-move
compliance question both remain open, Edu's call on both.

---

## 2026-09-24 — Client reported HVAC lead drop; diagnosed (no account changes), AM reply given

**Ticket.** "Client reached out regarding a drop in his HVAC leads." Read-only investigation, data through 09-23 (09-24 partial day excluded). **No changes were made to the account this session.**

**Verdict.** Not a demand collapse and nothing on our side broke. Mostly noise around a low baseline plus a client baseline inflated by the pre-8/24 traffic.

| HVAC Search | 09-10 to 09-16 | 09-17 to 09-23 |
|---|---|---|
| Impressions | 2,493 | 2,898 (+16%) |
| Clicks | 77 | 58 (-25%) |
| Leads | 8 | 2 |
| Conv. rate | 10.4% | 3.4% |

**Evidence it isn't demand.**
- Impressions and estimated eligible impressions up WoW (eligible is a lower bound, IS is floored at ~10%).
- Mansfield highs 97-98F the prior week, 95-96F last week (Open-Meteo), still peak cooling load. Lows eased ~78F to ~73-76F from 09-18.
- Mild softness is real: HVAC clicks -25% here, C&S Air (HVAC, Mansfield, same windows) non-branded clicks -18% and impressions -29%; LSA impressions fell in all three DFW-area accounts (Cool Hand, C&S Air, Spencer Air). Roughly a 20% click dip, not enough to explain 8 -> 2.
- Electrical on the same site/tracking went 6 -> 12 leads, so site and tags work.

**Why it reads as a drop.**
- Post-8/24 (Search Partners/Display fix) HVAC baseline is ~2.9 leads/wk: 13 leads / 272 clicks / $1,197 in 31 days, $92 CPL, 4.8% CVR. 09-17 to 09-23 (2 leads) is normal (~44% odds of <=2). 09-10 to 09-16 (8 leads) was the outlier (~1% odds).
- **Client anchor:** the 08-26 update we sent showed HVAC at 31 conversions / $20.65 per conversion for 08-10 to 08-25 (30 labelled "Calls"). Those were mostly `Click to call` taps, and per the 08-24 audit only ~12% of conversions came from real Google Search. Weekly HVAC leads were 9, 22, then 1, 2, 7, 1, 2. That level will not come back, so do not promise a rebound.
- Conversion signal also shifted on 08-31 (call asset wired to account-level `Calls from ads`, 60s threshold), so tap-era counts are not comparable to now.

**Controllable, found but NOT acted on (none caused the WoW dip; they cap volume):**
1. Rank, not budget, is the constraint: HVAC IS pinned ~10%, rank-lost 70-90% on most days. Bidding is Maximize Conversions with ~3 conv/wk and no target, so too little data to learn.
2. Geo is 8 cities (Arlington, Burleson, Ennis, Fort Worth, Mansfield, Midlothian, Red Oak, Waxahachie) on `PRESENCE_OR_INTEREST`; Dallas queries leak in ("hvac contractor dallas tx", "hvac companies in dallas texas") with 0 conversions. Converting terms were local ("hvac mansfield tx").
3. Phrase keyword `hvac repair` sits in the furnace-themed **Furnace-Heating** ad group and is the top impression source (639 -> 1,093 impressions, clicks 36 -> 25) at 95F. Ad-group CTR 5.5% -> 2.5%. Candidate for the same split treatment as the two QS-1 terms on 08-31.
4. No ad schedule; ~62% of HVAC clicks (84 of 135, 09-10 to 09-23) land outside Mon-Fri 8-5. Only matters if after-hours calls go unanswered; the hours vs "24/7 emergency" question in `internal-notes.md` is still unresolved.

**Planned next (Edu's call, not executed):** presence-only geo + Dallas negatives; move `hvac repair` into its own AC-themed ad group. **Hold:** bidding strategy change (resets learning), budget (needs written approval via AM ticket), ad schedule (needs hours answer). Re-check ~10-08 against the ~3 leads/wk baseline, not against one week.

**Ruled out.**
- Change history (API reaches back only 30 days, from ~08-26): last campaign/bid/keyword/budget edits were 08-31. Since then only two IMAGE asset creates, 09-02 and 09-16, by `analytics@relentless-digital.com` (outside email, unexplained, not linked to any campaign in the log). Worth asking the AM who that is.
- 17 of 17 Search ads APPROVED; call asset `469-550-1102` APPROVED/ELIGIBLE on Electrical, HVAC and Branded (phone impressions ~94% of impressions on HVAC).
- Landing pages `/` and `/ac-repair/` return 200 in under 0.6s.
- Campaign status: all ENABLED, primary status LIMITED (HVAC reason UNKNOWN, Electrical BUDGET_CONSTRAINED).

**Not checked.** Auction insights (not exposed via API, competitor pressure untested). The client's own call/CRM count, which is the real test; asked via the AM. Also noted while in the account: LSA budget was doubled $214 -> $428/day on 08-31 by `access@topservdigital.com` (LSA is out of scope), and LSA impressions kept falling anyway.

**Reply handed to the AM (internal, short).** Nothing broken, nothing changed on our side, ads running normally, impressions +16% WoW. Leads 8 -> 2 but the 8 was an unusually high week and HVAC averages ~3/wk since late August. Targeting tweaks coming. Suggested client line: ads running normally, prior week unusually high, adjusting targeting, and please share how many HVAC calls he's seen on his end. Heads-up for AM: the first two weeks looked higher because they included traffic outside regular Google Search, turned off 08-24.

**Still open from before.** 08-31 budget-move compliance flag (retroactive ticket vs revert), Meta launch slip, and the two open GTM items in `gtm-log.md`.

---

## 2026-10-08 — HVAC Search re-enabled

**Context.** Edu paused `TSD_Search_HVAC` (24118511502) by hand in the Ads UI on 2026-10-07 at 16:50 CT. He was worried it was sending traffic to the go. subdomain landing page (`go.coolhandelectric.com/electric-and-hvac-services/`). At 16:50:56 the same login also paused the only Branded ad (820479270937).

**Checked before re-enabling.** Every URL the campaign can send people to is on coolhandelectric.com: the ads, keyword final URLs, campaign/ad group/account sitelinks, tracking template and suffix. None of them use the go. subdomain. The go. page is only used by `TSD_YouTube` (Demand Gen), and its 9,768 clicks all-time all came from that campaign.

**Done.** On Edu's instruction, re-enabled via `update.py campaign --status ENABLED`. Read-back: ENABLED / SERVING / LIMITED (BUDGET_CONSTRAINED), still $36/day. Budget unchanged.

**Still open.**
- The Branded ad is still paused, so Branded can't serve. It points to the homepage, not the go. page. Waiting on Edu.
- The HVAC ad groups carry older ad-group-level sitelinks that point to electrical pages: grounding, outlets, panel, smoke detectors, surge, residential electrical, plus contact-us. They load (200), but they don't fit AC/HVAC searches.

---

## 2026-10-08 (later) — Branded ad re-enabled

**Done.** On Edu's instruction, re-enabled the only Branded ad (820479270937, ad group Brand-Terms 194393028410, campaign `TSD_Search_Branded` 24123995948) via `update.py ad --status ENABLED`. It had been paused from Edu's login on 10-07 at 16:50 CT together with HVAC Search. Read-back: ad ENABLED, APPROVED, final URL `https://coolhandelectric.com/` (homepage, not the go. LP). Campaign and ad group were already ENABLED. Budget unchanged.

**Still open.**
- Presence-only geo on all 3 Search campaigns (all still `PRESENCE_OR_INTEREST` as of 10-08). Drop the blanket Dallas negatives from the 09-24 plan: the 10-08 CPC check found Dallas-type searches converting (9 conv at ~$2.60 CPC).
- Move phrase `hvac repair` out of Furnace-Heating into its own AC-themed ad group.
- Replace the electrical ad-group sitelinks on the HVAC ad groups.

---

## 2026-10-08 (night) — Round 1 APPLIED: presence-only geo, negatives, Branded own-brand keywords, sitelinks

**Trigger.** Edu: "work on topics 1, 2, 3, 4, 5" (Cool Hand pending list). Edu chose to do them together, not 48h apart.
Budgets unchanged. Script: `round1_geo_negatives_sitelinks_2026-10-08.py` (validate-only first, then `--apply`, 127 ops).

**Why (QS pull, 30d, top 25 keywords).** Expected CTR is below average on every scored nonbranded keyword ($1,600 of
$2,389 scored spend). Ad relevance mostly above average except generic "near me" terms. Landing page below average on
`ac repair`, `hvac repair`, outlets. `hvac repair` QS 2.

**Done (read-back verified):**
1. **Geo:** HVAC, Electrical and Branded → PRESENCE (were PRESENCE_OR_INTEREST). Location lists unchanged (8 cities).
2. **Negatives (campaign-level PHRASE, from Aug 25 – Oct 7 search terms):** HVAC 19 → 37, Electrical 16 → 32.
   Both: cool hand, commercial, industrial, home depot, lowes, lowe's, ferguson, for sale, supply, apprentice,
   apprenticeship, solar, appliance. HVAC: window unit, team enoch, burke mechanical, daffan, jamar air. Electrical:
   encore electricity, fancher electric, motor repair. Blocked ~$190 of the visible 45-day spend.
   **Own brand first:** added PHRASE `cool hand hvac`, `cool hand heating`, `cool hand air`, `cool hand ac` to Branded
   (Brand-Terms) BEFORE negating `cool hand` in HVAC/Electrical, so brand searches keep an ad.
   **Left alone on purpose:** Dallas/Fort Worth/other city terms (converting), competitor names that converted
   (city wide electric, airmasters/air masters, lennox, milestone, joe cool's, arthur hagar), `24 hour electrician`.
   `industrial` and `motor repair` each blocked a term with 1 conversion; kept because the site says residential focus
   and motor repair isn't a listed service. Note: only ~44% of nonbranded spend shows as visible search terms.
4. **Sitelinks:** removed all 51 ad-group-level sitelink links (17 each on Furnace-Heating, HVAC-General-Broad,
   Brand-Terms). Several pointed to `/electrical/...` URLs that 301-redirect and DROP the gclid
   (`/electrical/residential-electrical-services/` lands on the homepage). Electrical had no sitelinks of its own, so it
   was showing the account-level HVAC set. New campaign-level sets, 14 new assets, direct URLs (200, no redirect, gclid
   kept), descriptions only from claims on the linked page:
   - HVAC (7): Air Conditioning Repair, AC Installation, AC Maintenance, Furnace Repair, Heat Pump Repair, Emergency HVAC Repair, Contact Us
   - Electrical (8): Electrician Services, Panel Upgrades, Surge Protection, Generator Installation, Ceiling Fan Installation, $37 Safety Inspection, EV Charger Installation, Contact Us
   - Branded (6): Electrician Services, Air Conditioning Repair, Panel Upgrades, Furnace Repair, $37 Safety Inspection, Contact Us
   The 4 account-level HVAC sitelinks are Google auto-created ("text customization"); the API refuses to link them
   anywhere, so they were left at account level (now overridden in every Search campaign).

**Round 2 (items 3 + 5) DRAFTED, NOT applied, waiting on Edu's copy approval.** `round2_rsa_drafts_2026-10-08.py`
(validate-only passed: rename + 16 RSAs), readable copy in `round2-rsa-copy-2026-10-08.md`. 16 new RSAs (15 headlines /
4 descriptions, keyword + city, verified claims, no pinning) next to the current ads; `round2_cutover_2026-10-08.py`
pauses each old ad only once its replacement is approved. Item 3 = rename Furnace-Heating → HVAC-Repair (it only holds
`hvac repair` + `hvac repair near me`, so no keyword move/history reset) with the new ad pointing to `/emergency-hvac/`
instead of the homepage.

**Site check 2026-10-08 (claims), flagged for Edu:**
- "Family-Owned Since 2015" callout (live on all 3 campaigns): "since 2015" is not on the site anymore.
- "$37 Safety Inspection" callout runs on HVAC too; it's an electrical offer.
- Current HVAC ads say "Licensed HVAC Pros/Techs"; the site only shows a TECL (electrical) license. The old ads go away at cutover.
- Site claims 24/7 / after-hours emergency service (and schema hours 00:00–23:59) while the hours on file are Mon–Fri 8–5. Still unresolved; kept out of ad copy.

**Next:** Edu approves copy → `round2_rsa_drafts --apply` → next day `round2_cutover --apply` (re-run until all 16 done).
Judge QS / expected CTR ~10-29 (structural changes take 2–3 weeks).

---

## 2026-10-08 (night, later) — Round 2 APPLIED: 16 new RSAs + Furnace-Heating renamed HVAC-Repair

**Edu approved all headlines and descriptions** (`round2-rsa-copy-2026-10-08.md`). `round2_rsa_drafts_2026-10-08.py --apply`:
Furnace-Heating (196336894302) renamed **HVAC-Repair**; 16 RSAs created ENABLED next to the old ads, all
REVIEW_IN_PROGRESS at read-back. New ad IDs in `.round2_new_ads.txt` (Electrician-Broad 827504261978 … HVAC-General-Broad
827504262143). Old ads still serving.

**Next:** run `round2_cutover_2026-10-08.py --apply` once reviews finish (re-run until all 16 report done). It pauses an
old ad only when its replacement is APPROVED/APPROVED_LIMITED. First run 10-08: nothing to pause yet (all under review).

---

## 2026-10-08 (night, last) — Callouts fixed

Edu: "execute on 1". `callout_fix_2026-10-08.py` (validate-only, then `--apply`, 10 ops). Read-back verified.
- "Family-Owned Since 2015" (not on the site anymore) → replaced by **"Family Owned and Local"** on HVAC, Electrical, Branded.
- "$37 Safety Inspection" (electrical offer) removed from **HVAC only**, replaced by **"Easy Payment Plans"** (site nav +
  AC install FAQ). It stays on Electrical and Branded.
Callouts now: Electrical / Branded = $37 Safety Inspection, Family Owned and Local, Financing Available, Licensed & Insured,
Work Guaranteed. HVAC = Easy Payment Plans, Family Owned and Local, Financing Available, Licensed & Insured, Work Guaranteed.

**Meta:** Edu 10-08: Cool Hand Meta is awareness only, no weekly Meta check needed.

---

## 2026-10-09 — Round 2 cutover APPLIED: 16 old ads paused

All 16 new RSAs came back APPROVED. `round2_cutover_2026-10-08.py` validate-only passed, then `--apply` paused 16 old ads
in one run (run via `tsd.sh`; plain `GADS_ENV_PATH` from the client folder picked up the skill's default `.env` and got
PERMISSION_DENIED). Read-back verified: every Electrical (9) and HVAC (7) ad group now has exactly one ENABLED ad, the new
one, APPROVED; the old one PAUSED (not removed, so it can be re-enabled). Branded untouched (1 ad, ENABLED/APPROVED).
The old HVAC ads with the "Licensed HVAC" claim are now off.

Paused old ad IDs: Electrician-Broad 822929426336, Electrician-General 820553832161, Ceiling-Fan-Installation 820479270625,
Circuit-Breaker-Repair 820438450764, Generator-Installation 820479130048, Outlet-Installation 820553800733, Panel-Upgrade
820479270472, Smoke-CO-Detector 820479268270, Surge-Protection 820438465884, AC-Repair 820438483143, AC-Installation
820553841350, HVAC-Repair 820553800784, Furnace-Repair 820479270910, Furnace-Replacement 820553832863, Heat-Pump-Repair
820553832866, HVAC-General-Broad 822929454677.

**Next:** QS / expected CTR recheck ~10-29.

---

## 2026-10-09 — 30-day client report built (Sep 9 – Oct 8)

**Deliverable:** `Cool Hand Electric - 30 Day Report (Sep 9 - Oct 8).pdf` (+ `Cool-Hand-Electric-30-Day-Report_2026-10-09.html`), plain style, 3 pages. For Edu to hand off via the AM; not sent.

**Numbers (Search only, LSA excluded):** $3,792.54 / 748 clicks / 20,806 impr / 66.5 conv / $57.03 CPL / 8.9% CVR / $5.07 CPC.
Electrical $2,091.85, 34, $61.52 · HVAC $1,071.80, 17, $63.05 · Branded $628.90, 15.5, $40.57.
Lead mix: Calls from ads 25.5, Contact Form 19, Book Now 8, Click to call (website taps) 14. Non-biddable "Local actions" and
Google-hosted "Clicks to call" left out. IS: Electrical 14.3%, HVAC 10.5%, Branded 79.3%, nonbranded combined ~12%;
rank-lost 55–59%, budget-lost ~30%.
Awareness, reported separately: YouTube $753.61 / 351,241 impr / 1,385 views / $2.15 CPM (its 55 "Click to call" + 2 subs
NOT shown as leads). Meta ARL campaign 120249398248040716 $599.10 / 118,981 impr / 35,423 reach / freq 3.36 / $5.04 CPM /
~1,200 est. ad recall at $0.50. All-channel total $5,145.25.

**Internal only, not in the client copy:**
- Oct 5–8 partial week = 4 leads at $138.78 (HVAC 0). Part of it is the 10-07 16:50 CT pause of HVAC Search + the only
  Branded ad (re-enabled 10-08); HVAC also spent only $11–34/d on 10-07/08. Report labels it a partial week and points to
  the 10-08/09 updates; it doesn't explain the dip.
- "Phone number taps" are CLICK_TO_CALL (website taps), not confirmed calls. Report asks the client for their call/job count.
- Report promises dedicated service landing pages "before they go live" (electrician, AC repair, HVAC repair). Cut if Edu
  doesn't want that committed yet.

---

## 2026-10-09 — Paused 4 small Electrical ad groups, first go. LP URL swaps (Edu's go)

**Context:** the new go.coolhandelectric.com pages are live: /electrician/, /ac-repair/, /hvac-repair/, and the homepage copy at the root (noindex).
Edu decided to pause the small Electrical services that have no dedicated LP yet, and to move 2 traffic sources onto pages that already exist.

**Paused (ad group level, ads untouched):**
- Smoke-CO-Detector `199868113420`: 30d $186.82, 3 conv
- Ceiling-Fan-Installation `204820073891`: 30d $151.13, 1 conv
- Generator-Installation `201604402920`: 30d $146.69, 3 conv
- Outlet-Installation `199194839716`: 30d $46.25, 0 conv

The TSD_Search_Electrical budget is unchanged. Its spend now concentrates on Electrician-General/Broad, which were ~30% budget-lost.

**Final URL changes (in-place AdService edits; the ads go back through review):**
- HVAC-General-Broad RSA `827504262143`: coolhandelectric.com/ → https://go.coolhandelectric.com/hvac-repair/
- TSD_YouTube (Demand Gen) ads `822291740824`, `822291773200`, `822364224155`, `822364489412`: go.coolhandelectric.com/electric-and-hvac-services/ → https://go.coolhandelectric.com/

The old combined page is no longer used by any ad.

**Read-back verified:** all 4 ad groups PAUSED. All 5 ads ENABLED with the new URLs, approval UNKNOWN (re-review).

**Open:**
- GHL form submits on go. pages are not a conversion yet (Edu's GTM work), so form leads from these 2 sources won't count until then. Calls are unaffected.
- On the go. homepage, "Book Online" still scrolls to the GHL form. The RecreateAI booking widget is not on the subdomain as of 10-09 (re-checked after Sha's fix: not live).
- Main ad groups (Electrician x2, AC-Repair, HVAC-Repair, Brand-Terms) still point to the main site. Their swap waits on Edu's test lead + GTM.

---

## 2026-10-09 (later): ALL serving ads moved to go.coolhandelectric.com (Edu's go)

**Context:** GTM v7 is live, tracking GHL forms + main-site contact form + Book Now. Edu's call: every ad goes to the new pages, Branded to the go. homepage.

**Final URL changes (in-place AdService edits, back in review):**

| Ad group | Ad ID | New URL | Old URL |
|---|---|---|---|
| Brand-Terms | 820479270937 | go./ | coolhandelectric.com/ |
| Electrician-General | 827504261981 | go./electrician/ | /electrician-mansfield-tx/ |
| Electrician-Broad | 827504261978 | go./electrician/ | /electrician-mansfield-tx/ |
| Panel-Upgrade | 827504261996 | go./electrician/ | /electrical-panel-repair-replacement/ |
| Circuit-Breaker-Repair | 827504261987 | go./electrician/ | /circuit-breaker-installation-repair/ |
| Surge-Protection | 827504262122 | go./electrician/ | /whole-house-surge-protector-installation/ |
| AC-Repair | 827504262125 | go./ac-repair/ | /ac-repair/ |
| AC-Installation | 827504262128 | go./ac-repair/ | /ac-installation-replacement/ |
| HVAC-Repair | 827504262131 | go./hvac-repair/ | /emergency-hvac/ |
| Furnace-Repair | 827504262134 | go./hvac-repair/ | /furnace-repair/ |
| Furnace-Replacement | 827504262137 | go./hvac-repair/ | /furnace-installation-replacement/ |
| Heat-Pump-Repair | 827504262140 | go./hvac-repair/ | /heat-pump/ |

The small groups were mapped by trade to the closest go. page (Claude's mapping). HVAC-General-Broad and the 4 YouTube ads were already moved earlier today and are now APPROVED.

**Read-back verified:** 17 serving-eligible ads, 0 on non-go URLs. The old combined LP is not referenced by any ad or linked asset.

**Not changed (still main site, as of 10-09):**
- All campaign sitelinks + the 5 Google auto-created account sitelinks.
- AC-Repair's 3 ad-group sitelinks, which override the campaign set (one is "Electrician In Mansfield").
- The call asset still dials the main line 469-550-1102.
- Paused ads/ad groups keep their old URLs.

**Watch:**
- On the go. homepage, "Book Online" still scrolls to the GHL form (no RecreateAI on the subdomain as of last check), so Branded bookings depend on Sha's fix.
- Check that all 12 ads come back APPROVED (~10-10).

---

## 2026-10-09 (later): Sitelinks moved to go. pages where policy allows (Edu: "use common sense")

**Policy constraint:** Google's sitelink requirements say each sitelink in a campaign must lead to a different landing page, and not to the ad's own page. With only 4 go. pages, the service campaigns can't point their sitelinks at go. (Electrical ads already land on /electrician/, HVAC ads on /ac-repair/ + /hvac-repair/).

**Applied** (script `sitelinks_go_pages_2026-10-09.py`, already run):
- New sitelink assets, linked to TSD_Search_Branded + TSD_YouTube (both land on go./):
  - 428923086331 "Electrician Services" → go./electrician/
  - 428923079863 "AC Repair" → go./ac-repair/
  - 428923086340 "Heating & HVAC Repair" → go./hvac-repair/
  - Descriptions use only claims already on the pages.
- Unlinked the old main-site sitelinks from Branded (6) and YouTube (4). The assets are kept, because Electrical/HVAC still use them.
- Unlinked AC-Repair's 3 ad-group sitelinks: "AC Repair Services" → homepage, "AC Maintenance", and "Electrician In Mansfield". AC-Repair ads now use the HVAC campaign set.

**Read-back verified.**

**Still on main site:**
- Electrical: 8 campaign sitelinks.
- HVAC: 7 campaign sitelinks.
- 5 Google auto-created account-level sitelinks. These don't show anyway, since every campaign has its own set.
- Decision pending with Edu.

---

## 2026-10-09 (late): go. ONLY, nothing to coolhandelectric.com (Edu's standing rule)

**Rule (Edu, said many times):** no ad, sitelink or asset goes to coolhandelectric.com or its pages. Only go.coolhandelectric.com.
YouTube + Branded → go./ · every Electrical ad group → go./electrician/ · AC groups → go./ac-repair/ · other HVAC groups → go./hvac-repair/.
The "decision pending" on Electrical/HVAC sitelinks in the entry above was wrong; it should have been done then.

**Applied** (script `go_only_sweep_2026-10-09.py`, already run):
- 20 ads still on main-site URLs moved to go. by trade: 16 old ads paused at cutover + the 4 enabled ads inside the paused
  Smoke-CO / Ceiling-Fan / Generator / Outlet ad groups. Nothing serves from these today; this is so a re-enable can't send traffic to the main site.
- Unlinked all 15 main-site campaign sitelinks (Electrical 8, HVAC 7) + the 5 Google auto-created account-level sitelinks.
- New sitelink asset 428823643154 "Schedule Service" → go./
- Electrical campaign: Schedule Service (go./) + AC Repair (go./ac-repair/) + Heating & HVAC Repair (go./hvac-repair/).
  Electrician Services is left off because every Electrical ad already lands on go./electrician/ (sitelinks can't repeat the ad's page).
- HVAC: ad-group-level sets so no sitelink repeats the ad's own page. AC-Repair + AC-Installation: Schedule Service + Heating & HVAC
  Repair + Electrician Services. HVAC-Repair, Furnace-Repair, Furnace-Replacement, Heat-Pump-Repair, HVAC-General-Broad: Schedule
  Service + AC Repair + Electrician Services. Campaign-level fallback: Schedule Service + Electrician Services.
- Branded + YouTube unchanged (already go.).

**Read-back verified:** 0 ads, 0 sitelinks (campaign/ad group/account), 0 keyword URLs, 0 tracking templates on the main site.
AI Max off and text asset automation opted out on all 3 Search campaigns, so Google can't route clicks to main-site pages itself.

**Not done / still open:**
- Meta: not checked or changed this session (Meta read permission denied). Per the 10-07 notes Meta paid traffic lands on the main-site homepage.
- Google can re-create dynamic (auto) sitelinks. Turn off "Dynamic sitelinks" under account-level Automated assets in the Ads UI.
- The call asset still dials the main line 469-550-1102 (phone, not a URL).
- Edited ads went back into review; check approvals ~10-10.

---

## 2026-10-09 (late, 2): sitelinks = SAME page as the ad + ?src=N (Edu)

**Rule (Edu):** sitelinks go to the same go. page the ad lands on, made distinct with ?src=1, ?src=2… Cross-trade sitelinks
(Electrical ads showing AC/HVAC links) read as disconnected. This replaces the Schedule Service / cross-sell sets from the entry above.

**Applied** (script `sitelinks_same_page_src_2026-10-09.py`, already run). Unlinked 11 campaign + 21 ad-group links, created 19 assets:
- Electrical (campaign): go./electrician/?src=1–6: Get Your Electrical Quote, $37 Safety Inspection, Panel Upgrades, Surge Protection, EV Charger Installation, Generator Installation
- HVAC (campaign, used by the 5 HVAC groups): go./hvac-repair/?src=1–5: Request HVAC Service, Furnace Repair, Heat Pump Repair, AC Repair & Replacement, Thermostats & Air Quality
- AC-Repair + AC-Installation (ad-group level): go./ac-repair/?src=1–4: Request AC Repair, AC Blowing Warm Air?, AC Installation, Repair or Replace?
- Branded + YouTube (campaign): go./?src=1–4: Electrical Services, AC Repair, Furnace Repair, Book Online
Text/descriptions use only claims on the live pages (checked 10-09). Pages return 200 with ?src.

**Read-back verified:** every active ad group's sitelinks point to its own ad's page. All 17 serving ads APPROVED.
**Watch:** new sitelink assets are in review. Google may flag same-page sitelinks as duplicate destinations; check ~10-10.
?src shows up as a URL param in GA4 page_location for sitelink clicks.

---

## 2026-10-10 (morning): post-change check (read-only, nothing changed)

**Approvals:** all 27 enabled sitelink links are APPROVED/ELIGIBLE. All 37 ads are APPROVED (17 serving + 20 paused).
**Change history** since 10-09 17:00 CT: only our API changes (17:02–17:29 CT). No one else touched the account.
**Destinations:** every click and impression on 10-10 is on go. URLs. The 10-09 main-site clicks were all before 17:00 (pre-change).
New ?src sitelinks are already showing on Electrical, HVAC, AC groups and Branded. YouTube's go./?src sitelinks took ~23 clicks on 10-09 evening.
**Since the change** (10-09 17:29 → 10-10 ~07:00 CT, Fri night into Sat morning): Search 1 click, Electrical 22h, $19.36 = 1 Call from ads.
Branded 3 impr / 0 clicks. YouTube ~$9 as usual. No form leads yet, too little traffic to test the go. page forms.
**HVAC was dark 16h–23h on 10-09, not from our changes:** a single $46.00 call click at 15h (Calls from ads) pushed the day to $54.16
on a $36/d budget (BUDGET_CONSTRAINED), so it stopped serving. 'fast response' ($8.16, 0 conv) also bought a click at 11h, worth a negative.
Leftovers moved to Command Center fu-036 (dynamic sitelinks toggle, Meta URLs).

---

## 2026-10-10: call asset switched to the CallRail number (Edu's go)

**Change** (script `call_asset_callrail_2026-10-10.py`, already run): new call asset 429092777632 with phone **469-351-1738**
(CallRail, same number as the go. pages) is linked to TSD_Search_HVAC, TSD_Search_Electrical and TSD_Search_Branded.
Old asset 415288389635 (469-550-1102, main line) is unlinked but kept. Rollback = relink it.
Same settings as before: US, account-level call conversion action ("Calls from ads"), no schedule. New links went in before old ones were removed, so there was no gap.

**Why:** ad-extension calls went straight to the main line and never touched CallRail. Now they go
Google forwarding number → 469-351-1738 (CallRail) → business, so they still count as "Calls from ads" in Google AND get logged in CallRail.

**Read-back verified:** 3 links ENABLED on the new asset, approval under review at write time.
The number shows on every go. page (the final-URL domain), which Google's phone verification needs.
**Watch:** call asset approved (phone verification)? "Calls from ads" still recording next week?
CallRail still not accessible to TSD (separate account, company 865715539).
**Caveat (noted after the switch):** the call asset and the go. pages now use the same CallRail number, so CallRail mixes
ad-button calls with website calls. Split them by matching Google's call_view (start time, duration) against the CallRail
call list, or, the proper fix once we have CallRail access, give the call asset its own CallRail number.

---

## 2026-10-10: "Calls from website" conversion for go. pages (Edu's go)

**Why:** to split the two call paths without a second CallRail number and get the funnel clicks → taps → calls by campaign/keyword.
Google's tag swaps 469-351-1738 on go. pages for ad visitors with a Google forwarding number → 469-351-1738 (CallRail) → business.
Calls ≥60s count as website calls, separate from "Calls from ads". CallRail still gets every call.

**Ads:** new conversion action **7835207883 "[TSD] Calls from website (go.)"**: WEBSITE_CALL, PHONE_CALL_LEAD, origin WEBSITE,
60s, one per click, value 1. **SECONDARY** (include_in_conversions_metric = False): it reports under All conv. only and
Max Conversions does NOT bid on it. Script `website_call_conversion_2026-10-10.py`.
**GTM:** live v8, tag 32 + trigger 31, go. hostname only (see gtm-log.md). Script `gtm_website_call_tag_2026-10-10.py`.

**Decision for Edu, after ~2 weeks of data:** make website calls biddable? If so, the "Click to call" taps action
(CLICK_TO_CALL, PHONE_CALL_LEAD/CALL_FROM_ADS, biddable today) should go secondary, or a tap that turns into a call counts twice.
Note: the taps share the PHONE_CALL_LEAD/CALL_FROM_ADS goal with "Calls from ads", so splitting them means recategorizing one
(goals can't split inside a bucket). Also open: "Phone Call" (UPLOAD_CLICKS, DEFAULT/WEBSITE, biddable, 0 conv since July), likely
a client CallRail integration. If it ever starts uploading, it double counts.

---

## 2026-10-10: Dynamic sitelinks OFF (Edu, Ads UI via Claude in Chrome)

Account-level automated assets → Dynamic sitelinks switched OFF; Edu confirmed it in the UI. The API change history doesn't log this
setting. Google can no longer auto-create sitelinks (the 5 old auto ones pointed at main-site pages; they're REMOVED and none are new).
Google side of the go.-only rule is complete. Only Meta destination URLs are left (Command Center fu-036).

---

## 2026-10-10 (later): CallRail Website pool replaces Google website-call tracking

**Found via the CallRail API** (same key, account "Cool Hand Electric & Air PPC TopServe"): a "Google Ads" tracker (469-351-1738, built for
the ad call button) and a 4-number "Website pool" that never swapped (its target 469-874-0198 isn't on any page). There's a Google Ads integration
(all calls, values on) feeding the "Phone Call" upload action, with 0 uploads ever because no call had a gclid. Only 1 call since June.
**Changes:**
- Edu re-pointed the pool's swap target to 469-351-1738 (CallRail UI). go. visitors now get a pool number carrying gclid/UTM/keyword/landing page.
  469-351-1738 now rings only from the ad call button → CallRail separates ad-button calls ("Google Ads" tracker) from website calls (pool).
- GTM v9: Google website-call tag 32 paused (see gtm-log.md). Action 7835207883 "[TSD] Calls from website (go.)" stays, secondary, now idle.
- "Phone Call" (7830770637, DEFAULT/WEBSITE) set **NON-BIDDABLE** at the account default (all 4 campaigns follow; read-back False).
  Script `phone_call_upload_observe_only_2026-10-10.py`. Once the pool gets website calls with gclid, CallRail uploads them; they report
  under All conv. only, so they don't double count with "Click to call" taps in Max Conversions.
**Funnel from here:** ad clicks (Ads) → taps ("Click to call") → website calls (CallRail pool, per click/keyword) → "Phone Call" uploads (All conv.);
ad-button calls = "Calls from ads" (Ads) + "Google Ads" tracker (CallRail).
**Decision for Edu (~10-24):** which call signal should bid: taps, CallRail website calls, or both with taps off.
**Watch:** pool of 4 vs YouTube's ~250 go. visits/day. Check CallRail pool accuracy/overflow after a week.

---

## 2026-10-10: Lead funnel on the Command Center

Command Center v3: Cool Hand pop-up has a "Lead funnel" section (week picker, Search / YouTube / All, website path +
ad-button path, per-campaign table). Data = `funnel_build.py` (Google Ads + CallRail, read-only) → `funnel/funnel_<date>.json`
→ db funnels/cool-hand-electric. Website calls tie to campaigns by matching gclid against Google click_view.
Refresh it on every check. First load: weeks Sep 29–Oct 5 (Google only) and Oct 6–12 (CallRail from Oct 10).
**Update same day:** funnel is now daily (one row per day per campaign since 08-10), and the page sums any range: Today, Yesterday,
Last 3/7/14/30 days (full days through yesterday), This week, Last week, Custom. Refresh = rerun funnel_build.py + reload the JSON.
**Refresh (10-10):** Command Center v5 has "Refresh now" + auto-refresh on open (data >6h old) via the local MCP tool tsd_funnel
(Claude desktop app only, owner only; needs one app restart). Scheduled twice-daily push NOT installed: the safety check blocked an
unattended headless-Claude job; needs Edu's explicit OK. Script ready: .claude/skills/google-ads-ratos/scripts/funnel_refresh_daily.sh.
