import sys; sys.path.insert(0, '.')
from lib import run_query
q = "SELECT campaign.name, metrics.cost_micros FROM campaign WHERE segments.date BETWEEN '2026-09-12' AND '2026-10-11' AND metrics.cost_micros > 0"
t = 0
for r in run_query('4467722415', q):
    m = r.get('metrics', {}); c = int(m.get('costMicros', m.get('cost_micros')))
    t += c; print(c, r['campaign']['name'])
print('total', t)
