---
name: tsd-napps
description: "Napps Cooling, Heating & Plumbing (Longview TX): Google 9509605037, LSA 9239407401, Meta 438790276573563; 6-mo review 09-25; split = 65% HVAC / 35% plumbing from 2026-11-01 (was 50/50 since 09-08)"
metadata:
  node_type: memory
  type: project
  originSessionId: 2d1baae8-377e-4a19-b9ca-17a2a8cf2346
  modified: 2026-09-30T11:37:20.243Z
---

Napps Cooling, Heating & Plumbing, Longview TX. Google PPC `9509605037`, LSA `9239407401` (separate, not in contas.yaml), Meta `438790276573563`, GA4 `383876275`. Log in `clients/napps/google-ads-log.md`; 6-month review and investigation in `paid/relatorios/napps/`.

**Service focus, in the client's own words (comments on the 6-mo review, 2026-09-29):** they asked for plumbing only on 6/30, then on 9/8 asked to split HVAC and plumbing **equally**. The 50/50 split went live 09-15 (AC Summer $50/d + TSD_06.05 Plumbing $50/d, Branded $60/d separate). Checked 09-29: still live, spend since 09-15 was even ($801 HVAC / $720 plumbing). AC Summer ran HVAC from 07-21 to 09-08, during the plumbing-only period, with no client re-approval found.

**The client got a rewritten report.** The version they commented on said "plumbing search campaign tightened 8/31" and "search budget entirely on plumbing 9/15". Our HTML said AC campaign and 50/50. Someone edited it before it was sent.

**Missed calls:** the client pushed back on "41 of 87 unanswered" in 2025, and they were right. All 41 were 0-second calls in bursts seconds apart (9 in 15 min on 2025-06-26), on the old non-TSD campaigns. So they were calls that never connected, not calls the staff failed to answer.

**"25 → 55 calls over a minute" is a valid win (Edu, 09-30): real connected calls count wherever they come from.** Internal context only: 31 of the 55 came from Branded, which didn't exist in 2025. Non-branded was flat (25 → 24), and plumbing search went 14 → 0, so that's the number to watch during the equal split.

**Hiring:** both Meta hiring campaigns are PAUSED (last spend 07-02). The client is not hiring, so don't propose relaunching.

**GAQL gotcha:** selecting `ad_group.*` fields on `call_view` silently drops Performance Max rows. The 09-24 investigation said "PMax has zero call_view rows", which is wrong: PMax logged 760 calls from 03-24 to 09-23 (124 of them ≥60s, median 24s), and that volume disappeared after July.

**Why:** the investigation's PMax caveat and the report wording both turned out to be wrong, and this client remembers exact request dates.

**How to apply:** before writing Napps copy, check the current HVAC/plumbing split: 50/50 through 10-31, then 65% HVAC / 35% plumbing from 11-01. Leave `ad_group` fields out of `call_view` queries on accounts that run PMax. Related: [[topserv-client-report-format]], [[tsd-client-message-style]].

**2026-10-05 weekly pass (AT task closed):** $181 CPL, 6 leads; HVAC/plumbing spend still even ($326/$350). Paused 'new air conditioner' (QS1), negatives store/scratch and dent. Open recs for Edu: Branded avg CPC $51.65 (broad brand kws, uncapped Max Conv) → Target IS with $8-10 cap (fulfils the 6-mo review's 'cost controls'); AC Summer $2,017/1 conv in 30d, still summer AC in Oct → rebuild for heating at $50/d; plumbing competitors (Benjamin Franklin etc.) block-or-keep.

**2026-10-19 (Gui weekly + 14-day, staged only):** PPC $816 / 1 conv, NB $1,345 / 0 in 2 weeks, Branded $58 CPC. **All plumbing ad groups land on the homepage (AC on /schedule-now/) though the site has dedicated plumbing/drain/AC/heating pages** → main 14-day rec. Meta awareness targets only ZIP 75605. LSA $145 / 4 msg leads.

**2026-10-22 NB diagnosis (log has detail):** both non-branded campaigns PAUSED 10-22 ~08:55 by someone outside TSD API (who = open question, don't re-enable until known). Expensive conv drivers: ~$846 of ~$2,960 30d NB spend on competitor names (near-phrase from 'plumber available now', which alone = 77% of Plumbing spend), QS 1–3 with landing page BELOW AVERAGE, Max Conv uncapped with ~no conv signal. PPC CPA Oct 1–20 ≈ $903 (3 CallRail wins, all existing customers). Recs pending Edu: competitor negatives, 'plumber available now' → exact, Max Clicks ~$15 cap, review 46–56s calls, LP experience.

**2026-10-22 night:** the pauses were Edu's (web UI): too expensive, he'll request new landing pages and relaunch NB Heating + Plumbing only on them, with the diagnosis fixes (fu-084).

**2026-10-23 client request (via Edu):** starting 2026-11-01, budget split 65% HVAC / 35% Plumbing, keep until the client says otherwise. Replaces the 9/8 equal split. Follow-up fu-092; fu-084 relaunch uses this ratio.
