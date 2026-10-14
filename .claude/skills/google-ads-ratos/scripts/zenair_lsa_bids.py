"""Zen Air LSA: show the stored bidding values (strategy, target per lead, max per lead).
Run: ./tsd.sh zenair_lsa_bids.py"""
from lib import run_query

rows = run_query('3740502923', """
    SELECT campaign.id, campaign.bidding_strategy_type,
           campaign.local_services_campaign_settings.category_bids
    FROM campaign""")
for r in rows:
    c = r['campaign']
    print(f"campaign {c['id']}  strategy: {c['bidding_strategy_type']}")
    for b in c.get('local_services_campaign_settings', {}).get('category_bids', []):
        tgt = int(b.get('target_cpa_bid_micros', 0)) / 1e6
        man = int(b.get('manual_cpa_bid_micros', 0)) / 1e6
        print(f"  {b['category_id']}: target per lead ${tgt:.2f} | manual max per lead ${man:.2f}")
