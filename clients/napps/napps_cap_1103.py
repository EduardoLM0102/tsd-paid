# APPLIED LIVE 2026-11-03, read-back confirmed (both caps $25, budgets $65/$35 unchanged). Do NOT re-run with --apply.
# Edu's go 2026-11-03 ("Yes, work on the three topics you brought up"), Command Center fu-120.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Napps (9509605037), 2026-11-03: Max Clicks CPC cap $15 -> $25 on both Nonbranded campaigns (Heating 24049055193, Plumbing 23819717682).
Budgets unchanged ($65 / $35). Week 1 spent $77 of $600 with ~70% rank-lost; CPCs were $26-39 before the relaunch. Aborts on unexpected values."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "9509605037"
CAMPS = {"24049055193": "NB Heating", "23819717682": "NB Plumbing"}
OLD, NEW = 15.0, 25.0
APPLY = "--apply" in sys.argv

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
SEL = f"""SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.bidding_strategy,
    campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros FROM campaign WHERE campaign.id IN ({','.join(CAMPS)})"""

ops = []
for r in q(SEL):
    c = r.campaign; cap = c.target_spend.cpc_bid_ceiling_micros / 1e6
    print(f"before: {c.name} {c.status.name} {c.bidding_strategy_type.name} cap ${cap:.2f} budget ${r.campaign_budget.amount_micros/1e6:.2f}")
    if c.bidding_strategy_type.name != "TARGET_SPEND" or c.bidding_strategy: sys.exit(f"ABORT: {c.name} not standard Max Clicks")
    if abs(cap - OLD) > 0.01: sys.exit(f"ABORT: {c.name} cap ${cap:.2f}, expected ${OLD:.2f}")
    op = client.get_type("CampaignOperation"); op.update.resource_name = ga.campaign_path(CID, str(c.id))
    op.update.target_spend.cpc_bid_ceiling_micros = int(NEW * 1e6)
    op.update_mask.paths.append("target_spend.cpc_bid_ceiling_micros"); ops.append(op)
if len(ops) != 2: sys.exit("ABORT: expected 2 campaigns")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print(f"cap ${OLD:.0f} -> ${NEW:.0f} on 2 campaigns", "APPLIED" if APPLY else "ok (validate_only, nothing changed)")
if APPLY:
    for r in q(SEL):
        print(f"read-back: {r.campaign.name} cap ${r.campaign.target_spend.cpc_bid_ceiling_micros/1e6:.2f} budget ${r.campaign_budget.amount_micros/1e6:.2f} {r.campaign.status.name}")
