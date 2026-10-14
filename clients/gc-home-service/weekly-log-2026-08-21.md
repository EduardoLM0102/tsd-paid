# GC Home Service — Internal Optimization Log
## Week ending Friday 2026-08-21

**INTERNAL ONLY.** Honest root cause lives here. Client version is sanitized per
`topserv-client-report-format` (never signal something was wrong, and this week specifically:
never state the account has 0 conversions in the client-facing copy) but calibrated per
`tsd-client-message-style` (don't over-sanitize real underperformance).

Data pulled 2026-08-21 via Ratos (`insights.py`, `read.py`, `st_conv_check.py`). Google Ads
`2375064049` (tz `Africa/Kampala`, ~1 day lag — newest complete day is 2026-08-20). Meta
`1434273655098937`.

---

## 1. Headline numbers, Aug 8–14 vs Aug 15–21 (through Aug 20)

| | Aug 8–14 (as reported) | Aug 15–21 (partial, thru Aug 20) |
|---|---|---|
| Google spend | $971.81 | $1,410.37 |
| Google clicks | 1,085 | 2,314 |
| Blended CPC | $0.90 | $0.61 |
| Standard "conversions" column | 0 | 0 |

Click volume roughly doubled and CPC fell ~32%, consistent with PMax's first full week pointed
entirely at `/gc-heating-and-cooling/` (the Aug 14 redirect) plus the Aug 10 budget ramp fully
landing. **The standard conversions column is still 0 across every live campaign** — same as
the prior two weeks. Per Edu's instruction, this does not appear anywhere in the client-facing
version; it's tracked here so we don't lose the signal internally.

## 2. Real activity found via `all_conversions` (not the biddable column)

Ran `st_conv_check.py` against the account. Segmented by day, Aug 1–20:

| Date | Action fired | Count |
|---|---|---|
| 08-01, 08-03, 08-06 | Calls from ads [1] | 1 each |
| 08-13 | [TSD] Lead Form [LP] | 1 |
| 08-15 | [TSD] Website Call Link | 15 |
| 08-16 | [TSD] Website Call Link | 12 |
| 08-17 | [TSD] Website Call Link | 13 |
| 08-18 | [TSD] Website Call Link | 4 |
| 08-19 | [TSD] Website Call Link | 6 |
| 08-20 | [TSD] Website Call Link | 5 |

**55 tel: tap firings since the Aug 14 redirect**, against essentially zero in the prior 90 days
(4 total). `[TSD] Website Call Link` is a click-to-call tap, `CALL_FROM_ADS` origin,
`PHONE_CALL_LEAD` category — **not currently biddable** (turned off in the Jul 28 goal rebuild in
favor of `DEFAULT/WEBSITE` + `QUALIFIED_LEAD/WEBSITE`). Zero `First Time Phone Call`, zero
`Repeat Phone Call`, zero `[TSD] Lead Form [LP]` fired this week — the two biddable goal
categories the account is actually optimizing toward are still silent.

**Read: the redirect surfaced real engagement (tap-to-call) that wasn't visible before, but the
categories the campaigns are bidding on haven't produced anything yet.** Not conclusive evidence
of a problem — could just be a thin-data week, or could mean the added PMax volume is skewing
toward lower-intent placements (search impression share for PMax is still only ~12%, i.e. PMax's
network mix likely leans Display/Discover/YouTube, which would explain the CPC collapse to
~$0.40 on PMax specifically). **Not yet verified** — would need a network/placement breakdown to
confirm before recommending any budget action. Flagging for a decision next week rather than
acting now.

## 3. Meta: the Yeti Giveaway launch — this week's actual headline

Checked the activity log (Aug 15–21) and initially misread this as an unrelated third party
touching the account — **wrong**. Edu confirmed the person behind these changes,
Jonathan Bannister, is on our side; this was our work, not an outside actor. Corrected here so
the record doesn't carry the wrong framing forward. (Also moot: the Meta MCP pause request from
Alex re: the installer/hiring ad — that campaign already shows $0 spent / inactive.)

