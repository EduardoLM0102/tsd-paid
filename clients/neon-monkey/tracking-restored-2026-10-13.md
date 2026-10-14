# Neon Monkey: Site tracking restored (2026-10-13)

Context: the site lost its GTM container around Aug 29–31 (see `action-plan-2026-10-08.md`, Phase 1). We sent
the GTM code over and the site installed it. This is the check that it's live. Read-only, nothing changed in
Google Ads or GTM.

## Result: back on since ~9am CT, Oct 13

| Check | Result |
|---|---|
| Snippet on the site | `GTM-WM9CDGPT` installed correctly: script in `<head>`, noscript right after `<body>`. Checked homepage, /contact/, /services/tree-service/tree-trimming/ (curl). |
| GA4 `328458299` (G-WF5DBMQ644) | First real site sessions since August, starting 2026-10-13 09:00 CT. By 6pm CT: 11 sessions, 19 page views, 8 first visits, scroll + engagement events. Partial day with GA4 processing lag, so compare to the 40–80/day norm from Oct 14. |
| GTM container (acct 6264215029, container 203561665) | Intact. Live = **v11**, 19 tags, Default Workspace has 0 pending changes. |
| Google Ads `7953905280` | Only `Calls from ads` recorded Oct 6–13 (1 each on 10-07, 10-10, 10-12, 10-13). No site-tag conversions yet. |
| Browser test | Not possible: the site shows a "Checking your browser" wall to headless Playwright (403), while curl gets the real page. No Chrome on this Mac. Verify via curl + GA4. |

## Open issue: phone taps are now a biddable conversion

The live container is not the v10 we audited on 10-08. **v11 was published Sat 2026-10-10 15:40 BRT**, not by
us, no version name or notes. Its only change vs v10 is one added tag:

- `Google Ads | Phone Call Click` (awct, label `a504CPz3mZgdEIy01Kso`, trigger `Link Click - Phone Number`)
- It feeds a new conversion action **`[TSD] Click to call`** `7835384828`: CLICK_TO_CALL, category
  PHONE_CALL_LEAD, primary, one per click.
- `PHONE_CALL_LEAD/WEBSITE` is **biddable on both Search campaigns** (Branded `23739724064` and Nonbranded
  Trimming `23825900343`). So every tap on a phone number now counts as a conversion, and Nonbranded on
  Maximize Conversions will bid toward taps.

This goes against the action plan ("Don't make phone-link taps a primary conversion when the tag comes
back", the Proud Pops lesson). No taps had been counted when this was checked, so it's clean to fix now.

- **Suggested fix (needs Edu's OK):** recategorize `[TSD] Click to call` to CONTACT, which isn't biddable on
  these campaigns. It stays visible in All conversions. Don't turn the `PHONE_CALL_LEAD/WEBSITE` goal off,
  because it also carries `NMS Website Calls`, the real website-call action from Phase 1 step 2.
- **Who created it:** unknown. Google Ads `change_event` doesn't cover conversion actions (0 account changes
  logged 10-09 → 10-14). Check with the team before changing it.

Biddable goals on live campaigns as of 10-13:
- Branded: PHONE_CALL_LEAD/WEBSITE, PHONE_CALL_LEAD/CALL_FROM_ADS
- Nonbranded: DEFAULT/WEBSITE, PHONE_CALL_LEAD/WEBSITE, PHONE_CALL_LEAD/CALL_FROM_ADS
- `Submit lead form - web` (SUBMIT_LEAD_FORM, fired by GTM `Google Ads | Event | Lead`) is **not** in a
  biddable goal on either Search campaign. Review in Phase 1 step 4.

## Still owed (Phase 1 step 6, Command Center fu-028, due Oct 19)

- One test form and one test call recorded end to end
- GA4 back to ~40–80 sessions/day
- The `[TSD] Click to call` decision above
- Whether CallRail (loads via GTM) now swaps the site's toll-free numbers, and whether the `Phone Call`
  offline upload resumes

## Scripts (read-only)

In `.claude/skills/google-ads-ratos/scripts/`: `neon_monkey_gtm_live_1013.py`, `neon_monkey_gtm_diff_1013.py`
(v10 vs v11), `neon_monkey_ga4_recovery_1013.py`, `neon_monkey_conv_actions_1013.py`, `neon_monkey_goals_1013.py`.
