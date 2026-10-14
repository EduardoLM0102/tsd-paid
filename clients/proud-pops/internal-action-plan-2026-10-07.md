# Proud Pops — Internal Action Plan (2026-10-07)

Everything here is ours to do in the account now, with no client input or approval needed.
Items that need the AM or client are in `am-client-action-plan-2026-10-07.md`.

Google Ads 1051843378 · GTM-WBFDB6L8 (account 6255217830, container 198527160, Default Workspace 43, live v41) ·
GA4 438523825

**Order matters:** the GTM fix (step 1) goes live and is verified before the phone-tap change (step 12).
Otherwise form leads become the only bidding signal while they're still ~75% job applications.

---

## Now: Oct 7–9

### GTM

**1. Remove job applications from the lead trigger** (draft in workspace 43)
- Trigger `[80] cEvent - Lead` (`ghl_form_submit`): change to Some Custom Events and add
  `{{Page Path}}` does not contain `/careers`.
- New variable `dlv - ghl_form_id` (Data Layer Variable `ghl_form_id`, v2). Add a second condition to `[80]`:
  `{{dlv - ghl_form_id}}` does not equal `ThmcYYHImwSoYS9oBt3n`. A missing form ID still passes, so customer
  forms can't be blocked.
- This one trigger feeds `[82] G.Ads - Lead`, `[90] GA4 - Lead`, `[94] G.Ads - User-provided Data` and
  `[111] Meta - Lead`, so all four are fixed at once.
- Don't touch the two listeners `[99]` and `[123]`. The `dlv - Email/Phone/...` variables read the flat keys
  only `[99]` pushes.

**2. Give job applications their own event**
- New trigger `cEvent - Job Application`: `ghl_form_submit`, Page Path contains `/careers`.
- New tag `06 | GA4 - Job Application`: GA4 event `job_application`, `page_location = {{Page URL}}`.
- No Google Ads or Meta tag for it.

**3. Test in Preview without creating GHL contacts**
- On `/careers`, run in the console: `dataLayer.push({event:'ghl_form_submit', ghl_form_id:'ThmcYYHImwSoYS9oBt3n'})`.
  Expected: only `06 | GA4 - Job Application` fires. None of the `05 |` lead tags fire.
- On `/schedule` (reached by clicking through from the HVAC page, not a fresh load), run
  `dataLayer.push({event:'ghl_form_submit', email:'tsd-test@example.com'})`.
  Expected: the `05 |` lead tags fire. Job Application doesn't.
- Without an ad click, Google Ads won't record anything. GA4 gets one test event from
  `tagassistant.google.com / referral`; ignore it in readouts.
- A real end-to-end submit is optional. It creates a GHL contact, so it's coordinated through the AM.

**4. Publish** (Edu approves)
- Version: `TSD - Exclude careers job applications from lead conversions (2026-10-0X)`.
- Re-list workspaces afterwards and confirm the live version is the new one.

**5. Fix the Meta lead tag** (separate version, low priority)
- `[111] 05 | Meta - Lead` sends `PageView`, not `Lead`. Switch it to the standard `Lead` event. It inherits the
  careers exclusion from step 1.

### Google Ads

**6. Stop PMax sending traffic to /careers.** Both PMax campaigns → Final URL expansion → URL exclusions →
`proudpops.com/careers`. Do PMax HVAC too, in case it's re-enabled.

**7. Job-seeker negatives at account level** (these also cover PMax search traffic): jobs, job, hiring,
careers, career, apprentice, apprenticeship, salary, employment, indeed.

**8. Call extension**
- Create a call asset with the site's real number, 210-225-5767. Attach it at account level and on all 6
  lead campaigns, and remove the disapproved 210-794-7570.
- If Google asks for verification beyond the website check, that goes to the AM (plan 2).

**9. Raise the `Calls from ads` minimum duration from 15s to 60s.** It's the account's call conversion
action. Nothing is lost today because it records 0 calls.

**10. Point Search ads at the right service pages**
- Electrical Search → `/services/electrical`. Plumbing Search → `/services/plumbing`.
- Both pages exist and already get traffic (157 and 31 views in 30 days). Check that each has the schedule CTA
  before swapping.
- Today only HVAC has its own page. Electrical and Plumbing still go to the homepage.

**11. Competitor negatives on Plumbing:** Beyer Boys, The Bearded Plumber, George's Plumbing, Bryco (from the
Sep 14 search-term report).

### GA4

**12. Clean up key events**
- Mark `generate_lead` as a key event. It's not one today.
- Unmark the 11 current key events. All are click events or dead txproblemsolvers.com events:
  `ads_conversion_Form_1`, `purchase`, `book_now_link_click`, `phone_link_click`, `mailto_link_click`, `Shop`,
  `ghl_contact_us`, `Schedule Online`, `instant_roof_quote_click`, `instant_quote_hvac_click`, `button_schedule_online`.
- The GA4-imported actions in Google Ads are already secondary, so this doesn't change bidding.
- Leave `job_application` as a normal event, not a key event.

### LSA

**13. Check all 3 LSA profiles in the Google Ads UI** (in-account, 7261668241, 6621969129):
- profile status, weekly budget, job types, service areas, business hours
- verification status (license, insurance, background check)
- reviews, missed calls

The data so far: impressions went from ~1,900/week combined in late July to near zero. 6621969129 has had none
since mid-September. Anything that needs the client (documents, answering calls, reviews) goes to the AM.

---

## After the GTM fix is verified: Oct 12–13

**14. Verify step 1 live (Oct 9–12)**
- GA4: no `generate_lead` on `/careers` after publish; `job_application` appears.
- Google Ads: `Website lead` falls to about a quarter of the old daily rate (~6/day → ~1.5/day). PMax
  Electrical drops the most.

**15. Phone taps to Secondary** (only after the AM heads-up has gone out, plan 2)
- In the UI, set `TSD - Website Call` to Secondary. Don't switch off its whole goal: `Calls from ads` shares it
  and becomes the real call signal once step 8 is live.
- Verify via API the next day: all_conversions > 0, conversions = 0 for that action.
- Fallback if it doesn't take: switch the goal off per campaign.

**16. Remove the $265 target CPA on Search HVAC** the same day. At ~$920 per customer form, it would choke
delivery.

**17. PMax Electrical:** keep it live 2 weeks on the clean signal. Fewer than 5 customer forms by Oct 26 →
recommend pausing it (that pause goes through the AM).

## Ongoing: Oct 13–30

**18. Geo:** widen HVAC and Plumbing Search beyond San Antonio city to the cities LSA already serves (47).
Budgets stay the same.

**19. Ad Rank:** RSA and expected-CTR work on non-branded Search. CPCs average $29 and 49–61% of impressions
are lost to rank.

**20. Re-baseline Oct 26:** per campaign: spend, customer forms (careers excluded), `Calls from ads`, LSA calls,
and CallRail calls if connected by then.

**21. Later cleanup:** merge the two GHL listeners (keep `[123]`, remap the `dlv` variables to `ghl_data.*`,
remove `[99]`, retest enhanced conversions).

**22. Log each step in Agency Titan** and in `google-ads-log.md`.
