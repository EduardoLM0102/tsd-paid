# Cool Hand Electric — GTM / GA4 log

Container `GTM-KWZDRBVQ` (GTM account `6370314680`, container `260649558`). CID `9865206319`. See `google-ads-log.md` for the Search campaign build and `internal-notes.md` for scope/hours context.

---

## 2026-08-10 — GTM tracking review (pre-existing build, not built this session)

Edu had already built out Google Ads conversion tracking in this container before asking for a review. Findings:

**Working correctly (verified live, cross-checked against the real Ads account, not just internal consistency):**
- Container published (live version 2 at review time), confirmed installed on coolhandelectric.com via a Playwright render.
- All 3 conversion labels matched 1:1 against the real, enabled conversion actions in Ads (CID `9865206319`): Contact Form → `GGAVCO6oxd8cELSQmrM-`, Book Now → `gFkXCKbetd8cELSQmrM-`, Phone Click → `Lst_CKq7xd8cELSQmrM-`.
- The 3 form-field selectors (`#form-field-name`, `#form-field-email`, `#form-field-field_5ad6fea`) and the "BOOK ONLINE"/"SUBMIT" click-text triggers all matched real elements on the live page.

**Issues flagged (not fixed unless noted below):**
1. Two orphaned triggers existed with no tag attached: "50% of the form (Book Now)" (trigger 5) and "Open Form (Book Online)" (trigger 6). → Filled in the 2026-08-10 GA4 build below.
2. Base Google tag (`00 | G Ads - Tag`, tag 12) fires on *All Pages*, while the Remarketing tag (`01 | G Ads - Remarketing Tag`, tag 13) fires on *Initialization - All Pages* — earlier than the tag that sets it up. Google's own guidance is base config on Initialization so it loads first. **Still unresolved** — not part of this session's changes, flagged for a future pass if Edu wants it fixed.
3. Contact Form trigger (11) is click-based (fires on SUBMIT click + all 3 fields non-empty), not a confirmed-submission signal — weaker than Book Now, which rides real funnel-stage dataLayer events from the widget. Structural, not something to "fix" without changing the site's form implementation.

---

## 2026-08-10 — GA4 tags built and published

**Why.** Edu asked to add GA4 tracking to the same container: page view, both lead forms as separate events, phone clicks, and tags for the two orphaned triggers from the review above.

