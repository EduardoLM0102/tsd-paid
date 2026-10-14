"""Cool Hand 2026-10-10 (Edu's go): Google 'Calls from website' conversion for the go. pages.
ALREADY APPLIED 2026-10-10, don't re-run (it would create a duplicate action).
Google's tag swaps 469-351-1738 on go. pages with a Google forwarding number for ad visitors -> calls forward to
469-351-1738 (CallRail) -> business. Counts website calls >= 60s by campaign/keyword, separate from 'Calls from ads'.
Created SECONDARY (observe only) so Max Conversions bidding doesn't change until Edu decides (taps vs calls double count).
Run: ./tsd.sh <abs path to this file>
"""
import os
import sys
sys.path.insert(0, os.path.expanduser("~/") + "Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
from lib import init_client

CID = "9865206319"
NAME = "[TSD] Calls from website (go.)"
c = init_client(); ga = c.get_service("GoogleAdsService")
E = c.enums

op = c.get_type("ConversionActionOperation"); a = op.create
a.name = NAME
a.type_ = E.ConversionActionTypeEnum.WEBSITE_CALL
a.category = E.ConversionActionCategoryEnum.PHONE_CALL_LEAD
a.status = E.ConversionActionStatusEnum.ENABLED
a.counting_type = E.ConversionActionCountingTypeEnum.ONE_PER_CLICK
a.phone_call_duration_seconds = 60          # same 60s bar as 'Calls from ads'
a.primary_for_goal = False                  # observe only
a.value_settings.default_value = 1
a.value_settings.always_use_default_value = True
rn = c.get_service("ConversionActionService").mutate_conversion_actions(customer_id=CID, operations=[op]).results[0].resource_name
print("created:", rn)

r = list(ga.search(customer_id=CID, query=f"""SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.category,
  conversion_action.origin, conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric,
  conversion_action.phone_call_duration_seconds, conversion_action.tag_snippets FROM conversion_action WHERE conversion_action.resource_name = '{rn}'"""))[0].conversion_action
print("id", r.id, "| category", r.category, "| origin", r.origin, "| primary", r.primary_for_goal, "| in Conversions column", r.include_in_conversions_metric, "| min sec", r.phone_call_duration_seconds)
for s in r.tag_snippets:
    print("---- snippet type", s.type_, "page_format", s.page_format)
    print(s.event_snippet[:900])
