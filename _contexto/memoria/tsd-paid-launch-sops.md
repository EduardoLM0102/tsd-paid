---
name: tsd-paid-launch-sops
description: "The four TSD paid-launch SOPs (Meta, Google PPC, YouTube, TikTok) — where they live, the shared 11-stage skeleton, how to rebuild the PDFs, and the decisions still open"
metadata: 
  node_type: memory
  type: project
  originSessionId: bd678abb-0ca3-4a79-8b13-48930b7ac06a
---

Eduardo's launch & buildout SOPs for the TopServ Paid Ads division, written 2026-07-12/13. Requested by Ryan (COO) in the AT Processes call of 2026-07-10 — Ryan builds them into **Agency Titan (AT — always call it "AT" in these docs)** as staged tasks; the recurring 7/14/30-day optimization processes take over where they end.

**Location:** `~/Documents/GitHub/topserv-workspace/paid/sops/` — `meta-`, `google-`, `youtube-`, `tiktok-ads-launch-buildout.md`. The `.md` is the source of truth. `python3 build_pdfs.py [meta|google|youtube|tiktok]` regenerates the styled HTML + PDF (headless Chrome, TSD navy/gold) and refreshes `PDFs/`, the folder sent to Ryan. Full index and open decisions in `paid/sops/README.md`.

**Shared 11-stage skeleton:** AM intake → access/billing → **tracking + end-to-end lead flow test (hard gate)** → research/brief → creative ‖ destination → buildout → QA (hard gate) → launch → 3-day → 7-day.

**Doctrine per channel** is summarized in `topserv-workspace/_contexto/preferencias.md` (Meta method in [[tsd-meta-ads-methodology]]; Google/YouTube/TikTok added there too).

**How these were written — the rule that matters:** doctrine came from Eduardo's own words and his real client logs (All Heart, Hawkins, Mission, Zen Air, Napps audit), never invented. The first draft of the Meta SOP invented a campaign structure and he caught it. **Do not invent paid methodology for him — ask, or pull it from the logs.**

**Why:** these are a formal deliverable to the COO and become the division's standard; a fabricated rule inside them becomes how the whole team executes.

**How to apply:** editing these = edit the `.md`, rerun `build_pdfs.py`. Style notes he enforced: no gimmicky rhetorical lines, stage table stays at the top, no forcing of back-end mechanics into the doc, and no client copy-approval step (removed on purpose — info comes from AT; if a client wants something removed later, that's fine).
