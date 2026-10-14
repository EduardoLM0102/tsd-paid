---
name: primary-text-mobile-scannability
description: "Formatting rule for Meta Primary Text — must be scannable on mobile UI, applies to every TSD account"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 303be81e-77a2-468f-8ce8-3550629cf63a
  modified: 2026-08-18T00:36:20.631Z
---

Every Primary Text has to be scannable in the mobile Feed/Reels UI, not just short in word count.

Rules:
1. **Max 3 lines as rendered on mobile** before it wraps/truncates. This is stricter than a character count — check how it actually breaks on a phone-width column, not just total length.
2. **No two same-length paragraphs back to back.** Consecutive blocks of similar length read as a wall of text even if each one is short; vary the rhythm.
3. **Ideal shape = one short paragraph (the hook/lead) + a bullet list with emoji underneath.** The paragraph carries the angle, the bullets carry the proof/features/benefits in scannable chunks instead of a second paragraph.

**Why:** Edu wants Primary Text to read as scannable at a glance in the mobile feed, not as prose that happens to be short. A short paragraph can still fail this if it's followed by another same-shaped paragraph — the eye can't find an entry point.

**How to apply:** treat this as a structural check on top of each account's existing tone/length rules ([[tsd-own-ad-copy-format]], [[tsd-client-facing-voice]]) — those govern voice and word choice, this governs the shape on the page. When drafting Primary Text, default to: hook paragraph (1-2 lines) → blank line → 2-4 emoji bullets → (optional) short closing line/CTA. Avoid stacking two full paragraphs of prose.
