# Nick's Heating and Air Conditioning — Google Ads log

Google Ads `1854100356` ("Nicks Heating and Cooling"), under Topservdigital MCC `4155514468`. LSA runs
inside the same account. Hammond, LA (Tangipahoa / Northshore). Agency Titan client "Nick's Heating and
Air Conditioning" (`0400fd40-cff2-46eb-ab46-c9befc4f7c7a`). Newest entry on top.

Folder created 2026-10-08. Before this there was no workspace record for Nick's, no Agency Titan 7-day
Google/LSA task, and zero account changes by anyone in the last 30 days (change_event, 09-08 → 10-08).
Campaigns are TSD-named (built Feb–May 2026, before Edu joined).

---

## 2026-10-08 (later) — Lead quality check: are the 30d leads real? (read-only, NO changes)

Window 09-08 → 10-08. Sources: `call_view`, `local_services_lead` + `local_services_lead_conversation`,
`lead_form_submission_data`. PII not copied here.

**Verdict: yes, almost all real.** No spam pattern in any source.

- **Calls from ads (18 counted = calls ≥60s):** 28 calls total (PMax 19, Branded 8, Nonbranded 1). All 18
  counted calls ran 66s–7min from local/regional area codes (985 ×12, 504 ×5, 225 ×3, 601, plus one 469).
  The other 10 were 3 missed and 7 short or hidden-caller-ID calls, none counted. The 3 missed calls were
  PMax calls during business hours (09-10 09:48, 09-11 09:54 and 11:00). Branded calls probably include
  existing customers phoning the office. The API can't separate new from existing.
- **LSA (35 leads, 25 charged):** 18 BOOKED (14 charged), most calls 2+ min. 7 still ACTIVE, i.e. Nick's
  hasn't marked them. 6 of those are 10-05 or later; one is a MESSAGE lead from 09-14 that has sat
  unmarked for 3+ weeks. 10 DECLINED: 6 not charged; of the 4 charged, 1 was credited and 3 were not (calls
  of 25s, 91s and 91s, 09-16). Of the 18 charged leads with an outcome, 14 booked (78%).
- **Google-hosted lead form (2 counted):** 09-20 and 10-04 (plus 09-04, just outside the window). All
  have real names, local phones and Northshore ZIPs (70445, 70435, 70455).
- **Website form ("Submit lead form - web"):** the tag works, just at low volume. Monthly fills:
  Apr 7, May 5, Jun 3, Jul 5, Aug 3, Sep 1 (last 09-13, Branded). The Branded campaign doesn't have the
  form goal as biddable, so that fill wasn't counted. NB had form fills in May (3), Jul (2), Aug (2).
- **Nonbranded's 1 conversion** = a 3-minute call from a 985 number on 09-16. Real, but it's still
  1 lead for $1,257.

**Correction to the entry below:** finding 3 said the web form "fired once in 30d". That's true, but the
tag isn't broken; it fires at low volume. The real tracking gap is no website call tracking.

**Follow-ups for the AM (lead handling, not ads):** 3 missed ad calls during business hours, the 09-14
LSA message still unmarked, 7 LSA leads to mark, and dispute review for the 3 charged DECLINED leads.

---

## 2026-10-08 — First check: full read-only 7-day pass (NO changes made)

**Trigger:** book-wide review found Nick's is an active client (confirmed in the "Client Accounts - Audit
(Master doc)" sheet) with ~$4.8k/30d Google spend and no one checking it.

**Account state**
| Campaign | ID | Type | Bid | Budget/d | Notes |
|---|---|---|---|---|---|
| LocalServicesCampaign | 23344968885 | LSA | Max Conv | $71.43 | Ad schedule Mon–Fri 7:00–16:00 only |
| TSD_02.20_PMAX_Q1 | 23586346547 | PMax | Max Conv | $35 | Final URL /contact-us/, geo PRESENCE_OR_INTEREST |
| TSD_03.22_Search_Branded_Evergreen | 23675600637 | Search | Max Conv tCPA $25 | $100 | Contains a non-brand BROAD kw |
| TSD_05.05_Leads_Search_Nonbranded_AC | 23821497590 | Search | Max Conv (no target) | $40 | primary_status LIMITED |
| TSD_02.20_SEARCH_Q1, TSD_03.22_Search_Branded_Evergreenn | — | Search | — | — | PAUSED |

