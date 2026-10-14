# Gillespie's Heating and Cooling — GTM log

Container `GTM-WJVDZBVF` (GTM account `6360204363`, container `255120208`). CID `7410489772`. See `google-ads-log.md` for account-level context (account was blank before this build — no conversion tracking, no GA4, no GTM snippet installed on site).

---

## 2026-08-18 — Full container scaffold cloned from Proud Pops, filler IDs

**Why.** Edu asked to build out Gillespie's GTM container using Proud Pops' setup (`GTM-WBFDB6L8`, account `6255217830`, container `198527160`, workspace 43) as the template — same tag/trigger/variable architecture, but with placeholder pixel/GA4/Google Ads IDs since Gillespie has none of those connected yet.

**What was cloned 1:1 (names, types, logic, folder structure):**
- 5 folders: Google Ads, GA4, Listener, Meta, CallRail
- 19 variables (constants, dataLayer reads, hashing/UUID JS macros, 1st-party cookie reads)
- 2 custom templates imported from the Community Gallery: `Facebook Pixel_import_1` (facebook/GoogleTagManager-WebTemplate-For-FacebookPixel) → new template id 28, and `Facebook Pixel` (facebookarchive, older version) → new template id 29. Tag type `cvt_198527160_91` → `cvt_255120208_28`, `cvt_198527160_21` → `cvt_255120208_29`.
- 14 triggers (button clicks, link clicks, custom dataLayer events, phone/mailto detection)
- 23 tags: Conversion Linker, GHL form listeners (x2), Google Ads conversion tags (Lead/Phone Call/Email/User-provided Data/Remarketing), GA4 event tags (Page View, Lead, Phone Click, Email Click, two Instant Quote clicks), Meta Pixel tags (Page View, Lead, Phone Click, Email Click, two Instant Quote clicks), CallRail swap script, base GA4 + Google Ads config tags.

**Filler values used at build time — MUST be swapped for real ones before this container goes live:**

| Variable/field | Filler value | Real value goes here once |
|---|---|---|
| `GA4 Measurement ID` (var) | ~~`G-XXXXXXXXXX`~~ | GA4 property is created for Gillespie |
| `Google Tag` (var) | ~~`AW-XXXXXXXXXX`~~ | Google Ads account tag is confirmed (CID 7410489772) |
| `Conversion ID` (var) | ~~`XXXXXXXXXX`~~ | same — numeric portion of the AW- tag |
| `Meta Pixel ID` (var) | `XXXXXXXXXXXXXXX` | Meta Pixel is created for Gillespie |
| `05 \| G.Ads - Lead` conversionLabel | ~~`REPLACE_WITH_LEAD_CONVERSION_LABEL`~~ | Lead conversion action is created in Ads |
| `02 \| G.Ads - Phone Call` conversionLabel | `REPLACE_WITH_PHONE_CALL_CONVERSION_LABEL` | Phone Call conversion action is created in Ads |
| `03 \| G.Ads - Email` conversionLabel | `REPLACE_WITH_EMAIL_CONVERSION_LABEL` | Email conversion action is created in Ads |
| `00 \| CallRail - All Pages` script src | `cdn.callrail.com/companies/REPLACE_WITH_CALLRAIL_COMPANY_ID/REPLACE_WITH_CALLRAIL_SCRIPT_ID/12/swap.js` | CallRail (or decision not to use it) is confirmed for Gillespie |

**2026-08-18, same day — real Google Ads/GA4 values swapped in:** Edu provided the real IDs. `Conversion ID` = `18229014139`, `Google Tag` = `AW-18229014139`, `GA4 Measurement ID` = `G-V636WJ3PSD`, and the `05 | G.Ads - Lead` conversionLabel = `zIcSCNmx1-McEPvcovRD` (form-fill conversion). These four now flow live to every tag that references them (Google Ads conversion linker/base tag/remarketing, all GA4 event tags, GA4 base config tag). **Meta Pixel ID, Phone Call conversion label, Email conversion label, and CallRail company/script ID are still filler** — not yet provided.

**Adapted (not filler, but changed from Proud Pops' real value to Gillespie's):**
- Conversion Linker `linkerDomains`: was Proud Pops' Lovable preview-domain list + `proudpops.com`/`txproblemsolvers.com` → set to `gillespieheatingcooling.com` (confirmed real domain; site is WordPress, not Lovable, so no preview subdomains needed).

