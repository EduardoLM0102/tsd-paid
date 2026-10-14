---
name: tsd-client-roster-status
description: Edu's 2026-09-29 confirmations of which ambiguous MCC/Meta accounts are current TSD clients, and known takeover dates
metadata:
  type: project
---

Confirmed by Edu on 2026-09-29 (during the Growth Engine pull, see [[tsd-growth-engine-brandformance]]):
- **Current clients not yet in the workspace:** Strickland Heating & Air (Google 9049508615, DFW, mostly Search + PMax) and Integrate Comfort Systems (Google 4571881760 + LSA 2895702982 / 2175964343 / 8323145223, New York DMA). The 09-11 "diligence only" note only covered the Belleville LSA account; the main account has TSD-named campaigns since 2026-03-22, and "ICS" = Integrate Comfort Systems (so Meta account "ICS" 2070047533283360, connector-disabled, is likely theirs). Open: whether TSD runs "Mitsubishi YouTube" in 2895702982 (only visible editor chriswisics@gmail.com).
- **Not current clients:** Gray Duct Technologies (Google LSA 6191956550, Minneapolis) and Concrete Adventures (Google 9215192296, Memphis/MS).
- **Takeovers inside the last 12 months (weeks before these dates were run by someone else):** On The Way, Google, before the 2026-09-09 TSD build; On Time Service Pros, Meta, before March 2026 (its ad account is owned by "TMD Management Group"). Proud Pops was TSD for the full 12 months.
- Still unknown: Meta 532145676808452 (business "Wattenbarger Racing", HVAC ads, TSD naming) and 170464733924961 ("Allen Black"); Google 8655979348 (unnamed LSA, Long Island NY), DFW _Unsuspended, Potomac, Supreme AC, Modern Comfort, AC Cornerstone, Ultimate Comfort LSA.
- All Heart is offboarded, but its 4 Google LSA accounts (9976029542, 8199337860, 5064174352, 7662998005) were still spending under the TSD MCC as of 2026-09-27.

**Why:** the MCC and Meta business hold many accounts with no workspace record, and scope decisions (what counts as "our clients") change book-level numbers.

**How to apply:** for any book-wide pull, start from `paid/relatorios/growth-engine-pull-2026-09/client_roster.csv` (status + tsd_managed_since per account) instead of treating "spent recently" as "current client".

**2026-10-07 (Edu):** On The Way is no longer counted as current (likely offboarding). Meta "ICS" 2070047533283360 = Integrate Comfort Systems (current; Ads MCP not enabled on it, only the agency token reads it). Rhino FB Ads Account 849885463684603 is unconfirmed (Oklahoma, owned by the Topservdigital business). It is NOT Lily Pad, even though Edu guessed it was.

**2026-10-08 change-history pull (30d, read-only) raised three questions for Edu:**
- **Strickland (9049508615):** every edit in 30 days is by `@onpurposemedia.com` (budgets 09-09 and 09-25, Branded status 09-25). All TSD_ campaigns are PAUSED; only `Cooling` + `Pmax - AC` (On Purpose Media names) run, ~$4.4k/30d. Looks like another agency runs Google, not TSD.
- **Nick's Heating (1854100356):** ~$4.8k/30d spend, zero changes by anyone in 30 days, no workspace folder, no Agency Titan 7-day task.
- **Live Wire:** Trade Vulcan took it over, see [[tsd-live-wire-electric]].
Only 13 clients have the AT 7-day Google + LSA tasks (All Seasons, C&S, Gillespie's, Hawkins, King's, Lilypad, Live Wire [stopped 09-21], MA, Napps, On The Way, Spencer, Watt's Right, Zen Air). Proud Pops, Neon Monkey, Golden Plumbing, Integrate, Strickland, Nick's, Cool Hand, GC Home Service and Eaglepoint have none.

**2026-10-08, accounts with NO AT 7-day task and how often we actually looked (Google + LSA):** Nick's (never logged, $4.8k/30d), My Favorite Service Co 9815330464 (Proud Pops' merged brand, 5 live campaigns, $1.8k/30d, not looked at since the July budget analysis), Golden Plumbing LSA (nothing logged since 07-21, LSA $0 in last 7d), Integrate (one-off checks 09-11/09-29/10-07, not found in AT by name), Proud Pops PPC + its LSA accounts (ad hoc ~every 10 days), Neon Monkey (ticket-driven only), Cool Hand (ticket-driven since 09-24). Eaglepoint is in AT as "Eagle Point Roofing and Exteriors" with 0 processes and $0 spend. Strickland is not in AT by name.

**2026-10-08 (Edu), latest status, overrides anything above:** GC Home Service = OFFBOARDED. Gillespie's Heating and Cooling = OFFBOARDED. On The Way = offboarding in progress (Edu "believes"). Golden Plumbing = ON FREEZE (not offboarded, not actively managed, not an "unchecked" gap). Integrate Comfort Systems is named "ICS" in Agency Titan (client id 1e439ca7-d2e8-4cd9-997d-70e654739ff5). Nick's Heating = ACTIVE (per the Client Accounts audit sheet, [[tsd-client-accounts-audit-sheet]]; LSA flagged for an expired COI since 08-05, but LSA was still spending as of 10-08). AM notes in that sheet: On The Way terminates 11/2/2026, On Time Service Pros terminates 10/16/2026. Still include all three when describing the weekly cadence and past work (they were on the 7-day cycle), but label them offboarded/offboarding and leave them out of current-client counts and new recommendations.

**2026-10-08 (Edu, LP rollout list):**
- Keep Strickland "just in case" and keep Live Wire in client lists, despite the On Purpose Media and Trade Vulcan edits.
- My Favorite Service Company = Proud Pops. Disregard it as a separate client.
- The active-clients source Edu points to is the "Client Accounts - Audit (Master doc)" sheet ([[tsd-client-accounts-audit-sheet]]). Cross-check book-wide lists against it.
