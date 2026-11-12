# APPLIED LIVE 2026-11-06, read-back confirmed. Do NOT re-run with --apply.
# Run from google-ads-ratos/scripts: ./tsd.sh <abs path to this file>   (validate-only without --apply)
"""Lilypad Septic (3797438623), 2026-11-06 account-audit fixes. Approved by Edu in chat ("Work on the fixes please").
1. Account sitelink 'Contact Us' -> https://www.lilypadseptic.com/contact/ (was RYNO LP service.lilypadseptic.com/lp/...,
   which runs RYNO's GTM-KQJ9K783 with no Google Ads conversion tag; forms there were never counted).
   Account sitelink 'Specials' UNLINKED from the account (same RYNO LP; the site's own /specials/ page only lists
   offers that expired 2026-10-31, so it is not repointed there).
2. Portable Restroom Rental RSA final URL -> https://www.lilypadseptic.com/portable-restrooms/ (was /get-septic-services/).
   Same GHL form + GTM-KG7WCQN listener (All Pages) on that page.
3. Keyword bids to first-page estimate (0 impressions in 30d at current bid): septic repair $6->$9,
   septic emergency service $6->$8, new septic tank installation $7->$8.
4. Brand misspellings: Branded 'Brand Terms' + 'lilly pad septic' PHRASE and 'salina septic' EXACT ($2.50, same as other
   brand kws). NonBranded campaign negatives 'lilly pad' BROAD (mirrors existing 'lily pad'/'lilypad') + 'salina septic' EXACT.
5. Pause 'septic tank installation cost' (QS 2, $46.58 / 0 conv in 30d).
6. NonBranded PHRASE negative 'how to install' (DIY, $14 / 0 conv).
"""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID = "3797438623"
BR, NB = "24153698844", "24164203087"
APPLY = "--apply" in sys.argv
VO = not APPLY
tag = "APPLIED" if APPLY else "(validate_only)"
c = init_client(); ga = c.get_service("GoogleAdsService"); E = c.enums
def q(s): return list(ga.search(customer_id=CID, query=s))

# ---------- 1. sitelinks
links = q("""SELECT customer_asset.resource_name, customer_asset.status, asset.id, asset.resource_name,
    asset.sitelink_asset.link_text, asset.final_urls FROM customer_asset
    WHERE customer_asset.field_type = 'SITELINK' AND customer_asset.status = 'ENABLED'""")
by_text = {r.asset.sitelink_asset.link_text: r for r in links}
for t in ("Contact Us", "Specials"):
    if t not in by_text: sys.exit(f"ABORT: sitelink '{t}' not found")
    if "service.lilypadseptic.com/lp/" not in by_text[t].asset.final_urls[0]:
        sys.exit(f"ABORT: '{t}' no longer points at the RYNO LP: {list(by_text[t].asset.final_urls)}")
# make sure neither asset is linked anywhere else
for res in ("campaign_asset", "ad_group_asset"):
    for t in ("Contact Us", "Specials"):
        other = q(f"SELECT {res}.resource_name FROM {res} WHERE asset.id = {by_text[t].asset.id} AND {res}.status != 'REMOVED'")
        if other: print(f"   note: '{t}' also linked at {res}: {[o for o in other]}")
op = c.get_type("AssetOperation")
op.update.resource_name = by_text["Contact Us"].asset.resource_name
op.update.final_urls.append("https://www.lilypadseptic.com/contact/")
op.update_mask.paths.append("final_urls")
c.get_service("AssetService").mutate_assets(request={"customer_id": CID, "operations": [op], "validate_only": VO})
print(f"1a. 'Contact Us' final URL -> /contact/ {tag}")
op = c.get_type("CustomerAssetOperation")
op.remove = by_text["Specials"].customer_asset.resource_name
c.get_service("CustomerAssetService").mutate_customer_assets(request={"customer_id": CID, "operations": [op], "validate_only": VO})
print(f"1b. 'Specials' unlinked from account {tag}")

