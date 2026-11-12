# APPLIED LIVE 2026-11-09 (Edu: "good to move that budget"), read-back OK on both. Do NOT re-run with --apply.
#!/usr/bin/env python3
"""
Proud Pops (1051843378), Google Ads: move unspent Branded budget to Nonbranded Electrical. Edu's go 2026-11-09 ("good to move that budget").
    Branded           23853361615  $130 -> $50
    Search Electrical 23866999121  $375 -> $455
  Total Search caps stay $880/day (constant total, no client approval needed).
  Why: Branded on Target IS spends $1-20/day of $130 (brand volume is small); Electrical is the only nonbranded campaign with real
  leads (8 at $214, 11-04..11-08) and loses 38% of its impressions to budget.
  Rollback = Branded $130, Electrical $375.
Asserts status + budget still match the expected 'before' and that neither budget is shared. Plain micros.
Default validate-only; --apply writes; read-back after.
Run from google-ads-ratos/scripts: ./tsd.sh <abs path> [--apply]
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "1051843378"
# campaign id: (label, expected budget before, new budget) in dollars/day
CHANGES = {
    "23853361615": ("Branded", 130, 50),
    "23866999121": ("Search Electrical", 375, 455),
}
assert sum(c[1] for c in CHANGES.values()) == sum(c[2] for c in CHANGES.values()), "total must not change"
client = init_client()


def state():
    ids = ", ".join(CHANGES)
    return {r["campaign"]["id"]: r for r in run_query(CID, f"""SELECT campaign.id, campaign.name, campaign.status, campaign_budget.resource_name,
campaign_budget.amount_micros, campaign_budget.reference_count, campaign_budget.explicitly_shared FROM campaign WHERE campaign.id IN ({ids})""")}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    before = state()
    assert set(before) == set(CHANGES), f"missing campaigns: {set(CHANGES) - set(before)}"
    ops = []
    for cid, (label, old, new) in CHANGES.items():
        r = before[cid]; b = r["campaign_budget"]; cur = int(b["amount_micros"]) / 1e6
        print(f"   {label:18s} {r['campaign']['name']} | {r['campaign']['status']} ${cur:.0f} -> ${new}  refs={b.get('reference_count')} shared={b.get('explicitly_shared', False)}")
        assert int(b.get("reference_count", 0)) == 1 and not b.get("explicitly_shared", False), "budget is shared, STOP"
        assert r["campaign"]["status"] == "ENABLED", f"{label} is {r['campaign']['status']}, expected ENABLED, STOP"
        assert cur == old, f"{label} budget drifted: expected ${old}, found ${cur:.2f}, STOP"
        o = client.get_type("MutateOperation"); u = o.campaign_budget_operation.update
        u.resource_name = b["resource_name"]; u.amount_micros = new * 1_000_000
        o.campaign_budget_operation.update_mask.paths.append("amount_micros"); ops.append(o)
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = not a.apply
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("APPLIED" if a.apply else "VALIDATE-ONLY OK") + f" ({len(ops)} ops)")
    if a.apply:
        after = state()
        for cid, (label, _, new) in CHANGES.items():
            got = int(after[cid]["campaign_budget"]["amount_micros"]) / 1e6; s = after[cid]["campaign"]["status"]
            print(f"   READ-BACK {label:18s} {s} ${got:.2f}/day " + ("OK" if got == new and s == "ENABLED" else "MISMATCH"))


if __name__ == "__main__":
    main()
