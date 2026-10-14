# Lead funnels: Command Center (funnels/<slug>)

Builder: `funnel_build.py` (read-only Google Ads + CallRail) with per-client config in `clients.json`. Refresh = `./tsd.sh funnel_build.py --client <slug>`
(or `--all`), then ArtifactData set funnels/<slug> with the JSON; or the page's "Refresh now" button (Claude desktop app, local MCP tool tsd_funnel).
Click-ID → campaign matches are cached per client in `<slug>/gclid_campaigns.json`.

## 2026-10-10: funnels for all 11 clients whose CallRail we can read
Cool Hand moved onto the shared builder (old `clients/cool-hand-electric/funnel_build.py` is superseded).
Tracking gaps found while building (nothing changed in any account; for Edu to decide):

| Client | Taps on the number | Website calls from ad clicks (CallRail) | Ad call button → CallRail |
|---|---|---|---|
| Watt's Right | GA4 phone_link_click recorded 0 in 60 days → not firing | Working (38 in 30d) | Yes |
| Spencer Air | GA4 phone click shows 0 (low traffic, likely not firing) | Working (20) | Yes |
| Napps | Click to call working (12) | No CallRail website numbers at all | Yes |
| Integrate Comfort | GA4 phone_link_click 0 → not firing | ~0 tied to ads (37 non-ad); CallRail→Ads link DISABLED (fu-031) | Yes |
| C&S Air | Working (69) | 0 tied to ads (23 non-ad) | Yes, but CallRail answered 1 vs 8 placed. Check |
| All Seasons | Working (72) | 0 tied to ads (5 non-ad); pool sources show "None" | Yes (60 answered) |
| Neon Monkey | Not firing (site Google tag dead since ~08-30) | 0 tied to ads | Yes |
| Lilypad | Working (26) | Working (2) | Can't match: call button number not found in the account |
| Kings Window | Working (20) | Working (55) | Yes |
| Hawkins | No tap action exists | Low (2+1) | Yes |
| Cool Hand | Working | Pool live since 10-10 | Yes since 10-10 |

**Taps root cause (10-10):** Watt's Right, ICS, Neon Monkey, Spencer and Hawkins GTMs all have a tel: trigger that sends GA4 `phone_click` (+ Meta),
but no Google Ads tag. Google Ads imports GA4 `phone_link_click`, an event the sites never send (Neon Monkey GA4, 90d: phone_click 35, phone_link_click 0).
Hawkins imports no phone event. Fix = a "[TSD] Click to call" Google Ads conversion on the existing tel: trigger (GTM ids below). Edu creates the actions.
