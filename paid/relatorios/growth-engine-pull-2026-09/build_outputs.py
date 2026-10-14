#!/usr/bin/env python3
"""
Builds the Growth Engine deliverable CSVs from raw/ (Meta connector pulls + Google Ads API pulls)
and client_roster.csv (which accounts belong to current TSD clients, and since when TSD runs them).

Window: 52 full Mon-Sun weeks, 2025-09-29 .. 2026-09-27, each account's own time zone, USD.
Revision 2026-10-07: roster changes (Integrate's ICS account added, On The Way offboarding), Cool Hand campaign
split, and 08 (awareness placements + optimization goal, pulled 2026-10-07 for the same window).

Scope rule, same on both platforms:
  - Headline numbers use only accounts whose roster status is "current".
  - Frequency numbers also drop weeks before the account's tsd_managed_since date (campaigns run by
    someone else before TSD took over). CPM keeps those weeks: it's a market price either way.
  - "all accounts" columns (reference only) include former and unconfirmed clients, never TopServ's
    own ad accounts.

Run:  python3 build_outputs.py
"""

import csv
import glob
import json
import os
import statistics
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
GRAW = os.path.join(RAW, "google")
LAST4_SINCE = "2026-08-31"   # last 4 weeks of the window
FLOOR = 3.0                  # weekly frequency floor under test
BRAND_MIN_SPEND = 500        # 12-month spend below this doesn't count as a market having a brand CPM

QUARTERS = [("Q4-2025", "2025-09-29", "2025-12-28"), ("Q1-2026", "2025-12-29", "2026-03-29"),
            ("Q2-2026", "2026-03-30", "2026-06-28"), ("Q3-2026", "2026-06-29", "2026-09-27")]

# Meta ad account -> market. The client's primary Nielsen DMA, taken from its Google Ads metro delivery
# (google_metro_12mo.csv) or the client folder when it has no Google account. Meta's own geo breakdown
# is not in this pull.
META_MARKET = {
    "381256660973192": "Atlanta, GA",
    "588638883283311": "Tulsa, OK",
    "1434273655098937": "Cincinnati, OH",
    "1846637992293356": "Minneapolis-St. Paul, MN",
    "438790276573563": "Tyler-Longview(Lufkin & Nacogdoches), TX",
    "79203382": "Phoenix, AZ",
    "1664197513868366": "Los Angeles, CA",
    "483679897962388": "Dallas-Ft. Worth, TX",
    "1845825982372184": "Dallas-Ft. Worth, TX",
    "2405306059725517": "New York, NY",
    "705877631084699": "Dallas-Ft. Worth, TX",
    "532145676808452": "unknown",
    "10086442468052740": "Dallas-Ft. Worth, TX",
    "2014320269203822": "Cincinnati, OH",
    "710350517676765": "New Orleans, LA",
    "1517373248873821": "Dallas-Ft. Worth, TX",
    "170464733924961": "unknown",
    "2070047533283360": "New York, NY",   # ICS = Integrate Comfort; connector can't read it
    "849885463684603": "unknown",         # Rhino; Oklahoma per Alex's region data, client unconfirmed
    "871958544802411": "unknown",         # Your New Door; no delivery
}

# Gillespie's ad sets became unreadable before the 10-07 pull, so its one awareness campaign keeps the
# goal its name states. Every other "- Ad Recall Lift" campaign in the book verified as AD_RECALL_LIFT.
GOAL_FROM_NAME = {"7000989212234": "AD_RECALL_LIFT"}

META_GROUP = {
    "OUTCOME_AWARENESS": "Awareness / Reach", "REACH": "Awareness / Reach", "BRAND_AWARENESS": "Awareness / Reach",
    "OUTCOME_TRAFFIC": "Traffic", "LINK_CLICKS": "Traffic",
    "OUTCOME_ENGAGEMENT": "Engagement", "POST_ENGAGEMENT": "Engagement",
    "OUTCOME_LEADS": "Leads / Conversions / Sales", "LEAD_GENERATION": "Leads / Conversions / Sales",
    "OUTCOME_SALES": "Leads / Conversions / Sales", "CONVERSIONS": "Leads / Conversions / Sales",
}
RECRUIT_WORDS = ("hiring", "job_", "journeyman", "technicians", "recruit")

GOOGLE_PRICING = {
    "VIDEO": "impression-priced (CPM/CPV): valid brand CPM",
    "DEMAND_GEN": "impression-priced: valid brand CPM",
    "DISPLAY": "impression-priced: valid brand CPM",
    "PERFORMANCE_MAX": "mixed: YouTube/Display networks are impression inventory, Search network is click-priced",
    "SEARCH": "click-priced: CPM is an artifact, not a brand price",
    "SMART": "click-priced: CPM is an artifact, not a brand price",
    "LOCAL_SERVICES": "lead-priced (LSA): CPM is an artifact, not a brand price",
}
# Google ad networks grouped the way the brand layer cares about them
NET_BUCKET = {"YOUTUBE": "youtube",
              "CONTENT": "display", "DISCOVER": "display", "GMAIL": "display",
              "GOOGLE_OWNED_CHANNELS": "display", "MIXED": "display",
              "SEARCH": "search", "SEARCH_PARTNERS": "search", "MAPS": "search"}
YT_LABEL = {"INSTREAM_SKIPPABLE": "In-stream (skippable)", "INFEED": "In-feed", "SHORTS": "Shorts",
            "UNKNOWN": "Not attributed by Google", "INSTREAM_NON_SKIPPABLE": "In-stream (non-skippable)",
            "BUMPER": "Bumper"}


def load(*parts):
    with open(os.path.join(*parts)) as f:
        return list(csv.DictReader(f))


def cpm(spend, impr):
    return round(spend / impr * 1000, 2) if impr else ""


def pct(a, b):
    return f"{a / b * 100:.1f}%" if b else ""


def w(name, header, rows):
    with open(os.path.join(HERE, name), "w", newline="") as f:
        cw = csv.writer(f)
        cw.writerow(header)
        cw.writerows(rows)
    print(f"{len(rows):>5} rows  {name}")


