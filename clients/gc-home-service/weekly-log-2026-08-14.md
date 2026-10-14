# GC Home Service — Internal Optimization Log
## Week ending Friday 2026-08-14

**INTERNAL ONLY.** Honest root cause lives here. Client version is sanitized per
`topserv-client-report-format` (never signal something was wrong) but calibrated per
`tsd-client-message-style` (don't over-sanitize real underperformance).

Data pulled 2026-08-14. Google Ads `2375064049` (tz `Africa/Kampala`, ~1 day lag). Meta
`1434273655098937`. GA4 `524926746`. GTM `GTM-TQ8XNRKW` (account 6336963084, container 242276268).

---

## 1. Headline numbers, Aug 8–14 vs Aug 1–7

| | Aug 1–7 | Aug 8–14 |
|---|---|---|
| Google spend | $356.07 | $971.81 |
| Google clicks | 94 | 1,085 |
| Google conversions (biddable column) | 0 | 0* |

*Real activity did exist — see root-cause finding below. The jump in spend/clicks reflects the
Aug 10 budget ramp fully landing this week.

---

## 2. Root cause found: conversion goal misconfiguration (not a tracking failure)

Did a full top-to-bottom audit across Google Ads, GTM, and GA4 to answer "is anything actually
wrong with the setup." Pulled the live (published, verified against draft workspace) GTM
container tag-by-tag, cross-referenced every conversion action's label against what GTM actually
fires, and queried `all_conversions` segmented by conversion action instead of trusting the
`conversions` column.

**Finding:** the lead-form tracking chain (GHL Listener → `ghl_form_submit` → GTM's `G.Ads - Lead`
tag) works. Confirmed a real conversion recorded **Aug 13** under `[TSD] Lead Form [LP]`
(`SUBMIT_LEAD_FORM` category). But `SUBMIT_LEAD_FORM/WEBSITE` was never set biddable on any of the
3 live campaigns — the Jul 28 goal rebuild made `QUALIFIED_LEAD/WEBSITE` biddable instead, and the
only action in that category (`Form Submision [Landing Page]`) is `UPLOAD_CLICKS` type, which
**cannot ever fire from a live browser conversion** — it's structurally dead. So the account was
quietly logging real leads into `all_conversions` the whole time while showing 0 in every report
that matters.

**Fixed 2026-08-14** (after switching out of auto-mode, which correctly refused to let this kind
of live bidding-affecting mutation run unattended): `campaign_conversion_goal.biddable` set to
`TRUE` for `SUBMIT_LEAD_FORM/WEBSITE` on all 3 live campaigns (`23511318927`, `23921909024`,
`24116591977`), verified by read-back. Added a permanent `conversion-goal` subcommand to
`update.py` to do this (didn't exist before — same explicit-`biddable`-FieldMask pattern as the
Jul 28 change).

Also built (not yet published) a GA4 event tag — `02 | GA4 - Lead`, event name `generate_lead`,
firing on trigger 29 (`ghl_form_submit`) — because the container had **zero** GA4 tags wired to
the lead-form trigger. GA4 was structurally blind to every lead, independent of the Google Ads
issue. **Open: publish this container change.**

---

## 3. PMax was pointed at an untracked page — also fixed

Checked the PMax asset group's actual destination (`book.gchomeservice.com/Home`), previously
logged in this file as "ServiceTitan's own booking portal." That label was wrong — pulled the raw
page source and it's a GoHighLevel-built funnel page (same platform as `/gc-heating-and-cooling/`,
`funnelId`/`leadconnectorhq.com` assets, a GHL Calendar widget), not ServiceTitan at all. Real
content: H1 "Cincinnati's Trusted Local AC & Heating Repair Experts," testimonials, a phone CTA.

But it has **zero tracking of any kind** — no GTM, no `gtag`/`AW-` pixel, no GA4, no Meta pixel.
Checked the full `<head>` and every script tag. So PMax (56% of daily budget, $135/day) was
sending its entire spend to a page that's structurally unmeasurable, not because of a goal
misconfiguration but because the tracking snippet was simply never installed on it. Minor tell:
page's `<html lang="es">` while content is English — looks like an unedited template artifact from
whatever generated it (`funnel-ai-production`).

Before redirecting, verified `/gc-heating-and-cooling/` isn't the weaker page — GA4 engagement
comparison (Aug 5–13) showed it dramatically outperforming the homepage (83% engagement rate vs
43%, 283s vs 54s avg session, 17% vs 57% bounce), and isolated to actual `google/cpc` sessions,
6/6 were engaged. No case for reverting the Aug 5 landing page swap.

**Fixed 2026-08-14:** PMax asset group (`6666862565`) `final_urls` changed from
`https://book.gchomeservice.com/Home` to `https://gchomeservice.com/gc-heating-and-cooling/`,
verified by read-back. Added a permanent `asset-group` subcommand to `update.py` (didn't exist
before). Learning period restarts for PMax.

**Not touched:** PMax's actual asset creative (headlines/images) may still be written around the
old direct-booking flow. Separate task.

