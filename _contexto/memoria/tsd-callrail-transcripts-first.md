---
name: tsd-callrail-transcripts-first
description: "Edu 2026-11-16: CallRail calls come already transcribed; pull fields=transcription before any local whisper"
metadata:
  type: feedback
---

CallRail calls can be downloaded **already transcribed**: `GET /v3/a/<acc>/calls.json?...&fields=transcription,...` returns a speaker-labeled transcript ("Agent: / Caller:"). Use that first; local whisper (call-wins `transcribe.py`) only for calls with no CallRail transcript (LSA recordings pulled from Google, trackers with recording OFF, accounts without it).

2026-11-16 check (calls 60s+, 11-10..11-14): agency account 792265907 13/13 transcribed, Watt's Right 19/19, King's 14/14, Proud Pops (own account 533681324) all Website-pool calls; Neon Monkey 0/4 (no transcription there). Calls on trackers with recording OFF (Proud Pops "210 - CALL POP") have none.

**Why:** Edu reminded this on 2026-11-16 while refreshing the Proud Pops review; whisper is slower and less accurate than what CallRail already has.

**How to apply:** in any call review / call-wins / strategy-review transcript pass, pull CallRail calls with `fields=transcription` (build the URL by hand, commas must not be urlencoded, see [[tsd-callrail-api-access]]). The call-wins SKILL.md line "a transcrição da própria CallRail exige add-on pago" is outdated. Related: [[tsd-call-wins-log-process]], [[tsd-at-client-strategy-review]].
