---
name: tsd-meta-ads-methodology
description: "Eduardo's Meta Ads method (CBO, one angle per DCT ad set, post ID isolation, Advantage+ only, always-on Ad Recall Lift awareness) — the doctrine behind every Meta build he does"
metadata: 
  node_type: memory
  type: project
  originSessionId: bd678abb-0ca3-4a79-8b13-48930b7ac06a
  modified: 2026-10-09T13:24:09.637Z
---

Eduardo's own Meta Ads methodology, as Head of Paid Ads at TopServ Digital. Full SOP lives in `~/Documents/GitHub/topserv-workspace/paid/sops/meta-ads-launch-buildout.md` (markdown is the source of truth; HTML/PDF are built from it).

- **Always CBO.** Budget at campaign level, never ad set. Spend is the algorithm's vote and that's the signal he reads.
- **One angle = one DCT ad set.** Each Dynamic Creative ad set carries ONE angle: 3 creatives (iterations of that same angle, same format), 2 headlines, 2 primary texts — all arguing that one angle. Angles run as parallel ad sets in the same CBO and compete for budget. He tests **offer/angle**, not layout.
- **No proven winners in the account → 100% testing.** Account with isolated post IDs → winners keep running in their isolated ad sets, testing runs alongside on a smaller budget share.
- **Winner isolation = reuse the original POST ID** so accumulated social proof and learning carry over. Never rebuild the winner as a new ad.
- **Kill rules:** didn't spend → dies (algorithm found it irrelevant vs. the others). Spent little → dies. Spent but only 1–2 leads (or few leads relative to total volume, in accounts that already have isolated post IDs) → dies.
- **Targeting:** Advantage+ on EVERYTHING. Never interests/behaviors/detailed targeting. Geo only (people *living in* the location), age at most as a *suggestion*. If a campaign underperforms, the fix is the offer/angle/creative, never a narrower audience.
- **Awareness campaign always on, in parallel:** objective Awareness optimized for **Ad Recall Lift** (not reach, not impressions), with video and statics purpose-built for branding/brand recall — never recycled conversion creative. Not judged on CPL. 5–10% of budget.
- **Frequency target on awareness: ~3x/week.** A rising or high frequency is not a fatigue red flag on its own — it's the goal, since recall needs repeated exposure. The actual failure mode is frequency *not* reaching or holding near 3x/week (or reach going flat while frequency climbs only because the audience isn't expanding) — that's the read to act on, not "frequency is climbing" by itself. Always check reach alongside frequency: reach growing while frequency holds steady/near-target is healthy (new people entering at a healthy exposure rate), not a warning sign.
- **Awareness campaigns NEVER get a frequency cap** (Edu, 2026-10-09: "we CANNOT have a frequency cap, we need at least 3x/week"). Not "raise it", none at all. Note: ARL has no minimum-frequency control (Meta's target frequency only works with Reach/ThruPlay + lifetime budget), so ≥3x/week is monitored, not forced. Meta locks frequency controls once a CBO campaign starts, so removing a cap = new campaign. Mechanics in [[tsd-meta-mcp-write-mechanics]].

**Why:** this is his own doctrine, not something written in the TSD playbooks — the ADS Playbook v3.1 only has the 90-95/5-10 budget split. Do not invent Meta structure for him; use this.

**How to apply:** any Meta build, SOP, brief, or creative/copy spec for TSD follows this. Copy specs must be 2 primary texts + 2 headlines *per angle*; creative specs 3 iterations *per angle*, same format. Related: [[topserv-google-ads-location]], [[topserv-client-report-format]].
