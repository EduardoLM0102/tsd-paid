# APPLIED LIVE 2026-10-16 on Edu's go ("Go ahead and apply all fixes"). Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""All Seasons AC PPC (4467722415), 2026-10-16, Edu's go ("Go ahead and apply all fixes") after the Oct 1-15
search-term diagnosis (62% of visible search-term spend on other companies' names, matched to CallRail transcripts).
1. 'call extension LEAD' (AD_CALL 497046840, the account-level + call-asset call conversion) min call 1s -> 60s.
2. Pause live competitor / product-shopper / job-title keywords (T.F. O'Brien, portable AC, 'mechanics and installers').
3. PHRASE negatives (competitors, oil delivery, retail/parts, jobs) on the 3 enabled Search campaigns, skipping ones present.
4. Geo target type PRESENCE_OR_INTEREST -> PRESENCE on Nonbranded (enabled) + 2 paused campaigns that still had it.
NOT done here (UI only / conflicts with Edu's 10-09 rule on C&S): 'Click to call' taps -> secondary.
Guards: aborts on unexpected current values; replays negatives against 30d search terms + active keywords first.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "4467722415"
LEADGEN, NB, MINI = "11803942938", "23813282398", "24050402045"
GEO_FIX = ["23813282398", "24202454875", "23699717251"]
CALL_CA, CALL_OLD, CALL_NEW = "497046840", 1, 60
PAUSE_KW = [("tf o brien", "PHRASE"), ("t f o brien & co inc", "PHRASE"), ("portable ac", "BROAD"),
            ("chilwell portable ac", "BROAD"), ("haier air conditioner portable", "EXACT"),
            ("costco portable air conditioner", "EXACT"), ("arctic wind portable air conditioner", "EXACT"),
            ("arctos portable ac where to buy", "EXACT"), ("heating and air conditioning mechanics and installers", "BROAD"),
            ("buy furnace air filters", "PHRASE"), ("used air conditioner for sale near me", "EXACT")]
NEG = ["petro", "gallett", "gallettair", "galette", "o brien", "obrien", "meenan", "slomin", "slomins", "kolb",
       "aircomfort", "traeger", "haviland", "kelly air", "burke energy", "burts", "burt's", "moses mechanical",
       "superior air conditioning", "sal manzo", "country wide heating", "appolo", "five star mechanical",
       "richards heating", "rigney", "perillo", "universal plumbing", "accurate mechanical", "american hvac",
       "great neck electric", "sunny hvac",
       "heating oil", "oil delivery", "oil company", "oil companies",
       "portable", "for sale", "parts", "hvac supply", "supplies", "customer service", "buy freon", "407c", "freon 22", "r22",
       "air filters", "filterbuy", "lowes", "home depot", "costco", "walmart",
       "jobs", "hiring", "careers", "mechanics and installers"]
APPLY = "--apply" in sys.argv
vo = not APPLY

client = init_client()
ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))
MT = client.enums.KeywordMatchTypeEnum
ST = client.enums.AdGroupCriterionStatusEnum
GT = client.enums.PositiveGeoTargetTypeEnum
CAMPS = [LEADGEN, NB, MINI]

# --- guards
ca = q(f"SELECT conversion_action.resource_name, conversion_action.name, conversion_action.phone_call_duration_seconds FROM conversion_action WHERE conversion_action.id = {CALL_CA}")[0].conversion_action
print(f"conversion '{ca.name}': min call {ca.phone_call_duration_seconds}s")
if ca.phone_call_duration_seconds != CALL_OLD: sys.exit(f"ABORT: expected {CALL_OLD}s")

kws = q(f"""SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
    ad_group_criterion.status, campaign.id, campaign.name, ad_group.name, ad_group.status FROM ad_group_criterion
    WHERE campaign.id IN ({','.join(CAMPS)}) AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
    AND ad_group_criterion.status = 'ENABLED'""")
to_pause = [k for k in kws if (k.ad_group_criterion.keyword.text.lower(), k.ad_group_criterion.keyword.match_type.name) in PAUSE_KW]
print(f"keywords to pause: {[(k.ad_group_criterion.keyword.text, k.ad_group_criterion.keyword.match_type.name, k.campaign.name[:24]) for k in to_pause]}")
missing = [p for p in PAUSE_KW if p not in {(k.ad_group_criterion.keyword.text.lower(), k.ad_group_criterion.keyword.match_type.name) for k in to_pause}]
if missing: print(f"  (not found enabled, skipped: {missing})")
pause_rns = {k.ad_group_criterion.resource_name for k in to_pause}
active = {}
for k in kws:
    if k.ad_group_criterion.resource_name in pause_rns: continue
    active.setdefault(str(k.campaign.id), []).append(k.ad_group_criterion.keyword.text.lower())

neg_plan = {}
for cid in CAMPS:
    existing = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
        WHERE campaign.id = {cid} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
    neg_plan[cid] = [n for n in NEG if n not in existing]
    print(f"campaign {cid}: {len(neg_plan[cid])} new negatives (already present: {[n for n in NEG if n in existing]})")

terms = q(f"""SELECT campaign.id, search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
    WHERE campaign.id IN ({','.join(CAMPS)}) AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0""")
all_conflicts = []
for n in NEG:
    hit = [r for r in terms if f" {n} " in f" {r.search_term_view.search_term.lower()} "]
    conflicts = sorted({k for cid in CAMPS for k in active.get(cid, []) if f" {n} " in f" {k} " and n in neg_plan[cid]})
    print(f"  neg '{n}': blocks {len(hit)} terms ${sum(r.metrics.cost_micros for r in hit)/1e6:.2f} conv {sum(r.metrics.conversions for r in hit):.1f}"
          f"{' e.g. ' + str(sorted({r.search_term_view.search_term for r in hit})[:3]) if hit else ''}{' KW CONFLICT ' + str(conflicts) if conflicts else ''}")
    if conflicts: all_conflicts.extend(conflicts)
if all_conflicts:
    for k in kws:
        if k.ad_group_criterion.keyword.text.lower() in all_conflicts and k.ad_group_criterion.resource_name not in pause_rns:
            print(f"  conflict kw: '{k.ad_group_criterion.keyword.text}' {k.ad_group_criterion.keyword.match_type.name} | {k.campaign.name} / {k.ad_group.name}")
    sys.exit("ABORT: negatives conflict with active keywords (listed above)")

geo = {str(r.campaign.id): r for r in q(f"""SELECT campaign.id, campaign.name, campaign.status, campaign.geo_target_type_setting.positive_geo_target_type
    FROM campaign WHERE campaign.id IN ({','.join(GEO_FIX)})""")}
for cid in GEO_FIX:
    r = geo[cid]; print(f"geo {r.campaign.name} ({r.campaign.status.name}): {r.campaign.geo_target_type_setting.positive_geo_target_type.name}")

# --- 1. call conversion threshold
op = client.get_type("ConversionActionOperation")
op.update.resource_name = ca.resource_name; op.update.phone_call_duration_seconds = CALL_NEW
op.update_mask.paths.append("phone_call_duration_seconds")
client.get_service("ConversionActionService").mutate_conversion_actions(request={"customer_id": CID, "operations": [op], "validate_only": vo})
print("call threshold ok", "(validate_only)" if vo else "APPLIED")

# --- 2. pause keywords
ops = []
for k in to_pause:
    op = client.get_type("AdGroupCriterionOperation")
    op.update.resource_name = k.ad_group_criterion.resource_name; op.update.status = ST.PAUSED
    op.update_mask.paths.append("status"); ops.append(op)
if ops: client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} keywords paused", "(validate_only)" if vo else "APPLIED")

