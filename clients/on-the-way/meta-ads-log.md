# On The Way AC Plumbing & Electric — Meta Ads Log

Convention: newest entry on top. One entry per work session — researched → found → did → open items. See `clients/README.md`.

---

## 2026-10-01 (session 3) — Activity log check: who built and changed the awareness campaign

Part of a cross-platform "list every change we made for On The Way" pass. The Google side is in `google-ads-log.md` session 8. Read-only, no account changes.

**Found (Meta activity log, 2026-08-15 → 10-01, account `1428068256022895`):**
- **09-02 17:29:** Ronnie Bedard added a user to the account with the role "Manage Creative Hub mockups".
- **09-04 10:25:** Jonathan Bannister (Power Editor) turned off 3 old boosted-post campaigns: "We got the old goat in our office to talk about...", "#shoplocal #supportlocal #localbusiness...", and "Our 50th Anniversary Ribbon Cutting with Santa...".
- **09-04 11:23–14:02:** Jonathan Bannister built `09/04/26 - CBO | Awareness / Ad Recall Lift` (`52685970356578`):
  - $50/d CBO.
  - Ad set "Service Area (40Mi from Office)", optimized for Ad Recall Lift.
  - Location: 2513 FM 646 Rd N, Santa Fe +35 mi, age 18+, Advantage+ audience on, automatic placements.
  - Ad "04/09/26 - Ad 01 | Cold Shower". It started delivering 09-04 14:18.
- **09-10 11:55:** Ronnie Bedard (Power Editor) set the ad set end date to 09-11 00:00. This confirms the session-2 finding.
- Nothing else since, apart from billing events and Meta's automatic `asa_auto_custom_audience` creations.
- Nobody on the TSD side has confirmed who Jonathan Bannister or Ronnie Bedard is. The campaign name follows the TSD Awareness / Ad Recall Lift template used on Gillespie's, Watt's Right and Nicks, but that's an inference, not a confirmation.

**Open items:**
- [ ] Confirm whether Jonathan Bannister is TSD (he built the campaign) and whether Ronnie Bedard is client side or TSD. Ronnie's identity is still open from session 2.
- [ ] Everything open from session 2 carries forward.

---

## 2026-09-30 (session 2) — Hook rate + ad recall lift read on "Cold Shower", client message on success metrics

Responding to the client's 09-29 ask for the exact success metrics, benchmarks and our stance on the drop-off. Edu asked for the hook rate the client was pointing at, then for the ad recall lift numbers (the metric the campaign actually optimizes for), then for a plain-language client message. No account changes made.

**Context carried in from the 09-29 check (not previously logged here):** the campaign `09/04/26 - CBO | Awareness / Ad Recall Lift` (`52685970356578`) has not been running since 09-11. On 09-10 11:55, **Ronnie Bedard** set an ad set end date of 09-11. It still shows ACTIVE but has spent $0 since. So the 09-16 entry below ("still ACTIVE, not turned off despite the client's read") is wrong, the ad did stop. Who Ronnie is (client side or TSD) is still unconfirmed.

**Hook rate (3-sec plays ÷ impressions, lifetime).** `3_second_video_plays` only exists at campaign/ad set level, not ad level. Fine here since the campaign has one ad.

| Campaign | Hook rate | ThruPlay rate |
|---|---|---|
| **On The Way** (`52685970356578`, Cold Shower) | **5.0%** (4,896 / 98,062) | 0.57% |
| Gillespie's Evergreen ARL (`7000989212234`) | 17.5% | 1.74% |
| Nicks Evergreen ARL (`120255428594060348`) | 14.0% | 1.50% |
| Watt's Right Brand Video ARL (`120248677375880470`) | 7.9% | 0.88% |

Cold Shower is the weakest hook in the set. The 09-16 conclusion that On The Way "sits inside the same band" was built on p25 and avg watch time, where every account looks equally low. It does not hold at the 3-second mark. Caveat: the comparison campaigns run 3–4 creatives each and Meta pushes delivery to the best one, so part of the gap is structure, not creative.

**Ad recall lift (lifetime).** Pulled via the `results` field (indicator `estimated_ad_recallers`) + `cost_per_result`. This is Meta's modeled estimate, not a Brand Lift survey.

| Campaign | Est. recallers | Cost / recaller | Recallers / 1k impr | Recallers / reach | CPM | Freq |
|---|---|---|---|---|---|---|
| **On The Way** ($363, 7 days) | **1,000** | **$0.36** | **10.2** | 2.6% | $3.71 | 2.57 |
| Gillespie's | 1,680 | $0.46 | 10.3 | 3.5% | $4.70 | 3.35 |
| Watt's Right | 540 | $0.54 | 9.6 | 3.0% | $5.17 | 3.12 |
| Nicks | 980 | $0.55 | 8.7 | 3.2% | $4.78 | 3.69 |

On the metric the campaign is bought for, On The Way was the best in the set: cheapest cost per recaller, mostly driven by the lowest CPM, and recall per impression level with Gillespie's despite a hook a third as strong. The one weaker number (recall per person reached) fits a campaign stopped after a week at 2.57 frequency. Read: **the hook is weak, the recall result was not.**