# ---------- 2. restroom RSA final URL
ads = q(f"""SELECT ad_group.name, ad_group_ad.ad.resource_name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ad_group_ad.status
    FROM ad_group_ad WHERE campaign.id = {NB} AND ad_group.name = 'Portable Restroom Rental' AND ad_group_ad.status = 'ENABLED'""")
if len(ads) != 1: sys.exit(f"ABORT: expected 1 enabled restroom ad, found {len(ads)}")
ad = ads[0].ad_group_ad.ad
if list(ad.final_urls) != ["https://www.lilypadseptic.com/get-septic-services/"]: sys.exit(f"ABORT: restroom ad URL is {list(ad.final_urls)}")
op = c.get_type("AdOperation")
op.update.resource_name = ad.resource_name
op.update.final_urls.append("https://www.lilypadseptic.com/portable-restrooms/")
op.update_mask.paths.append("final_urls")
c.get_service("AdService").mutate_ads(request={"customer_id": CID, "operations": [op], "validate_only": VO})
print(f"2. restroom ad {ad.id} final URL -> /portable-restrooms/ {tag}")

# ---------- 3 + 5. keyword bids / pause
kws = q(f"""SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
    ad_group_criterion.cpc_bid_micros, ad_group_criterion.effective_cpc_bid_micros, ad_group_criterion.status, ad_group.name
    FROM ad_group_criterion WHERE campaign.id = {NB} AND ad_group_criterion.type = 'KEYWORD'
    AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED'""")
kw = {r.ad_group_criterion.keyword.text: r.ad_group_criterion for r in kws}
BIDS = {"septic repair": (6.0, 9.0), "septic emergency service": (6.0, 8.0), "new septic tank installation": (7.0, 8.0)}
ops = []
for t, (old, new) in BIDS.items():
    k = kw.get(t)
    if not k: sys.exit(f"ABORT: keyword '{t}' not found")
    if abs(k.effective_cpc_bid_micros / 1e6 - old) > 0.01: sys.exit(f"ABORT: '{t}' bid is ${k.effective_cpc_bid_micros/1e6:.2f}, expected ${old:.2f}")
    op = c.get_type("AdGroupCriterionOperation"); op.update.resource_name = k.resource_name
    op.update.cpc_bid_micros = int(new * 1e6); op.update_mask.paths.append("cpc_bid_micros"); ops.append(op)
k = kw.get("septic tank installation cost")
if not k or k.status != E.AdGroupCriterionStatusEnum.ENABLED: sys.exit("ABORT: 'septic tank installation cost' not found/enabled")
op = c.get_type("AdGroupCriterionOperation"); op.update.resource_name = k.resource_name
op.update.status = E.AdGroupCriterionStatusEnum.PAUSED; op.update_mask.paths.append("status"); ops.append(op)
c.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops, "validate_only": VO})
print(f"3. bids: septic repair $9, septic emergency service $8, new septic tank installation $8 {tag}")
print(f"5. paused 'septic tank installation cost' {tag}")

# ---------- 4a. Branded keywords
ag = q(f"SELECT ad_group.resource_name FROM ad_group WHERE campaign.id = {BR} AND ad_group.name = 'Brand Terms' AND ad_group.status = 'ENABLED'")
if len(ag) != 1: sys.exit("ABORT: Brand Terms ad group not found")
have_br = {(r.ad_group_criterion.keyword.text, r.ad_group_criterion.keyword.match_type.name) for r in q(f"""SELECT ad_group_criterion.keyword.text,
    ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE campaign.id = {BR} AND ad_group_criterion.type = 'KEYWORD'
    AND ad_group_criterion.status != 'REMOVED'""")}
ops = []
for t, mt in (("lilly pad septic", "PHRASE"), ("salina septic", "EXACT")):
    if (t, mt) in have_br: print(f"   '{t}' {mt} already in Branded, skip"); continue
    op = c.get_type("AdGroupCriterionOperation"); x = op.create
    x.ad_group = ag[0].ad_group.resource_name; x.status = E.AdGroupCriterionStatusEnum.ENABLED
    x.keyword.text = t; x.keyword.match_type = getattr(E.KeywordMatchTypeEnum, mt); x.cpc_bid_micros = 2_500_000
    ops.append(op)
