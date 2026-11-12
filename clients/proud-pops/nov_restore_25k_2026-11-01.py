#!/usr/bin/env python3
"""
Proud Pops, Google Ads: Nov 1 restore to the client's new $25k/month (cut announced 2026-10-14). Account 1051843378.
  Oct 15-31 ran Branded only (branded_only_25k_2026-10-14.py). Run this ON Nov 1 (CT), not before, or Oct takes the spend.
  Caps $800/d. Google's monthly charge limit = daily x 30.4 -> $24,320 max for these 4, + LSA ~$600/mo (3 surfaces,
  demand-limited) = ~$24.9k. Max Conversions overspends single days; the month still caps at 30.4x.
  Default split (STAGED 10-14, re-check against fu-048 CallRail data before running):
    Branded           23853361615  $100 -> $120  ENABLED stays  (cheapest customer form ~$302, 13-21% lost to budget)
    Search Electrical 23866999121  $500 -> $340  enable         (best nonbranded, ~$480-500/form Oct 8-14)
    Search HVAC       23848895678  $300 -> $210  enable         (heating season; 0 forms Oct 8-14 on $3.6k, watch it)
    Search Plumbing   23853484024  $160 -> $130  enable         (Max Clicks, $45 CPC cap since 10-08)
  Stay PAUSED: PMax HVAC ($4,904/form, 99% Display), PMax Electrical ($2,296/form), both YouTube (0 leads).
  If CallRail shows a PMax campaign drives real calls, fund it out of Search HVAC first and keep the total at $800.
Asserts each campaign's status + budget still match the expected 'before'. Plain micros.
Default validate-only; --apply writes; read-back after.
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "1051843378"
# campaign id: (label, expected status before, expected budget before, new budget) in dollars/day
CHANGES = {
    "23853361615": ("Branded", "ENABLED", 100, 120),
    "23866999121": ("Search Electrical", "PAUSED", 500, 340),
    "23848895678": ("Search HVAC", "PAUSED", 300, 210),
    "23853484024": ("Search Plumbing", "PAUSED", 160, 130),
}
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
    for cid, (label, st, old, new) in CHANGES.items():
        r = before[cid]; b = r["campaign_budget"]; cur = int(b["amount_micros"]) / 1e6
        print(f"   {label:18s} {r['campaign']['status']} ${cur:.0f} -> ENABLED ${new}  refs={b.get('reference_count')} shared={b.get('explicitly_shared', False)}")
        assert int(b.get("reference_count", 0)) == 1 and not b.get("explicitly_shared", False), "budget is shared, STOP"
        assert r["campaign"]["status"] == st, f"{label} is {r['campaign']['status']}, expected {st}, STOP"
        assert cur == old, f"{label} budget drifted: expected ${old}, found ${cur:.2f}, STOP"
        o = client.get_type("MutateOperation"); u = o.campaign_budget_operation.update
        u.resource_name = b["resource_name"]; u.amount_micros = new * 1_000_000
        o.campaign_budget_operation.update_mask.paths.append("amount_micros"); ops.append(o)
        if st != "ENABLED":
            o = client.get_type("MutateOperation"); u = o.campaign_operation.update
            u.resource_name = f"customers/{CID}/campaigns/{cid}"; u.status = client.enums.CampaignStatusEnum.ENABLED
            o.campaign_operation.update_mask.paths.append("status"); ops.append(o)
    print(f"   total caps ${sum(c[3] for c in CHANGES.values())}/day (x30.4 = ${sum(c[3] for c in CHANGES.values()) * 30.4:,.0f} max)")
    req = client.get_type("MutateGoogleAdsRequest"); req.customer_id = CID; req.mutate_operations.extend(ops); req.validate_only = not a.apply
    client.get_service("GoogleAdsService").mutate(request=req)
    print(("APPLIED" if a.apply else "VALIDATE-ONLY OK") + f" ({len(ops)} ops)")
    if a.apply:
        after = state()
        for cid, (label, _, _, new) in CHANGES.items():
            got = int(after[cid]["campaign_budget"]["amount_micros"]) / 1e6; s = after[cid]["campaign"]["status"]
            print(f"   READ-BACK {label:18s} {s} ${got:.2f}/day " + ("OK" if got == new and s == "ENABLED" else "MISMATCH"))


if __name__ == "__main__":
    main()
