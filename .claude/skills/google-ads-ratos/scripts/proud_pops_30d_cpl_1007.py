import sys, os
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import run_query
from collections import defaultdict
CID = "1051843378"
S, U = "2026-09-07", "2026-10-06"
f = lambda x: float(x or 0)

print("== Website lead conversion action settings")
for r in run_query(CID, """
SELECT conversion_action.name, conversion_action.counting_type, conversion_action.click_through_lookback_window_days,
       conversion_action.include_in_conversions_metric, conversion_action.attribution_model_settings.attribution_model,
       conversion_action.status, conversion_action.type
FROM conversion_action WHERE conversion_action.name IN ('Website lead', 'TSD - Website Call')"""):
    print("  ", r["conversion_action"])

camp = {}
for r in run_query(CID, f"""
SELECT campaign.name, campaign.advertising_channel_type, metrics.cost_micros, metrics.clicks, metrics.impressions,
       metrics.conversions, metrics.all_conversions,
       metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
FROM campaign WHERE segments.date BETWEEN '{S}' AND '{U}' AND metrics.cost_micros > 0"""):
    m = r["metrics"]
    camp[r["campaign"]["name"]] = dict(ch=str(r["campaign"]["advertising_channel_type"]), cost=f(m.get("cost_micros"))/1e6,
        clicks=f(m.get("clicks")), conv=f(m.get("conversions")), allc=f(m.get("all_conversions")),
        is_=m.get("search_impression_share"), bl=m.get("search_budget_lost_impression_share"), rl=m.get("search_rank_lost_impression_share"))

# forms by click date (all + counted) and by conversion date
forms_click = defaultdict(float); forms_counted = defaultdict(float); wcall = defaultdict(float)
for r in run_query(CID, f"""
SELECT campaign.name, segments.conversion_action_name, metrics.all_conversions, metrics.conversions
FROM campaign WHERE segments.date BETWEEN '{S}' AND '{U}'"""):
    a = r["segments"].get("conversion_action_name"); n = r["campaign"]["name"]
    if a == "Website lead":
        forms_click[n] += f(r["metrics"].get("all_conversions")); forms_counted[n] += f(r["metrics"].get("conversions"))
    if a == "TSD - Website Call":
        wcall[n] += f(r["metrics"].get("all_conversions"))
forms_cdate = defaultdict(float)
for r in run_query(CID, f"""
SELECT campaign.name, segments.conversion_action_name, metrics.all_conversions_by_conversion_date
FROM campaign WHERE segments.date BETWEEN '{S}' AND '{U}'"""):
    if r["segments"].get("conversion_action_name") == "Website lead":
        forms_cdate[r["campaign"]["name"]] += f(r["metrics"].get("all_conversions_by_conversion_date"))

# network split
net = defaultdict(lambda: defaultdict(float))
for r in run_query(CID, f"""
SELECT campaign.name, segments.ad_network_type, metrics.cost_micros, metrics.clicks
FROM campaign WHERE segments.date BETWEEN '{S}' AND '{U}' AND metrics.cost_micros > 0"""):
    n = r["campaign"]["name"]; t = str(r["segments"]["ad_network_type"])
    net[n][t + "_cost"] += f(r["metrics"].get("cost_micros"))/1e6
    net[n][t + "_clk"] += f(r["metrics"].get("clicks"))

print(f"\n== Per campaign {S}..{U}")
pct = lambda v: f"{f(v)*100:.1f}" if v is not None else "-"
T = defaultdict(float)
for n, d in sorted(camp.items(), key=lambda x: -x[1]["cost"]):
    fc, fd, fk = forms_click[n], forms_cdate[n], forms_counted[n]
    print(f"{n[:46]:46s} {d['ch'][:6]:6s} ${d['cost']:>9,.0f} clk {d['clicks']:>6.0f} cpc ${d['cost']/max(d['clicks'],1):6.2f} "
          f"forms(click) {fc:5.1f} forms(convdate) {fd:5.1f} counted {fk:5.1f} phoneClk {wcall[n]:6.1f} "
          f"$/form {('$'+format(d['cost']/fc, ',.0f')) if fc else '-':>7s} IS {pct(d['is_'])} BL {pct(d['bl'])} RL {pct(d['rl'])}")
    print(f"      network: " + "  ".join(f"{k}={v:,.0f}" for k, v in sorted(net[n].items())))
    b = "LSA" if d["ch"] == "LOCAL_SERVICES" else "YT" if d["ch"] == "VIDEO" else "BRAND" if n.startswith("TSD_05.13") else "NB_SEARCH" if d["ch"] == "SEARCH" else "PMAX"
    for k, v in (("cost", d["cost"]), ("clicks", d["clicks"]), ("forms", fc), ("formsC", fd), ("conv", d["conv"]), ("wcall", wcall[n])):
        T[b + "_" + k] += v
