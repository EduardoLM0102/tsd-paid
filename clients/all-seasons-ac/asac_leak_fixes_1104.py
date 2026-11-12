# APPLIED LIVE 2026-11-04, read-back confirmed. Do NOT re-run with --apply.
# Edu's go 2026-11-04 ("Fix the leaks with your suggestions"), Command Center fu-089. Total budget unchanged ($46/d).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""All Seasons AC (4467722415), 2026-11-04 leak fixes from the fu-089 read:
1. Attach shared list COMPETITORS 8126127802 (already on LeadGen) to MiniSplit 24050402045, and add 11 new competitor names to it (PHRASE).
   + PHRASE 'insulation' on MiniSplit (residential insulation company $10.64).
2. MiniSplit 'mini split heat pump' BROAD ($99.21 / 10 clk / 0 conv) → add the same keyword as PHRASE in its ad group, pause the BROAD one.
3. Secondary (out of bidding, still under All conversions): 'Click to call' 7719769169 (CLICK_TO_CALL = ad call-button taps) and the GA4 CONTACT
   events mailto 7213245094, phone_link_click 7213245097, book_now 7214412880.
Guards: every new negative is replayed against LeadGen + MiniSplit enabled keywords; the COMPETITORS list is checked against MiniSplit keywords."""
import sys, re
sys.path.insert(0, ".")
from google.protobuf import field_mask_pb2
from lib import init_client

CID, LG, MS, COMP = "4467722415", "11803942938", "24050402045", "8126127802"
NEW_COMP = ["universe home services", "wcesp", "kool point", "flynn aire", "flynnaire", "sweezy's", "argo plumbing", "mac heating",
            "dix hills air conditioning", "quality air care", "dole fuel"]
MS_NEG = ["insulation"]
BROAD_KW = "mini split heat pump"
SECONDARY = {7719769169: "Click to call", 7213245094: "mailto_link_click", 7213245097: "phone_link_click", 7214412880: "book_now_link_click"}
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
E = client.enums
q = lambda s: list(ga.search(customer_id=CID, query=s))
norm = lambda t: f" {re.sub(r'[^a-z0-9 ]', ' ', t.lower())} "

kw_rows = q(f"""SELECT campaign.id, ad_group.id, ad_group_criterion.criterion_id, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
    ad_group_criterion.status FROM ad_group_criterion WHERE campaign.id IN ({LG},{MS}) AND ad_group_criterion.type = 'KEYWORD'
    AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED' AND ad_group.status = 'ENABLED'""")
kws = {(str(r.campaign.id), r.ad_group_criterion.keyword.text.lower()) for r in kw_rows}
ms_kws = [t for c, t in kws if c == MS]

# --- 1a. COMPETITORS list vs MiniSplit keywords
comp = [r.shared_criterion.keyword.text.lower() for r in q(f"SELECT shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.id = {COMP}")]
clash = [(n, k) for n in comp for k in ms_kws if norm(n).strip() and norm(n) in norm(k)]
print(f"COMPETITORS list: {len(comp)} terms; clashes with MiniSplit keywords: {clash[:10]}")
if clash: sys.exit("ABORT: COMPETITORS list would block a MiniSplit keyword")
attached = q(f"SELECT campaign_shared_set.status FROM campaign_shared_set WHERE campaign.id = {MS} AND shared_set.id = {COMP} AND campaign_shared_set.status = 'ENABLED'")

# --- 1b. new names + insulation vs all keywords
for n in NEW_COMP + MS_NEG:
    kc = [k for c, k in kws if norm(n) in norm(k)]
    if kc: sys.exit(f"ABORT: '{n}' would block {kc}")
new_comp = [n for n in NEW_COMP if n not in comp]
ms_existing = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {MS} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
ms_neg = [n for n in MS_NEG if n not in ms_existing]
print(f"new COMPETITORS terms: {new_comp}; MiniSplit campaign negs: {ms_neg}; list already on MiniSplit: {bool(attached)}")

# --- 2. broad → phrase
broad = [r for r in kw_rows if str(r.campaign.id) == MS and r.ad_group_criterion.keyword.text.lower() == BROAD_KW
         and r.ad_group_criterion.keyword.match_type.name == "BROAD"]
