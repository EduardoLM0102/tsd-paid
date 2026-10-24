---
name: tsd-call-wins-log-process
description: "Per-client 'call wins log' — CallRail recording -> local Whisper transcript -> day-by-day booked/open/not-a-lead log; built for Cool Hand Electric 2026-10-15, reusable for any client with CallRail recording on"
metadata:
  node_type: memory
  type: reference
  originSessionId: a71195c0-f13a-42e5-8604-be06c28ad0c7
  modified: 2026-10-15T00:00:00.000Z
---

**2026-10-23: packaged as the `call-wins` skill** (`.claude/skills/call-wins/`: `pull_calls.py`, `pull_lsa.py`, `transcribe.py` + SKILL.md with the log rules). Use it instead of rewriting scratchpad scripts; data goes to gitignored `_pessoal/call-wins/<slug>/`. Gui set up via ONBOARDING step 8 with Edu's CallRail key from Bitwarden.

Edu asked (2026-10-15) for "a full log of wons for each client" after we transcribed Cool Hand Electric's CallRail calls. First instance built at `clients/cool-hand-electric/call-wins-log.md`. Process, so it repeats cleanly for other clients:

1. **Pull calls**: query that client's own CallRail account directly (not via the agency-account `callrail.py` wrapper, which is hardwired to ACC 792265907 — see [[tsd-callrail-api-access]] for the per-client account id list), `fields=...,recording,recording_duration,customer_name,customer_phone_number,customer_city,...`.
2. **Download recordings**: the `recording` field returns a JSON `{"url": "..."}` pointer (not the audio itself), fetch that URL for the actual `audio/mpeg` file. Only calls with a nonzero `recording_duration` have audio.
3. **Transcribe locally, never cloud**: CallRail's own `transcription` field requires their paid "Premium Conversation Intelligence" add-on (confirmed gated via the API's `notice` field, 2026-10-15) — not available on this account. Used a local venv + `faster-whisper` (`small.en`, `device=cpu`, `compute_type=int8`) instead, since the recordings contain real customer PII (and on the Cool Hand 10-14 Tracy call, spoken payment-card details) that shouldn't leave the machine. No `ffmpeg`/`brew` needed — faster-whisper decodes via its own deps.
4. **Log format**: one `.md` per client at `clients/<slug>/call-wins-log.md`, grouped by day, each call = time/duration/source/city/name + one-line summary + outcome tag (✅ Booked / ⏳ Open / ❌ Not a lead), closing with a running tally table. Keep raw audio + full transcripts.json OUT of the repo (session scratchpad only) — the log file itself only carries the summarized, PII-light version, and never repeats actual card/CVV digits even when a call contains them.
5. **Caveat always included in the log**: small local ASR model on phone-quality audio will misspell names/emails/streets sometimes (confirmed: same caller's name came out two different ways in one Cool Hand call) — flag it as a lead to verify, not a verified record.

**Why:** Edu wants provable, call-level evidence of real revenue outcomes (bookings, membership renewals, upsells) from ad spend, not just funnel-metric counts — and wants it to scale to every client, not stay a one-off for Cool Hand.

**How to apply:** when asked to build/update this log for another client, first confirm that client's CallRail company has recording turned on and has actual call volume (many of the 11 CallRail-mapped clients in [[tsd-command-center]]'s funnel list may not). Reuse this exact pipeline rather than re-deriving it. Related: [[tsd-callrail-api-access]], [[tsd-command-center]], [[tsd-cool-hand-electric]].

**LSA calls often never touch CallRail (found 2026-10-15).** C&S Air, Napps, All Seasons and Cool Hand had 0 LSA calls in CallRail but 3 / 18 / 14 / 2 LSA leads in Google. When CallRail has no LSA, pull it straight from Google Ads: GAQL `local_services_lead` (status, charged, creation_date_time) + `local_services_lead_conversation` (`phone_call_details.call_recording_url`, `message_details.text`). The recording URL (ads.google.com/localservicesads/attachment/...) 302s to login without auth, but downloads as audio/mpeg with `Authorization: Bearer <token>` from the google-ads client's own `client.credentials` (refresh first). Run via `tsd.sh <script>`. `contact_details.phone_number` is NOT a valid GAQL field. Google "BOOKED" = whatever the business taps in the LSA app (Watt's Right marks ~97% booked), so report it beside transcript outcomes, never instead of them. `lsa_report.py`'s account list is missing Napps LSA 9239407401, Spencer 2524618054 and Kings 6769493219 (all have LSA leads).

**Ambiguity trap:** when splitting logs by source, match `\bLSA\b|Local Services` on the call's header only — a case-insensitive `lsa` matches "Tulsa".
