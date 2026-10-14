# Neon Monkey — PPC & LSA Geographic Targeting Review

**Date:** 2026-07-20
**Trigger:** Brock's 2026-07-16 meeting — wants to concentrate marketing on **West Fort Worth** (where he has traction) and stop chasing leads across the broader Metroplex. Specifically flagged **LSA leads from Grand Prairie** and other places he doesn't want to drive to.
**Accounts:** PPC `7953905280` · LSA `1219885876` (both under Topservdigital MCC `4155514468`). Business = tree service (trimming/pruning, removal, stump, plant health, holiday lighting, leaf cleanup).
**Window analyzed:** trailing 90 days, 2026-04-21 → 2026-07-19.

---

## 1. What is live today

### PPC account `7953905280`
| Campaign | Type | Budget | Geo method | Positive geo setting |
|---|---|---|---|---|
| TSD_04.25_PMAX_Evergreen | Performance Max | $60/day | 5 proximity radius circles | **Presence OR Interest** |
| TSD_04.09_Search_Branded_Evergreen_Mix | Search | $70/day | 5 city targets | Presence |
| TSD_08.05_Leads_Search_Nonbranded_Trimming | Search | $75/day | 1 city target (Fort Worth) | Presence |

(14 other Search/Smart campaigns exist but are PAUSED.)

### LSA account `1219885876`
| Campaign | Budget | Geo method |
|---|---|---|
| LocalServicesCampaign (system-generated) `19644340204` | $214/day | 19 location targets (mix of cities, ZIPs, and **whole counties**) |

---

## 2. Current geo targeting — exact findings

### PMax (`21225221220`) — 5 radius circles
| Radius | Center (approx area) | West-FW aligned? |
|---|---|---|
| 17 mi | ~Benbrook / SW Fort Worth (32.673, -97.461) | ✅ Yes — this is the West/SW core |
| 5 mi | ~Keller / North Fort Worth (32.934, -97.229) | ◑ North, borderline |
| 20 mi | ~Kennedale / SE Fort Worth (32.682, -97.247) | ❌ 20 mi reaches **east into Grand Prairie, Duncanville, Dallas County** |
| 5 mi | ~Grapevine / Southlake / DFW Airport (32.934, -97.078) | ❌ Far **NE** Metroplex, opposite side from West FW |
| 5 mi | ~Joshua / Cleburne (32.462, -97.388) | ❌ South (Johnson County) |

Plus the campaign is set to **Presence OR Interest** — it also serves to people merely *searching about* those areas from anywhere, not just people physically there. This is the single biggest "spillover" lever in PPC.

