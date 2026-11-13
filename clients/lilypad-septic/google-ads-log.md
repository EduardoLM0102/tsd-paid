# Lilypad Septic — Google Ads log

CID `3797438623`. Salina & Hutchinson, KS. Site: lilypadseptic.com.

---

## 2026-08-20 — Account found under TSD MCC: this is a takeover, not a blank-slate build

**Why.** Edu asked to check if Lilypad had an account under the TSD MCC and launch it. `internal-notes.md` and `README.md` (written 2026-07-20/07-31) assumed a full ground-up build — no CID, no tracking, blank slate.

**That assumption was wrong.** Refreshed the MCC's 124 accounts and found `3797438623`, descriptive name **"RYNO - Lily Pad Septic FKA Salina Septic Services"**, `status = ENABLED`, `currency = USD`, `time_zone = America/Chicago`. This is a **takeover from a prior agency (RYNO)**, added to the TSD MCC at some point without a corresponding update to this client's docs.

**Account inventory:**
- **5 pre-existing campaigns, all `SEARCH`, all `PAUSED`**: `RYNO - CG-Branded` (22614040020), `RYNO - CG-Septic` (22614040023), `RYNO - CG - Sewer and Drain Cleaning` (23391984957), `RYNO - CG-Plumbing` (23484885552), `RYNO - CG-Sewer` (23494641775). **Real 2026 YTD spend across them: ~$10,038** (Branded $2,461, Septic $4,975, Plumbing $1,130, Sewer $1,471, Sewer-and-Drain-Cleaning $0) — so these ran and were later paused, not stillborn.
- **`RYNO - CG-Plumbing` is out of TSD's scope** per the media plan (Edu's condition: site sells no water heaters, repiping, or fixtures — septic/drain/sewer/portable sanitation only). Left PAUSED, untouched — a scope decision, not a technical one, so not deleting it.
- **Conversion actions already exist**, several `ENABLED` and `primary_for_goal: true`: `BC Calls v2`, `BC Qualified Calls`, `BC Qualified Forms`, `BC Qualified Ext Calls` (all `UPLOAD_CLICKS`/`UPLOAD_CALLS`, call-tracking imports, "BC" = unidentified third-party provider, not confirmed), `Call Extension Calls` (`AD_CALL`), `RYNO Lead Forms` (`WEBPAGE`, `SUBMIT_LEAD_FORM`). Several GA4-linked actions exist but are `HIDDEN` (purchase, form_submission x2, bct_calls_all, bct_form_submission, close_convert_lead, qualify_lead, unt_click_call_nl_website).
- **These actions show real YTD 2026 volume**: Call Extension Calls 147, BC Qualified Calls ~99, BC Calls v2 68, Local actions - Other engagements 61, Local actions - Website visits 38, Clicks to call 32, BC Qualified Ext Calls ~14, Local actions - Directions 9, BC Qualified Forms 4, RYNO Lead Forms 2.
- **Not verified: whether any of this is still live post-transfer.** Volume above is YTD-cumulative from when the RYNO campaigns were still spending — it does not prove the call-tracking numbers or lead-form webhook still route anywhere TSD or the client can see today. Same failure mode as Proud Pops (tags died silently on a rebrand) and Golden Plumbing (conversions zeroed since April, never caught). **TSD hard rule stands: no end-to-end lead flow test has been run. Do not treat this tracking as working until one is.**

**Corrected: internal-notes.md and README.md's "prospect, blank slate" framing is stale and needs a rewrite** — not done in this session, flagging for next touch.

---

## 2026-08-20, same day — Branded + Non-Branded Search built (PAUSED)

**Why.** Edu confirmed the account and asked for the PPC campaign, branded and non-branded, now. Built both, everything PAUSED — matches the skill's hard rule and the Gillespie's precedent (build now, verify tracking and get budget signed off before flipping to ENABLED).

**Site recon** (`lilypadseptic.com/get-septic-services/`, fetched directly — WebFetch was blocked by a 403, used curl with a browser UA instead): confirms **real phone numbers — Salina 785-268-2656, Hutchinson 785-626-8621** (resolves the phone discrepancy flagged in `internal-notes.md`; matches the "researched" Salina number and one of the three intake numbers for Hutchinson). Also confirms: 24/7 emergency + same-day service, 5.0 Google rating, PSAI certified, Sludgehammer Aerobic certified, Salina Area Chamber member, locally owned, two yards (1550 S Broadway Blvd Salina / 420 S Main St Hutchinson), upfront pricing / no upsells, Flush Family Plan (yearly eval + full pump-out + 12-mo additive supply + $100 annual repair credit + guaranteed same-day service + member pricing — **no monthly dollar figure found on the live page**, so none used in ad copy), and portable restroom rental (standard units, luxury trailers, handwashing stations, next-business-day delivery, weekly cleaning/restocking, for weddings/events/construction).