def quarter(week_start):
    for q, a, b in QUARTERS:
        if a <= week_start <= b:
            return q
    return ""


def purpose(name):
    n = name.lower()
    return "recruiting" if any(k in n for k in RECRUIT_WORDS) or "now hiring" in n else "customer-facing"


def audience_note(name):
    n = name.lower()
    if "remarketing" in n or "retargeting" in n:
        return "retargeting"
    if "lookalike" in n:
        return "lookalike"
    return ""


def yn(b):
    return "yes" if b else "no"


# ----------------------------------------------------------------------------- roster
ROSTER = {(r["platform"], r["account_id"]): r for r in load(HERE, "client_roster.csv")}


def status(p, a):
    return ROSTER[(p, a)]["status"]


def current(p, a):
    return status(p, a) == "current"


def since(p, a):
    return ROSTER[(p, a)]["tsd_managed_since"]


def managed(p, a, week_start):
    """Counts toward 'what TSD delivers': a current client, in a week that starts after TSD took over."""
    s = since(p, a)
    return current(p, a) and (not s or week_start >= s)


def client(p, a):
    c = ROSTER[(p, a)]["client"]
    return f"{c} [{a}]" if c == "unknown" or c.startswith("UNCONFIRMED") else c


# ----------------------------------------------------------------------------- raw data
meta_weekly = load(RAW, "meta_weekly_account.csv")
meta_aw_weekly = load(RAW, "meta_awareness_campaign_weekly.csv")
meta_device = load(RAW, "meta_device_12mo.csv")
meta_camps = []
for f in sorted(glob.glob(os.path.join(RAW, "meta_campaign_12mo", "*.json"))):
    acct = os.path.basename(f).split(".")[0].split("_")[0]
    for x in json.load(open(f)):
        meta_camps.append({
            "account_id": acct, "campaign_id": x["id"], "campaign": x["name"],
            "objective": x["objective"], "status": x["effective_status"],
            "spend": float(x["amount_spent"]["value"]), "impressions": int(x["impressions"]),
            "reach": int(x["reach"]), "frequency": float(x["frequency"]),
        })
camp_name = {c["campaign_id"]: c["campaign"] for c in meta_camps}

g_camp = load(GRAW, "google_campaign_12mo.csv")
g_week = load(GRAW, "google_weekly_by_channel.csv")
g_wnet = load(GRAW, "google_weekly_by_network.csv")
g_net = load(GRAW, "google_network_12mo.csv")
g_dev = load(GRAW, "google_device_12mo.csv")
g_metro = load(GRAW, "google_metro_12mo.csv")
g_fmt = load(GRAW, "google_youtube_format_12mo.csv")
g_vfreq = load(GRAW, "google_video_weekly_frequency.csv")

# every account with data must be on the roster
seen = {("Meta", r["account_id"]) for r in meta_weekly} | {("Google", r["customer_id"]) for r in g_camp}
missing = sorted(seen - set(ROSTER))
if missing:
    raise SystemExit(f"accounts missing from client_roster.csv: {missing}")

# TopServ's own accounts never enter any number
meta_weekly = [r for r in meta_weekly if status("Meta", r["account_id"]) != "internal"]
meta_aw_weekly = [r for r in meta_aw_weekly if status("Meta", r["account_id"]) != "internal"]
meta_camps = [c for c in meta_camps if status("Meta", c["account_id"]) != "internal"]
meta_device = [r for r in meta_device if status("Meta", r["account_id"]) != "internal"]
g_camp, g_week, g_wnet, g_net, g_dev, g_metro, g_fmt, g_vfreq = (
    [r for r in rows if status("Google", r["customer_id"]) != "internal"]
    for rows in (g_camp, g_week, g_wnet, g_net, g_dev, g_metro, g_fmt, g_vfreq))

g_name = {r["customer_id"]: r["account"].replace("\xa0", " ") for r in g_camp}
meta_last4 = {r["account_id"] for r in meta_weekly if r["week_start"] >= LAST4_SINCE and float(r["spend_usd"]) > 0}
g_last4 = {r["customer_id"] for r in g_week if r["week_start"] >= LAST4_SINCE and float(r["spend_usd"]) > 0}

# primary DMA per Google account, and per client (by Google spend; Meta-only clients use META_MARKET)
_acct_dma = defaultdict(lambda: defaultdict(float))
_client_dma = defaultdict(lambda: defaultdict(float))
for r in g_metro:
    if r["metro_name"]:
        _acct_dma[r["customer_id"]][r["metro_name"]] += float(r["spend_usd"])
        _client_dma[client("Google", r["customer_id"])][r["metro_name"]] += float(r["spend_usd"])
g_dma = {k: max(v.items(), key=lambda x: x[1])[0] for k, v in _acct_dma.items() if sum(v.values()) > 0}
client_market = {k: max(v.items(), key=lambda x: x[1])[0] for k, v in _client_dma.items() if sum(v.values()) > 0}
for aid, mk in META_MARKET.items():
    c = client("Meta", aid)
    if c in client_market and client_market[c] != mk and mk != "unknown":
        print(f"  note: {c} Meta market {mk} differs from Google-derived {client_market[c]}")
    client_market.setdefault(c, mk)

# ============================================================================ 00 account registry
meta_spend = defaultdict(float)
for r in meta_weekly:
    meta_spend[r["account_id"]] += float(r["spend_usd"])
g_spend = defaultdict(float)
for r in g_camp:
    g_spend[r["customer_id"]] += float(r["spend_usd"])
rows = []
for (p, a), r in ROSTER.items():
    sp = meta_spend.get(a, 0.0) if p == "Meta" else g_spend.get(a, 0.0)
    mk = META_MARKET.get(a, "") if p == "Meta" else g_dma.get(a, "")
    last4 = (a in meta_last4) if p == "Meta" else (a in g_last4)
    rows.append([p, a, r["account_name"], r["client"], r["status"], r["tsd_managed_since"],
                 yn(r["status"] == "current"), mk, yn(last4), round(sp, 2), r["evidence"]])
