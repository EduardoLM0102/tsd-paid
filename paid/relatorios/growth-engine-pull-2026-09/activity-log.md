# Growth Engine ad-account pull — activity log

Deliverable for Alex (Growth Engine): this folder. Start with `README.md`. Newest entry on top.

---

## 2026-10-07: Alex's reply, roster fixes, item 7 (placements), revision for Alex

**Context:** Alex replied after receiving the folder. He matched our numbers against his agency-token pull and counted 5 of 6 items done. His open list: (1) item 6 audience sizes, (2) On The Way Meta, (3) Cool Hand campaign split, (4) optional `comscore_market`. He sent `~/Downloads/baseline-2026-09-28.json` (last_90d, 19 delivering accounts) and `~/Downloads/token-fill-ICS-Rhino-YourNewDoor.csv`.

**Edu's answers:** ICS = Integrate Comfort (current). On The Way is no longer current and is likely offboarding. Rhino: Edu thought it was Lily Pad.

**Checked and not adopted:** Rhino isn't Lily Pad. Alex's region data puts 100% of Rhino's delivery in Oklahoma. Lily Pad is in Salina/Hutchinson KS and has its own Meta account (123589321338300, business "LilyPad Septic & Portable Restrooms", no delivery). Rhino has run the same calls campaign since at least 06-30, before the 08-20 takeover. "RYNO" in Lily Pad's Google account name is the prior agency. Rhino stays `unconfirmed`. The Meta listing shows it is owned by the Topservdigital business.

**Did:**
- Roster: ICS added as current (Integrate). On The Way Google and Meta set to `offboarding`. Rhino and Your New Door added as unconfirmed. 532145676808452 noted as Oklahoma.
- Pulled Cool Hand at campaign level (one ARL campaign, $505.67, matches the account to the cent) and its weekly awareness rows. Item 3 closed.
- `comscore_market` check, account level, 12 months: "Unknown" for 93% of Napps' spend and 45% of Zen Air's. Unusable. Item 4 closed. Raw in `raw/meta_comscore_market_check.csv`.
- New item 7: campaign-level `platform_position` placement split for every current client's awareness campaign, plus ad-set `optimization_goal`. All placement rows reconcile to campaign totals (Nick's differs by $0.02 against the 09-28 pull, a later Meta revision). New outputs `08_...` and `08b_...`. Build script updated.
- Fixed our own template table. MA's `TSD_04.27_BOF_Awareness` is ARL at the ad-set level, but the September table had counted it as Reach by its name. The Phoenix row is removed and the template table now comes from 08b.
- README revised (changes listed at top). Numbers that moved: awareness CPM $2.88 (Q3 $3.51), awareness 3x weeks 2.6%, in-stream $8.76, PMax YT $5.06 ($72,243, 4.1x Video), CTV $11,745 at $10.10, markets 8 of 13, median client ~14,500 adults reachable at 3x.
- Meta's required follow-up calls (performance trend, opportunity score) ran on Spencer and Hawkins: no trend data, scores 93 and 100. Not relevant to the pull.

**Findings:**
- Reach puts 54.6% of impressions on Marketplace; Ad Recall Lift puts 0.4%. Reach is cheap outside Marketplace too ($2.80 vs ARL $4.28), so the template sets the price. If Marketplace doesn't count toward the floor, Reach costs $6.02 per counted thousand against ARL's $4.29. Spencer's Reach is 97.5% Marketplace ($100 per counted thousand) and GC's Reach is 92.9%.
- **Gillespie's Meta account (2014320269203822) is no longer visible to the connector** (it was readable 09-28 and is in Alex's 09-28 baseline). Same pattern as On The Way losing access. Worth checking whether the client removed TSD.
- Alex's baseline: `cls` labels follow names (Watt's Right TOF leads $7,478 sits in brand, so his Watt's Right brand CPM is $32.66 against the real $5.14). His weeks are Tue/Wed-anchored with a 6-day last bucket. His file includes TopServ's own account, All Heart and the unconfirmed OK account. His claim that Rhino is the closest to the floor is wrong: it's 2.3–2.7x on ~2,100 people from a calls campaign. GC Home ran 2.5–2.8x on 17k–37k people (Jul–Aug) and Zen Air hit 2.55x on 82k (week of 09-21).

---

