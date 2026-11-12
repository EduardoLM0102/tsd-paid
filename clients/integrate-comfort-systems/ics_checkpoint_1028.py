# READ-ONLY checkpoint on the 10-08 changes, Integrate Comfort main Google Ads 4571881760 (fu-012)
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>
import os, sys, collections
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import run_query
import callrail
CID = "4571881760"
PMAX, NB, BR = "22890783804", "24047025253", "23675636592"
NAMES = {PMAX: "PMax", NB: "NonBranded", BR: "Branded"}
PRE = ("2026-09-20", "2026-10-07")   # 18 days before the 10-08 apply
POST = ("2026-10-09", "2026-10-26")  # 18 days after (same weekday mix)
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

H("SETTINGS READ-BACK (enabled)")
for r in q("camps", """SELECT campaign.id, campaign.name, campaign.primary_status, campaign.primary_status_reasons, campaign.bidding_strategy_type,
  campaign.target_impression_share.cpc_bid_ceiling_micros, campaign.maximize_conversions.target_cpa_micros, campaign_budget.amount_micros
  FROM campaign WHERE campaign.status = 'ENABLED'"""):
    c = r["campaign"]
    print(f"- {c['name']} [{c['id']}] {c.get('primary_status')} {c.get('primary_status_reasons','')} {c.get('bidding_strategy_type')} "
          f"budget ${M(r['campaign_budget'].get('amount_micros')):.2f} tIS cap {M((c.get('target_impression_share') or {}).get('cpc_bid_ceiling_micros'))}")

H("CHANGES SINCE 10-08")
for r in q("chg", """SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type, change_event.resource_change_operation,
  change_event.changed_fields, campaign.name FROM change_event WHERE change_event.change_date_time BETWEEN '2026-10-08 00:00:00' AND '2026-10-28 23:59:59'
  ORDER BY change_event.change_date_time LIMIT 300"""):
    e = r["change_event"]
    print(f"  {e['change_date_time'][:16]} {e.get('user_email','?'):<32} {e.get('change_resource_type'):<20} {e.get('resource_change_operation'):<7} {r.get('campaign',{}).get('name','')[:35]} {str(e.get('changed_fields',''))[:70]}")

H(f"CAMPAIGNS PRE {PRE} vs POST {POST}")
for lab, rng in (("PRE", PRE), ("POST", POST)):
    print(f"-- {lab}")
    for r in q(lab, f"""SELECT campaign.id, campaign.name, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions,
      metrics.search_impression_share, metrics.search_rank_lost_impression_share, metrics.search_budget_lost_impression_share
      FROM campaign WHERE {W(rng)} AND metrics.impressions > 0"""):
        c = r["campaign"]; m = r["metrics"]; cost = M(m.get("cost_micros")); cl = int(m.get("clicks") or 0)
        print(f"   {c['name'][:40]:<40} ${cost:>7,.0f} clk {cl:>4} conv {float(m.get('conversions') or 0):>5.1f} all {float(m.get('all_conversions') or 0):>5.1f} "
              f"CPC ${cost/cl if cl else 0:>5.2f} IS {m.get('search_impression_share','-')} rank {m.get('search_rank_lost_impression_share','-')} bud {m.get('search_budget_lost_impression_share','-')}")

H("PRIMARY CONVERSIONS BY ACTION + click key (dedupe ghl_* pairs)")
for lab, rng in (("PRE", PRE), ("POST", POST)):
    rows = q("conv"+lab, f"""SELECT campaign.id, ad_group.id, segments.date, segments.hour, segments.device, segments.conversion_action_name, metrics.conversions
      FROM ad_group WHERE {W(rng)} AND metrics.conversions > 0""")
    pm = q("convpm"+lab, f"""SELECT campaign.id, segments.date, segments.hour, segments.device, segments.conversion_action_name, metrics.conversions
      FROM campaign WHERE campaign.id = {PMAX} AND {W(rng)} AND metrics.conversions > 0""")
    keys = collections.defaultdict(list)
    for r in rows + pm:
        s = r["segments"]; k = (r["campaign"]["id"], r.get("ad_group", {}).get("id", "pmax"), s["date"], s.get("hour"), s.get("device"))
        keys[k].append((s["conversion_action_name"], float(r["metrics"]["conversions"])))
    tot = collections.Counter(); real = collections.Counter(); byact = collections.Counter()
    for k, acts in keys.items():
        camp = NAMES.get(k[0], k[0]); n = sum(v for _, v in acts); tot[camp] += n
        for a, v in acts: byact[(camp, a)] += v
        ghl = sum(v for a, v in acts if "ghl_" in a.lower()); other = n - ghl
        real[camp] += other if (ghl and other) else n   # drop ghl_* when the GTM/Ads form shares the same click key
    print(f"-- {lab}: reported {dict(tot)} | deduped {dict(real)}")
    for (camp, a), v in sorted(byact.items()):
        print(f"     {camp:<11} {a[:55]:<55} {v:.1f}")