### Search Branded (`23739724064`) — 5 whole cities
Arlington · Fort Worth · **Grand Prairie** · Mansfield · Weatherford
→ Includes Grand Prairie (Brock's complaint) and Arlington/Mansfield (east/SE Tarrant).

### Search Nonbranded Trimming (`23825900343`) — 1 city
**Fort Worth only.** Already tight; this is the model for what "concentrated" looks like.

### LSA (`19644340204`) — 19 targets
- **Whole counties:** **Tarrant County**, **Johnson County** ← county-level blanket defeats any "West FW" focus. Tarrant County includes Arlington, Euless, Bedford, Hurst, Grand Prairie's Tarrant slice, Mansfield.
- **City: Grand Prairie** ← the exact place Brock named.
- **ZIP 75249** ← far SW Dallas / Grand Prairie edge (Dallas County).
- Far-north Denton County suburbs: Flower Mound, Roanoke, Trophy Club, Westlake (NE, not west).
- Genuinely West/SW (keep): Aledo, Weatherford, Granbury, Willow Park, Hudson Oaks, Crowley, ZIP 76035 (Cresson).
- South (Johnson Co.): Burleson, Joshua, ZIP 76028, 76058.
- **No negative locations anywhere** in PPC or LSA.

---

## 3. Where leads actually come from (90 days)

### PPC — $18,805 spend, 173 conversions
Top conversion sources by **physical presence**:
- **Fort Worth: 59 conv / $5,551** — the core, healthy.
- Benbrook 8, Saginaw 7, Lakeside 6, Westworth Village 3 — all **West/NW FW**, cheap, efficient. ✅
- Arlington 5, Richland Hills 5, Keller 3, Euless 3, Irving 2, Dallas 2, Duncanville 2, Grapevine 10*, Coppell 2, Grand Prairie 1 — **east/NE/Dallas-side**, further from West FW.
- *Grapevine's 10 came in as **Area of Interest** (people not physically there) — i.e. pure PMax interest spillover.
- **Grand Prairie (presence): 11,908 impressions, 472 clicks, $379, only 1 conversion** — high spend, near-zero return, and unwanted.
- Irving (presence): 10,449 impr, 390 clicks, 2 conv — same pattern.

### Cost-per-lead by campaign
| Campaign | Spend | Conv | CPL |
|---|---|---|---|
| PMax | $11,193 | 81 | **$138** |
| Search Nonbranded Trimming | $4,969 | 70 | $71 |
| Search Branded | $1,212 | 19 | $64 |

PMax burns **64% of PPC budget at ~2× the CPL** of Search, and it's the campaign with the widest, least West-FW-aligned footprint (20 mi SE circle + NE Grapevine circle + interest targeting).

### LSA — $5,413 spend, ~99 leads, ~$55/lead
- Lead quality: 20 BOOKED · 34 DECLINED · 40 ACTIVE · 5 NEW.
- Phone-area-code proxy for geo: **817/682/940 (Tarrant/FW) = 49 leads**; **214/469/972 (Dallas) = 14 leads**; plus a long tail of clearly out-of-state area codes (207 Maine ×5, 512 Austin ×3, AZ/CA/etc.) that read as spam/robocall — normal LSA noise, dispute those.
- The 14 Dallas-side leads + explicit Grand Prairie/Tarrant-County targeting = direct confirmation of Brock's complaint.

---

## 4. Opportunities to concentrate on West Fort Worth

**PPC**
1. **PMax is priority #1.** Switch positive geo from *Presence OR Interest* → **Presence only** (kills the "interest" spillover, e.g. the Grapevine-interest leads). Then rebuild the radius circles around West FW only: keep the 17 mi SW/Benbrook circle, drop or shrink the 20 mi SE circle (it's what reaches Grand Prairie/Dallas) and the NE Grapevine circle.
2. **Search Branded:** remove Grand Prairie (and likely Arlington/Mansfield) from the 5-city list; keep Fort Worth + Weatherford, add West/SW cities Brock confirms.
3. **Search Nonbranded Trimming** is already Fort Worth-only — leave as the template; optionally add confirmed West/SW cities.
4. **Add negative locations** (Grand Prairie, Dallas, Irving, and any east-Tarrant cities Brock excludes) across all three campaigns as a backstop — there are none today.

**LSA**
5. **Remove county-level blankets** (Tarrant County, Johnson County) and **remove Grand Prairie + ZIP 75249**. Replace with an explicit West-FW city/ZIP list. County targeting is the root cause of the east-side LSA leads.
6. LSA service area must stay **inside Neon Monkey's Google-verified service area** — trimming is fine, but adding new far-west ZIPs may require they sit within the verified area.

---

## 5. Effect on lead volume & performance (honest read)

- **Fort Worth core is ~⅓+ of all PPC conversions and most of the efficient volume** — concentrating there protects the majority of current results.
- Tightening geo will **reduce total lead count** (fewer east/NE/Dallas leads) but should **improve CPL and lead relevance**, because the trimmed areas are the low-conversion, high-spend ones (Grand Prairie 472 clicks→1 conv; Irving 390→2). We're cutting mostly waste, not winners.
- **Risk:** PMax is a black box — shrinking its geo and forcing Presence-only will lower its volume and Google may raise CPL short-term while it re-optimizes. Recommend staging the change and watching 2–3 weeks before further cuts.
- **LSA:** removing the two counties will cut lead *quantity* noticeably but should raise the share of jobs Brock will actually drive to. LSA is pay-per-lead, so unwanted-area leads are also **disputable** for refund regardless of targeting.

---

## 6. LSA visibility / ranking in the priority market

Concentrating budget geographically is itself a ranking lever — LSA ranks partly on responsiveness and review signals *within the served area*. To lift West-FW ranking:
- **Tighten the service area to West FW** so budget/impressions concentrate there instead of being spread thin across two counties.
- **Response speed & booking rate:** 34 declined vs 20 booked — declines and slow responses hurt Ranking. Improve answer rate on 817/682 calls.
- **Reviews:** steady flow of Google reviews from West-FW customers (LSA uses review count/recency/rating).
- **Dispute out-of-area & spam leads** promptly (the out-of-state area codes) — keeps the account's lead-quality signal clean and recovers spend.
- **Verify business hours & service list** are complete and accurate in the LSA profile.

---

## 7. What we need from Brock before we change anything

He's being asked separately for a target-location list. To implement cleanly, we need it at this precision:

1. **Confirmed "yes" list — the West Fort Worth footprint he wants**, as **specific cities AND/OR ZIP codes** (ZIPs are best for LSA). e.g. Fort Worth (which parts?), Benbrook, White Settlement, Westworth Village, Aledo, Weatherford, Willow Park, Azle, Lake Worth, Saginaw — he confirms which.
2. **A hard "no" list** — cities/areas to exclude even if nearby. He already named **Grand Prairie**; need the rest (Arlington? Mansfield? Irving? Dallas? east Tarrant generally?).
3. **How far west/how far will he drive** — a **max radius or drive-time from his base/shop address**, so we can size the PMax circles and LSA area. Need his **shop/base address or anchor ZIP**.
4. **Any must-keep pockets** outside a clean West-FW boundary (existing good customers, referral zones) so we don't cut a pocket that works.
5. **County call:** does he want us to drop **whole-county** targeting entirely (Tarrant/Johnson) in favor of a city/ZIP list? (Recommended — yes.)
6. **LSA verified service area:** confirm what geography his LSA profile is Google-verified for, so we know the westward limit we're allowed to add without re-verification.

Once we have #1–#3 at minimum (yes-list, no-list, and anchor/radius), the PPC and LSA changes above can be built and staged.

---

## Open items / next actions
- [ ] Send Brock the 6 questions above (route via AM ticket).
- [ ] On receipt: rebuild PMax geo (Presence-only + West-FW circles), trim Search Branded cities, add negatives, rewrite LSA service area (drop counties + Grand Prairie + 75249).
- [ ] Dispute out-of-area/spam LSA leads for the trailing period.
- [ ] Add before/after geo + CPL to the client log after changes go live.
