# APPLIED LIVE 2026-11-06, read-back confirmed (Electrical Max Conv, HVAC $8 cap, 13 negs each, none missing). Do NOT re-run with --apply.
# Edu's go 2026-11-06 ("apply 1, 2 and 3. Negate duct cleaning as well"), from the fu-112 check.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Cool Hand Electric (9865206319):
1. TSD_Search_Electrical: Maximize Clicks $9 cap -> Maximize Conversions (no target). Was $60 CPL on Max Conv the week before the cap; on the cap CPC fell
   $13 -> $5.28 but leads 7 -> 2. Budget $67 unchanged.
2. TSD_Search_HVAC: stays Max Clicks $8 cap (nothing sent, guard only).
3. PHRASE negatives on BOTH campaigns: competitor names, a supply house, an RV part + duct cleaning (go. pages don't list it).
Replays negatives against 30d search terms + live keywords, aborts on a live-keyword conflict or unexpected state.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "9865206319"
C = f"customers/{CID}"
HVAC, ELEC = "24118511502", "24123995882"
NEG = ["bean electric", "david brown", "cummins electrical", "cummings electrical", "rogers electric", "mak electric",
       "pro tech electrical", "walker engineering", "walkertx", "paschal", "reece", "dometic", "duct cleaning"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum

def state():
    out = {}
    for cid in (HVAC, ELEC):
        c = q(f"""SELECT campaign.name, campaign.bidding_strategy_type, campaign.bidding_strategy, campaign.target_spend.cpc_bid_ceiling_micros,
            campaign.maximize_conversions.target_cpa_micros, campaign_budget.amount_micros, campaign.primary_status FROM campaign WHERE campaign.id = {cid}""")[0]
        out[cid] = c
        print(f"  {c.campaign.name}: {c.campaign.bidding_strategy_type.name} cap ${c.campaign.target_spend.cpc_bid_ceiling_micros/1e6:.2f} "
              f"tCPA ${c.campaign.maximize_conversions.target_cpa_micros/1e6:.2f} budget ${c.campaign_budget.amount_micros/1e6:.2f} {c.campaign.primary_status.name} "
              f"portfolio='{c.campaign.bidding_strategy}'")
    return out

print("before:"); st = state()
for cid, cap in ((HVAC, 8.0), (ELEC, 9.0)):
    c = st[cid].campaign
    if c.bidding_strategy or c.bidding_strategy_type.name != "TARGET_SPEND" or abs(c.target_spend.cpc_bid_ceiling_micros / 1e6 - cap) > 0.01:
        sys.exit(f"ABORT: unexpected bidding on {c.name}")

conflict = False
neg_new = {}
for cid in (HVAC, ELEC):
    name = st[cid].campaign.name
    terms = q(f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
        WHERE campaign.id = {cid} AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0""")
    kws = [k.ad_group_criterion.keyword.text.lower() for k in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
        WHERE campaign.id = {cid} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
    existing = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {cid} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    neg_new[cid] = [n for n in NEG if n not in existing]
    print(f"\n{name}:")
    for n in NEG:
        hit = [t for t in terms if f" {n} " in f" {t.search_term_view.search_term.lower()} "]
        kc = [k for k in kws if f" {n} " in f" {k} "]
        conflict |= bool(kc)
        if hit or kc or n in existing:
            print(f"  '{n}': {'ALREADY THERE ' if n in existing else ''}blocks {len(hit)} terms {[h.search_term_view.search_term for h in hit][:4]}, "
                  f"${sum(t.metrics.cost_micros for t in hit)/1e6:.2f}, conv {sum(t.metrics.conversions for t in hit):.1f}; kw conflicts: {kc}")
if conflict: sys.exit("ABORT: a negative blocks a live keyword")

ops = []
o = client.get_type("MutateOperation"); u = o.campaign_operation.update
u.resource_name = f"{C}/campaigns/{ELEC}"; u.maximize_conversions.target_cpa_micros = 0
o.campaign_operation.update_mask.paths.append("maximize_conversions.target_cpa_micros"); ops.append(o)
for cid, lst in neg_new.items():
    for t in lst:
        o = client.get_type("MutateOperation"); cc = o.campaign_criterion_operation.create
        cc.campaign = f"{C}/campaigns/{cid}"; cc.negative = True; cc.keyword.text = t; cc.keyword.match_type = MT.PHRASE; ops.append(o)
req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = vo
ga.mutate(request=req)
print(("\nAPPLIED" if APPLY else "\nVALIDATE-ONLY OK (nothing written)") + f": Electrical -> Max Conversions, negatives HVAC {len(neg_new[HVAC])} / Electrical {len(neg_new[ELEC])}")

if APPLY:
    print("read-back:"); state()
    for cid in (HVAC, ELEC):
        got = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {cid} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
        print(f"  {cid} negatives missing: {[n for n in NEG if n not in got]}")
