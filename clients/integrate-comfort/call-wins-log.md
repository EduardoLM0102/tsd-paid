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

---

# Update 2026-10-28: calls 2026-10-16 → 2026-10-28

Same rule: CallRail calls with a gclid or a Google Ads / Call Extension / Local Services Ads source. 14 calls (12 Google Ads, 2 LSA). Transcribed locally with faster-whisper (small.en). Names and streets may be mis-transcribed.

## 2026-10-16

- **10:43 · 41s · Call Extension · Fair Lawn** — Hangs up during the extension menu. ⚠️ IVR-only.
- **11:43 · 54s · LSA · Brooklyn** — Full menu, then "please leave a message", no message left. ⚠️ IVR-only (Brooklyn is outside the NJ service area anyway).

## 2026-10-18 (Sat)

- **09:23 · 20s · Call Extension · Milwaukee** — Different greeting ("the heating and cooling experts, we have in..."), likely the after-hours message; caller hangs up. ⚠️ IVR-only.

## 2026-10-19

- **13:52 · 55s · LSA (GMB Calls-Belleville line) · Caldwell, repeat caller** — Full 8-option menu, picks service, the call ends during the transfer. ⚠️ IVR-only.

## 2026-10-20

- **15:06 · 19s · Call Extension · Succasunna** — Hangs up during the greeting. ⚠️ IVR-only.

## 2026-10-21

- **06:45 · 483s · Call Extension · Jersey City (new customer)** — Picks service, reaches Jason. Two central heating units in a family home not working right, wants an inspection. Booked a service visit the same day, 3–5 pm, gave card details over the phone. ✅ Booked (new customer, the 483s call from fu-031).

## 2026-10-22

- **08:30 · 73s · Call Extension · Orange** — Reaches Jerry in service, but the caller wanted "JW Pearson", an oil company. ❌ Not a lead (wrong company).
- **12:01 · 118s · Homepage Calls (Google Ads source) · Morristown, existing customer** — Confirms tomorrow's 9–11 visit and asks about the filter. ✅ Existing customer, not new pipeline.

## 2026-10-23

- **08:12 · 55s · Call Extension · Hackensack** — Hangs up during the menu. ⚠️ IVR-only.
- **15:38 · 18s · Call Extension · Bronx** — Hangs up during the greeting. ⚠️ IVR-only.

## 2026-10-26

- **14:06 · 41s · Call Extension · Succasunna** — Hangs up during the menu (same town as 10-20, possibly the same person trying again). ⚠️ IVR-only.

## 2026-10-27

- **12:45 · 333s · Call Extension · Queens** — Waits through the whole menu (~1 min) and reaches Jason. Old central AC not working well, wants a replacement estimate. Booked Thursday 11 am with project advisor Chris. ✅ Booked (new customer; Queens is outside the NJ geo, check that it's serviceable).

## 2026-10-28

- **10:26 + 10:30 · 217s + 249s · Call Extension · Newark (same caller)** — First call gets stuck in the name directory and loops back to the menu with no person. He calls back, reaches Jason, and asks where to buy a brand sticker for a condenser another contractor installed. ❌ Not a lead (not an ICS customer).

---

## Running tally (2026-10-16 → 2026-10-28, 14 calls)

| Outcome | Count | Detail |
|---|---|---|
| ✅ Booked, new | 2 | 10-21 same-day heating service (Jersey City), 10-27 AC replacement estimate (Queens) |
| ✅ Existing customer | 1 | 10-22 appointment confirmation |
| ❌ Not a lead | 2 | wrong company (oil), sticker question from a non-customer |
| ⚠️ IVR-only | 9 | 8 hang up in the menu/greeting (18–55s), 1 LSA reaches voicemail and leaves no message |

**Combined 10-01 → 10-28: 31 ad calls, 3 new jobs booked, 24 never reached a person.**

**Flag for Edu: the IVR question from the first log is now answered.** In this batch, every caller who picked an extension stayed recorded through the transfer to a live person (10-21, 10-22, 10-27, 10-28). So recording does NOT stop at the transfer. The IVR-only calls are real hang-ups, not a blind spot. The menu runs 8 options plus a name directory (~45–60s before it finishes). Ad callers who hang up do it at 18–55s, inside the menu. Everyone who got through reached a person within ~10s of picking service, so staffing isn't the problem. The menu is. Fix for the AM/ICS: route the Google Ads and LSA tracking numbers straight to the service/sales queue (skip the menu), or put "press 1 for service or a new system" first. Also, 2 of the 3 bookings and several hang-ups came from NYC (Queens, Bronx, Brooklyn, New York), outside the NJ county geo. Worth checking where those callers see the ads (presence vs interest, LSA area).

**Attribution check (2026-10-28, Google Ads call_view; Google times are 1h later than CallRail's):** the 10-21 Jersey City booking is a confirmed PMax ad call (484s in call_view, counted as "Calls from ads"). The 10-27 Queens booking is NOT in Google's call records and has no gclid. The caller dialed the CallRail number reserved for the call extension directly, so it's likely from a Google ad but can't be proven, and Google gives PMax no credit for it. The same goes for the 10-22 Orange wrong number. The 10-28 Newark sticker call (249s) WAS counted by Google as a PMax conversion, even though it's not a lead.
