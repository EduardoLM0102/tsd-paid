# Client Logs

One folder per client. Each client has two running logs — one per paid platform:

```
clients/
  <client-slug>/
    google-ads-log.md   # paid-search work
    meta-ads-log.md     # paid-social work
```

**Convention:**
- Newest entry on top, dated `YYYY-MM-DD`.
- One entry per work session: **what we researched → what we found → what we did → open items**.
- Include account/campaign IDs so the entry is reproducible.
- English (TopServ deliverables are in English).

**Clients:**
- `all-heart-heating-cooling/` — All Heart Heating & Cooling -PPC (Google Customer ID `9205826499`)
- `on-the-way/` — On The Way AC Plumbing & Electrical, Santa Fe TX (Google Customer ID `3454686129`). Registered 2026-09-09. Account pre-existed with live LSA/PMax/Demand Gen + legacy paused campaigns; TSD's own build is Phase 1 (Branded + 3 non-branded ad groups: AC-Repair, Plumbing-Emergency, Electrical), PAUSED, remaining services staged for Phase 2. See its `README.md` and `google-ads-log.md`.
- `mission-accomplished/` — Mission Accomplished (Google Customer ID `8634274092`; LSA `4904262993`)
- `hawkins-siding/` — Hawkins Siding and Exterior (Google Customer ID `2198608170`)
- `zen-air/` — Zen Air Heating and Cooling (Google Customer ID `4360840956`; LSA `3740502923`)
- `kings-window/` — King's Window Services, glass/window repair (Google Customer ID `6769493219`, PPC+LSA combined in one account). **Not yet in `contas.yaml`** — found via `customer_client` under the MCC.
- `nicks-heating/` — Nick's Heating and Air Conditioning, Hammond LA (Google Customer ID `1854100356`, PPC+LSA in one account). Registered 2026-10-08 after a book audit found it active but never checked. Only a `google-ads-log.md` so far.

**Prospects / not in the book:**
- `lilypad-septic/` — Lilypad Septic Company (Salina & Hutchinson, KS; owner Cole Leister). **No account IDs yet** — not in `contas.yaml`, no Google/LSA/Meta accounts, tracking is a blank slate. Folder holds the Q4 2026 quarterly media plan (client PDF + md source + build script) and `internal-notes.md`. See its `README.md`. **The client PDF deliberately excludes the operational guidelines — read `internal-notes.md` for the pre-launch gates.** When they become real: add to `contas.yaml`, move up to the Clients list, start the two logs.
- `on-time-service-pros/` — On Time Service Pros (Rosemount, MN — plumbing/HVAC/electrical). **No account IDs yet** — no Google/LSA/Meta CID on file in AT as of 2026-08-10. Folder holds the Stage 4 Meta campaign brief for the September HVAC promotion ($49 Tune-Up + 30% Off Install), first paid work for this client. See its `README.md`. When they become real: add to `contas.yaml` / Meta equivalent, move up to the Clients list, start the two logs.
- `integrate-comfort-systems/` — Integrate Comfort Systems - LSA Belleville (Google Customer ID `2895702982`). **Diligence only so far, not in `contas.yaml`** — CID given directly by Edu, confirmed reachable under the Topservdigital MCC. 2026-09-11: read-only history check (account structure, change_event/change_status, LSA lead volume, origin of the $10/week LOCAL_SERVICES budget — unresolved, not visible in Ads change history). No changes made. See its `google-ads-log.md`.
- `carey-walsh/` — Carey & Walsh Inc., HVAC, Briarcliff Manor NY (Westchester County). **No account IDs yet**: no Google Ads, LSA or Meta account found anywhere TSD can see (checked 2026-10-05). TSD's GTM already holds their container (account `6000900042`, `GTM-M5DW5ZN`) with an unpublished tag build in workspace 6. Folder holds the Nov 2026–Jan 2027 media plan (client PDF + md source + build script), `internal-notes.md` (pre-launch gates, open questions, research) and `gtm-log.md`. When accounts exist: add to `contas.yaml`, move up to the Clients list, start the platform logs.
