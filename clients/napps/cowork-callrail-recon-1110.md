# Cowork prompt: Napps CallRail recon for landing-page call tracking (fu-146, 2026-11-10)

Paste everything below the line into Cowork.

---

**Task: read-only recon for Napps Cooling, Heating & Plumbing (Longview TX). Change nothing.**

Context: Napps runs Google Ads to two new landing pages:
- https://nappsac.com/furnace-heating-repair-in-longview/
- https://nappsac.com/emergency-plumber-in-longview/

Both show the main business line **903-758-6482**. That's the number CallRail forwards to, not a tracking number, so calls placed from these pages aren't recorded in CallRail or Google Ads. We want to put a CallRail number on these pages for Google Ads visitors. Before choosing how, I need the facts below.

What we already know from the CallRail API (don't re-check these):
- CallRail account "TopServ Digital Clients", company "Napps Cooling-Heating-Plumbing" (COM4cd8da6854164edba5bd2d3ffc44179f).
- Company script: `//cdn.calltrk.com/companies/336278805/1286f50050a4f3ac8e79/12/swap.js`. DNI is not active.
- Active trackers: GBP 903-522-5601, LSA 903-289-6340, "Google Ads" call-asset number 903-289-7073, Organic Social 903-320-4458.
- "Paid Search (Google Ads)" session tracker: disabled since 2023-05-15, holds no numbers.
- Google Ads integration for Napps: state "pending", no Google Ads customer selected.

Before you start: in Chrome, turn off Global Privacy Control and the ad blocker for nappsac.com. Steps 6 and 7 must run as a first-time visitor, so clear site data for nappsac.com and link.leadnurturemachine.com, or use a fresh profile.

**Hard rules:** do not buy or provision numbers, do not enable, create or edit any tracker, do not connect or reauthorize integrations, do not edit or publish anything in GTM, and do not change WordPress settings. Look, screenshot and report only. If something can only be seen by starting a purchase or edit flow, stop at the screen before any confirm button and report what it shows.

**Collect:**

1. **CallRail plan and cost:** the account's plan name, how many local numbers are included and in use, and the price of one extra local number per month. Also whether the plan includes session (keyword-level) tracking, and any per-minute cost.
2. **Old session tracker:** open "Paid Search (Google Ads)" under Napps > Tracking Numbers (show disabled). Report its pool size, source rule, swap target and keyword settings, and whether the UI offers "re-enable". If it does, note what it says re-enabling would cost or provision. Don't click it.
3. **Number availability:** in the new-tracker flow, check whether local 903 numbers are offered (just the list, stop before purchase). Check both a single source tracker ("Google Ads" / paid search, website swap) and a session tracker pool. For the pool, note the size CallRail recommends for about 40 visits/week.
4. **Google Ads integration:** open Napps > Integrations > Google Ads. Screenshot the state and report which Google login it uses, which customer IDs it lists, whether 950-960-5037 (Napps PPC) is among them, and what's needed to finish it. Don't finish it.
5. **GTM-KH7RS4V** (Tag Manager UI, workspace in use): list every tag, paused or not, that mentions callrail or calltrk, with its trigger. Also note the live version number and its publish date.
6. **Live page check, first-time visitor:** open each landing page with `?gclid=TSDTEST1110&utm_source=google&utm_medium=cpc` appended. Note the phone number shown in the header, the body and the tel: links, before and after the first scroll. In DevTools > Network, filter `calltrk` and `callrail` and say whether anything loads.
7. **WP Rocket:** if we have WordPress admin access to nappsac.com, open WP Rocket > File Optimization > "Delay JavaScript execution". Is it on, and what's in the excluded list? Don't change it. If we have no WP access, say so and tell me who the site's web contact appears to be (footer credit or admin user list).

**Report back in this format:**
- Plan/cost: …
- Old session tracker: …
- 903 numbers available: single tracker yes/no, pool yes/no + recommended size …
- Google Ads integration: state, login, customer IDs listed, 950-960-5037 present yes/no, what finishing needs …
- GTM CallRail tags: … (live version + date)
- Live pages: number shown before/after scroll, calltrk loaded yes/no (per page) …
- WP Rocket: delay on/off, exclusions … or no access + web contact …
- Anything surprising: …

Attach screenshots for items 2, 4 and 6.
