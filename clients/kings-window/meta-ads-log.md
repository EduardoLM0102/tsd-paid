# King's Window Services — Meta Ads log

Account 483679897962388.

## 2026-10-26 — AT optimization tasks (Gui, via Claude)

Read-only, nothing changed in Meta.

**7d 10-19..10-25:** $69.90, 0 leads, only the awareness campaign TSD_02.26_TOF_AWARENESS_CBO_Creatives ($10/d, REACH, freq 1.96, CPM $3.67, CTR 0.15%). Prior week $294.65 / 6 leads / $49.11.
**⚠ Lead campaign dark since 10-17:** Guilherme Farias paused both ABO lead ad sets (Power Editor) and turned on the new DCT ad set Richlandtx_Broad_18.65_M.F_Dynamic ($30/d), but its only ad GlassReplace_Ads1,2,3_Dynamic_callform_FO (120254214546330721) failed to create ("Unknown Error When Creating Ad", WITH_ISSUES). 0 impressions since.

**Update 2026-10-26 (later):** the creation failure was a **Meta-side bug**, not a setup error (issue code 2465018, ad stuck in "Update Required"). Gui resubmitted the ad in Power Editor at 5:43 PM: status Update Required → Pending Process; `ads_get_errors` returns 0 errors on the ad and on the ad set (ad set ACTIVE, $30/d, waiting on its only ad). Not serving yet. Recheck 10-27 for impressions and leads; if still pending, turn the old GlassReplace ad set back on as a stopgap.

**Recheck 2026-10-27: NOT fixed.** At 5:51 PM on 10-26 (8 min after the resubmit) the ad fell back to WITH_ISSUES with the same error ("Unknown Error When Creating Ad: Something went wrong when creating your ad. Please try creating your ad again."). 0 impressions, $0 on 10-27. Resubmitting the same ad does not clear it: create a new ad in the DCT ad set and delete the broken one, or re-enable the old GlassReplace ad set as a stopgap. AT 7-Day + 30-Day Meta notes corrected.
**30d 09-26..10-25:** lead campaign $945.54 / 28 leads / $33.77. Winner GlassReplace_Image_callform_FO $627.38 / 24 / $26.14 (control); mirror ad $318.16 / 4 / $79.54. Awareness ad set $301.37, reach 24,103, freq 3.53, hook 16.81%, retention 6.72%, no ARL (REACH + cap 3/7d).

**Staged, not applied:** recreate the DCT ad (or reactivate the GlassReplace ad set as stopgap); lead campaign to CBO; awareness rebuild as ARL no cap (from 10-19); refresh awareness videos (running since 02-26); 2nd angle test (same-day broken glass) as its own DCT ad set.

Tasks (completed): [7-Day Meta](https://app.agencytitan.com/tasks/instance/492ee1ff-e02b-42db-bb1a-28e106b96829), [30-Day Meta](https://app.agencytitan.com/tasks/instance/7f437bd5-fa5f-4cce-84fb-de0e383594af). KPI - Meta 594bfb89.
