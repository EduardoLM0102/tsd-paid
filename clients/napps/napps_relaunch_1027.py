# APPLIED LIVE 2026-10-27 on Edu's go (incl. additions + Eagle Point unlink), read-back confirmed. Do NOT re-run with --apply.
# Edu's go 2026-10-27 ("We can implement them in the campaigns we paused and turn them on again"), Command Center fu-084 + fu-092.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Napps (9509605037), 2026-10-27. Relaunch the 2 non-branded campaigns (paused by Edu 10-22) on the 2 new landing pages, with the
10-22 diagnosis fixes. NB total stays $100/d, split 65 HVAC / 35 plumbing (client request 10-23). Branded untouched.

HEATING 24049055193 (TSD_07.21_Search_Nonbranded_HVAC_Heating): budget $50 -> $65, Max Conv -> Max Clicks $15 cap,
  Furnace Repair ad 828663394462 -> /furnace-heating-repair-in-longview/, PAUSE ad groups AC Repair / Heating Maintenance /
  Furnace Replacement (page is repair-only, no AC page), 8 HVAC competitor PHRASE negatives, ENABLE.
PLUMBING 23819717682 (TSD_06.05_Leads_Search_Nonbranded_Plumbing): budget $50 -> $35, Max Clicks $15 cap,
  Emergency Plumber ad 807944988879 -> /emergency-plumber-in-longview/, PAUSE 'plumber available now' PHRASE (EXACT stays),
  PAUSE ad groups Drain and Sewer / Leak Detection (page is emergency-only), 7 plumbing competitor PHRASE negatives,
  ENABLE.
EAGLE POINT (Edu: exclude, not just pause; old TSD client): unlink every Eagle Point Roofing sitelink from every campaign
  (2 assets x Plumbing + old paused HVAC 23819634471). Assets can't be deleted via API; the 3 unlinked ones stay orphaned.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "9509605037"
HT, PL = "24049055193", "23819717682"
CAP = 15.0
C = {
    HT: dict(name="Heating", budget=(50.0, 65.0), ad=("828663394462", "https://nappsac.com/furnace-heating-repair-in-longview/"),
             pause_ag={"199585109498": "AC Repair", "201383309757": "Heating Maintenance", "204217870311": "Furnace Replacement"},
             keep_ag="201511915619",
             neg=["chaffin smith", "a c pros", "wood air conditioning", "alford pace", "veterans pride", "servpro", "jack's ac", "walker heating"]),
    PL: dict(name="Plumbing", budget=(50.0, 35.0), ad=("807944988879", "https://nappsac.com/emergency-plumber-in-longview/"),
             pause_ag={"195930878603": "Drain and Sewer", "198990995169": "Leak Detection"},
             keep_ag="198991071809",
             neg=["benjamin franklin", "ledbetter", "holt plumbing", "eschberger", "jason's plumbing", "roy the plumber", "fountain plumbing"]),
}
PAUSE_KW = (PL, "198991071809", "plumber available now", "PHRASE")
BAD_SITELINKS = ["346848030215", "346848030218", "346848030221", "346848030224", "346848030227"]  # every Eagle Point Roofing asset in the account
EAGLE_CAMPS = f"{PL},23819634471"  # Plumbing + old paused TSD_06.05_Leads_Search_Nonbranded_HVAC
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
E = client.enums
q = lambda s: list(ga.search(customer_id=CID, query=s))
ids = f"{HT},{PL}"

# ---------- guards
for r in q(f"""SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.bidding_strategy,
    campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared, campaign_budget.reference_count
    FROM campaign WHERE campaign.id IN ({ids})"""):
    cid = str(r.campaign.id); c = C[cid]; cur = r.campaign_budget.amount_micros / 1e6
    print(f"{r.campaign.name}: {r.campaign.status.name} {r.campaign.bidding_strategy_type.name} ${cur:.2f}/d shared={r.campaign_budget.explicitly_shared}")
    if r.campaign.status.name != "PAUSED": sys.exit(f"ABORT: {c['name']} not PAUSED")
    if r.campaign.bidding_strategy: sys.exit(f"ABORT: {c['name']} on a portfolio strategy")
    if r.campaign_budget.explicitly_shared or r.campaign_budget.reference_count > 1: sys.exit(f"ABORT: {c['name']} budget shared")
    if abs(cur - c["budget"][0]) > 0.01: sys.exit(f"ABORT: {c['name']} budget ${cur:.2f}, expected ${c['budget'][0]:.2f}")
    c["budget_rn"] = r.campaign_budget.resource_name

