# APPLIED LIVE 2026-11-09 ~08:50 CT on Edu's go, read-back OK on every item. Do NOT re-run with --apply (guards abort anyway).
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Proud Pops (1051843378) + My Favorite Service (9815330464), 2026-11-09. Edu: "Apply all of the fixes, including the My Favorite Service".
From the keyword-level read of 11-04..11-09 (clients/proud-pops/google-ads-log.md, 2026-11-09 later 3).

1. Electrical 23866999121: pause `electrical services` [PHRASE] ($461 / 14 clicks / 0 leads); campaign negatives PHRASE
   'electric company', 'aep', 'hourly rate'.
2. Plumbing 23853484024: pause the generic plumber keywords inside AG1_Plumbing_LeakDetection (`plumber san antonio tx` [PHRASE],
   `plumber near me` [EXACT], `plumber san antonio` [EXACT]); AG4_Plumbing_General keeps the same three. Campaign negatives PHRASE 'cheap', 'saws'.
3. HVAC 23848895678: campaign negative PHRASE 'cheapest'; standard Max Conversions (tCPA $265) -> portfolio Max Conversions with the
   same tCPA and a $30 max CPC ceiling (`ac repair san antonio tx` was paying $53.52 a click).
4. Competitor names seen in the search terms -> the ACCOUNT-LEVEL list 'TSD - Account negatives (job seekers)' 12263521315 (PHRASE).
5. My Favorite Service 9815330464: pause Smart campaign 'HVAC Contractor Services' 23065942452.

HELD, not in this script: the 'commercial' negative on Electrical + HVAC. proudpops.com says "Residential & Commercial" on the homepage
and on the HVAC ad landing page, so it would block a service the client advertises. Edu/AM to decide.

Guards: expected status/text on every keyword, General must hold the same generic keywords, negatives must not contain-match any
enabled keyword in their scope, HVAC must be on standard Max Conversions with no portfolio, list must be attached at account level.
Rollback: re-enable the 4 keywords, remove the negatives, set campaign.bidding_strategy back to standard Maximize Conversions
(tCPA $265), re-enable the Smart campaign.
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

PPC, MFSC = "1051843378", "9815330464"
ELEC, PLUMB, HVAC = "23866999121", "23853484024", "23848895678"
LIST_ID = "12263521315"
AG_ELEC_SERVICES, AG_LEAK, AG_GENERAL = "196768586637", "196726297659", "199626362094"
PAUSE = [  # (ad group id, criterion id, text, match type)
    (AG_ELEC_SERVICES, "95420911", "electrical services", "PHRASE"),
    (AG_LEAK, "354371636767", "plumber san antonio tx", "PHRASE"),
    (AG_LEAK, "21810437552", "plumber near me", "EXACT"),
    (AG_LEAK, "1178376016", "plumber san antonio", "EXACT"),
]
CAMP_NEG = {ELEC: ["electric company", "aep", "hourly rate"], PLUMB: ["cheap", "saws"], HVAC: ["cheapest"]}
ACCOUNT_NEG = ["mesa electrical", "enterprise electrical", "1 tom plumber", "venture plumbing", "amg plumbing", "leaky's plumbing",
               "leakys plumbing", "benchmark plumbing", "bearded plumber", "cowboys heating", "ems hvac", "westerly air",
               "my father's ac", "my fathers ac", "gillette ac", "apollo air"]
HVAC_CEILING, HVAC_TCPA = 30.0, 265.0
PORTFOLIO_NAME = "TSD_ProudPops_HVAC_MaxConv_CPC30"
SMART = "23065942452"
APPLY = "--apply" in sys.argv
vo = not APPLY
tag = "APPLIED" if APPLY else "(validate_only)"

client = init_client()
ga = client.get_service("GoogleAdsService")
MT = client.enums.KeywordMatchTypeEnum
ST = client.enums.AdGroupCriterionStatusEnum