rows.sort(key=lambda x: (x[0], x[4] != "current", -x[9]))
w("00_account_registry.csv",
  ["platform", "account_id", "account_name", "client", "roster_status", "tsd_managed_since",
   "in_headline_numbers", "primary_market_dma", "spent_last_4_weeks", "spend_usd_12mo", "evidence"], rows)

# ============================================================================ 01 CPM by platform x objective
agg = defaultdict(lambda: {"s": 0.0, "i": 0, "c": 0, "a": set(), "S": 0.0, "I": 0})
for c in meta_camps:
    a = agg[("Meta", META_GROUP.get(c["objective"], c["objective"]), purpose(c["campaign"]))]
    a["S"] += c["spend"]; a["I"] += c["impressions"]
    if current("Meta", c["account_id"]):
        a["s"] += c["spend"]; a["i"] += c["impressions"]; a["c"] += 1; a["a"].add(c["account_id"])
for r in g_camp:
    a = agg[("Google", r["channel_type"], "customer-facing")]
    s, i = float(r["spend_usd"]), int(r["impressions"])
    a["S"] += s; a["I"] += i
    if current("Google", r["customer_id"]):
        a["s"] += s; a["i"] += i; a["c"] += 1; a["a"].add(r["customer_id"])
for r in g_net:
    if r["channel_type"] != "PERFORMANCE_MAX":
        continue
    a = agg[("Google", f"PERFORMANCE_MAX > {r['ad_network_type']} network", "customer-facing")]
    s, i = float(r["spend_usd"]), int(r["impressions"])
    a["S"] += s; a["I"] += i
    if current("Google", r["customer_id"]):
        a["s"] += s; a["i"] += i; a["a"].add(r["customer_id"])
rows = []
for (plat, grp, purp), a in sorted(agg.items(), key=lambda x: (x[0][0], ">" in x[0][1], x[0][2], -x[1]["s"])):
    if plat == "Google":
        note = ("PMax delivery on this network only (sub-row of PERFORMANCE_MAX)" if ">" in grp
                else GOOGLE_PRICING.get(grp, ""))
    else:
        note = ("impression-priced reach/recall buying: valid brand CPM" if grp == "Awareness / Reach"
                else "auction optimized for a downstream action: CPM runs higher by design")
    rows.append([plat, grp, purp, note, len(a["a"]), a["c"] if ">" not in grp else "",
                 round(a["s"], 2), a["i"], cpm(a["s"], a["i"]), round(a["S"], 2), a["I"], cpm(a["S"], a["I"])])
w("01_cpm_by_platform_and_objective.csv",
  ["platform", "objective_or_channel", "purpose", "pricing_note", "accounts_current_clients",
   "campaigns_current_clients", "spend_usd_current_clients", "impressions_current_clients",
   "cpm_usd_current_clients", "spend_usd_all_accounts", "impressions_all_accounts", "cpm_usd_all_accounts"], rows)

# 01b per-campaign detail, both platforms
rows = []
for c in meta_camps:
    a = c["account_id"]
    rows.append(["Meta", a, client("Meta", a), status("Meta", a), yn(current("Meta", a)), since("Meta", a),
                 META_MARKET.get(a, ""), yn(a in meta_last4), c["campaign_id"], c["campaign"], c["objective"],
                 META_GROUP.get(c["objective"], ""), purpose(c["campaign"]), audience_note(c["campaign"]),
                 c["status"], round(c["spend"], 2), c["impressions"], c["reach"], c["frequency"],
                 cpm(c["spend"], c["impressions"])])
for r in g_camp:
    a = r["customer_id"]
    rows.append(["Google", a, client("Google", a), status("Google", a), yn(current("Google", a)),
                 since("Google", a), g_dma.get(a, ""), yn(a in g_last4), r["campaign_id"], r["campaign"],
                 r["channel_type"], r["channel_sub_type"], purpose(r["campaign"]), "", r["status"],
                 r["spend_usd"], r["impressions"], "", "", cpm(float(r["spend_usd"]), int(r["impressions"]))])
w("01b_campaign_detail_both_platforms.csv",
  ["platform", "account_id", "client", "roster_status", "in_headline_numbers", "tsd_managed_since",
   "market_dma", "account_spent_last_4_weeks", "campaign_id", "campaign", "objective_or_channel",
   "objective_group_or_subtype", "purpose", "audience_note", "campaign_status", "spend_usd_12mo",
   "impressions_12mo", "reach_12mo_dedup", "frequency_12mo", "cpm_usd"], rows)

# ============================================================================ 02 CPM by market
GROUPS = {"VIDEO": "YouTube/Display/Demand Gen (impression-priced)",
          "DEMAND_GEN": "YouTube/Display/Demand Gen (impression-priced)",
          "DISPLAY": "YouTube/Display/Demand Gen (impression-priced)",
          "PERFORMANCE_MAX": "Performance Max (mixed)",
          "SEARCH": "Search + Smart (click-priced)", "SMART": "Search + Smart (click-priced)",
          "LOCAL_SERVICES": "Local Services Ads (lead-priced)"}
# 02a Google by DMA, current clients
dm = defaultdict(lambda: [0.0, 0, set()])
for r in g_metro:
    if not current("Google", r["customer_id"]):
        continue
    k = (r["metro_name"] or "(location not reported)", GROUPS.get(r["channel_type"], r["channel_type"]))
    dm[k][0] += float(r["spend_usd"]); dm[k][1] += int(r["impressions"]); dm[k][2].add(client("Google", r["customer_id"]))
rows = [[m, g, len(c), round(s, 2), i, cpm(s, i)] for (m, g), (s, i, c) in dm.items() if s >= 1]
rows.sort(key=lambda x: -x[3])
w("02a_google_cpm_by_dma.csv",
  ["dma_google_metro", "channel_group", "current_clients_delivering", "spend_usd_12mo", "impressions_12mo", "cpm_usd"], rows)

# 02b Meta by client market x objective group (customer-facing campaigns), every client, status shown
mm = defaultdict(lambda: [0.0, 0])
for c in meta_camps:
    if purpose(c["campaign"]) != "customer-facing":
        continue
    a = c["account_id"]
    k = (META_MARKET.get(a, "unknown"), client("Meta", a), status("Meta", a), META_GROUP.get(c["objective"], c["objective"]))
    mm[k][0] += c["spend"]; mm[k][1] += c["impressions"]
