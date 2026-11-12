# READ-ONLY recheck of the 10-21 changes on Nick's Heating & Air, Google Ads 1854100356 (fu-078)
import os
import sys, collections
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import run_query
CID = "1854100356"
PRE = ("2026-10-15", "2026-10-20")
POST = ("2026-10-22", "2026-10-27")
NB, BR, PMAX, LSA = "23821497590", "23675600637", "23586346547", "23344968885"
def q(label, gaql):
    try:
        return run_query(CID, gaql)
    except SystemExit:
        print(f"   !! query failed: {label}"); return []
    except Exception as e:
        print(f"   !! {label}: {str(e)[:300]}"); return []
M = lambda x: int(x or 0)/1e6
def H(t): print("\n" + "="*100 + f"\n{t}\n" + "="*100)
def W(r): return f"segments.date BETWEEN '{r[0]}' AND '{r[1]}'"

H("SETTINGS READ-BACK")
for r in q("camps", """SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons,
  campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros, campaign.maximize_conversions.target_cpa_micros,
  campaign.geo_target_type_setting.positive_geo_target_type, campaign_budget.amount_micros
  FROM campaign WHERE campaign.status = 'ENABLED'"""):
    c = r["campaign"]; b = r.get("campaign_budget", {})
    cap = (c.get("target_spend") or {}).get("cpc_bid_ceiling_micros")
    print(f"- {c['name']} [{c['id']}] {c.get('primary_status')} {c.get('primary_status_reasons','')}")
    print(f"    bid={c.get('bidding_strategy_type')} cap={'$%.2f' % M(cap) if cap else '-'} budget=${M(b.get('amount_micros')):.2f} geo={c.get('geo_target_type_setting',{}).get('positive_geo_target_type')}")

H("CHANGES SINCE 10-21 (anyone)")
for r in q("chg", """SELECT change_event.change_date_time, change_event.user_email, change_event.client_type, change_event.change_resource_type,
  change_event.resource_change_operation, change_event.changed_fields, campaign.name
  FROM change_event WHERE change_event.change_date_time BETWEEN '2026-10-21 00:00:00' AND '2026-10-28 23:59:59'
  ORDER BY change_event.change_date_time LIMIT 200"""):
    e = r["change_event"]
    print(f"  {e['change_date_time'][:16]} {e.get('user_email','?'):<35} {e.get('change_resource_type'):<22} {e.get('resource_change_operation'):<7} {r.get('campaign',{}).get('name','')[:35]} {str(e.get('changed_fields',''))[:80]}")

H(f"CAMPAIGNS: PRE {PRE} vs POST {POST} (6 days each)")
for lab, rng in (("PRE", PRE), ("POST", POST)):
    print(f"-- {lab}")
    tot = collections.Counter()
    for r in q(lab, f"""SELECT campaign.id, campaign.name, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions,
      metrics.all_conversions, metrics.search_impression_share, metrics.search_rank_lost_impression_share,
      metrics.search_budget_lost_impression_share FROM campaign WHERE {W(rng)} AND metrics.impressions > 0"""):
        c = r["campaign"]; m = r["metrics"]
        cost = M(m.get("cost_micros")); cl = int(m.get("clicks") or 0); cv = float(m.get("conversions") or 0)
        tot["cost"] += cost; tot["conv"] += cv
        if c["id"] != LSA: tot["ppc_cost"] += cost; tot["ppc_conv"] += cv
        print(f"   {c['name'][:40]:<40} ${cost:>7,.0f} ${cost/6:>5.0f}/d clk {cl:>4} impr {int(m.get('impressions') or 0):>5} conv {cv:>4.1f} "
              f"CPL {('$%.0f' % (cost/cv)) if cv else '-':>5} CPC ${cost/cl if cl else 0:>5.2f} IS {m.get('search_impression_share','-')} rank {m.get('search_rank_lost_impression_share','-')} bud {m.get('search_budget_lost_impression_share','-')}")
    print(f"   TOTAL ${tot['cost']:,.0f} conv {tot['conv']:.1f} | PPC ex-LSA ${tot['ppc_cost']:,.0f} conv {tot['ppc_conv']:.1f}")

H("DAILY SPEND POST (NB / PMax / Branded / LSA)")
d = collections.defaultdict(dict)
for r in q("daily", f"SELECT segments.date, campaign.id, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign WHERE segments.date BETWEEN '2026-10-21' AND '2026-10-28'"):
    m = r["metrics"]; d[r["segments"]["date"]][r["campaign"]["id"]] = f"${M(m.get('cost_micros')):.0f}/{m.get('clicks',0)}c/{float(m.get('conversions') or 0):.0f}cv"