def q(cid, s):
    return list(ga.search(customer_id=cid, query=s))


def contains(term, text):
    return f" {term} " in f" {text.lower()} "


# ---------------- guards ----------------
kw = q(PPC, """SELECT campaign.id, ad_group.id, ad_group_criterion.criterion_id, ad_group_criterion.keyword.text,
    ad_group_criterion.keyword.match_type, ad_group_criterion.status FROM ad_group_criterion
    WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'
    AND ad_group.status = 'ENABLED' AND campaign.status = 'ENABLED'""")
by = {(str(r.ad_group.id), str(r.ad_group_criterion.criterion_id)): r for r in kw}
for ag, crit, text, mt in PAUSE:
    r = by.get((ag, crit))
    if not r: sys.exit(f"ABORT: keyword {crit} in ad group {ag} is not ENABLED (already paused or gone)")
    k = r.ad_group_criterion.keyword
    if k.text != text or k.match_type.name != mt: sys.exit(f"ABORT: {crit} is '{k.text}' [{k.match_type.name}], expected '{text}' [{mt}]")
    if ag == AG_LEAK and (AG_GENERAL, crit) not in by: sys.exit(f"ABORT: '{text}' is not enabled in AG4_Plumbing_General, pausing it would drop the keyword")
    print(f"pause ok: '{text}' [{mt}] in ad group {ag}")
left = [r.ad_group_criterion.keyword.text for r in kw if str(r.ad_group.id) == AG_LEAK and (AG_LEAK, str(r.ad_group_criterion.criterion_id)) not in {(a, c) for a, c, _, _ in PAUSE}]
print(f"Leak Detection keeps {len(left)} keywords: {left}")
if not left: sys.exit("ABORT: Leak Detection would be left with no keywords")

have = {}
for r in q(PPC, f"""SELECT campaign.id, campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id IN ({ELEC},{PLUMB},{HVAC})
        AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE"""):
    have.setdefault(str(r.campaign.id), set()).add(r.campaign_criterion.keyword.text.lower())
camp_new = {}
for cid, terms in CAMP_NEG.items():
    camp_new[cid] = [t for t in terms if t not in have.get(cid, set())]
    for t in camp_new[cid]:
        conf = sorted({r.ad_group_criterion.keyword.text for r in kw if str(r.campaign.id) == cid and contains(t, r.ad_group_criterion.keyword.text)})
        if conf: sys.exit(f"ABORT: negative '{t}' would block enabled keywords in {cid}: {conf}")
    print(f"campaign {cid}: new negatives {camp_new[cid]} (already there: {[t for t in terms if t in have.get(cid, set())]})")

ss = q(PPC, f"SELECT shared_set.resource_name, shared_set.name FROM shared_set WHERE shared_set.id = {LIST_ID}")[0].shared_set
attached = [r for r in q(PPC, """SELECT customer_negative_criterion.negative_keyword_list.shared_set FROM customer_negative_criterion
    WHERE customer_negative_criterion.type = 'NEGATIVE_KEYWORD_LIST'""") if r.customer_negative_criterion.negative_keyword_list.shared_set == ss.resource_name]
if not attached: sys.exit("ABORT: account-level list not attached")
present = {r.shared_criterion.keyword.text.lower() for r in q(PPC, f"SELECT shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.id = {LIST_ID}")}
acct_new = [t for t in ACCOUNT_NEG if t not in present]
allkw = [r.ad_group_criterion.keyword.text for r in q(PPC, """SELECT ad_group_criterion.keyword.text FROM ad_group_criterion
    WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED' AND campaign.status != 'REMOVED'""")]
for t in acct_new:
    conf = sorted({k for k in allkw if contains(t, k)})
    if conf: sys.exit(f"ABORT: account negative '{t}' conflicts with keywords {conf[:5]}")
print(f"account list '{ss.name}': {len(acct_new)} new {acct_new} (already there: {[t for t in ACCOUNT_NEG if t in present]})")