H("CALLS FROM ADS (call_view) PRE vs POST, by campaign, >=60s")
for lab, rng in (("PRE", PRE), ("POST", POST)):
    c = collections.Counter(); c60 = collections.Counter()
    for r in q("calls"+lab, f"""SELECT call_view.start_call_date_time, call_view.call_duration_seconds, call_view.call_status, campaign.id FROM call_view
      WHERE call_view.start_call_date_time BETWEEN '{rng[0]} 00:00:00' AND '{rng[1]} 23:59:59'"""):
        k = NAMES.get(r["campaign"]["id"], r["campaign"]["id"]); c[k] += 1
        if int(r["call_view"].get("call_duration_seconds") or 0) >= 60: c60[k] += 1
    print(f"  {lab}: all {dict(c)} | >=60s {dict(c60)}")

H("PMAX CHANNEL SPLIT PRE vs POST")
for lab, rng in (("PRE", PRE), ("POST", POST)):
    for r in q("net"+lab, f"SELECT segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign WHERE campaign.id = {PMAX} AND {W(rng)}"):
        m = r["metrics"]; print(f"  {lab} {r['segments']['ad_network_type']:<15} ${M(m.get('cost_micros')):>7.0f} clk {m.get('clicks',0):>4} conv {float(m.get('conversions') or 0):.1f}")

H("NB AD GROUPS POST")
for r in q("ag", f"""SELECT ad_group.name, ad_group.status, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions FROM ad_group
  WHERE campaign.id = {NB} AND {W(POST)}"""):
    m = r["metrics"]; print(f"  {r['ad_group']['name'][:40]:<40} {r['ad_group']['status']:<8} ${M(m.get('cost_micros')):>6.0f} clk {m.get('clicks',0):>3} impr {m.get('impressions',0):>5} conv {float(m.get('conversions') or 0):.1f}")

H("NB SEARCH TERMS POST")
for r in q("st", f"""SELECT search_term_view.search_term, search_term_view.status, metrics.cost_micros, metrics.clicks, metrics.conversions FROM search_term_view
  WHERE campaign.id = {NB} AND {W(POST)} AND metrics.clicks > 0 ORDER BY metrics.cost_micros DESC LIMIT 50"""):
    m = r["metrics"]; print(f"  {r['search_term_view']['search_term'][:50]:<50} ${M(m.get('cost_micros')):>6.2f} clk {m.get('clicks',0):>3} conv {float(m.get('conversions') or 0):.1f}")

H("PMAX SEARCH CATEGORIES POST")
for r in q("pst", f"""SELECT campaign_search_term_insight.category_label, metrics.clicks, metrics.conversions FROM campaign_search_term_insight
  WHERE campaign_search_term_insight.campaign_id = '{PMAX}' AND {W(POST)} ORDER BY metrics.clicks DESC LIMIT 25"""):
    m = r["metrics"]; print(f"  {r['campaign_search_term_insight'].get('category_label','(blank)')[:50]:<50} clk {m.get('clicks',0):>3} conv {float(m.get('conversions') or 0):.1f}")

H("CALLRAIL: calls 09-20..10-27 by source (ICS)")
try:
    calls = callrail.get_all("/calls.json", "calls", company_id="COM742d39e3ff5d406db1000a4df1c02980", start_date=PRE[0], end_date="2026-10-27",
                             fields="source,gclid,duration,landing_page_url,campaign,first_call")
    agg = collections.Counter()
    for c in calls:
        per = "PRE" if c["start_time"][:10] <= PRE[1] else ("POST" if c["start_time"][:10] >= POST[0] else "chg")
        src = c.get("source") or "?"; g = "gclid" if c.get("gclid") else "-"
        lp = (c.get("landing_page_url") or "")[:60]
        agg[(per, src, g, int(c.get("duration") or 0) >= 60)] += 1
        if c.get("gclid") or "google ads" in src.lower():
            print(f"  {c['start_time'][:16]} {src[:25]:<25} {g:<5} {c.get('duration')}s first={c.get('first_call')} {lp}")
    for k, v in sorted(agg.items()):
        print("  ", k, v)
except Exception as e:
    print("  !! callrail:", str(e)[:200])