rows = [[mk, cl, st, yn(st == "current"), g, round(s, 2), i, cpm(s, i)] for (mk, cl, st, g), (s, i) in sorted(mm.items())]
w("02b_meta_cpm_by_client_market.csv",
  ["market_dma_assigned", "client", "roster_status", "in_headline_numbers", "objective_group",
   "spend_usd_12mo", "impressions_12mo", "cpm_usd"], rows)

# 02c one row per DMA, brand-relevant CPMs side by side, current clients
side = defaultdict(lambda: defaultdict(lambda: [0.0, 0]))
for c in meta_camps:
    a = c["account_id"]
    if not current("Meta", a) or purpose(c["campaign"]) != "customer-facing":
        continue
    g = "meta_awareness" if META_GROUP.get(c["objective"]) == "Awareness / Reach" else "meta_other"
    side[META_MARKET[a]][g][0] += c["spend"]; side[META_MARKET[a]][g][1] += c["impressions"]
for r in g_metro:
    if not current("Google", r["customer_id"]) or not r["metro_name"]:
        continue
    g = {"VIDEO": "g_video", "DEMAND_GEN": "g_video", "DISPLAY": "g_display",
         "PERFORMANCE_MAX": "g_pmax"}.get(r["channel_type"])
    if g:
        side[r["metro_name"]][g][0] += float(r["spend_usd"]); side[r["metro_name"]][g][1] += int(r["impressions"])
rows = []
for mk, d in side.items():
    row = [mk]
    for g in ("meta_awareness", "meta_other", "g_video", "g_display", "g_pmax"):
        s, i = d[g]
        row += [round(s, 2) if s else "", cpm(s, i) if s >= 50 else ""]
    if sum(v for v in row[1::2] if isinstance(v, float)) >= BRAND_MIN_SPEND:  # drop geo leakage
        rows.append(row)
rows.sort(key=lambda x: -sum(v for v in x[1::2] if isinstance(v, float)))
w("02c_market_summary_brand_cpms.csv",
  ["dma", "meta_awareness_spend", "meta_awareness_cpm", "meta_leads_traffic_eng_spend", "meta_leads_traffic_eng_cpm",
   "google_youtube_demandgen_spend", "google_youtube_demandgen_cpm", "google_display_spend", "google_display_cpm",
   "google_pmax_spend", "google_pmax_cpm"], rows)

# 02d market coverage: every market where a current client spent money, and whether it has a delivered brand CPM
cur_clients = defaultdict(float)
for (p, a), r in ROSTER.items():
    if r["status"] == "current":
        cur_clients[client(p, a)] += meta_spend.get(a, 0.0) if p == "Meta" else g_spend.get(a, 0.0)
markets = defaultdict(set)
for cl, sp in cur_clients.items():
    if sp > 0 and client_market.get(cl, "unknown") != "unknown":
        markets[client_market[cl]].add(cl)
cov = defaultdict(lambda: defaultdict(lambda: [0.0, 0]))
for c in meta_camps:
    a = c["account_id"]
    if current("Meta", a) and purpose(c["campaign"]) == "customer-facing" and META_GROUP.get(c["objective"]) == "Awareness / Reach":
        cov[META_MARKET[a]]["meta_aw"][0] += c["spend"]; cov[META_MARKET[a]]["meta_aw"][1] += c["impressions"]
for r in g_metro:
    if current("Google", r["customer_id"]) and r["channel_type"] in ("VIDEO", "DEMAND_GEN") and r["metro_name"]:
        cov[r["metro_name"]]["yt"][0] += float(r["spend_usd"]); cov[r["metro_name"]]["yt"][1] += int(r["impressions"])
for r in g_net:
    if current("Google", r["customer_id"]) and r["channel_type"] == "PERFORMANCE_MAX" and r["ad_network_type"] == "YOUTUBE":
        mk = client_market.get(client("Google", r["customer_id"]))
        if mk:
            cov[mk]["pmax_yt"][0] += float(r["spend_usd"]); cov[mk]["pmax_yt"][1] += int(r["impressions"])
meta_pulled = {r["account_id"] for r in meta_weekly}
rows = []
for mk, cls in markets.items():
    ma, yt, px = cov[mk]["meta_aw"], cov[mk]["yt"], cov[mk]["pmax_yt"]
    has_meta, has_yt = ma[0] >= BRAND_MIN_SPEND, yt[0] >= BRAND_MIN_SPEND
    if has_meta and has_yt:
        verdict = "yes: Meta awareness and YouTube"
    elif has_meta:
        verdict = "yes: Meta awareness only"
    elif has_yt:
        verdict = "yes: YouTube only"
    elif ma[0] or yt[0]:
        verdict = f"too thin to price (under ${BRAND_MIN_SPEND} of brand spend in 12 months)"
    elif px[0] >= BRAND_MIN_SPEND:
        verdict = "no dedicated brand campaign (only YouTube that PMax bought)"
    else:
        verdict = "no brand-layer delivery at all"
    notes = []
    for (p, a), r in ROSTER.items():
        if r["status"] != "current" or client(p, a) not in cls:
            continue
        if p == "Meta" and a not in meta_pulled:
            notes.append(f"{client(p, a)}: Meta account not in this pull")
        if p == "Google" and r["tsd_managed_since"] and any(
                x["customer_id"] == a and x["channel_type"] in ("VIDEO", "DEMAND_GEN") for x in g_camp):
            notes.append(f"{client(p, a)}: its YouTube ran before TSD took over ({r['tsd_managed_since']}); "
                         "counts for CPM, not for frequency")
    rows.append([mk, "; ".join(sorted(cls)), verdict,
                 round(ma[0], 2) if ma[0] else "", cpm(ma[0], ma[1]) if has_meta else "",
                 round(yt[0], 2) if yt[0] else "", cpm(yt[0], yt[1]) if has_yt else "",
                 round(px[0], 2) if px[0] else "", px[1] or "", cpm(px[0], px[1]) if px[0] >= BRAND_MIN_SPEND else "",
                 " | ".join(notes)])