for k in sorted(d):
    print(f"  {k}  NB {d[k].get(NB,'-'):<14} PMax {d[k].get(PMAX,'-'):<14} BR {d[k].get(BR,'-'):<14} LSA {d[k].get(LSA,'-')}")

H("CONVERSIONS BY ACTION, POST")
for r in q("conv", f"""SELECT campaign.name, segments.conversion_action_name, metrics.conversions, metrics.all_conversions
  FROM campaign WHERE {W(POST)} AND metrics.all_conversions > 0"""):
    print(f"  {r['campaign']['name'][:40]:<40} {r['segments']['conversion_action_name'][:40]:<40} conv {float(r['metrics'].get('conversions') or 0):.1f} all {float(r['metrics'].get('all_conversions') or 0):.1f}")

H("NB KEYWORDS, POST")
for r in q("kw", f"""SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status,
  metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.average_cpc
  FROM keyword_view WHERE campaign.id = {NB} AND {W(POST)} AND metrics.impressions > 0 ORDER BY metrics.cost_micros DESC"""):
    k = r["ad_group_criterion"]; m = r["metrics"]
    print(f"  {k['keyword']['text'][:45]:<45} {k['keyword']['match_type']:<7} {k['status']:<8} ${M(m.get('cost_micros')):>6.0f} clk {m.get('clicks',0):>3} impr {m.get('impressions',0):>4} conv {float(m.get('conversions') or 0):.1f} cpc ${M(m.get('average_cpc')):.2f}")

for cid, nm in ((NB, "NONBRANDED"), (BR, "BRANDED")):
    H(f"{nm} SEARCH TERMS, POST")
    for r in q("st"+nm, f"""SELECT search_term_view.search_term, search_term_view.status, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
      FROM search_term_view WHERE campaign.id = {cid} AND {W(POST)} ORDER BY metrics.cost_micros DESC LIMIT 60"""):
        s = r["search_term_view"]; m = r["metrics"]
        print(f"  {s['search_term'][:50]:<50} {s.get('status','')[:8]:<8} ${M(m.get('cost_micros')):>6.2f} clk {m.get('clicks',0):>3} impr {m.get('impressions',0):>4} conv {float(m.get('conversions') or 0):.1f}")

H("PMAX SEARCH TERM CATEGORIES, POST")
for r in q("pmaxst", f"""SELECT campaign_search_term_insight.category_label, metrics.clicks, metrics.impressions, metrics.conversions
  FROM campaign_search_term_insight WHERE campaign_search_term_insight.campaign_id = '{PMAX}' AND {W(POST)} ORDER BY metrics.clicks DESC LIMIT 25"""):
    m = r["metrics"]
    print(f"  {r['campaign_search_term_insight'].get('category_label','(blank)')[:50]:<50} clk {m.get('clicks',0):>3} impr {m.get('impressions',0):>5} conv {float(m.get('conversions') or 0):.1f}")

H("PMAX CHANNEL SPLIT, POST")
for r in q("pmaxnet", f"""SELECT segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign
  WHERE campaign.id = {PMAX} AND {W(POST)}"""):
    m = r["metrics"]
    print(f"  {r['segments']['ad_network_type']:<15} ${M(m.get('cost_micros')):>6.0f} clk {m.get('clicks',0):>3} conv {float(m.get('conversions') or 0):.1f}")

H("CALLS FROM ADS 10-21..10-28")
for r in q("calls", """SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, call_view.caller_area_code, campaign.name
  FROM call_view WHERE call_view.start_call_date_time >= '2026-10-21 00:00:00' ORDER BY call_view.start_call_date_time"""):
    c = r["call_view"]
    print(f"  {c['start_call_date_time'][:16]} {r['campaign']['name'][:35]:<35} {c.get('call_status'):<9} {c.get('call_duration_seconds',0):>4}s area {c.get('caller_area_code','?')}")

H("LSA LEADS 10-21..10-28")
for r in q("lsa", """SELECT local_services_lead.creation_date_time, local_services_lead.lead_type, local_services_lead.lead_status,
  local_services_lead.lead_charged, local_services_lead.category_id FROM local_services_lead
  WHERE local_services_lead.creation_date_time >= '2026-10-21 00:00:00' ORDER BY local_services_lead.creation_date_time"""):
    l = r["local_services_lead"]
    print(f"  {l['creation_date_time'][:16]} {l.get('lead_type'):<9} {l.get('lead_status'):<10} charged={l.get('lead_charged')} {l.get('category_id','')}")
