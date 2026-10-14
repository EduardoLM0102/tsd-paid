# Neon Monkey: Action Plan (2026-10-08)

Google Ads PPC `7953905280` · LSA `1219885876` · GA4 `328458299` (G-WF5DBMQ644) · site neonmonkeytree.com
AM: Angela · Owner: Brock · Background: `account-check-2026-10-08.md`, `geo-targeting-review-2026-07-20.md`

## Why this plan exists

Cost per lead has climbed while lead count fell. Last 7 days: $1,941, 5 leads, **$388 CPL**. Last 30 days:
$8,430, 32 leads, $263 CPL. Four problems are behind it, in this order of importance:

1. **The website lost its Google tag around Aug 29–31.** GA4 sessions on neonmonkeytree.com went from
   75 on Aug 28 to 2 on Aug 31, and from 1,458 in August to 12 in September. No gtag, GTM or Google Ads tag is
   in the homepage or /contact/ HTML today. Three conversion actions went to zero in September at the same
   time: `contact_us` (62 → 0), `Submit lead form - web` (3 → 0), and the `Phone Call` offline upload (10 → 0).
   Calls from people who land on the site and then dial were never tracked. Google Ads now sees only
   **Calls from ads** (call asset) and the server-side GA4 `ghl_contact_us` event.
2. **Nonbranded Search is overpaying per click.** It bids on uncapped Maximize Conversions with ~3 leads a
   week of signal. Weekly CPC went from $19–22 in August to $29–34 since mid-September; clicks fell from ~50
   to ~32 a week at the same ~$1,050 a week. That lines up with the signal loss in point 1.
3. **Spend is going to the wrong searches and places.**
   - Search terms on Nonbranded, 30 days (~$2,725 of the spend Google shows terms for): competitor tree
     companies ~$694 (2 conv), lawn and landscaping companies ~$861 (much of it before the 09-28 lawn
     negative), "tree trimming dallas" $210 for one click.
   - PMax is still on Presence OR Interest: **$2,286 of its $3,278 (70%)** in 30 days went to people outside
     the target areas. Dallas alone: $533, 0 conversions, nearly all of it PMax.
4. **LSA, the cheapest source, is shrinking.** ~$75 per lead over 30 days (27 leads, 11 booked) vs $263 on
   PPC. Weekly spend fell from ~$600 (July to mid-August) to ~$105–250, with the same $214/day budget,
   eligible status, and no changes in 30 days. The cause is on the LSA profile side.

On top of that, **spend is above the cap on record**: September PPC came in at $8,356 vs the $6,930/month cap
in the 08-10 log, and October is pacing ~$9.5–10k. Nonbranded's budget is $150/day (was $100 on 08-10); that
change is older than the 30-day change history, so who made it isn't visible.

| Last 30 days | Spend | Leads | CPL | Note |
|---|---:|---:|---:|---|
| Nonbranded Search | $4,604 | 15 | $307 | $29.51 avg CPC |
| PMax | $3,278 | 16 | $205 | 70% of spend outside target areas |
| Branded Search | $549 | 1 | $549 | $22.86 per brand click at ~100% IS |
| **PPC total** | **$8,430** | **32** | **$263** | |
| LSA (separate account) | $898 | 12 | $75 | 27 leads, 11 booked |

**Correction to the open geo ticket:** both Search campaigns already target a 36-location West Fort Worth
list (Aledo, Azle, Benbrook, White Settlement, Westworth Village, Willow Park, Hudson Oaks, Lake Worth,
Saginaw and others, plus 21 FW ZIPs), Presence only. That was applied before Sept 9. If the list came from
Brock, the geo ticket is unblocked for PMax and LSA. Confirm with Angela (Phase 0).

## Timeline at a glance

| When | Phase | Owner |
|---|---|---|
| Oct 9 | 0. Agency Titan tickets: Web Dev (site tag) + Angela (budget, LSA, geo list, holiday lighting) | Edu → Web Dev, AM |
| Oct 9 | 2. Account hygiene: negatives, wrong callout, asset cleanup | Edu |
| Oct 9–16 | 1. Restore site tracking + website call tracking | Web Dev (tag install) + Edu (tag config) |
| Oct 12 | 3. Bidding: Nonbranded to capped Max Clicks, Branded to Manual CPC | Edu |
| Oct 13 | 4. PMax geo: Presence only, then the Search location list | Edu |
| Oct 9–16 | 5. LSA dashboard review + disputes | Edu or client, via AM |
| Oct 15 | 7. Holiday lighting / leaf cleanup go or no-go | Brock, via AM |
| Oct 19 | Check-in: CPC, search terms, PMax geo, tracking | Edu |
| Oct 19–Nov 6 | 6. Ads and landing pages (CTR + LP rollout) | Edu |
| Nov 2 | 8. Re-baseline on restored tracking + November budget | Edu + AM + client |