for cid, c in C.items():
    ad_id, url = c["ad"]
    r = q(f"""SELECT ad_group.id, ad_group.status, ad_group_ad.resource_name, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.final_urls
        FROM ad_group_ad WHERE ad_group_ad.ad.id = {ad_id}""")[0]
    print(f"  {c['name']} ad {ad_id}: ag {r.ad_group.id} {r.ad_group.status.name}, ad {r.ad_group_ad.status.name} {r.ad_group_ad.policy_summary.approval_status.name} {list(r.ad_group_ad.ad.final_urls)} -> {url}")
    if str(r.ad_group.id) != c["keep_ag"] or r.ad_group.status.name != "ENABLED" or r.ad_group_ad.status.name != "ENABLED":
        sys.exit(f"ABORT: {c['name']} kept ad group/ad not as expected")
    live = q(f"SELECT ad_group.id, ad_group.name FROM ad_group WHERE campaign.id = {cid} AND ad_group.status = 'ENABLED'")
    left = {str(a.ad_group.id) for a in live} - set(c["pause_ag"]) - {c["keep_ag"]}
    print(f"  {c['name']} enabled ad groups: {[a.ad_group.name for a in live]} -> only {c['keep_ag']} stays on")
    if left: sys.exit(f"ABORT: unexpected enabled ad groups {left}")
    others = q(f"SELECT ad_group_ad.ad.id FROM ad_group_ad WHERE ad_group.id = {c['keep_ag']} AND ad_group_ad.status = 'ENABLED'")
    if len(others) != 1: sys.exit(f"ABORT: {c['name']} kept ad group has {len(others)} enabled ads, expected 1")

kw = q(f"""SELECT ad_group_criterion.resource_name, ad_group_criterion.status FROM ad_group_criterion WHERE ad_group.id = {PAUSE_KW[1]}
    AND ad_group_criterion.keyword.text = '{PAUSE_KW[2]}' AND ad_group_criterion.keyword.match_type = '{PAUSE_KW[3]}'""")
if len(kw) != 1: sys.exit("ABORT: 'plumber available now' PHRASE not found exactly once")
print(f"  kw '{PAUSE_KW[2]}' {PAUSE_KW[3]}: {kw[0].ad_group_criterion.status.name} -> PAUSED")

sl = q(f"""SELECT campaign.id, campaign_asset.resource_name, asset.id, asset.final_urls FROM campaign_asset WHERE campaign.id IN ({EAGLE_CAMPS})
    AND asset.id IN ({",".join(BAD_SITELINKS)}) AND campaign_asset.status = 'ENABLED'""")
for s in sl: print(f"  unlink sitelink {s.asset.id} from campaign {s.campaign.id} {list(s.asset.final_urls)}")
if any("eaglepoint" not in u for s in sl for u in s.asset.final_urls): sys.exit("ABORT: unlink list has a non-Eagle Point URL")
for lvl, qq in (("ad group", "SELECT ad_group.id, asset.id FROM ad_group_asset"), ("account", "SELECT asset.id FROM customer_asset")):
    if q(f"{qq} WHERE asset.id IN ({','.join(BAD_SITELINKS)})"): sys.exit(f"ABORT: Eagle Point asset linked at {lvl} level too, extend the script")
if any("nappsac.com" in u for s in sl for u in s.asset.final_urls): sys.exit("ABORT: a sitelink to unlink points to nappsac.com")