**Landing page:** `https://www.lilypadseptic.com/get-septic-services/`, per Edu, used for all ad groups (only page given, site doesn't have per-service pages). **Flagging a message-match risk**: the page's hero and primary CTA are entirely septic-emergency framed ("Septic Backed Up? Don't Wait"); portable-restroom-rental only appears in an FAQ answer. Non-branded restroom-rental clicks will land on a page that doesn't match search intent well — likely hurts Quality Score and conversion rate on that ad group specifically. Not blocking the build since it's the only page available, but worth a dedicated rental landing page later.

**Campaigns:**

| Campaign | ID | Budget | Bidding |
|---|---|---|---|
| TSD_08.20_Search_Branded_Evergreen | `24153698844` | $10/day | Manual CPC |
| TSD_08.20_Search_NonBranded_Evergreen | `24164203087` | $34/day | Manual CPC |

**Budget is a placeholder, not an approved number.** No written budget approval from Cole exists (same open gate `internal-notes.md` already flagged). Sized off the Aug-Sep interim media plan's $3,000/mo scenario — Google Ads gets 45% share = ~$1,350/mo ≈ $44/day, split $10 branded / $34 non-branded. **Needs real sign-off before activation**, per TSD's rule that paid never executes first and informs after.

**Geo:** Salina City (1017623), Hutchinson City (1017518), South Hutchinson City (1017635) — city-level LOCATION criteria on both campaigns. English language criterion (1000) added via direct mutate (no CLI flag for it). Did **not** split Salina and Hutchinson into separate campaigns despite `internal-notes.md`'s "never average their performance" guidance for the two markets — Edu asked for branded/non-branded specifically; market-level splitting is a follow-up if warranted once real data comes in.

**Ad groups + keywords (37 total, PHRASE match):**

| Ad group | Campaign | Keywords | CPC ceiling | Notes |
|---|---|---|---|---|
| Brand Terms | Branded | 7 | $2.50 | lilypad septic, legacy names (salina/hutchinson septic service) |
| Septic Pumping and Repair | NonBranded | 12 | $6.00 | Best landing-page match |
| Septic Installation | NonBranded | 8 | $7.00 | Aug-Sep priority — fills the fall dig calendar |
| Portable Restroom Rental | NonBranded | 10 | $5.00 | Aug-Sep priority — restroom season; landing page mismatch noted above |

CPC ceilings are planning-assumption based ($4-9 CPC per the media plan), not from fresh Keyword Planner data — the county-scoped Keyword Planner gate `internal-notes.md` flagged is still open.

**Negatives (15, campaign-level, non-branded):** plumbing/fixture exclusions (water heater, repiping, faucet repair, garbage disposal, toilet repair, leak detection, pipe repair, sump pump — keeps the account's own plumbing-out-of-scope rule intact even though `RYNO - CG-Plumbing` exists in the account), hiring/jobs/DIY exclusions, and brand cross-negatives (lilypad, lily pad) so brand queries route to the branded campaign.

**Ad copy:** 8 headlines + 3 descriptions per RSA (4 RSAs total), built only from verified site facts — no invented pricing (deliberately excluded the "$89/mo" figure referenced in `README.md`'s Aug-Sep plan summary since it doesn't appear on the live site). Extensions: 5 callouts per campaign (24/7 Emergency Service, 5.0 Google Rating, PSAI Certified, Locally Owned & Operated, Upfront Pricing). No sitelinks — only one landing page exists, didn't want to invent distinct destination URLs.

**QA verified before closing this entry:** both campaigns `PAUSED`, budgets $10/$34 per day, all 4 ad groups `PAUSED` with correct CPC bids, 37 keywords confirmed, 15 negatives confirmed, all 4 RSAs `PAUSED` with correct final URL and headline/description counts, 10 callout assets linked.

**Not done — blocks activation:**
1. **Written budget approval from Cole**, routed through the AM. Current $10/$34 split is Edu's placeholder from the media plan, not a client-approved number.
2. **End-to-end lead flow test.** The account's existing `BC`/`RYNO Lead Forms` conversion actions show real historical volume but are unverified as still live post-transfer — do not bid toward them, do not tell the client tracking works, until a real test lead is proven to land somewhere visible.
3. **LSA eligibility check** for "Sewage system" in 67401/67501 — still unrun, gates the LSA channel (not built in this session — this build was Search only, per what Edu asked for).
4. **Decision on the 5 legacy RYNO campaigns**, especially `CG-Plumbing` (out of scope) — left untouched and `PAUSED` this session. Worth a call on whether to formally end/remove them or leave dormant.
5. Hours conflict (24/7 advertised vs Mon-Fri 8-5 on file) — unresolved, relevant to any future ad schedule restriction.
6. QA by someone other than the builder.

---

## 2026-08-20, same day — Cole approved $2,000/mo, asked for LSA category review + advice on a no-LSA alternative

**Cole's message (via Edu/AM):** approved $2,000/mo. Flagged concern, from past experience, that few LSA categories may fit Lilypad's services — asked to confirm what's actually available. Proposed a fallback if LSA doesn't pan out: Google PPC ~$1,400/mo + Meta ~$600/mo, no LSA, non-branded Google spend split 50/50 between portable restroom rentals and septic service/install/repairs.

**LSA category review (restating the 2026-08-13 research already in `internal-notes.md`, nothing new found):**
- **"Sewage system" is the only category that fits.** Confirmed live, national, standalone (separate from Plumbers and Drain expert), with subcategories (Cleaning, Excavation, Inspection, Installation, Locating, Maintenance and Repairs, Pumping, Removal/Demolition) that map onto Lilypad's septic work.
- **"Drain expert" is restricted to California and Florida only** — not usable in Kansas regardless of anything else.
- **No LSA category exists for portable restroom / porta-potty rental, at all.** This isn't a Kansas-specific gap — the category doesn't exist anywhere in LSA. **This means LSA can never fund the restroom-rental line of business**, independent of the ZIP question below.
- **"Plumber" exists nationally but stays out of scope** — Lilypad isn't a general plumber (Edu's condition, holds regardless of channel).
- **Cole's instinct is correct: LSA categories genuinely are thin here** — one fitting category (Sewage system), for one of the business's two lines.
- **What's still unverified, and can't be checked from here:** whether "Sewage system" is actually *offered* in ZIP 67401/67501 specifically. Google doesn't publish category-by-ZIP availability anywhere queryable (not in the Ads API, not on a public page) — it only surfaces once someone runs the ZIP through the actual LSA sign-up flow at ads.google.com/localservices, which requires signing in and starting the onboarding wizard. This account has no LOCAL_SERVICES campaign today, so that check has never been run. It's a five-minute check for whoever is willing to start that sign-in flow — recommend doing it regardless of which budget path gets picked, since it's cheap and resolves real uncertainty either way.

**Recommendation: go with Cole's alternative (Google $1,400 + Meta $600, no LSA).**
Reasoning: LSA can *at best* cover half the business (septic only, restrooms are structurally excluded) and that best case is still unconfirmed at the ZIP level. $500-600/mo sitting in a channel that might not even be available, to fund only one of two business lines, is worse than folding it into Search — which already reaches both lines through the ad groups built above. Two channels (Google + Meta) is also simpler to monitor for a first launch on an account with inherited, unverified tracking. If the ZIP check later comes back eligible, LSA can be layered in afterward without disrupting this structure.

**On the 50/50 restroom-vs-septic split: directionally sound, one nuance to flag.** August-September is restroom season and matches the plan's own counter-cyclical logic, so 50/50 at the macro level holds up. Within the septic 50%, consider weighting Install above Pumping/Repair specifically in these two months — the fall dig window closes around October, so an install lead bought in August digs this fall while the same lead in October digs next spring (per the media plan's own reasoning); pumping/repair demand doesn't carry the same seasonal penalty and can be captured just as well later. Flagging as a refinement for Cole/AM to weigh in on, not overriding his number.