# --- 3. negatives
ops = []
for cid, items in neg_plan.items():
    for t in items:
        op = client.get_type("CampaignCriterionOperation"); c = op.create
        c.campaign = ga.campaign_path(CID, cid); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops: client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} negatives ok", "(validate_only)" if vo else "APPLIED")

# --- 4. geo presence only
ops = []
for cid in GEO_FIX:
    if geo[cid].campaign.geo_target_type_setting.positive_geo_target_type.name == "PRESENCE": continue
    op = client.get_type("CampaignOperation")
    op.update.resource_name = ga.campaign_path(CID, cid)
    op.update.geo_target_type_setting.positive_geo_target_type = GT.PRESENCE
    op.update_mask.paths.append("geo_target_type_setting.positive_geo_target_type"); ops.append(op)
if ops: client.get_service("CampaignService").mutate_campaigns(request={"customer_id": CID, "operations": ops, "validate_only": vo})
print(f"{len(ops)} campaigns geo -> PRESENCE", "(validate_only)" if vo else "APPLIED")

if APPLY:
    print("--- read-back")
    print("   call min:", q(f"SELECT conversion_action.phone_call_duration_seconds FROM conversion_action WHERE conversion_action.id = {CALL_CA}")[0].conversion_action.phone_call_duration_seconds, "s")
    st = {r.ad_group_criterion.resource_name: r.ad_group_criterion.status.name for r in q(f"""SELECT ad_group_criterion.resource_name, ad_group_criterion.status
        FROM ad_group_criterion WHERE campaign.id IN ({','.join(CAMPS)}) AND ad_group_criterion.type = 'KEYWORD'""")}
    print("   paused:", sum(1 for rn in pause_rns if st.get(rn) == "PAUSED"), "of", len(pause_rns))
    for cid in CAMPS:
        got = {r.campaign_criterion.keyword.text.lower() for r in q(f"""SELECT campaign_criterion.keyword.text FROM campaign_criterion
            WHERE campaign.id = {cid} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
        print(f"   {cid} negatives missing: {[n for n in NEG if n not in got]}")
    for r in q(f"SELECT campaign.name, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.id IN ({','.join(GEO_FIX)})"):
        print(f"   geo {r.campaign.name}: {r.campaign.geo_target_type_setting.positive_geo_target_type.name}")
