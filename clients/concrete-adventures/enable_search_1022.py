# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Concrete Adventures (9215192296), 2026-10-22, Edu: "ok so can we just push live now?" (after skipping the CallRail pool for now).
Enables TSD_10.22_Search_Branded_Oxford 24379794681 ($5/d) + TSD_10.22_Search_Nonbranded_Oxford 24379794684 ($10/d).
Aborts if budgets/caps differ from the build."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "9215192296"
EXPECT = {"24379794681": (5.0, 4.0), "24379794684": (10.0, 10.0)}
APPLY = "--apply" in sys.argv
client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
SQL = f"""SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign_budget.amount_micros,
    campaign.target_spend.cpc_bid_ceiling_micros FROM campaign WHERE campaign.id IN ({",".join(EXPECT)})"""
ops = []
for r in q(SQL):
    c = r.campaign; b, cap = EXPECT[str(c.id)]
    print(f"{c.name} {c.status.name} budget ${r.campaign_budget.amount_micros/1e6:.2f} cap ${c.target_spend.cpc_bid_ceiling_micros/1e6:.2f}")
    if abs(r.campaign_budget.amount_micros/1e6 - b) > 0.01 or abs(c.target_spend.cpc_bid_ceiling_micros/1e6 - cap) > 0.01: sys.exit("ABORT: budget/cap changed")
    op = client.get_type("CampaignOperation"); op.update.resource_name = c.resource_name
    op.update.status = client.enums.CampaignStatusEnum.ENABLED; op.update_mask.paths.append("status"); ops.append(op)
if len(ops) != 2: sys.exit("ABORT: campaigns not found")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print("OK", "APPLIED" if APPLY else "(validate_only)")
if APPLY:
    for r in q(SQL.replace("campaign.primary_status,", "campaign.primary_status, campaign.primary_status_reasons,")):
        print(f"   {r.campaign.name}: {r.campaign.status.name} / {r.campaign.primary_status.name} {[x.name for x in r.campaign.primary_status_reasons]}")
