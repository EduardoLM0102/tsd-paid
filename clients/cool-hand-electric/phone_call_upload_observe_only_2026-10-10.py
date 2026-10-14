"""Cool Hand 2026-10-10: make CallRail's 'Phone Call' upload action (7830770637, DEFAULT/WEBSITE) observe-only.
ALREADY APPLIED 2026-10-10, don't re-run.
Why: the CallRail Website pool started swapping on go. pages (10-10), so CallRail will begin uploading website calls with gclid
into 'Phone Call'. Its goal (DEFAULT/WEBSITE) was biddable on every campaign -> would double count with 'Click to call' taps
under Max Conversions. Edu decides later which call signal bids. 'Phone Call' is the only action in DEFAULT/WEBSITE.
Biddability lives in the goal, not primary_for_goal (see memory: goals mechanics). FieldMask must be explicit for False.
Rollback: same script with False -> True.
Run: ./tsd.sh <abs path to this file>
"""
import os
import sys
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import init_client
from google.protobuf import field_mask_pb2

CID = "9865206319"
c = init_client(); ga = c.get_service("GoogleAdsService"); E = c.enums
q = lambda s: list(ga.search(customer_id=CID, query=s))
others = [r.conversion_action.name for r in q("""SELECT conversion_action.name, conversion_action.category, conversion_action.origin FROM conversion_action
  WHERE conversion_action.status = 'ENABLED' AND conversion_action.category = 'DEFAULT' AND conversion_action.origin = 'WEBSITE'""")]
assert others == ["Phone Call"], others   # make sure we only switch off this one action

cust = [r.customer_conversion_goal.resource_name for r in q("""SELECT customer_conversion_goal.resource_name FROM customer_conversion_goal
  WHERE customer_conversion_goal.category = 'DEFAULT' AND customer_conversion_goal.origin = 'WEBSITE' AND customer_conversion_goal.biddable = TRUE""")]
ops = []
for rn in cust:
    op = c.get_type("CustomerConversionGoalOperation"); op.update.resource_name = rn; op.update.biddable = False
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["biddable"])); ops.append(op)
if ops: print("customer goal:", len(c.get_service("CustomerConversionGoalService").mutate_customer_conversion_goals(customer_id=CID, operations=ops).results))

camp = [(r.campaign.name, r.campaign_conversion_goal.resource_name) for r in q("""SELECT campaign.name, campaign.status, campaign_conversion_goal.resource_name
  FROM campaign_conversion_goal WHERE campaign_conversion_goal.category = 'DEFAULT' AND campaign_conversion_goal.origin = 'WEBSITE'
  AND campaign_conversion_goal.biddable = TRUE AND campaign.status != 'REMOVED'""")]
ops = []
for name, rn in camp:
    op = c.get_type("CampaignConversionGoalOperation"); op.update.resource_name = rn; op.update.biddable = False
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["biddable"])); ops.append(op)
if ops: print("campaign goals:", len(c.get_service("CampaignConversionGoalService").mutate_campaign_conversion_goals(customer_id=CID, operations=ops).results), [n for n, _ in camp])

print("READ-BACK")
for r in q("SELECT customer_conversion_goal.biddable FROM customer_conversion_goal WHERE customer_conversion_goal.category = 'DEFAULT' AND customer_conversion_goal.origin = 'WEBSITE'"):
    print("  account default DEFAULT/WEBSITE biddable =", r.customer_conversion_goal.biddable)
for r in q("""SELECT campaign.name, campaign.status, campaign_conversion_goal.biddable FROM campaign_conversion_goal
  WHERE campaign_conversion_goal.category = 'DEFAULT' AND campaign_conversion_goal.origin = 'WEBSITE' AND campaign.status = 'ENABLED'"""):
    print(f"  {r.campaign.name:42} biddable = {r.campaign_conversion_goal.biddable}")
