"""Zen Air 2026-09-30: read-back verification of zenair_change_0930.py."""
import sys
from collections import Counter
sys.path.insert(0, ".")
from lib import run_query
CID = "4360840956"
for r in run_query(CID, """SELECT campaign.name, campaign.status, campaign.bidding_strategy_type,
  campaign.target_spend.cpc_bid_ceiling_micros, campaign.target_impression_share.cpc_bid_ceiling_micros,
  campaign.target_impression_share.location_fraction_micros, campaign_budget.amount_micros, campaign.primary_status
  FROM campaign WHERE campaign.id IN (23675783172, 24100030790)"""):
    c = r["campaign"]
    print(f"{c['name']}: {c['status']} {c['bidding_strategy_type']} maxclicks_cap={c.get('target_spend')} "
          f"tis={c.get('target_impression_share')} budget=${int(r['campaign_budget']['amount_micros'])/1e6:.0f} primary={c.get('primary_status')}")
kw = run_query(CID, """SELECT campaign.id, ad_group_criterion.keyword.match_type, ad_group_criterion.status, ad_group_criterion.negative
  FROM ad_group_criterion WHERE campaign.id IN (23675783172, 24100030790) AND ad_group_criterion.type = 'KEYWORD'
  AND ad_group_criterion.status != 'REMOVED'""")
cnt = Counter(("BR" if r["campaign"]["id"] == "23675783172" else "NB", "NEG" if r["ad_group_criterion"].get("negative") else "POS",
               r["ad_group_criterion"]["keyword"]["match_type"], r["ad_group_criterion"]["status"]) for r in kw)
for k, v in sorted(cnt.items()):
    print("  ad group kw", k, v)
cn = run_query(CID, """SELECT campaign.id, campaign_criterion.keyword.match_type FROM campaign_criterion
  WHERE campaign.id IN (23675783172, 24100030790) AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE""")
for k, v in sorted(Counter(("BR" if r["campaign"]["id"] == "23675783172" else "NB", r["campaign_criterion"]["keyword"]["match_type"]) for r in cn).items()):
    print("  campaign negatives", k, v)
