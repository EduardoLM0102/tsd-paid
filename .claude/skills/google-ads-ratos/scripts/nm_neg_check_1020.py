import sys, os
sys.path.insert(0, os.getcwd())
from lib import init_client
c = init_client(); ga = c.get_service("GoogleAdsService"); cid = "7953905280"
def q(s):
    return [r for b in ga.search_stream(customer_id=cid, query=s) for r in b.results]
print("== campaigns")
for r in q("SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type FROM campaign WHERE campaign.status != 'REMOVED'"):
    print(r.campaign.id, r.campaign.name, r.campaign.status.name, r.campaign.advertising_channel_type.name)
print("== campaign negatives matching tree")
for r in q("SELECT campaign.name, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion WHERE campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'"):
    if 'tree' in r.campaign_criterion.keyword.text.lower(): print(r.campaign.name, r.campaign_criterion.keyword.text, r.campaign_criterion.keyword.match_type.name)
print("== adgroup negatives matching tree")
for r in q("SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE ad_group_criterion.negative = TRUE AND ad_group_criterion.type = 'KEYWORD'"):
    if 'tree' in r.ad_group_criterion.keyword.text.lower(): print(r.campaign.name, r.ad_group.name, r.ad_group_criterion.keyword.text)
print("== shared lists")
for r in q("SELECT shared_set.id, shared_set.name, shared_set.type, shared_set.status FROM shared_set WHERE shared_set.type = 'NEGATIVE_KEYWORDS'"):
    print(r.shared_set.id, r.shared_set.name, r.shared_set.status.name)
for r in q("SELECT shared_set.name, shared_criterion.keyword.text, shared_criterion.keyword.match_type FROM shared_criterion WHERE shared_criterion.type = 'KEYWORD'"):
    if 'tree' in r.shared_criterion.keyword.text.lower(): print("shared:", r.shared_set.name, r.shared_criterion.keyword.text)
for r in q("SELECT campaign.name, shared_set.name FROM campaign_shared_set WHERE campaign_shared_set.status = 'ENABLED'"):
    print("attached:", r.campaign.name, "<-", r.shared_set.name)
print("== search terms w/ tree place, 30d")
for r in q("SELECT campaign.name, search_term_view.search_term, metrics.clicks, metrics.cost_micros FROM search_term_view WHERE segments.date DURING LAST_30_DAYS"):
    t=r.search_term_view.search_term.lower()
    if 'tree place' in t or 'treeplace' in t: print(r.campaign.name, t, r.metrics.clicks, r.metrics.cost_micros/1e6)