---

## Phase 0: Tickets (Oct 9)

**Ticket A, to Web Dev (Justin):** the fix is on the site, so it routes to Web Dev, not through the client.

- The Google tag (GA4 `G-WF5DBMQ644`) dropped off neonmonkeytree.com around Aug 29–31. A staging copy exists
  (neonmonkeytreestaging.mystagingwebsite.com), so it looks like a site update went live without the tags.
- Ask: install a GTM container TSD can edit (Paid configures GA4 + Google Ads inside it), and keep it in the
  site template so the next update doesn't drop it again.
- If Web Dev doesn't manage this site, then it becomes a client question for Angela: who can add the tag.

**Ticket B, to Angela (AM):**

1. **Phone numbers.** The site shows toll-free numbers (800-315-2374 site-wide, 866-318-9768 on the
   homepage, 866-395-5395 and 866-944-2057 on /contact/). The ads use (817) 409-8954. What are the toll-free
   numbers (call tracking, answering service, another vendor)? This decides how we track website calls.
2. **Budget on record.** September PPC: $8,356 against the $6,930/month cap we have documented. Either
   confirm the higher number in writing or we bring spend back under the cap (options in Phase 8).
3. **Geo list.** Did Brock send the West Fort Worth list that's now on the Search campaigns? If yes, we
   apply it to PMax and LSA. If not, we still need: yes list, no list, shop address or max radius.
4. **LSA.** LSA leads cost ~$75 vs ~$263 on Google Search, but LSA volume has dropped by more than half
   since mid-August at the same budget. Ask: who answers LSA calls, are hours current, any change to the
   profile in August, and why 15 of 27 recent leads were declined.
5. **Holiday lighting and leaf cleanup.** Does Neon Monkey offer them this season, with crew capacity? Both
   campaigns exist and are paused. Holiday lighting has to launch by mid-October to catch booking season.

Suggested wording for the client part (plain, no internal detail):

> We found that your website's Google tracking stopped working around the end of August, likely during a
> site update. Since then Google Ads can only see calls that come straight from the ads, not calls or forms
> from people who visit the site first. Our team is putting it back this week. One question for you: what
> are the 800 and 866 numbers on the website used for?

## Phase 1: Restore tracking (Oct 9–16)

Order matters: tracking first, then judge bidding and CPL on real numbers.

> **Status 2026-10-13:** step 1 DONE (tag back ~9am CT, GTM v11 live). Watch step 4: v11 added a primary,
> biddable phone-tap action (`[TSD] Click to call`). See `tracking-restored-2026-10-13.md`.

1. **Put the tag back.** Web Dev installs a GTM container on neonmonkeytree.com (the site has none, per the
   10-08 LP inventory). Paid sets up GA4 `G-WF5DBMQ644` and the Google Ads conversion linker + tag inside it.
   Publish only after Edu approves.
2. **Website call tracking.** Depends on Ticket B item 1 (phone numbers):
   - If the toll-free numbers are a call tracking vendor: connect that vendor to Google Ads (qualified calls,
     60s+), same pattern as the CallRail fix on Proud Pops.
   - If not: turn on Google forwarding numbers on the site via the existing `NMS Website Calls` action
     (WEBSITE_CALL, 45s). It has never recorded a call because the tag piece was never live.
3. **Form leads.** GA4 already receives `ghl_contact_us` and `ghl_request_estimate` server-side (hostname
   "(not set)", likely GHL). `ghl_contact_us` is imported; **`ghl_request_estimate` is not.** Import it as
   a primary lead. Confirm in a test submission which GHL forms fire which event (route the test via AM; GHL
   changes go through Mo).
4. **Conversion action cleanup.** 21 actions are enabled and most are primary but have never fired since
   April. Keep primary: `Calls from ads`, website calls (from step 2), `ghl_contact_us`,
   `ghl_request_estimate`. Set to secondary: `phone_link_click`, `mailto_link_click`, `book_now_link_click`,
   `about_us`, `contact_us`, all `Local actions` / Smart campaign actions. Taps are not calls (Proud Pops
   lesson): if the tag comes back with a phone tap action primary, it will flood the Conversions column.
