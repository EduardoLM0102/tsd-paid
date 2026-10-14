---
name: tsd-proud-pops-impression-share
description: "Proud Pops PPC (1051843378) impression-share analysis: bottleneck flipped budget->Ad Rank post-rebuild; the 4 opportunities + the built Change 1 (General Plumber ad group) staged as a script"
metadata: 
  node_type: memory
  type: project
  originSessionId: c664d008-17ae-42b8-9ddf-4d1dc40d4779
  modified: 2026-07-30T19:38:51.730Z
---

Impression-share opportunity work on Proud Pops PPC acct **1051843378** (done 2026-07-27, data LAST_30_DAYS + 6-mo trend via `google-ads-ratos` skill, TSD profile). Builds on [[tsd-proud-pops]] / [[tsd-proud-pops-tracking]]. Client cluster + access in [[topserv-google-ads-location]].

**Headline finding — the bottleneck FLIPPED from budget to Ad Rank after the 2026-05-14 rebuild.** The rebuild reset Quality Score history. Monthly Search IS trend: Feb–Apr ~37–40% lost to BUDGET / ~33–38% to rank; by Jun–Jul budget-lost collapsed to 7–10% and **rank-lost exploded to ~78%**. So the old "budget-limited 17 of 18 months" read is stale — **more budget now buys almost nothing; QS is the only lever.** Search IS sits at 13–17% across search + PMax (showing ~1 in 6–7 auctions), so headroom is huge but gated behind Ad Rank.

Last-30d by campaign (SearchIS / LostBudget / LostRank): Plumbing Search 15.0 / 3.5 / **81.6**; Electrical Search 13.3 / **29.5** / 57.2 (only one still genuinely budget-limited, but priciest at ~$10.94 CPC); HVAC PMax 17.0 / 15.7 / 67.3; Electrical PMax 15.5 / 11.0 / 73.5. Bid strategy = MAXIMIZE_CONVERSIONS (so no CPC bids to set — QS is everything). Caveat: PPC `conv` column is ~0 since Apr because web tags are dead ([[tsd-proud-pops-tracking]]); judge leads only from LSA/call data.

**QS component diagnosis (Plumbing Search):** expected CTR is **Below Average on EVERY keyword** = the dominant leak. Ad relevance mostly fine, landing page mostly Average (Below only on the money term "plumber san antonio tx", which points at the generic proudpops.com homepage — ties to the site fix).

**The 4 opportunities I gave Edu (ranked):** (1) Plumbing Search — rehome generic plumber terms + fix QS (highest leverage, cheap ~$3.64 CPC clicks); (2) landing pages — all ads point at proudpops.com homepage, dedicated pages lift the LP score, same site work as the tracking fix; (3) competitor negatives — ~$290/mo bleeding on rival brand searches (george's, quarter moon, zeus, infinity, bryco, shafer, elbel, primo, anchor, vamvoras, elmer zubiate) at 0 conv, and they tank expected CTR; (4) build an ad group around the only converters ("plumbing contractors in my area" / "in my area").

**Change 1 — BUILT & STAGED as a script (not yet run; my live-account writes are blocked by the permission classifier, Edu runs it):** `topserv-workspace/clients/proud-pops/change1_plumber_general_adgroup.sh`. Creates ad group **AG4_Plumbing_General** (PAUSED) in campaign 23853484024 with an on-theme homeowner-voice RSA (15 headlines / 4 descriptions, url proudpops.com, path Plumber/San-Antonio) + the 3 generic keywords: "plumber san antonio" EXACT, "plumber near me" EXACT, "plumber san antonio tx" PHRASE. Then a separate commented CUTOVER block enables AG4 and pauses the 3 originals in AG1_Plumbing_LeakDetection (ad group 196726297659): kw ids 354371636767 ("plumber san antonio tx" PHRASE, the QS-3 $20.66-CPC 36%-of-spend monster), 1178376016 ("plumber san antonio" EXACT), 21810437552 ("plumber near me" EXACT). Everything auto-creates PAUSED so the build has zero live impact until cutover. RSA copy follows [[tsd-client-facing-voice]].

**Open:** Edu will run the script later; after cutover goes live, confirm it and consider tackling opportunities 2–4. Offered to write the full restructure + competitor negative list as the next build.

---

**UPDATE 2026-07-30 — the bottleneck flipped BACK to budget.** The GTM conversion fix (live v38, Jul 23) worked: every conversion in the trailing 30d landed in the last 8 days (Jul 22–29), so Maximize Conversions stopped bidding at the floor and Ad Rank recovered. Rank-lost IS fell 20–28 pts and budget-lost roughly doubled. Clean post-fix window Jul 22–29 ($/day, conv, CPA, IS/lostBudget/lostRank): PMax Electrical $61.9 / 16.5 / **$30** / 14.6-41.0-44.4; PMax HVAC $85.6 / 18.5 / **$37** / 14.7-25.5-59.8; Search Electrical $51.0 / 5.0 / $82 / 10.2-46.9-42.9; Search Plumbing $84.3 / 3.0 / **$225** / 15.0-44.4-40.6. PPC total $283/day, 43 conv, blended CPA $52.62 (cost per *tracked lead*, NOT validated vs ServiceTitan booked jobs). **So §13 above is stale — more budget now DOES buy volume.** Full analysis for the approved $50k Aug pool in `clients/proud-pops/budget-allocation-2026-08.md` — see [[tsd-proud-pops-aug-budget]].