rows.sort(key=lambda x: (not x[2].startswith("yes"), x[0]))
w("02d_market_coverage.csv",
  ["market_dma", "current_clients", "delivered_brand_cpm_available", "meta_awareness_spend_12mo",
   "meta_awareness_cpm", "standalone_youtube_spend_12mo", "standalone_youtube_cpm", "pmax_youtube_spend_12mo",
   "pmax_youtube_impressions_12mo", "pmax_youtube_cpm", "notes"], rows)

# ============================================================================ 03 YouTube by format
fm = defaultdict(lambda: [0.0, 0, set(), 0.0, 0])
for r in g_fmt:
    if r["channel_type"] == "PERFORMANCE_MAX":
        continue
    lab = YT_LABEL.get(r["ad_format_type"], r["ad_format_type"])
    for k in ((r["channel_type"], lab), ("VIDEO + DEMAND_GEN combined", lab)):
        x = fm[k]
        x[3] += float(r["spend_usd"]); x[4] += int(r["impressions"])
        if current("Google", r["customer_id"]):
            x[0] += float(r["spend_usd"]); x[1] += int(r["impressions"]); x[2].add(r["customer_id"])
for r in g_net:
    if r["channel_type"] == "PERFORMANCE_MAX" and r["ad_network_type"] == "YOUTUBE":
        x = fm[("PERFORMANCE_MAX", "YouTube network (format not reported by Google for PMax)")]
        x[3] += float(r["spend_usd"]); x[4] += int(r["impressions"])
        if current("Google", r["customer_id"]):
            x[0] += float(r["spend_usd"]); x[1] += int(r["impressions"]); x[2].add(r["customer_id"])
rows = [[ch, f, len(a), round(s, 2), i, cpm(s, i), round(S, 2), I, cpm(S, I)] for (ch, f), (s, i, a, S, I) in fm.items()]
rows.sort(key=lambda x: (x[0], -x[3]))
w("03_youtube_cpm_by_format.csv",
  ["campaign_type", "youtube_format", "accounts_current_clients", "spend_usd_current_clients",
   "impressions_current_clients", "cpm_usd_current_clients", "spend_usd_all_accounts",
   "impressions_all_accounts", "cpm_usd_all_accounts"], rows)
rows = [[r["customer_id"], client("Google", r["customer_id"]), status("Google", r["customer_id"]),
         yn(current("Google", r["customer_id"])), g_dma.get(r["customer_id"], ""), r["campaign_id"], r["campaign"],
         r["channel_type"], YT_LABEL.get(r["ad_format_type"], r["ad_format_type"]), r["spend_usd"], r["impressions"],
         cpm(float(r["spend_usd"]), int(r["impressions"]))]
        for r in g_fmt if r["channel_type"] != "PERFORMANCE_MAX"]
w("03b_youtube_format_detail.csv",
  ["customer_id", "client", "roster_status", "in_headline_numbers", "market_dma", "campaign_id", "campaign",
   "campaign_type", "youtube_format", "spend_usd_12mo", "impressions_12mo", "cpm_usd"], rows)

# ============================================================================ 04 CTV / OTT
ctv = defaultdict(lambda: [0.0, 0])
tot_ch = defaultdict(lambda: [0.0, 0.0])  # channel -> [all spend, current spend]
for r in g_dev:
    cur = current("Google", r["customer_id"])
    tot_ch[r["channel_type"]][0] += float(r["spend_usd"])
    if cur:
        tot_ch[r["channel_type"]][1] += float(r["spend_usd"])
    if r["device"] == "CONNECTED_TV":
        k = (r["customer_id"], r["channel_type"])
        ctv[k][0] += float(r["spend_usd"]); ctv[k][1] += int(r["impressions"])
rows = []
cur_s = cur_i = 0.0
for (cid, ch), (s, i) in sorted(ctv.items(), key=lambda x: -x[1][0]):
    if s < 0.01 and i < 100:
        continue
    cur = current("Google", cid)
    if cur:
        cur_s += s; cur_i += i
    rows.append(["Google Ads: YouTube served on TV screens", cid, client("Google", cid), status("Google", cid), yn(cur),
                 g_dma.get(cid, ""), ch, round(s, 2), i, cpm(s, i),
                 f"{s / tot_ch[ch][0] * 100:.1f}% of all {ch} spend in the pull" if tot_ch[ch][0] else ""])
video_ctv_cur = sum(s for (cid, ch), (s, i) in ctv.items() if ch == "VIDEO" and current("Google", cid))
rows.append(["Google Ads: total, current clients", "", "", "", "yes", "", "all", round(cur_s, 2), int(cur_i), cpm(cur_s, cur_i),
             f"standalone YouTube (VIDEO) on TV screens = {pct(video_ctv_cur, tot_ch['VIDEO'][1])} of current clients' VIDEO spend"])
md = defaultdict(lambda: [0.0, 0])
for r in meta_device:
    if current("Meta", r["account_id"]):
        md[r["impression_device"]][0] += float(r["spend_usd"]); md[r["impression_device"]][1] += int(r["impressions"])
md_tot = sum(v[1] for v in md.values())
rows.append(["Meta: delivery by device, current clients", "", "", "", "yes", "", "all", 0, 0, "",
             "Meta reports no TV device. Devices returned: " + ", ".join(sorted(md)) +
             f". 'other' = {md['other'][1]:,} of {md_tot:,} impressions ({pct(md['other'][1], md_tot)})."])
rows.append(["Dedicated OTT/CTV buys (Roku, Hulu, DSPs, etc.)", "", "NONE in any TSD Meta or Google Ads account", "", "",
             "", "", 0, 0, "", "Other vendors outside Meta and Google Ads were not checked."])
w("04_ctv_ott_delivery.csv",
  ["source", "customer_id", "client", "roster_status", "in_headline_numbers", "market_dma", "campaign_type",
   "ctv_spend_usd_12mo", "ctv_impressions_12mo", "ctv_cpm_usd", "note"], rows)

