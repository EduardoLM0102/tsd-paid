# Client Video Audit + Video Readiness (Nov 18–19, 2026)

**Why this exists:** LilyPad churned on 11-18 and JB blamed static ads. Ryan (COO) asked Edu in Slack DM for:
1. every client we run ads for: who is using video, who isn't, and why;
2. the list of clients with no video assets, so they get set up for video or have ads shut off.

The earlier version of this audit is Ryan's own Sep 8 doc `Video_Master_JB.docx`; Edu's Sep 9 answer was a text plus voice notes.

**Deliverables (all private, nothing shared with Ryan yet):**
- Report page: https://claude.ai/artifact/6fiQ5bxeJAQNnssJGLWQTM (v7). Local copy: `client-video-audit-2026-11-18.html`
- Google Sheet v2 (current): https://docs.google.com/spreadsheets/d/13-ou0aPnM471rrUVWCghheBaslp7utRndPS4d0CKPEw/edit (Clients tab = Running / Not running only, no Meta/Google split). Local copy: `Client_Video_Audit_Nov18_v2.xlsx`
- Google Sheet v1 (superseded, granular columns, still in Edu's My Drive, not trashed): `1E4ffCuXKEZnfUXkmG7dH5vNCg-mdDDc9VnT-dgsADiQ`
- Sheet builder: `build_xlsx_v2.py` (parses the report HTML table → xlsx; upload to Drive converts it to a Sheet). There is no Sheets editor connector, so every change = new upload.

**Sources:** Meta Ads MCP (last 14 days to 11-18), Google Ads API (11-04..11-17), Agency Titan video tasks + comments, Drive client folders, Slack.

---

## 1. Status on 11-18 (11 running video / 4 running ads without video / 2 leaving)

| Client | Meta | Google / YouTube | Video files we have | What's going on |
|---|---|---|---|---|
| **Watt's Right** | Video 80% of $3.9k, lead ads + awareness | PMax with our video paused 11-10 | Finished | Best setup we have. FourMode and Winter ads are still static. |
| **Spencer Air** | Video 100% of $545, awareness only | Search + pay-per-lead | Finished | No Meta lead ads, so video only does awareness. |
| **Nick's** | Video 100% of $276, awareness only | Auto video $43 on YouTube via PMax | Finished, approved Sep 11 | Live ads uploaded Sep 3, BEFORE the approved revisions (Tyler's testimonial removed Sep 4). Need the approved cuts swapped in. |
| **Cool Hand** | Video 100% of $275, awareness only | YouTube Demand Gen live daily | Finished + raw backlog | Fine. Raw backlog not edited. |
| **Napps** | Video 100% of $69, $5/day awareness | Search + LSA | Finished | Fixed since Sep 8 (was static only). Budget is tiny. |
| **Integrate Comfort (ICS)** | Can't check, account blocked from our API | YouTube Mitsubishi live; PMax with video paused 11-11 | Finished, old | Needs a manual look in Ads Manager for Meta. |
| **King's Window** | Video 31% of $445: 3 old video ads, lead ad is static | Search + pay-per-lead | 9 new finished ads from Oct 13 | Never reached Paid. Sara copied them to a "KINGS ADS" folder Oct 27. No task to Paid, no approval task. Old AD I–IV still running. |
| **Concrete Adventures** | Video 2%: 1 video live since 11-17 + 3 statics | Search only | Shot Oct 28–29, 1 of 5 cuts done | New client, launched on statics while editing ran. Plan promised 5 cuts by 11-12; 1 delivered. |
| **Zen Air** | Awareness video runs all year; off 11-13→11-18 (Meta policy false positive), re-cut + republished 11-18. Lead ads static | Search + LSA | Full new library finished in Aug: AD 1–4, brand story, 4 testimonials, What To Expect | New videos never reached Paid. We keep running a 2024 winter video. The 3 video tasks sit in Review & Close, nobody assigned since August, no client approval on record. |
| **Mission Accomplished** | Video, low: $183, 1 small video retargeting ad next to static lead ads; dark since 11-16 (card declines) | LSA only | Finished Sep 3 (incl. Kelly + Roger testimonials) | Running, but low and only on lead gen. Brian asked to pause the video awareness campaign himself on 10-30 (AT e3825422). Check with the AM whether we can turn it back on (fu-185). |
| **Proud Pops** | Off ($0 in 90 days) | YouTube RESTARTED 11-18: $100/day San Antonio + $100/day New Braunfels, 8 approved video ads | 4 finished YouTube cuts + 535 raw | Paused 10-16 in the client's cut to $25k; back on with room under the cap (Nov ~$23k). Video production removed from their program Jun 19, so no new footage is coming. |
| **Amazing Morrow** | Static: $675, 12 static ads | Pay-per-lead only | Raw only; shoot 11-17/18 | New client, launched 11-16 before the shoot. No video ever uploaded. |
| **Neon Monkey** | Off: client said 11-13 "no Facebook until real video exists" | PMax paused 11-16, Branded only now | Raw only, 100+ phone clips | Nobody assigned to edit the raw footage. Client is waiting on it. |
| **All Seasons** | Off since 10-16 (client budget cap; Meta off by client since 04-15) | Search + LSA | Finished, 10+ months old | Meta off by client choice. Footage stale. |
| **C&S Air** | No access, Meta account never shared | Search + LSA | Finished, ~2 years old | Can't run Meta without access. Footage stale. |
| Hawkins (leaving) | Off, paused 08-20 at client request | 94% of PMax went to YouTube (auto video) | Finished, never approved | Terminated 11-02, ends ~12-02. |
| LilyPad (churned) | Off | Search | Finished, approved Jul 29 | Churned 11-18. Video never reached Paid. |

