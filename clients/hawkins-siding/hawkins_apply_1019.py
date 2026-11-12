# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Hawkins Siding (2198608170), 2026-10-19, Edu's go ("You have my approval, apply these changes") after the
10-16 -> 10-19 post-fix read: all 4 PPC calls were non-leads, ~75% of visible NB search-term spend still off-target,
and the spend moved from the 3 keywords switched to phrase on 10-16 to the other BROAD keywords.
1. Nonbranded 23805382277: PHRASE negatives for suppliers / Angi / Dabella / Spanish 'venta' / stone veneer / hardie smart.
2. Nonbranded: the 5 BROAD keywords that spent 10-16 -> 10-19 get a PHRASE twin in the same ad group, then the BROAD is paused.
Guards: aborts on keyword conflicts or unexpected keyword state; replays negatives against 30d search terms first.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, NB = "2198608170", "23805382277"
NEG = ["supplier", "suppliers", "angie", "angies", "dabella", "venta", "stone veneer", "hardie smart"]
TO_PHRASE = ["siding repair near me", "exterior siding contractors", "vinyl siding", "siding replacement", "house exterior siding"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum
ST = client.enums.AdGroupCriterionStatusEnum

# --- guards
existing = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
neg_new = [n for n in NEG if n not in existing]
print(f"negatives: {len(neg_new)} new, already present: {[n for n in NEG if n in existing]}")

terms = q(f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
    WHERE campaign.id = {NB} AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0""")
kws = q(f"""SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
    ad_group_criterion.status, ad_group.resource_name, ad_group.name, ad_group.status FROM ad_group_criterion
    WHERE campaign.id = {NB} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED'""")
active = [k.ad_group_criterion.keyword.text.lower() for k in kws
          if k.ad_group_criterion.status.name == "ENABLED" and k.ad_group.status.name == "ENABLED"]
for n in neg_new:
    hit = [r for r in terms if f" {n} " in f" {r.search_term_view.search_term.lower()} "]
    conflicts = [k for k in active if f" {n} " in f" {k} "]
    print(f"  neg '{n}': blocks {len(hit)} terms ${sum(r.metrics.cost_micros for r in hit)/1e6:.2f} conv {sum(r.metrics.conversions for r in hit):.1f}"
          f"{' e.g. ' + str([r.search_term_view.search_term for r in hit][:4]) if hit else ''}{' KW CONFLICT ' + str(conflicts) if conflicts else ''}")
    if conflicts: sys.exit("ABORT: negative conflicts with an active keyword")

broad, phrase_exists = {}, set()
for k in kws:
    t, m = k.ad_group_criterion.keyword.text.lower(), k.ad_group_criterion.keyword.match_type.name
    if t in TO_PHRASE and m == "BROAD" and k.ad_group_criterion.status.name == "ENABLED" and k.ad_group.status.name == "ENABLED": broad[t] = k
    if t in TO_PHRASE and m == "PHRASE": phrase_exists.add((t, k.ad_group.resource_name))
print(f"broad to convert: {[(t, broad[t].ad_group.name) for t in broad]}; phrase already exists: {sorted(x[0] for x in phrase_exists)}")
if set(broad) != set(TO_PHRASE): sys.exit(f"ABORT: expected enabled BROAD for all of {TO_PHRASE}")

# --- 1. negatives
ops = []
for t in neg_new:
    op = client.get_type("CampaignCriterionOperation"); c = op.create
    c.campaign = ga.campaign_path(CID, NB); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} negatives ok", "(validate_only)" if vo else "APPLIED")

# --- 2. broad -> phrase (create phrase twins first, pause broad only after they exist)
agc = client.get_service("AdGroupCriterionService")
ops = []
for t, k in broad.items():
    if (t, k.ad_group.resource_name) in phrase_exists: continue
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
    got = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"   NB negatives missing: {[n for n in NEG if n not in got]}")
    for r in q(f"""SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status
            FROM ad_group_criterion WHERE campaign.id = {NB} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
            AND ad_group_criterion.status != 'REMOVED'"""):
        if r.ad_group_criterion.keyword.text.lower() in TO_PHRASE:
            print(f"   {r.ad_group.name}: '{r.ad_group_criterion.keyword.text}' {r.ad_group_criterion.keyword.match_type.name} {r.ad_group_criterion.status.name}")
    left = [f"{r.ad_group.name}: {r.ad_group_criterion.keyword.text}" for r in q(f"""SELECT ad_group.name, ad_group_criterion.keyword.text
            FROM ad_group_criterion WHERE campaign.id = {NB} AND ad_group.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD'
            AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED' AND ad_group_criterion.keyword.match_type = 'BROAD'""")]
    print(f"   enabled BROAD left in live ad groups: {len(left)}")