Changes made 2026-08-20, 9:36–9:43 AM, via Business Manager / Power Editor (some steps logged
under "ads MCP server" application name):
- **Launched `CBO | YETI GIVEAWAY | 20 AUG`** — $100/day CBO, broad 18–65+ M+F across the full
  service area, Advantage+ audience on, 7 new static "Yeti" ads, optimization goal "Leads." This
  is the actual headline of the week and is written up as such in the client report. Re-checked
  status after the first pull showed it as PAUSED — a later pull shows `effective_status: ACTIVE`,
  $0.00 spent in the last 7 days, no impressions/leads yet. Reads as newly launched and still
  ramping up, not stalled — worth a status check early next week before the next report.
- Paused `CBO | NEW CREATIVES | 8 JUL` (the quote-back creative test; lifetime $616.94 / 2 leads /
  $308.47 CPL per the account's own attribution — doesn't match the $47.16 CPL read from the raw
  breakdown in the 07-31 log, worth reconciling attribution windows before citing either number
  again) — retired now that the Yeti campaign replaces it.
- Paused the older `TOFU - Awareness - Ad Recall Lift` ad set — **not** the whole awareness
  campaign. The campaign (`TSD_2026-01_TOF_AWARENESS_CBO_Evergreen - Ad Recall Lift`) is still
  ACTIVE, now delivering solely through its other ad set, `08/06/2026 - ZIP Codes | Broad`
  ($62.79 spent this week). Corrected in-session after Edu caught the overstatement — do not
  repeat "awareness paused."

## 4. Client report

Built as `GC-Home-Service-Weekly-Update_2026-08-21.html` / `.pdf`. Same plain format as the prior
three weeks (Playwright/Chromium headless render this time — system Chrome isn't installed on
this machine; used the same recipe as `build_calendar_pdf.py`). QA'd via full-page screenshot,
fits on one page, screenshot deleted after review.

Sanitized per doctrine, and per Edu's explicit instruction this week — **no conversions figure
of any kind appears in the client copy**, positive or zero. Rebuilt a second time after Edu's
correction to: (1) drop the Google week-over-week comparison table entirely, and (2) make the
Yeti Giveaway launch the lead item of the report instead of burying it — first draft wrongly said
"no changes on our end" for Meta.
- Headline (both intro and Meta section) now leads with the Yeti Giveaway campaign launch.
- Google section keeps the CPC callout ($0.90 → $0.61) as a supporting sentence, no table.
- Awareness described as "continues running as planned" (accurate, per the correction above).
- Next Steps repeats last week's humidity (Google) and hail-response (Meta) ideas since neither
  has been started yet, plus a new bullet to monitor the Yeti campaign's early delivery.

**Status: built, not yet sent to Eve/AM for review.**

---

## 5. Open items (unchanged from Aug 14, still open)

- [ ] Publish the GTM container — GA4 lead tag built in draft, not live.
- [ ] YouTube video ads still point to the homepage, not `/gc-heating-and-cooling/`.
- [ ] Google: build the humidity/dehumidifier ad groups into the paused nonbranded shell.
- [ ] Meta: build the hail-response offer.
- [ ] AM tickets still owed, now four deep: Jul 28 PMax cut, Aug 10 budget ramp, Aug 14 PMax
      redirect, Aug 14 conversion-goal biddable change.
- [ ] ServiceTitan offline import — still the real long-term attribution fix.
- [ ] **New this week:** check the Yeti Giveaway campaign's status/delivery early next week — it
      showed ACTIVE with $0 spent and no impressions yet on the last pull, consistent with a fresh
      launch still ramping, but worth confirming it's actually serving.
- [ ] **New this week:** verify PMax's network/placement mix (Search vs Display/Discover/YouTube)
      before deciding whether the CPC collapse is a good thing or a signal to tighten targeting.
