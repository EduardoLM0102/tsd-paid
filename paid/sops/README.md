# Paid Ads — Launch & Buildout SOPs

The one-time process for launching a new campaign on each channel, from client intake to the 7-day check. Written to be built as staged tasks in **Agency Titan (AT)**: every stage has one owner, an explicit blocker, and a closeout condition.

Requested by Ryan (COO) and Jonathan (CEO) in the AT Processes call on **2026-07-10**. Ryan builds these into AT; the recurring 7/14/30-day optimization processes take over where these end.

## The four SOPs

| Channel | Source of truth | What it covers |
|---|---|---|
| Meta | `meta-ads-launch-buildout.md` | Conversion (CBO + DCT per angle) + always-on Awareness on Ad Recall Lift |
| Google (PPC) | `google-ads-launch-buildout.md` | Search Branded + Non-Branded. **LSA out of scope.** PMax not at launch. |
| YouTube | `youtube-ads-launch-buildout.md` | Conversion (Video Action / Demand Gen) + Video Views for Ad Recall Lift |
| TikTok | `tiktok-ads-launch-buildout.md` | Conversion (Instant Form or Call Ads) + Awareness (no recall-lift objective exists on the platform) |

All four share the same skeleton: 11 stages, AM intake → access → **tracking + end-to-end lead flow test (hard gate)** → research/brief → creative ‖ destination → buildout → QA (hard gate) → launch → 3-day → 7-day.

## Rebuilding the PDFs

The **`.md` files are the source of truth.** The `.html` and `.pdf` are artifacts — never edit them by hand.

```bash
pip install markdown          # once
python3 build_pdfs.py         # rebuild all four
python3 build_pdfs.py meta    # rebuild one: meta | google | youtube | tiktok
```

Renders through headless Chrome in TSD navy/gold. Writes the PDF next to the `.md` **and** into `PDFs/` — that folder is what gets sent to Ryan, so it never drifts from the source.

## Open decisions these SOPs are waiting on

Each is flagged inside the doc where it bites:

1. **Campaign naming convention** (division-wide, all platforms). The Google SOP uses the de facto `TSD_MM.DD_<Type>_<Brand|NonBranded>_<Theme>`. Not formally locked.
2. **CPL / CPV benchmarks per trade and tier.** Don't exist. Until they do, the target comes from the client's own economics, never from a guess.
3. **Meta:** the concrete threshold for "statistical relevance" before isolating a winner (days? spend? conversions?). The doc currently reads at day 7 and says extend rather than force it.
4. **Meta:** do isolated post-ID winners live in the same CBO as the test, or in a separate campaign? The doc assumes the same CBO.
5. **Meta:** the lead flow test still sits in Stage 8 (the native form only exists after buildout). Google/YouTube/TikTok moved it to Stage 3. Decide whether Meta follows.
6. **TikTok:** confirm the two rules carried over from Meta — broad targeting with geo only (let the platform's ML work), and Spark Ads as the winner-isolation mechanism (the analogue of post-ID isolation).
7. **YouTube:** the brief asks Vince for **two distinct videos** (conversion + recall). If the real-world budget is one shoot with two cuts, the SOP needs to say so.
8. **Timings are estimates, not measured cycle times.** Re-baseline after the first real builds.
