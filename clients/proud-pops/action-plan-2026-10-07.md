# Proud Pops — Action Plan (2026-10-07)

> Superseded the same day by two split plans: `internal-action-plan-2026-10-07.md` (our account work) and
> `am-client-action-plan-2026-10-07.md` (AM and client items). Kept for the full background.

Google Ads 1051843378 · GTM-WBFDB6L8 (account 6255217830, container 198527160) · GA4 438523825

## Why this plan exists

Three measurement problems are distorting every number on this account:

1. **About 3 in 4 "form leads" are job applications.** The `/careers` page embeds a GHL job application
   form (`ThmcYYHImwSoYS9oBt3n`). Its submit fires the same `ghl_form_submit` event as the customer form,
   so it counts as `Website lead` in Google Ads, `generate_lead` in GA4, and fires the Meta lead tag.
   GA4, Sep 7–Oct 6, Google Ads traffic: 99 job applications vs 32 customer forms. Both PMax campaigns
   have Final URL expansion on, and PMax Electrical sent 176 sessions straight to /careers.
2. **Phone-link taps are bid on as leads.** `TSD - Website Call` (a `tel:` link click) is 88% of
   reported conversions. PMax HVAC has spent 100% on Display since Aug 24 buying these taps.
3. **No confirmed calls reach Google Ads.** The call asset (210-794-7570) is disapproved, and CallRail
   is not connected to Ads. LSA, the only confirmed-call source, fell from 88 calls in June to 2 in Oct 1–6.

Real cost per customer form, last 30 days: **~$1,115** ($53,355 lead-gen spend, ~48 customer forms),
not the $296 Google shows.

| Sep 7–Oct 6 | Spend | Ads forms | GA4 job apps | GA4 customer | Est. customer forms | $/customer form |
|---|---:|---:|---:|---:|---:|---:|
| Search Electrical | $18,569 | 35 | 9 | 10 | ~18 | ~$1,010 |
| Search HVAC | $11,001 | 15 | 2 | 8 | ~12 | ~$920 |
| PMax HVAC | $9,814 | 2 | 0 | 2 | 2 | ~$4,900 |
| PMax Electrical | $6,735 | 103 | 79 | 2 | ~3 | ~$2,650 |
| Search Plumbing | $5,130 | 9 | 3 | 5 | ~6 | ~$910 |
| Branded | $2,106 | 16 | 6 | 5 | ~7 | ~$290 |
| **Total** | **$53,355** | **180** | **99** | **32** | **~48** | **~$1,115** |

**Order matters.** Fix the job application tracking first. If phone taps stop counting before that,
form leads become the only bidding signal and PMax chases job seekers even harder.

## Timeline at a glance

| When | Phase | Owner |
|---|---|---|
| Oct 7 | 0. Agency Titan ticket + client heads-up | Edu → AM (Jonathan) |
| Oct 7–8 | 1. GTM: remove job applications from lead tags | Paid (Claude drafts, Edu approves publish) |
| Oct 8 | 2. PMax: exclude /careers + job-seeker negatives | Edu (UI) |
| Oct 8–9 | 5. LSA dashboard check (all 3 profiles) | Edu or client, via AM |
| Oct 8–16 | 4. Real call tracking (call asset + CallRail) | Edu + client, via AM |
| Oct 9–12 | 1. Verify the GTM fix live (3 clean days) | Paid |
| Oct 12–13 | 3. Bidding: phone taps to secondary, pause PMax HVAC | Edu (UI), after AM approval |
| Oct 13–30 | 6. Search efficiency work (budget-neutral) | Paid |
| Oct 26 | 7. Re-baseline on real leads | Paid |
| Oct 27–30 | 8. November budget decision | Edu + AM + client |

---

## Phase 0 — Ticket and heads-up (Oct 7)

One Agency Titan ticket through the AM, covering:

- The GTM fix, and that 2 test submissions will land in GHL (one job application, one booking), named
  `TSD TEST - please delete`. The client should know before a test applicant hits their hiring pipeline.