**Budgets adjusted to match (still PAUSED, still placeholders pending final confirmation):**
- `TSD_08.20_Search_Branded_Evergreen` (24153698844): $10/day → **$5/day**
- `TSD_08.20_Search_NonBranded_Evergreen` (24164203087): $34/day → **$41/day**
- Total Google Ads: $46/day ≈ $1,400/mo, matching the alternative allocation.

**Known limitation of this structure:** the three non-branded ad groups (Restroom, Septic Service, Septic Install) still share one campaign budget — Google's auction decides the actual spend split day to day, the ad group CPC ceilings ($5/$6/$7) only bias it, they don't hard-enforce a 50/50 split. If Cole wants the 50/50 literally budget-enforced, that needs two separate non-branded campaigns (Restroom vs Septic) each with its own daily budget — not done yet, flagging as a follow-up if he wants it precise rather than auction-biased.

**Meta ($600/mo) is out of scope of this build** — no Meta campaign exists for Lilypad yet, separate tool/session.

---

## 2026-08-20, same day — Legacy RYNO campaigns renamed (cosmetic only)

**Why.** Edu asked to rename the inherited RYNO campaigns to TSD's naming convention so the account doesn't show a prior agency's branding. Name field only — no change to status, budget, targeting, or the ad groups/keywords underneath.

| Old name | New name | ID |
|---|---|---|
| RYNO - CG-Branded | TSD_Search_Branded_Legacy | 22614040020 |
| RYNO - CG-Septic | TSD_Search_Septic_Legacy | 22614040023 |
| RYNO - CG - Sewer and Drain Cleaning | TSD_Search_SewerDrainCleaning_Legacy | 23391984957 |
| RYNO - CG-Plumbing | TSD_Search_Plumbing_Legacy | 23484885552 |
| RYNO - CG-Sewer | TSD_Search_Sewer_Legacy | 23494641775 |

Appended `_Legacy` rather than reusing today's naming pattern so the two structures (today's fresh Branded/NonBranded build vs. the inherited RYNO structure) don't get confused later. `TSD_Search_Plumbing_Legacy` is still out of scope per the media plan — renamed for consistency, not reactivated. Read back and confirmed via `read.py campaigns`: all 7 campaigns in the account now read as TSD names, all still `PAUSED`.

---

## 2026-08-20, same day — Launched: TSD_08.20_Search_Branded_Evergreen + NonBranded_Evergreen enabled

**Why.** Edu asked to turn on "the ones we need to turn on." Interpreted as today's two fresh campaigns only — not the 5 renamed legacy campaigns, which overlap with the new build's keyword coverage and include an out-of-scope Plumbing campaign. Did not enable any legacy campaign.

