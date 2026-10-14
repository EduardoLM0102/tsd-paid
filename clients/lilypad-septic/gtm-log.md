# Lilypad Septic — GTM log

GTM account `6064090385` ("Lilly Pad Septic Service"), container `GTM-KG7WCQN` (97590507), workspace `12` (Default Workspace). Site: lilypadseptic.com.

---

## 2026-08-20 — Access granted, found and fixed a real broken-tracking root cause

**Why.** Edu got TSD access added to Lilypad's GTM account and asked to work on tracking. Followed up directly on the tracking-visibility gap flagged when the Search campaigns went live — TSD previously had no way to see inside this container.

**Container is not blank — real, purpose-built infrastructure already exists:**
- Google Ads: `Manual Call Tracking` (awcc), `Adwords Mobile Click To Call Tracking` (awct), `Google Ads - Form Tracking` (awct), `Google Conversion Linker` (gclidw)
- GA4: config tag (measurement ID `G-JGJRN475K2`) + event tags for click-to-call, click-to-text, email clicks, form submissions
- `RSS - Invoca - Base Pixel` — Invoca (call tracking / dynamic number insertion platform), fires on GTM's built-in All Pages trigger, not paused. This is very likely the real source of the `BC Calls v2` / `BC Qualified Calls` / `BC Qualified Forms` / `BC Qualified Ext Calls` conversion actions seen in Ads (`UPLOAD_CLICKS`/`UPLOAD_CALLS` — offline imports, independent of the site's own gtag calls). Invoca's own connection to the Google Ads account is unverified and outside GTM — no Invoca dashboard access, can't check from here.
- `Service Titan` and `Schedule Engine` custom HTML tags (the CRM and the booking widget), `HomeAndConstructionBusiness Schema` (SEO, unrelated to conversions).
- A real Enhanced Conversions setup (`RSS - EC - ...` tags/variables): captures first name, last name, email, phone from forms and hashes them via an `awec`-type variable for Google's Enhanced Conversions.

**Root cause found: 3 Google Ads conversion tags were firing with blank IDs.** `Manual Call Tracking`, `Mobile Click To Call`, and `Form Tracking` all read their `conversionId`/`conversionLabel` from Data Layer Variables (`phoneConversionId`, `phoneConversionLabel`, `mobilePhoneConversionId`, `mobilePhoneConversionLabel`, `formConversionId`, `formConversionLabel`) — meaning something on the site is supposed to push these values into `dataLayer` before the tags fire. **Checked three live pages directly (`/get-septic-services/` — the paid landing page, `/thank-you/`, and the homepage) and found zero occurrences of these variable names or any `AW-` conversion ID anywhere in the rendered HTML.** Nothing populates them. These three tags have almost certainly been firing with `undefined` conversion IDs since at least the account transfer, and likely longer — `RYNO Lead Forms` (the WEBPAGE conversion action these tags feed) shows only 2 conversions all of 2026 YTD against ~$10K of real ad spend, consistent with being broken rather than just low-volume.

**Found the real, correct values directly from the Ads account** (`conversion_action.tag_snippets` via GAQL, not guessed):
- Account conversion ID: **`AW-16840964046`**
- Call conversion label (`BC Qualified Ext Calls`, matches the `WEBSITE_CALL` tag type `Manual Call Tracking`/`Mobile Click To Call` need): **`lqFfCOzku-QaEM7vst4-`**
- Form conversion label (`RYNO Lead Forms`): **`RA5lCMmZ5usaEM7vst4-`**

**Fixed in the workspace (draft — not published, not live):** converted all 6 variables from Data Layer Variable to Constant, hardcoded to the real values above. Read back and confirmed: all 6 now show `type: c` with the correct values.

