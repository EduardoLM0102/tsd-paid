---
name: tsd-client-video-audit
description: Nov 18-19 2026 client video audit for Ryan (after LilyPad churn): 11 running video / 4 not; no no-video client can go live today; Nick's swap is the only Paid-only fix; root cause = AT video handoff never reaches Paid
metadata:
  type: project
---

**What:** Ryan (COO) asked on 2026-11-18, after LilyPad churned (JB blamed static ads), for every paid client's video status + the list of clients with no video (set up video or shut ads off). Full write-up, tables and deliverable links: `paid/relatorios/client-video-audit-2026-11/README.md`.

**State on 2026-11-19:**
- 11 running client video: Watt's Right, Spencer, Nick's, Cool Hand, Napps, ICS, King's, Concrete, Zen Air, Mission Accomplished (low, lead gen only), Proud Pops (YouTube restarted 11-18).
- 4 running ads without video: Amazing Morrow (raw, shoot 11-17/18), Neon Monkey (raw, no editor, client waiting), All Seasons (Meta off by budget, footage 10+ mo old), C&S (no Meta access, footage ~2 yrs old). **None can go live today**; each is blocked outside Paid.
- Leaving: Hawkins, LilyPad. Golden removed from the audit (frozen) but its PMax is still serving ⚑. Carey & Walsh = not a paid client.

**Video that exists but isn't running (priority order):** Nick's approved Sep 11 cuts (Paid-only swap, fu-186) → King's 9 Oct 13 ads (AM approval, fu-187) → Zen August library (AM approval, fu-188) → Mission Accomplished testimonials (card + Angela, fu-185/177) → Concrete 4 cuts owed (fu-174).

**Root cause:** Agency Titan video tasks end at the AM or the client, never at Paid (LilyPad, Zen, King's). Proposed fix for Ryan: a closing "client approved → hand to Paid" step with the Drive link + 48h Paid SLA.

**Why:** this was the second time Ryan asked (first: his Sep 8 `Video_Master_JB.docx`), so the audit will be repeated. **How to apply:** when a client's video comes up, check this list + its follow-up first; rebuild the sheet with `build_xlsx_v2.py` from the report HTML. Related: [[tsd-meta-media-upload-drive-route]], [[tsd-zen-air]], [[tsd-mission-accomplished-meta]], [[tsd-concrete-adventures]].
