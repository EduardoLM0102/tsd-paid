# APPLIED LIVE 2026-11-11 09:52 BRT (Edu: "Execute B" + "Execute C"), read-back $50.00 on both. Do NOT re-run with --apply (guards skip: budgets no longer $1.43 / $1,429).
"""Integrate Comfort LSA budgets, 2026-11-11:
 B. LSA Belleville 2895702982, campaign 15786867110: $1.43 (= $10/week) -> $50.00/day (May 2026 level: 30 leads on $1,435). Aborts unless the
    budget is still under $2, not shared, and the API insurance status is PASSED. Angela is asked in parallel (AT draft) whether the
    client wants Belleville back; PMax + NB paused the same morning ($62/day), so total paid goes DOWN.
 C. LSA Englewood Cliffs 8323145223, campaign 21467507022: $1,429 -> $50.00/day (never served, 0 impressions ever; cap it before
    it ever does). Aborts unless the budget is still above $1,000 and not shared.
Each block skips on its own abort so the other still runs."""
import sys
sys.path.insert(0, ".")
from lib import init_client

APPLY = "--apply" in sys.argv
client = init_client(); ga = client.get_service("GoogleAdsService")
JOBS = [  # (label, customer_id, campaign_id, expected_now_check, new_daily)
    ("B Belleville", "2895702982", "15786867110", lambda v: v < 2.00, 50.00),
    ("C Englewood Cliffs", "8323145223", "21467507022", lambda v: v > 1000, 50.00),
]
for label, cid, camp, ok_now, new in JOBS:
    print(f"\n== {label} ({cid} / {camp})")
    q = lambda s: list(ga.search(customer_id=cid, query=s))
    try:
        ins = q("SELECT customer.local_services_settings.granular_insurance_statuses FROM customer")[0].customer.local_services_settings.granular_insurance_statuses
        print("  insurance:", [(s.category_id, s.verification_status.name) for s in ins])
    except Exception as e:
        ins = []; print("  insurance: (not readable)", str(e).splitlines()[0][:100])
    if label.startswith("B") and (not ins or any(s.verification_status.name != "PASSED" for s in ins)):
        print("  SKIP: insurance not PASSED in the API"); continue
    b = q(f"SELECT campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared, campaign_budget.period FROM campaign WHERE campaign.id = {camp}")[0].campaign_budget
    now = b.amount_micros / 1e6
    print(f"  budget now ${now:,.2f} {b.period.name} shared={b.explicitly_shared}")
    if b.explicitly_shared or not ok_now(now):
        print("  SKIP: budget not at the expected value or shared"); continue
    op = client.get_type("CampaignBudgetOperation")
    op.update.resource_name = b.resource_name; op.update.amount_micros = int(new * 1e6); op.update_mask.paths.append("amount_micros")
    client.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": cid, "operations": [op], "validate_only": not APPLY})
    print(f"  budget -> ${new:.2f}", "APPLIED" if APPLY else "(validate_only)")
    if APPLY:
        print("  read-back: $%.2f" % (q(f"SELECT campaign_budget.amount_micros FROM campaign WHERE campaign.id = {camp}")[0].campaign_budget.amount_micros / 1e6))