All Search campaigns: Google Search only (partners/display off). Geo: Amite City, Covington, Hammond,
Mandeville, Madisonville, Ponchatoula (95% of 30d spend from Louisiana). No auto-apply subscriptions.
**Zero negative keywords anywhere** (no campaign negatives, no shared lists). All RSAs approved, all
pointing at the homepage nicksac.com.

**Numbers**
| | 7d (10-01→10-07) | 30d (09-08→10-07) |
|---|---|---|
| LSA | $649 / 7 leads / $93 | $2,313 / 25 / $93 |
| PMax | $257 / 3 / $86 | $1,072 / 12 / $89 |
| Branded Search | $73 / 4 / $18 | $206 / 7 / $29 |
| Nonbranded AC | $372 / 0 / – | $1,257 / 1 / $1,257 |
| **PPC only (excl. LSA)** | **$702 / 7 / $100 CPL, CPC $16.71, CVR 16.7%** | **$2,535 / 20 / $127, CPC $12.01, CVR 9.5%** |

Branded vs unbranded (PPC, 7d): branded 4 leads / $18 CPL; unbranded (PMax + NB) 3 leads / $210 CPL.
Brand keyword IS: "nicks heating and air" 98%, "nicks ac" 100%. Nonbranded IS ~42% (rank-lost 32%,
budget-lost 26%).

Monthly Search + PMax: Jul $2,889 / 39 leads ($74) → Aug $2,573 / 29 ($89) → Sep $2,460 / 20 ($123).
LSA flat at ~22 leads/month, ~$2.15k.

**Findings**
1. **Nonbranded AC is the leak.** $1,257 for 1 conversion in 30d. CPC $24.65 (30d), $46.49 (7d). One
   PHRASE keyword, "air conditioner repair Louisiana", took $856 (68%) for 1 conversion. Max Conversions
   with no target and ~1 conversion/month has no signal to bid on. Visible search terms include
   competitors (professional heating and air, surgis/southern air), supply houses (ferguson hvac,
   trane dealers), car AC ("auto ac repair"), out of area ("hvac metairie") and price research. Only
   $519 of $1,463 Search spend shows as search terms. AC only, nothing for heating going into Nov–Feb.
2. **Branded campaign has a non-brand BROAD keyword**, "hvac contractors near me" (IS 10%). It matched
   ~100 competitor names and supply searches. 4 of the 7 "branded" conversions came from it (one on
   "berthelot's ac and heating"). That inflates the branded numbers and drags the campaign IS to 12%.
3. **Website conversions are nearly invisible.** No website call tracking. "Submit lead form - web"
   fired once in 30d (0 counted). Counted conversions are only Calls from ads, the Google-hosted lead form
   and LSA leads. NB ads land on the homepage, so site calls from NB aren't measured. No GA access
   (per the audit sheet), so we can't cross-check.
4. **LSA is the best channel but only runs Mon–Fri 7am–4pm.** 35 leads in 30d, 18 booked. 3 DECLINED
   leads were charged with no credit (1 other was credited). Check if they're disputable (30-day window).
5. **LSA insurance:** the API shows insurance PASSED (uploaded 2025-12-10, $2M), license PASSED
   (2026-04-09), background PASSED, campaign ELIGIBLE. The audit sheet says the COI expired 2026-08-05.
   Google hasn't acted yet. Get the renewed COI uploaded before it does.
6. PMax: 91% of spend on Search, $89 CPL, budget-lost IS 31%. It also picks up brand searches (26 clicks
   on "nick's heating and air") and competitor names. Geo setting is PRESENCE_OR_INTEREST.

**Recommendations (not applied, Edu to decide; all can be done at constant total budget)**
- NB: pause "air conditioner repair Louisiana", add negatives (competitors, supply houses, car AC,
  out of area, price research), and cap bids (Max Clicks with a CPC cap, as on Zen Air) until conversions
  come back. Consider moving part of NB's $40/d to PMax (budget-limited at $89 CPL).
- Branded: pause the BROAD "hvac contractors near me" in the branded campaign.
- PMax: geo to PRESENCE.
- LSA: ask the AM if Nick's takes calls evenings/weekends, review the 3 charged DECLINED leads for
  dispute, chase the renewed COI.
- Tracking: request GA access, check the GTM form tag, add website call tracking.
- Ask for Agency Titan 7-day Google Search + LSA tasks for Nick's.

**Open items**
- [ ] Edu: approve/decline the changes above.
- [ ] AM: renewed COI, weekend/evening hours, GA access.
- [ ] Heating coverage for NB (Nov–Feb).
