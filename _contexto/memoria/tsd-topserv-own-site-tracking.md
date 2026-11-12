---
name: tsd-topserv-own-site-tracking
description: TopServ's OWN site tracking: GA4 482013707 (G-PSDPRNYVCW) + GTM-PR3DRB45; booking_click v4; Default ws holds someone's old unpublished draft
metadata:
  type: project
---

TopServ Digital's own website (topservdigital.com, Webflow; new Next.js site on staging topservstaging.vercel.app since 2026-10-27, same container).

- **GA4** property `482013707` (stream G-PSDPRNYVCW, account "Topservdigital" 349087094). The TSD GA4 token reads it, but it's READ-ONLY, so key event changes are a UI job (see [[tsd-ga4-data-api-access]]).
- **Key events BEFORE 10-28 change:** purchase, phone_link_click, mailto_link_click, ghl_webinar, ghl_calendar, ghl_survey, phone_call, ghl_book, ghl_form. The requester (AT user c8265043) checked them against GHL Growth Strategy Call bookings 9/25–10/22: **ghl_calendar = the real booking key event** (1 per booking, cancelled ones included), ghl_book never fired. So ghl_book comes off, and `assessment_complete` gets added (it comes from the new site's Brand Assessment form; its 9 custom dimensions are already registered).
- **GTM** GTM-PR3DRB45 = account 6273170749 / container 208573125 (other containers in that account: Web | Topserv Digital, Events Container, Brand Equity, Server). Live v3 before 10-28. Constant "Measurement id" = G-PSDPRNYVCW.
- **booking_click (AT task 0092f797, 10-28):** version 4 = trigger 35 "Link Click - Booking (book.topservdigital.com, excl /FDM)" (Click URL contains book.topservdigital.com AND does not match /fdm, ignore case; wait for tags 2s) + tag 36 "GA4 - booking_click" (gaawe, param link_url = Click URL). Plain event, not a key event. Headless test 10/10 on staging + live (scripts `topserv_site_booking_click_*_1028.py`). **PUBLISHED 2026-10-28 (live = v4)** on Edu's explicit go; Default ws synced (0 conflicts), test env 37 deleted, Items 1-2 done by Cowork in the GA4 UI 10-28 and verified via Admin API (ghl_book off, assessment_complete on, stream G-PSDPRNYVCW). assessment_complete had saved with a $1 USD default value despite Cowork saying it cleared it; Cowork fixed it 10-28, API confirms no default value on any key event. Lesson: verify Cowork GA4 edits via the Admin API, its self-report was wrong once. AT: all 3 ticked, Execution Response written, Execution completed → Review & Close with Johnny P. (requester c8265043) 10-28.
- ⚠ **Default Workspace (id 4) holds someone's unpublished Jan/Feb 2026 draft**: Conversion Linker, Google Ads conversion "Diagnostic Call Button Clicked" (AW-17856876156), and it deletes the 3 paused "Book Now" tags. Never publish from Default without asking who owns that draft. Side workspace + sync after publish.

**Why:** the container serves both the live and staging sites, so anything published goes live on the current site immediately.

**How to apply:** test changes headless on BOTH hosts. On the live Webflow site, hide the `[class*="pop-up"]` overlay before clicking (the /FDM ebook links sit inside it), and stub book.* instead of aborting it. Aborting the navigation kills the page before GA4 flushes and gives a false FAIL. One GA4 hit showing twice with the same `_s` = gtag retrying a blocked request, not a double fire.

**GA4 UI 2026-10:** there is no separate Key events page or "New key event" button anymore. Use Admin > Data display > Events > Key events tab. To add a key event before the event has data, use Create event > Create with code, then turn on Mark as key event. Cowork's picker showed the account as "KickCharge Creative 1", but the API says account 349087094 "Topservdigital". Trust the property ID.