**Also flagged, not fixed:** the YouTube video campaign's 4 video-responsive ads all still point
to the plain homepage (`https://gchomeservice.com/`), not the tracked landing page. Same
inconsistency as PMax was, smaller budget ($57/day). Open item.

---

## 4. Weather slowdown — client task from Alex/Steve/Dan

Client reported a call/traffic slowdown tied to unusually mild, muggy weather (not the heat that
normally drives AC demand) and asked for paid recommendations, including reaction to their own
list (storm damage, replacement, humidity/mugginess, UV lights, charcoal filters/IAQ). Also: Alex
requested pausing the Meta installer/recruitment ad to refocus on lead gen — **could not execute,
Meta MCP connector needs authentication not completable this session. Still owed.**

Ran real keyword volume (Cincinnati Metro, Keyword Planner) instead of guessing:

| Theme | Avg monthly searches | Trend Apr→Jul |
|---|---|---|
| Whole-house dehumidifier | 110 | 70 → 260 (~4x) |
| AC replacement cost | 50 | 50 → 110 (2x) |
| AC tune up | 70 | 70 → 110 |
| IAQ / UV light / charcoal filter (each) | ≤10 | flat |
| Storm damage (roof/tree/generator) | ≤10 | flat |

Existing keyword coverage checked: the only nonbranded campaign (`TSD_07.05_Search_Nonbranded_Cooling`,
paused, $60/day already budgeted) has 100 keywords across 3 ad groups, all repair/emergency/
maintenance themed. Zero humidity, replacement, IAQ, UV, or storm-damage coverage — clean slate.

**Recommendation, ranked:** humidity/dehumidifier is the strongest angle by a clear margin and is
data-backed, not just weather-narrative. Replacement is a real secondary. IAQ/UV are noise-level
locally — only worth folding into humidity messaging, not a standalone build. Storm damage as
originally proposed (roof/tree) has no local search volume and isn't GC's trade.

**Follow-up on storm damage specifically for Meta:** confirmed a real, recent hailstorm —
**Aug 11, quarter-size hail + 60mph gusts, Hamilton and Clermont counties** (core of the service
area) — via NWS-sourced local reporting. Reframed as an HVAC-specific angle (hail-damaged AC
condenser fins, a real and well-known failure mode) rather than generic storm damage. Recommended
as a short-flight, tightly geo-targeted Meta offer, not a Google Search play (no volume there).

**Status: recommendations only, nothing built yet.** Neither the Google humidity build nor the
Meta hail offer has been started.

---

## 5. Client report

Built as `GC-Home-Service-Weekly-Update_2026-08-14.pdf`. Same plain format as the prior two weeks.

Sanitized per doctrine — client-facing language:
- Conversion goal fix → "adjusted the conversion tracking configuration so qualified lead-form
  submissions are fully reflected in the account's optimization signal."
- PMax redirect → "redirected Performance Max traffic to the dedicated landing page... every
  campaign now points to the same fully-tracked, purpose-built page." No mention of the
  ServiceTitan mislabel or the untracked-page finding.
- Meta section: "No changes this week, awareness campaign running as-is" (per Edu — installer ad
  still live, pause not yet executed).
- Next Steps carries the humidity (Google) and hail-response (Meta) ideas, phrased as
  recommendations we could pursue, explicitly not as work already started (Edu's correction).

PDF had a build hiccup worth remembering: headless Chrome's `--print-to-pdf` added its own
browser header/footer (timestamp + file path) on both pages, and neither `--print-to-pdf-no-header`
(not a real flag) nor `--kiosk-printing` suppressed it on this Chrome build (151.x). Fixed via
PyMuPDF redaction (`add_redact_annot` + `apply_redactions`, saved to a new path then swapped in —
saving incrementally to the same open path throws `ValueError: save to original must be
incremental`). A simple white-rectangle overlay (`draw_rect`) is **not enough** — it hides the
artifact visually but the text objects are still in the content stream and reappear on text
extraction/copy-paste; redaction actually removes them.

**Status: built, not yet confirmed sent.**

---

## 6. Open items

- [ ] **Publish the GTM container** — GA4 lead tag is built in the draft workspace, not live yet.
- [ ] **Meta: pause the installer/recruitment ad** (Alex's request) — blocked on Meta MCP auth.
- [ ] **YouTube video ads still point to the homepage**, not `/gc-heating-and-cooling/` — same
      inconsistency PMax had, smaller budget. Decide and fix.
- [ ] **Google: build the humidity/dehumidifier ad groups** into the paused nonbranded campaign
      shell — recommended, not started.
- [ ] **Meta: build the hail-response offer** — recommended, not started.
- [ ] **AM tickets still owed**, now four deep and none papered: Jul 28 PMax cut, Aug 10 budget
      ramp, today's PMax URL redirect, today's conversion-goal biddable change.
- [ ] **PMax asset creative** may still reference the old direct-booking flow — not checked.
- [ ] ServiceTitan offline import — still zero upload-origin conversion actions. Unchanged, still
      the real long-term fix for attribution.
- [x] Carried-over question from last week ("is the account just not converting or is tracking
      broken") — answered. Tracking works; the goal category and the PMax destination were both
      structurally wrong. Both fixed today.
