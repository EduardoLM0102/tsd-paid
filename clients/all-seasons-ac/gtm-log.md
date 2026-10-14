# All Seasons AC — GTM log

Container `GTM-T7BZWVQ` (GTM account `6000633807` "All Seasons", container `30715121`). CID `4467722415` (see `google-ads-log.md`). Site `seasonsair.com`, WordPress + Elementor + NitroPack.

---

## 2026-08-13 — New Lead/Phone Click conversion tags (draft) + GA4 data source disconnected in Ads

**Trigger.** Follow-up cleanup on the tracking mess found 2026-08-11: `book_now_link_click` inflating PMax conversions, four near-dead `ghl_*` conversion actions fed by server-side GHL events invisible to GTM, and GA4 sending whatever junk events it has straight into Ads as conversions via the GA4 data source link.

**What Edu built in GTM — workspace 26 (Default Workspace; supersedes workspace 23 from 2026-08-11, which was published and closed out as version 22, then 24).**

- **Trigger 45 "Lead Trigger"** (Custom Event) — fires when `{{_event}}` equals `ghl_form_submit`.
- **Tag 46 "03 | G Ads - Lead"** (`awct`, Google Ads Conversion Tracking) — fires on trigger 45. Conversion ID `{{Conversion ID}}`, label `OB9ECJu6luEcENjDqPsC`.
- **Tag 49 "03 | GA4 - Lead"** (`gaawe`) — also fires on trigger 45, GA4 event name `lead`.
- **Tag 47 "02 | G Ads - Phone Click"** (`awct`) — fires on the existing trigger 13 ("Link Click - Phone Number"), the same trigger already driving GA4 Phone Click (tag 29). Label `RapPCNGoieEcENjDqPsC`.
- **Tag 48 "01 | GA4 - PageView"** — rebuilt page_view tag on the built-in All Pages trigger. Old duplicate config tag (32, "GA4 - Configuration", flagged 2026-08-11 as untidy hygiene) no longer appears in this workspace — looks consolidated away as part of this pass.
- **Net effect once published:** lead tracking collapses from the five scattered server-side `ghl_*` events onto one client-side `ghl_form_submit` custom event, paired with a dedicated Phone Click conversion mirroring the GA4 one that already existed.
- **Status: NOT published.** Live container version is still 24 (from the 2026-08-11 fix). Confirmed via `versions().live()` — none of the above is affecting real traffic yet.
- **Open verification:** `ghl_form_submit` is not one of the event names the 2026-08-11 audit found anywhere (those were all server-side GHL events, invisible to GTM/page source). Confirm in GTM Preview that GHL's form embed actually pushes this event to the dataLayer on submit before publishing — otherwise trigger 45 never fires and tags 46/49 stay silent.

**What Edu did in Google Ads (not GTM).** Disconnected GA4 as a data source in the Ads account's conversion/data-source settings, so GA4 events (including whatever junk was flowing through, e.g. the inflated `book_now_link_click` events) can no longer auto-populate as Ads conversions. Once the new `awct` tags (46, 47) above are live, Google Ads conversion tracking runs off its own dedicated tags — Lead and Phone Click — instead of importing from GA4. Also logged in `google-ads-log.md`.

**Open / next steps:**

- [ ] Verify `ghl_form_submit` actually fires (GTM Preview, real form submit) before publishing workspace 26.
- [ ] Once verified, publish workspace 26 and confirm live via `versions().live()`.
- [ ] After publish, confirm in Ads which conversion actions are still receiving events vs. gone quiet (the old `ghl_*` actions and anything that depended on the GA4 import should go to zero).
- [ ] Carry over unresolved items from 2026-08-11: orphaned dead tag in workspace "1" (still not deleted), and the `campaign_conversion_goal` read-first pass for excluding near-dead conversion actions from bidding goals.

---

## 2026-08-11 — GTM tracking review + book_now_link_click trigger fix

**Trigger.** Follow-up to the PPC executive summary session, which flagged PMax's "conversions" as suspicious (mostly `book_now_link_click`, not verified leads). This session had GTM access to check where tracking actually originates.

**Findings:**