print("\nBUCKETS:")
for b in ("BRAND", "NB_SEARCH", "PMAX", "YT", "LSA"):
    c = T[b+"_cost"]; fo = T[b+"_forms"]
    if c:
        print(f"  {b:10s} cost ${c:,.0f} clicks {T[b+'_clicks']:.0f} cpc ${c/max(T[b+'_clicks'],1):.2f} forms {fo:.1f} (convdate {T[b+'_formsC']:.1f}) $/form {('$'+format(c/fo, ',.0f')) if fo else '-'} reportedConv {T[b+'_conv']:.1f} phoneClk {T[b+'_wcall']:.1f}")
lg = sum(T[b+"_cost"] for b in ("BRAND", "NB_SEARCH", "PMAX")); lf = sum(T[b+"_forms"] for b in ("BRAND", "NB_SEARCH", "PMAX"))
lfc = sum(T[b+"_formsC"] for b in ("BRAND", "NB_SEARCH", "PMAX")); lconv = sum(T[b+"_conv"] for b in ("BRAND", "NB_SEARCH", "PMAX"))
lclk = sum(T[b+"_clicks"] for b in ("BRAND", "NB_SEARCH", "PMAX")); lw = sum(T[b+"_wcall"] for b in ("BRAND", "NB_SEARCH", "PMAX"))
print(f"  LEADGEN   cost ${lg:,.0f} clicks {lclk:.0f} forms {lf:.1f} (convdate {lfc:.1f}) $/form ${lg/lf:,.0f} (convdate ${lg/lfc:,.0f}) reportedConv {lconv:.1f} reportedCPL ${lg/lconv:.2f} phoneClk {lw:.1f} ({lw/lconv*100:.0f}% of reported)")
print(f"  NB_SEARCH share of leadgen spend: {T['NB_SEARCH_cost']/lg*100:.1f}%")
unb_c = T["NB_SEARCH_cost"] + T["PMAX_cost"]; unb_f = T["NB_SEARCH_forms"] + T["PMAX_forms"]
print(f"  UNBRANDED (NB search + PMax) cost ${unb_c:,.0f} forms {unb_f:.1f} $/form ${unb_c/unb_f:,.0f}")

for r in run_query(CID, f"""
SELECT metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
FROM customer WHERE segments.date BETWEEN '{S}' AND '{U}'"""):
    print("  ACCOUNT search IS:", {k: round(f(v)*100, 1) for k, v in r["metrics"].items()})

print("\n== Pre-ramp baseline check (lead-gen excl YT/LSA)")
for s, u in (("2026-07-23", "2026-07-30"), ("2026-08-03", "2026-08-09"), ("2026-08-10", "2026-08-16")):
    cost = 0.0; fo = 0.0
    for r in run_query(CID, f"""
SELECT campaign.name, campaign.advertising_channel_type, metrics.cost_micros FROM campaign
WHERE segments.date BETWEEN '{s}' AND '{u}' AND metrics.cost_micros > 0"""):
        if str(r["campaign"]["advertising_channel_type"]) in ("SEARCH", "PERFORMANCE_MAX"):
            cost += f(r["metrics"].get("cost_micros"))/1e6
    for r in run_query(CID, f"""
SELECT campaign.name, campaign.advertising_channel_type, segments.conversion_action_name, metrics.all_conversions FROM campaign
WHERE segments.date BETWEEN '{s}' AND '{u}'"""):
        if r["segments"].get("conversion_action_name") == "Website lead" and str(r["campaign"]["advertising_channel_type"]) in ("SEARCH", "PERFORMANCE_MAX"):
            fo += f(r["metrics"].get("all_conversions"))
    print(f"  {s}..{u}: spend ${cost:,.0f} ({cost/((int(u[-2:])-int(s[-2:]))+1):,.0f}/d) forms {fo:.0f} $/form ${cost/fo if fo else 0:,.0f}")
