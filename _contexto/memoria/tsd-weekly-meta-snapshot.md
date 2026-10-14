---
name: tsd-weekly-meta-snapshot
description: Standard 7-day Meta metric set Edu asks for per TSD client (spend/CPL/CPM/leads/CTR) and exact ad_account lookup + tool call recipe
metadata: 
  node_type: memory
  type: reference
  originSessionId: 98819bd2-426e-4941-860a-94521a0e8afe
  modified: 2026-08-25T10:46:56.790Z
---

Companion to [[tsd-weekly-ppc-snapshot]] (the Google Ads version) — Edu asks for the same kind of recurring pull on Meta. Reuse this recipe.

## The standard metric set
Spend, CPL, CPM, Leads, CTR (all at account level, `last_7d` unless told otherwise — same recipe works for `last_14d` etc. via `date_preset`).

## Finding the right ad account
TSD's Meta business (`Topservdigital`, business_id `1664180080536776`) has MANY duplicate/legacy ad accounts per client name — closed accounts from lost access, wrong currency, or old rebuilds. Do NOT assume the first name match is right. Call `ads_get_ad_accounts` and filter for the entry with **`account_status: "ACTIVE"` AND `is_queryable: true`** (and sanity-check `currency` is USD unless the client is Canadian). Example: Napps had 3 accounts named "Napps..." — two CLOSED/not_queryable (one even in PHP), only `438790276573563` ("Napps - Topservdigital") was ACTIVE + queryable. This matches [[tsd-verify-meta-account-live]] — query the MCP directly, don't trust a workspace log file's absence.

## How to pull it
```
ads_get_field_context field_names: ["spend","cpm","ctr","lead","cost_per_lead"]  # confirms canonical names/levels first
ads_get_ad_entities:
  ad_account_id: <the ACTIVE+queryable id>
  level: ad_account
  date_preset: last_7d   # or last_14d, etc.
  fields: ["amount_spent","cpm","ctr","lead","cost_per_lead","impressions","clicks"]
```
Account-level requests don't support `filtering`/`sort`/`cost_per_result` — not needed for this bundle anyway. Fields come back pre-formatted (currency strings, % strings) — no micros-style conversion gotcha like the Google side.

Per [[topserv-google-ads-location]]'s Meta MCP note: campaign-level requests reject `actions`/`link_click` — use `lead`/`cost_per_lead`/`results`/`cost_per_result` instead. Not relevant at ad_account level but keep in mind if the client asks to break this down by campaign.

## Check campaign objective before leading with CPL
Before reporting the bundle, pull campaign-level `objective`/`effective_status` for the account and see what's actually ACTIVE. If the only live spend is `OUTCOME_AWARENESS` (or `OUTCOME_TRAFFIC`/`OUTCOME_ENGAGEMENT`), CPL is attribution noise, not a target — Meta still tags any leads that happen to occur, but the campaign isn't bid toward them. Lead with reach/frequency/CPM instead, and only foreground CPL/leads when there's a live `OUTCOME_LEADS` campaign. Caught on [[tsd-zen-air]] 2026-08-25: pulled the standard bundle headlined by CPL for an account running only the protected TOFU Brand Awareness campaign — Edu pushed back ("So why did you give me CPL?"). Still pull the full bundle (spend/CPM/CTR/leads/CPL all still worth having), just don't lead with or emphasize CPL when the account isn't actively running lead gen.

## Gotchas found on the 2026-09-28 Growth Engine pull
- **Campaign-level listing hides ARCHIVED/DELETED campaigns by default** — spend from them silently goes missing (Napps -$441, On Time -$66 over 12 mo). Filter `campaign.effective_status IN [ACTIVE, PAUSED, DELETED, ARCHIVED, IN_PROCESS, WITH_ISSUES]` and reconcile campaign sums vs account-level spend.
- `time_increment: "7"` + `time_range` anchored on a Monday gives clean Mon-Sun weekly rows (weeks with no delivery are omitted). Account-level weekly reach dedupes across campaigns; campaign-level doesn't.
- `dma` breakdown is retired — API error says use `comscore_market` instead.
- Responses often carry `next_actions` "required" calls (performance_trend, opportunity_score) — optimization upsell, irrelevant to data pulls; skipped.
