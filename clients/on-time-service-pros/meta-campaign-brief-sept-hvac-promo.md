# Meta Campaign Brief — September HVAC Promotion
**Client:** On Time Service Pros (OTSP) — Rosemount, MN
**Prepared by:** Eduardo, Paid Ads
**Date:** 2026-08-10
**Ticket priority:** High · Client approved: Yes · Needed by: Monday 2026-08-17
**Target launch:** Week of Aug 24–25, 2026
**SOP reference:** `paid/sops/meta-ads-launch-buildout.md` — this is the Stage 4 output (Market, Offer & Audience Research). Stages 1–3 status is called out below since this is OTSP's first Meta build.

---

## 0. Account status — read this first

OTSP is **not yet in the TSD paid book.** Confirmed 2026-08-10: no Google Ads CID, no LSA CID, no ads budget on file in AT. The client card also shows **no Facebook Pixel ID** and no Meta CID recorded.

That makes this a **Stage 1–3 build, not just Stage 4.** Before Stage 7 (buildout) can start, we need, from the AM:

1. **Meta Business Manager + Ad Account access confirmed** (or the "Create Meta Ads Account" process fired now — it's on the critical path).
2. **Pixel / Conversions API** — installed and firing on ontimeservicepros.com, or built fresh. Verify with Test Events, not assumption.
3. **Written monthly budget approval** — nothing in AT yet. Needed before Stage 7.
4. **Conversion event + CRM routing** — ServiceTitan + CallRail are both already in place (confirmed in AT), which is the hard part done. We still need the Meta lead event wired into that flow and Verified Live if GHL touches it.

**Timeline math:** brief closes Mon Aug 17 → buildout the week of Aug 18 → launch week of Aug 24–25 is 5–7 business days from a complete intake. That's inside the SOP's 6–8 business day native-form estimate, but only if #1–#3 above are moving **in parallel this week**, not queued behind this brief. Recommend the AM opens the access/tracking request today rather than waiting for brief sign-off.

---

## 1. Offer & angles

Two angles, per the client's brief — mapped to the TSD one-angle-one-DCT-ad-set method:

| Angle | Offer | Ticket value | Role |
|---|---|---|---|
| **A — Tune-Up** | $49 Furnace Tune-Up | ~$385 avg service ticket | Volume, low-friction, seasonal urgency |
| **B — Install** | 30% Off Furnace & AC Installation | ~$13,500 avg install ticket | High-ticket, fewer conversions, each one is worth ~35x a tune-up |

**No proven Meta winners exist for this account** (State A in the SOP) — this launches 100% testing on both angles. No post IDs to isolate yet.

**Hypotheses:**
- *Angle A:* We believe homeowners in the target ZIPs respond to a low-cost preventative-maintenance offer before the Minnesota heating season because it removes the price barrier to "check the furnace before it fails in January." We'll know we're right if Angle A's CPL lands near or under the $385 service ticket's economics and out-earns Angle B on spend share inside the CBO.
- *Angle B:* We believe homeowners with 26+ year old homes (OTSP's own ICP: Replacement Era + Heritage/Vintage) respond to 30% off a full install when it's paired with financing, because the barrier on a $13,500 purchase is monthly payment, not the discount alone. We'll know we're right if Angle B produces even a small number of qualified leads — the math tolerates a much higher CPL than Angle A (see §3).

---

## 2. Campaign structure

**Two separate CBO conversion campaigns**, not two ad sets inside one campaign. Reason: the client's brief specifies a fixed 80/20 split by strategic intent (fill the pipeline cheap, then upsell installs), not a split we want the algorithm to discover. Inside a single CBO, Angle A's much lower CPL would out-compete Angle B for spend almost immediately and could starve the install offer below the SOP's kill-rule threshold before it ever gets a fair read. Two campaigns lets each angle keep its own CBO-managed budget while still following the doctrine (budget always at campaign level, never ad set).

```
OTSP — Meta / Sept 2026
├── Campaign 1: TSD_09.XX_Leads_TuneUp49_Sept        [CBO, 80% of conversion budget]
│     └── Ad Set: Angle A — $49 Tune-Up                [DCT: 3 creatives / 2 headlines / 2 texts]
├── Campaign 2: TSD_09.XX_Leads_Install30Off_Sept     [CBO, 20% of conversion budget]
│     └── Ad Set: Angle B — 30% Off Install             [DCT: 3 creatives / 2 headlines / 2 texts]
└── Campaign 3: TSD_09.XX_Awareness_RecallLift_Sept   [Awareness, Ad Recall Lift, 5–10% of TOTAL]
```

If Angle A's volume is strong enough by the Day 7 check to justify it, Campaign 1 can be split into two DCT ad sets in a later round (e.g. an urgency angle vs. a value angle) to keep testing inside the winning offer — not at launch, since day-1 splitting would thin each set below a meaningful read.

**Budget split** (percent of the *approved* monthly figure — no dollar number is on file yet, so this is expressed as ratio per the client's brief until the AM returns one):
- **90–95%** conversion (SOP standard) → split **80% Campaign 1 / 20% Campaign 2** inside that pool
- **5–10%** Awareness, always on, Ad Recall Lift objective, never judged on CPL

**The math that justifies the 80/20, not just the client's instruction:** a service-ticket lead is worth ~$385; an install-ticket lead is worth ~$13,500 — roughly 35x. Even at 20% of budget, Campaign 2 only needs a handful of leads a month to outperform Campaign 1's entire contribution in revenue terms. That's the argument for keeping it alive at a real (if minority) budget rather than treating it as an afterthought.

---

## 3. Targeting — per doctrine, no exceptions

**Advantage+ everywhere. Geo only. No interest/behavior targeting on either campaign.**

- **Geo:** the 15 ZIPs on file in AT — Burnsville, Chaska, Eagan (55121/55122/55123), Eden Prairie (55344/55347), Inver Grove Heights (55076/55077), Mendota Heights (55118/55120), Oak Park Heights, Savage, Shakopee (55372/55379), Stillwater. **People living in**, not "recently in."
- **Age:** no suggestion applied unless the AM confirms a real reason to — the ICP notes are about the *home* (26+ years old) and *ownership status* (owner-occupied, landlord, property manager), not buyer age, and none of that becomes a targeting filter per doctrine. It informs creative and proof, not the audience.
- **Placements:** Advantage+ (all).
- If either campaign underperforms, the fix is offer/angle/creative — not narrowing the audience.

---

## 4. Destination — native Meta lead form (Route A)

Checked ontimeservicepros.com directly: there is **no existing unified tune-up or install promo page** — service info is spread across separate Furnace Repair/Install and AC Repair/Install pages, with no page built for a discrete campaign offer. That rules out Route B (existing page). Building a new page (Route C) needs to be live 4 business days before buildout — with a Mon Aug 17 brief and an Aug 24–25 launch, there isn't room for that without pushing the date.

**Recommendation: Route A, native Meta lead form, for both campaigns.**
- Fields: name, phone, ZIP, service needed. Nothing else.
- Higher-intent form type with a review/confirm step.
- One qualifying question on Campaign 2 only ("Is your system 15+ years old?" or similar) — worth the friction on a $13,500-ticket lead, not worth it on the $49 tune-up.
- Custom thank-you screen with click-to-call.
- Leads must land in the CRM automatically — this is the single most common way a native-form launch quietly fails, so it's part of the Stage 8 QA either way.

**For a future cycle:** the missing unified promo page is worth flagging to the AM/Web independent of this launch — right now every seasonal offer inherits the same limitation.

---

## 5. Creative spec (for Héctor/Mac — brief for the task card already in motion)

Per angle, per the DCT method — same as what's already being briefed, restated here so the campaign and the creative match:

**Angle A — $49 Tune-Up**
- 3 creatives, one format, iterations of the same promise (not 3 different offers).
- Lead with the price and the season: pre-winter furnace check before it fails in January.
- Proof to use: **"On time, every time, or your repair is free up to $300"** (literally the brand name as the guarantee — strongest asset on the site), 80 years in Minnesota (since 1945), 5-star reviews.
- 2 headlines / 2 primary texts, same angle, genuinely different takes (not reworded duplicates).

**Angle B — 30% Off Install**
- 3 creatives, one format, iterations of the same promise.
- Lead with the discount + financing together — "30% off, financing as low as $120/mo" removes the two real objections (price and monthly payment) in one line. Financing is already live on their site; confirm the $120/mo figure with the AM before it goes in an ad.
- Proof to use: same guarantee + tenure, plus the 10-year-old-and-up equipment angle (aging system = the real trigger).
- 2 headlines / 2 primary texts, same angle.

**Competitor scan (North State Mechanical, their listed competitor):** no visible discount or promo messaging on their site — they position on trust and "no upselling," 200+ reviews, 20+ years, no price-forward offers. A dollar-and-percent offer from OTSP will look sharper next to that by contrast; no reason to soften the price angle to compete on their trust ground — we already have 80 years and a guarantee tied to the brand name.

---

## 6. Awareness campaign (always on, per doctrine)

Campaign 3, 5–10% of total, objective **Ad Recall Lift**, not reach or CPL. Needs its own creative brief — branding statics/video (name, trucks, the "On time or it's free" line), never the promo creatives recycled. Flag to Vince/Héctor as a separate ask from the DCT creative above if it isn't already scoped on the task card.

---

## 7. Open items — blocking or time-sensitive

1. **Meta Business Manager / Ad Account access** — confirm with AM today. Fires "Create Meta Ads Account" if it doesn't exist.
2. **Pixel / Conversions API** — install + verify. Hard gate before Stage 4 technically closes; running in parallel here given the date.
3. **Written monthly budget figure** — this brief is built on ratios; needs the actual number to buildout.
4. **Confirm the $120/mo financing figure** before it appears in ad copy (Stage 1A: no invented pricing).
5. **GHL/CRM lead routing test** — ServiceTitan + CallRail already exist, so this is a routing/mapping task, not a build from zero. Still needs Mo's Verified Live if GHL is in the path.

---

## 8. What happens after launch

Standard SOP: 3-Day Check (delivery/tracking only, no creative judgment), 7-Day Check (first real read, kill/isolate per §7.5 of the SOP). Given the Sept promotion is date-bound, the 7-day read lands right as the promotion is mid-flight — worth deciding now whether "kill" on Campaign 2 gets more patience than usual given its small sample size and high per-lead value; recommend not killing Angle B on Day 7 unless it produced zero spend, given how few leads it needs to pencil out.
