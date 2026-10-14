# Gillespie's Heating and Cooling — Internal Optimization Log
## Week ending Friday 2026-08-21

**INTERNAL ONLY.** First weekly report ever built for this client. Client-facing version is
`Gillespies-Heating-Cooling-Weekly-Update_2026-08-21.html` / `.pdf`, same plain format as
GC Home Service.

Data pulled 2026-08-21 via Ratos (`read.py campaigns/ad-groups/ads/search-terms`) for Google
Ads `7410489772`, and via the Meta MCP (`ads_get_ad_accounts`, `ads_get_ad_entities`) for Meta
`2014320269203822`.

---

## 1. First pass missed the Meta account entirely

Built the first draft of this report off the workspace's existing Gillespie's docs
(`google-ads-log.md`, `gtm-log.md`), which only cover the Google Search build launched 08-18.
Reported "no Meta presence, nothing built yet." **Wrong** — Edu corrected it immediately
("we have a campaign on Meta"). Checked live via the Meta MCP instead of trusting the absence of
a workspace log and found a real, active campaign that predates this workspace's Gillespie's
folder entirely: `Lead Gen | HVAC | NKY & Cincinnati | Jul 2026`, running since July 2026, in an
ad account owned by Gillespie's own Meta business (`1728244028382959`), not Topservdigital's —
which is exactly why it never surfaced in any TSD-side doc. Saved as a standing lesson:
[[tsd-verify-meta-account-live]].

Rebuilt the report with real Meta numbers before sending. See `meta-ads-log.md` for the full
account inventory (campaign/ad set/ad breakdown, creative list).

## 2. Google Ads — first four days live (08-18 to 08-21)

| Campaign | Impr. | Clicks | Cost | Conversions |
|---|---|---|---|---|
| Non-Branded | 201 | 12 | $106.57 | 1 |
| Branded | 0 | 0 | $0.00 | 0 |

Ad group breakdown (non-branded): HVAC-General-Company (catch-all, `/` final URL, $18 CPC
ceiling) took 104 impr / 7 clicks / $77.06 of the $106.57 total — the majority of spend and the
one recorded lead. Furnace-Heating-Repair, Heat-Pump-Services, and AC-Repair-Install split the
rest thinly (2, 1, and 2 clicks respectively).

**Search terms flag, not yet actioned:** pulled the full search-term list for the week.
HVAC-General-Company (the catch-all group) is already picking up competitor brand names
(Anderson Heating and Cooling Cincinnati, Reinhart Heating and Cooling Alexandria KY, Logan
HVAC/A&C, Thomas and Galbraith, Golden Rule HVAC, Premier Heating and Air, Reliant Heating and
Air Dallas) and off-target/research queries (wholesale distributor searches like "johnstone
supply," car AC repair, manufacturer-name research like "daikin furnace" / "payne furnace" /
"120 btu furnace" with no local-service intent). None of this is in the client-facing report —
worth a negative-keyword pass before this ad group scales further, since it's both the highest
CPC ceiling and the only one with a homepage (not a service-page) final URL.

Branded campaign at 0 impressions in 4 days is expected given ~10/mo Keyword Planner volume on
brand terms and the short window — not a delivery or policy problem, confirmed all 5 RSAs are
`REVIEWED` / `APPROVED`.

## 3. Meta Ads — this week vs lifetime

| | Last 7 days | Lifetime (since Jul launch) |
|---|---|---|
| Impressions | 11,784 | 35,358 |
| Clicks | 241 | 764 |
| Spend | $337.92 | $1,062.93 |
| CPC | $1.40 | $1.39 |
| Cost per lead | $112.64 | $96.63 |
| Leads (derived) | ~3 | ~11 |

Single ad set (`NKY & Cincinnati | 30+ | Instant Form | $50/day`), native Meta Instant Form lead
ads — leads captured inside Meta, not via website pixel, which is why the GTM container's still-
filler Meta Pixel ID (noted in `gtm-log.md`) hasn't blocked lead capture on this channel. Would
still matter for any future website-conversion or retargeting use.

Five ads in rotation, four active + one paused (`Heat Pump & Mini-Split`, retired). All five are
bottom-funnel direct response (testimonial, seasonal tune-up offer, value prop, repair-vs-
replace) — **no awareness-stage creative anywhere in the account**, and frequency already at 2.71
over just this week on the one always-on ad set. Edu's explicit ask: **bring an awareness-layer
Meta campaign as a recommendation next time we talk to this client.** Written into the report's
Next Steps and logged in `meta-ads-log.md` so it isn't lost.

## 4. Client report

Built as `Gillespies-Heating-Cooling-Weekly-Update_2026-08-21.html` / `.pdf`, same plain
Times-New-Roman one-page format as GC Home Service. Rendered via Brave headless
(`--print-to-pdf`) since system Chrome isn't installed on this machine — same fallback GC's
08-21 report used. One page, confirmed via `mdls kMDItemNumberOfPages`.

Sent directly to Edu (not yet routed to Eve/AM for review — first-ever report for this client,
no established review step in this workspace yet).

---

## 5. Open items

- [ ] Add negative keywords to Google's HVAC-General-Company ad group (competitor brand names +
      research/wholesale-intent queries) before it takes a larger share of the small non-branded
      budget.
- [ ] Confirm with Edu/AM whether TSD is meant to be actively managing the Meta account, or
      whether it predates the engagement and needs a proper scope/budget-approval handoff — same
      written-approval rule as Google.
- [ ] Propose the Meta awareness-layer campaign at the next client touchpoint (see above).
- [ ] Decide the paused `Heat Pump & Mini-Split` Meta ad's fate — resume, replace, or leave
      retired.
- [ ] Real Meta Pixel ID still filler in the GTM container — fine for now (Instant Form doesn't
      need it), but blocks future website-conversion tracking or retargeting builds.
- [ ] Written budget approval on file with the AM for the Google $80/$80 → $3.62/$32.57 cut,
      same pattern as other budget moves logged elsewhere in this workspace (Edu authorized
      directly on 08-18).
