# APPLIED LIVE 2026-11-04 (~17:00 -03), read-back confirmed. Do NOT re-run with --apply.
# Watt's Right (3651667805), Option 3 "Push" (+$7,000/mo, all to Google Search) from the 11-04 Google-only proposal.
# Approval: Angela (Slack DM 2026-11-04 14:54 -03): "Watt's Right is going to the Push budget - increase $7000/month". Edu's go 11-04 in-session.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Search $140/d -> $370/d (~$11,250/mo; proposal = $11,260). PMax $95 and LSA unchanged.
1. Budgets: Branded 23690645223 $35 -> $50/d, Nonbranded 23832838033 $105 -> $320/d.
2. Nonbranded tCPA $95 -> $110 (client accepted higher CPL; at $95 a bigger budget won't spend, NB rank-lost ~60%).
3. Three new Nonbranded ad groups (proposal: generic "electrician" + generators/surge), each with keywords, ad-group negatives and 1 RSA:
   Electrician (General) -> /locations/tulsa-ok/, Whole-Home Generator, Whole-Home Surge Protector.
4. Campaign negatives (PHRASE) for job seekers, replayed against 30d search terms first.
Aborts on shared budgets / unexpected current values / ad group names already present.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, BR, NB = "3651667805", "23690645223", "23832838033"
BUDGETS = {BR: (35.0, 50.0), NB: (105.0, 320.0)}
TCPA_OLD, TCPA_NEW = 95.0, 110.0
SITE = "https://www.callwattsright.com"

LIC, PRICE, LOCAL, TOP = "Licensed & Insured in Oklahoma", "Price Up Front, No Surprises", "Local Tulsa Electricians", "Top-Rated on Google"
GROUPS = [
    {
        "name": "Electrician (General)",
        "url": f"{SITE}/locations/tulsa-ok/", "path": ("Electrician", "Tulsa"),
        "kw": [("electrician", "EXACT"), ("electrician near me", "EXACT"), ("electricians near me", "EXACT"),
               ("local electrician", "EXACT"), ("electrician tulsa", "PHRASE"), ("tulsa electrician", "PHRASE"),
               ("electrician in tulsa", "PHRASE"), ("residential electrician", "PHRASE"), ("electrical contractor", "PHRASE"),
               ("electrical repair", "PHRASE")],
        "neg": ["auto", "automotive", "marine", "boat", "aircraft", "industrial"],
        "h1": ["Electrician in Tulsa, OK", "Tulsa's Trusted Electrician", LOCAL],
        "h": [LIC, "Same-Day Service Available", PRICE, "Background-Checked Techs", "Nights, Weekends & Holidays",
              "No Extra Fees on Weekends", "24/7 Emergency Response", TOP, "Panels, Wiring, Outlets & More",
              "Serving Tulsa & Broken Arrow", "Your Neighborhood Electrician", "Request Service Online"],
        "d": ["Licensed, local electricians for Tulsa homes. Same-day service, clear price up front.",
              "Panels, wiring, outlets, lighting and repairs. Background-checked, fully insured techs.",
              "Nights, weekends and holidays at no extra fee. Call now or request service online.",
              "Top-rated on Google by Tulsa homeowners. You'll know the full cost before we start."],
    },
    {
        "name": "Whole-Home Generator",
        "url": f"{SITE}/upgrades/whole-home-generators/", "path": ("Generators", "Tulsa"),
        "kw": [("whole house generator", "PHRASE"), ("whole home generator", "PHRASE"), ("home standby generator", "PHRASE"),
               ("standby generator installation", "PHRASE"), ("generator installation", "PHRASE"), ("generator installer", "PHRASE"),
               ("home generator installation", "PHRASE")],
        "neg": ["portable", "rental", "rent", "used", "parts", "manual", "inverter", "solar", "harbor freight", "home depot",
                "lowes", "costco", "sams club", "walmart", "amazon"],
        "h1": ["Generator Installation Tulsa", "Whole-Home Generators Tulsa", "Home Standby Generator Tulsa"],
        "h": ["Keep Power Through Outages", "Turns On Automatically", "Natural Gas or Propane", "Heat & Fridge Stay Running",
              "Sized to Your Home's Needs", "Transfer Switch Installed", "Ready Before Winter Storms", "Get a Generator Quote",
              LIC, PRICE, LOCAL, TOP],
        "d": ["Whole-home generators that turn on by themselves when the power goes out in Tulsa.",
              "We size it to your home, install the transfer switch and do the hookup to code.",
              "Runs on natural gas or propane, so heat, lights and the fridge stay on in a storm.",
              "Licensed, local Tulsa electricians with upfront pricing. Call now or request a quote."],
    },
    {
        "name": "Whole-Home Surge Protector",
        "url": f"{SITE}/upgrades/whole-home-surge-protectors/", "path": ("Surge-Protector", "Tulsa"),
        "kw": [("whole house surge protector", "PHRASE"), ("whole home surge protector", "PHRASE"),
               ("whole house surge protection", "PHRASE"), ("surge protector installation", "PHRASE"),
               ("panel surge protector", "PHRASE"), ("electrical panel surge protector", "PHRASE")],
        "neg": ["amazon", "home depot", "lowes", "best buy", "walmart", "power strip", "reviews", "review", "diy"],
        "h1": ["Whole-Home Surge Protector", "Surge Protection in Tulsa", "Whole-House Surge Protection"],
        "h": ["Installed at Your Main Panel", "Protects Every Outlet at Once", "Guard Appliances & Electronics",
              "Lightning & Grid Surges", "More Than a Power Strip", "Protect Your HVAC & Fridge", LIC, PRICE, LOCAL, TOP,
              "Request Service Online"],
        "d": ["A surge protector at your main panel stops voltage spikes before they reach your devices.",
              "Protects appliances, HVAC, TVs and computers in every room, not just one power strip.",
              "Licensed, local Tulsa electricians. Clear price up front before any work starts.",
              "Fewer fried electronics and costly repairs. Call now or request service online."],
    },
]
CAMP_NEG = ["electrician jobs", "electrical jobs", "electrician job", "jobs hiring", "hiring", "careers", "career", "salary", "apprentice", "apprenticeship", "school", "training",
            "classes", "course", "union", "how to become", "certification"]

APPLY = "--apply" in sys.argv
vo = not APPLY

# --- static checks
for g in GROUPS:
    hs = g["h1"] + g["h"]
    assert 3 <= len(hs) <= 15 and len(set(hs)) == len(hs), (g["name"], len(hs))
    for h in hs: assert len(h) <= 30, (h, len(h))
    assert len(g["d"]) == 4
    for d in g["d"]: assert len(d) <= 90, (d, len(d))
    for p in g["path"]: assert len(p) <= 15, p

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

# --- guards
bud = {str(r.campaign.id): r for r in q(f"""SELECT campaign.id, campaign.name, campaign.bidding_strategy_type, campaign.bidding_strategy,
    campaign.maximize_conversions.target_cpa_micros, campaign_budget.resource_name, campaign_budget.amount_micros,
    campaign_budget.explicitly_shared, campaign_budget.reference_count FROM campaign WHERE campaign.id IN ({BR},{NB})""")}
for cid, (old, new) in BUDGETS.items():
    r = bud[cid]; cur = r.campaign_budget.amount_micros / 1e6
    print(f"{r.campaign.name}: ${cur:.2f}/d -> ${new:.2f}/d  shared={r.campaign_budget.explicitly_shared} refs={r.campaign_budget.reference_count}")
    if r.campaign_budget.explicitly_shared or r.campaign_budget.reference_count > 1: sys.exit(f"ABORT: {cid} budget shared")
    if abs(cur - old) > 0.01: sys.exit(f"ABORT: {cid} budget ${cur:.2f}, expected ${old:.2f}")
nb = bud[NB].campaign
if nb.bidding_strategy_type.name != "MAXIMIZE_CONVERSIONS" or nb.bidding_strategy:
    sys.exit("ABORT: Nonbranded is not standard Maximize Conversions")
if abs(nb.maximize_conversions.target_cpa_micros / 1e6 - TCPA_OLD) > 0.01:
    sys.exit(f"ABORT: NB tCPA ${nb.maximize_conversions.target_cpa_micros/1e6:.2f}, expected ${TCPA_OLD:.2f}")
existing_ag = {r.ad_group.name for r in q(f"SELECT ad_group.name FROM ad_group WHERE campaign.id = {NB} AND ad_group.status != 'REMOVED'")}
for g in GROUPS:
    if g["name"] in existing_ag: sys.exit(f"ABORT: ad group '{g['name']}' already exists")

# --- negative replay (30d NB search terms) for campaign + ad-group negatives
terms = q(f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
    WHERE campaign.id = {NB} AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0""")
kws_live = [r.ad_group_criterion.keyword.text.lower() for r in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE campaign.id = {NB} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")]
existing_neg = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
    WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
camp_neg = [n for n in CAMP_NEG if n not in existing_neg]
new_kws = [k for g in GROUPS for k, _ in g["kw"]]
for n in CAMP_NEG:
    hit = [r for r in terms if f" {n} " in f" {r.search_term_view.search_term.lower()} "]
    conv = sum(r.metrics.conversions for r in hit)
    print(f"camp neg '{n}': {'ALREADY ' if n in existing_neg else ''}{len(hit)} terms ${sum(r.metrics.cost_micros for r in hit)/1e6:.2f} conv {conv:.1f} "
          f"{[h.search_term_view.search_term for h in hit][:3]} kw conflicts {[k for k in kws_live + new_kws if f' {n} ' in f' {k} ']}")
    if conv > 0 or [k for k in kws_live + new_kws if f" {n} " in f" {k} "]: sys.exit(f"ABORT: camp neg '{n}' blocks converting terms/keywords")
for g in GROUPS:
    for n in g["neg"]:
        c = [k for k, _ in g["kw"] if f" {n} " in f" {k} "]
        if c: sys.exit(f"ABORT: ad group neg '{n}' conflicts with {c}")

# --- mutations: ad groups + keywords + negatives + RSAs in ONE atomic GoogleAdsService.mutate (temp ids -1..-3)
MT = client.enums.KeywordMatchTypeEnum
mops, ag_paths = [], []
for i, g in enumerate(GROUPS):
    path = ga.ad_group_path(CID, str(-(i + 1))); ag_paths.append(path)
    m = client.get_type("MutateOperation"); a = m.ad_group_operation.create
    a.resource_name = path; a.name = g["name"]; a.campaign = ga.campaign_path(CID, NB)
    a.status = client.enums.AdGroupStatusEnum.ENABLED; a.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    mops.append(m)
for g, path in zip(GROUPS, ag_paths):
    for text, mt in g["kw"]:
        m = client.get_type("MutateOperation"); c = m.ad_group_criterion_operation.create
        c.ad_group = path; c.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        c.keyword.text = text; c.keyword.match_type = MT[mt]; mops.append(m)
    for text in g["neg"]:
        m = client.get_type("MutateOperation"); c = m.ad_group_criterion_operation.create
        c.ad_group = path; c.negative = True; c.keyword.text = text; c.keyword.match_type = MT.PHRASE; mops.append(m)
    m = client.get_type("MutateOperation"); ad = m.ad_group_ad_operation.create
    ad.ad_group = path; ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    ad.ad.final_urls.append(g["url"])
    rsa = ad.ad.responsive_search_ad; rsa.path1, rsa.path2 = g["path"]
    for t in g["h1"]:
        h = client.get_type("AdTextAsset"); h.text = t; h.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1; rsa.headlines.append(h)
    for t in g["h"]:
        h = client.get_type("AdTextAsset"); h.text = t; rsa.headlines.append(h)
    for t in g["d"]:
        d = client.get_type("AdTextAsset"); d.text = t; rsa.descriptions.append(d)
    mops.append(m)
res = ga.mutate(request={"customer_id": CID, "mutate_operations": mops, "validate_only": vo})
print(f"ad groups + kw/negs + RSAs ({len(mops)} ops) ok", "(validate_only)" if vo else "APPLIED")
if APPLY:
    for r in res.mutate_operation_responses:
        if r.ad_group_result.resource_name: print("   ", r.ad_group_result.resource_name)

cc_ops = []
for t in camp_neg:
    op = client.get_type("CampaignCriterionOperation"); c = op.create
    c.campaign = ga.campaign_path(CID, NB); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; cc_ops.append(op)
if cc_ops:
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": cc_ops, "validate_only": vo})
print(f"campaign negatives ({len(cc_ops)}) ok", "(validate_only)" if vo else "APPLIED")

op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(CID, NB)
op.update.maximize_conversions.target_cpa_micros = int(TCPA_NEW * 1e6)
op.update_mask.paths.append("maximize_conversions.target_cpa_micros")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("NB tCPA ok", "(validate_only)" if vo else "APPLIED")

ops = []
for cid, (old, new) in BUDGETS.items():
    op = client.get_type("CampaignBudgetOperation")
    op.update.resource_name = bud[cid].campaign_budget.resource_name
    op.update.amount_micros = int(new * 1e6); op.update_mask.paths.append("amount_micros"); ops.append(op)
client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("budgets ok", "(validate_only)" if vo else "APPLIED")

if APPLY:
    print("--- read-back")
    cnt = {}
    for r in q(f"""SELECT campaign.name, campaign.maximize_conversions.target_cpa_micros, campaign_budget.amount_micros, campaign.primary_status
            FROM campaign WHERE campaign.status = 'ENABLED' AND campaign.advertising_channel_type IN ('SEARCH','PERFORMANCE_MAX')"""):
        print(f"   {r.campaign.name}: ${r.campaign_budget.amount_micros/1e6:.2f}/d tCPA ${r.campaign.maximize_conversions.target_cpa_micros/1e6:.2f} "
              f"{r.campaign.primary_status.name}")
    for r in q(f"""SELECT ad_group.name, ad_group.status, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.policy_summary.approval_status,
            ad_group_ad.policy_summary.review_status FROM ad_group_ad WHERE campaign.id = {NB} AND ad_group.name IN
            ({','.join(repr(g['name']) for g in GROUPS)})"""):
        print(f"   {r.ad_group.name} ({r.ad_group.status.name}): ad {r.ad_group_ad.ad.id} {r.ad_group_ad.status.name} "
              f"{r.ad_group_ad.policy_summary.review_status.name}/{r.ad_group_ad.policy_summary.approval_status.name}")
    for r in q(f"""SELECT ad_group.name, ad_group_criterion.negative FROM ad_group_criterion WHERE campaign.id = {NB}
            AND ad_group_criterion.type = 'KEYWORD' AND ad_group.name IN ({','.join(repr(g['name']) for g in GROUPS)})"""):
        cnt[(r.ad_group.name, r.ad_group_criterion.negative)] = cnt.get((r.ad_group.name, r.ad_group_criterion.negative), 0) + 1
    print("   keyword counts (group, negative):", cnt)
    got = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    print(f"   campaign negatives missing: {[n for n in CAMP_NEG if n not in got]}")