# ============================================================================ 05 Frequency
# 05a Meta weekly per client (account level: Meta dedupes people across all the client's campaigns that week)
rows = []
for r in meta_weekly:
    a, f = r["account_id"], float(r["frequency"])
    rows.append(["Meta", a, client("Meta", a), status("Meta", a), META_MARKET.get(a, ""),
                 yn(managed("Meta", a, r["week_start"])), r["week_start"], r["week_stop"], r["spend_usd"],
                 r["impressions"], r["reach"], f, yn(f >= FLOOR)])
w("05a_meta_weekly_frequency_by_client.csv",
  ["platform", "account_id", "client", "roster_status", "market_dma", "counts_as_tsd_delivery", "week_start",
   "week_stop", "spend_usd", "impressions", "reach", "frequency", "meets_3x_floor"], rows)

# 05b Meta weekly per awareness campaign
rows = []
for r in meta_aw_weekly:
    a, f = r["account_id"], float(r["frequency"])
    n = camp_name.get(r["campaign_id"], "")
    rows.append(["Meta", a, client("Meta", a), status("Meta", a), META_MARKET.get(a, ""),
                 yn(managed("Meta", a, r["week_start"])), r["campaign_id"], n, audience_note(n), r["week_start"],
                 r["week_stop"], r["spend_usd"], r["impressions"], r["reach"], f, yn(f >= FLOOR)])
w("05b_meta_weekly_frequency_awareness_campaigns.csv",
  ["platform", "account_id", "client", "roster_status", "market_dma", "counts_as_tsd_delivery", "campaign_id",
   "campaign", "audience_note", "week_start", "week_stop", "spend_usd", "impressions", "reach", "frequency",
   "meets_3x_floor"], rows)

# 05c Google weekly per YouTube / Display / Demand Gen campaign
rows = []
for r in g_vfreq:
    a, f = r["customer_id"], float(r["avg_impression_frequency_per_user"])
    rows.append(["Google", a, client("Google", a), status("Google", a), g_dma.get(a, ""),
                 yn(managed("Google", a, r["week_start"])), r["campaign_id"], r["campaign"], r["channel_type"],
                 r["week_start"], r["week_stop"], r["spend_usd"], r["impressions"], r["unique_users"], round(f, 4),
                 yn(f >= FLOOR)])
w("05c_google_weekly_frequency_video_display.csv",
  ["platform", "customer_id", "client", "roster_status", "market_dma", "counts_as_tsd_delivery", "campaign_id",
   "campaign", "campaign_type", "week_start", "week_stop", "spend_usd", "impressions", "unique_users",
   "avg_frequency_per_user", "meets_3x_floor"], rows)


def summarize(series):
    fs = [x["f"] for x in series]
    last = [x["f"] for x in series if x["ws"] >= LAST4_SINCE]
    n3 = sum(1 for f in fs if f >= FLOOR)
    return [len(fs), round(sum(x["s"] for x in series), 2), round(statistics.median(fs), 2), round(max(fs), 2),
            n3, pct(n3, len(fs)), int(statistics.median([x["r"] for x in series])),
            round(statistics.mean(last), 2) if last else ""]


# 05d per client / campaign, current clients, TSD-run weeks only
by = defaultdict(list)
excluded = defaultdict(int)


def add(key, p, a, pt):
    if not current(p, a):
        return
    if managed(p, a, pt["ws"]):
        by[key].append(pt)
    else:
        excluded[key] += 1


for r in meta_weekly:
    a = r["account_id"]
    add(("Meta: all campaigns (per client)", a, client("Meta", a), META_MARKET.get(a, ""), ""), "Meta", a,
        {"f": float(r["frequency"]), "s": float(r["spend_usd"]), "r": int(r["reach"]), "ws": r["week_start"]})
for r in meta_aw_weekly:
    a = r["account_id"]
    add(("Meta: awareness campaign", a, client("Meta", a), META_MARKET.get(a, ""), camp_name.get(r["campaign_id"], "")),
        "Meta", a, {"f": float(r["frequency"]), "s": float(r["spend_usd"]), "r": int(r["reach"]), "ws": r["week_start"]})
for r in g_vfreq:
    a = r["customer_id"]
    add((f"Google: {r['channel_type']} campaign", a, client("Google", a), g_dma.get(a, ""), r["campaign"]), "Google", a,
        {"f": float(r["avg_impression_frequency_per_user"]), "s": float(r["spend_usd"]), "r": int(r["unique_users"]),
         "ws": r["week_start"]})
rows = []
for k in sorted(set(by) | set(excluded), key=lambda k: (k[0], -sum(y["s"] for y in by.get(k, [])))):
    if by.get(k):
        rows.append(list(k) + summarize(by[k]) + [excluded.get(k, 0)])
    else:
        rows.append(list(k) + [0, "", "", "", "", "", "", ""] + [excluded.get(k, 0)])
w("05d_frequency_summary.csv",
  ["level", "account_id", "client", "market_dma", "campaign", "weeks_counted", "spend_usd",
   "median_weekly_frequency", "max_weekly_frequency", "weeks_at_or_above_3x", "pct_weeks_at_or_above_3x",
   "median_weekly_reach_or_unique_users", "avg_weekly_frequency_last_4_weeks", "pre_tsd_weeks_excluded"], rows)


# 05e book-level rollup
def book(label, fs):
    n3 = sum(1 for f in fs if f >= FLOOR)
    return [label, len(fs), round(statistics.median(fs), 2) if fs else "", n3, pct(n3, len(fs))]


cw = [float(r["frequency"]) for r in meta_weekly if managed("Meta", r["account_id"], r["week_start"])]
cw4 = [float(r["frequency"]) for r in meta_weekly
       if managed("Meta", r["account_id"], r["week_start"]) and r["week_start"] >= LAST4_SINCE]
aw = [float(r["frequency"]) for r in meta_aw_weekly
      if managed("Meta", r["account_id"], r["week_start"]) and float(r["spend_usd"]) >= 20]
yt = [float(r["avg_impression_frequency_per_user"]) for r in g_vfreq
      if r["channel_type"] in ("VIDEO", "DEMAND_GEN") and managed("Google", r["customer_id"], r["week_start"])]
