"""Summarize weekly_pull.py output. python3 weekly_summary.py <json> [--terms N]"""
import json, sys
from collections import defaultdict
d = json.load(open(sys.argv[1]))
NT = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[2] == "--terms" else 25
M = 1e6
def g(r, *path, default=None):
    for p in path:
        if not isinstance(r, dict): return default
        r = r.get(p)
    return default if r is None else r
def num(x):
    try: return float(x)
    except: return 0.0

def camp_table(rows, label):
    print(f"\n### Campaigns {label}")
    tot = defaultdict(float)
    for r in sorted(rows, key=lambda r: -num(g(r,'metrics','cost_micros',default=0))):
        c = r['campaign']; m = r.get('metrics', {})
        cost = num(m.get('cost_micros'))/M
        if cost == 0 and c.get('status') != 'ENABLED': continue
        ch = c.get('advertising_channel_type')
        conv = num(m.get('conversions')); clk = num(m.get('clicks'))
        bud = num(g(r,'campaign_budget','amount_micros'))/M
        isv = m.get('search_impression_share'); bl = m.get('search_budget_lost_impression_share'); rl = m.get('search_rank_lost_impression_share')
        ceil = num(g(c,'target_impression_share','cpc_bid_ceiling_micros'))/M or num(g(c,'target_spend','cpc_bid_ceiling_micros'))/M
        tcpa = num(g(c,'maximize_conversions','target_cpa_micros'))/M
        net = g(c,'network_settings',default={})
        print(f"- {c['name']} ({c['id']}) [{ch}/{c.get('status')}/{c.get('primary_status')}] {c.get('bidding_strategy_type')}"
              f"{' ceil $%.2f'%ceil if ceil else ''}{' tCPA $%.0f'%tcpa if tcpa else ''} bud ${bud:.0f}/d | spend ${cost:,.2f} clk {clk:.0f} conv {conv:.1f} allconv {num(m.get('all_conversions')):.1f}"
              f" CPL {('$%.2f'%(cost/conv)) if conv else '-'} CPC {('$%.2f'%(cost/clk)) if clk else '-'}"
              f" IS {isv} bl {bl} rl {rl} partners={net.get('target_search_network')} display={net.get('target_content_network')}")
        key = 'LSA' if ch == 'LOCAL_SERVICES' else 'PPC'
        tot[key+'_cost'] += cost; tot[key+'_conv'] += conv; tot[key+'_clk'] += clk; tot[key+'_impr'] += num(m.get('impressions'))
    for k in ('PPC','LSA'):
        if tot[k+'_cost'] or tot[k+'_conv']:
            c, v, k2 = tot[k+'_cost'], tot[k+'_conv'], tot[k+'_clk']
            print(f"  TOTAL {k}: spend ${c:,.2f} clk {k2:.0f} conv {v:.1f} CPL {('$%.2f'%(c/v)) if v else '-'} CPC {('$%.2f'%(c/k2)) if k2 else '-'} CVR {('%.2f%%'%(v/k2*100)) if k2 else '-'}")
    return tot

if isinstance(d['campaigns'], dict): print("ERR", d['campaigns']); sys.exit()
print(f"# {d['cid']} window {d['window']} prev {d['prev']}")
camp_table(d['campaigns'], "THIS WEEK")
camp_table(d['campaigns_prev'], "PREV WEEK")

names = {r['campaign']['id']: r['campaign']['name'] for r in d['campaigns'] + d['campaigns_prev']}
print("\n### Enabled campaigns (status reasons)")
for r in d['campaigns_enabled']:
    c = r['campaign']; print(f"- {c['name']} {c.get('advertising_channel_type')} {c.get('primary_status')} {c.get('primary_status_reasons')} bud ${num(g(r,'campaign_budget','amount_micros'))/M:.0f}")