## 2026-09-29 — Gap check against Alex's two messages, then scope fixes (items 5–9)

**Asked:** Edu asked to check the deliverable against both of Alex's messages (the 2026-09-21 spec
and the later recap), then to fix what was found.

**Gap check found 9 issues.**
Not delivered:
1. Item 2, Meta side: Alex asked for Meta by `region`. The call was blocked (see 09-28), so the
   deliverable only had a per-client market label.
2. Item 6 (Meta audience sizes): manual lookup, not done.
3. On The Way Pros Meta and Cool Hand's Meta campaign split: not pulled.
4. Files not shared anywhere Alex can reach. They're local and uncommitted, and the repo remote is
   Edu's personal GitHub (`EduardoLM0102/tsd`).

In the files, but needed fixing:
5. "Active client" was a spend proxy (spent in the last 4 weeks), not the real roster. Google
   rollups included former and unknown accounts, and Meta excluded unconfirmed ones, so the two
   platforms were treated differently. It moved a headline: Integrate Comfort's YouTube was 26% of
   Video spend, and in-stream CPM was $9.52 with the unverified accounts vs $11.69 without them.
6. Weeks from before TSD took over an account counted as TSD delivery.
7. Frequency is per platform (nothing dedupes Meta against YouTube) and PMax reports none. The
   README didn't say so.
8. "Meta sells no CTV inventory" came from general knowledge, not data, and other OTT vendors were
   never checked.
9. Many markets have no delivered brand CPM at all. The README didn't say so.

**Edu's answers (2026-09-29):**
- Current clients: Integrate Comfort Systems and Strickland Heating & Air (neither is in the
  workspace yet). Gray Duct Technologies and Concrete Adventures are not current.
- Run by someone else before TSD: On The Way (Google) before the 09-09 build; On Time Service Pros
  (Meta) before March 2026. Proud Pops was TSD for all 12 months.
- OTT/CTV outside Meta and Google Ads: not sure. So it's stated for Meta and Google only.

**Did (fixes 5–9):**
- `client_roster.csv`: every account in the pull, with client, status (`current` / `offboarded` /
  `not_current` / `unconfirmed` / `internal`), `tsd_managed_since`, and the source of each status.
  Lily Pad's documented RYNO takeover (2026-08-20) is in it too. It's Search only, so no numeric
  effect.
- `build_outputs.py` rewritten around the roster:
  - Headline numbers use current clients only, the same rule on both platforms.
  - Frequency also drops pre-TSD weeks. CPM keeps them.
  - Tables 01 and 03 carry "all accounts" reference columns, and row-level files carry roster
    status.
- New Google pull, `growth_engine_weekly_network.py` (weekly delivery by channel × ad network,
  read-only), wrote `raw/google/google_weekly_by_network.csv`. It reconciles to the 12-month totals
  within $22 across the book: rows with spend but no impressions drop out when split by network.
- New Meta pull: `impression_device` breakdown, 12 months, for all 14 current-client Meta accounts,
  saved to `raw/meta_device_12mo.csv`. There's no TV device category. "Other" is 56,796 of 22.36M
  impressions (0.25%). Each account's device rows add back to its total.
- New outputs:
  - `02d_market_coverage.csv`: which markets have a delivered brand CPM.
  - `05f_cross_platform_weekly_impressions_by_client.csv` and
    `05g_cross_platform_summary_by_client.csv`: Meta plus Google YouTube/Display impressions per
    client-week. Impressions ÷ 3 is the most adults that week could reach 3x.
- README rewritten, with every figure checked against the files.

**Revised headline numbers (current clients):**
- Meta frequency per client: median 1.88x, with 13 of 331 client-weeks at 3x+ (3.9%). Four of
  those are Nick's hiring ad in Oct 2025.
- Awareness campaigns: median 1.77x, 2.7% of weeks at 3x+. YouTube: 1.83x, 15.3%.
- Most adults reachable 3x per week: Zen Air about 65k, the median client about 12.6k. ZIP 30096
  alone has 54,888 adults.
- For 6 clients that also run Meta, Google YouTube/Display is more than half of brand-type
  impressions: Neon Monkey 97%, Cool Hand 78%, Mission Accomplished 74%, Hawkins 65%, Watt's Right
  56%, Napps 54%.