# replay: what would the new negatives have blocked since 09-01 (terms with conversions are the ones to look at)
terms = q(PPC, """SELECT campaign.id, search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.conversions FROM search_term_view
    WHERE segments.date BETWEEN '2026-09-01' AND '2026-11-09' AND metrics.clicks > 0""")
for scope, lst in [(None, acct_new)] + [(cid, v) for cid, v in camp_new.items()]:
    for t in lst:
        hit = [r for r in terms if contains(t, r.search_term_view.search_term) and (scope is None or str(r.campaign.id) == scope)]
        if hit:
            print(f"  replay '{t}' ({'account' if scope is None else scope}): {len(hit)} term rows, {sum(r.metrics.clicks for r in hit)} clicks,"
                  f" ${sum(r.metrics.cost_micros for r in hit)/1e6:.2f}, conv {sum(r.metrics.conversions for r in hit):.1f}"
                  f" e.g. {sorted({r.search_term_view.search_term for r in hit})[:4]}")

hv = q(PPC, f"""SELECT campaign.name, campaign.bidding_strategy_type, campaign.bidding_strategy, campaign.maximize_conversions.target_cpa_micros
    FROM campaign WHERE campaign.id = {HVAC}""")[0].campaign
print(f"HVAC: {hv.bidding_strategy_type.name} portfolio='{hv.bidding_strategy}' tCPA ${hv.maximize_conversions.target_cpa_micros/1e6:.0f}")
if hv.bidding_strategy or hv.bidding_strategy_type.name != "MAXIMIZE_CONVERSIONS": sys.exit("ABORT: HVAC is not on standard Max Conversions")
if abs(hv.maximize_conversions.target_cpa_micros / 1e6 - HVAC_TCPA) > 0.01: sys.exit("ABORT: HVAC tCPA is not $265, someone changed it")
if q(PPC, f"SELECT bidding_strategy.resource_name FROM bidding_strategy WHERE bidding_strategy.name = '{PORTFOLIO_NAME}'"): sys.exit("ABORT: portfolio already exists")

sm = q(MFSC, f"SELECT campaign.name, campaign.status, campaign.advertising_channel_type FROM campaign WHERE campaign.id = {SMART}")[0].campaign
print(f"MFSC: '{sm.name}' {sm.advertising_channel_type.name} {sm.status.name}")
if sm.status.name != "ENABLED": sys.exit("ABORT: Smart campaign is not ENABLED")

# ---------------- writes ----------------
ops = []
for cid, lst in camp_new.items():
    for t in lst:
        op = client.get_type("CampaignCriterionOperation"); c = op.create
        c.campaign = ga.campaign_path(PPC, cid); c.negative = True; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    client.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": PPC, "operations": ops, "validate_only": vo})
print(f"1. {len(ops)} campaign negatives {tag}")

ops = []
for t in acct_new:
    op = client.get_type("SharedCriterionOperation"); c = op.create
    c.shared_set = ss.resource_name; c.keyword.text = t; c.keyword.match_type = MT.PHRASE; ops.append(op)
if ops:
    client.get_service("SharedCriterionService").mutate_shared_criteria(request={"customer_id": PPC, "operations": ops, "validate_only": vo})
print(f"2. {len(ops)} account-level negatives {tag}")

ops = []
for ag, crit, text, mt in PAUSE:
    op = client.get_type("AdGroupCriterionOperation")
    op.update.resource_name = f"customers/{PPC}/adGroupCriteria/{ag}~{crit}"; op.update.status = ST.PAUSED
    op.update_mask.paths.append("status"); ops.append(op)
client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={"customer_id": PPC, "operations": ops, "validate_only": vo})
print(f"3. {len(ops)} keywords paused {tag}")