**Setup:**
- New constant variable `GA4 Measurement ID` = `G-ZHH3FSDC4J` (variable 18) — every GA4 tag below references this instead of hardcoding the ID, per Edu's instruction.
- GA4 Config tag (`05 | GA4 - Config`, tag 19, type `googtag` — GTM auto-normalizes the modern "Google tag" config type) fires on *Initialization - All Pages*, correct best-practice placement (ahead of the pre-existing Ads base tag issue in #2 above).

**Event tags (all type `gaawe`, all reference `{{GA4 Measurement ID}}` via `measurementIdOverride`):**

| Tag | Event name | Fires on | Notes |
|---|---|---|---|
| 06 \| GA4 - Lead (Contact Form) | `contact_form_lead` | Contact Form Trigger (11) | `oncePerLoad` |
| 07 \| GA4 - Lead (Book Now) | `book_now_lead` | Lead Trigger Book Now (4) | `oncePerLoad` |
| 08 \| GA4 - Phone Click | `phone_click` | Phone Click (7) | `oncePerLoad` |
| 09 \| GA4 - Book Now Form 50% | `book_now_form_50_percent` | 50% of the form (5) — was orphaned | `oncePerEvent` |
| 10 \| GA4 - Book Now Widget Opened | `book_now_widget_open` | Open Form Book Online (6) — was orphaned | `oncePerEvent` |
| 11 \| GA4 - Page View | `page_view` | All Pages (2147479573) | `oncePerEvent` |

**Two deliberate corrections made mid-build, both at Edu's direction:**
1. Initially set the Config tag to auto-send `page_view` (`send_page_view = true`) — the default, simplest setup. Edu asked for a dedicated Page View tag instead, so `send_page_view` was flipped to `false` on tag 19 and tag 11 (above) was added as a standalone event, firing on *All Pages* (after the Config tag's *Initialization*, so gtag is already set up when it fires).
2. Set `oncePerLoad` on the two lead-form tags and Phone Click (06/07/08) so a double-click or repeat submit in the same page load only sends one event each — mirrors the same protection already on the corresponding Google Ads conversion tags (15/16/17).

**PII avoided deliberately:** the container already has `user - full name` / `user - email` / `user - phone` variables (used by the Contact Form trigger's click-validation logic), but none of them were passed into any GA4 event as a parameter — GA4 prohibits collecting PII in event data, and doing so risks the property getting flagged. Only a non-PII `form_name` parameter (`contact_form` / `book_now`) was attached to the two lead events.

**Published:** live version 3, name "GA4 tags", same day. Confirmed via `containers().versions().live()` read-back — 12 tags live (5 pre-existing Google Ads + this build's 7 GA4 tags).

**Status: LIVE.** Full container is now: Google Ads conversion tracking (pre-existing, reviewed) + GA4 event tracking (built and published this session). No YouTube/Meta/TikTok pixel work done — out of scope for this session.

---

## 2026-08-31 — Tracking check on `/electrician-mansfield-tx/` (new Electrician-Broad landing page)

**Why.** Same session as the Search Ad Rank overhaul in `google-ads-log.md` — `electrician` was moved into a
new dedicated ad group (Electrician-Broad) pointing at this existing page. Edu asked to confirm tracking is
actually working there before relying on it.

**Method note — false start, then corrected.** A raw HTML fetch showed the GTM snippets present in the
page source, but a first live Playwright render showed **zero** analytics network calls and a `null`
`dataLayer` — looked broken. Traced to a `nitro-nojs` class in the markup: this site (via a
caching/performance plugin, likely NitroPack) delays *all* JavaScript, GTM included, until the visitor
actually interacts with the page (scroll/mouse move). An inert headless load never triggers that. Once
mouse movement + a scroll were simulated, the real stack fired within ~2s. **Lesson for future checks on
this site:** a static or no-interaction render will always look tracking-broken here; must simulate
interaction to get a true read.

**Confirmed working, consistent with this page's real conversion history since 2026-08-10:**
- `GTM-KWZDRBVQ` (the documented container) loads and initializes.
- GA4 property `G-ZHH3FSDC4J` fires a `page_view` hit.
- Google Ads conversion tag `AW-16750381108` fires its page_view/conversion-linker hits.
- The page's Contact Form (Elementor: `post_id`, `form_id`, `form_fields[name]`, `form_fields[email]`,
  `form_fields[field_5ad6fea]` as phone, `form_fields[message]`, checkbox, reCAPTCHA) uses the **same field
  IDs** documented in the 2026-08-10 GTM review (`#form-field-name`, `#form-field-email`,
  `#form-field-field_5ad6fea`) — strong structural match, so this is very likely the same form the
  site-wide "[TSD] Contact Form" click-validation trigger already covers, not a separate/missing
  integration. Not confirmed with a live test submission.

**Open item — Book Now may not be reachable from this page.** No "Book Now" widget/button rendered
anywhere on this landing page in a full-viewport render. Per the 2026-08-10 review, Book Now tracking
"rides real funnel-stage dataLayer events from the widget" — i.e. it's tied to that specific widget
component, not a generic form. If the widget genuinely isn't present on this template, this page's traffic
structurally cannot produce a `[TSD] Book Now Form` conversion — it would only ever convert via phone or
the contact form. Not fixed this session; worth confirming on the actual template/theme.

**Open item — phone click, inconclusive.** Couldn't get a clean read on whether the on-page `phone_click`
GA4 event fires: the simulated click landed on one of nine `tel:469-550-1102` links that wasn't visible in
the rendered viewport at the time. Not confirmed broken, just untested. Separately, the account's dominant
lead type — the ad-level "Click to call" (`CALL_FROM_ADS`) conversion — is tracked natively by Google off
the call extension itself, independent of this page's JS entirely, and is already proven working via
existing volume.

**New finding — a second, undocumented tracking stack fires on this page.** A separate GTM container,
`GTM-M7TSQ2S`, loads alongside `GTM-KWZDRBVQ` and initializes its own GA4 property, `G-PNHE045DRB`.
Confirmed via grep that neither ID appears anywhere in this repo (`gtm-log.md` or `google-ads-log.md`) —
genuinely not part of TSD's build. Origin unknown: could be a leftover from a previous developer/agency, a
theme/plugin default, or something the client's own team set up — **no evidence found either way**, so not
assuming it's any one of these. Not removed or investigated further this session; flagged as open if Edu
wants to pursue it (e.g. checking whether TSD's Google account has any visibility into that container, or
asking the client directly).

**Net assessment:** the tracking that actually feeds Ads/GA4 reporting for this page is confirmed intact.
Two things aren't resolved: the Book Now widget gap and the unexplained second GTM/GA4 pair.

---

## 2026-10-09: v5/v6 (Edu) GHL form tracking, v7 (Claude, Edu's go) restored main-site conversions

**v5 + v6 (Edu, 21:34 / 21:38 UTC):**
- Added `00 | cHTML - GHL Listener` (tag 27, Consent Init). It handles iframe embeds, including the white-label link.leadnurturemachine.com domain, plus native GHL forms, and pushes `ghl_form_submit`.
- Added trigger `GHL Lead` (28) on that event.
- Pointed `03 | G Ads - Lead (Contact Form)` (15, label GGAVCO6oxd8cELSQmrM-) and `03 | GA4 - Lead (Contact Form)` (20, event renamed contact_form_lead → `lead`) at GHL Lead ONLY.
- Deleted `04 | G Ads - Lead (Book Now)` and `07 | GA4 - Lead (Book Now)`.
- Side effect: main-site Elementor contact forms and RecreateAI bookings stopped counting while the 5 main Search ad groups still land on coolhandelectric.com. That was 27 of 66 Search conversions over the last 30 days.

**v7 (published 2026-10-09, workspace 7):**
- Tags 15 and 20 now fire on BOTH `Contact Form Trigger` (11) and `GHL Lead` (28).
- Recreated the Book Now lead tags from v5 with the same label/event, firing on `Lead Trigger (Book Now)` (4): new tag IDs 29 (`G Ads`, gFkXCKbetd8cELSQmrM-) and 30 (`GA4`, book_now_lead).
- Edu's GA4 event rename (`lead`) was kept.
- Read-back of the live v7 confirmed all of the above. To roll back, republish v6.

---

## 2026-10-10: v8 (Claude, Edu's go) Google "Calls from website" on go. pages

- New trigger 31 `Page View - go. subdomain` (Page Hostname equals go.coolhandelectric.com). The container also runs on the main site.
- New tag 32 `05 | G Ads - Calls from Website (go.)`, type awcc (API param keys: conversionId, conversionLabel, phoneConversionNumber):
  AW-16750381108 / 1SZGCMuRj5gdELSQmrM- (Ads action 7835207883), number to replace 469-351-1738.
- Built in workspace 9 → version 8 (test env first, then published) → Default Workspace 8 synced, 0 conflicts.
- Tested before publish (headless, Ads/GA4/Meta hits blocked): draft on go. page loads gstatic wcm/loader.js and calls
  googleadservices .../16750381108/wcm?dn=4693511738&cl=1SZGCMuRj5gdELSQmrM-; live v7 control = nothing; main site + draft = nothing.
  Re-checked on live v8 after publish: same on /electrician/ and /hvac-repair/, nothing on the main site.
- A fake gclid can't get a real forwarding number. The true test is a real ad click from a phone: the number should change
  and the tel: links should follow (they're tel:+14693511738, so confirm Google rewrites those too).
- Rollback = republish v7.

---

## 2026-10-10 (later): v9, tag 32 PAUSED, CallRail Website pool takes over number swapping

- Edu (via Claude in Chrome) changed the CallRail "Website pool" swap target 469-874-0198 → 469-351-1738. The pool (4 numbers:
  469-643-4559, 469-238-2518, 469-523-5395, 469-789-1607, source All, ring to 469-874-0198, recording on) now replaces the number on go. pages.
- Tag 32 (Google awcc) would race the pool for the same number, so it's PAUSED, not deleted (workspace 10 → version 9).
- Tested v9 before publish: go. pages show pool numbers (different per visit), no Google wcm request; main site unchanged
  (469-550-1102). Live v8 at the time showed the race (pool number shown, but Google's wcm request still firing).
- Published v9, test env deleted, Default Workspace synced (0 conflicts). Live re-check on /electrician/ + /hvac-repair/: pool numbers, no wcm.
- Rollback: unpause tag 32 (and set the pool swap target back to 469-874-0198 in CallRail), or republish v8.