if ops:
    c.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops, "validate_only": VO})
print(f"4a. Branded +{len(ops)} keywords {tag}")

# ---------- 4b + 6. NonBranded negatives, with safety replay
terms = q(f"""SELECT search_term_view.search_term, metrics.conversions, metrics.cost_micros FROM search_term_view
    WHERE campaign.id = {NB} AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0""")
live_kws = [t.lower() for t, r in kw.items() if r.status == E.AdGroupCriterionStatusEnum.ENABLED]
have_neg = {(r.campaign_criterion.keyword.text.lower(), r.campaign_criterion.keyword.match_type.name) for r in q(f"""SELECT
    campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion WHERE campaign.id = {NB}
    AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'""")}
NEGS = [("lilly pad", "BROAD"), ("salina septic", "EXACT"), ("how to install", "PHRASE")]
def blocks(neg, mt, term):
    t = term.lower()
    if mt == "EXACT": return t == neg
    if mt == "PHRASE": return f" {neg} " in f" {t} "
    return all(w in t.split() for w in neg.split())
ops = []
for n, mt in NEGS:
    hit = [r for r in terms if blocks(n, mt, r.search_term_view.search_term)]
    conf = [k for k in live_kws if blocks(n, mt, k)]
    print(f"   neg '{n}' {mt}: blocks {len(hit)} terms ${sum(h.metrics.cost_micros for h in hit)/1e6:.2f} "
          f"conv {sum(h.metrics.conversions for h in hit):.1f} {[h.search_term_view.search_term for h in hit][:6]}; kw conflicts {conf}")
    if conf: sys.exit("ABORT: negative conflicts with a live keyword")
    if (n, mt) in have_neg: print("     already there, skip"); continue
    op = c.get_type("CampaignCriterionOperation"); x = op.create
    x.campaign = ga.campaign_path(CID, NB); x.negative = True; x.keyword.text = n; x.keyword.match_type = getattr(E.KeywordMatchTypeEnum, mt)
    ops.append(op)
if ops:
    c.get_service("CampaignCriterionService").mutate_campaign_criteria(request={"customer_id": CID, "operations": ops, "validate_only": VO})
print(f"4b/6. NonBranded +{len(ops)} negatives {tag}")

# ---------- read-back
if APPLY:
    print("\n--- READ-BACK")
    for r in q("""SELECT asset.sitelink_asset.link_text, asset.final_urls, customer_asset.status FROM customer_asset
        WHERE customer_asset.field_type = 'SITELINK' AND customer_asset.status != 'REMOVED'"""):
        print(f"   sitelink {r.asset.sitelink_asset.link_text}: {list(r.asset.final_urls)} {r.customer_asset.status.name}")
    for r in q(f"""SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.approval_status
        FROM ad_group_ad WHERE campaign.id = {NB} AND ad_group_ad.status = 'ENABLED'"""):
        print(f"   ad {r.ad_group.name}: {list(r.ad_group_ad.ad.final_urls)} {r.ad_group_ad.policy_summary.approval_status.name}")
    for r in q(f"""SELECT campaign.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
        ad_group_criterion.effective_cpc_bid_micros, ad_group_criterion.status FROM ad_group_criterion
        WHERE campaign.id IN ({BR}, {NB}) AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
        AND ad_group_criterion.keyword.text IN ('septic repair','septic emergency service','new septic tank installation',
        'septic tank installation cost','lilly pad septic','salina septic')"""):
        k = r.ad_group_criterion
        print(f"   kw {r.campaign.name[:22]} {k.keyword.text} {k.keyword.match_type.name} ${k.effective_cpc_bid_micros/1e6:.2f} {k.status.name}")
    for r in q(f"""SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion
        WHERE campaign.id = {NB} AND campaign_criterion.negative = TRUE AND campaign_criterion.keyword.text IN ('lilly pad','salina septic','how to install')"""):
        print(f"   NB neg {r.campaign_criterion.keyword.text} {r.campaign_criterion.keyword.match_type.name}")
