---
name: tsd-napps
description: "Napps Cooling, Heating & Plumbing (Longview TX): Google 9509605037, LSA 9239407401, Meta 438790276573563; 6-mo review 09-25; client wants HVAC/plumbing EQUAL since 09-08"
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

**How to apply:** before writing Napps copy, check the current HVAC/plumbing split and describe it as equal. Leave `ad_group` fields out of `call_view` queries on accounts that run PMax. Related: [[topserv-client-report-format]], [[tsd-client-message-style]].

**2026-10-05 weekly pass (AT task closed):** $181 CPL, 6 leads; HVAC/plumbing spend still even ($326/$350). Paused 'new air conditioner' (QS1), negatives store/scratch and dent. Open recs for Edu: Branded avg CPC $51.65 (broad brand kws, uncapped Max Conv) → Target IS with $8-10 cap (fulfils the 6-mo review's 'cost controls'); AC Summer $2,017/1 conv in 30d, still summer AC in Oct → rebuild for heating at $50/d; plumbing competitors (Benjamin Franklin etc.) block-or-keep.