- That reported conversions in Google Ads will drop sharply after Phase 1 and Phase 3. This is the
  count getting honest, not performance falling.
- Pausing PMax HVAC (spend change: brings the monthly pace from ~$59.8k back to ~$50k).
- Getting September/October budget approval on record. The last written approval is $50k for August.
- Asks for the client: CallRail account access (or who owns it), and LSA dashboard access if TSD
  doesn't have it.

## Phase 1 — Remove the job application form from the lead trigger and tags (Oct 7–8)

**Where:** Default Workspace 43 (the only workspace). Live version is v41.

**What fires on job applications today:** trigger `[80] cEvent - Lead` (custom event `ghl_form_submit`)
feeds four tags:

| Tag | What it sends |
|---|---|
| `[82] 05 \| G.Ads - Lead` | Google Ads `Website lead` (label u5lXCI2jk7kYEKrcxssp) |
| `[90] 05 \| GA4 - Lead` | GA4 `generate_lead` |
| `[94] 05 \| G.Ads - User-provided Data` | Enhanced conversions user data |
| `[111] 05 \| Meta - Lead` | Meta pixel (currently sends PageView, see side findings) |

Fixing the trigger fixes all four at once.

### Change A — exclude /careers on trigger [80]

Edit `[80] cEvent - Lead`. Keep `{{_event}} equals ghl_form_submit`, and change it to fire on
**Some Custom Events** with:

- `{{Page Path}}` **does not contain** `/careers`

Page Path is the right key. GA4 already records these events with `page_location = /careers` from the same
`{{Page URL}}` built-in, so the variable resolves correctly at submit time on this React site.

### Change B — form-ID guard on trigger [80]

Covers the case where someone later embeds the job form on another page.

- New variable `dlv - ghl_form_id` (Data Layer Variable, name `ghl_form_id`, version 2).
- Add a second condition to `[80]`: `{{dlv - ghl_form_id}}` **does not equal** `ThmcYYHImwSoYS9oBt3n`.

