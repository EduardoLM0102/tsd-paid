#!/usr/bin/env python3
"""
Proud Pops — Step 1 launch (2026-07-30)
Account 1051843378 (PPC)

Order matters: negatives go in BEFORE budgets, budgets before the HVAC enable,
so the new campaign launches already protected.

  1. Attach shared negative list CSMS_Negatives to the 3 nonbranded Search campaigns
  2. Add campaign-level negatives for the gaps CSMS_Negatives does not cover
  3. Set step-1 budgets
  4. Enable Search Nonbranded HVAC

Run:  ./tsd.sh <path>/step1_launch_2026-07-30.py            (dry run, default)
      ./tsd.sh <path>/step1_launch_2026-07-30.py --apply    (writes)
"""
import sys, os, argparse

SKILL = os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts")
sys.path.insert(0, SKILL)
import lib

CID = "1051843378"

SEARCH_PLUMBING   = "23853484024"
SEARCH_ELECTRICAL = "23866999121"
SEARCH_HVAC       = "23848895678"

NONBRANDED = [SEARCH_PLUMBING, SEARCH_ELECTRICAL, SEARCH_HVAC]

# --- 2. Negatives CSMS_Negatives does NOT cover (verified 2026-07-30) ---

# Own brand — 0 hits in the shared list. Brand belongs in the Branded campaign,
# not paying $28-38/click here.
OWN_BRAND = ["proud pops", "problem solvers"]

# Competitor/junk terms absent from the shared list, seen spending Jul 22-29.
# NOTE: 'pops heating and air' is deliberately EXCLUDED - distinct company, but it
# collides with Proud Pops brand recall and a negative here may block real brand
# searches. Needs a human call before it goes in.
MISSING_COMPETITORS = [
    "quan air",
    "elmer zubiate",
    "mr electric",
    "mr sparky",
    "allgood electric",
    "handyman",
]

# Cross-service: per campaign, block the other two trades.
CROSS_SERVICE = {
    SEARCH_ELECTRICAL: ["hvac", "plumbing", "plumber", "air conditioning", "ac repair",
                        "water heater", "furnace", "drain", "sewer", "heating"],
    SEARCH_PLUMBING:   ["hvac", "air conditioning", "ac repair", "electrician",
                        "electrical", "furnace"],
    SEARCH_HVAC:       ["plumbing", "plumber", "electrician", "electrical",
                        "drain", "sewer", "water heater"],
}

