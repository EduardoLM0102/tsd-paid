# Neon Monkey — Call / Lead Volume Drop Diagnosis (2026-07-28)

**Trigger:** Ticket reopened by Eve. Brock emailed: *"Over the last 2 weeks we have seen an extreme drop off in our call/lead volume. Are there any metrics we can look at to identify what might be going wrong?"*

This is a follow-on to the 2026-07-16 reply, where the early-month impressions drop was reported as budget-related and not concerning *unless the client reported a change in lead volume*. He now has.

**Accounts:** PPC `7953905280`, LSA `1219885876` (MCC `4155514468`). Data pulled via `google-ads-ratos` skill (`tsd.sh` → `.env.topserv`).

## Root cause

Budget reduction taken early July to bring the client in line with the media plan, which included **pausing PMax** (`TSD_04.25_PMAX_Evergreen`, now `PAUSED`, last day with data 2026-07-21). PMax was the account's main reach; removing it took call volume down with it. The live footprint now is the two Search campaigns (`Nonbranded_Trimming`, `Branded`) plus LSA.

## Numbers

**PPC June vs July MTD (27d), account `7953905280`:**

| | Impressions | Clicks | Cost | Tracked conv |
|---|---|---|---|---|
| June | 104,370 | ~3,900 | $9,513 | 96.0 |
| July MTD | 14,444 | ~610 | $3,937 | 58.1 |
| Δ | −86% | −84% | −59% | −40% (−33%/day) |

**Call conversions specifically (conversions-by-action query):**

| Conversion action | June | July MTD | Δ |
|---|---|---|---|
| Calls from ads (call-only) | 30 | 14 | −53% |
| "Phone Call" (type UPLOAD_CLICKS — offline import, source unconfirmed) | 29 | 8 | −72% |
| NMS-Website GA4 contact_us (primary) | 36 | 33 | −8% |
| **LSA calls/leads** (acct `1219885876`) | **23** | **30** | **+30%** |

**PMax collapse:** June imp 100,259 / 50 conv / $6,813 → July MTD imp 10,586 / 11 conv / $1,337, then paused ~Jul 21.

## Why the blended conv number looks softer than the call drop

Headline "conversions" only fell ~40% because it's propped up by soft GA4 web actions marked **primary** (contact_us page engagement barely moved, plus GA4 page_view / engagement events flagged primary). Those mask the real call drop. Same conversion-goal pollution pattern seen on Golden / Proud Pops / GC. Worth cleaning up separately so reported lead counts aren't inflated.

## Recommendation

Restore volume by reallocating budget from other sources or bumping it back to prior level, then re-enable PMax. Pair it with locking targeting to West Fort Worth (the still-open geo ticket) so recovered volume is clean, not Grand Prairie. Needs Brock's sign-off on budget + the target-location list requested on 2026-07-16 (still blocked).

## Caveats / unverified (do not assert as fact to client)

- "Phone Call" action labeled offline/CRM upload is an inference from `type=UPLOAD_CLICKS`; actual source not confirmed.
- LSA "calls" are LSA *conversions* (calls + messages lumped).
- LSA assumed untouched because spend/leads rose; change history not pulled.
- Whether Andrea's budget cut + PMax pause were client-approved (written approval via AM ticket per playbook) not confirmed — verify internally.

## Delivered

Short ticket reply drafted for Eve (per [[tsd-client-message-style]]): diagnosis + call numbers + fix + ask (Brock's budget go + location list). No self-underselling, no right/wrong framing.