**Not on the list on purpose:**
- **Golden Plumbing** removed entirely (frozen; Edu: "take golden plumbing completely out"). ⚑ Open: `TSD_02.19_Pmax` is still ENABLED and serving since 11-09 (~$228 in 14 days) despite the freeze. Offered to pause twice, no answer yet.
- **Carey & Walsh** = not a paid client (told Angela 11-09 they won't do paid ads or share access).
- Never shot, not running ads: Ryan Heating & Air, Cartwright, Supreme, North Bay, AC Cornerstone, JR Michalski.

## 2. Root cause

The Agency Titan video handoff ends at the AM or the client, never at Paid. No task routes finished video to Paid and no approval task exists. Same failure on LilyPad (approved Jul 29, never ran), Zen Air (August library), King's (Oct 13 batch). Fix to propose to Ryan: every finished video task gets a closing step "Client approved → hand to Paid Ads" with the Drive folder link, and Paid gets a 48h SLA to put it live.

## 3. Video readiness (Edu asked 11-19: "do we have clients that aren't running video that we can put to run right away?")

**Answer: no.** None of the 4 clients running ads without video can have video live today. Each one is blocked by something Paid can't fix alone:

| Client | Blocker | Fastest unblock | Owner | Follow-up |
|---|---|---|---|---|
| Amazing Morrow | Raw only, shoot 11-17/18 | Editing delivers first cuts → Paid uploads via the Drive route | Video team | fu-190 |
| Neon Monkey | 100+ raw phone clips, no editor assigned; client wants no Facebook until real video | Get an editor assigned (only one where the client is actively waiting) | AM / Video team | fu-189 (+ fu-173 for the budget question) |
| All Seasons | Finished video is 10+ months old; Meta off by client budget cap | Written Meta budget approval via AM; fresh footage ideally | AM / client | fu-191 |
| C&S Air | Meta account never shared; footage ~2 years old | Access first | AM / client | fu-018 (note added) |

**Where video can move faster: running clients with finished video sitting unused.**

| # | Client | What to do | Blocked on | Follow-up |
|---|---|---|---|---|
| 1 | **Nick's** | Swap the Sep 3 live videos for the Sep 11 approved cuts (removes Tyler's testimonial, cut Sep 4). Paid-only, no sign-off needed. Check the approved cuts in Drive against the live ads first, then upload through the Drive route. | Nothing. **Do first.** Waiting on Edu's go. | fu-186 |
| 2 | **King's Window** | 9 finished ads from Oct 13 ("KINGS ADS" folder, Sara 10-27) → launch | AM confirms client approval | fu-187 |
| 3 | **Zen Air** | August library (AD 1–4, brand story, 4 testimonials, What To Expect) → launch | AM approval (3 video tasks in Review & Close, unassigned since Aug) | fu-188 (fu-183 = the re-cut review check) |
| 4 | **Mission Accomplished** | Sep 3 testimonials into lead ads; video awareness back on | Card declines (dark since 11-16) + Angela's answer on awareness | fu-185, fu-177 |
| 5 | **Concrete** | 4 of 5 cuts still owed (promised by 11-12) | Editing | fu-174 (note added) |

Plan Edu was offered: do Nick's swap today + one note to the AMs about King's and Zen approvals.

## 4. Other open items from this thread
- **Slack reply to Ryan:** not sent. Numbers to use: 11 running video / 4 running ads without video. Draft only, Edu sends.
- **Sharing:** report page + Sheet v2 are private; Edu shares with Ryan.
- **Sheet v1:** trash or keep? Edu hasn't answered. Don't trash without an explicit OK.
- **Golden PMax pause:** waiting on Edu's yes.

## 5. Work done during the audit (11-18)
- **Zen Air:** Cold Weather AD disapproved (adult nudity false positive, satin pajamas close-up). Re-cut v2 (hand + thermostat crop), 1:1 + 9:16 uploaded via the Drive route, PAC creative 1089767234034640, ad 120248171261340711 published, old ad 120248098173470711 paused. Log: `clients/zen-air/meta-ads-log.md`.
- **Proud Pops:** YouTube restarted (UI, VIDEO status mutate not allowed via API). Log: `clients/proud-pops/google-ads-log.md`.
- **New team rule:** every Meta media upload goes through the Drive route end to end. `_contexto/memoria/tsd-meta-media-upload-drive-route.md`.
