# APPLIED LIVE 2026-11-11 10:21 BRT (Edu: "Execute 1 to 3"). 39 non-brand keywords PAUSED, 16 brand keywords left ENABLED (read-back OK). Re-running pauses nothing new.
"""Nick's (1854100356): Branded 23675600637 ("Branded Evergreen Mix", Max Conversions, $100/day) holds ~50 NON-brand keywords, almost all BROAD
('heating repair hammond', 'residential hvac companies', 'heating company near me', 'ac repair hammond la' broad...). On 10-21 only 'hvac contractors
near me' was paused. In heating season those broad keywords are now getting impressions (11-04..11-10: 'ac repair hammond la' 42, 'heating repair
hammond' 32, 'residential hvac companies' 22) and losing 50-80% to rank, which is why 'Branded' reads IS 40% while the real brand keywords sit at
83-100%. They would also compete with the new NB heating ad group.
PAUSE every keyword in Branded whose text does not contain 'nick'. Brand keywords untouched. Budget untouched (spends ~$5/day of $100).
Rollback = re-enable the printed list."""
import sys
sys.path.insert(0, ".")
from lib import init_client

CID, BR = "1854100356", "23675600637"
APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
q = lambda s: list(ga.search(customer_id=CID, query=s))

rows = q(f"""SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status
    FROM ad_group_criterion WHERE campaign.id = {BR} AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE
    AND ad_group_criterion.status = 'ENABLED'""")
keep = [r for r in rows if "nick" in r.ad_group_criterion.keyword.text.lower()]
pause = [r for r in rows if "nick" not in r.ad_group_criterion.keyword.text.lower()]
print(f"Branded enabled keywords: {len(rows)} | keep (brand): {len(keep)} | pause (non-brand): {len(pause)}")
print("keep:", [f"{r.ad_group_criterion.keyword.text} [{r.ad_group_criterion.keyword.match_type.name[:1]}]" for r in keep])
print("pause:", [f"{r.ad_group_criterion.keyword.text} [{r.ad_group_criterion.keyword.match_type.name[:1]}]" for r in pause])
if not keep: sys.exit("ABORT: no brand keyword would remain")
ops = []
for r in pause:
    op = client.get_type("AdGroupCriterionOperation"); op.update.resource_name = r.ad_group_criterion.resource_name
    op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED; op.update_mask.paths.append("status"); ops.append(op)
client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(request={"customer_id": CID, "operations": ops, "validate_only": not APPLY})
print(f"pause {len(ops)} ok", "APPLIED" if APPLY else "(validate_only)")
if APPLY:
    left = q(f"""SELECT ad_group_criterion.keyword.text FROM ad_group_criterion WHERE campaign.id = {BR} AND ad_group_criterion.type = 'KEYWORD'
        AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'""")
    print("read-back enabled:", [r.ad_group_criterion.keyword.text for r in left])