cw_all = [float(r["frequency"]) for r in meta_weekly]
aw_all = [float(r["frequency"]) for r in meta_aw_weekly if float(r["spend_usd"]) >= 20]
yt_all = [float(r["avg_impression_frequency_per_user"]) for r in g_vfreq if r["channel_type"] in ("VIDEO", "DEMAND_GEN")]
w("05e_frequency_book_rollup.csv",
  ["series", "weeks_counted", "median_weekly_frequency", "weeks_at_or_above_3x", "pct_at_or_above_3x"],
  [book("HEADLINE Meta, per client (all campaigns deduped), current clients, TSD-run weeks", cw),
   book("HEADLINE Meta, per client, current clients, last 4 weeks", cw4),
   book("HEADLINE Meta, awareness campaigns (weeks with $20+ spend), current clients, TSD-run weeks", aw),
   book("HEADLINE Google, YouTube (Video + Demand Gen), current clients, TSD-run weeks", yt),
   book("reference: Meta, per client, every account in the pull, all weeks", cw_all),
   book("reference: Meta, awareness campaigns, every account in the pull, all weeks", aw_all),
   book("reference: Google, YouTube, every account in the pull, all weeks", yt_all)])

# 05f cross-platform weekly impressions per current client (Meta + Google by network).
# Nothing dedupes people across Meta and Google, so this counts exposures, not people.
cw_rows = defaultdict(lambda: {"meta_i": 0, "meta_r": 0, "meta_f": "", "yt": 0, "disp": 0, "search": 0,
                               "managed": True, "has_meta": False})
for r in meta_weekly:
    a = r["account_id"]
    if not current("Meta", a):
        continue
    x = cw_rows[(client("Meta", a), r["week_start"])]
    x["meta_i"] += int(r["impressions"]); x["meta_r"] += int(r["reach"]); x["meta_f"] = float(r["frequency"])
    x["has_meta"] = True
    x["managed"] &= managed("Meta", a, r["week_start"])
for r in g_wnet:
    a = r["customer_id"]
    if not current("Google", a):
        continue
    b = NET_BUCKET.get(r["ad_network_type"], "display")
    x = cw_rows[(client("Google", a), r["week_start"])]
    x[{"youtube": "yt", "display": "disp", "search": "search"}[b]] += int(r["impressions"])
    if int(r["impressions"]) and b != "search":
        x["managed"] &= managed("Google", a, r["week_start"])
meta_clients = {client("Meta", r["account_id"]) for r in meta_weekly if current("Meta", r["account_id"])}
rows = []
for (cl, ws), x in sorted(cw_rows.items()):
    tot = x["meta_i"] + x["yt"] + x["disp"]
    if not tot:
        continue
    rows.append([cl, client_market.get(cl, ""), ws, yn(x["managed"]),
                 x["meta_i"] if x["has_meta"] else "", x["meta_r"] if x["has_meta"] else "", x["meta_f"],
                 x["yt"], x["disp"], tot, round(tot / 3), pct(x["yt"] + x["disp"], tot), x["search"]])
w("05f_cross_platform_weekly_impressions_by_client.csv",
  ["client", "market_dma", "week_start", "counts_as_tsd_delivery", "meta_impressions", "meta_reach",
   "meta_frequency", "google_youtube_impressions", "google_display_impressions",
   "total_impressions_excl_search", "max_adults_reachable_3x_this_week", "google_share_of_total",
   "google_search_impressions_not_counted"], rows)

# 05g per-client summary of 05f over TSD-run weeks with any brand-type delivery. Every column uses the
# same set of weeks; a week where one platform delivered nothing counts as 0 for that platform.
agg5 = defaultdict(list)
for r in rows:
    if r[3] == "yes":
        agg5[(r[0], r[1])].append(r)
out = []
for (cl, mk), rs in sorted(agg5.items(), key=lambda x: -statistics.median([r[9] for r in x[1]])):
    tot = [r[9] for r in rs]
    g = [r[7] + r[8] for r in rs]
    m = [r[4] or 0 for r in rs]
    out.append([cl, mk, yn(cl in meta_clients), len(rs), sum(1 for x in m if x), int(statistics.median(tot)),
                int(statistics.median(m)) if cl in meta_clients else "", int(statistics.median(g)),
                pct(sum(g), sum(tot)), int(statistics.median(tot) / 3)])
w("05g_cross_platform_summary_by_client.csv",
  ["client", "market_dma", "has_meta_in_pull", "tsd_run_weeks_with_brand_type_delivery", "weeks_with_meta_delivery",
   "median_weekly_impressions_excl_search", "median_weekly_meta_impressions",
   "median_weekly_google_youtube_display_impressions", "google_share_of_impressions",
   "median_max_adults_reachable_3x_per_week"], out)

# ============================================================================ 06 audience size template
w("06_meta_audience_size_estimates.csv",
  ["zone", "zip", "census_adults_18plus", "meta_estimated_audience_low", "meta_estimated_audience_high",
   "ratio_meta_to_census", "notes"],
  [["Duluth, GA", "30096", 54888, "", "", "", "Manual lookup in Ads Manager (audience definition, location = ZIP, 18+). Not available through the connector."],
   ["(client ZIP 1)", "", "", "", "", "", "Suggested: Zen Air zone ZIP near 30096, e.g. 30097 (Duluth/Johns Creek) or 30043 (Lawrenceville)"],
   ["(client ZIP 2)", "", "", "", "", "", "Pick a ZIP from a client Edu knows well"]])

# ============================================================================ 07 CPM by quarter, current clients
qs = defaultdict(lambda: [0.0, 0])
for r in meta_aw_weekly:
    if current("Meta", r["account_id"]):
        k = ("Meta", "Awareness / Reach campaigns", quarter(r["week_start"]))
        qs[k][0] += float(r["spend_usd"]); qs[k][1] += int(r["impressions"])
for r in meta_weekly:
    if current("Meta", r["account_id"]):
        k = ("Meta", "All objectives (account level)", quarter(r["week_start"]))
        qs[k][0] += float(r["spend_usd"]); qs[k][1] += int(r["impressions"])
