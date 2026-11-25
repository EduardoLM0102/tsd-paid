# King's Window Services — Meta Ads log

Account 483679897962388.

## 2026-11-19 — Client Video Audit: 9 finished video ads never reached Paid

9 finished ads from Oct 13 sit in Sara's 'KINGS ADS' folder (copied 10-27); no task to Paid, no approval task. Meta still runs old AD I-IV (video 31% of $445/14d); lead ad static. Next: AM confirms client approval, then launch same day (fu-187).
Full audit + readiness plan: `paid/relatorios/client-video-audit-2026-11/README.md`.

## 2026-10-26 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in Meta.

**7d 10-19..10-25:** $69.90, 0 leads, only the awareness campaign TSD_02.26_TOF_AWARENESS_CBO_Creatives ($10/d, REACH, freq 1.96, CPM $3.67, CTR 0.15%). Prior week $294.65 / 6 leads / $49.11.
**⚠ Lead campaign dark since 10-17:** Guilherme Farias paused both ABO lead ad sets (Power Editor) and turned on the new DCT ad set Richlandtx_Broad_18.65_M.F_Dynamic ($30/d), but its only ad GlassReplace_Ads1,2,3_Dynamic_callform_FO (120254214546330721) failed to create ("Unknown Error When Creating Ad", WITH_ISSUES). 0 impressions since.

**Update 2026-10-26 (later):** the creation failure was a **Meta-side bug**, not a setup error (issue code 2465018, ad stuck in "Update Required"). Gui resubmitted the ad in Power Editor at 5:43 PM: status Update Required → Pending Process; `ads_get_errors` returns 0 errors on the ad and on the ad set (ad set ACTIVE, $30/d, waiting on its only ad). Not serving yet. Recheck 10-27 for impressions and leads; if still pending, turn the old GlassReplace ad set back on as a stopgap.

**Recheck 2026-10-27: NOT fixed.** At 5:51 PM on 10-26 (8 min after the resubmit) the ad fell back to WITH_ISSUES with the same error ("Unknown Error When Creating Ad: Something went wrong when creating your ad. Please try creating your ad again."). 0 impressions, $0 on 10-27. Resubmitting the same ad does not clear it: create a new ad in the DCT ad set and delete the broken one, or re-enable the old GlassReplace ad set as a stopgap. AT 7-Day + 30-Day Meta notes corrected.
**30d 09-26..10-25:** lead campaign $945.54 / 28 leads / $33.77. Winner GlassReplace_Image_callform_FO $627.38 / 24 / $26.14 (control); mirror ad $318.16 / 4 / $79.54. Awareness ad set $301.37, reach 24,103, freq 3.53, hook 16.81%, retention 6.72%, no ARL (REACH + cap 3/7d).

**Staged, not applied:** recreate the DCT ad (or reactivate the GlassReplace ad set as stopgap); lead campaign to CBO; awareness rebuild as ARL no cap (from 10-19); refresh awareness videos (running since 02-26); 2nd angle test (same-day broken glass) as its own DCT ad set.

