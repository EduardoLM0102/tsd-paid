---
name: tsd-client-facing-voice
description: "Voice rule for ALL TSD client-facing output (every client) — natural and organic, never textbook English, zero AI tells"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3fc692f3-2e62-4c50-8c06-c36d39b31b4e
  modified: 2026-09-11T12:38:20.981Z
---

Standing voice rule for **every TopServ (TSD) client, no exceptions**: all client-facing output has to sound **natural and organic — the way a real person actually talks.** Never textbook English.

**Scope — client-facing only:** ad copy (Meta primary text/headlines, Google RSAs, on-image creative copy), video scripts, client report PDFs, and emails/messages to the client. NOT covered: internal `google-ads-log.md`, `paid/sops/*`, AM tickets, and replies to Edu — those stay as they are.

**"Textbook English" = what Edu is rejecting.** Grammatically perfect, correct, and dead. The register of a brochure or an ESL textbook rather than a person. Contractions get used, sentences run how speech runs, a fragment is fine if that's how someone would say it.

**AI tells to kill on sight:**
- Em dashes used as sentence-interruption punctuation (the parenthetical-aside habit). Never. **Refined 2026-08-05 on [[tsd-cool-hand-electric]]:** this doesn't cover em dashes used as topic/label separators — section headers ("September — AC Tail & Early Replacement"), table phase cells, bold list-item leads ("Google Ads — Search:"). Test: if cutting the dash and reading it as two plain sentences loses nothing, it was a stylistic interruption, kill it; if the dash is literally separating a name/label from what follows, keep it.
- Generic openers: "In today's world", "In an increasingly...", "Let's dive in", "Imagine this".
- "Not just X, it's Y" / "It's not about X, it's about Y" dichotomies.
- Empty release adjectives: powerful, robust, seamless, comprehensive, cutting-edge, trusted.
- Recap conclusions: "In summary", "At the end of the day".
- Decorative emoji and forced enthusiasm.
- Symmetric bullet structure where running prose would do; series of short fragment sentences in a row.

**Vocabulary:** use the customer's words, not agency/marketing register. For the home-services book that means how a homeowner actually describes it — AC quit, breaker keeps tripping, water heater's out, no one showed up — not "HVAC solutions" or "service offerings."

**Why:** copy that reads like a machine or a brochure kills trust with the lead. Edu asked for this explicitly, so it's a standing rule for all TSD client output, not a one-off note.

**How to apply:** write it, then reread it as if you're the homeowner/prospect. Anything that could have been generated or that no real person would say out loud gets rewritten. Composes with [[topserv-client-report-format]] (the golden rule — never signal anything was wrong — still governs *what* you say; this governs *how* it sounds) and with [[tsd-meta-ads-methodology]] for structure.

**Always run a batch-read pass before delivering a set.** Proven on the [[tsd-on-the-way-client]] 14-script batch (2026-07-16). Individual lines can each read fine while the *set* screams machine. Read all of them in sequence and hunt four things:
1. **Repeated phrases across scripts** — the single strongest tell. That batch had "That part's free" verbatim 3×, "We come out" 4×, "Here's the thing" 2×. Vary or cut; the filler ones ("Here's the thing") delete cleanly, which proves they were filler.
2. **Non-American idiom** — Edu is Brazilian and I drift too. Caught: "inside the hour" (British/sportscaster → "within the hour"), "get hold of us" (→ "get ahold of us"), "knocking out the breaker" (a mash → "tripping the breaker", and it was a *hook*).
3. **Register slips back to brochure** — "we hold three state licenses" (legal), "pinpoint" (marketing verb), "what your system makes" ("system" = trade brochure, say "your AC"), spec sheets jammed into one breath.
4. **Breath length** — anything past ~30 words in one sentence can't be said aloud. Matters because a human performs it.

**Proactively grep before delivering, don't wait to be told.** Slipped through on the [[tsd-gillespie-heating-cooling]] full PPC report (2026-09-11) — drafted the plain-format client PDF with 5 sentence-interruption em dashes still in the prose, sent it, and Edu had to ask for a cleanup pass. Before rendering any client-facing HTML/PDF, `grep -n "—"` the file and apply the cut-test from the AI-tells list above to every hit, rather than relying on writing cleanly the first time.

**No closing offers or sign-off lines in client reports (Edu, 2026-10-12, angry).** Never end a report with lines like "If you'd like to move money between platforms or campaigns, just let us know and we'll lay out what each option would look like." Edu: "never put stuff like this." The report ends on its last piece of content. Same for "let us know if you have questions", "happy to walk through", "feel free to reach out". It came in by copying the 10-08 All Seasons budget report forward; check old templates for these lines too.

**Don't over-correct.** In that same pass I flagged the second-person hooks ("your AC quit", "you found out") as sameness and was **wrong** — naming the prospect's exact situation is what a direct-response hook is *for*. That's a media-planning issue (don't run 14 near-identical-shaped ads at once), not a copy fix. Sanding good lines flat to satisfy a pattern you named is worse than the pattern.
