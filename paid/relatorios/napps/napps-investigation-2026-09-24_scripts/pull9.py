from h import *
from collections import defaultdict
q = """
SELECT campaign.id, campaign.name, campaign.advertising_channel_type, segments.date,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions
FROM campaign
WHERE segments.date BETWEEN '2025-01-01' AND '2026-09-23'
"""
rows=list(run_query(CID,q))
json.dump(rows, open(OUT+"daily_all.json","w"), default=str)
print(len(rows))
