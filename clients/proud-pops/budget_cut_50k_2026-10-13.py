#!/usr/bin/env python3
"""
Proud Pops, Google Ads (Edu OK 2026-10-13): bring October back to the approved $50k/month. Account 1051843378.
  Oct 1-13 spent ~$26.2k at ~$2,000/d (caps $1,960/d = the Aug catch-up rate, never rolled back).
  $50k leaves ~$23.8k for Oct 14-31 (18 days) -> ~$1,285/d caps incl. YouTube.
  Cuts, worst real cost per customer form first (30d Sep 8-Oct 7 + post-fix Oct 8-12):
    PMax HVAC        23853595615  $295 -> $50   ($4,904/form 30d, 99% Display, 0 forms post-fix; full pause waits on P-2)
    PMax Electrical  23866982084  $230 -> $75   ($2,296/form 30d, 0 forms post-fix, 184 taps)
    Search HVAC      23848895678  $375 -> $300  ($929/form 30d, 0 forms on $2.7k post-fix, 0% budget-lost)
    Search Electrical 23866999121 $600 -> $500  ($1,094/form 30d, $533 post-fix; Aug 17 raise was for the pool gap)
  Untouched: Branded $100, Plumbing $160. YouTube San Antonio ($100/d) = UI only (API blocks VIDEO mutations).
Asserts each budget is non-shared and still at its expected 'before' value. Plain micros.
Default validate-only; --apply writes; read-back after.
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "1051843378"
# campaign id: (expected before, new) in dollars/day
CHANGES = {
    "23853595615": (295, 50),    # PMax HVAC
    "23866982084": (230, 75),    # PMax Electrical
    "23848895678": (375, 300),   # Search HVAC
    "23866999121": (600, 500),   # Search Electrical
}
client = init_client()


def budgets():
    ids = ", ".join(CHANGES)
    return {r["campaign"]["id"]: r for r in run_query(CID, f"""SELECT campaign.id, campaign.name, campaign_budget.resource_name,
campaign_budget.amount_micros, campaign_budget.reference_count, campaign_budget.explicitly_shared FROM campaign WHERE campaign.id IN ({ids})""")}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    before = budgets()
    assert set(before) == set(CHANGES), f"missing campaigns: {set(CHANGES) - set(before)}"
    ops = []
    for cid, (old, new) in CHANGES.items():
        r = before[cid]; b = r["campaign_budget"]; cur = int(b["amount_micros"]) / 1e6
        print(f"   {r['campaign']['name'][:45]:45s} ${cur:.0f} -> ${new}  refs={b.get('reference_count')} shared={b.get('explicitly_shared', False)}")
        assert int(b.get("reference_count", 0)) == 1 and not b.get("explicitly_shared", False), "budget is shared, STOP"
        assert cur == old, f"budget drifted: expected ${old}, found ${cur:.2f}, STOP"
        o = client.get_type("MutateOperation"); u = o.campaign_budget_operation.update
        u.resource_name = b["resource_name"]; u.amount_micros = new * 1_000_000
        o.campaign_budget_operation.update_mask.paths.append("amount_micros"); ops.append(o)
    print(f"   these 4: ${sum(o for o, _ in CHANGES.values())} -> ${sum(n for _, n in CHANGES.values())}/day")
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = not a.apply
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("APPLIED" if a.apply else "VALIDATE-ONLY OK") + f" ({len(ops)} ops)")
    if a.apply:
        after = budgets()
        for cid, (_, new) in CHANGES.items():
            got = int(after[cid]["campaign_budget"]["amount_micros"]) / 1e6
            print(f"   READ-BACK {after[cid]['campaign']['name'][:45]:45s} ${got:.2f}/day " + ("OK" if got == new else "MISMATCH"))


if __name__ == "__main__":
    main()
