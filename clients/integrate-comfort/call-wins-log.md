# Integrate Comfort (ICS) — Call Wins Log

Day-by-day log of CallRail-recorded calls attributed to paid ads (Google Ads call-extension or Local Services Ads source), last 15 days (2026-10-01 → 2026-10-15). Transcribed locally (`faster-whisper small.en`); see [[tsd-call-wins-log-process]] for the pipeline. Raw audio/transcripts kept out of this repo (session scratchpad only).

**Outcome legend:** ✅ Booked · ⏳ Open/follow-up needed · ❌ No contact / not a lead · ⚠️ IVR-only (no visible live conversation in the recording)

---

## 2026-10-01

- **06:45 · 377s · Poughkeepsie** — Allison Ferranti, converting her boiler from oil to natural gas (gas line being run to her street) plus a new gas line into the kitchen. Office took full contact info and **booked a project advisor visit for Wednesday Oct 7, 2–3pm**, quoted a 2–3 week lead time. ✅ Booked — a real, sizable conversion project, the strongest call in this client's window.

## 2026-10-05

- **08:30 · 47s · Lawrence** — Hits the extension-routing menu, call ends partway through. ⚠️ IVR-only.
- **11:50 · 28s · Hackensack** — Same, ends very early in the menu. ⚠️ IVR-only.

## 2026-10-06

- **08:25 · 124s · Jersey City** — Full extension menu plays out, call ends with no selection captured. ⚠️ IVR-only.
- **09:05 · 120s · Morristown** — Same pattern. ⚠️ IVR-only.

## 2026-10-07

- **07:48 · 144s · Phoenix** — Same pattern (unusual city for an NJ HVAC company — likely a mobile caller or misattributed location). ⚠️ IVR-only.
- **12:46 · 139s · Caldwell** (Google Local Services Ads) — Same pattern. ⚠️ IVR-only.

## 2026-10-09

- **08:10 · 32s · Pleasantville** — Menu cuts off almost immediately. ⚠️ IVR-only.
- **08:28 · 35s · Newark** — Same. ⚠️ IVR-only.
- **08:32 · 46s · Bronx NYC** — Same. ⚠️ IVR-only.
- **11:48 · 25s · Cranford** — Same, very short. ⚠️ IVR-only.
- **15:00 · 56s · Cranford** — Same caller/area, same pattern. ⚠️ IVR-only.

## 2026-10-13

- **09:03 · 65s · Succasunna** — Gets transferred to the service department and reaches a live rep ("ICS service... Jury?"), but the caller was looking for a different company ("Harmony Heating") and the call ends as the rep starts to repeat the menu. ❌ Not a lead (wrong number, but notable it's the only call that reached a live person besides the Poughkeepsie one).
- **10:41 · 18s · Passaic** — Menu cuts off almost immediately. ⚠️ IVR-only.

## 2026-10-15

- **10:29 · 55s · New York** — Same pattern. ⚠️ IVR-only.
- **11:58 · 31s · Hackensack** — Same. ⚠️ IVR-only.
- **13:43 · 40s · Bayonne** — Same. ⚠️ IVR-only.

---

## Running tally (2026-10-01 → 2026-10-15, 17 calls)

| Outcome | Count |
|---|---|
| ✅ Booked | 1 (Allison Ferranti — oil-to-gas boiler conversion, real project booked) |
| ❌ Not a lead | 1 (wrong number, reached a live rep) |
| ⚠️ IVR-only, no visible live conversation | 15 |

**Flag for Edu — this is the real finding here, not the one good call:** 15 of 17 ad-driven, recorded calls show nothing beyond ICS's multi-option extension menu ("dial 704 for service, 715 for install, 716 commercial, 703 sheet metal, 710 accounting, 723 project management...") — no live conversation captured in any of them. Two explanations are both possible from what we can see: (1) callers are hanging up partway through a long menu, which is a real lead-loss risk, or (2) CallRail's recording for this call object simply stops once the call forwards to whichever extension the caller picked, and the real conversation continues on an unrecorded leg — which would mean this isn't a loss, just a blind spot in what we can measure. This needs a direct look at ICS's call-forwarding/recording setup before concluding either way.
