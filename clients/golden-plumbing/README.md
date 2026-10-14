# Golden Plumbing — internal log

**Google Ads (PPC):** `4193142570` — "Golden Plumbing", USD, MCC Topservdigital 4155514468.
LSA lives in the **same account** (campaign `21051260085`, LOCAL_SERVICES) — not a separate customer ID.

Conversion tracking is `CONVERSION_TRACKING_MANAGED_BY_SELF`, conversion_tracking_id **16474870397**,
`google_ads_conversion_customer` = itself. So tracking is owned by this account, not the MCC — any
config change was made inside this account.

Note: the website conversion tags are named **"Gardner's Plumbing (web) …"**. There is also a
separate, never-used **"Golden Plumbing (web)"** tag family (all HIDDEN, zero conversions all time).
Worth confirming with the AM which brand the site actually runs under.

---

## Ticket 2026-07-21 — client asked to pause all PPC + wants an ROI report

Two asks from the client:
1. Pause all PPC campaigns and spend immediately.
2. Comprehensive report of results vs investment — they believe ROI is negative.

### Pause status — verified 2026-07-21

**All PPC is already paused.** Every Search + PMax campaign shows `PAUSED`, and the last day with any
PPC spend was **2026-07-17**. Nothing to pause.

**LSA is still live and spending** — `21051260085` at ~$500-750/day, $745.81 on 2026-07-20.

> **Edu's call 2026-07-21: do NOT pause LSA. This report covers PPC only.**
>
> Flag for the AM: the client's ticket says "all PPC campaigns and associated ad spend." If they
> meant *everything* including LSA, that needs explicit written confirmation before anyone touches
> it. Budget changes need written client approval via AM ticket anyway.

---

## THE TRACKING BREAK — what is actually provable

Earlier framing of "April 1" was wrong; that was an artifact of looking at monthly buckets.
Day-level data shows **two separate hard cliffs in March**, ten days apart, and they group
**perfectly by conversion-action `origin`** — not by campaign.

### Cliff 1 — 2026-03-10: every WEBSITE-origin "Gardner's Plumbing" tag

| Action (origin = WEBSITE) | First fire | **Last fire** |
|---|---|---|
| Gardner's (web) ghl_contact_us | 2025-05-05 | **2026-03-01** |
| Gardner's (web) schedule_button-click | 2025-04-15 | **2026-03-09** |
| Gardner's (web) book_now_link_click | 2025-04-20 | **2026-03-10** |
| Gardner's (web) phone_link_click | 2025-04-22 | **2026-03-10** |
| Gardner's (web) estimate_link_click | 2025-05-02 | **2026-03-10** |

Zero every single day from 2026-03-11 onward. Not a taper — a cliff.

### Cliff 2 — 2026-03-20: every GOOGLE_HOSTED action

| Action (origin = GOOGLE_HOSTED) | First fire | **Last fire** |
|---|---|---|
| Clicks to call | 2025-04-09 | **2026-03-19** |
| Local actions - Other engagements | 2025-04-09 | **2026-03-20** |
| Local actions - Directions | 2025-04-14 | **2026-03-20** |
| Local actions - Website visits | 2025-04-08 | **2026-03-20** |

Healthy right up to the end (23 conversions on Mar 19), then zero forever from Mar 21.
These are Google Business Profile–driven → points at the **GBP link being severed or local assets
removed** around Mar 19-20.

### Still firing (proves it is not a total teardown)

| Action | Origin | Status |
|---|---|---|
| Calls from ads | CALL_FROM_ADS | alive through 2026-07-15 |
| Submit lead form - Web | WEBSITE | started 2026-02-18, alive through 2026-07-11 |
| local_services_phone_lead / message_lead | LSA | alive, current |

**`Submit lead form - Web` is WEBSITE-origin and survived.** So the site did not lose its Google tag
entirely — the *Gardner's tag family specifically* stopped. That narrows it to those tags being
removed/unlinked (site rebuild, GTM container change, GA4/tag unlink), not a blanket gtag deletion.
Its start on Feb 18, three weeks before Cliff 1, is consistent with a tracking migration where the
new setup went in and the old family was later torn out — but that is a hypothesis, not proven.

### What I could NOT determine, and where the answer lives

**The specific human action is not recoverable through the API.** `change_event` is hard-capped at
30 days (`START_DATE_TOO_OLD`); March 2026 is out of reach. So I can prove *what* broke, *when*, and
*which layer* — but not *who did what*.

To close it:
- **Google Ads UI → Tools → Change history**, filtered to **Mar 1–25 2026**. The UI retains far more
  history than the API. Look for conversion-action edits, tag removal, and Business Profile unlink.
- **GTM container version history** for the site around **Mar 9-10 2026**.
- **Google Business Profile** — confirm whether it is still linked to the Ads account (Cliff 2).

---

## Second, independent problem: no revenue signal, ever

`ServiceTitan – Booked Job` (type CONVERTED_LEAD) exists but has **never recorded a single
conversion, all time, any campaign**. It is also `primary_for_goal = False`.

No conversion carries a revenue value anywhere in the account — everything is a $1 placeholder.