1. **Two separate tracking pipelines feed GA4 (and from there, Ads' conversion import) — only one goes through GTM.**
   - GTM (browser click tracking): `page_view`, `phone_link_click`, `mailto_link_click`, `book_now_link_click`.
   - GoHighLevel (server-side, entirely outside GTM): `ghl_contact_us`, `ghl_book_now`, `ghl_installation`, `ghl_schedule_service`, `ghl_service_contract`. Confirmed by pulling the actual GHL form iframe source directly (`link.leadnurturemachine.com/widget/form/wKOrv1V0SICIaUaCwzYA`, a white-labeled GHL domain) — zero gtag/GA4/GTM code in it. These fire from GHL's backend on CRM contact/workflow events, invisible to GTM and to page source.

2. **Root cause of PMax's inflated "conversions."** Trigger 22 ("Link Click - Book Online") matched *any* link whose URL contains "contact-us" — including the plain nav "Contact Us" menu item (8 of the 14 contact-us links on the homepage), not just real Book Now CTAs. Site-wide `book_now_link_click` totaled only 237 events in the trailing 30 days across all traffic, yet Ads credited PMax alone with 135 conversions mostly from this one event — one campaign claiming the majority of a site-wide click total that isn't even a real booking action.

3. **Orphaned dead Ads tag found, not fixed.** A separate, non-default workspace ("1") sits abandoned in this container (the Default Workspace everyone actually uses is **23**). Workspace "1" holds a dead "Google Ads Conversion Tracking" tag (`awct`) firing on *All Pages* with no click gate, pointed at conversion action `417432139` ("Lead"), which is REMOVED in Ads. Never published, not visible in the normal GTM UI view — low risk, but should be deleted for hygiene. **Not deleted** — attempted twice, both blocked by the Claude Code permission classifier on the `tags().delete()` call. Left for Edu to remove manually (GTM UI → workspace "1" → tag 3) or retry later.

4. **Duplicate GA4 config tags — downgraded, not fixed.** Two "Google tag" config tags (12 "GA4", 32 "GA4 - Configuration") both point at the same measurement ID `G-2KGSP7N92C`. Initially flagged as a likely page_view double-counting bug; downgraded after checking real GA4 data — `session_start`/`sessions` ratio is ~1:1, and GTM's "Google tag" type is designed to dedupe same-ID configs. Untidy config hygiene, not a confirmed live bug.

5. **Four `ghl_*` conversion actions in Ads are near-dead.** `ghl_installation`, `ghl_service_contract`, `ghl_book_now`, `ghl_schedule_service` are all `ENABLED` / `primary_for_goal: true`, but `ghl_installation` and `ghl_service_contract` had **zero** events in 90 days of GA4 data; `ghl_book_now` had 4, `ghl_schedule_service` had 5. Not fixed — deferred because `primary_for_goal` is a no-op on the conversion action itself (see `topserv-workspace` conversion-goals notes); the real bidding-goal control lives per-campaign in `campaign_conversion_goal`, which needs a read-first pass before any safe write.

**Fix shipped:**

- GTM account `6000633807`, container `30715121`, workspace **23** (Default Workspace — an earlier attempt targeted workspace "1" by mistake before Edu caught it; no write happened there).
- Enabled the "Click Classes" built-in variable (not previously enabled).
- Updated trigger 22 ("Link Click - Book Online") to add a second, ANDed filter: `{{Click Classes}}` matches regex `as-qlink|as-btn|elementor-button`, on top of the existing `{{Click URL}} contains "contact-us"` condition. Scoped from markup verified on the homepage: nav "Contact Us" = `class="nav-link"` (now excluded), real CTAs = `as-qlink` (header quicklinks: "Book Now / Request an Estimate", "Maintenance / Schedule a Tune-Up"), `as-btn-gold` (hero button), `elementor-button` (another CTA block) — all still included.
- Published as container **version 22**, name "Fix book_now_link_click over-triggering". Confirmed live via `versions().live()` read-back.
- **Caveat:** only verified CTA markup on the homepage + contact-us page. If another page (service pages, footer variants, mobile menu) uses a differently-classed Book Now button, it could stop firing there too — worth checking if `book_now_link_click` volume drops more than expected once real data comes in.

**Testing — inconclusive, flagged honestly rather than faked.** Tried to verify independently via headless Playwright, 4 different approaches (network request capture, `dataLayer.push` hooking, JS-level navigation blocking, network-level navigation blocking). All four gave inconsistent results, including the known-good case sometimes showing zero tracking activity at all — most likely NitroPack's deferred/lazy script loading interacting badly with synthetic clicks in headless Chromium, not a real signal about the fix itself. Did not report a pass/fail verdict from any of these runs. Real verification is still open.

**Open / next steps:**

- [ ] Verify the trigger fix against real behavior — either a manual click test in GTM Preview mode, or check real GA4 `book_now_link_click` volume/pattern in a few days.
- [ ] Delete orphaned dead tag in workspace "1" (blocked twice by permission classifier — manual deletion in GTM UI is the fastest path).
- [ ] Read per-campaign `campaign_conversion_goal` config before deciding whether/how to exclude the 4 near-dead `ghl_*` actions from bidding goals.
- [ ] Consider consolidating the two duplicate GA4 config tags (12, 32) — low priority, config hygiene only.