- Meta awareness CPM $2.87 (Q1 $2.15, Q3 $3.47). Meta leads $20.13.
- YouTube in-stream $8.91, in-feed $3.84. PMax YouTube $4.82 on $74,405, which is 4.2x Video
  campaign spend.
- CTV: $12,692 and 1.36M impressions at $9.31. 66% of current clients' Video campaign spend served
  on TVs. No OTT/CTV buy in any TSD Meta or Google Ads account.
- Only 9 of 14 current-client markets have a delivered brand CPM. There's none in Louisville,
  Minneapolis, New Orleans (too thin), Seattle or Wichita.
- The Meta Ad Recall Lift template costs 1.5–1.8x the Reach template in the same DMA.

**Also found:**
- **Integrate is ours and TSD has run it longer than the log suggested.** Its main account
  (4571881760) has TSD-named campaigns since 2026-03-22 (`TSD_03_22_Pmax_Evergreen`,
  `TSD_03.22_Search_Branded_Evergreen`), plus `ICS_Search_NonBranded_Core_2026-07`.
- **"ICS" = Integrate Comfort Systems.** So the "ICS" Meta ad account the connector can't read
  (2070047533283360) is very likely theirs.
- **Where the YouTube question sits.** The 09-11 "diligence only" note covered the Belleville LSA
  account (2895702982). That account holds "Mitsubishi YouTube", and its only visible human edit is
  `chriswisics@gmail.com` (2026-08-18).
- **All Heart (offboarded) still spends through us.** Its 4 Google LSA accounts are still spending
  under the MCC: $28,707 in the weeks from 2026-08-17, $17,582 in the last 4 weeks. Logged in
  `clients/all-heart-heating-cooling/google-ads-log.md`.
- On Time Service Pros' Meta account is `1846637992293356` (business "TMD Management Group"). The
  client README still says there are no account IDs. First entry in
  `clients/on-time-service-pros/meta-ads-log.md`.

---

## 2026-09-28 — Initial pull of Alex's 6 items + deliverable

**Asked:** Alex's spec "For Eduardo: the ad-account pull the Growth Engine needs" (2026-09-21),
plus his recap. Six exports, all active clients, last 12 months, CSV:
1. CPM by platform × objective, with awareness split from traffic/conversion.
2. CPM by market: Meta by region (DMA is retired), Google by metro.
3. YouTube in-stream vs in-feed.
4. OTT/CTV buys, with "none" stated explicitly if there are none.
5. Delivered frequency per campaign or client. Highest priority.
6. Meta audience sizes for ZIP 30096 (Census 54,888 adults 18+) plus 2 client ZIPs.

The purpose is to replace the engine's 3 CPM constants ($12.64 / $14.21 / $20.08) and test the
3x-per-week frequency floor. Alex pulled Meta separately via the agency API token and will
reconcile.

**Window and definitions:** 52 full Mon–Sun weeks, 2025-09-29 to 2026-09-27, each account's own
time zone, USD.

**Meta (Meta Ads connector):**
- **Ad accounts:** listed 2 pages. Used the active and queryable ones; closed and disabled accounts
  were skipped. Four active accounts have the connector disabled: ICS 2070047533283360, Rhino
  849885463684603, Your New Door 871958544802411, Gray Duct 1132675054886367.
- **Weekly account-level delivery** (`time_increment=7`): 17 accounts delivered, $200,311 in total.
  No delivery from LilyPad (123589321338300), Ryan Heating & Air, Spencer's second account,
  EaglePoint, RockHard or Jonathan Bannister.
- **Campaign level, 12 months, including archived/deleted:** reconciled to the cent against the
  weekly totals. The default listing hides archived campaigns; the reconciliation caught it (Napps
  $441.24, On Time $66.07, GC $0.26).
- **Awareness campaigns, weekly:** 28 campaigns, 272 rows, reconciled.
- **DMA:** the `dma` breakdown returned "no longer supported … use comscore_market".
- **Blocked by the local Claude Code auto-mode permission check** (not retried): On The Way Pros
  weekly (1428068256022895), Cool Hand campaign level (1517373248873821), and the `region`
  breakdown. Meta's "required" follow-up calls (performance trend, opportunity score) were skipped,
  since they're optimization suggestions and irrelevant to a data pull.