**The client's "ROI is negative" claim cannot be confirmed or refuted from Google Ads.** Nobody can
compute ROI here and never could. Any ROI number would be fabricated. Real answer needs a
ServiceTitan revenue-by-source export.

Same shape as the Mission Accomplished / ServiceTitan escalation — ST action exists, not Primary,
not receiving data. See `clients/mission-accomplished/servicetitan-marketing-pro-escalation.md`.

## Third problem: `include_in_conversions_metric = False` on most primary goals

Almost every ENABLED, `primary_for_goal = True` action is excluded from the `conversions` metric:

- `include=False, primary=True`: phone_link_click, schedule_button-click, ghl_contact_us,
  estimate_link_click, Local actions ×3, Clicks to call
- `include=True`: only local_services ×2, Calls from ads, book_now_link_click, Submit lead form - Web

So the column Smart Bidding optimizes toward has never matched the actions marked primary. This is
why `metrics.conversions` and `metrics.all_conversions` diverge so hard (e.g. Search_HVAC_Calls:
75.2 vs 566.6). Independent of the March break and needs fixing too.

## Fourth: goals polluted with non-leads

`Local actions - Website visits` (PAGE_VIEW), `- Directions` (GET_DIRECTIONS), `- Other engagements`
(ENGAGEMENT) are all set Primary. Not leads. **358 soft actions in P1 alone** were inflating the
pre-break picture — so the $11.63 P1 CPL was flattering, and the true gap between phases is
narrower than raw numbers suggest.

Net: the account over-reported before March 10 and under-reported after.

---

## Investment — PPC only, LSA excluded

Split at the **real** break dates:

| Phase | Window | Days | Spend | $/day | Clicks | CPC | Recorded leads | CPL |
|---|---|---|---|---|---|---|---|---|
| **P1** tracking intact | Dec 15 – Mar 10 | 86 | $6,977.10 | $81.13 | 2,512 | $2.78 | 600 | $11.63 |
| Transition (web dead, local alive) | Mar 11 – Mar 20 | 10 | $932.51 | $93.25 | 155 | $6.02 | 19 | $49.08 |
| **P2** both families dead | Mar 21 – Jul 17 | 119 | $11,338.24 | $95.28 | 2,836 | $4.00 | 112 | $101.31 |
| **Total TSD PPC era** | Dec 15 – Jul 17 | 215 | **$19,247.85** | $89.52 | 5,503 | $3.50 | 731 | $26.34 |

Pre-TSD legacy PPC (Sep 2024 – Jul 2025): $24,015.07. **PPC lifetime total: $43,262.92.**
Account lifetime incl. LSA = $107,687.89. LSA alone = $64,424.97 / 791 leads / $81.44 CPL.

**The key comparison: P1 vs P2 bought nearly the same traffic.** 2,512 clicks vs 2,836 clicks, at
similar daily spend. Recorded leads went 600 → 112. **505 of P1's 600 leads (84%) came from tags
that later died.** That is the bulk of the apparent collapse.

CPC did genuinely rise $2.78 → $4.00, and PMax impressions decayed sharply after ~Mar 23 — consistent
with Smart Bidding starved of conversion signal. So there is real damage on top of the reporting gap.
The two are not separable with available data. **Do not present $101 as a true CPL.**

Per-campaign, TSD era:

| Campaign | Spend | Clicks | CPC | Leads | CPL |
|---|---|---|---|---|---|
| TSD_04.30_Calls_Nonbranded_Evergreen | $9,173.28 | 2,290 | $4.01 | 83 | $110.52 |
| TSD_02.19_Pmax | $4,829.50 | 1,616 | $2.99 | 281 | $17.17 |
| TSD_04.07_Search_HVAC_Calls | $4,131.33 | 1,443 | $2.86 | 354 | $11.68 |
| TSD_04.30_Search_Branded_Evergreen | $691.71 | 99 | $6.99 | 9 | $76.86 |
| TSD_03.17_Search_Branded_Evergreen | $278.37 | 35 | $7.95 | 3 | $95.54 |
| TSD_03.17_Search_NonBranded_Evergreen | $143.66 | 20 | $7.18 | 1 | $143.66 |

Note the campaign-level CPLs are distorted by the same break: the two "good" CPLs (PMax $17.17,
HVAC_Calls $11.68) are campaigns that ran mostly *before* Mar 10; Calls_Nonbranded ($110.52) only
started Apr 30, entirely inside the blind window.

---

## Open items

- [ ] **Pull Google Ads UI change history for Mar 1–25 2026** — only place the specific cause lives.
- [ ] Check GTM container versions around Mar 9-10.
- [ ] Confirm whether GBP is still linked to the Ads account (Cliff 2, Mar 20).
- [ ] Confirm with AM whether "all ad spend" was meant to include LSA. **Written approval required.**
- [ ] Get revenue-by-source from ServiceTitan — only path to a real ROI answer.
- [ ] Fix `ServiceTitan – Booked Job`: get it receiving data, set Primary.
- [ ] Fix `include_in_conversions_metric` on the primary actions.
- [ ] Demote `Local actions - *` from Primary to Secondary.
- [ ] Confirm the "Gardner's Plumbing" vs "Golden Plumbing" brand naming on the web tags.