# --- 3. Step-1 budgets (dollars/day) ---
# Deliberate: Plumbing held flat at $60 despite 44.4% budget-lost share - $225 CPA
# on 3 conversions, 40.6% still rank-lost, routing service queries to the homepage.
# HVAC Search opens at $150 not $250: brand-new Max Conversions campaign, zero
# conversion history. Steps to $250 on Aug 8.
BUDGETS = {
    "23853595615": (80,  130, "PMax HVAC"),
    "23866982084": (60,  110, "PMax Electrical"),
    SEARCH_ELECTRICAL: (50, 75, "Search Nonbranded Electrical"),
    SEARCH_HVAC:  (100, 150, "Search Nonbranded HVAC (relaunch)"),
    # SEARCH_PLUMBING intentionally unchanged at $60
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually write (default: dry run)")
    args = ap.parse_args()
    apply = args.apply
    tag = "APPLY" if apply else "DRY RUN"

    client = lib.init_client()
    ga = client.get_service("GoogleAdsService")

    print(f"\n=== Proud Pops step 1 — {tag} — account {CID} ===\n")

    # ---------- 1. attach shared negative list ----------
    rows = lib.run_query(CID, """
        SELECT shared_set.id, shared_set.resource_name, shared_set.name, shared_set.member_count
        FROM shared_set WHERE shared_set.name = 'CSMS_Negatives'
    """)
    shared_rn = rows[0]["shared_set"]["resource_name"]
    print(f"[1] CSMS_Negatives = {shared_rn} ({rows[0]['shared_set']['member_count']} members)")

    already = lib.run_query(CID, """
        SELECT campaign.id, shared_set.name FROM campaign_shared_set
        WHERE shared_set.name = 'CSMS_Negatives'
    """)
    attached = {r["campaign"]["id"] for r in already}

    css_service = client.get_service("CampaignSharedSetService")
    ops = []
    for camp in NONBRANDED:
        if camp in attached:
            print(f"    - {camp}: already attached, skip")
            continue
        op = client.get_type("CampaignSharedSetOperation")
        op.create.campaign = ga.campaign_path(CID, camp)
        op.create.shared_set = shared_rn
        ops.append(op)
        print(f"    + {camp}: ATTACH CSMS_Negatives")
    if ops and apply:
        r = css_service.mutate_campaign_shared_sets(customer_id=CID, operations=ops)
        print(f"    -> attached {len(r.results)}")

    # ---------- 2. campaign-level negatives ----------
    print("\n[2] campaign-level negatives (gaps CSMS_Negatives does not cover)")
    existing = lib.run_query(CID, """
        SELECT campaign.id, campaign_criterion.keyword.text
        FROM campaign_criterion
        WHERE campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'
    """)
    have = {(r["campaign"]["id"], r["campaign_criterion"]["keyword"]["text"].lower())
            for r in existing if isinstance(existing, list)}

    cc_service = client.get_service("CampaignCriterionService")
    ops, planned = [], []
    for camp in NONBRANDED:
        terms = OWN_BRAND + MISSING_COMPETITORS + CROSS_SERVICE[camp]
        for t in terms:
            if (camp, t.lower()) in have:
                continue
            op = client.get_type("CampaignCriterionOperation")
            c = op.create
            c.campaign = ga.campaign_path(CID, camp)
            c.negative = True
            c.keyword.text = t
            c.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            ops.append(op)
            planned.append((camp, t))
    for camp in NONBRANDED:
        ts = [t for c, t in planned if c == camp]
        print(f"    {camp}: +{len(ts)} phrase negatives -> {ts}")
    if ops and apply:
        for i in range(0, len(ops), 500):
            r = cc_service.mutate_campaign_criteria(customer_id=CID, operations=ops[i:i+500])
            print(f"    -> added {len(r.results)}")

    # ---------- 3. budgets ----------
    print("\n[3] step-1 budgets")
    budget_service = client.get_service("CampaignBudgetService")
    ops = []
    for camp, (old, new, label) in BUDGETS.items():
        rows = lib.run_query(CID, f"""
            SELECT campaign.campaign_budget, campaign_budget.amount_micros,
                   campaign_budget.reference_count
            FROM campaign WHERE campaign.id = {camp}
        """)
        rn = rows[0]["campaign"]["campaign_budget"]
        cur = float(rows[0]["campaign_budget"]["amount_micros"]) / 1e6
        refs = rows[0]["campaign_budget"]["reference_count"]
        assert int(refs) == 1, f"budget {rn} shared by {refs} campaigns - aborting"
        print(f"    {label} ({camp}): ${cur:.2f} -> ${new:.2f}/day  [budget refs={refs}]")
        op = client.get_type("CampaignBudgetOperation")
        op.update.resource_name = rn
        op.update.amount_micros = int(new * 1_000_000)
        op.update_mask.paths.append("amount_micros")
        ops.append(op)
    print(f"    Search Nonbranded Plumbing ({SEARCH_PLUMBING}): $60.00 unchanged (deliberate)")
    if apply:
        r = budget_service.mutate_campaign_budgets(customer_id=CID, operations=ops)
        print(f"    -> updated {len(r.results)} budgets")

    # ---------- 4. enable HVAC search ----------
    print("\n[4] enable Search Nonbranded HVAC")
    camp_service = client.get_service("CampaignService")
    op = client.get_type("CampaignOperation")
    op.update.resource_name = ga.campaign_path(CID, SEARCH_HVAC)
    op.update.status = client.enums.CampaignStatusEnum.ENABLED
    op.update_mask.paths.append("status")
    print(f"    {SEARCH_HVAC} TSD_05.14_Leads_Search_Nonbranded_HVAC: PAUSED -> ENABLED")
    if apply:
        r = camp_service.mutate_campaigns(customer_id=CID, operations=[op])
        print(f"    -> {r.results[0].resource_name}")

    print(f"\n=== {tag} complete ===")
    if not apply:
        print("Nothing was written. Re-run with --apply.")


if __name__ == "__main__":
    main()