**Decision (Edu): Cold Shower is NOT a control.** It ran alone for one week, so there are no control numbers to beat. Next step is running 3–4 videos at the same time, Cold Shower included, and using their AVERAGE recall lift and cost per recaller as the benchmark every new video is measured against. This overrides the 09-16 plan of "keep Cold Shower as control, add 2–3 hook variants." Setup note: if all videos share one ad set, Meta will push spend to whichever it likes early, so weaker videos may not get enough spend to judge individually. The average is still valid.

**Did:** drafted the client message (for Edu or Angela to send). Final text:

> This campaign was never set up to get people to watch the whole video. Its goal is to get as many people in your area as possible to remember On The Way (that's exactly what ad recall lift, the goal this campaign is set to, means), so when their AC or water heater goes out, your name is the one they think of. Meta shows it to the people most likely to remember it, not the people most likely to keep watching. It works like a billboard: most people drive past without reading every word, but after seeing it a few times they know the name.
>
> On that goal it did well. In 7 days it reached about 38,000 people in your area, and Meta estimates around 1,000 of them will remember the ad. That came out to $0.36 per person, the lowest of the other home service companies we run this same campaign for (they're at $0.46 to $0.55).
>
> Watch time is a secondary number for this type of campaign, though we don't ignore it. Only about 5% of people watched past 3 seconds, while the same campaign gets 8% to 17% for other clients, so the opening can be stronger. Cold Shower ran alone for one week, which isn't enough to call it the number to beat. The next step is to run 3 or 4 videos at the same time, Cold Shower included, the same way we do on the other accounts. That gives us an average cost per person who remembers the ad, and that average becomes the benchmark every new video is measured against.

**Open items:**
- [ ] Send the client message (Edu or Angela). Not confirmed sent as of this entry.
- [ ] Confirm whether Angela's 09-16 reply went out. If it did, it said the ad was still running, which was wrong.
- [ ] Identify Ronnie Bedard (client side or TSD) before the client asks why the campaign only ran 7 days.
- [ ] Get 3–4 videos approved/produced to run together with Cold Shower. Decide ad set structure (shared vs one per video) before launch.
- [ ] Campaign still shows ACTIVE with an expired end date. Clean up status once the new structure is decided.

---

## 2026-09-16 (session 1) — Awareness campaign retention pushback: pulled comparison data, drafted AM reply

Started as a book-wide check (Edu asked which TSD clients currently have a live Meta awareness campaign) and turned into a specific ticket response for this account. Meta ad account is `1428068256022895` ("On The Way Pros Ad Account").

**Book-wide context:** of 25 queryable TSD Meta accounts, 12 currently have an active awareness/reach objective campaign. On The Way is one of them: `09/04/26 - CBO | Awareness / Ad Recall Lift` (campaign id `52685970356578`, objective `OUTCOME_AWARENESS`, launched 2026-09-04, still ACTIVE).

**The trigger:** client emailed Angela pushing back on the awareness ad, citing ~97% of viewers dropping off around the 1-second mark after 7 days live, and proposing a hook/opening test against the current creative as control.

**Found (lifetime data, single ad in the campaign — `04/09/26 - Ad 01 | Cold Shower`, id `52685970356978`, still ACTIVE, not turned off despite the client's read):**
- 98,062 impressions, 94,886 video plays, $363.37 spent.
- Only 1,197 plays (1.3%) reached 25% of the video. Average watch time: 1 second. 560 ThruPlays (0.6% of plays). Cost per ThruPlay $0.65.
- Client's number matches reality — this isn't a misread on their part.

**Benchmarked against the same `Awareness / Ad Recall Lift` campaign template running live on three other current accounts** (Gillespie's Heating and Cooling `2014320269203822`, Watt's Right Electric `588638883283311`, Nicks Heating & Air `710350517676765`):
- p25 reach rate across their creatives: 0.15%–2.4%. Average watch time: 1–2 seconds. ThruPlay rate: 0.6%–2.2%. Cost per ThruPlay: $0.22–$1.15.
- On The Way's numbers sit inside that same band. The retention curve is the norm for this campaign format across the book, not a signal specific to this creative — Ad Recall Lift optimizes for reach/frequency against the audience Meta's model predicts will recall the ad, not for watch-through.
- One real structural difference: all three comparison accounts run 3–4 creative variants inside the awareness campaign at once. On The Way is running a single ad ("Cold Shower").

**Did:**
- Drafted a ticket reply for the AM (Angela) to send back: explains the drop-off is expected for this objective, backed by the cross-account comparison, and agrees to the client's hook-test proposal — keep "Cold Shower" as control, add 2–3 new hook variants once the client approves more creative. No account changes made yet, pending client go-ahead on new creative.

**Open items:**
- [ ] Waiting on client approval to build 2–3 new hook/opening variants for this campaign.
- [ ] Once approved, deploy alongside "Cold Shower" (control), matching the 3–4 variant pattern already running on Gillespie's / Watt's Right / Nicks Heating.
- [ ] No prior meta-ads-log existed for this account — this is the first entry. `README.md`'s "Account status" section still says "Not in the TSD book" from the 2026-07-16 check and needs a refresh (Google Ads has been live since session 6 on 2026-09-09, and Meta since at least 2026-09-04) — not fixed in this session, flagging for next pass.

---