| Variable | Was | Now |
|---|---|---|
| phoneConversionId | Data Layer Variable (unset) | Constant: `AW-16840964046` |
| phoneConversionLabel | Data Layer Variable (unset) | Constant: `lqFfCOzku-QaEM7vst4-` |
| mobilePhoneConversionId | Data Layer Variable (unset) | Constant: `AW-16840964046` |
| mobilePhoneConversionLabel | Data Layer Variable (unset) | Constant: `lqFfCOzku-QaEM7vst4-` |
| formConversionId | Data Layer Variable (unset) | Constant: `AW-16840964046` |
| formConversionLabel | Data Layer Variable (unset) | Constant: `RA5lCMmZ5usaEM7vst4-` |

**What this fixes vs. doesn't:**
- **`Mobile Click To Call`** (tap-to-call button on mobile) needs only `conversionId`/`conversionLabel` — no other dependency. This should be fully correct once published.
- **`Form Tracking`** needs only `conversionId`/`conversionLabel`, fired on the `/thank-you/` page. Should be fully correct once published, **assuming the site's form actually redirects to `/thank-you/` on success** — not independently verified (didn't submit a real test form).
- **`Manual Call Tracking`** (the one that swaps the displayed phone number for a Google forwarding number) also needs `phoneConversionNumber = {{formattedPhone}}` — a **separate Data Layer Variable I did not touch**. It's also unpopulated (same site-wide check found nothing), so number-swap display likely still won't work correctly even after this fix. Didn't guess a value here on purpose: there are two real business numbers (Salina 785-268-2656, Hutchinson 785-626-8621) and the tag doesn't obviously differentiate between them — needs a real decision (which number, or a per-market variant) rather than a guess.