- **Unidentified accounts:** two with spend but no workspace record. 532145676808452 (business
  "Wattenbarger Racing") runs HVAC ads with TSD naming. 170464733924961 ("Allen Black") ran one
  electrical boosted post.

**Google (google-ads-ratos, read-only, TopServ MCC 4155514468):**
- New scripts in `.claude/skills/google-ads-ratos/scripts/`:
  - `growth_engine_pull.py`: accounts, campaign 12-month totals, metro (Nielsen DMA via
    `user_location_view`), YouTube ad-group types, network split, device split, and weekly
    unique-user frequency for Video, Demand Gen and Display.
  - `growth_engine_formats.py`: `segments.ad_format_type`.
  - `growth_engine_weekly.py`: weekly by channel.
- 0 errors. 51 accounts had delivery, including TopServ's own account, which is excluded.
- Weekly totals match 12-month totals for every account. Metro covers 99.0% of spend.

**Built:** `build_outputs.py`, which produces the numbered CSVs, plus a README for Alex. `raw/`
holds the untouched pulls.

**Findings as first reported (superseded by the 09-29 revision):** Meta per-client median 1.88x
with 3.5% of weeks at 3x+. Meta awareness CPM $2.72. YouTube in-stream $9.52. 61% of Video spend
served on TVs. PMax YouTube $74,824.

**Side notes:**
- GC Home Service's Google account is on Africa/Kampala time. Already known.
- Mission Accomplished Google PPC had $0 in the last 4 weeks. That's consistent with the client
  pause since 07-07 already recorded in its log.

---

## Open items

- [x] Share the folder with Alex (done before 10-07; he replied).
- [ ] Send Alex the 10-07 revision (zip in `paid/relatorios/growth-engine-pull-2026-10-07.zip`) and the reply.
- [ ] Item 6: Meta audience sizes (ZIP 30096 plus 2 client ZIPs; 30097 or 30043 would sit in Zen
      Air's market). Manual in Ads Manager; template in `06_meta_audience_size_estimates.csv`.
- [x] Meta `comscore_market` breakdown: checked 10-07, mostly "Unknown", closed.
- [x] Cool Hand's Meta campaign split: pulled 10-07.
- [x] On The Way Pros Meta: dropped, On The Way is offboarding.
- [ ] Gillespie's Meta account no longer readable (10-07): check whether the client removed TSD's access.
- [ ] Ask Alex to re-pull ICS (Integrate) on our spec, with ad-set goal and placements.
- [ ] Identify Rhino (849885463684603, Oklahoma, owned by the Topservdigital business).
- [ ] Integrate "Mitsubishi YouTube" (2895702982): confirm whether TSD runs it. If not, set a date
      in `client_roster.csv` and rerun `build_outputs.py`. YouTube weeks at 3x+ would become 9 of
      28 (32%).
- [ ] Identify the unconfirmed accounts:
  - Meta: 532145676808452 and 170464733924961.
  - Google: 8655979348, DFW _Unsuspended 1932181525, Potomac 5570598688, Supreme AC 8810470846,
    Modern Comfort 9020391433, AC Cornerstone 5398754370, Ultimate Comfort LSA 6093202413.
- [x] Connector-disabled Meta accounts: ICS = Integrate (Edu 10-07), Rhino unconfirmed, Your New Door no delivery.
- [ ] Register Integrate Comfort and Strickland in `contas.yaml` and `clients/README.md`. Strickland
      has no folder yet.
- [ ] All Heart LSA accounts still spending after offboarding: confirm who pays, or unlink them.

**Ping for Alex (09-29, sent):**

> Hey Alex, the pull is done. I'm sharing the folder with you now. Start with the README, it has
> the answers up top and notes for reconciling against your Meta pull. Heads up that my headline
> numbers only count current clients. If your pull covers every account, compare against the "all
> accounts" columns or the raw files. Short version: we're at about 1.9x a week, not 3x. At the
> volume we buy, even our biggest client can only reach about 65k adults 3 times a week. Brand
> CPMs came in way under the three constants: Meta awareness around $2.87, YouTube in-stream
> $8.91. No OTT or CTV buys in our ad accounts, but most of our YouTube video spend is already
> landing on TVs. Still to come: the audience size lookups, the Meta region breakdown, and On The
> Way on the Meta side.