# negatives: replay vs live keywords + existing
for cid, c in C.items():
    kws = [k.ad_group_criterion.keyword.text.lower() for k in q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
        WHERE campaign.id = {cid} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE""")]
    existing = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {cid} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    c["neg_new"] = [n for n in c["neg"] if n not in existing]
    conflicts = {n: [k for k in kws if f" {n} " in f" {k} "] for n in c["neg"]}
    conflicts = {n: v for n, v in conflicts.items() if v}
    print(f"  {c['name']} negatives new {len(c['neg_new'])}/{len(c['neg'])}, keyword conflicts: {conflicts or 'none'}")
    if conflicts: sys.exit("ABORT: negative conflicts with a keyword")

# ---------- mutations
tag = "(validate_only)" if vo else "APPLIED"
ops = []
for cid, c in C.items():
    op = client.get_type("CampaignBudgetOperation"); op.update.resource_name = c["budget_rn"]
    op.update.amount_micros = int(c["budget"][1] * 1e6); op.update_mask.paths.append("amount_micros"); ops.append(op)
client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("budgets", tag)

ops = []
for cid, c in C.items():
    o = client.get_type("AdOperation"); a = o.update
    a.resource_name = ga.ad_path(CID, c["ad"][0]); a.final_urls.append(c["ad"][1]); o.update_mask.paths.append("final_urls"); ops.append(o)
client.get_service("AdService").mutate_ads(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("ad final URLs", tag)

ops = []
for cid, c in C.items():
    for ag in c["pause_ag"]:
        op = client.get_type("AdGroupOperation"); op.update.resource_name = ga.ad_group_path(CID, ag)
        op.update.status = E.AdGroupStatusEnum.PAUSED; op.update_mask.paths.append("status"); ops.append(op)
client.get_service("AdGroupService").mutate_ad_groups(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("ad group pauses", tag)

op = client.get_type("AdGroupCriterionOperation"); op.update.resource_name = kw[0].ad_group_criterion.resource_name
op.update.status = E.AdGroupCriterionStatusEnum.PAUSED; op.update_mask.paths.append("status")
client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("keyword pause", tag)

ops = []
for cid, c in C.items():
    for t in c["neg_new"]:
        op = client.get_type("CampaignCriterionOperation"); cc = op.create
        cc.campaign = ga.campaign_path(CID, cid); cc.negative = True; cc.keyword.text = t; cc.keyword.match_type = E.KeywordMatchTypeEnum.PHRASE; ops.append(op)
if ops: client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"negatives ({len(ops)})", tag)

if sl:
    ops = []
    for s in sl:
        op = client.get_type("CampaignAssetOperation"); op.remove = s.campaign_asset.resource_name; ops.append(op)
    client.get_service("CampaignAssetService").mutate_campaign_assets(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"sitelink unlink ({len(sl)})", tag)

# bidding + enable last, in one campaign mutate
ops = []
for cid in C:
    op = client.get_type("CampaignOperation"); u = op.update
    u.resource_name = ga.campaign_path(CID, cid)
    u.target_spend.cpc_bid_ceiling_micros = int(CAP * 1e6)
    u.status = E.CampaignStatusEnum.ENABLED
    op.update_mask.paths.extend(["target_spend.cpc_bid_ceiling_micros", "status"]); ops.append(op)
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print("Max Clicks $15 cap + ENABLE", tag)

if APPLY:
    print("--- read-back")
    for r in q(f"""SELECT campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.target_spend.cpc_bid_ceiling_micros,
        campaign_budget.amount_micros, campaign.primary_status FROM campaign WHERE campaign.id IN ({ids})"""):
        print(f"   {r.campaign.name}: {r.campaign.status.name} {r.campaign.bidding_strategy_type.name} cap ${r.campaign.target_spend.cpc_bid_ceiling_micros/1e6:.2f} "
              f"${r.campaign_budget.amount_micros/1e6:.2f}/d {r.campaign.primary_status.name}")
    for r in q(f"SELECT campaign.id, ad_group.name, ad_group.status FROM ad_group WHERE campaign.id IN ({ids}) AND ad_group.status = 'ENABLED'"):
        print(f"   live ad group: {C[str(r.campaign.id)]['name']} / {r.ad_group.name}")
    for r in q(f"SELECT ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE ad_group_ad.ad.id IN ({C[HT]['ad'][0]},{C[PL]['ad'][0]})"):
        print(f"   ad {r.ad_group_ad.ad.id}: {r.ad_group_ad.status.name} {r.ad_group_ad.policy_summary.approval_status.name} {list(r.ad_group_ad.ad.final_urls)}")
    print("   kw:", q(f"SELECT ad_group_criterion.status FROM ad_group_criterion WHERE ad_group_criterion.resource_name = '{kw[0].ad_group_criterion.resource_name}'")[0].ad_group_criterion.status.name)
    left = q(f"SELECT campaign.id, asset.id FROM campaign_asset WHERE campaign.id IN ({EAGLE_CAMPS}) AND asset.id IN ({','.join(BAD_SITELINKS)}) AND campaign_asset.status = 'ENABLED'")
    print(f"   Eagle Point sitelinks still linked (Plumbing + old HVAC): {len(left)}")
    for cid, c in C.items():
        got = {k.campaign_criterion.keyword.text.lower() for k in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {cid} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
        print(f"   {c['name']} negatives missing: {[n for n in c['neg'] if n not in got]}")