for r in g_week:
    if current("Google", r["customer_id"]):
        k = ("Google", r["channel_type"], quarter(r["week_start"]))
        qs[k][0] += float(r["spend_usd"]); qs[k][1] += int(r["impressions"])
rows = []
for p, g in sorted({(p, g) for p, g, _ in qs}):
    row = [p, g]
    for q, _, _ in QUARTERS:
        s, i = qs[(p, g, q)]
        row += [round(s, 2), cpm(s, i)]
    rows.append(row)
w("07_cpm_by_quarter.csv",
  ["platform", "objective_or_channel"] + [x for q, _, _ in QUARTERS for x in (f"{q}_spend_usd", f"{q}_cpm_usd")], rows)

# ============================================================================ 08 where awareness impressions land
# Goal comes from the ad sets (optimization_goal), not the campaign name: a name can say nothing about the
# template (Mission Accomplished's 04.27 campaign is Ad Recall Lift without saying so).
placements = load(RAW, "meta_awareness_placement_12mo.csv")
goal_rows = load(RAW, "meta_awareness_adset_goal_12mo.csv")
_goal_spend = defaultdict(lambda: defaultdict(float))
for r in goal_rows:
    _goal_spend[r["campaign_id"]][r["optimization_goal"]] += float(r["spend_usd"])
camp_goal = {}
for cid, d in _goal_spend.items():
    spent = [g for g, s in d.items() if s > 0]
    camp_goal[cid] = spent[0] if len(spent) == 1 else "mixed"
camp_goal.update(GOAL_FROM_NAME)
GOAL_LABEL = {"AD_RECALL_LIFT": "Ad Recall Lift", "REACH": "Reach"}

pc = defaultdict(lambda: {"s": 0.0, "i": 0, "ms": 0.0, "mi": 0, "other": defaultdict(int)})
for r in placements:
    x = pc[r["campaign_id"]]
    s, i = float(r["spend_usd"]), int(r["impressions"])
    x["s"] += s; x["i"] += i
    if r["platform_position"] == "marketplace":
        x["ms"] += s; x["mi"] += i
    else:
        x["other"][r["platform_position"]] += i
rows = []
for c in meta_camps:
    if META_GROUP.get(c["objective"]) != "Awareness / Reach":
        continue
    a, cid = c["account_id"], c["campaign_id"]
    goal = GOAL_LABEL.get(camp_goal.get(cid), camp_goal.get(cid, "not pulled"))
    if cid in GOAL_FROM_NAME:
        goal += " (from campaign name; ad sets no longer readable)"
    x = pc.get(cid)
    if x:
        top = max(x["other"].items(), key=lambda kv: kv[1])[0] if x["other"] else ""
        place = [x["mi"], pct(x["mi"], x["i"]), round(x["ms"], 2), cpm(x["ms"], x["mi"]),
                 cpm(x["s"] - x["ms"], x["i"] - x["mi"]), cpm(x["s"], x["i"] - x["mi"]), top]
    else:
        place = ["", "", "", "", "", "", "placement not pulled"]
    rows.append([a, client("Meta", a), status("Meta", a), yn(current("Meta", a)), META_MARKET.get(a, ""), cid,
                 c["campaign"], goal, round(c["spend"], 2), c["impressions"], cpm(c["spend"], c["impressions"])] + place)
rows.sort(key=lambda r: (r[3] != "yes", r[7], -r[8]))
w("08_meta_awareness_placement.csv",
  ["account_id", "client", "roster_status", "in_headline_numbers", "market_dma", "campaign_id", "campaign",
   "optimization_goal", "spend_usd_12mo", "impressions_12mo", "cpm_usd", "marketplace_impressions",
   "marketplace_share_of_impressions", "marketplace_spend_usd", "marketplace_cpm_usd", "cpm_usd_outside_marketplace",
   "cpm_usd_if_marketplace_does_not_count", "largest_placement_outside_marketplace"], rows)

# 08b rollups, current clients: by goal across the book, and goal x market where a market ran both
gb = defaultdict(lambda: {"s": 0.0, "i": 0, "ms": 0.0, "mi": 0, "ps": 0.0, "pi": 0, "c": set(), "a": set()})
for c in meta_camps:
    a, cid = c["account_id"], c["campaign_id"]
    if not current("Meta", a) or META_GROUP.get(c["objective"]) != "Awareness / Reach" or cid not in camp_goal:
        continue
    goal = GOAL_LABEL.get(camp_goal[cid], camp_goal[cid])
    for key in (("book", "all markets", goal), ("market", META_MARKET[a], goal)):
        x = gb[key]
        x["s"] += c["spend"]; x["i"] += c["impressions"]; x["c"].add(cid); x["a"].add(a)
        if cid in pc:
            x["ps"] += pc[cid]["s"]; x["pi"] += pc[cid]["i"]; x["ms"] += pc[cid]["ms"]; x["mi"] += pc[cid]["mi"]
both = {mk for (lvl, mk, g) in gb if lvl == "market"
        if ("market", mk, "Reach") in gb and ("market", mk, "Ad Recall Lift") in gb}
rows = []
for (lvl, mk, g), x in sorted(gb.items()):
    if lvl == "market" and mk not in both:
        continue
    rows.append([lvl, mk, g, len(x["a"]), len(x["c"]), round(x["s"], 2), x["i"], cpm(x["s"], x["i"]),
                 pct(x["mi"], x["pi"]), cpm(x["ms"], x["mi"]), cpm(x["ps"] - x["ms"], x["pi"] - x["mi"]),
                 cpm(x["ps"], x["pi"] - x["mi"]),
                 "" if x["pi"] >= 0.995 * x["i"] else f"placement split covers {pct(x['pi'], x['i'])} of impressions"])
w("08b_meta_awareness_goal_summary.csv",
  ["level", "market_dma", "optimization_goal", "accounts", "campaigns", "spend_usd_12mo", "impressions_12mo",
   "cpm_usd", "marketplace_share_of_impressions", "marketplace_cpm_usd", "cpm_usd_outside_marketplace",
   "cpm_usd_if_marketplace_does_not_count", "note"], rows)