When the form ID is missing (listener `[99]` doesn't send one), the condition still passes, so customer
forms are never blocked by this guard.

`[73] cEvent - Appointment Scheduled` stays as is. The job form shouldn't emit that event. Confirm in Preview.

### Change C — job applications get their own event

- New trigger `cEvent - Job Application`: custom event `ghl_form_submit`, Some Custom Events,
  `{{Page Path}}` contains `/careers`.
- New tag `06 | GA4 - Job Application`: GA4 event `job_application`, parameter `page_location = {{Page URL}}`,
  measurement ID `{{GA4 Measurement ID}}`, firing on the trigger above.
- **No Google Ads tag and no Meta lead tag** for job applications. Keep them out of every ad platform's
  bidding signal. The client still gets visibility in GA4.

### What NOT to touch in this change

- The two form listeners, `[99] 00 | cHTML - GHL Form Listener` and `[123] 00 | cHTML - Listener`. Both
  push `ghl_form_submit`. The `dlv - Email/Phone/First Name...` variables read the flat keys only `[99]`
  pushes, so removing `[99]` would break enhanced conversions and Meta advanced matching. Duplicates are
  small (GA4: 131 events / 124 sessions on /careers) and Google Ads counts one per click. Cleanup is a
  separate item.

### Preview test (before publishing)

1. Start GTM Preview on proudpops.com.
2. Go to `/careers` and submit a test application (`TSD TEST - please delete`).
   - Expected: `cEvent - Job Application` fires → `06 | GA4 - Job Application` fires.
   - Expected NOT to fire: `05 | G.Ads - Lead`, `05 | GA4 - Lead`, `05 | G.Ads - User-provided Data`, `05 | Meta - Lead`.
   - Record the `ghl_form_id` in the dataLayer push. It should be `ThmcYYHImwSoYS9oBt3n`.
3. Go to the HVAC page, click through to `/schedule` (in-app navigation, not a fresh load), and submit a
   test booking.
   - Expected: `05 | G.Ads - Lead` and `05 | GA4 - Lead` fire once each. Job Application does not.
   - Record the schedule form's `ghl_form_id` for the log.
4. Repeat step 3 starting from the homepage, the Electrical/Plumbing landing route.
5. Note: Preview traffic shows up in GA4 as `tagassistant.google.com / referral`. Exclude it from readouts.

### Publish

- Version name: `TSD - Exclude careers job applications from lead conversions (2026-10-0X)`.
- Only one workspace exists, so there's no side-workspace sync step. Re-list workspaces after publishing and
  confirm the live version is the new one.

### Verify live (Oct 9–12)

- GA4: `generate_lead` with pagePath `/careers` = 0 from publish time; `job_application` events appear.
- Google Ads: `Website lead` all_conversions falls to roughly a quarter of the prior daily rate
  (~6/day → ~1.5/day). PMax Electrical drops the most (~3.4/day → near 0). This is expected.
- If job applications still show as `generate_lead`, check whether the form fires from a different path
  (for example a modal on another route) and extend the exclusion.

## Phase 2 — Stop PMax sending traffic to /careers (Oct 8)

- Both PMax campaigns: Settings → Final URL expansion → **URL exclusions** → add `proudpops.com/careers`.
  Do it on PMax HVAC too, so it's clean if it's ever re-enabled.
- Account-level negative keywords (these also apply to PMax search traffic): `jobs`, `job`, `hiring`,
  `careers`, `career`, `apprentice`, `apprenticeship`, `salary`, `employment`, `indeed`. Job-seeker
  search terms on Search are small today ($15 in 30 days), so this is cheap insurance, not a big saving.

## Phase 3 — Fix the bidding signal (Oct 12–13, only after Phase 1 is verified)

1. **Set `TSD - Website Call` to Secondary** in the UI (Goals → the phone call lead goal → set this action to
   secondary). Do NOT switch off the whole PHONE_CALL_LEAD / CALL_FROM_ADS goal. `Calls from ads` sits in
   the same goal, and once the call asset is approved (Phase 4) it becomes the real call signal.
   - Verify via API the next day: `TSD - Website Call` should show all_conversions > 0 but conversions = 0.
     The API-side primary_for_goal flip has silently done nothing on another account, so trust only the
     read-back.
   - Fallback if it doesn't take: switch the goal to non-biddable per campaign and accept losing
     `Calls from ads` until CallRail import is live.
2. **Remove the $265 target CPA on Search HVAC** the same day. On customer forms only (~$920 each), that
   target would choke delivery to near zero.
3. **Pause PMax HVAC** once the AM ticket is approved. It's ~$9.8k/month of Display phone taps with 2
   customer forms in 30 days. Its August "44 forms" were job applications too (GA4: 41 of 42).
4. **PMax Electrical:** keep it live for 2 weeks on the clean signal. If it produces fewer than 5 customer
   forms on ~$3k spend by Oct 26, pause it until call import exists.
5. Tell the AM before the flip: the Conversions column goes from ~1,376/30 days to ~50. Compare everything
   on all_conversions split by action from here on.

What the clean signal looks like (30-day estimate): Search Electrical ~18, Search HVAC ~12, Branded ~7,
Plumbing ~6, PMax Electrical ~3. That's thin for Smart Bidding, which is why Phase 4 matters.

## Phase 4 — Get real calls into Google Ads (Oct 8–16)

1. **Call asset.** Create a call asset with the site's real number, 210-225-5767. Submit it for
   verification (the client may need to answer a verification call), attach it at account level and on all
   6 lead campaigns, and remove the disapproved 210-794-7570. Set `Calls from ads` to a 60-second minimum.
2. **CallRail → Google Ads.** CallRail already swaps numbers on every page (tag `[104]`). Connect its
   Google Ads integration so qualified calls from ad visitors (first-time, 60 seconds or more) import as a
   primary PHONE_CALL_LEAD conversion. This is the real replacement for the `tel:` tap. Needs client access.
3. After 2 weeks of call data: true CPL = spend / (customer forms + qualified calls), per campaign.

## Phase 5 — LSA recovery (Oct 8–9)

LSA was the cheapest confirmed source: 88 calls on $6,793 in June (~$77/call). Getting it back is worth
more than any PPC change.

Check all 3 profiles (in-account, 7261668241, 6621969129) in the LSA dashboard:

- Profile active vs paused, weekly budget
- Job types and service areas switched on
- Business hours / ad schedule
- Verification: license, insurance, background checks, and expiry dates
- Reviews (count and rating) and responsiveness (missed calls)
- Lead disputes

What the data shows: weekly impressions ~1,900 combined in late July → near zero now; 6621969129 has had no
impressions since mid-September. In September, 7 of 22 leads were marked declined and 10 of 21 calls weren't
charged. All 3 campaigns read enabled and eligible in Google Ads with no changes, so the cause is on the LSA side.

## Phase 6 — Search efficiency, budget-neutral (Oct 13–30)

- **Landing pages:** point Electrical and Plumbing Search at `/services/electrical` and `/services/plumbing`.
  Only HVAC has its own page today. Open since July.
- **Competitor negatives** on Plumbing (Beyer Boys, The Bearded Plumber, George's Plumbing, Bryco), from
  the Sep 14 search-term report.
- **Geo:** HVAC and Plumbing still target San Antonio only, vs LSA's 47 cities.
- **Ad Rank:** Search CPCs average $29 and 49–61% of impressions are lost to rank. Expected CTR was Below
  Average on every Plumbing keyword in July. RSA and landing page work is the lever, not budget.
- **Branded** is the cheapest real lead source in PPC (~$290 per customer form) and loses 25% of
  impressions to budget. Candidate for a raise once there's approval on record.

## Phase 7 — Reporting and re-baseline

- **September report:** customer forms only (job applications excluded), and phone-link taps never
  labeled as calls.
- **August report (sent Sep 3):** it stated 129 form leads at $256 and called PMax the strongest cost per
  lead. GA4 shows ~79% of August's ad-driven forms were job applications (104 of 132), so the real figure was
  closer to ~27 customer forms. It also called 1,069 phone-link taps "calls to your business line".
  Recommendation: restate August next to September in the September report. These numbers sat behind the
  $50k decision, and it's better coming from us than the client finding it in GA4. Edu and the AM decide
  the framing.
- **Re-baseline Oct 26:** per campaign: spend, customer forms, `Calls from ads` (if live), CallRail calls
  (if live), LSA calls. That's the first honest CPL this account has had since July.

## Phase 8 — November budget decision (Oct 27–30)

Decide from the Oct 26 re-baseline, not from Google's reported conversions. Proposed framing (benchmarks
put non-branded Search at ~$150–183 per lead including calls):

- **True CPL within ~2x of benchmark:** hold ~$50k, shift budget toward what's proven (Branded, the best
  Search campaign, LSA).
- **Above that:** cut to Branded + the best Search campaign + LSA while Ad Rank and landing page work lands.
- No budget increase on any campaign before this point.

## Side findings (low priority, not part of Phase 1)

- `[111] 05 | Meta - Lead` sends **PageView**, not Lead (`standardEventName = PageView`). If Proud Pops runs
  or plans Meta ads, Meta has never received a lead event from the site. Fix to Lead after Phase 1, so it
  inherits the careers exclusion.
- The two GHL listeners `[99]` and `[123]` both push `ghl_form_submit`. Later: keep `[123]` (it has form ID),
  remap the `dlv` variables to `ghl_data.*`, then remove `[99]`. Test enhanced conversions after.
- As of Jul 30, GA4's only key event was `instant_quote_hvac_click` (a button click), and `generate_lead`
  wasn't a key event. Recheck; after Phase 1, mark `generate_lead` as the key event.

## Don't

- Don't flip phone taps to secondary before Phase 1 is verified live.
- Don't enable or un-hide other conversion actions to "replace" lost volume.
- Don't raise any budget before the Oct 26 re-baseline.