op = client.get_type("BiddingStrategyOperation"); bs = op.create
bs.name = PORTFOLIO_NAME
bs.maximize_conversions.cpc_bid_ceiling_micros = int(HVAC_CEILING * 1e6)
bs.maximize_conversions.target_cpa_micros = int(HVAC_TCPA * 1e6)
res = client.get_service("BiddingStrategyService").mutate_bidding_strategies(request={"customer_id": PPC, "operations": [op], "validate_only": vo})
print(f"4a. portfolio '{PORTFOLIO_NAME}' (Max Conversions, tCPA ${HVAC_TCPA:.0f}, ceiling ${HVAC_CEILING:.0f}) create {tag}")
if APPLY:
    rn = res.results[0].resource_name
    op = client.get_type("CampaignOperation")
    op.update.resource_name = ga.campaign_path(PPC, HVAC); op.update.bidding_strategy = rn; op.update_mask.paths.append("bidding_strategy")
    client.get_service("CampaignService").mutate_campaigns(request={"customer_id": PPC, "operations": [op]})
    print("4b. HVAC moved to the portfolio APPLIED:", rn)

op = client.get_type("CampaignOperation")
op.update.resource_name = ga.campaign_path(MFSC, SMART); op.update.status = client.enums.CampaignStatusEnum.PAUSED
op.update_mask.paths.append("status")
client.get_service("CampaignService").mutate_campaigns(request={"customer_id": MFSC, "operations": [op], "validate_only": vo})
print(f"5. MFSC Smart campaign pause {tag}")

# ---------------- read-back ----------------
if APPLY:
    print("--- read-back")
    for r in q(PPC, f"""SELECT ad_group.name, ad_group_criterion.criterion_id, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
            ad_group_criterion.status FROM ad_group_criterion WHERE ad_group.id IN ({AG_ELEC_SERVICES},{AG_LEAK},{AG_GENERAL})
            AND ad_group_criterion.criterion_id IN ({",".join(c for _, c, _, _ in PAUSE)}) AND ad_group_criterion.negative = FALSE"""):
        k = r.ad_group_criterion
        print(f"   {r.ad_group.name:28s} '{k.keyword.text}' [{k.keyword.match_type.name}] {k.status.name}")
    got = {}
    for r in q(PPC, f"""SELECT campaign.id, campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id IN ({ELEC},{PLUMB},{HVAC})
            AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE"""):
        got.setdefault(str(r.campaign.id), set()).add(r.campaign_criterion.keyword.text.lower())
    for cid, lst in CAMP_NEG.items():
        print(f"   campaign {cid} negatives: {len(got.get(cid, ()))} total; missing: {[t for t in lst if t not in got.get(cid, set())]}")
    lst_now = {r.shared_criterion.keyword.text.lower() for r in q(PPC, f"SELECT shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.id = {LIST_ID}")}
    print(f"   account list: {len(lst_now)} terms; missing: {[t for t in ACCOUNT_NEG if t not in lst_now]}")
    r = q(PPC, f"""SELECT campaign.name, campaign.bidding_strategy_type, campaign.bidding_strategy, campaign.primary_status,
        bidding_strategy.name, bidding_strategy.maximize_conversions.cpc_bid_ceiling_micros, bidding_strategy.maximize_conversions.target_cpa_micros
        FROM campaign WHERE campaign.id = {HVAC}""")[0]
    print(f"   {r.campaign.name}: {r.campaign.bidding_strategy_type.name} via '{r.bidding_strategy.name}' ceiling ${r.bidding_strategy.maximize_conversions.cpc_bid_ceiling_micros/1e6:.0f}"
          f" tCPA ${r.bidding_strategy.maximize_conversions.target_cpa_micros/1e6:.0f} primary {r.campaign.primary_status.name}")
    r = q(MFSC, f"SELECT campaign.name, campaign.status, campaign.primary_status FROM campaign WHERE campaign.id = {SMART}")[0].campaign
    print(f"   MFSC '{r.name}': {r.status.name} primary {r.primary_status.name}")
