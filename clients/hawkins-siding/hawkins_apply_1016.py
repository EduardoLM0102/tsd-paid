# APPLIED LIVE 2026-10-16 on Edu's go ("Go ahead and apply all fixes"). Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Hawkins Siding (2198608170), 2026-10-16, Edu's go ("Go ahead and apply all fixes") after the Oct 1-15
search-term diagnosis (64% of visible NB search-term spend on other companies/brands/stores, matched to CallRail transcripts).
1. 'Calls from ads' (AD_CALL 6798761275) min call duration 10s -> 60s, so wrong-number calls stop counting as conversions.
2. Nonbranded 23805382277: PHRASE negatives for other companies / brands / stores / jobs (skips ones already present).
3. Nonbranded: the 3 biggest BROAD keywords get a PHRASE twin in the same ad group, then the BROAD version is paused.
Guards: aborts on unexpected current values; replays negatives against 30d search terms + active keywords first.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB = "2198608170", "23805382277"
CALL_CA, CALL_OLD, CALL_NEW = "6798761275", 10, 60
NEG = ["style crest", "sherwin williams", "bee builders", "homeland vinyl", "leaf filter", "leaffilter",
       "patriot gutters", "h&a home", "home genius", "bluestone homes", "ply gem", "certainteed", "nichiha",
       "master wall", "dolphin panel", "james hardie phone", "james hardie contact", "james hardie products",
       "jameshardie", "jobs", "hiring", "careers", "salary", "for sale", "painting", "free charity"]
TO_PHRASE = ["siding repair", "home siding", "home exterior contractors near me"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum
ST = client.enums.AdGroupCriterionStatusEnum

# --- guards
ca = q(f"SELECT conversion_action.resource_name, conversion_action.name, conversion_action.phone_call_duration_seconds FROM conversion_action WHERE conversion_action.id = {CALL_CA}")[0].conversion_action
print(f"conversion '{ca.name}': min call {ca.phone_call_duration_seconds}s")
if ca.phone_call_duration_seconds != CALL_OLD: sys.exit(f"ABORT: expected {CALL_OLD}s")

existing = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
neg_new = [n for n in NEG if n not in existing]
print(f"negatives: {len(neg_new)} new, already present: {[n for n in NEG if n in existing]}")

terms = q(f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
    WHERE campaign.id = {NB} AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0""")
kws = q(f"""SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
    ad_group_criterion.status, ad_group.resource_name, ad_group.name FROM ad_group_criterion
    WHERE campaign.id = {NB} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED'""")
active = [k.ad_group_criterion.keyword.text.lower() for k in kws if k.ad_group_criterion.status.name == "ENABLED"]
for n in neg_new:
    hit = [r for r in terms if f" {n} " in f" {r.search_term_view.search_term.lower()} "]
    conflicts = [k for k in active if f" {n} " in f" {k} "]
    print(f"  neg '{n}': blocks {len(hit)} terms ${sum(r.metrics.cost_micros for r in hit)/1e6:.2f} conv {sum(r.metrics.conversions for r in hit):.1f}"
          f"{' e.g. ' + str([r.search_term_view.search_term for r in hit][:3]) if hit else ''}{' KW CONFLICT ' + str(conflicts) if conflicts else ''}")
    if conflicts: sys.exit("ABORT: negative conflicts with an active keyword")

broad, phrase_exists = {}, set()
for k in kws:
    t, m = k.ad_group_criterion.keyword.text.lower(), k.ad_group_criterion.keyword.match_type.name
    if t in TO_PHRASE and m == "BROAD" and k.ad_group_criterion.status.name == "ENABLED": broad[t] = k
    if t in TO_PHRASE and m == "PHRASE": phrase_exists.add(t)
print(f"broad to convert: {[(t, broad[t].ad_group.name) for t in broad]}; phrase already exists: {sorted(phrase_exists)}")
if set(broad) != set(TO_PHRASE): sys.exit(f"ABORT: expected enabled BROAD for all of {TO_PHRASE}")

# --- 1. call conversion threshold
op = client.get_type("ConversionActionOperation")
op.update.resource_name = ca.resource_name
op.update.phone_call_duration_seconds = CALL_NEW
op.update_mask.paths.append("phone_call_duration_seconds")
client.get_service("ConversionActionService").mutate_conversion_actions(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("call threshold ok", "(validate_only)" if vo else "APPLIED")

# --- 2. negatives
ops = []
for t in neg_new:
    op = client.get_type("CampaignCriterionOperation"); c = op.create
    c.campaign = ga.campaign_path(CID, NB); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} negatives ok", "(validate_only)" if vo else "APPLIED")

# --- 3. broad -> phrase (create phrase twins first, pause broad only after they exist)
agc = client.get_service("AdGroupCriterionService")
ops = []
for t, k in broad.items():
    if t in phrase_exists: continue
    op = client.get_type("AdGroupCriterionOperation"); c = op.create
    c.ad_group = k.ad_group.resource_name; c.status = ST.ENABLED; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    agc.mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} phrase keywords created", "(validate_only)" if vo else "APPLIED")
ops = []
for t, k in broad.items():
    op = client.get_type("AdGroupCriterionOperation")
    op.update.resource_name = k.ad_group_criterion.resource_name; op.update.status = ST.PAUSED
    op.update_mask.paths.append("status"); ops.append(op)
agc.mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} broad keywords paused", "(validate_only)" if vo else "APPLIED")

if APPLY:
    print("--- read-back")
    ca2 = q(f"SELECT conversion_action.phone_call_duration_seconds FROM conversion_action WHERE conversion_action.id = {CALL_CA}")[0]
    print(f"   Calls from ads min call: {ca2.conversion_action.phone_call_duration_seconds}s")
    got = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"   NB negatives missing: {[n for n in NEG if n not in got]}")
    for r in q(f"""SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status
            FROM ad_group_criterion WHERE campaign.id = {NB} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
            AND ad_group_criterion.status != 'REMOVED'"""):
        if r.ad_group_criterion.keyword.text.lower() in TO_PHRASE:
            print(f"   {r.ad_group.name}: '{r.ad_group_criterion.keyword.text}' {r.ad_group_criterion.keyword.match_type.name} {r.ad_group_criterion.status.name}")