phrase_exists = [r for r in kw_rows if str(r.campaign.id) == MS and r.ad_group_criterion.keyword.text.lower() == BROAD_KW
                 and r.ad_group_criterion.keyword.match_type.name == "PHRASE"]
print(f"'{BROAD_KW}' BROAD found: {len(broad)}, PHRASE already: {len(phrase_exists)}")

# --- 3. conversion actions
ca = {r.conversion_action.id: r.conversion_action for r in q(f"""SELECT conversion_action.id, conversion_action.name, conversion_action.primary_for_goal
    FROM conversion_action WHERE conversion_action.id IN ({','.join(map(str, SECONDARY))})""")}
for i, frag in SECONDARY.items():
    if i not in ca or frag.lower() not in ca[i].name.lower(): sys.exit(f"ABORT: conversion action {i} not '{frag}'")

ops = []
def op(): return client.get_type("MutateOperation")
if not attached:
    o = op(); c = o.campaign_shared_set_operation.create; c.campaign = ga.campaign_path(CID, MS); c.shared_set = ga.shared_set_path(CID, COMP); ops.append(o)
for t in new_comp:
    o = op(); c = o.shared_criterion_operation.create; c.shared_set = ga.shared_set_path(CID, COMP); c.keyword.text = t; c.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE; ops.append(o)
for t in ms_neg:
    o = op(); c = o.campaign_criterion_operation.create; c.campaign = ga.campaign_path(CID, MS); c.negative = True
    c.keyword.text = t; c.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE; ops.append(o)
for b in broad:
    if not phrase_exists:
        o = op(); c = o.ad_group_criterion_operation.create; c.ad_group = ga.ad_group_path(CID, str(b.ad_group.id))
        c.status = E.AdGroupCriterionStatusEnum.ENABLED; c.keyword.text = BROAD_KW; c.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE; ops.append(o)
    o = op(); u = o.ad_group_criterion_operation.update
    u.resource_name = ga.ad_group_criterion_path(CID, str(b.ad_group.id), str(b.ad_group_criterion.criterion_id))
    u.status = E.AdGroupCriterionStatusEnum.PAUSED; o.ad_group_criterion_operation.update_mask.paths.append("status"); ops.append(o)
req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = vo
if ops: ga.mutate(request=req)
ca_ops = []
for i in SECONDARY:
    if ca[i].primary_for_goal:
        o = client.get_type("ConversionActionOperation"); o.update.resource_name = ga.conversion_action_path(CID, str(i)); o.update.primary_for_goal = False
        o.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["primary_for_goal"])); ca_ops.append(o)
if ca_ops:
    client.get_service("ConversionActionService").mutate_conversion_actions(request={"customer_id": CID, "operations": ca_ops, "validate_only": vo})
print(f"{len(ops)} account op(s) + {len(ca_ops)} conversion action(s)", "APPLIED" if APPLY else "ok (validate_only)")

if APPLY:
    print("read-back: list on MiniSplit:", bool(q(f"SELECT campaign_shared_set.status FROM campaign_shared_set WHERE campaign.id = {MS} AND shared_set.id = {COMP} AND campaign_shared_set.status = 'ENABLED'")))
    got = {r.shared_criterion.keyword.text.lower() for r in q(f"SELECT shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.id = {COMP}")}
    print("read-back: new competitor terms missing:", [n for n in NEW_COMP if n not in got])
    for r in q(f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status FROM ad_group_criterion
        WHERE campaign.id = {MS} AND ad_group_criterion.keyword.text = '{BROAD_KW}'"""):
        print("read-back kw:", r.ad_group_criterion.keyword.text, r.ad_group_criterion.keyword.match_type.name, r.ad_group_criterion.status.name)
    for r in q(f"SELECT conversion_action.id, conversion_action.name, conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric FROM conversion_action WHERE conversion_action.id IN ({','.join(map(str, SECONDARY))})"):
        a = r.conversion_action; print(f"read-back: {a.id} {a.name[:40]} primary={a.primary_for_goal} in_conv={a.include_in_conversions_metric}")
