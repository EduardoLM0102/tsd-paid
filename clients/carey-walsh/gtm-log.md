# Carey & Walsh — GTM log

GTM account `6000900042` ("Carey and Walsh inc,"), container `GTM-M5DW5ZN` (31040482), workspace `6` (Default Workspace). Site: careyandwalsh.com.

---

## 2026-10-05 — Read-only check while building the media plan. No changes made.

**Why.** New client, checking the tracking state before writing the plan's pre-launch gates.

**Container is in TSD's GTM and is the one on the live site.** `GTM-M5DW5ZN` loads on careyandwalsh.com (home + contact pages checked).

**Workspace 6 has a full tag build that isn't published:**
- Google Ads: `Google Ads | Configuration | All Pages` (googtag), `Google Ads | Event | Lead` (awct), `Google Ads | Event | User-provided Data` (awud), `Conversion Linker` (gclidw)
- Meta: `Meta | Event | Page View / Lead / Phone Click / Email Click` (cvt_5RM3Q template)
- GA4: config + events for Page View, Lead, Phone Click, Email Click
- `CallRail | Configuration | All Pages` (html), `cHTML - GHL Form Listener` (html)
- Triggers: `cEvent - Lead` (custom event), `Trigger | Phone Click`, `Trigger | Email Click` (link clicks)
- Variables include constants `Conversion ID`, `Google Tag`, `Meta Pixel ID`, `GA4 Measurement ID`, plus hashed email/phone and FBC/FBP cookie variables for enhanced matching. Constant values were not read.

**Live published container (version 5, from gtm.js):** only GA4 `G-6J3K34P4W5` and the GHL / LeadConnector listener. No `AW-` conversion ID and no Meta pixel. CallRail is not in the live container, but CallRail is hardcoded in the site HTML.

**Read:** someone at TSD started the tracking build and stopped before publishing, most likely because the Google Ads and Meta accounts were never created (none exist as of 2026-10-05). Forms run on GHL.

**Open items:**
- Once the Google Ads account exists: confirm the Conversion ID constant points to it, review the Lead tag's trigger against a real GHL form submission, then publish (as its own step, separate from edits).
- Once the Meta ad account and pixel exist: fill `Meta Pixel ID`, test events in Events Manager.
- Decide whether CallRail stays hardcoded or moves into GTM (don't run both).
- No end-to-end lead test has been run. Don't treat any of this as working until one is.