**Pre-flight check on the tracking gate before flipping anything:** fetched the live landing page again and found a GTM container actually loading on the page — `GTM-KG7WCQN`. **This container is not one of TSD's own managed GTM accounts** (checked `gtm.py accounts` under the TSD GTM login — not present), meaning TSD cannot currently see or edit what's configured inside it. It's presumably still under RYNO's control. **This means the true end-to-end lead flow (does a call/form on this page actually reach Cole/ServiceTitan) remains unverified**, and TSD has no visibility to verify it independently right now. Flagged this to Edu directly before activating — he proceeded on his own authorization as the accountable Head of Paid role. Noting per `aprendizados.md`'s general rule (never report success without read-back) that this applies to trust-in-tracking too, not just to writes: **historical conversion volume in this account is not proof current tracking works.**

**Technical note:** both campaigns use Manual CPC, not Maximize Conversions, so they do **not** require a working conversion action to serve or spend — they will generate clicks and spend budget regardless of whether any lead is actually being captured downstream. This is a real business risk (spend without provable ROI), not a technical blocker.

**Activated, in order (campaign → ad groups → ads, per the skill's activation rule), all confirmed via read-back:**
- `TSD_08.20_Search_Branded_Evergreen` (24153698844, $5/day) — `ENABLED`. Ad group `Brand Terms` — `ENABLED`. RSA `821590689304` — `ENABLED`.
- `TSD_08.20_Search_NonBranded_Evergreen` (24164203087, $41/day) — `ENABLED`. Ad groups `Portable Restroom Rental`, `Septic Pumping and Repair`, `Septic Installation` — all `ENABLED`. All 3 RSAs — `ENABLED`.
- All 5 legacy (RYNO-origin, now TSD-renamed) campaigns confirmed still `PAUSED`, untouched.

**Open items, now that this is live (not paused):**
1. **Tracking visibility gap** (above) — get access to `GTM-KG7WCQN` (or confirm with Cole what's actually wired) as soon as possible. Until then, nobody at TSD can independently confirm a lead is being captured.
2. Written budget approval on file with the AM for the $2,000/mo (Cole approved directly per Edu; per MasterOps this should still get a ticket for the record, same pattern noted on other clients in this workspace).
3. LSA ZIP-eligibility check (67401/67501, "Sewage system") still unrun — moot for today's launch (going with the no-LSA alternative) but worth doing since it's cheap and could add a channel later.
4. Hours conflict (24/7 advertised vs Mon-Fri 8-5 on file) — still unresolved, relevant to whether an ad schedule restriction should be added.
5. Meta ($600/mo) not built yet — separate session/tool.
6. **Stage: 3-day check should be scheduled** — is it spending, lost to rank or budget, and critically, is anything showing up as a real lead anywhere visible.
7. QA by someone other than the builder, not done.

---

## 2026-08-26 — Targeting check finds Search Partners/Display still on, fixed same session

**Why.** Edu asked to check Lilypad's targeting as part of a portfolio sweep (Zen Air, Cool Hand
Electric, Lilypad). Location targeting confirmed correct — Salina (1017623), Hutchinson (1017518),
South Hutchinson (1017635) city criteria present on both live campaigns, matches the 08-20 build.

**But:** both live campaigns still had `target_search_network = true` and
`target_content_network = true`. This is the same `create.py` bug found across the book on 08-24
([[tsd-zen-air]], [[tsd-cool-hand-electric]]) — Lilypad was named on that audit's still-open list
and never got circled back to, because this account's build (08-20) predates the 08-24 audit that
found the pattern.

**Impact at time of fix** (2026-08-20 to 2026-08-26, 6 days live):

| Network | Clicks | Spend |
|---|---|---|
| Real Search | 44 | $176.78 |
| Search Partners | 2 | $2.02 |
| Display/Content | 1 | $1.15 |

Small in dollar terms (~2% of spend) since the account is only 6 days old — caught early, before it
compounds toward the full $2,000/mo.

**Fixed 2026-08-26**, authorized by Edu, direct mutate on both campaigns (`update.py` doesn't expose
`network_settings`):
- `TSD_08.20_Search_Branded_Evergreen` (24153698844): `target_search_network` / `target_content_network` → `false`
- `TSD_08.20_Search_NonBranded_Evergreen` (24164203087): same

Confirmed via fresh GAQL read-back post-mutate, not just the mutate response.

### Aberto

- [ ] Fold into the AM ticket already owed for the $2,000/mo verbal approval (open item #2 above) —
  one more change to register in writing.
- [ ] Next performance pull should show real-Search-only volume; blended numbers from 08-20–08-25
  include a small amount of Partners/Display.

---

## 2026-09-15 — Weekly snapshot (LAST_7_DAYS) + conversion-type check

**Why.** Edu asked for the standard weekly PPC metric bundle, then a follow-up on what conversion
actions made up the total. Pulled via `insights.py account`, `read.py campaigns`, and a one-off
GAQL (`FROM customer`, `segments.conversion_action_name`) — all against CID `3797438623`, no LSA
running on this account so nothing to exclude.

**Account-level:**

| Metric | Value |
|---|---|
| Spend | $239.21 |
| CPL | $29.94 |
| CPC | $4.12 |
| Total Conversions | 7.99 |
| Conv Rate | 13.78% |
| Impression Share (Search) | 68.47% |

**Branded vs. Unbranded:**

| | Branded | Unbranded |
|---|---|---|
| Conversions | 2.50 | 5.50 |
| CPL | $16.82 | $35.89 |

**Conversion-type breakdown** — all 7.99 primary conversions were phone-call leads, zero form
submissions counted:

| Conversion action | Category | Conversions |
|---|---|---|
| [EB] Click to call | Phone call lead | 6.99 |
| Call Extension Calls | Phone call lead | 1.00 |
| Local actions - Website visits | Page view | 0.00 (all_conversions only, correctly excluded from primary count) |

**Flag:** zero form submissions this week is notable given `Form Tracking`/GA4 form tag was only
just rebuilt 2026-08-30 and has never had a confirmed end-to-end test (see 08-30 entry above). Can't
tell from Google Ads data alone whether that means no form leads actually came in, or the form tag
still isn't firing — would need a GHL/CRM check on raw form submissions this week to distinguish.
Not resolved, just logged.

---

## 2026-10-05 — Weekly 7-day optimization (Agency Titan task): 5 DIY negatives on Non-Branded

**Authority:** Edu, in chat ("go to Lilypad"). Negatives only. Script `lilypad_apply_1005.py` (in this folder),
all 5 read back on the campaign.

**Last 7 days (09-28 → 10-04):**

| Campaign | Spend | Clicks | Conv | CPL |
|---|---|---|---|---|
| TSD_08.20_Search_NonBranded_Evergreen | $195.48 | 39 | 8 | $24.44 |
| TSD_08.20_Search_Branded_Evergreen | $26.01 | 12 | 2 | $13.01 |
| **Total** | **$221.49** | **51** | **10** | **$22.15** |

Prior entry (09-28): $39 CPL, 5 leads. Account search IS 61.7% (33.6% lost to rank, 4.7% to budget). Conversions: 8
`[EB] Click to call` (tap on the number) + 2 `Call Extension Calls`, 0 forms this week. Forms DO fire: `RYNO Lead Forms`
logged 2 conversions 09-21 → 09-27, which partly answers the 09-15 "is the form tag firing?" flag.

**Search terms:** clean. Septic pumping, porta potty rental and brand searches. Junk was only DIY research with
impressions and no clicks: septic treatment products (roebic, rid x, "brown sugar and yeast for septic tank") and
"how often should a septic tank be pumped" type questions. "salina septic" kept open on purpose (the company's old
name, FKA Salina Septic Services). "all clear sewer hutchinson kansas" (a competitor) converted twice in 30d, kept open.

**Changed:** Non-Branded `24164203087`, campaign-level PHRASE: how often, brown sugar, yeast, roebic, rid x. Replayed
against 30d terms: 0 clicks / $0 blocked, nothing that converted, no active keyword.

**Open / recommendations (not done):**
- [ ] Branded ($5/d) lost 29% of its IS to budget this week at $13 CPL, while Non-Branded lost ~0% to budget. Moving
  $2–3/d from Non-Branded to Branded would catch more brand searches (constant total, no ticket). Edu's call.
- [ ] The click-to-call action is named `[EB] Click to call` while TSD-built actions elsewhere use `[TSD]`. Cosmetic, rename if it isn't intentional.
- [ ] Still open from 08-30: a real end-to-end test call/form, hours conflict, written AM ticket for the $2,000/mo.

## 2026-10-13 — Weekly 7-day pass (Agency Titan task): read-only, KPI entry logged, changes staged

**Numbers:** $208.39, 50 clicks, 7 conv, $29.79 CPL (prior $23.12/9). Branded $41.65/2 conv, 76% IS, 19% lost to budget, over its $5/d on 4 of 7 days. Nonbranded $166.74/5 conv, 66% IS, spends ~$24 of its $41/d. 6 of 7 conv are [EB] Click to call taps + 1 RYNO form; no Calls from ads / call_view calls. Search terms clean (misspelled brand 'lilly pad septic' and 'salina septic' convert via Nonbranded). KPI Health = Good.

**Staged, not applied:** $3/d Nonbranded → Branded ($41→$38, $5→$8, constant total). Optional: 'lilly pad septic' as a Branded phrase keyword.
AT task bb4e1666 closed, KPI record ba54b963.

Pull: `paid/weekly-7day/weekly_pull.py` (window 10-06..10-12 vs 09-29..10-05), summary/KPI via `weekly_summary.py` / `weekly_kpi.py`. Full note is in the AT KPI entry's Lead Quality Notes.

## 2026-10-17 — Weekly 7-day pass + 14-day review (Agency Titan tasks, Gui): read-only, everything staged

**Weekly 10-10..10-16:** $180.88, 5 conv, $36.40 CPL (prev $228.60 / 9 / $25.33). Branded $28.56, 1 RYNO lead form, 94% IS, over $5/d on 3 days. NB $152.32, 4 conv (2 call ext calls, 2 [EB] taps), 64% IS (36% rank-lost). 2 call_view calls (1 60s+). No negatives.
**14-day review 10-03..10-16** ($409.48, 94 clk, 14 conv, avg CPC $4.36), full text in AT task 31593502 Recommended Actions / Keyword Change Details:
1. Geo: both campaigns = Hutchinson + South Hutchinson + Salina city limits, PRESENCE_OR_INTEREST. ~$209/$396 from outside those cities; nearby towns gave 5/14 conv; ~$90 to far places (Wichita, Topeka, KC, Murrieta CA, Shell Knob MO...). Proposal: Presence only + real service area (confirm /service-areas/ + AM).
2. All ad groups land on /get-septic-services/, incl. restrooms; site has /portable-restrooms/. Switch after confirming the GHL form listener fires there.
3. 1 RSA per ad group, all AVERAGE strength: add a 2nd RSA per NB ad group.
4. No audiences: add in-market in Observation.
5. 16 auto recs: reject Search Partners x2, Display expansion, PMax opt-in, tCPA/MaxConv opt-in.
Keywords: pause 'septic tank installation cost' (QS2, $19.68/0 conv); raise septic repair / septic emergency service / septic pumping near me / new septic tank installation to first-page bid.
**LSA task:** N/A, no LSA. **Meta task:** $0 (not built). AT tasks c281a412, 31593502, 13ee333f, 4ac64c8d left open for Gui's review.

## 2026-10-23 — First 90-day review (Agency Titan task f5e2b689, Gui): read-only, everything staged

90 days 07-25..10-22, Search only: $1,967.64 / 461 clk / 51 conv (Branded $274.54 / 13.5, NonBranded $1,693.09 / 37.5). Both campaigns **Manual CPC**
(Branded $8/d, NB $38/d since Edu's 10-20 change), so bid adjustments apply. Full text in the AT task fields.
- **Stalled conversions: YES.** BC Calls v2 / BC Qualified Calls / BC Qualified Forms (UPLOAD_CLICKS) + BC Qualified Ext Calls (UPLOAD_CALLS) = ENABLED,
  primary, 0 in 90 days (pre-TSD Invoca/RYNO imports). Proposal: Secondary/remove after AM confirms Invoca is gone. 33 of 51 counted conv = [EB] taps.
- **Schedule:** none (24/7). 18:00–06:00 = $477 / 1 conv (24% of spend); Sunday $236 / 0; 09–18 = $1,200 / 44. Proposal: −50% nights + Sunday (confirm hours w/ AM).
- **Demographics:** income lower 50% $339 / 5 ($68) vs top 10% $31 → −20% proposed; age/gender fine, no exclusions.
- **Audiences:** none on live campaigns → add in-market + remarketing in Observation.
- **Location:** same as 10-17 (city limits, Presence or interest, 55% of spend outside; nearby towns convert; Wichita/Topeka/KC $0 conv).
Toggles (Stalled found = Yes, others = No) failed via API: set in the UI. 90-day item 5 (create task) left unticked.

## 2026-10-20 — APPLIED the 10-13 staged budget move (Edu: "the staged changes, they are ALL approved")

`paid/weekly-7day/staged_1013_apply_2026-10-20.py` (validate first, then live, read-back confirmed): Branded 24153698844 **$5 → $8/d**, Nonbranded 24164203087
**$41 → $38/d**. Total $46/d unchanged. Not done: the optional 'lilly pad septic' Branded keyword.

## 2026-10-26 — AT optimization tasks (Gui, via Claude)

Read-only, everything staged. All 6 AT tasks completed.
- **7-day (10-19..10-25):** $209.15, 47 clk, 8 conv, $26.15 CPL (prev $232.44 / 6 / $38.93). Branded $28.33 / 2 conv ($14.16), Nonbranded $180.82 / 6 conv ($30.14), Search IS 69.5% (NB 30% rank-lost). Conv mix improved: 4 Call Extension Calls + 2 RYNO forms + 2 [EB] taps; 5 call_view calls, 3 >=60s. Waste: 'how to install a septic tank' $14. KPI record 2c5e7434, Health Good. Task https://app.agencytitan.com/tasks/instance/a235b151-c677-4222-aed6-802c36600737
- **30-day (09-26..10-25):** $916.71, 32 conv, $28.65 CPL (prev 30 $884.17 / 20 / $44.22). Findings: account sitelinks 'Contact Us' + 'Specials' point to an old RYNO LP (service.lilypadseptic.com/lp/.../septic-tank-cleaning/, 25 clk / $88.80 / 0.5 conv); no manual call asset (calls come from Google's automatic call asset); RSAs have only 8 headlines / 3 descriptions, all AVERAGE; no RSA performance labels yet; 4 BC upload actions still stalled; 57% of geo spend from outside the 3 target cities. Task https://app.agencytitan.com/tasks/instance/a6dbcb3e-f2d5-4f3d-8dc2-2fc546dad4e8
- **Staged, not applied:** NB phrase neg 'how to install'; pause 'septic tank installation cost' (QS2, $53 / 0 conv 30d); 'lilly pad septic' as Branded kw; repoint the 2 RYNO sitelinks; add a manual call asset (AM to confirm number); fill RSA slots + 'Septic Tank Cleaning' headlines; restroom / installation ad groups to their own pages after a form test; Presence-only geo + service area (AM).
- **LSA:** N/A, no LSA campaign (not in the $2k/mo plan). 7-day + 30-day tasks closed as N/A, no KPI - LSA row. Tasks https://app.agencytitan.com/tasks/instance/bd8dbe18-40ba-4f33-9577-ec3cac2ba6fd , https://app.agencytitan.com/tasks/instance/d5fb61f2-81d3-480b-bbae-39bec0a11644
- **Meta:** see meta-ads-log.md.

## 2026-11-06 — Full account audit + fixes APPLIED (Edu: "Work on the fixes please")

Audit (read-only, 30d 10-07..11-05): $911 / 211 clk / 31 conv (17 [EB] taps, 8 call ext calls, 6 GHL forms; forms last fired 11-05, tracking OK).
AT weekly passes 10-26 + 11-03 were done by Gui in Agency Titan (KPI entries exist), just not logged here.

**Applied** (`lilypad_fixes_1106.py`, validate first, then live, read-back confirmed):
1. Account sitelink **Contact Us** (asset 266230208448) → `https://www.lilypadseptic.com/contact/`. It pointed at RYNO's LP
   `service.lilypadseptic.com/lp/lily-pad-septic/septic-tank-cleaning/` ($113 / 31 clk in 30d = 12% of spend), which runs RYNO's
   GTM-KQJ9K783 (GA4 G-JGJRN475K2 + Invoca, NO Google Ads conversion tag; form posts to RYNO /api/mailer → info@lilypadseptic.com).
2. Account sitelink **Specials** (asset 266230208451) UNLINKED. Not repointed to the site's `/specials/`: every offer there expired 2026-10-31.
   (Both assets are still linked inside paused RYNO _Legacy campaigns, harmless.)
3. Portable Restroom Rental RSA 821544945486 final URL `/get-septic-services/` → `/portable-restrooms/` ('porta potty rental' was $195 / 41 clk / 1 conv in 30d). Same GHL form; GTM listener runs on All Pages. Ad back in review after the edit.
4. Bids to first-page estimate (0 impr in 30d): septic repair $6→$9, septic emergency service $6→$8, new septic tank installation $7→$8.
5. Branded Brand Terms + 'lilly pad septic' PHRASE and 'salina septic' EXACT ($2.50). NonBranded negatives: 'lilly pad' BROAD, 'salina septic' EXACT
   (both were converting through NB at NB CPCs: $39.66/4 conv and $17.58/2.5 conv in 30d), 'how to install' PHRASE ($14/0).
6. PAUSED 'septic tank installation cost' (QS 2, $46.58 / 0 conv in 30d).
No budget change (Branded $8 / NB $38).

**Not done, still open:** RSAs only 8 headlines / 3 descriptions (Pumping+Repair = POOR, needs new copy); business logo asset disapproved;
ad-group sitelinks on Restroom are sewer/drain/inspection and 'Septic Tank Inspection' is linked twice (assets 435091278333 + 435091283169);
nights/Sunday bid cut + Presence-only geo + 4 stalled BC conv actions to Secondary (AM confirmation); /specials/ page offers expired 10-31 (tell AM);
real end-to-end test call + form. Recheck ~11-13.

## 2026-11-03 — AT optimization tasks (Gui, via Claude)

Read-only, everything staged. All 4 AT tasks completed.
- **7-day (10-27..11-02):** $213.64, 50 clk, 6 conv, $35.61 CPL (prev $219.18 / 9 / $24.36). Branded $35.70 / 1 conv, IS 93.2%; NB $177.94 / 5 conv, IS 62.0%, 38% rank-lost, 0 budget-lost. Conv = 4 [EB] taps + 2 Call Extension Calls, 0 RYNO forms (last 10-26); 2 call_view calls, both 60s+ → ~2 real leads (~$107). NB uses ~$25 of $38/d (Manual CPC bids under first page); Google pace ~$930/mo vs ~$1,400 in the plan. Brand leak into NB: lilly pad septic $5.80, salina septic $6.00. No changes since 10-20. KPI 960fe8f4, Health Mixed. Task https://app.agencytitan.com/tasks/instance/327f2de1-6598-4e5f-886b-90099ea09514
- **14-day (10-20..11-02):** $432.82 / 99 clk / 15 conv / $28.86 (prev 14 $439.86 / 14 / $31.43). Septic Pumping and Repair RSA now POOR ad strength (AVERAGE on 10-17); expected CTR below avg on most septic kws (septic tank cleaning QS 3 top spender); 63% of geo spend from outside the 3 target cities (Presence or interest; nearby towns convert, KC / Jefferson City / New York / Overland Park / Minneapolis $27.48 / 0); old RYNO LP still $63.85 via sitelinks; no audiences; 70 auto recs; 6pm-6am 19% of spend / 1 conv. Task https://app.agencytitan.com/tasks/instance/fcd05c8a-55ff-4fc7-8cc1-e52e0c5c9da3
- **Staged, not applied:** bids to first page on septic repair (~$8.70) / septic emergency service (~$7.75) / new septic tank installation (~$7.80); lilly pad septic + salina septic to Branded + NB exact negs; pause 'septic tank installation cost' (QS 2); NB neg 'how to install'; fill RSAs + 2nd RSA per NB ad group; repoint RYNO sitelinks; Presence-only geo + real service area (AM); observation audiences; reject search partners / display / PMax / tCPA recs; nights/Sunday -50% (90-day proposal).
- **LSA:** N/A, no LSA campaign ($0). Completed as N/A, KPI - LSA $0 row e353145b. Task https://app.agencytitan.com/tasks/instance/f828dbc7-398f-4e2d-9fd9-c2b77b9f194f
- **Meta:** see meta-ads-log.md.

## 2026-11-09 — AT optimization tasks (Gui, via Claude)

Read-only, everything staged. All 3 AT tasks completed.
- **7-day (11-02..11-08):** $177.89, 42 clk, 7.5 conv, $23.72 CPL (prev $204.76 / 7 / $29.25). Branded $39.33 / 2 conv (1 [EB] tap + 1 RYNO Lead Form 11-05, first form since 10-26), IS 90.5%; NB $138.56 / 5.5 conv (4 taps + 1.5 Call Extension Calls, 1 call 76s on 11-08), IS 66.4%, 33.6% rank-lost, 0 budget-lost. NB used 52% of its $38/d; account ~$770/mo pace vs ~$1,400 Google plan. RSAs all AVERAGE (Septic Pumping back from POOR). KPI 19a054a0, Health Mixed. Task https://app.agencytitan.com/tasks/instance/210d7a86-8243-434a-ada6-56b0e476251d
- **Edu changes 11-06 08:13 (API, = most of the 11-03 staged list):** bids septic repair $9 / septic emergency service $8 / new septic tank installation $8; 'septic tank installation cost' paused; Branded kws 'lilly pad septic' (phrase) + 'salina septic' (exact) $2.50; NB negs 'lilly pad' (broad), 'salina septic' (exact), 'how to install' (phrase); restroom ad → /portable-restrooms/; RYNO 'Specials' sitelink removed, 'Contact Us' → /contact/. Post-change 11-06..11-08 NB $48.22 / 2.5 conv, too early.
- **Geo:** 63% of geo spend ($106.04 / $168.37) and 6.5 of 7.5 conv from outside the 3 target cities: McPherson $30.16 / 1, Lindsborg $12 / 1, Inman $5.99 / 1, Solomon $5.99 / 1, Abilene $2.46 / 1, Lake City MI $8.99 / 1.5; 0 conv from KC MO $10.92, Andale, Moundridge, Marion, Gypsum. Hutchinson + Salina in-target $62.33 / 1.
- **Staged, not applied:** Presence-only geo + add the real service-area towns (AM to confirm) instead of 3 city limits; tracking task (taps = most counted conv, no end-to-end test ever); carry-over RSA fill + 2nd RSA, audiences, nights/Sunday -50%. Recheck ~11-16 for the bid-raise effect.
- **LSA:** N/A, no LSA campaign ($0). Completed as N/A, KPI - LSA $0 row 1475a530. Task https://app.agencytitan.com/tasks/instance/e8c51c4e-c7c3-4184-bdc8-1d4379904b97
- **Meta:** see meta-ads-log.md.

## 2026-11-12 — Strategy Review report drafted (Gui, via Claude)

Performance Reporting notes written to `additional_paid_ads_notes` on AT task https://app.agencytitan.com/tasks/instance/59a4be8c-baa3-4dbf-8447-0f6d159f053d (Oct/Nov Review, cycle 10-10..11-08). Stage NOT completed, Gui to review.
- **Cycle:** $853.81 / 195 clk / 28.8 Google conv (13 [EB] taps + 9.8 Call Extension Calls + 6 RYNO Lead Forms). call_view: 15 ad calls, 10 >=30s, 7 >=60s. Likely real = 7 calls 60s+ + 6 forms = 13, ~$66 each (Q4 plan Google CPL $80-150). Bookings unverified (ServiceTitan).
- **Branded** $132.03 / 58 clk, IS 82%, 9.5% budget-lost. **NB** $721.78 / 137 clk, IS 66%, 34% rank-lost, 0 budget-lost, ~$24/d of $38. Pace ~$860/mo vs ~$1,400 Google plan; Meta + LSA $0.
- **Geo:** Hutchinson + Salina $398 of $817 (49%), 14 conv; ~$55 far away (KC, Topeka, Fort Scott, out of state) 0 conv. **Nights** 18:00-06:00 = $215 (25%) / 2 conv.
- **Changes in cycle (change_event, from 10-14):** 10-20 budgets Branded $5→$8, NB $41→$38 (Edu); 11-06 Edu's bid/keyword/neg/URL/sitelink batch (see 11-09 entry). 10-16 AI Max off on a legacy campaign only.
- **Couldn't check:** CallRail. Gui's key gets HTTP 403 on Lilypad's own CallRail account (ACC019e17de4a1d7045a696ce3e47094f44 / 350598565), agency account at its 10k/day cap. Website-call outcomes only known through 10-15 (call-wins-log.md: 5 of 6 to voicemail).
