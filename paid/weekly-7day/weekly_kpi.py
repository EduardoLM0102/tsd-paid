"""KPI - Google Search numbers from weekly_pull.py output (PPC only, LSA excluded, PMax/Smart = unbranded).
python3 weekly_kpi.py <json> ..."""
import json, sys
M = 1e6
def f(x):
    try: return float(x)
    except: return 0.0
for p in sys.argv[1:]:
    d = json.load(open(p))
    t = dict(spend=0, clk=0, conv=0, b_spend=0, b_conv=0, u_spend=0, u_conv=0, impr=0, elig=0)
    for r in d['campaigns']:
        c, m = r['campaign'], r['metrics']
        if c.get('advertising_channel_type') == 'LOCAL_SERVICES': continue
        cost = f(m.get('cost_micros'))/M; conv = f(m.get('conversions')); clk = f(m.get('clicks'))
        if not (cost or conv or clk): continue
        n = c['name'].lower()
        branded = 'branded' in n and 'nonbranded' not in n and 'non-branded' not in n
        t['spend'] += cost; t['clk'] += clk; t['conv'] += conv
        t['b_spend' if branded else 'u_spend'] += cost; t['b_conv' if branded else 'u_conv'] += conv
        isv = m.get('search_impression_share')
        if c.get('advertising_channel_type') == 'SEARCH' and isv:
            t['impr'] += f(m.get('impressions')); t['elig'] += f(m.get('impressions'))/f(isv)
    IS = t['impr']/t['elig']*100 if t['elig'] else None
    out = dict(cid=d['cid'], spend=round(t['spend'],2), leads=round(t['conv'],1), clicks=int(t['clk']),
        cpl=round(t['spend']/t['conv'],2) if t['conv'] else None, cpc=round(t['spend']/t['clk'],2) if t['clk'] else None,
        cvr=round(t['conv']/t['clk']*100,2) if t['clk'] else None,
        branded_leads=round(t['b_conv'],1), branded_spend=round(t['b_spend'],2), branded_cpl=round(t['b_spend']/t['b_conv'],2) if t['b_conv'] else None,
        unbranded_leads=round(t['u_conv'],1), unbranded_spend=round(t['u_spend'],2), unbranded_cpl=round(t['u_spend']/t['u_conv'],2) if t['u_conv'] else None,
        search_IS=round(IS,2) if IS is not None else None)
    print(json.dumps(out))