print("\n### Conversions by action (this week)")
for r in sorted(d['conv_by_action'], key=lambda r: -num(r['metrics'].get('all_conversions'))):
    s = r['segments']; m = r['metrics']
    print(f"- {r['campaign']['name'][:45]:45s} | {s.get('conversion_action_name')[:40]:40s} {s.get('conversion_action_category')} conv {num(m.get('conversions')):.1f} all {num(m.get('all_conversions')):.1f}")
print("\n### Conversions by action (prev week, primary only)")
agg = defaultdict(float)
for r in d['conv_by_action_prev']:
    agg[(names.get(r['campaign']['id'], r['campaign']['id'])[:45], r['segments']['conversion_action_name'])] += num(r['metrics']['conversions'])
for k, v in sorted(agg.items(), key=lambda x: -x[1]): print(f"- {k[0]:45s} | {k[1]} {v:.1f}")

print("\n### Networks")
for r in d['networks']:
    m = r['metrics']; print(f"- {r['campaign']['name'][:45]:45s} {r['segments']['ad_network_type']:16s} ${num(m.get('cost_micros'))/M:,.2f} clk {m.get('clicks')} conv {num(m.get('conversions')):.1f}")

print("\n### Daily spend vs budget (days > 1.4x budget flagged)")
bud = {r['campaign']['id']: num(g(r,'campaign_budget','amount_micros'))/M for r in d['campaigns']}
for r in sorted(d['daily'], key=lambda r: (r['campaign']['name'], r['segments']['date'])):
    cost = num(r['metrics'].get('cost_micros'))/M; b = bud.get(r['campaign']['id'], 0)
    if b and cost > 1.4*b:
        print(f"- {r['campaign']['name'][:45]} {r['segments']['date']} ${cost:.2f} vs ${b:.0f} clk {r['metrics'].get('clicks')}")

calls = d['calls'] if isinstance(d['calls'], list) else []
print(f"\n### Calls (call_view) this week: {len(calls)}")
bycamp = defaultdict(lambda: [0,0])
for r in calls:
    dur = num(g(r,'call_view','call_duration_seconds')); n = r['campaign']['name']
    bycamp[n][0] += 1; bycamp[n][1] += dur >= 60
for n,(a,b) in bycamp.items(): print(f"- {n}: {a} calls, {b} >=60s")

print("\n### Changes since prev start (grouped)")
ch = d['changes'] if isinstance(d['changes'], list) else []
grp = defaultdict(int)
for r in ch:
    e = r.get('change_event', r)
    k = (e.get('change_date_time','')[:13], e.get('user_email'), e.get('client_type'), e.get('change_resource_type'), e.get('resource_change_operation'), names.get(str(e.get('campaign','')).split('/')[-1], str(e.get('campaign','')).split('/')[-1]), str(e.get('changed_fields'))[:70])
    grp[k] += 1
for k, n in grp.items(): print(f"- x{n} " + " ".join(str(x) for x in k))

print(f"\n### Keywords (spend>0) with QS")
for r in sorted(d['keywords'], key=lambda r: -num(r['metrics'].get('cost_micros')))[:30]:
    k = r['ad_group_criterion']; m = r['metrics']
    print(f"- {r['campaign']['name'][:28]:28s} {r['ad_group']['name'][:22]:22s} [{k['keyword']['match_type'][:6]}] {k['keyword']['text'][:38]:38s} {k.get('status')} QS {g(k,'quality_info','quality_score')} ${num(m.get('cost_micros'))/M:,.2f} clk {m.get('clicks')} conv {num(m.get('conversions')):.1f}")

print(f"\n### Search terms by cost (top {NT})")
for r in sorted(d['search_terms'], key=lambda r: -num(r['metrics'].get('cost_micros')))[:NT]:
    m = r['metrics']; s = r['search_term_view']
    print(f"- {r['campaign']['name'][:28]:28s} {s['search_term'][:50]:50s} [{g(r,'segments','keyword','info','match_type',default='')[:5]}] {g(r,'segments','keyword','info','text',default='')[:28]:28s} ${num(m.get('cost_micros'))/M:,.2f} clk {m.get('clicks')} conv {num(m.get('conversions')):.1f} {s.get('status')}")
