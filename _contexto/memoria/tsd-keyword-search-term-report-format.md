---
name: tsd-keyword-search-term-report-format
description: "Exact visual standard for TSD \"Keyword & Search Term Report\" PDFs (per-industry data reports) — portrait Georgia, not the plain Times/black-border recipe used for client performance reports"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 98c9f421-24cc-4cf4-a450-8870d55ec67d
  modified: 2026-09-14T09:53:02.629Z
---

TSD's "Keyword & Search Term Report" deliverables (one per industry/campaign — e.g. Proud Pops has
separate Plumbing/Electrical/HVAC reports, Hawkins Siding has one for its single siding campaign) follow
a **different, more refined visual standard** than [[tsd-client-report-plain-design]]'s stark black-border
Times New Roman recipe. Found by reverse-engineering the actual Proud Pops PDFs (built by a separate
session) after a first Hawkins attempt (landscape, pure-black-border Times) was rejected as not matching.

**Reverse-engineered spec** (via PyMuPDF font/color/geometry extraction — `page.get_fonts()`,
`get_text("dict")` span colors/sizes, `get_drawings()` fill colors):

- **Portrait Letter**, not landscape, even for wide 10-column tables — columns compress and keyword text
  wraps to 2+ lines rather than widening the page. Margins ~0.85–0.95in (top slightly larger, ~0.95in).
- **Font: Georgia** (not Times New Roman) — title 18pt bold, section headings (`##`) 14pt bold, body 12pt
  regular, line-height ~1.5. Table text 8.5pt, both header and body cells.
- **Text color #111111** (soft near-black), not pure #000.
- **Tables**: header row background `#ededed` bold; body rows zebra-striped `#fafafa` / white alternating;
  borders 1px solid `#999999` (mid-gray, not black). This is a deliberate soft-gray data-table look, not
  the "no color anywhere" plain-recipe rule — it still reads as restrained/non-"AI-designed", just less
  severe than pure black-on-white.
- **Header meta block** (Account/Campaign/Date range/Pulled/Scope) renders as **one flowing paragraph**,
  not separate lines — because the source markdown has no blank lines between those fields, so standard
  markdown rendering collapses them. Author it that way if hand-writing HTML instead of converting markdown.
- Thin `#bbbbbb` `<hr>` rule between major sections.

**Structure** (3 sections, same on every industry report): 1. Best Keywords (current targeting, ranked by
conversions) 2. Top Converting Search Terms (actual queries, with a "Matched Keyword (Match Type)" column
via `segments.keyword.info` on `search_term_view` — see [[tsd-proud-pops-deliverables]]-adjacent scripts,
e.g. `hvac_terms.py` / `hawkins_kw_st_report.py` in the google-ads-ratos skill) 3. High-Volume Search Terms
With Zero Conversions (negative-keyword / new-ad-group candidates). Date range = full lifetime of the
current campaign (by campaign creation date in its name), not a rolling 30-day window — richer data,
matches what the precedent used.

**How to apply:** when asked for a "keyword and search-term report" or "PDF report like the ones for
[client]," build this exact spec, not the plain Times/black-border client-report recipe — this is an
internal/reference data document, a different deliverable class than a client-facing performance summary.
QA by rendering to PNG with PyMuPDF before sending, same as the plain-recipe workflow.

**Tooling note:** this Mac has no Google Chrome install (`/Applications/Google Chrome.app` doesn't exist)
despite it being the default recipe elsewhere — use Playwright's bundled Chromium instead
(`playwright.sync_api`, `page.pdf(...)`) which is already cached at `~/Library/Caches/ms-playwright`.

**Content scope — match the precedent exactly, don't layer in analysis.** First Hawkins draft added two
extra callout paragraphs beyond the 3 tables + methodology footnote (a "data-quality flag" note and a
"biggest un-blocked leak" note) — genuinely useful findings, but not present in any of the three Proud
Pops reports and not asked for. Edu caught it: "is the same info in the Hawkins report as we have in the
Proud Pops one? Or did you add more things... that I didn't ask for?" **When told to match an existing
report's standard, that means structure AND content scope, not just visual styling** — reproduce exactly
what the precedent contains (header block, table 1, table 2, table 3, methodology footnote, nothing else),
even when extra analysis is obviously true and useful. Surface findings like that in the chat response
instead, or ask before adding them to the deliverable.