**NOT adapted — carried over verbatim from Proud Pops, will misfire if left as-is:**
Proud Pops is an HVAC+plumbing+electric+**roofing** merger; several triggers match exact button text / URL fragments from *their* site that don't exist on gillespieheatingcooling.com (checked via live fetch of the site, which is WordPress):
- `Button - Instant HVAC Quote` / `Link Click - Instant Roof Quote` (URL fragment `instant-roof-quote`) — Gillespie has no roofing and no "Instant Quote" tool; real CTAs are "Get a Free Estimate" (`#request-estimate`), "Request Estimate Online" (`#request-estimate`), "Request a Free Estimate" (`/contact/`).
- `Button - Header_Schedule Online`, `Button - Home_Schedule_1HApprointment` ("SCHEDULE MY 1-HR APPOINTMENT"), `Button - All_Pages_Schedule_My_Appointment` ("SCHEDULE MY APPOINTMENT") — no matching button copy found on Gillespie's site.
- `Link Click - Contact Us` (URL fragment `contact-us`) and `Link Click - Book Now` (URL fragment `book-now`) — Gillespie's contact page is `/contact/`, no `book-now` path found.
- Generic ones that should work as-is regardless of site copy: `Trigger | Phone Click`/`Link Click - Phone Number` (matches any `tel:` link — confirmed Gillespie uses `tel:` links), `Trigger | Email Click`/`Link Click - Mailto` (matches any `mailto:` link — confirmed), `cEvent - Lead`/`cEvent - Appointment Scheduled`/`User data to LS` (dataLayer-event based, not text-based).

## 2026-08-18, later same day — published (live version 3)

Edu gave the real "form fill" Google Ads conversion label (`zIcSCNmx1-McEPvcovRD`, verified against the live account's enabled "TSD - Lead Form" conversion action) and the real phone-call label (`8I3bCM-L3-McEPvcovRD`, verified against the live account's enabled "Click to call" conversion action — both `AW-18229014139`, both primary-for-goal), then asked to publish.

**Compile blocker found and fixed:** `create_version` kept returning `compilerError: true` with no detail. Bisected by deleting tag groups and re-checking compile status (each removed group restored afterward from the saved source JSON — one bisection step also surfaced an unrelated GTM API quirk: a *successful* `create_version` call permanently seals the calling workspace, "Workspace is already submitted," same as clicking Submit in the UI — so mid-diagnosis a workspace got sealed with only partial content; it didn't lose data, a new workspace was created and it automatically inherited the container's real current baseline, which luckily already had everything from that point except 19 of the tags). Root cause: **a workspace created via the Tag Manager API starts with zero built-in variables enabled** (`built_in_variables().list()` returned `{}`), unlike the GTM web UI which auto-enables ~7 defaults for a new workspace. Six tags referenced `{{Page URL}}` and several triggers referenced `{{Click Text}}`/`{{Click URL}}` — all undefined, which fails compile. Fixed by enabling the same 11 built-ins Proud Pops' container has (`clickElement`, `clickClasses`, `clickId`, `clickTarget`, `clickText`, `clickUrl`, `pageUrl`, `pageHostname`, `pagePath`, `referrer`, `event`) via `built_in_variables().create()`. **Worth remembering for any future GTM container built via this API rather than the web UI** — always enable built-ins first, before creating any tag/trigger referencing them.

**Status: PUBLISHED. Live version 3** ("Initial build"), confirmed via `versions().live()`: 23 tags, 14 triggers, 19 variables, 2 custom templates, 5 folders — matches the full intended scaffold.

**Still filler in the live container:** `Meta Pixel ID` (now `0000000000000000` — switched from the original `XXXXXXXXXXXXXXX` filler because the Facebook Pixel template enforces a `^[0-9,]+$` regex on this field at compile time, so it has to be numeric even as a placeholder), `03 | G.Ads - Email` conversionLabel (`REPLACE_WITH_EMAIL_CONVERSION_LABEL`), and the CallRail company/script ID. Real and live: `Google Tag` (`AW-18229014139`), `Conversion ID` (`18229014139`), `GA4 Measurement ID` (`G-V636WJ3PSD`), Lead and Phone Call conversion labels.

**Housekeeping left behind, harmless but worth knowing about:** workspace 2 got sealed mid-diagnosis (contains only 4 of the 23 tags, not used); an empty workspace 3 also exists (a cross-workspace template test that failed as expected); container version 2 ("diag") exists but was never published and only has 4 tags. None of this affects the live container (version 3), and the API token doesn't have delete-workspace scope to clean them up — cosmetic clutter only, visible in the GTM UI's workspace/version list.

**Before this is fully live in production:** (1) install the `GTM-WJVDZBVF` snippet on the site — it isn't there yet (WordPress site, no GTM container detected as of this session), (2) create the Meta Pixel, Email conversion action, and CallRail account (or drop that tag) and swap in the real values, (3) update the site-copy-specific triggers listed above to match Gillespie's actual CTAs.