Tasks (completed): [7-Day Meta](https://app.agencytitan.com/tasks/instance/492ee1ff-e02b-42db-bb1a-28e106b96829), [30-Day Meta](https://app.agencytitan.com/tasks/instance/7f437bd5-fa5f-4cce-84fb-de0e383594af). KPI - Meta 594bfb89.

## 2026-11-03 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in Meta.

**7d 10-27..11-02:** $71.83, 0 leads, awareness only (TSD_02.26_TOF_AWARENESS_CBO_Creatives: 21,893 impr, reach 11,195, freq 1.96, CPM $3.28, CTR 0.16%, hook 14.4%, retention 6.2%). Prior week $70.12 / 0.
**⚠ Lead campaign STILL DARK (17 days, since 10-17):** ad GlassReplace_Ads1,2,3_Dynamic_callform_FO (120254214546330721) still WITH_ISSUES, 'Unknown Error When Creating Ad' (code 2465018). Activity log: no change since the 10-26 5:51 PM fallback. DCT ad set ACTIVE ($30/d) but $0; old ABO ad sets PAUSED.

**Staged, not applied:** create a NEW ad in the DCT ad set and delete the broken one, or re-enable the old GlassReplace ad set as stopgap (urgent); lead campaign to CBO; awareness as ARL no cap; refresh awareness creative.

Task (completed): [7-Day Meta](https://app.agencytitan.com/tasks/instance/40dbd800-414f-49b4-9d1e-ea9fb3570d8e). KPI - Meta cde68bf8.

## 2026-11-09 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in Meta.

**7d 11-02..11-08:** $66.97, 0 leads, awareness only (TSD_02.26_TOF_AWARENESS_CBO_Creatives: 23,754 impr, reach 12,358, freq 1.92, CPM $2.82, CTR 0.14%, $5.42 per 1,000 reached, hook 14.1%, retention 6.9%). Prior week $72.16 / 0.
**⚠ Lead campaign STILL DARK (23 days, since 10-17):** ad 120254214546330721 still WITH_ISSUES (code 2465018, last update 10-26 17:51). Activity log since 11-01: only a billing event, nobody touched it. Old ABO ad sets paused.

**Staged, not applied:** NEW ad in the DCT ad set (delete the broken one) or re-enable the GlassReplace ad set as stopgap (urgent, 3rd week); lead campaign to CBO; awareness as ARL no cap; refresh awareness creative.

Task (completed): [7-Day Meta](https://app.agencytitan.com/tasks/instance/f4c80451-60b9-4cdb-8e9e-46302cab1b64). KPI - Meta 553e77bd.

## 2026-11-16 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in Meta.

**7d 11-09..11-15:** $316.48, 8 leads, $39.56 per lead on all spend, CPM $10.53, CTR 0.44% (prior $66.98 / 0). Lead ad set Richlandtx_Broad_18.65_M.F (back ON 11-10, Edu): $246.41 / 8 leads / $30.80 CPL, CTR 1.37%, freq 1.80, only ad GlassReplace_Image_callform_FO (control). Awareness TX_Broad_Homeowners_18.65_M.F (REACH, cap 3/7d): $70.07, reach 11,553, freq 1.95, CPM $3.11, CTR 0.13%, creative since 02-26.
**⚠ Broken DCT ad set Richlandtx_Broad_18.65_M.F_Dynamic (120254214478390721) still ACTIVE at $30/d**, $0; ad 120254214546330721 still WITH_ISSUES. Activity log since 11-09: only the 11-10 re-enable. Not touched.

**Staged, not applied:** pause the DCT ad set (or delete its ad) so it can't double lead spend if Meta clears the error, rebuild from scratch without the Willis TX pin; lead campaign to CBO; awareness as ARL no cap + creative refresh; same-day broken glass angle test; ask AM how the 8 leads turned out.

Task (completed): [7-Day Meta](https://app.agencytitan.com/tasks/instance/6e65176c-a2a6-4450-a70c-64545f4f49c2). KPI - Meta 045c490c.


## 2026-11-16 (later) — APPLIED: broken DCT ad set PAUSED (Gui's go)

Ad set 120254214478390721 'Richlandtx_Broad_18.65_M.F_Dynamic' (campaign TSD_04.29_BOF_Leads_Evergreen, $30/d, ad stuck WITH_ISSUES since 10-17, $0 spend last 7d) set PAUSED via Meta MCP (live pause, is_draft false), read back PAUSED/PAUSED. Live lead delivery stays on the re-enabled ABO ad set Richlandtx_Broad_18.65_M.F. Prevents the $30/d doubling if Meta ever clears the creation error. A rebuild without the Willis TX pin stays a staged rec.

## 2026-11-24 — AT tasks (Gui, via Claude)

Read-only, nothing changed in Meta.

**7d 11-17..11-23:** $290.08 / 11 leads / $26.37 per lead on all spend, CPM $10.72, CTR 0.45%, freq 2.01 (prior $342.04 / 9 / $38.00). Lead ad set Richlandtx_Broad_18.65_M.F: $220.32 / 11 / $20.03 CPL (best week since the 11-10 re-enable), CTR 1.58%, freq 1.80, only ad GlassReplace_Image_callform_FO. Awareness TX_Broad_Homeowners_18.65_M.F (REACH, cap 3/7d): $69.76, reach 10,242, freq 2.03, CPM $3.35; IMAGE_..._V3 takes 83%. Activity since 11-16: only Gui's DCT ad set pause + billing 11-18.

**Staged, not applied:** keep lead ad set as is; awareness ARL no cap + creative refresh folds into the Growth Engine brand build (1496977c, fu-196); lead campaign to CBO + 2nd angle DCT rebuilt without Willis pin; ask AM how the Meta form leads since 11-10 turned out.

Task (completed): [7-Day Meta](https://app.agencytitan.com/tasks/instance/943187a2-dbee-4326-b490-ee63ec35bd21). KPI - Meta 8ee752bb.
