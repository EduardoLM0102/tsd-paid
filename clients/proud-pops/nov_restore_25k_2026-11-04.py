# APPLIED LIVE 2026-11-04 (Edu: "Let's bring them back to 25k/mo"), read-back OK on all 4. Do NOT re-run with --apply.
#!/usr/bin/env python3
"""
Proud Pops, Google Ads: November restore to the client's $25k/month, run LATE on 2026-11-04 (Edu: "Let's bring them back to 25k/mo").
  Copy of nov_restore_25k_2026-11-01.py with caps scaled ~10% because Nov 1-3 ran Branded only ($362 spent).
  Math: $25,000 - $362 = $24,638 over Nov 4-30 (27 days) = ~$912/d total; LSA (3 surfaces) runs ~$31/d -> Search caps ~$880/d.
    Branded           23853361615  $100 -> $130  ENABLED stays
    Search Electrical 23866999121  $500 -> $375  enable
    Search HVAC       23848895678  $300 -> $230  enable
    Search Plumbing   23853484024  $160 -> $145  enable
  PMax HVAC/Electrical + both YouTube stay PAUSED. CallRail (11-04) can't judge PMax (paused the whole data window).
  Recheck pacing fu-054 (~11-11): land $24-25k; trim Search HVAC/Electrical if > ~$950/d average.
Asserts each campaign's status + budget still match the expected 'before'. Plain micros.
Default validate-only; --apply writes; read-back after.
"""
import sys, os, argparse
sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/topserv-workspace/.claude/skills/google-ads-ratos/scripts"))
from lib import init_client, run_query
CID = "1051843378"
# campaign id: (label, expected status before, expected budget before, new budget) in dollars/day
CHANGES = {
    "23853361615": ("Branded", "ENABLED", 100, 130),
    "23866999121": ("Search Electrical", "PAUSED", 500, 375),
    "23848895678": ("Search HVAC", "PAUSED", 300, 230),
    "23853484024": ("Search Plumbing", "PAUSED", 160, 145),
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