5. **`Phone Call` offline upload** (UPLOAD_CLICKS, 36 in June, 0 since September). It stopped with the site
   tag, which fits a CRM import that relies on a gclid captured on the site. Find out who set it up (likely
   GHL) and whether it resumes once the tag is back.
6. **Verify (Oct 16–19):** GA4 sessions on neonmonkeytree.com back to ~40–80/day, the Google Ads tag shows
   active, one test form and one test call recorded, Conversions column only shows real leads.

## Phase 2: Account hygiene, no approval needed (Oct 9)

1. **Negatives on Nonbranded (phrase):**
   - Competitors from the 30-day terms: wise tree, maverick tree, jc tree, h2h tree, integrity tree, mercer
     tree, arbor masters, chippers, trevino, j davis, legacy tree, brown tree, trinity forest, tenorio,
     matt tree, blue ox, fowlkes. Two of these converted (wise, maverick), likely people calling the wrong
     company; still exclude, since there is no competitor strategy on this account.
   - Lawn/landscaping not caught by "lawn": landscaping, landscape, trugreen, yard cutting, yard service.
   - Out of area: dallas, plus the hard no list once confirmed (grand prairie, arlington, irving).
   - Off-service: planting, plant removal, stump grinder rental, rental.
2. **Reuse the old shared list carefully.** `CSMS_Negatives` (477 terms) is attached only to 3 paused
   campaigns. Don't attach it as is: it blocks real tree work for a tree company: `pine`, `pruning crape
   myrtle`, `trim crape myrtle`, `trimming crepe myrtles`, `pruning crape myrtle trees`, `pruning mature
   pecan trees`, `pruning evergreen tree`, `trimming peach trees`, `bush`, and `tree service 76116` (a
   target ZIP). Copy it to a new `NMS - Core Negatives` list without those, and attach to Nonbranded only.
   `reviews` and `free` in it would hurt Branded.
3. **Remove the "Free Pump Inspections" callout** from Nonbranded. It's from a septic or plumbing client.
   Also remove "Click and Call" and "Call Now" (wasted callout slots) and the account-level "Landscape
   Cleanups" callout (invites landscaping intent).
4. Fix or remove the "Plant Health Care" sitelink (NOT_ELIGIBLE) and de-duplicate Branded's callouts and
   sitelinks (16 callouts and 8 sitelinks, each set listed twice).
5. Verify the 09-28 lawn fix keeps holding (0 "lawn" terms since 09-29 so far).

## Phase 3: Bidding (Oct 12)

Doesn't depend on tracking, because neither strategy below uses the conversion signal.

1. **Nonbranded Trimming → Maximize Clicks, max CPC $20.** Keep the $150/day budget for now (budget is a
   Phase 0 / Phase 8 decision). At ~$20 instead of ~$30 per click, the same spend buys ~50% more clicks. In
   August, at $19–22 CPC, the campaign showed ~50 clicks a week.
   - Watch: impression share at the top of page, and whether close-variant junk rises with cheaper clicks
     (Phase 2 negatives should cover it).
   - Rule: on Oct 26, compare calls + forms per $1,000 vs the 30 days before. Move back to Max Conversions
     (with a target CPA) only once tracking is restored and the campaign has ~30 real leads in 30 days.
2. **Branded → Manual CPC, $5 max** (or Target Impression Share, absolute top 90%, $6 cap). Branded shows
   for ~40 searches a week at ~100% IS and pays $22.86 per click on average (30 days). Expected: brand spend falls from ~$550 to
   ~$100–150 a month with no loss in coverage. If IS drops below 90%, raise the cap in $1 steps.

## Phase 4: PMax geo (Oct 13)

1. **Switch positive geo to Presence only** now. This doesn't need Brock's list and it is the biggest
   single waste: 70% of PMax spend reaches people outside the targets. Expect PMax volume and reported
   conversions to drop (12 of its 16 conversions in 30 days came from outside-target users); that's what
   Brock asked for, but tell Angela before it happens.
2. **Replace the 5 radius circles + Fort Worth city** with the Search campaigns' West FW list once Ticket B
   item 3 confirms it. Today PMax has a 20 mi circle centered SE of Fort Worth (reaches Grand Prairie and
   Dallas County), plus 5 mi circles at Grapevine, Keller and Joshua.
3. Add the same location exclusions as Search (Dallas, Grand Prairie, Arlington, Irving) as a backstop.
4. Copy the Phase 2 competitor/landscaping negatives into PMax's own campaign negatives (60 today). Final URL
   expansion and brand exclusions: check in the UI; the API didn't expose them on this account.

## Phase 5: LSA (Oct 9–16)

In the LSA dashboard (Edu, or the client via Angela if TSD lacks access):

- Budget mode and weekly budget (the Google Ads side shows $214/day, spending ~$30/day over 30 days)
- Business hours, job types, service areas (still whole Tarrant + Johnson County, Grand Prairie and ZIP
  75249 as of July)
- Verification status (license, insurance, background checks) and expiry dates
- Reviews: count, rating, recent ones. Responsiveness: missed calls, answer rate
- The two $0 weeks (Aug 17 and Aug 31) with clicks recorded: was the profile paused?
- **Dispute** the 3 leads marked declined but still charged, if out of area or spam

Then apply the West FW geo to LSA (drop the counties, Grand Prairie, 75249) once the list is confirmed. LSA
is not budget-limited, so don't raise its budget; raise its ranking.

## Phase 6: Ads and landing pages (Oct 19–Nov 6)

1. **Expected CTR is Below Average on every Nonbranded keyword** with data (ad relevance and landing page are
   mostly Average/Above). The fix is ad copy, not bids. Write a new RSA per ad group with West Fort Worth
   area names and real offers. Check every claim on neonmonkeytree.com first (certified arborists, free
   estimates, insured, years in business). New ads are added next to the current ones, not edited in place,
   since each ad group has a single ad (Proud Pops lesson: editing sends it back to review).
2. **Landing pages.** Every ad goes to the homepage. Neon Monkey is #4 in the 10-08 LP rollout ($9,195 web-ad
   spend): Tree Trimming ($3,254), Stump Removal ($1,350), Tree Service for PMax ($3,278). Build on the go.
   subdomain with the local number and the tag from day one.
3. Nonbranded runs 24/7 with no schedule; PMax runs Mon–Sat 6am–9pm. Revisit an hour-of-day schedule for
   Search after 30 days of restored call data, not before.

## Phase 7: Seasonal services (decision by Oct 15)

- **Holiday Lighting** (`18787352551`, paused): 52 keywords ready. It didn't run last season (no
  impressions Aug 2025–Jan 2026). 2 of its 4 enabled ads are disapproved and the approved RSA points to the old
  domain neonmonkeyservices.com (redirects to neonmonkeytree.com). If Brock says yes: new RSAs with a
  holiday lighting page, West FW geo, Presence only, its own budget from Oct ~20 to Dec ~10, written
  approval for the added spend.
- **Leaf Cleanup** (`19146431184`, paused): 21 keywords, also didn't run last season. Leaf cleanup sits
  next to the lawn and landscaping searches Brock complained about. Only relaunch if he wants it, with the
  lawn negatives kept.
- Neither goes live before Phase 1 tracking is verified.

## Phase 8: Re-baseline and November budget (Nov 2)

- Per campaign, Oct 19–Nov 1: spend, calls from ads, website calls, forms (contact + estimate), LSA leads
  and booked jobs. That's the first clean CPL since August.
- Budget options for Angela, if the $6,930 cap stands:
  - **Hold the cap:** Nonbranded $150 → $100/day, PMax $110/day, Branded on the $5 cap ≈ $6.4–6.6k/month.
  - **Confirm a higher number in writing** if Brock wants the current ~$9–10k pace, and put the extra into
    whichever campaign has the best clean CPL on Nov 2.
  - LSA gets more only once its ranking recovers; until then extra budget there doesn't spend.
- Holiday lighting spend (if approved) is separate and time-boxed.

## Side findings (low priority)

- PMax returned no biddable campaign-level conversion goals via the API, yet it reports conversions. Check
  in the UI which goals it bids on (it may use a custom goal) before Phase 1 step 4.
- GA4 also receives a server-side `phone_call` event (251 in June, 143 July, 141 August, 170 September). It
  looks like all inbound calls from GHL, not just ad calls. Total inbound calls didn't collapse in
  September. Confirm the source before quoting it to anyone.
- Meta account `705877631084699` spent ~$765 in 30 days. Scope still unconfirmed (Command Center flag).
- No weekly Agency Titan 7-day task exists for this client; requested in tarefas.md.

## Don't

- Don't judge CPL or switch Nonbranded back to Max Conversions before tracking is restored and verified.
- Don't make phone-link taps a primary conversion when the tag comes back.
- Don't attach `CSMS_Negatives` unedited.
- Don't change any budget before Ticket B item 2 (budget) is answered in writing.
- Don't launch the seasonal campaigns on the old domain or before Phase 1 is verified.
