---
name: tsd-client-report-plain-design
description: "RESOLVED boundary — TSD CLIENT-FACING reports go plain Word-style too, not navy/gold; Edu called the designed version 'too AI looking'"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 10ac7dae-7a18-48b0-b4b9-a0a220dea0d0
  modified: 2026-07-31T13:51:34.751Z
---

TSD **client-facing** reports go **plain**, like a Word document. Resolved 2026-07-31 on the GC Home
Service weekly update: I built it navy/gold per [[topserv-client-report-format]] and Edu said
*"make it more plain. It's too AI looking."*

This closes the "unverified boundary" flagged in [[topserv-client-report-format]] (plain was only
ever confirmed for internal/production docs; whether client reports should also go plain was never
asked). **Answer: yes, plain for client reports too.** Default to plain; treat navy/gold as the
exception that needs asking for.

**What reads as "AI looking" and must go:** gradient header bars, KPI card rows, colored chips/pills,
green highlight numbers, tinted callout boxes, uppercase letterspaced micro-headings. The decoration
is the tell, not the writing.

**Plain recipe** (same headless-Chrome build, different CSS): Times New Roman 12pt, black on white,
`@page { size: Letter; margin: 0.85in 1in }`, bold section headings, bold-italic subheads, standard
disc bullets, tables with plain 1px black borders all around. No color anywhere.

**Layout gotchas learned building it:**
- `page-break-after: avoid` on headings prevents orphaned headings but strands whole blocks and can
  *add* a page. If it pushes you over, fix it with `line-height` (1.24 is fine and still looks like
  Word single spacing), not by removing the rule.
- Never leave a final page holding one paragraph. Fold a trailing note into the last list item.
- QA by rendering PDF pages to PNG with **PyMuPDF** (`fitz`, installed) since `pdftoppm`/poppler is
  NOT on this Mac and the Read tool's PDF rendering fails without it. Measure fill with
  `max(b[3] for b in page.get_text('blocks'))` to find stranded whitespace.

Composes with [[tsd-client-facing-voice]] (how it sounds) and [[topserv-client-report-format]]
(the golden framing rule, which still governs *what* you say).