**Not done — still open:**
1. **Not published.** Everything above is in the workspace only, matching the house rule that publish is always a separate, explicit step. Nothing changes on the live site until someone reviews and confirms publish.
2. `formattedPhone`/`unformattedPhone` variables — still unset, blocks the number-swap piece of `Manual Call Tracking` specifically (the other two fixed tags don't need them).
3. No real end-to-end test performed (no actual test call placed, no test form submitted) — the fix is verified as *correctly configured* against real values pulled from the Ads account, not yet verified as *actually firing* in production.
4. Invoca's own Google Ads connection (feeding the `BC ...` actions) is unverified and outside GTM's visibility.
5. `RYNO Lead Forms` form action showing 2 YTD conversions despite ~$10K spend — worth revisiting once this fix is live and a real test has run, to confirm the form-to-thank-you-page redirect itself works, not just the tag.

---

## 2026-08-20, same day — Call-click tracking confirmed already built; real root cause found for the form gap; GHL listener built

**Call tracking via `tel:` clicks (Edu's question: "can't we just track calls with link clicks contains tel:?"):** Yes, and it already existed. `Click To Call Clicks` trigger (id 15) fires on any element click where `{{Click Element}}` contains `tel:` — no device restriction despite feeding a tag named "Mobile Click To Call". That tag uses `mobilePhoneConversionId`/`mobilePhoneConversionLabel`, both already fixed to real values in the entry above. **No new build needed here** — this path is complete once published, independent of the incomplete `Manual Call Tracking` number-swap piece.

**Why the form conversion was actually broken, found via the DOM, not guessed:** the "Schedule Septic Service" CTA on `/get-septic-services/` is not a native WordPress form — it's an iframe (`id="inline-L77TylxI6XxhMELKlkJP"`, `data-form-name="Schedule Service - Activate"`) embedded from `link.leadnurturemachine.com/widget/form/L77TylxI6XxhMELKlkJP`. That domain is a white-labeled GoHighLevel instance (RYNO's). **This means the existing `Form Tracking` tag's trigger (`Thank You Page`, firing on exact path `/thank-you/`) was never going to fire** — GHL's inline embed shows a success state without a page navigation, so no `/thank-you/` pageview ever happens. That's the real, mechanical reason `RYNO Lead Forms` shows only 2 conversions against ~$10K of spend.

**Built the same GHL listener pattern already proven on Proud Pops (and cloned onto Gillespie's, All Seasons AC)** — pulled the exact tag/trigger code from Gillespie's live container (`GTM-WJVDZBVF`, workspace 8) rather than reinvent it:
- **Variable `ghl_form_id`** (id 55) — Data Layer Variable reading `ghl_form_id`.
- **Tag `GHL - Listener`** (id 56, Custom HTML, fires on All Pages `2147479553`) — the proven `postMessage` listener script, unmodified. Its whitelisted origins (`leadnurturemachine.com`, `leadconnectorhq.com`, `msgsndr.com`) already cover Lilypad's specific GHL domain, confirmed by direct match against the iframe found on the live page — no edits needed to the script itself. On a valid GHL `set-sticky-contacts` postMessage, pushes `dataLayer.push({event: 'ghl_form_submit', ghl_form_id, ghl_data})`.
- **Trigger `GHL Form Submit - Lead`** (id 57, Custom Event) — `{{_event}} equals 'ghl_form_submit'` AND `{{ghl_form_id}} matches RegEx '.+'` (per Edu's explicit ask — a catch-all on form ID rather than hardcoding `L77TylxI6XxhMELKlkJP`, so it keeps working if the form ID ever changes).
- **Repointed the existing `Google Ads - Form Tracking` tag (id 24)** from `firingTriggerId: ['23']` (the dead Thank You Page trigger) to `['57']` (the new real trigger). Its `conversionId`/`conversionLabel` params were already correct (`{{formConversionId}}` / `{{formConversionLabel}}`, fixed to `AW-16840964046` / `RA5lCMmZ5usaEM7vst4-` in the entry above).

**Full chain, read-back confirmed, all in the draft workspace (not published):** GHL form submits → `postMessage` from `leadnurturemachine.com` → `GHL - Listener` tag catches it → `dataLayer.push({event:'ghl_form_submit', ghl_form_id:'L77TylxI6XxhMELKlkJP', ...})` → `GHL Form Submit - Lead` trigger matches (event name + non-empty form ID) → `Google Ads - Form Tracking` fires with `AW-16840964046/RA5lCMmZ5usaEM7vst4-`.

**Not done:**
1. Still not published — same gate as above, needs explicit go-ahead since it's the live site.
2. GA4's own form-submission tag (`RSS - GA4 - Form Submissions`) still relies on the same dead `/thank-you/`-path trigger — same root cause, not fixed yet, out of scope of what was asked this round (Google Ads tracking specifically). Flagging as a clear follow-up.
3. No real test submission run yet.

---

## 2026-08-25 — Published: conversion tracking fix + GHL listener now live

**Why.** Edu asked for a Lilypad status check. Found the 08-20 fix (conversion IDs/labels hardcoded, GHL listener built) was still sitting in the workspace, unpublished, 5 days into the two Search campaigns being live and spending (~$152 across 5 days, 1 conversion — a native call-extension click, unrelated to any of this GTM config). Edu asked to publish.

**Published** workspace 12 → container version 12 ("Fix conversion tracking + GHL form listener") via `gtm.py publish --account 6064090385 --container 97590507 --workspace 12`.

**Verified live**, not just published-per-API — fetched the public container (`googletagmanager.com/gtm.js?id=GTM-KG7WCQN`) directly and confirmed by string match:
- Real conversion ID `AW-16840964046` present
- Both real labels present (`lqFfCOzku-QaEM7vst4-` call, `RA5lCMmZ5usaEM7vst4-` form)
- GHL listener present (`ghl_form_submit` event name, `leadnurturemachine` origin string)

**What this actually fixes now that it's live:** `Mobile Click To Call` (tap-to-call button) and `Form Tracking` (via the new GHL trigger instead of the dead `/thank-you/` pageview trigger) should both report real conversions to Google Ads going forward.

**Still open, unchanged:**
1. `Manual Call Tracking`'s number-swap piece — `formattedPhone`/`unformattedPhone` still unset, needs a real decision (which number, Salina vs Hutchinson, or a per-market variant) before it can be filled in.
2. GA4's own form-submission tag — same dead-trigger root cause, not touched, still relies on the never-firing `/thank-you/` path.
3. **No real end-to-end test has been run** — a real form submission and a real test call, to confirm this fires in production and not just in config. Publish makes it live, it doesn't prove it works.

---

## 2026-08-30 — Deep check: the 3 fixed tags are still PAUSED, always have been, since before TSD touched the account

**Why.** Edu asked for a full tracking deep-check across Google Ads, GTM, and GA4. Pulled live conversion data by action (2026-08-20 → 08-30), then went past the 08-25 "verified live" string-match (which only confirmed the correct values were present in the `gtm.js` bundle) and checked the actual `paused` flag on each tag in the live container version via the Tag Manager API directly.

**Finding: `Google Ads - Manual Call Tracking` (14), `Adwords Mobile Click To Call Tracking` (21), and `Google Ads - Form Tracking` (24) are all `paused: true` in the live container (version 12, published 2026-08-25) — the exact three tags the 08-20/08-25 session fixed the conversion IDs, labels, and firing trigger on.** Pulled the same three tags out of version 10 (`Added RYNO Tracking Tags`, RYNO's original build) and version 11 — paused there too. **This paused state pre-dates any TSD involvement; the fix session corrected the config but never checked or flipped the paused flag, so none of the three tags has ever been able to fire, before or after the fix.**

**This reconciles the zero-conversion data:** since publish (08-25) through today, the two live campaigns have real traffic — 38 clicks, ~$149 spend, 6 days — and zero conversions from any of `RYNO Lead Forms`, `BC Qualified Ext Calls`, `BC Calls v2`, `BC Qualified Forms`, or `BC Qualified Calls`. The only conversions recorded this whole period are Google-hosted automatic actions unrelated to any site tag (`Local actions - Other engagements` x3, `Call Extension Calls` x1, `Local actions - Directions` x1) — i.e., nothing from the GTM container has fired a single Google Ads conversion since launch, paused or not.

**GA4 form tracking, checked separately, still broken as flagged 08-25 — no change.** `RSS - GA4 - Website Actions - Form Submission` (tag 44, trigger 43) still fires on `Page Path contains "thank"` — the GHL iframe never navigates there, so this event still can't fire. Not part of today's fix scope, just confirmed still open.

**New finding: TSD has no GA4 access for this property.** `ga4.py properties` (TSD's GA4 login) does not list a Lilypad Septic / lilypadseptic.com property at all — TSD can read/edit the GTM container that feeds GA4, but cannot independently query GA4 itself (sessions, event counts, the automatically-imported `GOOGLE_ANALYTICS_4_CUSTOM` conversion actions sitting `HIDDEN` in the Ads account like `bct_form_submission`, `bct_calls_all`). Same blind spot flagged for GTM on 08-20 (before access was granted), never resolved for GA4 specifically. Worth asking Cole/whoever admins Lilypad's GA4 for read access.

**Not changed — no live edits made this session.** Confirmed via API read only (`versions().live()`, plus version 10/11 pulls for history); did not touch the workspace or publish anything. Flagging for an explicit go-ahead before unpausing, per house rule.

### Aberto (updated)

- [ ] **Unpause tags 14, 21, 24** in a new workspace and publish — this is very likely the actual remaining blocker for Google Ads-side conversion tracking, on top of everything already fixed 08-25.
- [ ] Still needs `formattedPhone`/`unformattedPhone` filled in before tag 14 (Manual Call Tracking) is fully correct even once unpaused (Salina vs Hutchinson decision, carried over from 08-20).
- [ ] GA4 form-submission trigger still needs its own fix (separate from the Ads tags) — same dead `/thank-you/` path.
- [ ] Request GA4 read access for Lilypad's property.
- [ ] **A real end-to-end test (test call + test form submission) is now more overdue than before** — everything found today was via API/config inspection, not a live production test.

---

## 2026-08-30, same day — Unpaused and published: the 3 tags can now actually fire

**Why.** Edu reviewed the deep-check finding above and asked to unpause + publish immediately.

Fetched full tag definitions for 14, 21, 24 from workspace 13, flipped `paused` to `false`, `update-tag`'d each (read-back confirmed each one `paused=False` in the draft before publishing). Published workspace 13 → container version 13 ("Unpause Google Ads conversion tags"). **Verified live** via `versions().live()` (not just the publish response): all three tags — `Google Ads - Manual Call Tracking` (14), `Adwords Mobile Click To Call Tracking` (21), `Google Ads - Form Tracking` (24) — now show `paused: false` in the live version. Per the house rule (publishing from a lateral workspace leaves Default stale otherwise — this is what caused the Proud Pops "v34 Revert" incident), ran `workspaces.sync()` on the new Default Workspace (14): 0 conflicts.

**State now:** all three tags are live, unpaused, with the correct conversion IDs/labels (from 08-20/08-25) and the correct firing triggers (`Form Tracking` on the working GHL listener, not the dead `/thank-you/` page). This is the first point since RYNO's original build where this config has actually been capable of firing.

**Still true, unchanged by this action:**
1. **No real end-to-end test has been run yet.** Config-correct + unpaused is not the same as verified-firing. Next real call or form submission on the site is the actual test — should be checked for in Ads (`RYNO Lead Forms`, `BC Qualified Ext Calls`) within a day or two.
2. `formattedPhone`/`unformattedPhone` still unset — `Manual Call Tracking`'s number-swap display piece specifically still needs the Salina-vs-Hutchinson decision before it's fully correct, independent of being unpaused now.
3. GA4's own form-submission tag — still on the dead `/thank-you/` trigger, untouched.
4. TSD still has no GA4 access for this property.

### Aberto (updated again)

- [ ] Watch for real conversions on `RYNO Lead Forms` / `BC Qualified Ext Calls` / `Adwords Mobile Click To Call` over the next few days — first real signal this is actually working end to end.
- [ ] `formattedPhone`/`unformattedPhone` decision (Salina vs Hutchinson number) still open.
- [ ] GA4 form-submission trigger fix still open.
- [ ] GA4 read access request still open.
- [ ] Fold this unpause into the AM ticket alongside the still-owed $2,000/mo written approval and the 08-26 network-targeting fix.

---

## 2026-08-30, same day — Rebuilt conversion tracking on the Proud Pops pattern instead of continuing to patch RYNO's structure

**Why.** Edu didn't want to keep trusting/patching RYNO's inherited tag structure piecemeal — asked to rebuild conversion tracking using a proven, already-working TSD pattern instead. Pulled Proud Pops' live container (`GTM-WBFDB6L8`, account `6255217830`, container `198527160`) directly via the API to see the actual proven structure, not just go from memory. Confirmed scope with Edu: just conversion tracking (Ads + GA4 lead/call/form events), not the whole container — Invoca, Enhanced Conversions, ServiceTitan tag, and schema stay untouched and unaudited.

**What Proud Pops' pattern actually is, read from its live tags/triggers:** one custom event fans out to every destination in parallel (`cEvent - Lead` fires both the Ads lead tag and the GA4 lead tag off the same `firingTriggerId` list) — no separate broken proxy per destination. And no Google-side number-swap tag at all — DNI is left entirely to the dedicated vendor (CallRail for them), GTM just tracks plain `tel:` clicks into one phone-call tag per destination.

**Two changes made, same workspace/publish/verify-live/sync discipline as this morning's unpause:**
1. **`RSS - GA4 - Form Submissions` (tag 44)** — `firingTriggerId` changed from `['43']` (the dead `Page Path contains "thank"` trigger) to `['57']` (`GHL Form Submit - Lead`, the same real event already firing the Ads form tag). This closes the GA4 form-tracking gap flagged since 08-20 — GA4 now rides the same working event Ads already uses, instead of its own broken proxy.
2. **`Google Ads - Manual Call Tracking` (tag 14)** — re-paused, by design, not left half-built. It duplicates Invoca's own dynamic number insertion (already live on this site since RYNO's build), was never finished (`formattedPhone`/`unformattedPhone` never populated, no Salina-vs-Hutchinson decision made), and `Adwords Mobile Click To Call Tracking` (tag 21) already reports every real `tel:` click to Google Ads without it. Matches Proud Pops' pattern of leaving DNI to the dedicated vendor rather than running a second Google-side number swap that could fight over the same displayed number.

Published as container version 14 ("Rebuild conversion tracking on Proud Pops pattern"). **Verified live** via `versions().live()` directly (not the publish response): tag 44 `firingTriggerId` = `['57']`, tag 14 `paused` = `true`. New Default Workspace (15) synced, 0 conflicts. Public `gtm.js` refetched and confirmed serving normally post-publish.

**Not changed:** `formattedPhone`/`unformattedPhone` variables left in place (unused now, not deleted) in case a future per-market number decision revives tag 14. The orphaned paused legacy `Google Analytics GA4 Configuration` tag (5) — cosmetic only, left alone to keep this change minimal. Everything outside conversion tracking (Invoca, EC, ServiceTitan, Schedule Engine, Schema, the other RSS - GA4 - * event tags) — not touched, not audited this round.

### Aberto (updated)

- [ ] Watch for real conversions on `RYNO Lead Forms` / `BC Qualified Ext Calls` / `Adwords Mobile Click To Call` over the next few days.
- [ ] **A real end-to-end test (test call + test form submission) is the one thing that actually proves any of today's work, and still hasn't happened.**
- [ ] Fold all of today's GTM changes (unpause + rebuild) into the AM ticket, alongside the $2,000/mo written approval and the 08-26 network-targeting fix.
- [ ] GA4 read access for TSD still not granted for this property.

---

## 2026-09-07 — Checked GA4 (still no access) + confirmed the "1 conversion" Ads is reporting is real signal

**Why.** Edu flagged that Google Ads was showing only 1 conversion and asked for a GA4 check.

**Re-ran `ga4.py properties` (TSD's GA4 login).** Lilypad Septic / lilypadseptic.com still doesn't show up — same gap flagged 08-30, still unresolved 8 days later. TSD has no way to independently query GA4 (sessions, event counts) for this property; can only see it indirectly through the GTM container that feeds it.

**Pulled fresh Ads conversions by action, 2026-08-30 → 2026-09-07 (since the tag rebuild), account-level:**

| Action | Total | Date |
|---|---|---|
| RYNO Lead Forms | 1 | 2026-09-07 |
| Call Extension Calls | 1 | 2026-09-07 |
| Local actions - Website visits | 1 | 2026-09-02 |

Campaign spend/clicks same window: `TSD_08.20_Search_Branded_Evergreen` $42.26 / 20 clicks, `TSD_08.20_Search_NonBranded_Evergreen` $285.95 / 53 clicks.

**Read:** the 1 conversion Edu saw is `RYNO Lead Forms`, dated today — the GHL listener → `Google Ads - Form Tracking` pipeline rebuilt 08-30 firing for the first time since the RYNO takeover. Not a new break; it's the first real signal the rebuild is working end to end. `Call Extension Calls` and `Local actions - Website visits` are Google-hosted automatic actions, unrelated to any TSD tag work.

**Not done:**
1. Still can't verify anything GA4-side directly (sessions, `RSS - GA4 - Form Submissions` actually firing) — blocked on access, not on config.
2. Still no real end-to-end test (test call, test form submission) — same open item since 08-20.

### Aberto (updated)

- [ ] Request GA4 read access for Lilypad's property from Cole/whoever admins it — now the single blocker to independently verifying tracking, unresolved since 08-20.
- [ ] Real end-to-end test (test call + test form) still owed.
- [ ] Keep watching `RYNO Lead Forms` / `BC Qualified Ext Calls` volume over the next few days to confirm today's 1 form conversion isn't a one-off.
