---
name: topserv-client-report-format
description: "How to build a TopServ client-facing Google Ads report — 1-page PDF recipe + the golden framing rule (never signal a problem, frame every fix as proactive optimization)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c824868d-c8a7-4be1-bd2f-b3c0347fc9b2
---

For TopServ (TSD) client-facing paid-ads reports:

**Golden framing rule:** NEVER flag to the client that anything was wrong. Frame every fix as routine, proactive optimization. Banned words in client copy: problem, issue, gap, leak, unprotected, mistake, wasted, "fix." Use instead: refined, sharpened, focused, tuned out, optimization, weekly review. (Example: negative keywords added to stop off-service leads were presented as "search refinements applied to your live campaign," shown as chips.) This is a standing client-comms stance, not a one-off.

**Internal vs client split:** keep the honest root-cause version in the client's internal `clients/<slug>/google-ads-log.md` (and internal `report_*.md`); the client PDF is the sanitized, upside-focused version.

**Build recipe (1-page PDF):** English (US company). Write standalone HTML → render with headless Chrome: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=out.pdf in.html`. Letter size via `@page { size: Letter; margin: 0 }` + `print-color-adjust: exact`. QA by screenshotting the HTML (`--screenshot`, `--window-size=816,1056`) and reading the PNG, then delete the temp PNG. Layout used: navy/gold header w/ Brandformance tagline, lead blurb, "What we optimized" bullets, refinement chips, "What this means for you" 3-card row, "What's next," confidential footer.

**Placeholder branding:** no official TSD brand colors/logo in the workspace — used navy (#12305a) + gold (#c9a24b). If real brand assets surface, restyle.

**Navy/gold is for CLIENT-FACING reports only. Internal/production docs go PLAIN.** On 2026-07-17 Edu took a designed navy/gold script doc and asked to "wipe out any design and make it look plain, like I just downloaded from Word." Plain = **Times New Roman 12pt, 1in margins, black on white, no color, no cards/boxes/rules, bold headings, italics for stage direction** (Calibri is NOT installed on his Mac — don't reach for it). Same headless-Chrome recipe, just different CSS. Since styling is only CSS and the content lives in markdown, designed↔plain is always cheap to reverse.
**Unverified boundary:** he asked for this on an internal script/shoot doc, not on a client report. Whether client-facing reports should also go plain was never asked and never answered — ask before restyling one.

**Governance:** client comms route through the AM's ticket — build the artifact for Edu to hand off, don't imply direct send. See [[topserv-google-ads-location]].
